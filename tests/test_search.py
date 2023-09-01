

import pytest
import unittest
import mock
from tests.common.mock_service_clients import (MockSearchHandler, MockQueryHandler, SearchQuery, FullSearchQuery)
import json
import asyncio


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
        
        entire_payload = FullSearchQuery()
        # entire payload
        entire_oas_query = mock_query_handler.build_query(entire_payload)
        assert oas_query == entire_oas_query
       
       
class TestSearchBuilders(unittest.TestCase):
    
    def test_search_builder(self):
        mock_search_handler = MockSearchHandler()
        mock_query_handler = MockQueryHandler()
        request_oas_query = SearchQuery()
        
        assert mock_search_handler is not None
        assert mock_query_handler is not None
        assert request_oas_query is not None
        
        response = asyncio.run(mock_search_handler.search(mock_query_handler, request_oas_query))
        assert response is not None
        print(response)
        assert response['total']['value'] > 0