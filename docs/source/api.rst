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

Scanco
======

Scanco instruments save data and the meta-data in an ISQ file. To extract the meta-data you can use the code example below

Code
----

.. toctree::

   api/readers.scanco


Dependencies
------------

Create a new conda environment::

        conda create --name nocturn python=3.9

and activate the new environment with::

        conda activate nocturn

then install the following packages::

        conda install json
        conda install pathlib
        pip install itk-ioscanco


Run
---

::

        conda activate nocturn
        python scanco.py /nocturn/data/scanco_file.ISQ

will print the meta-data as:

.. code-block:: text

    "CalibrationData": "",
    "CreationDate": "16-AUG-2023 14:32:47.206",
    "DataRange": [
        -21716.0,
        32767.0
    ],
    "Energy": 55.0,
    "Intensity": 0.145,
    "MeasurementIndex": 24292,
    "ModificationDate": "16-AUG-2023 14:32:47.206",
    "MuScaling": 4096.0,
    "MuWater": 0.7032999992370605,
    "NumberOfProjections": 1000,
    "NumberOfSamples": 2000,
    "PatientIndex": 9130,
    "PatientName": "SB_WT_G3955",
    "ReconstructionAlg": 3,
    "ReferenceLine": 37.704,
    "RescaleIntercept": -1000.0,
    "RescaleSlope": 0.34713582434927287,
    "RescaleType": 0,
    "RescaleUnits": "",
    "SampleTime": 200.0,
    "ScanDistance": 12.0,
    "ScannerID": 4274,
    "ScannerType": 10,
    "Site": 4,
    "SliceIncrement": 0.006,
    "SliceThickness": 0.006,
    "Version": "CTDATA-HEADER_V1",
    "direction": [
        [
            1.0,
            0.0,
            0.0
        ],
        [
            0.0,
            1.0,
            0.0
        ],
        [
            0.0,
            0.0,
            1.0
        ]
    ],
    "origin": [
        0.0,
        0.0,
        0.0
    ],
    "spacing": [
        0.006,
        0.006,
        0.006
    ]}



Tomcat
======

Tomcat instruments save data and the meta-data in a json file. To extract the meta-data you can use the code example below

Code
----

.. toctree::

   api/readers.tomcat

Run
---

::

        conda activate nocturn
        python tomcat.py /nocturn/data/tomcat.json

will print the meta-data as:

