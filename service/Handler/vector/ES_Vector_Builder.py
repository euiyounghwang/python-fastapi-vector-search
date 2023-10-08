
from fastapi import FastAPI
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import ElasticVectorSearch
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceHub
import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import json
from elasticsearch import TransportError
import elasticsearch.exceptions

load_dotenv()

# https://teddylee777.github.io/langchain/langchain-tutorial-02/
# https://python.langchain.com/docs/integrations/llms/huggingface_hub
# os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'xx'


# A k-nearest neighbor (kNN) search finds the k nearest vectors to a query vector, as measured by a similarity metric.
class ES_Simantic_Builder:
    # @inject(
    #     es_client=ElasticsearchConnection,
    # )
    def __init__(self, es_client, logger, doc):
        self.es_client = es_client
        self.logger = logger
        self.doc = doc
        self.sentence_vector = SentenceTransformer('paraphrase-mpnet-base-v2')
        self.OMNI_INDEX_ALIAS = 'elastic-index'
        self.search_after = None

    async def build_search(self, query_builder, query, pit=None):
        self.logger.info('build_search : {}'.format(query))
        if not query:
            return
        query = self.sentence_vector.encode(query)
        self.logger.info('build_search to query with vector: {}'.format(query))
       
        if pit is None:
            resp = self.es_client.open_point_in_time(index=self.OMNI_INDEX_ALIAS, keep_alive='1m')
            pit_id = resp['id']
            self.search_after = None
        # else:
        #     pit_id = oas_query.get('pit_id')

        es_query = query_builder.build_query(query, pit_id, self.search_after)
        # self.logger.info('query_build_query:query - {}'.format(json.dumps(es_query, indent=2)))

        try:
            es_result = self.es_client.search(
                body=es_query,
            )
        # This is what Elasticserch throws as an exception if the point in time context has expired
        except elasticsearch.exceptions.NotFoundError as nfe:
            raise ContinuationTokenException(
                "Continuation token has expired. Please set the token to None/null and restart the pagination.")

        es_hits = es_result["hits"]
        results = [es_hit for es_hit in es_hits["hits"]]

        # self.search_after = results[int(len(results))-1]["sort"] if results else None
        # es_hits['pit'] = pit_id
        # es_hits['aggregations'] = es_result['aggregations']
       
        self.logger.info('response total : {}'.format(es_hits['total']['value']))
        return {
            "response": es_hits,
        }
        


class ES_Chain_Vector_Builder:
    # @inject(
    #     es_client=ElasticsearchConnection,
    # )
    def __init__(self, logger, doc, global_settings):
        self.logger = logger
        self.doc = doc
        self.embeddings = HuggingFaceEmbeddings()
        self.db = ElasticVectorSearch(
            elasticsearch_url=global_settings.get_Hosts(),
            index_name="elastic-index",
            embedding=self.embeddings,
        )
        self.qa = RetrievalQA.from_chain_type(
            # llm=ChatOpenAI(temperature=0),
            llm=HuggingFaceHub(repo_id="stabilityai/stablelm-tuned-alpha-3b", model_kwargs={"temperature":0.1, "max_new_tokens":250}),
            # chain_type="stuff",
            retriever=self.db.as_retriever(),
        )
        
    async def build_search(self, query):
        self.logger.info('build_search : {}'.format(query))
        response = self.qa.run(query)
        self.logger.info('response : {}'.format(response))
        return {
            "response": response,
        }
        