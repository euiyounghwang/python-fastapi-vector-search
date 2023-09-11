from fastapi import FastAPI, Request, Depends
# from config.log_config import create_log
from injector import (logger, doc)
from repository.schemas import Item, Search
import json
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info

import repository.models
from repository.database import engine, metadata

from controller import (es_search_controller, vector_search_controller, api_controller)
from basic import api_request_counter, api_request_summary

# --
# Add Tables
# --
# openapi.models.Base.metadata.drop_all(bind=engine)
repository.models.Base.metadata.create_all(engine)

# --
#  Create the FastAPI client.
# --


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
# prometheus_fastapi_instrumentator(metric_name="fastapi-app",).Instrumentator().instrument(app).expose(app)
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
app.include_router(es_search_controller.app, tags=["Search"], )
app.include_router(vector_search_controller.app, tags=["FAISS"], )
app.include_router(api_controller.app, tags=["Note"], )