.. code-block:: text


    {
        "accessGroups": [
            "slstomcat",
            "p19555"
        ],
        "classification": "IN=medium,AV=low,CO=low",
        "contactEmail": "ElseMarie.Friis@nrm.se, peter.crane@yale.edu, krp@geo.au.dk",
        "createdAt": "2023-03-02T16:19:26.096Z",
        "createdBy": "slstomcat",
        "creationTime": "2023-02-23T22:59:34.782Z",
        "datasetName": "S266379\_10x\_",
        "datasetlifecycle": {
            "archivable": false,
            "archiveRetentionTime": "2033-03-02T00:00:00.000Z",
            "archiveStatusMessage": "datasetOnArchiveDisk",
            "dateOfPublishing": "2026-03-02T00:00:00.000Z",
            "isOnCentralDisk": true,
            "publishable": false,
            "publishedOn": "2023-07-10T14:14:21.940Z",
            "retrievable": true,
            "retrieveIntegrityCheck": false,
            "retrieveStatusMessage": ""
        },
        "description": "SRXTM insights into major evolutionary transitions",
        "history": [
            {
                "datasetlifecycle": {
                    "currentValue": {
                        "archivable": "false",
                        "archiveStatusMessage": "started",
                        "retrievable": "false"
                    },
                    "previousValue": {
                        "archivable": false,
                        "archiveRetentionTime": "2033-03-02T00:00:00.000Z",
                        "archiveStatusMessage": "scheduledForArchiving",
                        "dateOfPublishing": "2026-03-02T00:00:00.000Z",
                        "isOnCentralDisk": true,
                        "publishable": false,
                        "retrievable": false,
                        "retrieveIntegrityCheck": false,
                        "retrieveStatusMessage": ""
                    }
                },
                "id": "e8553257-c37c-4b39-922a-0c83a35c3c39",
                "updatedAt": "2023-03-02T19:36:05.542Z",
                "updatedBy": "archiveManager"
            },
            {
                "datasetlifecycle": {
                    "currentValue": {
                        "archivable": "false",
                        "archiveStatusMessage": "datasetOnArchiveDisk",
                        "retrievable": "true"
                    },
                    "previousValue": {
                        "archivable": false,
                        "archiveRetentionTime": "2033-03-02T00:00:00.000Z",
                        "archiveStatusMessage": "started",
                        "dateOfPublishing": "2026-03-02T00:00:00.000Z",
                        "isOnCentralDisk": true,
                        "publishable": false,
                        "retrievable": false,
                        "retrieveIntegrityCheck": false,
                        "retrieveStatusMessage": ""
                    }
                },
                "id": "cb9a2fe8-009a-4088-81b4-755180088dd8",
                "updatedAt": "2023-03-02T19:43:36.763Z",
                "updatedBy": "archiveManager"
            },
            {
                "datasetlifecycle": {
                    "currentValue": {
                        "publishedOn": "2023-07-10T14:14:21.940Z"
                    },
                    "previousValue": {
                        "archivable": false,
                        "archiveRetentionTime": "2033-03-02T00:00:00.000Z",
                        "archiveStatusMessage": "datasetOnArchiveDisk",
                        "dateOfPublishing": "2026-03-02T00:00:00.000Z",
                        "isOnCentralDisk": true,
                        "publishable": false,
                        "retrievable": true,
                        "retrieveIntegrityCheck": false,
                        "retrieveStatusMessage": ""
                    }
                },
                "id": "12fb47ee-5129-47e9-8540-daa925411764",
                "isPublished": {
                    "currentValue": true,
                    "previousValue": false
                },
                "updatedAt": "2023-07-10T14:14:21.945Z",
                "updatedBy": "anonymous"
            }
        ],
        "inputDatasets": [
            "20.500.11935/9e9db9ec-413a-4dcf-8b43-bb6a7663a902"
        ],
        "investigator": "ElseMarie.Friis@nrm.se, peter.crane@yale.edu, krp@geo.au.dk",
        "isPublished": true,
        "license": "CC BY-SA 4.0",
        "numberOfFiles": 2161,
        "numberOfFilesArchived": 2162,
        "owner": "Else Marie Friis, Peter R. Crane, Kaj Raunsgaard Pedersen",
        "ownerEmail": "ElseMarie.Friis@nrm.se, peter.crane@yale.edu, krp@geo.au.dk",
        "ownerGroup": "p19555",
        "packedSize": 5276518400,
        "pid": "20.500.11935/c8fae0ad-270b-46d9-9daf-38fe625f4073",
        "scientificMetadata": {
            "beamlineParameters": {
                "Beam energy": {
                    "u": "keV",
                    "unitSI": "(kg m^2) / s^2",
                    "v": 10,
                    "valueSI": 1.602176565e-15
                },
                "FE-Filter": "No Filter 100%",
                "Monostripe": "Ru/C",
                "OP-Filter1": "No Filter",
                "OP-Filter2": "No Filter",
                "OP-Filter3": "No Filter",
                "Ring current": {
                    "u": "mA",
                    "unitSI": "A",
                    "v": 401.409,
                    "valueSI": 0.401409
                }
            },
            "detectorParameters": {
                "Actual pixel size": {
                    "u": "um",
                    "unitSI": "m",
                    "v": 0.65,
                    "valueSI": 6.5e-07
                },
                "Camera": "PCO.Edge 5.5",
                "Delay time": {
                    "u": "ms",
                    "unitSI": "s",
                    "v": 0,
                    "valueSI": 0
                },
                "Exposure time": {
                    "u": "ms",
                    "unitSI": "s",
                    "v": 150,
                    "valueSI": 0.15
                },
                "Microscope": "Opt.Peter MB op",
                "Microscope x position": {
                    "u": "mm",
                    "unitSI": "m",
                    "v": 138.26,
                    "valueSI": 0.13826
                },
                "Microscope y position": {
                    "u": "mm",
                    "unitSI": "m",
                    "v": -23.71,
                    "valueSI": -0.023710000000000002
                },
                "Microscope z position": {
                    "u": "mm",
                    "unitSI": "m",
                    "v": 52,
                    "valueSI": 0.052000000000000005
                },
                "Millisecond shutter": "not used",
                "Objective": 10,
                "Scintillator": "LuAg:Ce 20um (C20-76)",
                "X-ROI End": 2560,
                "X-ROI Start": 1,
                "Y-ROI End": 2160,
                "Y-ROI Start": 1
            },
            "postProcessingParameters": [
                {
                    "commandLineArgument": {
                        "angle": "0",
                        "angleShift": 0,
                        "anglesFile": "",
                        "axisPositionIn2piScan": "",
                        "binSize": "1,1",
                        "centerOfRotation": "1231.2",
                        "corBandParams": "0.125,0.5,0.5,0.875",
                        "correctionOnly": false,
                        "correctionType": 7,
                        "createMissing": true,
                        "cutoff": "0.5",
                        "darkMedian": false,
                        "decompositionLevel": "0:0",
                        "differenceInStandardDeviation": 0,
                        "doFBPA": false,
                        "doNotCropReconstructions": false,
                        "doSimulateImages": false,
                        "doTestRun": false,
                        "filter": "parz",
                        "firstIndex": 1,
                        "flatMedian": false,
                        "geometry": "6",
                        "gridRecRoiParameters": "726,198,1838,2390",
                        "imageSize": "",
                        "inputSource": "/sls/X02DA/Data10/e19555/disk2/S266379_10x_/S266379_10x_.h5",
                        "inputType": "2",
                        "jsonFile": false,
                        "jsonMetaDataFile": "",
                        "keepSinograms": "0",
                        "logFile": "/sls/X02DA/data/e19555/Data10/disk2/S266379_10x_/S266379_10x_.log",
                        "maxRingWidth": 0,
                        "maxTif": "2.622e-03",
                        "mbaFilterParams": "",
                        "minTif": " -2.594e-03",
                        "moosmannFilterParams": "",
                        "numberOfGPUs": 0,
                        "pSWF_LUT_length": 0,
                        "paganinFilterParams": "",
                        "pathToPixelmaskFile": "",
                        "preFlatsOnly": false,
                        "prefix": "S266379_10x_",
                        "pswf": 0,
                        "recOnlySelect": "0,0",
                        "recOutputDir": "",
                        "reconstruct": "abs",
                        "ringRemoval": "0",
                        "roiParameters": "0,0,0,0",
                        "scaleImageFactor": 1,
                        "scanparameters": "1500,10,100,0,0",
                        "senderReceiverRatio": "8",
                        "separateAngles": "/sls/X02DA/data/e19555/Data10/disk2/S266379_10x_/S266379_10x_.h5",
                        "separateCorrection": "",
                        "shiftCorrection": false,
                        "sigmaInGaussFilter": "0",
                        "sinogramDirectory": "/sls/X02DA/Data10/e19555/disk2/S266379_10x_/sin",
                        "skipPiProj": true,
                        "stepLines": 1,
                        "stitching": "N",
                        "stripeOrientation": "v",
                        "stripeRemoval": "",
                        "thresholdInZinger": 0.95,
                        "tifConversionType": "8",
                        "underSampleSinoFactor": 1,
                        "verbose": 0,
                        "waveletPaddingMode": "0",
                        "waveletType": "0",
                        "widthOfSmoothingKernel": 9,
                        "zeroPadding": "0.5",
                        "zinger": ""
                    },
                    "gitRepositoryLink": "f9e3d5f356f014a4d55c53901f2ba9c5dbdea97e",
                    "postProcessingTimestamp": "2023-02-23T22:59:34.782Z"
                }
            ],
            "scanParameters": {
                "Angular step": {
                    "u": "deg",
                    "unitSI": "rad",
                    "v": 0.12,
                    "valueSI": 0.0020943951023931952
                },
                "File Prefix": "S266379_10x_",
                "Flat frequency": 0,
                "Number of darks": 10,
                "Number of flats": 100,
                "Number of inter-flats": 0,
                "Number of projections": 1500,
                "Raw Source": "/sls/X02DA/Data10/e19555/disk2/S266379_10x_/",
                "Rot Y max position": {
                    "u": "deg",
                    "unitSI": "rad",
                    "v": 180,
                    "valueSI": 3.141592653589793
                },
                "Rot Y min position": {
                    "u": "deg",
                    "unitSI": "rad",
                    "v": 0,
                    "valueSI": 0
                },
                "Rotation axis position": "Standard",
                "Sample In": {
                    "u": "um",
                    "unitSI": "m",
                    "v": 0,
                    "valueSI": 0
                },
                "Sample Out": {
                    "u": "um",
                    "unitSI": "m",
                    "v": 5000,
                    "valueSI": 0.005
                },
                "Sample folder": "/sls/X02DA/data/e19555/Data10/disk2/S266379_10x_/",
                "Sample holder X-position": {
                    "u": "um",
                    "unitSI": "m",
                    "v": 7835.4,
                    "valueSI": 0.0078354
                },
                "Sample holder Y-position": {
                    "u": "um",
                    "unitSI": "m",
                    "v": 2560.1,
                    "valueSI": 0.0025600999999999996
                }
            }
        },
        "size": 5272583164,
        "sourceFolder": "/sls/X02DA/Data10/e19555/disk2/S266379_10x_/rec_8bit_abs",
        "sourceFolderHost": "x02da-cons-bl-9.psi.ch",
        "techniques": [],
        "type": "derived",
        "updatedAt": "2023-07-10T14:14:23.015Z",
        "updatedBy": "anonymous",
        "usedSoftware": [
            "Schindelin, J.; Arganda-Carreras, I. & Frise, E. et al. (2012), \"Fiji: an open-source platform for biological-image analysis\", Nature methods 9(7): 676-682, PMID 22743772, doi:10.1038/nmeth.2019",
            "Marone, F. et al. (2017), \"Towards on-the-fly data post-processing for real-time tomographic imaging at TOMCAT\", Advanced Structural and Chemical Imaging 3(1): 1, doi:10.1186/s40679-016-0035-9"
        ],
        "version": "3.1.0"
    }



Zeiss Xradia
============

.. image:: img/meta_zeiss.png
    :width: 40%
    :align: center

Zeiss Xradia instrument use a proprietary xrm/txrm data and meta data format. A python reader is avaialble at `DXChange <https://dxchange.readthedocs.io/en/latest/source/api/dxchange.reader.html#dxchange.reader.read_txrm>`_ .


Bruker SkyScan 1272
===================

The Bruker SkyScan 1272 instruments generates .log files for data collection and data analysis. An example is available at :ref:`Bruker`.

