
import pytest

def test_api(mock_client):
    response = mock_client.get("/v1/basic")
    assert response is not None
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
    
def test_CRUD_api(mock_client):
    sample_payload = {
        "title": "test_title",
        "description": "test_decription",
        "completed": "False"
    }
    
    # Create Item
    response = mock_client.post("/Note", json=sample_payload)
    assert response.status_code == 200
    assert response.json() == {
            "message ": "OK - Successful Query executed",
            "uuid": response.json()['uuid']
    }
    print(response.json()['uuid'])
    uuid = str(response.json()['uuid'])
       
    # Get Item
    response = mock_client.get("/Note/{}".format(uuid))
    assert response.status_code == 200
     
    # Delete Item
    response = mock_client.delete("/Note/{}".format(uuid))
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Item: {} was deleted successfully'.format(uuid)
    }
    
    