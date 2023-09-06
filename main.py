from fastapi import FastAPI, Request, Depends
# from config.log_config import create_log
from injector import (logger, doc)
from openapi.schemas import Item, Search
import json
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info
# from openapi.db import engine, metadata, database
from openapi.models import engine, metadata, Base
from controller import (es_search_controller, vector_search_controller)
from basic import api_request_counter, api_request_summary

# --
# Add Tables
# --
Base.metadata.create_all(engine)

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



@app.get("/v1/basic")
# async def root():
def api():
    return {"message": "Hello World"}


@app.get("/v1/basic/api/{id}")
def get(id:str):
    api_request_counter.labels(method="GET", endpoint="/v1/basic/api/{id}", http_status=200).inc()
    api_request_summary.labels(method="GET", endpoint="/v1/basic/api/{id}").observe(0.1)
    return {"message": "Hello your id {}".format(id)}


# router
app.include_router(es_search_controller.app, tags=["search"], )
app.include_router(vector_search_controller.app, tags=["vector_search"], )