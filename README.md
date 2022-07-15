# *Backend-NFT-API*

## *Technology: FastAPI*

### *1. Project folder structure*

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── item.py
│   ├── offline_extractor.py
│   ├── routers
│   │   ├── __init__.py
│   │   └── item.py
│   ├── service
│   │   ├── api_handle.py
│   │   ├── feature_extractor.py
│   │   ├── file_handle.py
│   │   ├── image_upload_handle.py
│   │   ├── __init__.py
│   │   ├── model_results_processing.py
│   │   └── retrieval
│   │       └── crawler
│   │           ├── collection_info_crawler.py
│   │           ├── crawler_file_handle.py
│   │           ├── crawler_process.py
│   │           ├── item_extractor.py
│   │           ├── item_info_crawler.py
│   │           └── url_modify.py
│   ├── static
│   │   ├── Data   
│   │   ├── DataAddress.csv
│   │   └── uploaded
│   └── test_main.http
├── auto_scrawl.sh
├── Dockerfile
└── requirements.txt
```

### *2. Prerequisite*
- [x] Python3 (3.8.10)
- [x] Pip (22.0.4)
- [x] Install all necessary python packages:


  `pip install -r requirements.txt`
- [x] Put all images into the database folder (Data) and run the extract feature:

  `cd app && python3 offline_extractor.py`

### *3. How to run*

- Run app command:

  `uvicorn  main:app --reload`

- Docker repository: [ NFT-Backend-API-Image ](https://hub.docker.com/r/anhgrew/nft-backend)
- Open static folder with terminal and use docker command to start local server:

  `docker run --name tmp --restart=always -v $(pwd)/static:/app/static/ -v $(pwd)/static/feature:/app/static/feature  -p 9090:9090 -d anhgrew/nft-backend:V2`


- Local api server link: http://127.0.0.1:8000/docs or http://127.0.0.1:9090/docs (Run with docker command)


Run successfully:
---


![Screenshot from 2022-05-03 13-56-35](https://user-images.githubusercontent.com/47881661/166416130-ac9b7758-92c3-46a8-994c-fe26197b137e.png)
