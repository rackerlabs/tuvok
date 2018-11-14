FROM python:3-alpine
LABEL maintainer="Rackspace"

ENV PATH="/root/.local/bin:${PATH}"

# Install packages/updates/dependencies
RUN wget -q https://github.com/kvz/json2hcl/releases/download/v0.0.6/json2hcl_v0.0.6_linux_amd64 -O /usr/local/bin/json2hcl && chmod +x /usr/local/bin/json2hcl
RUN apk --update add git openssh curl jq

ADD . /tuvok
WORKDIR /tuvok
RUN pip3 install --user -r test-requirements.txt -r requirements.txt -e .

WORKDIR /root
ENTRYPOINT [ "/bin/sh", "-c" ]
CMD [ "tuvok" ]
