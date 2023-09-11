
from fastapi import APIRouter
from repository.schemas import Item, Search
from prometheus_client import Counter, Histogram
from basic import api_request_counter, api_request_summary
from injector import (logger, doc, SearchOmniHandlerInject, QueryBuilderInject, metrics_service)
import json
import datetime

app = APIRouter(
    prefix="/es",
)

@app.post("/search", description="Search to ES", summary="Search to ES")
async def Elasticsearch_Search(request: Search):
    ''' Search to Elasticsearch '''
    StartTime, EndTime, Delay_Time = 0, 0, 0
    
    try:
        StartTime = datetime.datetime.now()
        api_request_counter.labels(method="POST", endpoint="/v1/basic/search", http_status=200).inc()
        api_request_summary.labels(method="POST", endpoint="/v1/basic/search").observe(0.1)
        
        # logger.info("api_controller doc: {}".format(json.dumps(doc, indent=2)))
        request_json = {k : v for k, v in request}
        print(request, type(request), request.size, request_json)
        logger.info("es_search_controller : {}".format(json.dumps(request_json, indent=2)))
        
        EndTime = datetime.datetime.now()

        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]
        
        return await SearchOmniHandlerInject.search(QueryBuilderInject, oas_query=request_json)
    
    finally:
        metrics_service.track_performance_metrics(Delay_Time)
