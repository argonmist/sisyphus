#!/bin/bash

docker run --privileged -d -p 6080:6080 -p 5554:5554 -p 5555:5555 -e DEVICE="Samsung Galaxy S6" -v  ./android:/root/.android -v ./android-emulator:/root/android_emulator --name android-container argonhiisi/docker-android:arm-enable
