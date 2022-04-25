FROM fnndsc/ubuntu-python3
MAINTAINER ming <liumingmad@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y nodejs cron rsyslog vim

# timezone
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# RUN python -m pip install --upgrade pip
WORKDIR /work
COPY ./ /work
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
