
import sys
import os
import pathlib
from pathlib import Path
# ROOT_PATH = pathlib.Path(__file__).parents[1]
# sys.path.append(os.path.join(ROOT_PATH, ''))
# sys.path.append(str(Path(__file__).parent.parent))

from langchain.document_loaders import BSHTMLLoader
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch

# from config import Paths, openai_api_key
from dataclasses import dataclass
import json
import datetime
from elasticsearch.client import Elasticsearch, IndicesClient
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from elasticsearch.helpers import bulk

# from ...config.log_config import create_log

# logger = create_log()
MAX_BYTES = 102400

@dataclass
class Paths:
    root: Path = Path(__file__).parent
    data: Path = root / "data"
    book: Path = (
        data
        / "Marcus_Aurelius_Antoninus_-_His_Meditations_concerning_himselfe/index.html"
    )

def get_headers():
    ''' Elasticsearch Header '''
    return {'Content-type': 'application/json', 'Connection': 'close'}

def get_es_instance(url="http://localhost:9209"):
    es_client = Elasticsearch(hosts=url,
                          headers=get_headers(),
                          verify_certs=False,
                          timeout=600
    )
    return es_client

def management_index(es, index_name):
    '''
    Create index for semantic search with delete api
    '''
    ic = es.indices
    def try_delete_index(index):
        try:
            if ic.exists(index):
                print('Delete index : {}'.format(index))
                ic.delete(index)
        except NotFoundError:
            pass
    try_delete_index(index_name)

    def create_index(index, def_file_name):
        from os.path import dirname
        # print(open(dirname(__file__) + def_file_name))
        with open(dirname(__file__) + def_file_name) as f:
            index_def = f.read()
        ic.create(index, index_def)
    create_index(index_name, "/mapping/semantic-search-mapping.json")
    print('created index : {}'.format(index_name))



def Get_Buffer_Length(docs):
    """
    :param docs:
    :return:
    """
    max_len = 0
    for doc in docs:
        max_len += len(str(doc))

    return max_len

# Compare this sentence_transformers with langchain vector
def build_vector_to_index(es, documents, index_name, embedding_type):
    '''
    title: doc.metadata['title']
    text : doc.page_content
    i.e)  page_content='Meditations\nMeditations\nMarcus Aurelius\n\n\n\nExported from Wikisource on February 8, 2023' metadata={'source': '/Users/euiyoung.hwang/ES/Python_Workspace/python-fastapi-vector-search/tools/semantic_search/data/Marcus_Aurelius_Antoninus_-_His_Meditations_concerning_himselfe/index.html', 
    'title': 'Meditations'}
    '''
    print(len(documents))
    actions = []
    trained_model = 'paraphrase-mpnet-base-v2'
    # trained_model = 'sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens'
    if embedding_type =='es_langchain':
        embeddings = HuggingFaceEmbeddings()
        # c_vector = embeddings.embed_query(doc.page_content)
        db = ElasticVectorSearch.from_documents(
                    documents,
                    embeddings,
                    elasticsearch_url="http://localhost:9209",
                    index_name=index_name,
                    # ssl_verify={
                    # "verify_certs": True,
                    # "basic_auth": ("elastic", "xxx"),
                    # "ca_certs": "./data/xxxx"
                    #  },
        )
        print(json.dumps(db.client.info(), indent=2))
        query = "What did the president say about Ketanji Brown Jackson"
        docs = db.similarity_search(query)
        print(docs)
        return
    
    elif embedding_type =='es_v':
        for i, doc in enumerate(documents):
            # print('doc : {}'.format(doc.page_content))
            c_vector = SentenceTransformer(trained_model).encode(doc.page_content)
            c_vector = np.array(c_vector)
            # _vector = np.array([search_vector])
            # print(i, c_vector)
            print(i, doc.metadata['title'])
            '''
            bulk (from elasticsearch.helpers import bulk)
            bulk(es, actions)
            actions.append(
                {
                    "_index": index_name,
                    "_id": i,
                    "_source": {        
                        "title": doc.metadata['title'],
                        "vector" : c_vector,
                        "metadata" : doc.metadata
                    }
                }
            )
            '''
            
            doc = {
                 "title": doc.metadata['title'],
                 "vector" : c_vector,
                 "metadata" : doc.metadata,
                 "text" : doc.page_content,
                 "text_vector" : c_vector,
            }
            actions.append({'index': {'_index': index_name}})
            actions.append(doc)
            
            if Get_Buffer_Length(actions) > MAX_BYTES:
                response = es.bulk(body=actions)
                # bulk(es, actions)
                print('Get_Buffer_Length(actions) > MAX_BYTES : Push into ES..')
                del actions[:]
                if response['errors']:
                    raise Exception(response)

        # --
        # Remains
        response = es.bulk(body=actions)
        # bulk(es, actions)
        print(json.dumps(es.info(), indent=2))
        print('Finshed & Push into ES..')
        del actions[:]
        # --
        
def main(es, index_name):
    """
    Vector search provides the foundation for implementing semantic search for text or similarity search for images, videos, or audio.
    Search based on meaning, not just matching keywords.
    """
    loader = BSHTMLLoader(str(Paths.book))
    data = loader.load()
    
    # data = [data[0]]
    
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    documents = text_splitter.split_documents(data)
    # print(len(documents))
    # documents = documents[:2]

    # embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    
    # --
    # Langchain with HuggingFaceEmbeddings
    '''
    embeddings = HuggingFaceEmbeddings()
    db = ElasticVectorSearch.from_documents(
        documents,
        embeddings,
        elasticsearch_url="http://localhost:9209",
        index_name=index_name,
    )
    print(json.dumps(db.client.info(), indent=2))
    '''
    # --
    
    # --
    # Sentence_transformer
    # build_vector_to_index(documents, index_name, embedding_type='es_langchain')
    build_vector_to_index(es, documents, index_name, embedding_type='es_v')
    # --
    

if __name__ == "__main__":
    StartTime, EndTime, Delay_Time = 0, 0, 0
    try:
        # --
        index_name = "elastic-index"
        # Create Index
        es = get_es_instance()
        management_index(es, index_name)
        # --
        StartTime = datetime.datetime.now()
        main(es, index_name)
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]
    except Exception as e:
        print(e)
    finally:
        print("Delay_Time : {}".format(Delay_Time))