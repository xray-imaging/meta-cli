import os
import sys
import argparse
import datetime

import pandas as pd
import dxchange.reader as dxreader

from pathlib import Path
from metah5 import log


def show_meta(args):

    meta, year_month, pi_name = extract_meta(args)
    if meta != None:
        print(meta)

def add_header(label):

    header = add_decorator(label) + '\n' + label + '\n' + add_decorator(label) + '\n\n'

    return header

def add_title(label):

    title = label + '\n' + add_decorator(label, decorator='-') + '\n\n' 

    return title


def add_decorator(label, decorator='='):
    
    return decorator.replace(decorator, decorator*len(label))
 

def create_rst_file(args):
    
    meta, year_month, pi_name = extract_meta(args)

    decorator = '='
    if os.path.isdir(args.doc_dir):
        log_fname = os.path.join(args.doc_dir, 'log_' + year_month + '.rst')

    with open(log_fname, 'a') as f:
        if f.tell() == 0:
            # a new file or the file was empty
            f.write(add_header(year_month))
            f.write(add_title(pi_name))
        else:
            #  file existed, appending
            f.write(add_title(pi_name))
        f.write('\n')        
        f.write(meta)        
        f.write('\n\n')        
    print(log_fname)

def extract_dict(fname, list_to_extract, index=0):

    meta = dxreader.read_dx_meta(fname) 
    # print(meta)
    try: 
        dt = datetime.datetime.strptime(meta['start_date'][0], "%Y-%m-%dT%H:%M:%S%z")
        year_month = str(dt.year) + '-' + '{:02d}'.format(dt.month)
    except ValueError:
        log.error("The start date information is missing from the hdf file %s. Error (2020-01)." % fname)
        year_month = '2020-01'
    except TypeError:
        log.error("The start date information is missing from the hdf file %s. Error (2020-02)." % fname)
        year_month = '2020-02'
    pi_name = meta['experimenter_name'][0]

    # compact full_file_name to file name only as original data collection directory may have changed
    meta['full_file_name'][0] = os.path.basename(meta['full_file_name'][0])

    # sub_dict = {k:v for k, v in meta.items() if k in list_to_extract}
    sub_dict = {(('%3.3d' % index) +'_' + k):v for k, v in meta.items() if k in list_to_extract}

    return sub_dict, year_month, pi_name
    

def extract_meta(args):

    fname = args.h5_name

    list_to_extract = ('experimenter_name', 'start_date', 'end_date', 'full_file_name',  'sample_in_x', 'sample_in_y', 'proposal', 'sample_name', 'sample_y', 'camera_objective', 'resolution', 'energy', 'camera_distance', 'exposure_time', 'num_angles', 'scintillator_type', 'model')
    # set pandas display
    pd.options.display.max_rows = 999
    year_month = 'unknown'
    pi_name = 'unknown'
    if os.path.isfile(fname): 
        meta_dict, year_month, pi_name = extract_dict(fname, list_to_extract)
        # print (meta_dict, year_month, pi_name)
    elif os.path.isdir(fname):
        # Add a trailing slash if missing
        top = os.path.join(fname, '')
        # Set the file name that will store the rotation axis positions.
        h5_file_list = list(filter(lambda x: x.endswith(('.h5', '.hdf')), os.listdir(top)))
        h5_file_list.sort()
        meta_dict = {}
        file_counter=0
        for fname in h5_file_list:
            h5fname = top + fname
            sub_dict, year_month, pi_name = extract_dict(h5fname, list_to_extract, index=file_counter)
            meta_dict.update(sub_dict)
            file_counter+=1
        if year_month == 'unknown':
            log.error('No valid HDF5 file(s) fund in the directory %s' % top)
            log.warning('Make sure to use the --h5-name H5_NAME  option to select  the hdf5 file or directory containing multiple hdf5 files')
            return None
           
    else:
        log.error('No valid HDF5 file(s) fund')
        return None


    df = pd.DataFrame.from_dict(meta_dict, orient='index', columns=('value', 'unit'))
    return df.to_markdown(tablefmt='grid'), year_month, pi_name

