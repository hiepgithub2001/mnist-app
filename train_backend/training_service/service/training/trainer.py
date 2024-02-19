import importlib
import torch
from torchvision import datasets, transforms

import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
import torch.nn.functional as F
from dto.training_job_dto import ParamterDTO

from service.logging.log import RMQLogger
class Trainer:
    def __init__(self, job_id : int, user_code_encode : str, parameter : ParamterDTO):
        self.job_id = job_id
        self.user_code_encode = user_code_encode
        self.parmeter = parameter

    def load_model_from_code(self, user_mode_code):
        try:
            spec = importlib.util.spec_from_loader("model", loader=None)
            module = importlib.util.module_from_spec(spec)
            exec(user_mode_code, module.__dict__)
            return module.MNISTModel()
        except Exception as e:
            raise Exception(str(e))

    def train(self, args, model, device, train_loader, optimizer, epoch):
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()
            if batch_idx % args.log_interval == 0:
                RMQLogger.getInstance().log(self.job_id, 'Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                    100. * batch_idx / len(train_loader), loss.item()))
                if args.dry_run:
                    break

    def test(self, model, device, test_loader):
        model.eval()
        test_loss = 0
        correct = 0
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
                pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
                correct += pred.eq(target.view_as(pred)).sum().item()

        test_loss /= len(test_loader.dataset)

        RMQLogger.getInstance().log(self.job_id, '\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
            test_loss, correct, len(test_loader.dataset),
            100. * correct / len(test_loader.dataset)))

    def start(self, args, user_code):
        train_kwargs, test_kwargs, device = self.prepare_device_and_kwargs(args)

        try:
            model = self.load_model_from_code(user_code).to(device)

            transform=transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
                ])

            train_dataset = datasets.MNIST('../data', train=True, download=True,
                            transform=transform)
            test_dataset = datasets.MNIST('../data', train=False,
                            transform=transform)
            
            train_loader = torch.utils.data.DataLoader(train_dataset,**train_kwargs)
            test_loader = torch.utils.data.DataLoader(test_dataset, **test_kwargs)
            
            optimizer = optim.Adadelta(model.parameters(), lr=args.lr)

            scheduler = StepLR(optimizer, step_size=1, gamma=args.gamma)
            for epoch in range(1, args.epochs + 1):
                self.train(args, model, device, train_loader, optimizer, epoch)
                scheduler.step()
            self.test(model, device, test_loader)
        except Exception as exception:
            RMQLogger.getInstance().error(self.job_id, exception)

    def prepare_device_and_kwargs(self, args):
        train_kwargs = {'batch_size': args.batch_size}
        test_kwargs = {'batch_size': args.test_batch_size}
        
        use_cuda =  torch.cuda.is_available()
        use_mps = torch.backends.mps.is_available()

        if use_cuda:
            device = torch.device("cuda")
        elif use_mps:
            device = torch.device("mps")
        else:
            device = torch.device("cpu")

        if use_cuda:
                cuda_kwargs = {'num_workers': 1,
                            'pin_memory': True,
                            'shuffle': True}
                train_kwargs.update(cuda_kwargs)
                test_kwargs.update(cuda_kwargs)
        return train_kwargs,test_kwargs,device

    def train_model(self):
        self.start(self.parmeter, self.user_code_encode)