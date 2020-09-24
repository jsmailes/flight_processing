# Adapted from https://www.benjack.io/2018/02/02/python-cpp-revisited.html

import os
import re
import sys
import platform
import subprocess
import pathlib
import shutil

from distutils.version import LooseVersion
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install_lib import install_lib


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)',
                                         out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            #cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(
            #    cfg.upper(),
            #    extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get('CXXFLAGS', ''),
            self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args,
                              cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args,
                              cwd=self.build_temp)
        print()  # Add an empty line for cleaner output


class InstallCMakeLibs(install_lib):
    """
    Get the libraries from the parent distribution, use those as the outfiles

    Skip building anything; everything is already built, forward libraries to
    the installation step
    """

    def run(self):
        """
        Copy libraries from the bin directory and place them as appropriate
        """

        self.announce("Moving library files", level=3)

        # We have already built the libraries in the previous build_ext step

        self.skip_build = True

        bin_dir = "src/flight_processing"

        libs = [os.path.join(bin_dir, _lib) for _lib in
                os.listdir(bin_dir) if
                os.path.isfile(os.path.join(bin_dir, _lib)) and
                os.path.splitext(_lib)[1] in [".dll", ".so"]]

        print("Library files: {}".format(libs))

        print("Copy destination: {}".format(os.path.join(self.build_dir, os.path.basename(libs[0]))))

        for lib in libs:
            shutil.move(lib, os.path.join(self.build_dir,
                                          "flight_processing",
                                          os.path.basename(lib)))

        # Mark the libs for installation, adding them to
        # distribution.data_files seems to ensure that setuptools' record
        # writer appends them to installed-files.txt in the package's egg-info
        #
        # Also tried adding the libraries to the distribution.libraries list,
        # but that never seemed to add them to the installed-files.txt in the
        # egg-info, and the online recommendation seems to be adding libraries
        # into eager_resources in the call to setup(), which I think puts them
        # in data_files anyways.
        #
        # What is the best way?

        # These are the additional installation files that should be
        # included in the package, but are resultant of the cmake build
        # step; depending on the files that are generated from your cmake
        # build chain, you may need to modify the below code

        self.distribution.data_files = [os.path.join(self.build_dir,
                                                     "flight_processing",
                                                     os.path.basename(lib))
                                        for lib in libs]

        # Must be forced to run after adding the libs to data_files

        self.distribution.run_command("install_data")

        super().run()


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='flight_processing',
    version='0.8.0',
    author='Joshua Smailes',
    author_email='joshua.smailes@cs.ox.ac.uk',
    description='Extract useful data from OpenSky position reports and previously extracted airspace data.',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jsmailes/flight_processing",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Matplotlib",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Security",
    ],
    include_package_data=True,
    package_data={
        "": ["*.conf", "*.so"],
    },
    install_requires=[
        "python-dateutil>=2.8.1",
        "scipy>=1.5.2",
        "pandas>=1.1.2",
        "geopandas>=0.8.1",
        "Shapely>=1.7.1",
        "networkx>=2.5",
        "simplejson>=3",
        "traffic>=2.4",
        "numpy>=1.19.1",
        "pyproj>=2.6.1",
        "hvplot>=0.6.0",
        "matplotlib>=3",
        "cartopy>=0.18.0",
        "pathlib>=1",
        "appdirs>=1.4.4",
        "configparser>=5.0.0",
    ],
    # tell setuptools to look for any packages under 'src'
    packages=find_packages('src'),
    # tell setuptools that all packages will be under the 'src' directory
    # and nowhere else
    package_dir={'':'src'},
    # add an extension module named 'python_cpp_example' to the package
    # 'python_cpp_example'
    ext_modules=[CMakeExtension('flight_processing/process_flights')],
    # add custom build_ext command
    cmdclass=dict(
        build_ext=CMakeBuild,
        install_lib=InstallCMakeLibs),
    zip_safe=False,
)
