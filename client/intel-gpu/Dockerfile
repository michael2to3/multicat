FROM ubuntu:22.04

ENV HASHCAT_VERSION        v6.2.6
ENV HASHCAT_UTILS_VERSION  v1.9
ENV HCXTOOLS_VERSION       6.2.7
ENV HCXDUMPTOOL_VERSION    6.2.7
ENV HCXKEYS_VERSION        master
ENV HC_LIB_DIR=/usr/local/lib
ENV HC_SOURCES_DIR=/app/hashcat
ENV HC_PATH=/app/hashcat
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}

WORKDIR /app

RUN apt-get update && apt-get install -y clinfo wget make clinfo build-essential git libcurl4-openssl-dev libssl-dev zlib1g-dev libcurl4-openssl-dev libssl-dev pkg-config pciutils python3.11 python3.11-dev && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3.11 get-pip.py && \
    apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/intel/intel-graphics-compiler/releases/download/igc-1.0.12812.24/intel-igc-core_1.0.12812.24_amd64.deb && \
    wget https://github.com/intel/intel-graphics-compiler/releases/download/igc-1.0.12812.24/intel-igc-opencl_1.0.12812.24_amd64.deb && \
    wget https://github.com/intel/compute-runtime/releases/download/22.49.25018.24/intel-level-zero-gpu-dbgsym_1.3.25018.24_amd64.ddeb && \
    wget https://github.com/intel/compute-runtime/releases/download/22.49.25018.24/intel-level-zero-gpu_1.3.25018.24_amd64.deb && \
    wget https://github.com/intel/compute-runtime/releases/download/22.49.25018.24/intel-opencl-icd-dbgsym_22.49.25018.24_amd64.ddeb && \
    wget https://github.com/intel/compute-runtime/releases/download/22.49.25018.24/intel-opencl-icd_22.49.25018.24_amd64.deb && \
    wget https://github.com/intel/compute-runtime/releases/download/22.49.25018.24/libigdgmm12_22.3.0_amd64.deb && \
    dpkg -i *.deb && rm *.deb && \
    update-pciids

RUN git clone https://github.com/hashcat/hashcat.git && cd hashcat && git checkout ${HASHCAT_VERSION} && make install_library && make install -j4 && \
    git clone https://github.com/hashcat/hashcat-utils.git && cd hashcat-utils/src && git checkout ${HASHCAT_UTILS_VERSION} && make && \
    ln -s /root/hashcat-utils/src/cap2hccapx.bin /usr/bin/cap2hccapx && \
    git clone https://github.com/ZerBea/hcxtools.git && cd hcxtools && git checkout ${HCXTOOLS_VERSION} && make install && \
    git clone https://github.com/ZerBea/hcxdumptool.git && cd hcxdumptool && git checkout ${HCXDUMPTOOL_VERSION} && make install && \
    git clone https://github.com/hashcat/kwprocessor.git && cd kwprocessor && git checkout ${HCXKEYS_VERSION} && make && \
    ln -s /root/kwprocessor/kwp /usr/bin/kwp

COPY . /app/

RUN pip3.11 install setuptools && \
    git clone https://github.com/michael2to3/pyhashcat.git && \
    cd pyhashcat/ && \
    python3.11 setup.py build_ext -I /usr/include/lzma/ && \
    python3.11 setup.py install

RUN pip3.11 install --no-cache-dir -r /app/requirements.txt
