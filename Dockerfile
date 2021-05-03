FROM tensorflow/tensorflow:1.15.3-gpu-py3

ENV DEBIAN_FRONTEND noninteractive  # 入力待ちでブロックしなくなる
ENV TZ JST-9                        # タイムゾーンをJSTにする

RUN apt-get update && apt-get install python3-tk -y && \
    pip install --upgrade pip && pip install pillow