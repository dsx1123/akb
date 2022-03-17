FROM debian:latest
# Install required packages and remove the apt packages cache when done
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y \
        git \
        python3 \
        python3-pip \
        wget \
        && \
    apt-get clean && \
    rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

#RUN echo [global] > /etc/pip.conf
#RUN echo proxy=http://proxy.esl.cisco.com:80/ >> /etc/pip.conf
#RUN echo extra-index-url = https://engci-maven.cisco.com/artifactory/api/pypi/yang-suite-dev-pypi/simple >> /etc/pip.conf
RUN wget -nc -O - https://releases.hashicorp.com/terraform/1.1.7/terraform_1.1.7_linux_amd64.zip  |  gunzip - >/usr/local/bin/terraform && chmod +x /usr/local/bin/terraform
RUN git clone https://github.com/camrossi/akb.git /opt/nkt &&  python3 -m pip install -r /opt/nkt/requirements.txt
WORKDIR /opt/nkt/terraform
ENTRYPOINT ["python3", "appflask.py"]
