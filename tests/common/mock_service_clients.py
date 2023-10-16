
import pytest
from injector import (SearchOmniHandlerInject, QueryBuilderInject, Redis_Cache)


def SearchQuery():
    Request_Query = {
        "include_basic_aggs": True,
        "pit_id": "",
        "query_string": "Cryptocurrency",
        "size": 20,
        "sort_order": "DESC",
        "start_date": "2021 01-01 00:00:00"
    }
    return Request_Query

def FullSearchQuery():
    ''' entire paramters '''
    Request_Query = {
        "ids_filter": [
            "*"
        ], 
        "include_basic_aggs": True,
        "pit_id": "",
        "query_string": "Cryptocurrency",
        "size": 20,
        "sort_order": "DESC",
        "start_date": "2021 01-01 00:00:00"
    }
    return Request_Query
    

def MockSearchHandler():
    return SearchOmniHandlerInject

def MockQueryHandler():
    return QueryBuilderInject

def MockRedisHandler():
    return Redis_Cache
