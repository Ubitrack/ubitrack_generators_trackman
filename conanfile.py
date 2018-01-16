from conans.client.generators.virtualrunenv import VirtualRunEnvGenerator
from conans import ConanFile, CMake
import platform
import os

class ubitrack_virtualenv_generator(VirtualRunEnvGenerator):

    def __init__(self, conanfile):
        super(ubitrack_virtualenv_generator, self).__init__(conanfile)
        self.venv_name = "ubitrackrunenv"


    def _trackman_startscript_lines(self, venv_name):
        script_lines = []
        deps_env_vars = self.conanfile.deps_env_info.vars
        if platform.system() == "Windows":
          script_lines.append("@echo off")
          script_lines.append("activate_run.bat")
          script_lines.append("SET CLASSPATH=%s" % deps_env_vars["TRACKMAN_LIB_PATH"])
        else:
          script_lines.append("source activate_run.sh")
          script_lines.append("export CLASSPATH=%s" % deps_env_vars["TRACKMAN_LIB_PATH"])

        script_lines.append("java -jar %s" % os.path.join(deps_env_vars["TRACKMAN_BIN_PATH"], "trackman.jar"))
        return script_lines


    @property
    def content(self):
        ret = super(ubitrack_virtualenv_generator, self).content

        # add ubitrack specific scripts here
        ext = "bat" if platform.system() == "Windows" else "sh"

        deps_env_vars = self.conanfile.deps_env_info.vars
        
        if "TRACKMAN_BIN_PATH" in deps_env_vars:
          trackman_startscript_lines = self._trackman_startscript_lines(self.venv_name)
          ret["startTrackman.%s" % ext] = os.linesep.join(trackman_startscript_lines)

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