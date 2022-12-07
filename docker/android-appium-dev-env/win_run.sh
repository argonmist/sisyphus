#!/bin/bash

docker network create sisyphus-net
docker run --privileged -d -v %cd%\sisyphus:/root/sisyphus -e TZ="Asia/Taipei" -e LANG=C.UTF-8 -p 4723:4723 -p 8883:8883 --network=sisyphus-net --name android-dev argonhiisi/sisyphus:appium-1.22.3
docker exec --rm --privileged -v %cd%\sisyphus:/root/sisyphus -w/root/sisyphus/bin android-dev-run apt install -y dos2unix && dos2unix  -k -o sisyphus
