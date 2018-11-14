FROM python:3-alpine
LABEL maintainer="Rackspace"

ENV PATH="/root/.local/bin:${PATH}"
ENTRYPOINT [ "/bin/sh" ]

# Install packages/updates/dependencies
ADD https://github.com/kvz/json2hcl/releases/download/v0.0.6/json2hcl_v0.0.6_linux_amd64 /usr/local/bin/json2hcl
RUN chmod +x /usr/local/bin/json2hcl
RUN apk --update add git openssh curl jq && pip3 install --upgrade pip

ADD . ${WORKDIR}
RUN pip3 install --user -r test-requirements.txt && pip3 install --user -r requirements.txt && pip3 install --user -e .

# just try to run tuvok, so we can be sure it is installed correctly
RUN tuvok --version
CMD [ "tuvok" ]
