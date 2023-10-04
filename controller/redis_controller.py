
from fastapi import APIRouter, Depends, HTTPException, Request
from service.Handler.search.StatusHanlder import (StatusHanlder, StatusException)
from injector import (logger, doc, Redis_Cache)
from service.Handler.message.redis_handler import Cache
from fastapi.responses import JSONResponse
from fastapi import status

app = APIRouter(
    # prefix="/redis",
    responses={404: {"description": "Page not found"}}
)

@app.get("/Redis", 
         status_code=StatusHanlder.HTTP_STATUS_200,
         description="Search all key & value from Redis", 
         summary="Search all key & value from Redis")
async def redis_get_keys():
    """
	rd = RedisHanlderInject
	rd.set("A", "B", ex=ttl) # set
	
	return {
	    "data": rd.get("A") # get
	}
    """
    try:
        all_datas = {}
        
        for k in Redis_Cache.get_keys_all():
            all_datas.update({k : Redis_Cache.get_key(k)})
            
        return {"data" : all_datas}
    except Exception as e:
        # raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ex.args})
        logger.error(e)
        """
        return JSONResponse(
            status_code=StatusHanlder.HTTP_STATUS_404,
            content={"code": StatusHanlder.HTTP_STATUS_404,"message": str(e)}
        )
        """
        return StatusException.raise_exception(e)
    
    
@app.post("/Redis", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          description="Set key & value to Redis", 
          summary="Set key & value to Redis")
async def redis_set_keys(key, value):
    try:
        Redis_Cache.set_key(key, value)
        return {"data" : Redis_Cache.get_key(key)}
    except Exception as ex:
        raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ex.args})