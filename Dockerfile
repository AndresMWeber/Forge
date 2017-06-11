FROM mottosso/maya:2016sp1

MAINTAINER andresmweber@gmail.com

# Need to enable execution rights on all test files just in case
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    mayapy get-pip.py && \
    mayapy -m pip install -r /Forge/requirements.txt && \
    chmod -x $(find /Forge/tests/ -name '*.py')

WORKDIR /Forge

ENTRYPOINT mayapy -m nose --with-coverage --cover-package=forge tests