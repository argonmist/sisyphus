#!/bin/bash

docker run --privileged -d -v $(pwd)/sisyphus:/root/sisyphus --net=host -e TZ="Asia/Taipei" -e LANG=C.UTF-8 --name android-dev argonhiisi/sisyphus:appium-1.22.3
