FROM python:3.8.15-bullseye

VOLUME /app
VOLUME /config
VOLUME /models

# Install coral dependencies \
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractiv apt-get install -yq \
    gasket-dkms \
    libedgetpu1-std \
    libedgetpu1-legacy-std \
    gstreamer-1.0 \
    gstreamer1.0-plugins-bad  \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    python3-gst-1.0  \
    python3-gi  \
    gir1.2-gtk-3.0 \
    python3-cairo  \
    python3-cairo-dev  \
    libcairo2-dev  \
    libglib2.0-dev \
    libgirepository1.0-dev  \
    python3-pycoral \
    x264  \
    libx264-dev \
    libavcodec-extra

WORKDIR /app

COPY . .

RUN python -m pip install -r requirements.txt

CMD [ "python", "-m", "edgetpu_server", "--model","efficientnet-edgetpu-L_quant.tflite", "--labels", "imagenet_labels.txt", "--videofmt", "h264", "--headless=true", "rtsp://192.168.1.175:7447/PlOYMITFLVdHYJrq ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert" ]