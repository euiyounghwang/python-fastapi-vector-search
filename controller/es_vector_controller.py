

from fastapi import APIRouter
from service.Handler.search.StatusHanlder import (StatusHanlder, 
                                                  StatusException
                                                  )
from injector import (logger, 
                      doc, 
                      es_client,
                      global_settings,
                      QueryVectorBuilderInject
                      )
from service.Handler.vector.ES_Vector_Builder import (ES_Chain_Vector_Builder,
                                                      ES_Simantic_Builder
                                                      )
import json
import datetime

ES_Vector = ES_Chain_Vector_Builder(logger, doc, global_settings)
ES_Index_Vector = ES_Simantic_Builder(es_client, logger, doc)

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

@app.post("/es_v_search", 
          status_code=StatusHanlder.HTTP_STATUS_200, 
          description="Search using Elasticsearch v8.", 
          summary="Search with Lanchain.ElasticVectorSearch using Elasticsearch v8.")
async def ES_Langchain_Vector_Search(keyword: str = "Where is your office?"):
    try:
        logger.info("langchain_vector_search_controller : {}".format(json.dumps(keyword, indent=2)))
        return await ES_Vector.build_search(keyword)
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
    
    
@app.post("/es_search", 
          status_code=StatusHanlder.HTTP_STATUS_200, 
          description="Search using Elasticsearch v8.", 
          summary="Search Sentence_Transformer_using Elasticsearch v8.")
async def ES_Vector_Search(keyword: str = "Where is your office?"):
    try:
        logger.info("es_vector_search_controller : {}".format(json.dumps(keyword, indent=2)))
        return await ES_Index_Vector.build_search(QueryVectorBuilderInject, keyword)
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