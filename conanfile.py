from conans.client.generators.virtualrunenv import VirtualRunEnvGenerator
from conans.paths import BUILD_INFO
from conans import ConanFile, CMake

class ubitrack_virtualenv_generator(VirtualRunEnvGenerator):

    def __init__(self, conanfile):
        super(ubitrack_virtualenv_generator, self).__init__(conanfile)
        self.venv_name = "ubitrackrunenv"

    @property
    def content(self):
        ret = super(ubitrack_virtualenv_generator, self).content
        # add ubitrack specific scripts here

        return ret


class MyCustomGeneratorPackage(ConanFile):
    name = "ubitrack_virtualenv_generator"
    version = "1.3.0"
    url = "https://github.com/Ubitrack/ubitrack_virtualenv_generator"
    license = "GPL"

    def build(self):
      pass

    def package_info(self):
      self.cpp_info.includedirs = []
      self.cpp_info.libdirs = []
      self.cpp_info.bindirs = []