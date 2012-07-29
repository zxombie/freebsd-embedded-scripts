#
#  Copyright (c) 2012 Andrew Turner
#  All rights reserved.
# 
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
# 
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
#  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
#  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#  SUCH DAMAGE.
# 

import elftools.elf.elffile
import elftools.elf.sections

class Kernel(object):
    '''A class to hold Kernel data. Currently ARM specific.'''
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename)
        self.elf = elftools.elf.elffile.ELFFile(self.file)

        # The virtual address for the start of kernel memory is fixed
        self.virtbase = 0xc0000000

        # The virtual address of the entry point
        self.virtentry = self.elf.header['e_entry']

        # Find the virtual address we are loaded to
        for segment in self.elf.iter_segments():
            if not segment['p_type'] == "PT_LOAD":
                continue
            self.virtload = segment['p_vaddr']

        # Find the physical address of the start of memory
        done = False
        for section in self.elf.iter_sections():
            if not isinstance(section,
              elftools.elf.sections.SymbolTableSection):
                continue
            for nsym, symbol in enumerate(section.iter_symbols()):
                if symbol.name == "physaddr":
                    self.physbase = 0l + symbol['st_value']
                    done = True
                    break
            if done:
                break

    def virt_to_phys(self, addr):
        '''Translate from a virtual address to a physical address'''
        return addr + self.physbase - self.virtbase

    physload = property(lambda self : self.virt_to_phys(self.virtload))
    physentry = property(lambda self : self.virt_to_phys(self.virtentry))

