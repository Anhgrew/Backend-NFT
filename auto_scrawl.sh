#! /bin/bash -x

MAX_ITEMS=2
SERVER="backend-api"
URL="http://127.0.0.1:9090/api/v1/crawl/amount"
response=$(curl -s -w "%{http_code}" $URL/$MAX_ITEMS)

http_code=$(echo "$response" | tail -n1 ) # get the last line


status_code=$(echo -n "$http_code" | grep -o -E '[0-9]+')

echo $status_code

if [ "${status_code}" -eq "200" ]
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

