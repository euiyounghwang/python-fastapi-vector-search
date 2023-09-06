from fastapi import FastAPI, Request
# from config.log_config import create_log
from injector import (logger, doc)
from openapi.api_model import Item, Search
from controller.api_controller import (api_controller)
import json
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator.metrics import Info
# from openapi.db import engine, metadata, database
from openapi.db import engine, metadata

metadata.create_all(engine)

# https://github.com/KenMwaura1/Fast-Api-Grafana-Starter/blob/main/src/app/db.py

app = FastAPI()
# instrumentator = Instrumentator(
#     should_group_status_codes=False,
#     should_ignore_untemplated=True,
#     should_respect_env_var=True,
#     should_instrument_requests_inprogress=True,
#     excluded_handlers=[".*admin.*", "/metrics"],
#     env_var_name="ENABLE_METRICS",
#     inprogress_name="inprogress",
#     inprogress_labels=True,
# )
Instrumentator().instrument(app).expose(app)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["DELETE", "GET", "POST", "PUT"],
#     allow_headers=["*"],
# )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define a counter metric
REQUESTS_COUNT = Counter(
    "requests_total", "Total number of requests", ["method", "endpoint", "status_code"]
)
# Define a histogram metric
REQUESTS_TIME = Histogram("requests_time", "Request processing time", ["method", "endpoint"])
api_request_summary = Histogram("api_request_summary", "Request processing time", ["method", "endpoint"])
api_request_counter = Counter("api_request_counter", "Request processing time", ["method", "endpoint", "http_status"])

@app.get("/v1/basic")
# async def root():
def api():
    return {"message": "Hello World"}


@app.get("/v1/basic/api/{id}")
def get(id:str):
    api_request_counter.labels(method="GET", endpoint="/v1/basic/api/{id}", http_status=200).inc()
    api_request_summary.labels(method="GET", endpoint="/v1/basic/api/{id}").observe(0.1)
    return {"message": "Hello your id {}".format(id)}


@app.post("/v1/basic/search")
async def Elasticsearch_Search(request: Search):
    api_request_counter.labels(method="POST", endpoint="/v1/basic/search", http_status=200).inc()
    api_request_summary.labels(method="POST", endpoint="/v1/basic/search").observe(0.1)
    response_json = await api_controller(request)
    return response_json


@app.post("/v1/basic/vector_search")
async def Vector_Search(item: Item):
    response_json = await api_controller(item)
    return response_json