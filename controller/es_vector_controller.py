

from fastapi import APIRouter
from service.Handler.search.StatusHanlder import (StatusHanlder, 
                                                  StatusException
                                                  )
from injector import (logger, doc)
import json
import datetime


app = APIRouter(
    prefix="/es_vector",
)


ITEM_NOT_FOUND = "Item not found for id: {}"
ITEM_NOT_FOUND_ALL = "Item not found all"

"""
@app.get("/reloading", 
         status_code=StatusHanlder.HTTP_STATUS_200,
         description="Reload trained model", 
         summary="Reload trained model")
async def get_reload_model():
    ''' Saved model and call this api to reload '''
    return {'message' : "reloading"}
"""

@app.post("/search", 
          status_code=StatusHanlder.HTTP_STATUS_200, 
          description="Search using Elasticsearch v8.", 
          summary="Search using Elasticsearch v8.")
async def ES_Vector_Search(keyword: str = "Where is your office?"):
    try:
        logger.info("vector_search_controller : {}".format(json.dumps(keyword, indent=2)))
        return {"message": keyword}
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