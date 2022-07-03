#! /bin/bash -x

MAX_ITEMS=2
SERVER="backend-api"

URL="http://13.215.156.162:9090/api/v1/crawl/amount"

response=$(curl -s -w "%{http_code}" $URL/$MAX_ITEMS)

http_code=$(tail -n1 <<<"$response") # get the last line

status_code=$(echo -n "$http_code" | grep -o -E '[0-9]+')

if [[ "${status_code}" == 20* ]]
then
    echo "Craw successfully with status code ${status_code} !!!"
    sleep 10
    echo "Restarting backend api server ..."
    docker restart $SERVER
    echo "Restarting backend api server successfully !!!"
    echo ">>>> Crawling data successfully <<<<"
else
    echo "Craw failed with status code ${status_code} !!!"
fi

