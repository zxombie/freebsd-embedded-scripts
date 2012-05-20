#
# Useful functions to get details from the Kernel
#

buildkernel()
{
	DIR="$1"
	KERNCONF="$2"
	TARGET="$3"
	TARGET_ARCH="$4"
	shift 4
	EXTRA_ARGS=$@

	ARGS="TARGET=${TARGET} TARGET_ARCH=${TARGET_ARCH} KERNCONF=${KERNCONF}"
	make buildkernel -C ${DIR} ${ARGS} ${EXTRA_ARGS}
}

# Gets the kernel file for a given build
get_kernel_file()
{
	DIR="$1"
	KERNCONF="$2"
	TARGET="$3"
	TARGET_ARCH="$4"

	echo /usr/obj/${TARGET}.${TARGET_ARCH}${DIR}/sys/${KERNCONF}/kernel
}

# Get the physical address the kernel expects to be loaded to
kernel_phys_address()
{
	KERNEL_FILE="$1"
	readelf -s ${KERNEL_FILE} | grep -m 1 "[^L]physaddr" | \
	    awk '{ print $2; }' | tr 'a-f' 'A-F'
}

# Translate a virtual address to a physical address
kernel_virt_to_phys()
{
	ADDRESS="$1"
	VIRT_BASE="$2"
	PHYS_BASE="$3"

	DELTA=`echo "obase=16 ; ibase=16 ; ${VIRT_BASE} - ${PHYS_BASE}" | bc`
	echo "obase=16 ; ibase=16 ; ${ADDRESS} - ${DELTA}" | bc
}

# Get the virtual address the kernel expects to be loaded to
kernel_virt_address()
{
	KERNEL_FILE="$1"
	readelf -s ${KERNEL_FILE} | grep -m 1 "kernbase" | \
	    awk '{ print $2; }' | tr 'a-f' 'A-F'
}

# Get the virtual address of the kernel entry point
kernel_virt_entry()
{
	KERNEL_FILE="$1"

	readelf -h ${KERNEL_FILE} | grep "Entry point address" | \
	    awk '{ print $NF; }' | sed 's/^0x//' | tr 'a-f' 'A-F'
}

# Get the physical address of the kernel entry point
kernel_phys_entry()
{
	KERNEL_FILE="$1"
	
	# Find the physical address we should load the kernel to
	PHYSADDR=`kernel_phys_address ${KERNEL_FILE}`

	# Find the virtual address we should load the kernel to
	KERNBASE=`kernel_virt_address ${KERNEL_FILE}`

	# Find the entry point
	ENTRY=`kernel_virt_entry ${KERNEL_FILE}`

	kernel_virt_to_phys ${ENTRY} ${KERNBASE} ${PHYSADDR}
}

