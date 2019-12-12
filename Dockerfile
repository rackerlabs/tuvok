FROM python:3-alpine
LABEL maintainer="Rackspace"

ENV PATH="/root/.local/bin:${PATH}"

# Install packages/updates/dependencies
RUN apk --update add git openssh curl jq gcc build-base

ADD . /tuvok
WORKDIR /tuvok
RUN pip3 install --user -r test-requirements.txt
RUN pip3 install --user -r requirements.txt
RUN pip3 install --user -e .

WORKDIR /root
ENTRYPOINT [ "/bin/sh", "-c" ]
CMD [ "tuvok" ]
