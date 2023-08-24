
import pytest
from elasticsearch.client import Elasticsearch, IndicesClient
import json

    
def test_search_elasticsearch(mock_es_client):
    assert mock_es_client is not None

    es = mock_es_client

    # print(response)
    # assert response.status == 404

    response = es.get(index="test_omnisearch_v1", id=222)
    print(response)
    assert response is not None
    assert '_source' in response and response['_source']['title'] == 'Cryptocurrency Regulations Act 222'

    query = {
        "query": {
            "match": {
                "title": "Cryptocurrency"
            }
        }
    }

    # query_string
    # query = {
    #     "query": {
    #         "query_string": {
    #             "fields": ['title^3', 'field2'],
    #            "default_operator": "AND",
    #             "analyzer": "standard",
    #             "query": "Cryptocurrency"
    #         }
    #     }
    # }

    response = es.search(index="test_omnisearch_v1", body=query)
    assert response is not None
    assert response['hits']['total']['value'] > 0
    # print(response)
    # print("Got %d Hits:" % response['hits']['total']['value'])
    for hit in response['hits']['hits']:
        print(hit["_source"])
        assert hit["_source"] is not None


def test_api_es_search(mock_client):
    ''' API call '''
    assert mock_client is not None

    test_client = mock_client
    
    request_body = {
            "include_basic_aggs": True,
            "pit_id": "",
            "query_string": "Cryptocurrency",
            "size": 20,
            "sort_order": "DESC",
            "start_date": "2021 01-01 00:00:00"
     }
    response = test_client.post(
            '/v1/basic/search',
            # data=json.dumps(request_body),
            # content_type='application/json',
            json = request_body
    )
    assert response.status_code == 200
    response_json = response.json()

    print(json.dumps(response_json, indent=2))

    assert response_json['total']['value'] > 0
    assert 'hits' in response_json
        

