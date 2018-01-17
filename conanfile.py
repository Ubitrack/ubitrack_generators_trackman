from conans.client.generators.virtualrunenv import VirtualRunEnvGenerator
from conans import ConanFile, CMake
import platform
import os

class ubitrack_virtualenv_generator(VirtualRunEnvGenerator):

    def __init__(self, conanfile):
        super(ubitrack_virtualenv_generator, self).__init__(conanfile)
        self.venv_name = "ubitrackrunenv"

    def _activate_lines(self, venv_name):
        ret = super(ubitrack_virtualenv_generator, self)._activate_lines(venv_name)
        if platform.system() == "Windows":
          script_lines.append("SET UBITRACK_COMPONENTS_PATH=%s" % os.path.join(self.output_path, "lib", "ubitrack"))
        else:
          script_lines.append("export UBITRACK_COMPONENTS_PATH=%s" % os.path.join(self.output_path, "lib", "ubitrack"))
        return ret

    def _trackman_startscript_lines(self, venv_name):
        script_lines = self._activate_lines(venv_name)
        deps_env_vars = self.conanfile.deps_env_info.vars
        if platform.system() == "Windows":
          script_lines.append("SET CLASSPATH=%s" % deps_env_vars["TRACKMAN_LIB_PATH"][0])
        else:
          script_lines.append("export CLASSPATH=%s" % deps_env_vars["TRACKMAN_LIB_PATH"][0])

        script_lines.append("java -jar %s" % os.path.join(deps_env_vars["TRACKMAN_BIN_PATH"][0], "trackman.jar"))
        return script_lines


    def _trackman_config_lines(self, venv_name):
        script_lines = ["#trackman configuration file"]
        script_lines.append("UbitrackComponentDirectory=%s" % os.path.join(self.output_path, "lib", "ubitrack"))
        script_lines.append("LastDirectory=.")
        script_lines.append("UbitrackWrapperDirectory=%s" % os.path.join(self.output_path, "lib"))
        script_lines.append("AutoCompletePatterns=")
        script_lines.append("PatternTemplateDirectory=%s" % os.path.join(self.output_path, "share", "Ubitrack", "utql"))
        script_lines.append("UbitrackLibraryDirectory=%s" % os.path.join(self.output_path, "lib"))
        # need to escape backslashes for windows
        if platform.system() == "Windows":
          script_lines = [l.replace("\\", "\\\\") for l in script_lines]
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

          trackman_config_lines = self._trackman_config_lines(self.venv_name)
          ret["trackman.conf"] = os.linesep.join(trackman_config_lines)

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