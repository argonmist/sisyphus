#!/bin/bash

docker run --privileged -d -v ~/sisyphus:/root/sisyphus --net=host --name android-dev argonhiisi/sisyphus:appium-1.22.3
