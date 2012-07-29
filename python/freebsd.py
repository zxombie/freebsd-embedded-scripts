
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

