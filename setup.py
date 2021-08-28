import os

from setuptools import setup, find_packages

import sys
sys.path.append("./")

from gen_so import cc
__version__ = "0.0.3"
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()




setup(
    name = "HeXGButil",
    version = __version__,
    author = "xili wang",
    author_email = "zdlp@sina.cn",
    description = ("numba functions needed for HEXGB"),
    packages=find_packages(),
    license = "BSD",
    keywords = "HeXGB",
    url = "https://zizdlp.com",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],

    ext_modules=[cc.distutils_extension()],
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    ext_package='HeXGButil',
    zip_safe=False,
)

