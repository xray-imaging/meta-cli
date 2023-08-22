=================
Meta-data readers
=================

HDF
===


**meta-cli** is commad-line-interface for extracting meta data from a generic HDF file like  `data exchange <https://dxfile.readthedocs.io/en/latest/source/xraytomo.html/>`_, the tomographic data format used at the `Advanced Photon Source <https://www.aps.anl.gov/>`_  `beamlines <https://dxfile.readthedocs.io/en/latest/source/demo/doc.areadetector.html>`_ or `NeXus <https://www.nexusformat.org/>`_ adopted at Diamond, ESRF and Desy.


Installation
------------

::

    $ git clone https://github.com/xray-imaging/meta-cli.git
    $ cd meta-cli
    $ python setup.py install

in a prepared virtualenv or as root for system-wide installation.

.. warning:: 
   If your python installation is in a location different from #!/usr/bin/env python please edit the first line of the bin/meta file to match yours.


Dependencies
------------

- `meta <https://github.com/xray-imaging/meta.git>`_
- pandas => ``conda install pandas``
- tabulate => ``conda install tabulate``


Usage
-----

View the hdf tree
~~~~~~~~~~~~~~~~~

To view the data tree contained in a generic hdf file:

::

    $ meta tree --file-name data/base_file_name_001.h5 

.. image:: img/meta_tree.png
    :width: 40%
    :align: center


View the meta data
~~~~~~~~~~~~~~~~~~

To view the meta data contained in a generic hdf file:

::

    $ meta show --file-name data/base_file_name_001.h5 


.. image:: img/meta_show.png
    :width: 40%
    :align: center

View a subset meta data
~~~~~~~~~~~~~~~~~~~~~~~

To view a subset of the meta data contained in a generic hdf file:

::

    $ meta show --file-name data/base_file_name_001.h5 --key energy


Replace an hdf entry value
~~~~~~~~~~~~~~~~~~~~~~~~~~

To replace the value of an entry:

 ::

    $ meta set --file-name data/base_file_name_001.h5 --key /process/acquisition/rotation/rotation_start --value 10


Meta data rst table
~~~~~~~~~~~~~~~~~~~

To generate a meta data rst table compatible with sphinx/readthedocs::

    $ meta docs --file-name data/base_file_name_001.h5 
    2022-02-09 12:30:16,983 - Please copy/paste the content of ./log_2020-05.rst in your rst docs file


The content of the generated rst file will publish in a sphinx/readthedocs document as:

**2022-05**

**decarlo**

+--------------------------------------------------------+--------------------+--------+
|                                                        | value              | unit   |
+========================================================+====================+========+
|     /measurement/instrument/monochromator/energy       | 30.0               | keV    |
+--------------------------------------------------------+--------------------+--------+
|     /measurement/instrument/sample_motor_stack/setup/x | 0.0                | mm     |
+--------------------------------------------------------+--------------------+--------+
|     /measurement/instrument/sample_motor_stack/setup/y | 0.4000116247000278 | mm     |
+--------------------------------------------------------+--------------------+--------+
|     /measurement/sample/experimenter/email             | decarlof@gmail.com |        |
+--------------------------------------------------------+--------------------+--------+


.. note:: 
   when using the **docs** option --file-name can be also a folder, e.g. --file-name data/ in this case all hdf files in the folder will be processed.


to list of all available options::

    $ meta  -h


Configuration File
~~~~~~~~~~~~~~~~~~

meta parameters are stored in **meta.conf**. You can create a template with::

    $ meta init

**meta.conf** is constantly updated to keep track of the last stored parameters, as initalized by **init** or modified by setting a new option value. For example to re-run the last meta with identical --file-name parameters used before just use::

    $ meta docs



GE Phoenix v|tome|x m µCT
=========================

The GE Phoenix v|tome|x m µCT instruments generates .pca, .dtxml, .pcj and .pcp files. An example is available at :ref:`GE`.

Code
----

.. toctree::

   api/readers.ge


Dependencies
------------

Create a new conda environment::

        conda create --name nocturn python=3.9

and activate the new environment with::

        conda activate nocturn

then install the following packages::

        conda install xmltodict
        conda install pandas
        conda install openpyxl


Run
---

::

        conda activate nocturn
        python ge.py /nocturn/data/FEG230530_413

ge.py cretes an excel spreasheet called **master.xlsx** containing meta data as defined by the National Museum of Natural History. 

If **master.xlsx** already exists it will append a new meta data row to the existing spreadsheet. In practice you can run ge.py multiple times to automatically populate the excel spreadsheet with meta data::

        python ge.py /nocturn/data/FEG230509_407        
        python ge.py /nocturn/data/FEG230530_408        
        python ge.py /nocturn/data/FEG230530_409        
        python ge.py /nocturn/data/FEG230530_410        
        python ge.py /nocturn/data/FEG230530_411        
        python ge.py /nocturn/data/FEG230530_412        
        python ge.py /nocturn/data/FEG230530_413

will append to the Sheet1 of master.xlsx the meta data for all samples listed above


.. toctree::

   api/readers.ge


Zeiss Xradia
============

.. image:: img/meta_zeiss.png
    :width: 40%
    :align: center

Zeiss Xradia instrument use a proprietary xrm/txrm data and meta data format. A python reader is avaialble at `DXChange <https://dxchange.readthedocs.io/en/latest/source/api/dxchange.reader.html#dxchange.reader.read_txrm>`_ .


Bruker SkyScan 1272
===================

The Bruker SkyScan 1272 instruments generates .log and .oog files. An example is available at :ref:`Bruker`.

