FROM mottosso/maya:2016sp1

MAINTAINER andresmweber@gmail.com

# Make mayapy the default Python
RUN echo alias hpython="\"/usr/autodesk/maya/bin/mayapy\"" >> ~/.bashrc && \
    echo alias hpip="\"mayapy -m pip\"" >> ~/.bashrc && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    mayapy get-pip.py

ADD . /Forge

# Needs to install Python2.7 for coveralls
RUN yum install -y zlib-devel openssl-devel sqlite-devel readline-devel && \
    wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz && \
    tar -xvf Python-2.7.13.tgz && \
    cd Python-2.7.13 && \
    ./configure --prefix=/usr/local --enable-shared --with-system-expat --with-system-ffi --enable-unicode=ucs4 && \
    make -s && \
    make altinstall -s && \
    export PATH="/usr/local/bin:$PATH"

# Setup environment
ENV MAYA_LOCATION=/usr/autodesk/maya/
ENV PATH=$MAYA_LOCATION/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/lib
# Workaround for "Segmentation fault (core dumped)"
# See https://forums.autodesk.com/t5/maya-general/render-crash-on-linux/m-p/5608552/highlight/true
ENV MAYA_DISABLE_CIP=1

# Install project and dependencies
RUN mayapy -m pip install -r /Forge/requirements.txt && \
    mayapy -m pip install /Forge[test] coverage && \
    chmod -x $(find /Forge/tests/ -name '*.py')

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python2.7 get-pip.py && \
    python2.7 -m pip install coveralls pyyaml

# Cleanup
WORKDIR /Forge

#ENTRYPOINT ["mayapy"]
#CMD ["app.py"]

ENTRYPOINT mayapy -m nose --with-coverage --cover-package=forge tests && \
           coveralls