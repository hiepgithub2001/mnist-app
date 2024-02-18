from pydantic import BaseModel

class HyperParametersDTO(BaseModel):
    batch_size: int = 10
    test_batch_size: int = 10
    epochs: int = 1
    lr: float = 0.01
    gamma: float = 0.5
    no_cuda: bool = False
    no_mps: bool = False
    seed: int = 1
    log_interval: int = 10
    save_model: bool = False
    dry_run: bool = False
    drop_out: float = 0.1

    def tojson(self):
        return {
            "batch_size" : self.batch_size,
            "test_batch_size" : self.test_batch_size,
            "epochs" : self.epochs,
            "lr": self.lr,
            "gamma": self.gamma,
            "no_cuda" : self.no_cuda,
            "no_mps" : self.no_mps,
            "seed" : self.seed,
            "log_interval" : self.log_interval,
            "save_model" : self.save_model,
            "dry_run" : self.dry_run,
            "drop_out" :  self.drop_out,
        }


    
class SubmitParamter(BaseModel):
    model_id : int
    hyper_param : HyperParametersDTO