#
# frc_rekt dockerfile
# gets dependencies installed for fast builds
#
# https://github.com/jaustinpage/frc_rekt
#

FROM ubuntu

RUN \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y ca-certificates && \
  apt-get install -y python3 && \
  apt-get install -y python3-venv python3-pip libenchant1c2a && \
  rm -rf /var/lib/apt/lists/*

ADD requirements.txt /root/requirements.txt

RUN \
  python3 -m venv ./env && \
  env/bin/python3 -m pip install --upgrade pip && \
  env/bin/python3 -m pip install -r /root/requirements.txt

ENV HOME /root

WORKDIR /root

CMD ["bash"]
