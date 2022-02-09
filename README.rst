====
meta
====

**meta** is commad-line-interface for extracting meta data from `data exchange <https://dxfile.readthedocs.io/en/latest/source/xraytomo.html/>`_ tomographic data used at the `Advanced Photon Source <https://www.aps.anl.gov/>`_  `beamlines <https://dxfile.readthedocs.io/en/latest/source/demo/doc.areadetector.html>`_.

Installation
============

::

    $ git clone https://github.com/xray-imaging/meta.git
    $ cd meta
    $ python setup.py install

in a prepared virtualenv or as root for system-wide installation.

.. warning:: 
	If your python installation is in a location different from #!/usr/bin/env python please edit the first line of the bin/meta file to match yours.


Dependencies
============

- `dxchange <https://github.com/data-exchange/dxchange>`_ version > 0.1.6 
- pandas => ``conda install pandas``
- tabulate => ``conda install tabulate``

Usage
=====

View the hdf tree
-----------------

To view the data tree contained in a generic hdf file::

    $ meta tree --h5-name data/base_file_name_001.h5 
    │
    ├── defaults
    │   │
    │   ├── ColorMode (754,)
    │   ├── NDArrayEpicsTSSec (754,)
    │   ├── NDArrayEpicsTSnSec (754,)
    │   ├── NDArrayTimeStamp (754,)
    │   ├── NDArrayUniqueId (754,)
    │   ├── SaveDest (754,)
    │   └── timestamp (754, 5)
    ├── exchange
    │   │
    │   ├── data (726, 2048, 2448)
    │   ├── data_dark (8, 2048, 2448)
    │   ├── data_white (20, 2048, 2448)
    │   └── theta (726,)
    ├── measurement
    ...


View the meta data
------------------

To view the meta data contained in a `dxchange <https://github.com/data-exchange/dxchange>`_ file::

    $ meta dx --h5-name data/base_file_name_001.h5 

	2020-06-12 23:26:19,796 - General
	2020-06-12 23:26:19,797 -   config           ./meta.conf
	2020-06-12 23:26:19,797 -   verbose          True

+-----------------------+--------------------------+---------+
|                       | value                    | unit    |
+=======================+==========================+=========+
| 000_resolution        | 4.7                      | microns |
+-----------------------+--------------------------+---------+
| 000_energy            | 20.0                     | keV     |
+-----------------------+--------------------------+---------+
| 000_experimenter_name | Francesco De Carlo       |         |
+-----------------------+--------------------------+---------+
| 000_full_file_name    | base_file_name_001.h5    |         |
+-----------------------+--------------------------+---------+
| 000_end_date          | 2020-06-12T15:11:12-0500 |         |
+-----------------------+--------------------------+---------+
| 000_sample_in_x       | 0.0                      | mm      |
+-----------------------+--------------------------+---------+
| 000_sample_in_y       | 0.0                      | mm      |
+-----------------------+--------------------------+---------+
| 000_start_date        | 2020-06-12T14:02:35-0500 |         |
+-----------------------+--------------------------+---------+

To generate an rst file containing a table compatible sphinx/readthedocs::

    $ meta docs --h5-name data/base_file_name_001.h5


.. note:: 
	--h5-name can be also a folder, e.g. --h5-name data/ in this case all hdf files in the folder will be processed.


to list of all available options::

    $ meta  -h


Configuration File
------------------

meta parameters are stored in **meta.conf**. You can create a template with::

    $ meta init

**meta.conf** is constantly updated to keep track of the last stored parameters, as initalized by **init** or modified by setting a new option value. For example to re-run the last meta with identical --h5-name parameters used before just use::

    $ meta docs

