
from fastapi import APIRouter, HTTPException
from openapi.schemas import Item, Search, NoteSchema
from prometheus_client import Counter, Histogram
# from metrics_var import api_request_counter, api_request_summary
from basic import api_request_counter, api_request_summary
from injector import (logger, doc, SearchOmniHandlerInject, QueryBuilderInject, es_client, metrics_service)
from openapi.vector_model import (V_FAISS, V_FAISS_Example)
# from controller.Util.es_utils import ES_Utils
from controller.Handler.StatusHanlder import StatusHanlder
import json
import datetime

app = APIRouter(
    prefix="/model",
)

''' test FAISS model '''
v_model = V_FAISS_Example()
f_model = V_FAISS()

ITEM_NOT_FOUND = "Item not found for id: {}"
ITEM_NOT_FOUND_ALL = "Item not found all"

@app.get("/reloading", 
         status_code=StatusHanlder.HTTP_STATUS_200,
         description="Reload trained model", 
         summary="Reload trained model")
async def get_reload_model():
    ''' Saved model and call this api to reload '''
    return {'message' : "reloading"}


@app.get("/train", 
         status_code=StatusHanlder.HTTP_STATUS_200,
         description="Train the model", 
         summary="Train the model")
async def build_train_model():
    ''' Train and Save the model '''
    status_code = await f_model.train_model()
    if not status_code:
        raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ITEM_NOT_FOUND_ALL})
        
    return {'message' : "build_train_model"}


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
    StartTime, EndTime, Delay_Time = 0, 0, 0
    try:
        StartTime = datetime.datetime.now()
    
        logger.info("vector_search_controller : {}".format(json.dumps(keyword, indent=2)))
        # logger.info(await v_model.get_text_df())
        ressult_dic = await f_model.search(keyword)
        
        EndTime = datetime.datetime.now()

        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]
        
        if not ressult_dic:
            raise HTTPException(status_code=StatusHanlder.HTTP_STATUS_404, detail={'message': ITEM_NOT_FOUND.format(keyword)})
    
        return ressult_dic
    finally:
        metrics_service.track_performance_metrics(Delay_Time)
