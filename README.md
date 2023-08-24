
### Python-Vector-Search Project based on Python-Fastapi

Install Poerty
```
https://python-poetry.org/docs/?ref=dylancastillo.co#installing-with-the-official-installer
```

Using Poetry: Create the virtual environment in the same directory as the project and install the dependencies:
```
poetry config virtualenvs.in-project true
poetry init
poetry add faiss-cpu
poetry add sentence-transformers
```

Using Poetry: Poetry install when buding the project initially
```
poetry install
```

Using venv and pip: Create a virtual environment and install the dependencies listed in requirements.txt:
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Poetry Enviroment
Install Poerty to Dockerfile as indexing_environment
```

```

Install Poerty to Dockerfile as runtime
```

```

## Docker build
![Alt text](image.png)

## Docker run
```
docker run --platform linux/amd64 -it -d \
  --name fn-vector-search-app \
  --network bridge \
  -e ES_HOST="http://host.docker.internal:9209" \
  -v "$SCRIPTDIR:/app/ES-Services/" \
  fn-vector-search-api:es \
```
