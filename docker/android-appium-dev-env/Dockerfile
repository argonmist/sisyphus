From appium/appium:v1.22.3-p1

RUN apt-get -qqy update && \
    apt dist-upgrade -y && \
    apt-get -qqy --no-install-recommends install \
    curl \
    vim \
    python3.7 \
    python3-pip \
    python3-setuptools \
    tesseract-ocr \
    zip \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /root/sisyphus

RUN update-alternatives --install /usr/bin/python3 python /usr/bin/python3.7 1 && \
    python3.7 -m pip install --upgrade pip

ADD allure-2.18.1/ /opt/allure-2.18.1/

RUN ln -s /opt/allure-2.18.1/bin/allure /usr/bin/allure && \
    pip3 install Appium-Python-Client --upgrade selenium \
    loguru \
    behave \
    airium \
    allure-behave \
    Pillow \
    pytesseract \
    opencv-python

EXPOSE 8883
WORKDIR /root/sisyphus
