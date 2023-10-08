
import json
import numpy as np

class QueryBuilder:
    # @inject(
    #     es_client=ElasticsearchConnection,
    # )
    def __init__(self, es_client, logger, config):
        self.es_client = es_client
        self.logger = logger
        self.es_query = {}
        self.must_clauses = []
        self.should_clauses = []
        self.filter_clauses = []
        self.query_string = ""  # ES query string
        self.highlight_clauses = {}
        self.config = config
        self.OMNI_INDEX_ALIAS = self.config["es"]["index"]["alias"]
        

    def build_sort(self, oas_query=None):
        '''  Builds the sort field format for elasticsearch '''
        order = oas_query.get("sort_order", "DESC")
        sort_field = oas_query.get("sort_field")

        ordered_date_sorts = [
            {
                # "start_date": {
                #     "order": oas_query.get("sort_order"),
                #     "missing": "_last"
                # },
                "title.keyword": {
                    "order": oas_query.get("sort_order"),
                    "missing": "_last"
                }
            }
        ]

        if not sort_field:
            return [{"_score": {"order": order}}] + ordered_date_sorts
        else:
            return [
                {sort_field: {"order": order, "missing": "_last"}},
                ordered_date_sorts[0]
            ]

    def transform_query_string(self, oas_query=None):
        # Base case for search, empty query string
        if not oas_query.get("query_string", ""):
            self.query_string = {"match_all": {}}
        else:
            self.query_string = {
                "query_string": {
                    # "fields": ['title^3', 'field2'],
                    "fields": ['*'],
                    "default_operator": "AND",
                    "analyzer": "standard",
                    "query": oas_query.get('query_string')
                }
            }

    def add_highlighting(self):
        self.highlight_clauses = {
            "highlight": {
                "order": "score",
                "pre_tags": [
                    "<b>"
                ],
                "post_tags": [
                    "</b>"
                ],
                "fields": {
                    "*": {
                        "number_of_fragments": 1,
                        "type": "plain",
                        "fragment_size": 150
                    }
                }
            }
        }

        self.es_query.update(self.highlight_clauses)

    def add_pagination(self, search_after=None):
        if search_after is not None:
            self.logger.warn('Not none for search after')
            self.es_query['search_after'] = search_after
        else:
            self.logger.warn('None for search after')

    def add_aggregations(self, oas_query=None):
        if oas_query.get("include_basic_aggs"):
            aggs_clauses = {
                "aggs": {
                    "bill_type": {
                        "terms": {
                            "field": "bill_type.keyword",
                            "size": 150000
                        }
                    }
                }
            }

            self.es_query.update(aggs_clauses)


    def build_query(self, oas_query=None, pit_id=None, search_after=None):
        if not oas_query:
            return {}

        # self.logger.info('QueryBuilder:oas_query_params - {}'.format(oas_query))

        self.transform_query_string(oas_query)
        self.must_clauses = [self.query_string]
        self.filter_clauses = [{
            "bool": {
                "must": []
            }
        }]
        self.es_query = {
            "track_total_hits": True,
            "sort": self.build_sort(oas_query),
            "query" : {
                "bool" : {
                    "must": self.must_clauses,
                    "should" : self.should_clauses,
                    "filter": self.filter_clauses
                }
            },
            "size" : oas_query.get("size", 1),
            "pit": {
                "keep_alive": "30m",
                "id": pit_id
            }
        }

        self.add_highlighting()
        self.add_pagination(search_after)
        self.add_aggregations(oas_query)

        # self.logger.info('QueryBuilder:oas_query_build - {}'.format(json.dumps(self.es_query, indent=2)))

        return self.es_query


class QueryVectorBuilder:
    # @inject(
    #     es_client=ElasticsearchConnection,
    # )
    def __init__(self, es_client, logger, config):
        self.es_client = es_client
        self.logger = logger
        self.es_query = {}
        self.must_clauses = []
        self.should_clauses = []
        self.filter_clauses = []
        self.query_string = ""  # ES query string
        self.highlight_clauses = {}
        self.config = config
        # self.OMNI_INDEX_ALIAS = self.config["es"]["index"]["alias"]
 
    def build_query(self, oas_query=None, pit_id=None, search_after=None):
        
        oas_query = np.array(oas_query).tolist()
                
        self.filter_clauses = [{
            "bool": {
                "must": []
            }
        }]
        
        self.es_query = {
            "track_total_hits": True,
            "_source": ["metadata", "text", "title"], 
            "query" : {
                "bool" : {
                    "must": self.must_clauses,
                    "should" : self.should_clauses,
                    "filter": self.filter_clauses
                }
            },
            "knn": {
                "field": "text_vector",
                "query_vector": oas_query,
                "k": 10,
                "num_candidates": 100
            },
            # "size" : oas_query.get("size", 1),
            "pit": {
                "keep_alive": "30m",
                "id": pit_id
            }
        }

        # self.add_highlighting()
        # self.add_pagination(search_after)
        # self.add_aggregations(oas_query)

        self.logger.info('QueryVectorBuilder:oas_query_build - {}'.format(json.dumps(self.es_query, indent=2)))

        return self.es_query

