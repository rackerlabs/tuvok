FROM amazonlinux:2.0.20180622.1
LABEL maintainer="Rackspace"

ENV APP_HOME /tuvok

# Install OS packages
RUN yum update -y && \
    yum install -y git python37

RUN mkdir -p ${APP_HOME}
ADD . ${APP_HOME}

CMD ["/bin/bash"]

