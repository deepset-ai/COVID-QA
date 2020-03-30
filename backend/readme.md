# Overview
We run two services in the backend: elasticsearch + the model API. 
The model API is configured via environment variables that can be passed into the docker container or set in backend/config.py

# Run elasticsearch
a) Fresh elasticsearch index:

         docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.5.1
   Then ingest data via `data_ingestion.py`
   
b) Dev: 

        docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" deepset/covid-qa-elastic

 This image has already some docs indexed, so you can skip `data_ingestion.py`



# Run model API 
     docker image build -t deepset/covid-qa-haystack .
     docker run --net=host -e TEXT_FIELD_NAME=answer -e SEARCH_FIELD_NAME=question -e EXCLUDE_META_DATA_FIELDS='["question_emb"]' deepset/covid-qa-haystack:latest

or without docker:

    pip install -r requirements.txt
    uvicorn backend.api:app

# Alternative: Run both via docker-compose 
     docker-compose up
Edit `docker-compose.yml`, if you want to configure elasticsearch host, models etc.
    
