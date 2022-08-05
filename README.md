# *Backend-NFT-API*

## *Technology: FastAPI*

### *1. Project folder structure*

```
.
├── app
│   ├── core
│   │   ├── config.py
│   │   └── __init__.py
│   ├── .env
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── item.py
│   ├── offline_extractor.py
│   ├── routers
│   │   ├── __init__.py
│   │   └── item.py
│   ├── service
│   │   ├── api_handle.py
│   │   ├── feature_extractor.py
│   │   ├── file_handle.py
│   │   ├── image_upload_handle.py
│   │   ├── __init__.py
│   │   ├── model_results_processing.py
│   │   └── retrieval
│   │       └── crawler
│   │           ├── collection_info_crawler.py
│   │           ├── crawler_file_handle.py
│   │           ├── crawler_process.py
│   │           ├── item_extractor.py
│   │           ├── item_info_crawler.py
│   │           └── url_modify.py
│   ├── static
│   │   ├── Data
│   │   └── uploaded
│   ├── temp
│   │   └── Crawler
│   │       └── Data
│   └── test_main.http
├── auto_scrawl.sh
├── docker-compose.yml
├── Dockerfile
├── .dockerignore
├── .github
│   └── workflows
│       └── github-action-cicd-pipeline.yml
├── .gitignore
├── README.md
└── requirements.txt
```

### *2. Prerequisite*
- [x] Python3 (3.8.10)
- [x] Pip (22.0.4)
- [x] Install all necessary python packages:
- [x] Download initial image database from url: https://files.fm/f/bxpquhnmv

  `pip install -r requirements.txt`
- [x] Unzip the static.zip file which is downloaded above and replace the database folder (static) by unzipping static folder that was extracted and run:
  

  `cd app`

### *3. How to run*

- Run app command:

  `uvicorn main:app --reload --port=9090`

- Docker repository: [ NFT-Backend-API-Image ](https://hub.docker.com/r/anhgrew/nft-backend-api)
- Open static folder with terminal and use docker command to start local server:

  `docker run --name nft-backend --restart=always -v $(pwd)/static:/app/static/ -p 9090:9090 -d anhgrew/nft-backend-api:latest`


- Local api server link: http://127.0.0.1:9090/docs


Run successfully:

![Screenshot from 2022-08-05 08-19-27](https://user-images.githubusercontent.com/47881661/182981397-909e3c97-e657-42c4-bd2b-7dd7fb195e76.png)



