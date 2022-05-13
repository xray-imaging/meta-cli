#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: meta.py
   :platform: Unix
   :synopsis: Reads the meta data of a tomographic hdf5 file and generates a table (rst) compatible with sphynx/readthedocs.

"""

import os
import sys
import pathlib 
import argparse
import numpy as np
import meta

from datetime import datetime

from meta_cli import log
from meta_cli import config
from meta_cli import utils

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

def init(args):
    if not os.path.exists(str(args.config)):
        config.write(str(args.config))
    else:
        raise RuntimeError("{0} already exists".format(args.config))

def status(args):
    config.show_config(args)

def run_show(args):

    error = 0
    file_path = pathlib.Path(args.file_name)
    if file_path.is_file():
        log.info("Publishing a single file: %s" % args.file_name)  
        tree, meta_dict = meta.read_hdf(args.file_name)
        for entry in meta_dict:
            # print(type(entry))
            if meta_dict[entry][1] == None or type(meta_dict[entry][0]) == str:
                print(f'{bcolors.OKGREEN}{entry} {bcolors.OKBLUE}{meta_dict[entry][0]}{bcolors.ENDC}')
            else:
                if np.isnan(meta_dict[entry][0]):
                    error += 1
                    print(f'{bcolors.OKGREEN}{entry} {bcolors.FAIL}{meta_dict[entry][0]} {meta_dict[entry][1]}{bcolors.ENDC}')
                else:
                    print(f'{bcolors.OKGREEN}{entry} {bcolors.WARNING}{meta_dict[entry][0]} {meta_dict[entry][1]}{bcolors.ENDC}')
        if error > 0:
            log.error("Found %d PVs listed has having valid units but containing a NaN value. Please check the detector XML attribute file" % error)              
    elif file_path.is_dir():
        log.info("publishing a multiple files in: %s" % args.file_name)
        top = os.path.join(args.file_name, '')
        h5_file_list = list(filter(lambda x: x.endswith(('.h5', '.hdf', 'hdf5')), os.listdir(top)))
        h5_file_list_sorted = sorted(h5_file_list, key = lambda x: x.split('_')[-1])
        if (h5_file_list):
            # h5_file_list.sort()
            log.info("found: %s" % h5_file_list_sorted) 
            index=0
            for fname in h5_file_list_sorted:
                args.file_name = top + fname
                log.warning("  *** file %d/%d;  %s" % (index, len(h5_file_list_sorted), fname))
                index += 1
                tree, meta_dict = meta.read_hdf(args.file_name)
                error = 0
                for entry in meta_dict:
                    if meta_dict[entry][1] == None or type(meta_dict[entry][0]) == str:
                        print(f'{bcolors.OKGREEN}{entry} {bcolors.OKBLUE}{meta_dict[entry][0]}{bcolors.ENDC}')
                    else:
                        if np.isnan(meta_dict[entry][0]):
                            error += 1
                            print(f'{bcolors.OKGREEN}{entry} {bcolors.FAIL}{meta_dict[entry][0]} {meta_dict[entry][1]}{bcolors.ENDC}')
                        else:
                            print(f'{bcolors.OKGREEN}{entry} {bcolors.WARNING}{meta_dict[entry][0]} {meta_dict[entry][1]}{bcolors.ENDC}')
                if error > 0:
                    log.error("Found %d PVs listed has having valid units but containing a NaN value. Please check the detector XML attribute file" % error)
        else:
            log.error("directory %s does not contain any file" % args.file_name)
    else:
        log.error("directory or File Name does not exist: %s" % args.file_name)

def run_tree(args):
    tree, meta_dict = meta.read_hdf(args.file_name)
    for entry in tree:
        # log.info(entry)
        print(entry)

def run_docs(args):
    utils.create_rst_file(args)

def main():
    home = os.path.expanduser("~")
    logs_home = home + '/logs/'

    # make sure logs directory exists
    if not os.path.exists(logs_home):
        os.makedirs(logs_home)

    lfname = logs_home + 'meta_' + datetime.strftime(datetime.now(), "%Y-%m-%d_%H:%M:%S") + '.log'
    log.setup_custom_logger(lfname)

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', **config.SECTIONS['general']['config'])
    show_params = config.meta_PARAMS
    docs_params = config.meta_PARAMS

    cmd_parsers = [
        ('init',        init,           (),                             "Create configuration file"),
        ('status',      status,         show_params,                    "Show meta status"),
        ('show',        run_show,       show_params,                    "Show meta data extracted from --file-name"),
        ('tree',        run_tree,       show_params,                    "Show meta data tree extracted from --file-name"),
        ('docs',        run_docs,       docs_params,                    "Create in --doc-dir an rst file compatible with sphinx/readthedocs containing the DataExchange hdf file meta data"),
    ]

    subparsers = parser.add_subparsers(title="Commands", metavar='')

    for cmd, func, sections, text in cmd_parsers:
        cmd_params = config.Params(sections=sections)
        cmd_parser = subparsers.add_parser(cmd, help=text, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        cmd_parser = cmd_params.add_arguments(cmd_parser)
        cmd_parser.set_defaults(_func=func)

    args = config.parse_known_args(parser, subparser=True)
  
    try:
        # load args from default (config.py) if not changed
        config.log_values(args)
        args._func(args)
        # undate meta5.config file
        sections = config.meta_PARAMS
        config.write(args.config, args=args, sections=sections)
    except RuntimeError as e:
        log.error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()