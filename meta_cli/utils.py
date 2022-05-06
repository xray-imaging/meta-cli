import os
import meta
import datetime
import pandas as pd
from meta_cli import log


def add_header(label):

    header = add_decorator(label) + '\n' + label + '\n' + add_decorator(label) + '\n\n'

    return header

def add_title(label):

    title = label + '\n' + add_decorator(label, decorator='-') + '\n\n' 

    return title


def add_decorator(label, decorator='='):
    
    return decorator.replace(decorator, decorator*len(label))

def create_rst_file(args):
    
    meta_data, year_month, pi_name = extract_rst_meta(args)

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
        f.write(meta_data)        
        f.write('\n\n')        
    log.warning('Please copy/paste the content of %s in your rst docs file' % (log_fname))

def extract_rst_meta(args):

    # Customize this list to add more meta_data in the rst table.
    # To see the full list of available meta_data run:
    # meta show --file-name myfile.h5
    list_to_extract = ('measurement_instrument_monochromator_energy', 
                    'measurement_sample_experimenter_email',
                    'measurement_instrument_sample_motor_stack_setup_x', 
                    'measurement_instrument_sample_motor_stack_setup_y'
                    )

    # set pandas display
    pd.options.display.max_rows = 999
    year_month = 'unknown'
    pi_name    = 'unknown'
    fname      = args.file_name

    if os.path.isfile(fname): 
        meta_dict, year_month, pi_name = extract_dict(fname, list_to_extract)
        # print (meta_dict, year_month, pi_name)
        # exit()
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

    df = pd.DataFrame.from_dict(meta_dict, orient='index', columns=('hdf path', 'value', 'unit'))
    return df.to_markdown(tablefmt='grid'), year_month, pi_name

def extract_dict(fname, list_to_extract, index=0):

    tree, meta_data = meta.read_hdf(fname)

    start_date     = 'process_acquisition_start_date'
    experimenter   = 'measurement_sample_experimenter_name'
    full_file_name = 'measurement_sample_file_full_name'

    try: 
        dt = datetime.datetime.strptime(meta_data[start_date][0], "%Y-%m-%dT%H:%M:%S%z")
        year_month = str(dt.year) + '-' + '{:02d}'.format(dt.month)
    except ValueError:
        log.error("The start date information is missing from the hdf file %s. Error (2020-01)." % fname)
        year_month = '2020-01'
    except TypeError:
        log.error("The start date information is missing from the hdf file %s. Error (2020-02)." % fname)
        year_month = '2020-02'
    try:
        pi_name = meta_data[experimenter][0]
    except KeyError:
        log.error("The experimenter name is missing from the hdf file %s." % fname)
        pi_name = 'Unknown'
    try:    
        # compact full_file_name to file name only as original data collection directory may have changed
        meta_data[full_file_name][0] = os.path.basename(meta_data[full_file_name][0])
    except KeyError:
        log.error("The full file name is missing from the hdf file %s." % fname)

    sub_dict = {(('%3.3d' % index) +'_' + k):v for k, v in meta_data.items() if k in list_to_extract}

    return sub_dict, year_month, pi_name
