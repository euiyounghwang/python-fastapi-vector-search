
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
''' conda create --yes --quiet --name fastapi_service python==3.9 '''
''' conda install -c conda-forge sentence-transformers '''
''' conda install -c conda-forge faiss-cpu '''
''' pip list --format=freeze > requirements.txt '''


class V_FAISS(object):
    
    def __init__(self):
        self.data = [
            ['Where are your headquarters located?', 'location'],
            ['Throw my cellphone in the water', 'random'],
            ['Network Access Control?', 'networking'],
            ['Address', 'location']
        ]
        self.df = self.inital_data_loading()
        
        
    def inital_data_loading(self):
        df = pd.DataFrame(self.data, columns = ['text', 'category'])
        return df
        
        
    async def get_text_df(self):
        return self.df
    
    
    async def create_vector(self, search):
        search_vector = encoder.encode(search)
        _vector = np.array([search_vector])
        faiss.normalize_L2(_vector)
        logger.info("create_vector's keyword : {}, vectors : {}".format(text, _vector))
        
    
    async def train_vector(self):
        text = self.df['text']
        encoder = SentenceTransformer("paraphrase-mpnet-base-v2")
        vectors = encoder.encode(text)
        logger.info("create_vector's keyword : {}, vectors : {}".format(text, vectors))
        