#!/usr/bin/env python

import sys
# Needed for the freebsd module
sys.path.extend(["/home/andrew/building/pyelftools/"])

import os.path
sys.path.extend([os.path.dirname(sys.argv[0]) + "/python"])

import freebsd
import uboot

def main():

    try:
        k = freebsd.Kernel(sys.argv[1])
    except IndexError:
        print 'No input file specified'
        return
    u = uboot.UBoot(k)
    try:
        u.mkimage(sys.argv[2])
    except IndexError:
        u.mkimage()

if __name__ == '__main__':
    main()

