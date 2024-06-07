#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: meta.py
   :platform: Unix
   :synopsis: Reads the meta data of a tomographic hdf5 file and generates a table (rst) compatible with sphynx/readthedocs.

"""

import re
import os
import sys
import pathlib 
import meta
import click

from datetime import datetime

from meta_cli import log
from meta_cli import config
from meta_cli import utils

@click.group()
def cli():
    pass

@cli.command()
@click.option('--config-file-name', default=str(os.path.join(str(pathlib.Path.home()), 'meta.conf')), help='Name of the configuration file.')
def init(config_file_name):
    if not os.path.exists(config_file_name):
        config.write(config_file_name)
    else:
        log.error("{0} already exists".format(config_file_name))

@cli.command()
@click.option('--file-name', default='.', help="An hdf5 file or directory containing multiple hdf5 files, e.g. /data/sample.h5 or /data/")
@click.option('--key', default='', help="When set only tags containing key are shown")
def show(file_name, key):
    errors = 0
    file_path = pathlib.Path(file_name)
    if file_path.is_file():
        mp = meta.read_meta.Hdf5MetadataReader(file_name)
        meta_dict = mp.readMetadata()
        mp.close()
        for entry in meta_dict:
            if key == '':
                errors += utils.show_entry(meta_dict, entry)
            else:
                if key in entry:
                    errors += utils.show_entry(meta_dict, entry)
        if errors > 0:
            log.error("Found %d PVs listed has having valid units but containing a NaN value. The EPICS IOC associted with these PVs was not running during data collections." % errors)
    elif file_path.is_dir():
        log.info("publishing a multiple files in: %s" % file_name)
        top = os.path.join(args.file_name, '')
        h5_file_list = list(filter(lambda x: x.endswith(('.h5', '.hdf', 'hdf5')), os.listdir(top)))
        h5_file_list_sorted = sorted(h5_file_list, key = lambda x: x.split('_')[-1])
        if (h5_file_list):
            # h5_file_list.sort()
            log.info("found: %s" % h5_file_list_sorted) 
            index=0
            for fname in h5_file_list_sorted:
                file_name = top + fname
                log.warning("  *** file %d/%d;  %s" % (index, len(h5_file_list_sorted), fname))
                index += 1
                mp = meta.read_meta.Hdf5MetadataReader(file_name)
                meta_dict = mp.readMetadata()
                error = 0
                for entry in meta_dict:
                    if key == '':
                        errors += utils.show_entry(meta_dict, entry)
                    else:
                        if key in entry:
                            errors += utils.show_entry(meta_dict, entry)
                if errors > 0:
                    log.error("Found %d PVs listed has having valid units but containing a NaN value. The EPICS IOC associted with these PVs was not running during data collections." % errors)

        else:
            log.error("directory %s does not contain any file" % file_name)
    else:
        log.error("directory or file name does not exist: %s" % file_name)

@cli.command()
@click.option('--file-name', default='.', help="An hdf5 file, e.g. /data/sample.h5")
@click.option('--key', default='', help="Key entry to be modified")
@click.option('--value', default=None, help="Value to replace the original key entry")
def set(file_name):

    file_path = pathlib.Path(file_name)
    if file_path.is_file():
        mp = meta.read_meta.Hdf5MetadataReader(file_name)
        meta_dict = mp.readMetadata()
        mp.close()

        error = 0
        for entry in meta_dict:
            # print(type(entry))
            # print(entry)
            if key == entry:
                log.info("%s does match a hdf file tag" % key)
                utils.swap(file_name, entry, value)
                return
            else:
                error = 1
        if error == 1:
            log.error("%s does not match any hdf file tag" % key)
    else:
        log.error("file %s does not exist" % file_name)


@cli.command()
@click.option('--file-name', default='.', help="An hdf5 file, e.g. /data/sample.h5")
def tree(file_name):
    tree = meta.get_hdf_tree(file_name, display=False)
    for entry in tree:
        log.info(entry)

@cli.command()
@click.option('--file-name', default='.', help="An hdf5 file, e.g. /data/sample.h5")
def docs(file_name):
    utils.create_rst_file(file_name)

def main():
    home = os.path.expanduser("~")
    logs_home = home + '/logs/'

    # make sure logs directory exists
    if not os.path.exists(logs_home):
        os.makedirs(logs_home)

    lfname = logs_home + 'meta_' + datetime.strftime(datetime.now(), "%Y-%m-%d_%H:%M:%S") + '.log'
    log.setup_custom_logger(lfname)

    cli()

if __name__ == "__main__":
    main()
