
from fastapi import FastAPI
from service.Handler.message.Pika_Client import PikaClient
from injector import logger

class RabbitMQApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(logger, self.log_incoming_message)
        
    @classmethod
    def log_incoming_message(cls, message: dict):
        """Method to do something meaningful with the incoming message"""
        logger.info('Here we got incoming message : {}'.format(message))