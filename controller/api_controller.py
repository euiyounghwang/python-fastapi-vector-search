
from injector import (logger, doc, SearchOmniHandlerInject, QueryBuilderInject)
import json

async def api_controller(request):
    # logger.info("api_controller doc: {}".format(json.dumps(doc, indent=2)))
    request_json = {k : v for k, v in request}
    print(request, type(request), request.size, request_json)
    logger.info("api_controller : {}".format(json.dumps(request_json, indent=2)))
    
    return await SearchOmniHandlerInject.search(QueryBuilderInject, oas_query=request_json)