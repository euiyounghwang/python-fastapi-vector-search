
from dotenv import load_dotenv
import pika
import os

class PikaClient:

    def __init__(self, logger, process_callable):
        
        self.publish_queue_name = os.getenv('PUBLISH_QUEUE', 'foo_publish_queue')
        self.credentials = pika.PlainCredentials('guest', 'guest')
        # self.parameters = pika.URLParameters('amqp://euiyoung.hwang:1234@{}:25672'.format(str(os.getenv('RABBIT_HOST', '127.0.0.1'))))
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBIT_HOST', '127.0.0.1'), 
                                                                            port=5672, 
                                                                            credentials=self.credentials, 
                                                                            heartbeat=6000))
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable
        self.logger = logger
        self.logger.info('Pika connection initialized')