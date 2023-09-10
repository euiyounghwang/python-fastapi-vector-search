
import pandas as pd
import numpy as np
import json
import faiss
from injector import (logger, doc)
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
        
    
    async def reloading_model(self):
        pass
    
    
    async def train_model(self):
        pass
    
    async def train_model(self):
        pass
    
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
        
       
        
        
