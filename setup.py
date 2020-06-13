from setuptools import setup, find_packages
from setuptools.command.install import install
import os


setup(
    name='metah5',
    version=open('VERSION').read().strip(),
    #version=__version__,
    author='Francesco De Carlo',
    author_email='decarlof@gmail.com',
    url='https://github.com/xray-imaging/metah5',
    packages=find_packages(),
    include_package_data = True,
    scripts=['bin/metah5'],
    description='cli to extract meta data from an h5 tomographic file',
    zip_safe=False,
)