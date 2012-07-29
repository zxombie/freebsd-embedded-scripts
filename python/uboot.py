
import subprocess

class UBoot(object):
    def __init__(self, kernel):
        self.kernel = kernel

    def mkimage(self, out_file = None):
        print self.kernel.filename

        if out_file is None:
            out_file = self.kernel.filename + '.uboot'

        cmd = ['mkimage',
          '-A', 'arm',
          '-O', 'linux',
          '-T', 'kernel',
          '-C', 'none',
          '-a', '%x' % self.kernel.physload,
          '-e', '%x' % self.kernel.physentry,
          '-n', 'FreeBSD',
          '-d', self.kernel.filename, out_file]
        print ' '.join(cmd)
        subprocess.call(cmd)

