
from config.log_config import create_log
from config import config
from service.Handler.search.SearchOmniHandler import (SearchOmniHandler)
from service.Handler.search.QueryBuilder import (QueryBuilder, QueryVectorBuilder)
from service.Handler.message.redis_handler import Cache
from elasticsearch import Elasticsearch
from service.Handler.util.es_utils import ES_Utils
from dotenv import load_dotenv
import yaml
import json
import os

def read_config_yaml():
    with open('./config.yaml', 'r') as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)
        
    logger.info(json.dumps(doc, indent=2))
    
    return doc

def get_headers():
    ''' Elasticsearch Header '''
    return {'Content-type': 'application/json', 'Connection': 'close'}


load_dotenv()
    
# Initialize & Inject with only one instance
logger = create_log()
doc = read_config_yaml()
# print(doc)

# Read_Doc with arguments from Docker -e option
"""
hosts = os.getenv("ES_HOST", doc['app']['es']['omni_es_host'])
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@{}:{}/postgres".format(doc['app']['mud']['host'],
                                                                                            doc['app']['mud']['port']
                                                                                            ))
RABBITMQ_HOST = os.getenv('RABBIT_HOST', doc['app']['rabbitmq']['host'])
"""

global_settings = config.Settings(logger, doc)
# --
# RabbitMQ
DATABASE_URL = global_settings.get_DATABASE_URL()
RABBITMQ_HOST = global_settings.get_RABBITMQ_HOST()
# --

# --
# Redis
RedisHanlderInject = global_settings.get_REDIS_HOST()
Redis_Cache = Cache(logger, doc, RedisHanlderInject)
# --

es_client = Elasticsearch(hosts=global_settings.get_Hosts(),
                          headers=get_headers(),
                          verify_certs=False,
                          timeout=600
)

SearchOmniHandlerInject = SearchOmniHandler(es_client, logger, doc['app'])
QueryBuilderInject = QueryBuilder(es_client, logger, doc['app'])
QueryVectorBuilderInject = QueryVectorBuilder(es_client, logger, doc['app'])
metrics_service = ES_Utils(logger, doc, es_client)


# --
# Jinja2 template & filter call from html
# --
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./template")

'''
https://abstractkitchen.com/blog/how-to-create-custom-jinja-filters-in-flask/
'''
from controller.Custome_jinja.filter import locale_code_to_name_filter
templates.env.filters['lc_name'] = locale_code_to_name_filter