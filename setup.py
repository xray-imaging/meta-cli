from setuptools import setup, find_packages
from setuptools.command.install import install
import os


setup(
    name='meta-cli',
    version=open('VERSION').read().strip(),
    #version=__version__,
    author='Francesco De Carlo',
    author_email='decarlof@gmail.com',
    url='https://github.com/xray-imaging/meta-cli',
    packages=find_packages(),
    include_package_data = True,
    scripts=['bin/metacli.py'],
    entry_points={'console_scripts':['meta = metacli:main'],},
    description='cli to extract meta data from an h5 tomographic file',
    zip_safe=False,
)