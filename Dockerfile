FROM python:3-alpine
LABEL maintainer="Rackspace"

ENV APP_HOME /tuvok
ENV PATH="/root/.local/bin:${PATH}"

# Install packages/updates/dependencies
ADD https://github.com/kvz/json2hcl/releases/download/v0.0.6/json2hcl_v0.0.6_linux_amd64 /usr/local/bin/json2hcl
RUN chmod +x /usr/local/bin/json2hcl
RUN apk --update add bash git openssh curl py-pip jq && pip install --upgrade pip

RUN mkdir -p ${APP_HOME}
ADD . ${APP_HOME}
RUN cd ${APP_HOME} && pip3 install --user -r test-requirements.txt && pip3 install --user -r requirements.txt && pip3 install --user -e .

# just try to run tuvok, so we can be sure it is installed correctly
RUN tuvok --version
CMD [ "tuvok" ]
