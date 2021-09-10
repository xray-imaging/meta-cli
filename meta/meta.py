import os
import sys
import argparse
import datetime

import pandas as pd
import dxchange.reader as dxreader

from pathlib import Path
from meta import log


def show_meta(args):

    fname = args.h5_name
    if os.path.isfile(fname): 
        all_meta = dxreader.read_dx_meta(fname) 
        log.info('All meta data available in the HDF5 raw data file: start')
        log.info(all_meta)
        log.info('All meta data available in the HDF5 raw data file: end')
    meta, year_month, pi_name = extract_meta(args)
    if meta != None:
        log.info('All meta data extracted from the HDF5 raw data file:')
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

    list_to_extract = ('experimenter_name', 'start_date', 'end_date', 'full_file_name', 'sample_in_x', 'sample_in_y', 'proposal', 'sample_name', 'sample_y', 'camera_objective', 'resolution', 'energy', 'camera_distance', 'exposure_time', 'num_angles', 'scintillator_type', 'model')
    list_to_extract = ('attenuator_name', 'user_filter_ds', 'user_filter_ds_legend', 'user_filter_us', 'user_filter_us_legend', 'attenuator_1_name', 'description', 
        'camera_motor_stack_name', 'camera_distance', 'camera_objective', 'camera_tube_length', 'resolution', 'scintillating_thickness', 'scintillator_type', 'ADcore_version', 
        'HDFplugin_version', 'SDK_version', 'acquire_period', 'array_counter', 'binning_x', 'binning_y', 'convert_pixel_format', 'dimension_x', 'dimension_y', 'driver_version', 
        'exposure_time', 'firmware_version', 'frame_rate', 'frame_rate_enable', 'gain', 'gain_auto', 'manufacturer', 'model', 'pixel_format', 'pixel_size', 'microns', 'min_x', 'min_y', 
        'size_x', 'size_y', 'serial_number', 'temperature', 'instrument_name', 'mirror_name', 'mirror_angle', 'mirror_dsy', 'mirror_usy', 'mirror_x', 'mirror_y', 'stripe', 'stripe_legend', 
        'Energy_list', 'USArm_list', 'energy', 'energy_mode', 'energy_mode_legend', 'monochromator_name', 'dmm_ds_arm', 'dmm_m2_y', 'dmm_m2_z', 'dmm_table_ds_y', 
        'dmm_table_usy_ib', 'dmm_table_usy_ob', 'dmm_us_arm', 'sample_motor_stack_name', 'sample_pitch', 'sample_roll', 'sample_rotary', 'sample_x', 'sample_x_cent', 'sample_y', 'sample_z_cent', 
        'hslits_ds_center', 'hslits_ds_size', 'hslits_us_center', 'hslits_us_size', 'vslits_ds_center', 'vslits_ds_size', 'vslits_us_center', 'vslits_us_size', 'slits_name', 'beamline', 
        'current', 'fill_mode', 'source_name', 'top_up', 'description_1', 'description_2', 'description_3', 'ESAF_number', 'proposal', 'title', 'email', 'experimenter_name', 'facility_user_id', 
        'institution', 'file_name', 'file_path', 'full_file_name', 'sample_name', 'dark_field_mode', 'dark_field_value', 'num_dark_fields', 'end_date', 'flat_field_axis', 'flat_field_mode', 
        'flat_field_value', 'num_flat_fields', 'sample_in_x', 'sample_in_y', 'sample_out_x', 'sample_out_y', 'num_angles', 'return_rotation', 'rotation_speed', 'rotation_start', 'rotation_step', 'start_date')

    # list_to_extract = ('experimenter_name', 'full_file_name', 'description_1', 'description_2', 'resolution', 'energy', 'start_date','sample_pitch', 'sample_roll')
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

