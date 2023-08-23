
from injector import (logger, doc, SearchOmniHandlerInject)
import json

async def api_controller(item):
    # logger.info("api_controller doc: {}".format(json.dumps(doc, indent=2)))
    request_json = [{k : v} for k, v in item]
    print(item, type(item), item.process_id, request_json)
    logger.info("api_controller : {}".format(json.dumps(request_json, indent=2)))
    
    await SearchOmniHandlerInject.search()
    
    return request_json