#!/bin/bash

docker network create sisyphus-net
docker run --privileged -d -v %cd%\sisyphus:/root/sisyphus -e TZ="Asia/Taipei" -e LANG=C.UTF-8 -p 4723:4723 -p 8883:8883 --network=sisyphus-net --name android-dev argonhiisi/sisyphus:appium-1.22.3
docker exec android-dev dos2unix  -k -o bin/sisyphus.sh
