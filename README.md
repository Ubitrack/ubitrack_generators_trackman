## This repository holds a conan virtualenv generator for Ubitrack

This is a special "generator package" which creates environment and launch scripts for TUM ubitrack.

### Preparations

All TUM Ubitrack related software packages are hosted on the [CAMPAR](http://campar.in.tum.de) conan repository. The repository can be added using the following command after installing conan and your favourite compiler.

    $ conan remote add camp "https://conan.campar.in.tum.de"


## For Users: Use this package

### Basic setup

    $ conan install ubitrack/1.3.0@ubitrack/stable -g ubitrack_virtualenv_generator

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    ubitrack/1.3.0@ubitrack/stable

    [generators]
    ubitrack_virtualenv_generator

Complete the installation of requirements for your project running:</small></span>

    $ mkdir build && cd build && conan install ..
    
Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they shoudl not be added to the root of the project, nor committed to git. 

### License
[Ubitrack](LICENSE)