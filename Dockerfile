
FROM --platform=linux/amd64 python:3.9.0 as fta_environment
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app
ENV CONDA_NUMBER_CHANNEL_NOTICES=0

RUN wget https://repo.continuum.io/miniconda/Miniconda3-4.7.12.1-Linux-x86_64.sh
RUN bash Miniconda3-4.7.12.1-Linux-x86_64.sh -b -p conda

RUN conda/bin/conda install \
    # Install boto3 to use our S3 channel
    boto3
RUN echo 'conda ==4.7.12' > /app/conda/conda-meta/pinned

# COPY .condarc /root/.condarc
COPY requirements.txt deps/requirements.txt
COPY requirements-test.txt deps/requirements-test.txt
COPY environment_search.lst deps/environment_search.lst

# Create environment
# RUN --mount=type=cache,id=aws_config,dst=/original_credentials \
    # conda/bin/conda create --yes --quiet --name fn_fta_services python=3.9.0 --file deps/environment_search.lst && \
RUN conda/bin/conda create --yes --quiet --name fn_fta_services python=3.9.0 && \
    /bin/bash -c 'source /app/conda/bin/activate fn_fta_services && \
    /app/conda/bin/conda update -y setuptools && \
    /app/conda/bin/conda install -c conda-forge sentence-transformers=2.2.2 && \
    /app/conda/bin/conda install -c conda-forge faiss-cpu=1.7.4 && \
    pip install --upgrade pip && \
    PKG_VERSION=git pip install --no-deps -r deps/requirements.txt --ignore-installed && \
    PKG_VERSION=git pip install --no-deps -r deps/requirements-test.txt --ignore-installed'



# Create test image
FROM --platform=linux/amd64 python:3.9.0 as fta_test

# RUN mkdir -p /app
WORKDIR /app
COPY --from=fta_environment /app .
COPY . FN-FTA-Services

# RUN /bin/bash -c 'source /app/conda/bin/activate fn_fta_services'

RUN useradd deploy
# RUN chown -R deploy: /app/conda/envs/fn_fta_services /app/FN-FTA-Services

# RUN mkdir -p test-reports/junit/
RUN mkdir -p /FN-FTA-Services/test-reports/junit/

# Need these two lines to install VSCode extensions in devcontainer
RUN mkdir -p /home/deploy/
RUN chown -R deploy: /home/deploy

USER deploy

ENTRYPOINT ["/app/FN-FTA-Services/docker-run-tests.sh"]



# Create runtime image
FROM --platform=linux/amd64 python:3.9.0 as fta_runtime

WORKDIR /app
COPY --from=fta_environment /app .
COPY . FN-FTA-Services

RUN /bin/bash -c 'source /app/conda/bin/activate fn_fta_services'

RUN useradd deploy

#COPY config.yaml .fn_rabbit.json logging.yaml /app/FN-FTA-Services/
RUN chown -R deploy: /app/conda/envs/fn_fta_services /app/FN-FTA-Services

RUN mkdir -p /home/deploy/fn_services_logs && \
    chown -R deploy: /home/deploy/fn_services_logs/

# Need these two lines to install VSCode extensions in devcontainer
RUN mkdir -p /home/deploy/
RUN chown -R deploy: /home/deploy

USER deploy

ENTRYPOINT ["/app/FN-FTA-Services/docker-run-entrypoints.sh"]
EXPOSE 7000
