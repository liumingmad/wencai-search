FROM fnndsc/ubuntu-python3
MAINTAINER ming <liumingmad@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive

# install python require
# RUN python -m pip install --upgrade pip
WORKDIR /work
COPY ./requirements.txt /work
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
