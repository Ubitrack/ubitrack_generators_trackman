from conans.client.generators.virtualrunenv import VirtualRunEnvGenerator
from conans.client.run_environment import RunEnvironment
from conans import ConanFile, CMake
from conans.tools import os_info
import os

import textwrap
from jinja2 import Template



sh_trackman_script_tpl = Template(textwrap.dedent("""\
    #!/usr/bin/env sh
    {%- for it in modified_vars %}
    export CONAN_OLD_{{it}}="${{it}}"
    {%- endfor %}
    while read -r line; do
        LINE="$(eval echo $line)";
        export "$LINE";
    done < "{{ environment_file }}"
    export CONAN_OLD_PS1="$PS1"
    export PS1="({{venv_name}}) $PS1"
    java -jar {{jar_path}}
"""))

cmd_trackman_script_tpl = Template(textwrap.dedent("""\
    @echo off
    
    {%- for it in modified_vars %}
    SET "CONAN_OLD_{{it}}=%{{it}}%"
    {%- endfor %}
    
    FOR /F "usebackq tokens=1,* delims==" %%i IN ("{{ environment_file }}") DO (
        CALL SET "%%i=%%j"
    )
    
    SET "CONAN_OLD_PROMPT=%PROMPT%"
    SET "PROMPT=({{venv_name}}) %PROMPT%"
    java -jar {{jar_path}}
"""))

class ubitrack_virtualenv_generator(VirtualRunEnvGenerator):

    venv_name = "ubitrackrunenv"
    suffix    = "_utrun"


    def __init__(self, conanfile):
        super(ubitrack_virtualenv_generator, self).__init__(conanfile)


    def trackman_config_items(self):
        items = {}
        items["UbitrackComponentDirectory"] = os.path.join(self.output_path, "lib", "ubitrack")
        items["LastDirectory"] = "."
        items["UbitrackWrapperDirectory"] = os.path.join(self.output_path, "lib")
        items["AutoCompletePatterns"] = ""
        items["PatternTemplateDirectory"] = os.path.join(self.output_path, "share", "Ubitrack", "utql")
        items["UbitrackLibraryDirectory"] = os.path.join(self.output_path, "lib")
        return items.items()

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
                flavor = "cmd"
                environment_filename = "environment{}.{}.env".format(self.suffix, flavor)
                ret = list(self._format_values(flavor, self.env.items()))
                modified_vars = [name for name, _, existing in ret if existing]
                new_vars = [name for name, _, existing in ret if not existing]

                environment_filepath = os.path.abspath(os.path.join(self.output_path, environment_filename))
                result["startTrackman.bat"] = cmd_trackman_script_tpl.render(environment_file=environment_filepath,
                                                       modified_vars=modified_vars, new_vars=new_vars,
                                                       jar_path=os.path.join(deps_env_vars["TRACKMAN_BIN_PATH"][0], "trackman.jar"),
                                                       venv_name=self.venv_name)

            if os_info.is_posix:
                flavor = "sh"
                environment_filename = "environment{}.{}.env".format(self.suffix, flavor)
                ret = list(self._format_values(flavor, self.env.items()))
                modified_vars = [name for name, _, existing in ret if existing]
                new_vars = [name for name, _, existing in ret if not existing]

                environment_filepath = os.path.abspath(os.path.join(self.output_path, environment_filename))
                result["startTrackman.sh"] = sh_trackman_script_tpl.render(environment_file=environment_filepath,
                                                       modified_vars=modified_vars, new_vars=new_vars,
                                                       jar_path=os.path.join(deps_env_vars["TRACKMAN_BIN_PATH"][0], "trackman.jar"),
                                                       venv_name=self.venv_name)
        return result

    @property
    def content(self):

        if os_info.is_windows and not os_info.is_posix:
            self.env['UBITRACK_COMPONENTS_PATH'] = os.path.join(".", "bin", "ubitrack")
        else:
            self.env['UBITRACK_COMPONENTS_PATH'] = os.path.join(".", "lib", "ubitrack")

        deps_env_vars = self.conanfile.deps_env_info.vars
        for key, v in deps_env_vars.items():
            if key == "TRACKMAN_BIN_PATH":
              self.env["CLASSPATH"] = v[0]

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