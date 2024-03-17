FROM intel/oneapi-basekit:devel-ubuntu22.04

# Fix apt update forbidden issue
RUN rm /etc/apt/sources.list.d/intel-graphics.list

# Remove FPGA device support
RUN rm /opt/intel/oneapi/compiler/2023.0.0/linux/lib/x64/cl.fpga_emu.cfg
RUN rm -rf /opt/intel/oneapi/compiler/2023.0.0/linux/lib/oclfpga
RUN rm /etc/OpenCL/vendors/Altera.icd
RUN rm /etc/OpenCL/vendors/Intel_FPGA_SSG_Emulator.icd


RUN apt-get update && apt-get install -y clinfo pkg-config

ENV HASHCAT_VERSION        v6.2.6
ENV HASHCAT_UTILS_VERSION  v1.9
ENV HCXTOOLS_VERSION       6.2.7
ENV HCXDUMPTOOL_VERSION    6.2.7
ENV HCXKEYS_VERSION        master

# Update & install packages for installing hashcat
RUN apt-get update && \
    apt-get install -y wget make clinfo build-essential git libcurl4-openssl-dev libssl-dev zlib1g-dev libcurl4-openssl-dev libssl-dev pciutils python3.11 python3-pip

# Fetch PCI IDs list to display proper GPU names
RUN update-pciids

WORKDIR /app

RUN git clone https://github.com/hashcat/hashcat.git && cd hashcat && git checkout ${HASHCAT_VERSION} && make install_library && make install -j4

RUN git clone https://github.com/hashcat/hashcat-utils.git && cd hashcat-utils/src && git checkout ${HASHCAT_UTILS_VERSION} && make
RUN ln -s /root/hashcat-utils/src/cap2hccapx.bin /usr/bin/cap2hccapx

RUN git clone https://github.com/ZerBea/hcxtools.git && cd hcxtools && git checkout ${HCXTOOLS_VERSION} && make install

RUN git clone https://github.com/ZerBea/hcxdumptool.git && cd hcxdumptool && git checkout ${HCXDUMPTOOL_VERSION} && make install

RUN git clone https://github.com/hashcat/kwprocessor.git && cd kwprocessor && git checkout ${HCXKEYS_VERSION} && make
RUN ln -s /root/kwprocessor/kwp /usr/bin/kwp

ENV HC_LIB_DIR=/usr/local/lib
ENV HC_SOURCES_DIR=/app/hashcat
ENV HC_PATH=/app/hashcat
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}

COPY . /app/

RUN pip3 install setuptools && \
    git clone https://github.com/michael2to3/pyhashcat.git && \
    cd pyhashcat/ && \
    python3 setup.py build_ext -I /usr/include/lzma/ && \
    python3 setup.py install

RUN pip3 install --no-cache-dir -r /app/requirements.txt
