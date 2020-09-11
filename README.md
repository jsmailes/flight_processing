# flight_processing

Flight_processing is a python library aimed at extracting useful data from OpenSky flight position reports and airspace data.

## Installation

You can install flight_processing from [PyPI](https://pypi.org/):
```
TODO put on pypi
```

## Usage

Documentation coming soon

## Build

Requirements on Fedora (package names may vary between distributions):

```
boost-devel
boost-python3-devel
boost-numpy3
git
cmake
gcc-c++
python3
```

### Build

```
pip3 install setuptools
python3 setup.py build
```

### Build Wheel

```
pip3 install setuptools
python3 setup.py sdist bdist_wheel
```

### Install

```
pip3 install setuptools
pip3 install .
```

Pip should automatically call the underlying `cmake` build pipeline and install all the python prerequisites.