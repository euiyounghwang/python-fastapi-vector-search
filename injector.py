
from config.log_config import create_log
from service.Handler.search.SearchOmniHandler import (SearchOmniHandler)
from service.Handler.search.QueryBuilder import (QueryBuilder)
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
hosts = os.getenv("ES_HOST", doc['app']['es']['omni_es_host'])
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@{}:{}/postgres".format(doc['app']['mud']['host'],
                                                                                            doc['app']['mud']['port']
                                                                                            ))
RABBITMQ_HOST = os.getenv('RABBIT_HOST', doc['app']['rabbitmq']['host'])
print('@@RABBIT ', RABBITMQ_HOST)

es_client = Elasticsearch(hosts=hosts,
                          headers=get_headers(),
                          verify_certs=False,
                          timeout=600
)

SearchOmniHandlerInject = SearchOmniHandler(es_client, logger, doc['app'])
QueryBuilderInject = QueryBuilder(es_client, logger, doc['app'])
metrics_service = ES_Utils(logger, doc, es_client)