from conans.client.generators.virtualrunenv import VirtualRunEnvGenerator
from conans.paths import BUILD_INFO
from conans import ConanFile, CMake

class UbitrackVirtualRunEnvGenerator(VirtualRunEnvGenerator):

    def __init__(self, conanfile):
        super(UbitrackVirtualRunEnvGenerator, self).__init__(conanfile)
        self.venv_name = "ubitrackrunenv"

    @property
    def content(self):
        ret = super(UbitrackVirtualRunEnvGenerator, self).content
        # add ubitrack specific scripts here

        return ret


class MyCustomGeneratorPackage(ConanFile):
    name = "ubitrack_virtualenv_generator"
    version = "0.1"
    url = "https://github.com/Ubitrack/ubitrack_virtualenv_generator"
    license = "GPL"

    def build(self):
      pass

    def package_info(self):
      self.cpp_info.includedirs = []
      self.cpp_info.libdirs = []
      self.cpp_info.bindirs = []