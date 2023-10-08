
import json
from elasticsearch import TransportError
import elasticsearch.exceptions

class SearchOmniHandler(object):
    
    def __init__(self, es_client, logger, config):
        self.es_client = es_client
        self.logger = logger
        self.config = config
        self.OMNI_INDEX_ALIAS = self.config["es"]["index"]["alias"]
        self.search_after = None
        
        
    async def search(self, query_builder, oas_query=None):
        ''' Search with QuerBuilder '''
        if not oas_query:
            oas_query = {}

        if not oas_query.get('pit_id'):
            resp = self.es_client.open_point_in_time(index=self.OMNI_INDEX_ALIAS, keep_alive='1m')
            pit_id = resp['id']
            self.search_after = None
        else:
            pit_id = oas_query.get('pit_id')

        es_query = query_builder.build_query(oas_query, pit_id, self.search_after)
        self.logger.info('query_builder_build_query:oas_query - {}'.format(json.dumps(es_query, indent=2)))

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

        self.search_after = results[int(len(results))-1]["sort"] if results else None
        es_hits['pit'] = pit_id
        es_hits['aggregations'] = es_result['aggregations']

        return es_hits