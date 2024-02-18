import pika
import logging
import json

class RMQLogger:
    _instance = None

    def __new__(cls, connection: pika.BlockingConnection, channel: pika.channel.Channel, queue_name: str):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.connection = connection
            cls._instance.channel = channel
            cls._instance.queue_name = queue_name
            cls._instance.log_stack = {}
            cls._instance.log_batch_index = {}
        return cls._instance

    @staticmethod
    def createInstance(connection: pika.BlockingConnection, channel: pika.channel.Channel, queue_name: str):
        RMQLogger._instance = RMQLogger(connection, channel, queue_name)
        return RMQLogger._instance


    @staticmethod
    def getInstance():
        if RMQLogger._instance is None:
            raise Exception("Require to call createInstance before use")
        return RMQLogger._instance

    def log(self, id : str, message: str):
        logging.info(msg=f'[parameter_id {id}] ' + message)
        if (self.log_stack.get(id) is None) :
            self.log_stack[id] = []

        self.log_stack[id].append(message)

        if len(self.log_stack[id]) >= 10:
            self.flush_buffer(id)

    def error(self,id : str, e : Exception) :
        logging.info(msg=f'[parameter_id {id}] ' + str(e))

        if (self.log_stack.get(id) is None) :
            self.log_stack[id] = []

        self.log_stack[id].append(str(e))
        self.flush_buffer()

    def flush_buffer(self, id):
        if self.log_stack:
            log_content = '\n'.join(self.log_stack[id])
            log_batch_index = self.get_batch_index(id)
            message = {
                'id' : id,
                'content' : log_content,
                'batch' : log_batch_index
            }
            self.channel.basic_publish(
                exchange='training', 
                routing_key=self.queue_name, 
                body=json.dumps(message)
            )
            logging.info(f'Logs parameter_id {id} published to RabbitMQ')
            self.log_stack[id].clear()
            self.update_batch_index(id)
    
    def get_batch_index(self, id):
        if self.log_batch_index.get(id) is None:
            self.log_batch_index[id] = 0;
            return 0
        else:
            return self.log_batch_index.get(id)
        
    def update_batch_index(self, id):
        if self.log_batch_index.get(id) is None:
            self.log_batch_index[id] = 0;
        
        self.log_batch_index[id] += 1