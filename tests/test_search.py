

import pytest
import unittest
import mock
from tests.common.mock_service_clients import (MockSearchHandler, MockQueryHandler, SearchQuery)
import json


class TestQueryBuilders(unittest.TestCase):
    
     def test_query_builder(self):
        
        mock_query_handler = MockQueryHandler()
        request_oas_query = SearchQuery()
        
        assert mock_query_handler is not None
        assert request_oas_query is not None
        
        oas_query = mock_query_handler.build_query(request_oas_query)
        assert oas_query is not None
        print(oas_query)
        assert oas_query['query'] ==  {
            "bool":{
                "must":[
                    {
                    "query_string":{
                        "fields":[
                            "*"
                        ],
                        "default_operator":"AND",
                        "analyzer":"standard",
                        "query":"Cryptocurrency"
                    }
                    }
                ],
                "should":[
                    
                ],
                "filter":[
                    {
                    "bool":{
                        "must":[
                            
                        ]
                    }
                    }
                ]
            }
        }