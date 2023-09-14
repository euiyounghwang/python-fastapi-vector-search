
from dotenv import load_dotenv
from injector import RABBITMQ_HOST
import pika
from aio_pika import connect, IncomingMessage
import os
import uuid
import json

class PikaClient:

    def __init__(self, logger, process_callable):
        # https://itracer.medium.com/rabbitmq-publisher-and-consumer-with-fastapi-175fe87aefe1
        self.publish_queue_name = os.getenv('PUBLISH_QUEUE', 'fastapi_publish_queue')
        self.credentials = pika.PlainCredentials('guest', 'guest')
        # self.parameters = pika.URLParameters('amqp://euiyoung.hwang:1234@{}:25672'.format(str(os.getenv('RABBIT_HOST', '127.0.0.1'))))
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, 
                                                                            port=5672, 
                                                                            credentials=self.credentials, 
                                                                            heartbeat=6000))
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable
        self.logger = logger
        self.logger.info('Pika connection initialized -> {}'.format(self.connection))
        
        
    def send_message(self, message: dict):
        """Method to publish message to RabbitMQ"""
        self.channel.basic_publish(
            exchange='',
            routing_key=self.publish_queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message)
        )

        
    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        self.logger.info('Established pika async listener')
        connection = await connect("amqp://guest:guest@{}:5672/".format(RABBITMQ_HOST), loop = loop)
        channel = await connection.channel()
        queue = await channel.declare_queue(os.getenv('PUBLISH_QUEUE', 'fastapi_publish_queue'))

        await queue.consume(self.process_incoming_message, no_ack=False)
        return connection
    
    
    async def process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        # message.ack()
        body = message.body
        self.logger.info('Received message')
        if body:
            self.process_callable(json.loads(body))
