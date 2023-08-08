============
Installation
============

::

    $ git clone https://github.com/xray-imaging/meta-cli.git
    $ cd meta-cli
    $ python setup.py install

in a prepared virtualenv or as root for system-wide installation.

.. warning:: 
   If your python installation is in a location different from #!/usr/bin/env python please edit the first line of the bin/meta file to match yours.


Dependencies
============

- `meta <https://github.com/xray-imaging/meta.git>`_
- pandas => ``conda install pandas``
- tabulate => ``conda install tabulate``

