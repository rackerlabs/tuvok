FROM amazonlinux:2.0.20180622.1
LABEL maintainer="Rackspace"

ENV APP_HOME /tuvok

# Install OS packages
RUN yum update -y && \
    yum install -y git python37 jq

# Install other tools (not packaged)
RUN curl -SsL https://github.com/kvz/json2hcl/releases/download/v0.0.6/json2hcl_v0.0.6_linux_amd64 \
  | tee /usr/local/bin/json2hcl > /dev/null && chmod 755 /usr/local/bin/json2hcl && json2hcl -version

RUN mkdir -p ${APP_HOME}
ADD . ${APP_HOME}

RUN cd ${APP_HOME} && pip3 install --user -r test-requirements.txt -e .

ENTRYPOINT [ "python3", "tuvok/tuvok/cli.py" ]
