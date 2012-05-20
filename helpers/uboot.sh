#
# Useful functions for using the kernel with U-Boot
#

uboot_kernel()
{
	KERNEL_FILE="$1"

	echo ${KERNEL_FILE}.boot
}

uboot_mkimage()
{
	KERNEL_FILE="$1"
	UBOOT_KERNEL=`uboot_kernel "${KERNEL_FILE}"`

	PHYSADDR=`kernel_phys_address ${KERNEL_FILE}`
	PHYS_ENTRY=`kernel_phys_entry ${KERNEL_FILE}`

	mkimage -A arm -O freebsd -T kernel -C none -a ${PHYSADDR} \
	    -e ${PHYS_ENTRY} -n "FreeBSD" -d ${KERNEL_FILE} ${UBOOT_KERNEL}
}

