FROM mottosso/maya:2016sp1

MAINTAINER andresmweber@gmail.com

# Make mayapy the default Python
RUN echo alias hpython="\"/usr/autodesk/maya/bin/mayapy\"" >> ~/.bashrc && \
    echo alias hpip="\"mayapy -m pip\"" >> ~/.bashrc

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN mayapy get-pip.py
RUN rm get-pip.py
ADD . /Forge
RUN /usr/autodesk/maya/bin/mayapy -m pip install -r /Forge/requirements.txt
RUN /usr/autodesk/maya/bin/mayapy -m pip install /Forge
RUN chmod -x $(find /Forge/tests/ -name '*.py')
#ENTRYPOINT ["mayapy"]
#CMD ["app.py"]

# Setup environment
ENV MAYA_LOCATION=/usr/autodesk/maya/
ENV PATH=$MAYA_LOCATION/bin:$PATH

# Workaround for "Segmentation fault (core dumped)"
# See https://forums.autodesk.com/t5/maya-general/render-crash-on-linux/m-p/5608552/highlight/true
ENV MAYA_DISABLE_CIP=1

# Cleanup
WORKDIR /Forge