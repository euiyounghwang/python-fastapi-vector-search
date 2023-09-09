
### Python-Vector-Search Project based on Python-Fastapi
- We use Facebook AI Similarity Search (FAISS) to efficiently search for similar text (https://medium.com/loopio-tech/how-to-use-faiss-to-build-your-first-similarity-search-bf0f708aa772). Finding items that are similar is commonplace in many applications. Perhaps you want to find products in your store that match the description input by a customer. Or perhaps you want to find related keyword
- A vector or an embedding is a numerical representation of text data. For example, using an embedding framework, text like ‘name’ can be transformed into a numerical representation
- Semantic search consists of retrieving texts whose meaning matches a search query. For example, if your search query is “car,” the retrieved texts could include words such as “car,” “automobile,” “vehicle,” and so on. In contrast, keyword search only returns text passages with words of the search query.
- The results of a semantic search are the texts whose embeddings are most similar to the query's embedding (https://blog.dataiku.com/semantic-search-an-overlooked-nlp-superpower?ref=dylancastillo.co)
- Reference : https://pytest-with-eric.com/pytest-advanced/pytest-fastapi-testing/ 

### Environment
- <i>No module named 'sentence_transformers' based on Poetry and Python .Venv Environment</i>
- Try to make an enviroment on Conda and builder Docker & Docker-compose.yml

### Swagger for FAISS Model
- __<i>Support Similarity Search using FAISS Model from trained sample datasets</i>__
- <i>I'll try to make it to REST API Endpoint with building /train, /reloading the model and search</i>
![Alt text](image-3.png)

### Swagger for Elasticsearch
- __<i>Support Enterprise Search using Elasticsearch Docker Instance</i>__
![Alt text](image-4.png)

## Docker build
```
docker build \
  -f "$(dirname "$0")/Dockerfile" \
  -t fn-vector-search-api:es \
  --target build \
  "$(dirname "$0")/."
```
![Alt text](image.png)

## Docker run
```
docker run --rm --platform linux/amd64 -it -d \
  --name fn-vector-search-api --publish 7000:7000 --expose 7000 \
  --network bridge \
  -v "$SCRIPTDIR:/app/FN-BEES-Services/" \
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
![Alt text](image-1.png)


## FastAPI with Swagger UI
```
Willing to build FAISS (Facebook AI Similarity Search) with train model to search for similar text
Build Model/Schema with Postgres
Build Search with Elasticsearch
```

![Alt text](image-2.png)