FROM alpine:latest
# Install required packages and remove the apt packages cache when done
#ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /opt/
RUN echo $SOURCE_BRANCH
RUN apk update && \
    apk add \
        git \
        python3 \
        py3-pip \
        gzip \
        wget \
        libxml2-dev \
        libxslt-dev \
        python3-dev \
        libffi-dev \
        openssl-dev \
        py3-wheel \
        build-base

#RUN echo [global] > /etc/pip.conf
#RUN echo proxy=http://proxy.esl.cisco.com:80/ >> /etc/pip.conf
#RUN echo extra-index-url = https://engci-maven.cisco.com/artifactory/api/pypi/yang-suite-dev-pypi/simple >> /etc/pip.conf
RUN wget -nc -O - https://releases.hashicorp.com/terraform/1.1.7/terraform_1.1.7_linux_amd64.zip  |  gzip - >/usr/local/bin/terraform && chmod +x /usr/local/bin/terraform
RUN git clone --branch dev https://github.com/camrossi/akb.git  &&  python3 -m pip install -r /opt/akb/requirements.txt
WORKDIR /opt/nkt/terraform
ENTRYPOINT ["python3", "appflask.py"]
