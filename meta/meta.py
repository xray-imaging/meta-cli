import os
import sys
import h5py
import argparse
import datetime

import pandas as pd
import dxchange.reader as dxreader

from collections import OrderedDict, deque
from pathlib import Path
from meta import log

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

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
    try: 
        dt = datetime.datetime.strptime(meta['start_date'][0], "%Y-%m-%dT%H:%M:%S%z")
        year_month = str(dt.year) + '-' + '{:02d}'.format(dt.month)
    except ValueError:
        log.error("The start date information is missing from the hdf file %s. Error (2020-01)." % fname)
        year_month = '2020-01'
    except TypeError:
        log.error("The start date information is missing from the hdf file %s. Error (2020-02)." % fname)
        year_month = '2020-02'
    try:
        pi_name = meta['experimenter_name'][0]
    except KeyError:
        log.error("The experimenter name is missing from the hdf file %s." % fname)
        pi_name = 'Unknown'
    try:    
        # compact full_file_name to file name only as original data collection directory may have changed
        meta['full_file_name'][0] = os.path.basename(meta['full_file_name'][0])
    except KeyError:
        log.error("The full file name is missing from the hdf file %s." % fname)

    # sub_dict = {k:v for k, v in meta.items() if k in list_to_extract}
    sub_dict = {(('%3.3d' % index) +'_' + k):v for k, v in meta.items() if k in list_to_extract}

    return sub_dict, year_month, pi_name
    

def extract_meta(args):

    fname = args.h5_name

    # list_to_extract = ('experimenter_name', 'start_date', 'end_date', 'full_file_name', 'sample_in_x', 'sample_in_y', 'proposal', 'sample_name', 'sample_y', 'camera_objective', 'resolution', 'energy', 'camera_distance', 'exposure_time', 'num_angles', 'scintillator_type', 'model')
    # list_to_extract = ('experimenter_name', 'full_file_name', 'description_1', 'description_2', 'resolution', 'energy', 'start_date','sample_pitch', 'sample_roll')
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

def _get_subgroups(hdf_object, key=None):
    """
    Supplementary method for building the tree view of a hdf5 file.
    Return the name of subgroups.
    """
    list_group = []
    if key is None:
        for group in hdf_object.keys():
            list_group.append(group)
        if len(list_group) == 1:
            key = list_group[0]
        else:
            key = ""
    else:
        if key in hdf_object:
            try:
                obj = hdf_object[key]
                if isinstance(obj, h5py.Group):
                    for group in hdf_object[key].keys():
                        list_group.append(group)
            except KeyError:
                pass
    if len(list_group) > 0:
        list_group = sorted(list_group)
    return list_group, key

def _add_branches(tree, hdf_object, key, key1, index, last_index, prefix,
                  connector, level, add_shape):
    """
    Supplementary method for building the tree view of a hdf5 file.
    Add branches to the tree.
    """
    shape = None
    key_comb = key + "/" + key1
    if add_shape is True:
        if key_comb in hdf_object:
            try:
                obj = hdf_object[key_comb]
                if isinstance(obj, h5py.Dataset):
                    shape = str(obj.shape)
            except KeyError:
                shape = str("-> ???External-link???")
    if shape is not None:
        tree.append(f"{prefix}{connector} {key1} {shape}")
    else:
        tree.append(f"{prefix}{connector} {key1}")
    if index != last_index:
        prefix += PIPE_PREFIX
    else:
        prefix += SPACE_PREFIX
    _make_tree_body(tree, hdf_object, prefix=prefix, key=key_comb,
                    level=level, add_shape=add_shape)

def _make_tree_body(tree, hdf_object, prefix="", key=None, level=0,
                    add_shape=True):
    """
    Supplementary method for building the tree view of a hdf5 file.
    Create the tree body.
    """
    entries, key = _get_subgroups(hdf_object, key)
    num_ent = len(entries)
    last_index = num_ent - 1
    level = level + 1
    if num_ent > 0:
        if last_index == 0:
            key = "" if level == 1 else key
            if num_ent > 1:
                connector = PIPE
            else:
                connector = ELBOW if level > 1 else ""
            _add_branches(tree, hdf_object, key, entries[0], 0, 0, prefix,
                          connector, level, add_shape)
        else:
            for index, key1 in enumerate(entries):
                connector = ELBOW if index == last_index else TEE
                if index == 0:
                    tree.append(prefix + PIPE)
                _add_branches(tree, hdf_object, key, key1, index, last_index,
                              prefix, connector, level, add_shape)

def get_hdf_tree(args, output=None, add_shape=True, display=True):
    """
    Get the tree view of a hdf/nxs file.

    Parameters
    ----------
    file_path : str
        Path to the file.
    output : str or None
        Path to the output file in a text-format file (.txt, .md,...).
    add_shape : bool
        Including the shape of a dataset to the tree if True.
    display : bool
        Print the tree onto the screen if True.

    Returns
    -------
    list of string
    """
    file_path = args.h5_name
    hdf_object = h5py.File(file_path, 'r')
    tree = deque()
    _make_tree_body(tree, hdf_object, add_shape=add_shape)
    if output is not None:
        make_folder(output)
        output_file = open(output, mode="w", encoding="UTF-8")
        with output_file as stream:
            for entry in tree:
                print(entry, file=stream)
    else:
        if display:
            for entry in tree:
                print(entry)
    return tree
