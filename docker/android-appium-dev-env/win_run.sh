#!/bin/bash

docker network create sisyphus-net
docker run --privileged -d -v ~\sisyphus:/root/sisyphus -p 4723:4723 -p 8883:8883 --network=sisyphus-net --name android-dev argonhiisi/sisyphus:appium-1.22.3

#docker exec --rm --privileged -v ~\sisyphus:/root/sisyphus -w/root/sisyphus/features android-dev-run apt install -y dos2unix && dos2unix  -k -o *.sh
#docker exec --rm --privileged -v ~\sisyphus:/root/sisyphus -w/root/sisyphus/settings android-dev-run apt install -y dos2unix && dos2unix  -k -o *.sh
