FROM daemonecles/centos6-maya:2017

MAINTAINER andresmweber@gmail.com

ADD . /Forge

# Need to enable execution rights on all test files just in case
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    mayapy get-pip.py && \
    mayapy -m pip install -r /Forge/requirements.txt && \
    chmod -x $(find /Forge/tests/ -name '*.py')

WORKDIR /Forge

ENTRYPOINT mayapy -m nose --with-coverage --cover-package=forge /forge/tests