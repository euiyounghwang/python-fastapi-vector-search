
from fastapi import APIRouter
from openapi.schemas import Item, Search, NoteSchema
from prometheus_client import Counter, Histogram
# from metrics_var import api_request_counter, api_request_summary
from basic import api_request_counter, api_request_summary
from injector import (logger, doc, SearchOmniHandlerInject, QueryBuilderInject)
import json

app = APIRouter(
    prefix="/v1/basic",
)


@app.post("/v1/basic/vector_search")
async def Vector_Search(request: NoteSchema):
    request_json = {k : v for k, v in request}
    print(request, type(request), request_json)
    logger.info("vector_search_controller : {}".format(json.dumps(request_json, indent=2)))
    return {"okay" : "1"}
