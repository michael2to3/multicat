#!/bin/bash

set -eo pipefail

apt update
apt install -y lshw pciutils util-linux

install_amd() {
  echo "Installing OpenCL for AMD GPU."
  echo 'deb [arch=amd64] http://repo.radeon.com/rocm/apt/debian/ xenial main' | tee /etc/apt/sources.list.d/rocm.list
  apt update
  apt install -y rocm-opencl rocm-dkms rocm-libs
}

install_nvidia() {
  echo "Installing OpenCL for NVIDIA GPU."
  apt install -y nvidia-opencl-dev nvidia-cuda-toolkit
}

install_intel() {
  echo "Installing OpenCL for Intel CPU and GPU."
  apt install -y intel-opencl-icd
}

gpus=$(lspci | grep -i 'vga\|3d\|2d' | awk -F: '{print $3}' | awk '{print $1}' | sort | uniq)

for gpu in $gpus; do
  case "$gpu" in
    "NVIDIA")
      install_nvidia
      ;;
    "AMD"|"Radeon")
      install_amd
      ;;
    "Intel")
      install_intel
      ;;
    *)
      echo "Unknown GPU: $gpu. Skipping."
      ;;
  esac
done

echo "OpenCL installation completed."
