from skbuild import setup
from setuptools import find_packages


setup(
    name='meta-cli',
    version=open('VERSION').read().strip(),
    author='Francesco De Carlo',
    author_email='decarlof@gmail.com',
    url='https://github.com/xray-imaging/meta-cli',

    package_dir={"": "src"},
    entry_points={'console_scripts':['meta = meta_cli.__main__:main'],},
    packages=find_packages('src'),
    description='cli to extract meta data from an h5 tomographic file',
    zip_safe=False,
)