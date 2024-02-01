from fastapi import FastAPI, Request, Depends
# from config.log_config import create_log
from injector import (logger, doc)
from repository.schemas import Item, Search
import json
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info
import asyncio

import repository.models
from repository.database import engine, metadata

from controller import (es_search_controller, 
                        # vector_search_controller, 
                        api_controller, 
                        task_controller, 
                        message_controller,
                        redis_controller,
                        # es_vector_controller
                        )
from basic import api_request_counter, api_request_summary
from service.Handler.message.rabbitmq_handler import RabbitMQApp

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


rabbitmq = RabbitMQApp()

@app.on_event('startup')
async def rabbitmq_event():
    logger.info('@@rabbitmq_event starting...@@')
    loop = asyncio.get_running_loop()
    task = loop.create_task(rabbitmq.pika_client.consume(loop))
    await task


@app.on_event("startup")
async def kafka_event():
    logger.info('@@kafka_event starting...@@')
    
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



# --
# Jinja2 template & filter call from html
# --
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")


'''
http://localhost:7000/v1/basic/11
https://fastapi.tiangolo.com/advanced/templates/
'''
from injector import templates
@app.get("/v1/basic/{id}")
def template_api(request: Request, id: str):
    logger.info("request : {}, id : {}".format(request, id))
    return templates.TemplateResponse("index.html", {"request": request, "id": id})



# router
app.include_router(es_search_controller.app, tags=["Search"], )
# app.include_router(es_vector_controller.app, tags=["ES Vector Search"], )
# app.include_router(vector_search_controller.app, tags=["FAISS"], )
app.include_router(api_controller.app, tags=["Note"], )
app.include_router(task_controller.app, tags=["Task"], )
app.include_router(message_controller.app, tags=["Message"], )
app.include_router(redis_controller.app, tags=["Redis"], )
