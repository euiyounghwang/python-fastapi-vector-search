
from config.log_config import create_log
from controller.Handler.SearchOmniHandler import (SearchOmniHandler)
from elasticsearch import Elasticsearch
import yaml

def read_config_yaml():
    with open('./config.yaml', 'r') as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)
    
    return doc

def get_headers():
    ''' Elasticsearch Header '''
    return {'Content-type': 'application/json', 'Connection': 'close'}


    
# Initialize & Inject with only one instance
logger = create_log()
doc = read_config_yaml()
es_client = Elasticsearch(hosts=doc['app']['es']['omni_es_host'],
                          headers=get_headers(),
                          verify_certs=False,
                          timeout=600
)

SearchOmniHandlerInject = SearchOmniHandler(es_client, logger, doc['app'])

