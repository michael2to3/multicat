FROM ubuntu:22.04

ENV LLVM_VERSION 15
ENV HASHCAT_VERSION        v6.2.6
ENV HASHCAT_UTILS_VERSION  v1.9
ENV HCXTOOLS_VERSION       6.2.7
ENV HCXDUMPTOOL_VERSION    6.2.7
ENV HCXKEYS_VERSION        master
ENV HC_LIB_DIR=/usr/local/lib
ENV HC_SOURCES_DIR=/app/hashcat
ENV HC_PATH=/app/hashcat
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
ENV POCL_VERSION           v3.1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-dev libpython3-dev build-essential ocl-icd-libopencl1 cmake git pkg-config libclang-${LLVM_VERSION}-dev clang-${LLVM_VERSION} llvm-${LLVM_VERSION} make ninja-build ocl-icd-libopencl1 ocl-icd-dev ocl-icd-opencl-dev libhwloc-dev zlib1g zlib1g-dev clinfo dialog apt-utils libxml2-dev libclang-cpp${LLVM_VERSION}-dev libclang-cpp${LLVM_VERSION} llvm-${LLVM_VERSION}-dev


RUN mkdir -p /etc/OpenCL/vendors/ && \
    git clone https://github.com/pocl/pocl.git && cd pocl && git checkout ${POCL_VERSION} && \
    mkdir build && cd build && cmake .. && make install -j4 && cp pocl.icd /etc/OpenCL/vendors/

RUN apt-get update && \
    apt-get install -y wget make clinfo build-essential git libcurl4-openssl-dev libssl-dev zlib1g-dev libcurl4-openssl-dev libssl-dev pciutils python3.11 python3.11-dev && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3.11 get-pip.py && \
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
