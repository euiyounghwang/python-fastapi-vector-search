
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
