
### Python-Vector-Search Project based on Python-Fastapi
- We use Facebook AI Similarity Search (FAISS) to efficiently search for similar text (https://medium.com/loopio-tech/how-to-use-faiss-to-build-your-first-similarity-search-bf0f708aa772). Finding items that are similar is commonplace in many applications. Perhaps you want to find products in your store that match the description input by a customer. Or perhaps you want to find related keyword
- A vector or an embedding is a numerical representation of text data. For example, using an embedding framework, text like ‘name’ can be transformed into a numerical representation
- Semantic search consists of retrieving texts whose meaning matches a search query. For example, if your search query is “car,” the retrieved texts could include words such as “car,” “automobile,” “vehicle,” and so on. In contrast, keyword search only returns text passages with words of the search query.
- The results of a semantic search are the texts whose embeddings are most similar to the query's embedding (https://blog.dataiku.com/semantic-search-an-overlooked-nlp-superpower?ref=dylancastillo.co)
- Reference : https://pytest-with-eric.com/pytest-advanced/pytest-fastapi-testing/ 

### Install Tools
- Postgres
```
docker run --name postgres-local --network bridge -e POSTGRES_PASSWORD=1234 -p 15432:5432 -d postgres
```
- Elasticsearch/Kibana v8.
```
docker run --name kibaba-run --network bridge -e "ELASTICSEARCH_URL=http://host.docker.internal:9209" -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" -e "ELASTICSEARCH_HOSTS=http://host.docker.internal:9209" -p 5801:5601 docker.elastic.co/kibana/kibana:8.7.0
docker run --name es8-run --network bridge -p 9209:9200 -p 9114:9114 -p 9309:9300 -e "http.cors.enabled=true" -e "http.cors.allow-origin=\"*\"" -e "http.cors.allow-headers=X-Requested-With,X-Auth-Token,Content-Type,Content-Length,Authorization" -e "http.cors.allow-credentials=true" -e "xpack.security.enabled=false" -e "discovery.type=single-node" -e "ES_JAVA_OPTS=-Xms2g -Xmx2g" docker.elastic.co/elasticsearch/elasticsearch:8.7.0
```

### REST API Realtime Performance using Prometheus
![Alt text](screenshot/image-6.png)

### Flow

![Alt text](image.png)
- Controllers - Contains application logic and passing user input data to service
- Services - The middleware between controller and repository. Gather data from controller, performs validation and business logic, and calling repositories for data manipulation.
- Repositories - layer for interaction with models and performing DB operations
- Models - common laravel model files with relationships defined

### Environment
- <i>No module named 'sentence_transformers' based on Poetry on Python/.Venv Environment. So try to make an enviroment on Conda and builder Docker & Docker-compose.yml

### Swagger for FAISS Model
- __<i>Support Similarity Search using FAISS Model from trained sample datasets</i>__
- <i>I'll try to make it to REST API Endpoint with building /train, /reloading the model and search</i>

![Alt text](screenshot/image-3.png)

### Swagger for Elasticsearch
- __<i>Support Enterprise Search using Elasticsearch Docker Instance</i>__
![Alt text](screenshot/image-4.png)

## Docker build
```
docker build \
  -f "$(dirname "$0")/Dockerfile" \
  -t fn-vector-search-api:test \
  --target fta_test \
  "$(dirname "$0")/."

docker build \
  -f "$(dirname "$0")/Dockerfile" \
  -t fn-vector-search-api:es \
  --target runtime \
  "$(dirname "$0")/."
```
![Alt text](screenshot/image.png)

## Docker run
```
docker run --rm --platform linux/amd64 -it -d \
  --name fn-vector-search-api --publish 7001:7000 --expose 7000 \
  -e DATABASE_URL=postgresql://postgres:1234@host.docker.internal:15432/postgres \
  -e ES_HOST=http://host.docker.internal:9209 \
  --network bridge \
  -v "$SCRIPTDIR:/app/FN-FTA-Services/" \
  fn-vector-search-api:es
```

## services_start.sh for local env
```
#!/bin/bash
set -e

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $SCRIPTDIR
source .venv/bin/activate
uvicorn main:app --reload --port=7000 --workers 4
```
![Alt text](screenshot/image-1.png)


## FastAPI with Swagger UI
```
Willing to build FAISS (Facebook AI Similarity Search) with train model to search for similar text
Build Model/Schema with Postgres
Build Search with Elasticsearch
```

![Alt text](screenshot/image-5.png)