
from fastapi import APIRouter
from openapi.schemas import Item, Search
from prometheus_client import Counter, Histogram
from metrics_var import api_request_counter, api_request_summary
from controller.api_controller import (api_controller)


app = APIRouter(
    prefix="/v1/basic",
)

@app.post("/search")
async def Elasticsearch_Search(request: Search):
    api_request_counter.labels(method="POST", endpoint="/v1/basic/search", http_status=200).inc()
    api_request_summary.labels(method="POST", endpoint="/v1/basic/search").observe(0.1)
    response_json = await api_controller(request)
    return response_json
