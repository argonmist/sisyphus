#!/bin/bash

git clone https://github.com/budtmo/docker-android.git
cd docker-android
docker build --build-arg ANDROID_VERSION=11.0 --build-arg PROCESSOR=x86_64 --build-arg SYS_IMG=x86_64 --build-arg API_LEVEL=30 --build-arg IMG_TYPE=google_apis -f docker/Emulator_x86 -t argonhiisi/docker-android11:arm-enable .
