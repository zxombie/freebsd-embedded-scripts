#!/bin/sh

#
# An example script to cross build a given kernel.
# This script assumes you already have a valid environment.
#

# Set these to the values required
BASE_DIR=/home/andrew/freebsd/repos/head
KERNCONF="LN2410SBC"
TARGET=arm
TARGET_ARCH=arm

# The arguments for buildkernel
ARGS="TARGET=${TARGET} TARGET_ARCH=${TARGET_ARCH} KERNCONF=${KERNCONF}"
ARGS="${ARGS} -DKERNFAST"

# Source the required files
. ./helpers/kernel.sh
. ./helpers/uboot.sh

# Exit on failure
set -e

# Build the kernel
cd ${BASE_DIR}
nice make buildkernel ${ARGS}
KERNEL_FILE=`get_kernel_file "${BASE_DIR}" "${KERNCONF}" \
    "${TARGET}" "${TARGET_ARCH}"`

# Turn it into a U-Boot image
uboot_mkimage ${KERNEL_FILE}

# Print the name of the file
echo "The kernel file is:"
uboot_kernel ${KERNEL_FILE}

