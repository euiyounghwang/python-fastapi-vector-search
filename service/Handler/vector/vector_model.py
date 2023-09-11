
import pandas as pd
import numpy as np
import json
import faiss
import pickle
from injector import (logger, doc)
from service.Handler.search.StatusHanlder import StatusHanlder
from sentence_transformers import SentenceTransformer
''' conda create --yes --quiet --name fastapi_service python==3.9 '''
''' conda install -c conda-forge sentence-transformers '''
''' conda install -c conda-forge faiss-cpu '''
''' pip list --format=freeze > requirements.txt '''


class V_FAISS(object):
    ''' build train model, load it and search in this class '''
    def __init__(self):
        self.data = [
            ['Where are your headquarters located?'],
            ['Throw my cellphone in the water'],
            ['Network Access Control?'],
            ['Address']
        ]
        self.df = pd.DataFrame(self.data, columns = ['text'])
        self.encoder = SentenceTransformer("paraphrase-mpnet-base-v2")
        self.model_path = './model/faiss_data_vector'
        self.model = None
        
        ''' search '''
        if not self.model:
            ''' reloading model after create trained model '''
            self.model = self.reloading_model()
            logger.info("@@@ reloading @@@@")
            
        
    def reloading_model(self):
        with open(self.model_path, 'rb') as f:
            data = pickle.load(f)
            return data
        
    def build_FAISS_index(self, vectors):
        vector_dimension = vectors.shape[1]
        index = faiss.IndexFlatL2(vector_dimension)
        faiss.normalize_L2(vectors)
        index.add(vectors)
        return index
    
    async def train_model(self):
        text = self.df['text']
        vectors = self.encoder.encode(text)
        # logger.info("train_vector's keyword : {}, vectors : {}".format(text, vectors))
        index = self.build_FAISS_index(vectors)
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(index, f, pickle.HIGHEST_PROTOCOL)
        logger.info("trained model finished ..")
        
        ''' reloading model after create trained model '''
        self.model = self.reloading_model()
        logger.info("trained model loading ..")
        
        return StatusHanlder.HTTP_STATUS_200
    
    async def search(self, search):
        ''' transforming to numerical representation for search text '''
        search_vector = self.encoder.encode(search)
        _vector = np.array([search_vector])
        faiss.normalize_L2(_vector)
        # logger.info("create_vector's keyword : {}, vectors : {}".format(search, _vector))
        
        k = self.model.ntotal
        distances, ann = self.model.search(_vector, k=k)
            
        ''' resulsts '''
        results = pd.DataFrame({'distances': distances[0], 'ann': ann[0]})
        logger.info("results : {}".format(results))
            
        ''' merge with meta datas '''
        df = pd.merge(results, self.df, left_on='ann', right_index=True)
        logger.info("merge : {}".format(df))
        
        return await self.df_transform_to_json(df)
        
    async def df_transform_to_json(self, df):
        ''' transforming to json from df '''
        list_dict = []
        for index, row in list(df.iterrows()):
            list_dict.append(dict(row))
        logger.info("list_dict : {}".format(json.dumps(list_dict, indent=2)))
        
        return list_dict


class V_FAISS_Example(object):
    
    def __init__(self):
        self.data = [
            ['Where are your headquarters located?', 'location'],
            ['Throw my cellphone in the water', 'random'],
            ['Network Access Control?', 'networking'],
            ['Address', 'location']
        ]
        self.df = self.inital_data_loading()
        self.encoder = SentenceTransformer("paraphrase-mpnet-base-v2")
        self.f_index = self.build_FAISS_index(self.train_vector())
        
        
    def inital_data_loading(self):
        df = pd.DataFrame(self.data, columns = ['text', 'category'])
        # df = pd.DataFrame(self.data, columns = ['text'])
        return df
        
        
    async def get_text_df(self):
        return self.df
    
    
    def train_vector(self):
        text = self.df['text']
        vectors = self.encoder.encode(text)
        logger.info("train_vector's keyword : {}, vectors : {}".format(text, vectors))
        return vectors
    
    
    def build_FAISS_index(self, vectors):
        vector_dimension = vectors.shape[1]
        index = faiss.IndexFlatL2(vector_dimension)
        faiss.normalize_L2(vectors)
        index.add(vectors)
        return index
            
    async def df_transform_to_json(self, df):
        ''' transforming to json from df '''
        list_dict = []
        for index, row in list(df.iterrows()):
            list_dict.append(dict(row))
        logger.info("list_dict : {}".format(json.dumps(list_dict, indent=2)))
        
        return list_dict

    async def search(self, search):
        ''' transforming to numerical representation for search text '''
        search_vector = self.encoder.encode(search)
        _vector = np.array([search_vector])
        faiss.normalize_L2(_vector)
        logger.info("create_vector's keyword : {}, vectors : {}".format(search, _vector))
        
        ''' search '''
        k = self.f_index.ntotal
        distances, ann = self.f_index.search(_vector, k=k)
        
        ''' resulsts '''
        results = pd.DataFrame({'distances': distances[0], 'ann': ann[0]})
        logger.info("results : {}".format(results))
        
        ''' merge with meta datas '''
        df = pd.merge(results, self.df, left_on='ann', right_index=True)
        logger.info("merge : {}".format(df))
        
        return await self. df_transform_to_json(df)
        
       
        
        
