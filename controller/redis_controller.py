
from fastapi import APIRouter, Depends, HTTPException, Request
from service.Handler.search.StatusHanlder import StatusHanlder
from injector import (logger, doc, Redis_Cache)
from service.Handler.message.redis_handler import Cache

app = APIRouter(
    # prefix="/redis",
    responses={404: {"description": "Page not found"}}
)

@app.get("/Redis", description="Search all key & value from Redis", summary="Search all key & value from Redis")
async def redis_get_keys():
    """
	rd = RedisHanlderInject
	rd.set("A", "B", ex=ttl) # set
	
	return {
	    "data": rd.get("A") # get
	}
    """
    all_datas = {}
    for k in Redis_Cache.get_keys_all():
        all_datas.update({k : Redis_Cache.get_key(k)})
        
    return {
        "data" : all_datas
    }
    
@app.post("/Redis", description="Set key & value to Redis", summary="Set key & value to Redis")
async def redis_set_keys(key, value):
    Redis_Cache.set_key(key, value)
    
    return {
        "data" : Redis_Cache.get_key(key)
    }