
from fastapi import APIRouter
from openapi.schemas import Item, Search, NoteSchema
from prometheus_client import Counter, Histogram
# from metrics_var import api_request_counter, api_request_summary
from basic import api_request_counter, api_request_summary
from injector import (logger, doc, SearchOmniHandlerInject, QueryBuilderInject)
from openapi.vector_model import (V_FAISS, V_FAISS_Example)
from controller.Handler.StatusHanlder import StatusHanlder
import json


app = APIRouter(
    prefix="/model",
)

''' test FAISS model '''
v_model = V_FAISS_Example()

ITEM_NOT_FOUND = "Item not found for id: {}"



@app.get("/reloading", 
         status_code=StatusHanlder.HTTP_STATUS_200,
         description="Reload trained model", 
         summary="Reload trained model")
async def get_reload_model():
    ''' Saved model and call this api to reload '''
    return {'message' : "reloading"}


@app.post("/search", 
          status_code=StatusHanlder.HTTP_STATUS_200, 
          description="Search using FAISS", 
          summary="Search using FAISS")
async def Vector_Search(keyword: str = "Where is your office?"):
    ''' 
    A vector or an embedding is a numerical representation of text data. 
    For example, using an embedding framework, text like ‘name’ can be transformed into a numerical representation like: 
    Normalization is the process of transforming numerical data so that it uses a common scale 
    '''
    logger.info("vector_search_controller : {}".format(json.dumps(keyword, indent=2)))
    logger.info(await v_model.get_text_df())
    ressult_dic = await v_model.create_vector(keyword)
    
    if not ressult_dic:
        raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ITEM_NOT_FOUND.format(keyword)})
    
    return ressult_dic
