from conans.client.generators.virtualrunenv import VirtualRunEnvGenerator
from conans import ConanFile, CMake
from conans.tools import os_info
import os

class ubitrack_virtualenv_generator(VirtualRunEnvGenerator):

    def __init__(self, conanfile):
        super(ubitrack_virtualenv_generator, self).__init__(conanfile)
        self.venv_name = "ubitrackrunenv"

    def ubitrack_env_items(self):
        items = {}
        if os_info.is_windows and not os_info.is_posix:
            items['UBITRACK_COMPONENTS_PATH'] = os.path.join(self.output_path, "bin", "ubitrack")
        else:
            items['UBITRACK_COMPONENTS_PATH'] = os.path.join(self.output_path, "lib", "ubitrack")

        deps_env_vars = self.conanfile.deps_env_info.vars
        for key, v in deps_env_vars.items():
            if key == "TRACKMAN_BIN_PATH":
              items["CLASSPATH"] = v[0]
            # else:
            #     if isinstance(v, list):
            #         v = ":".join(v)
            #     print("Export: %s=%s" % (key, v))
            #     items[key] = v

        return items.items()

    def trackman_config_items(self):
        items = {}
        items["UbitrackComponentDirectory"] = os.path.join(self.output_path, "lib", "ubitrack")
        items["LastDirectory"] = "."
        items["UbitrackWrapperDirectory"] = os.path.join(self.output_path, "lib")
        items["AutoCompletePatterns"] = ""
        items["PatternTemplateDirectory"] = os.path.join(self.output_path, "share", "Ubitrack", "utql")
        items["UbitrackLibraryDirectory"] = os.path.join(self.output_path, "lib")
        return items.items()

    def _sh_lines(self):
        activate_lines, deactivate_lines = super(ubitrack_virtualenv_generator, self)._sh_lines()

        variables = self.ubitrack_env_items()
        
        for name, activate, deactivate in self.format_values("sh", variables):
            activate_lines.append("%s=%s" % (name, activate))
            activate_lines.append("export %s" % name)
            if deactivate == '""':
                deactivate_lines.append("unset %s" % name)
            else:
                deactivate_lines.append("%s=%s" % (name, deactivate))
                deactivate_lines.append("export %s" % name)            
        activate_lines.append('')
        deactivate_lines.append('')

        return activate_lines, deactivate_lines

    def _cmd_lines(self):
        activate_lines, deactivate_lines = super(ubitrack_virtualenv_generator, self)._cmd_lines()

        variables = self.ubitrack_env_items()

        for name, activate, deactivate in self.format_values("cmd", variables):
            activate_lines.append("SET %s=%s" % (name, activate))
            deactivate_lines.append("SET %s=%s" % (name, deactivate))
        activate_lines.append('')
        deactivate_lines.append('')

        return activate_lines, deactivate_lines

    def _ps1_lines(self):
        activate_lines, deactivate_lines = super(ubitrack_virtualenv_generator, self)._ps1_lines()

        variables = self.ubitrack_env_items()

        for name, activate, deactivate in self.format_values("ps1", variables):
            activate_lines.append('$env:%s = %s' % (name,activate))
            deactivate_lines.append('$env:%s = %s' % (name,deactivate))
        activate_lines.append('')

        return activate_lines, deactivate_lines

    def _trackman_config_lines(self):
        config_lines = []
        for key, value in self.trackman_config_items():
            # need to escape backslashes for windows
            if os_info.is_windows and not os_info.is_posix:
                value = value.replace("\\", "\\\\")
            config_lines.append('%s=%s' % (key, value))
        return config_lines


    def _add_trackman_files(self, result):
        deps_env_vars = self.conanfile.deps_env_info.vars
        if "TRACKMAN_BIN_PATH" in deps_env_vars:
            trackman_items = {}
            trackman_items["CLASSPATH"] = deps_env_vars["TRACKMAN_LIB_PATH"][0]

            # add trackman config file
            trackman_config_lines = self._trackman_config_lines()
            result["trackman.conf"] = os.linesep.join(trackman_config_lines)


            if os_info.is_windows and not os_info.is_posix:
                script_lines, _ = self._cmd_lines()
                for name, activate, deactivate in self.format_values("cmd", trackman_items.items()):
                    script_lines.append("SET %s=%s" % (name, activate))
                script_lines.append("java -jar %s" % os.path.join(deps_env_vars["TRACKMAN_BIN_PATH"][0], "trackman.jar"))
                result["startTrackman.bat"] = os.linesep.join(script_lines)

                script_lines, _ = self._ps1_lines()
                for name, activate, deactivate in self.format_values("cmd", trackman_items.items()):
                    script_lines.append("SET %s=%s" % (name, activate))
                script_lines.append("java -jar %s" % os.path.join(deps_env_vars["TRACKMAN_BIN_PATH"][0], "trackman.jar"))
                result["startTrackman.ps1"] = os.linesep.join(script_lines)

            if os_info.is_posix:
                script_lines, _ = self._sh_lines()
                for name, activate, deactivate in self.format_values("sh", trackman_items.items()):
                    script_lines.append("%s=%s" % (name, activate))
                    script_lines.append("export %s" % name)
                script_lines.append("java -jar %s" % os.path.join(deps_env_vars["TRACKMAN_BIN_PATH"][0], "trackman.jar"))
                result["startTrackman.sh"] = os.linesep.join(script_lines)

        return result

    @property
    def content(self):
        ret = super(ubitrack_virtualenv_generator, self).content
        return self._add_trackman_files(ret)


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