import os
# from injector import (logger, doc)
import redis

class Settings:
    """
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: str = os.getenv("TESTING", "0")
    redis_url: AnyUrl = os.environ.get("REDIS_URL", "redis://redis")
    redis_password: str = os.getenv("REDIS_PASSWORD", "redis_pass")
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    redis_hash: str = os.getenv("REDIS_TEST_KEY", "covid-19-test")
    up: str = os.getenv("UP", "up")
    down: str = os.getenv("DOWN", "down")
    web_server: str = os.getenv("WEB_SERVER", "web_server")
    """
    def __init__(self, logger, doc):
        self.logger = logger
        self.doc = doc
        
        # Read_Doc with arguments from Docker -e option
        self.hosts: str = os.getenv("ES_HOST", doc['app']['es']['omni_es_host'])
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:1234@{}:{}/postgres".format
                                    (doc['app']['mud']['host'],
                                    doc['app']['mud']['port']
                                    ))
        self.RABBITMQ_HOST: str = os.getenv('RABBIT_HOST', doc['app']['rabbitmq']['host'])
        self.RADIS_HOST: str = redis.Redis(host=os.getenv("RADIS_HOST", doc['app']['redis']['host']), 
                                           port=os.getenv("RADIS_PORT", doc['app']['redis']['port']), 
                                           db=os.getenv("REDIS_DATABASE", doc['app']['redis']['db']),
                                        #    password='MTIzNA==',
                                           decode_responses=True
                                           )
        self.logger.info('@@RABBIT - {}'.format(self.RABBITMQ_HOST))
        self.logger.info('@@RADIS_HOST - {}'.format(self.RADIS_HOST))
        
    def get_Hosts(self):
        return self.hosts
    
    def get_DATABASE_URL(self):
        return self.DATABASE_URL
    
    def get_RABBITMQ_HOST(self):
        return self.RABBITMQ_HOST
    
    def get_REDIS_HOST(self):
        return self.RADIS_HOST
    
"""    
@lru_cache()
def get_settings():
    logger.info("Loading config settings from the environment...")
    return Settings()
"""
    
