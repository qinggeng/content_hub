db=content_db
app=content_app
port=8000
docker rm -f $db
docker rm -f $app
./mkmemdisk.sh
docker run -d -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=content_hub --name $db -v$(realpath memstore):/var/lib/mysql mysql --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
docker run -it -v $(realpath .):/usr/local/portal -p $port:$port --link $db --name $app python:2.7 /bin/bash
