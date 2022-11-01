# #########################################################################
# Copyright (c) 2022, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2022. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################

import os
import h5py
import meta
import datetime
import numpy as np
import pandas as pd
from meta_cli import log

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
    list_to_extract = ('/measurement/instrument/monochromator/energy', 
                    '/measurement/sample/experimenter/email',
                    '/measurement/instrument/sample_motor_stack/setup/x', 
                    '/measurement/instrument/sample_motor_stack/setup/y'
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

    df = pd.DataFrame.from_dict(meta_dict, orient='index', columns=('value', 'unit'))
    return df.to_markdown(tablefmt='grid'), year_month, pi_name

def extract_dict(fname, list_to_extract, index=0):

    tree, meta_data = meta.read_hdf(fname)

    start_date     = '/process/acquisition/start_date'
    experimenter   = '/measurement/sample/experimenter/name'
    full_file_name = '/measurement/sample/file/full_name'

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

def show_entry(meta_dict, entry):
    if entry.find('exchange') != -1:
        log.error("Found 1D array at %s" % entry)
    else:
        try:
            if meta_dict[entry][1] == None or type(meta_dict[entry][0]) == str:
                print(f'{bcolors.OKGREEN}{entry} {bcolors.OKBLUE}{meta_dict[entry][0]}{bcolors.ENDC}')
            else:
                if np.isnan(meta_dict[entry][0]):
                    error += 1
                    print(f'{bcolors.OKGREEN}{entry} {bcolors.FAIL}{meta_dict[entry][0]} {meta_dict[entry][1]}{bcolors.ENDC}')
                else:
                    print(f'{bcolors.OKGREEN}{entry} {bcolors.WARNING}{meta_dict[entry][0]} {meta_dict[entry][1]}{bcolors.ENDC}')
        except ValueError:
            log.error('One of the /exchange data array has dims (1,:,:)')

def swap(args, entry):

    if args.value is not None:
        with h5py.File(args.file_name, "r+") as f:
            data = list(f[entry])
            data = f[entry]
            log.warning("Old %s: %s" % (entry, data[0]))
            data[0] = args.value
            log.warning("New %s: %s" % (entry, data[0]))

    else:
        log.error('Set --value to make a change to %s', entry)