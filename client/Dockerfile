FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y \
    git \
    make \
    gcc \
    g++ \
    liblzma-dev \
    opencl-headers \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

RUN git clone https://github.com/hashcat/hashcat.git && \
    cd hashcat && \
    git checkout tags/v6.2.6 && \
    make install_library && make install

ENV HC_LIB_DIR=/usr/local/lib
ENV HC_SOURCES_DIR=/build/hashcat

RUN git clone https://github.com/michael2to3/pyhashcat.git && \
    cd pyhashcat/ && \
    python setup.py build_ext -I /usr/include/lzma/

FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    liblzma-dev \
    ocl-icd-libopencl1 \
    ocl-icd-opencl-dev \
    clinfo \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Install base OpenCL driver"

WORKDIR /app

COPY --from=builder /build/pyhashcat/ /app/pyhashcat
COPY --from=builder /build/hashcat/ /app/hashcat
COPY --from=builder /usr/local/lib /usr/local/lib
COPY --from=builder /usr/local/bin/hashcat /usr/local/bin/hashcat
COPY . /app/

ENV HC_LIB_DIR=/usr/local/lib
ENV HC_SOURCES_DIR=/app/hashcat
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}

RUN ln -s /app/hashcat/OpenCL /usr/local/bin/OpenCL
RUN ln -s /app/hashcat /usr/local/share/hashcat
RUN ln -s /app/hashcat/modules /usr/local/bin/modules

RUN cd /app/pyhashcat && python setup.py install
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY opencl.sh /tmp/opencl.sh
RUN chmod +x /tmp/opencl.sh && /tmp/opencl.sh

ENV PATH="/usr/local/bin:${PATH}"
