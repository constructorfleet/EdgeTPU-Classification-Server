FROM 3.8.15-bullseye

VOLUME /app
VOLUME /config
VOLUME /models

# Install coral dependencies \
RUN DEBIAN_FRONTEND=noninteractive apt-get install -yq \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-good \
    python3-gst-1.0 python3-gi gir1.2-gtk-3.0 \
    python3-cairo python3-cairo-dev libglib2.0-dev \
    libgirepository1.0-dev libcairo2-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get install -yq \
    python3-pycoral

WORKDIR /app

COPY . .

RUN python -m pip install -r requirements.txt


CMD [ "python", "-m", "edgetpu_server", "--model","efficientnet-edgetpu-L_quant.tflite", "--labels", "imagenet_labels.txt", "--videofmt", "h264", "rtsp://192.168.1.175:7447/625hU4BGD4Txs6F2" ]