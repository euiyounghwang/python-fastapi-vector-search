

from fastapi import APIRouter, Depends, HTTPException, Request
from service.Handler.search.StatusHanlder import StatusHanlder
from repository.schemas import MessageSchema
from injector import (logger)
# from service.Handler.message.Pika_Client import PikaClient
from service.Handler.message.rabbitmq_handler import RabbitMQApp
import json
                      
app = APIRouter(
    # prefix="/api",
    responses={404: {"description": "Page not found"}}
)

# pika_client = PikaClient()
rabbitmq = RabbitMQApp()

@app.post('/send-message')
async def send_message(payload: MessageSchema, request: Request):
    # request_json = {k : v for k, v in request}
    logger.info(request)
    rabbitmq.pika_client.send_message(
        {"message": payload.message}
    )
    return {"status": "ok"}