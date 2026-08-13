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

import datetime

import h5py
import numpy as np
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


def _mark_stale_start_date(meta_data):
    """Detect and mark stale /process/acquisition/start_date in-place.

    The XML-based DateTimeStart NDAttribute in older tomoscan deployments
    used when="OnFileOpen", which reads the last-cached NDArray timestamp.
    Between scans no NDArrays flow, so start_date froze at the previous
    scan's last-frame time (off by seconds to days).

    Heuristic: if the implied duration (end - start) is more than 3x the
    physical acquisition duration + 300 s, treat start_date as stale.
    Physical = num_angles*acquire_period + num_dark*exp + num_flat*flat_exp
                + 30 s (motion/shutter overhead).

    When stale, replace start_date's value with a derived timestamp
    (end - physical) plus the marker " [derived]" so any downstream
    formatter (show_entry, table, rst) makes the substitution visible.
    """
    fmt = "%Y-%m-%dT%H:%M:%S%z"
    key_start = '/process/acquisition/start_date'
    key_end   = '/process/acquisition/end_date'
    if key_start not in meta_data or key_end not in meta_data:
        return
    try:
        start = datetime.datetime.strptime(meta_data[key_start][0], fmt)
        end   = datetime.datetime.strptime(meta_data[key_end  ][0], fmt)
    except (ValueError, TypeError, KeyError):
        return

    def _num(key, default=0):
        try: return float(meta_data[key][0])
        except (KeyError, ValueError, TypeError): return default

    n_proj    = _num('/process/acquisition/rotation/num_angles', 0)
    n_dark    = _num('/process/acquisition/dark_fields/number', 0)
    n_flat    = _num('/process/acquisition/flat_fields/number', 0)
    period    = _num('/measurement/instrument/detector/acquire_period', 0)
    expo      = _num('/measurement/instrument/detector/exposure_time', period)
    flat_expo = _num('/process/acquisition/flat_fields/flat_exposure_time', expo)

    physical = n_proj * period + n_dark * expo + n_flat * flat_expo + 30.0
    span = (end - start).total_seconds()
    if physical <= 0 or span <= 3 * physical + 300:
        return

    derived = (end - datetime.timedelta(seconds=physical)).strftime(fmt)
    meta_data[key_start] = (derived + ' [derived]', meta_data[key_start][1])


def show_entry(meta_dict, entry):
    error = 0
    if entry.find('exchange') != -1:
        log.error("Found 1D array at %s" % entry)
    else:
        try:
            if meta_dict[entry][1] == None or type(meta_dict[entry][0]) == str:
                print(f'{bcolors.OKGREEN}{entry} {bcolors.OKBLUE}{meta_dict[entry][0]}{bcolors.ENDC}')
            else:
                if np.isnan(meta_dict[entry][0]):
                    error = 1
                    print(f'{bcolors.OKGREEN}{entry} {bcolors.FAIL}{meta_dict[entry][0]} {meta_dict[entry][1]}{bcolors.ENDC}')
                else:
                    print(f'{bcolors.OKGREEN}{entry} {bcolors.WARNING}{meta_dict[entry][0]} {meta_dict[entry][1]}{bcolors.ENDC}')
        except ValueError:
            log.error('One of the /exchange data array has dims (1,:,:)')

    return error

def swap(file_name, entry, value):

    if value is not None:
        with h5py.File(file_name, "r+") as f:
            data = list(f[entry])
            data = f[entry]
            if isinstance(data[0], float):
                log.warning("Old %s: %s" % (entry, data[0]))
                data[0] = value
                log.warning("New %s: %s" % (entry, data[0]))
            else:
                log.error('Only floating point variable can be modified')
    else:
        log.error('Set --value to make a change to %s', entry)