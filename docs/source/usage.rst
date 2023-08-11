Usage
=====

View the hdf tree
-----------------

To view the data tree contained in a generic hdf file:

::

    $ meta tree --file-name data/base_file_name_001.h5 

.. image:: img/meta_tree.png
    :width: 40%
    :align: center


View the meta data
------------------

To view the meta data contained in a generic hdf file:

::

    $ meta show --file-name data/base_file_name_001.h5 


.. image:: img/meta_show.png
    :width: 40%
    :align: center

View a subset meta data
-----------------------

To view a subset of the meta data contained in a generic hdf file:

::

    $ meta show --file-name data/base_file_name_001.h5 --key energy


Replace an hdf entry value
--------------------------

To replace the value of an entry:

 ::

    $ meta set --file-name data/base_file_name_001.h5 --key /process/acquisition/rotation/rotation_start --value 10


Meta data rst table
-------------------

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
------------------

meta parameters are stored in **meta.conf**. You can create a template with::

    $ meta init

**meta.conf** is constantly updated to keep track of the last stored parameters, as initalized by **init** or modified by setting a new option value. For example to re-run the last meta with identical --file-name parameters used before just use::

    $ meta docs

