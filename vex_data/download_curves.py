#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import logging
import os
import re
import requests
import zipfile

from pathlib import Path
from urllib.parse import urlparse

# yapf: disable
files = {'cim':      ['https://content.vexrobotics.com/motors/217-2000-cim/cim-motor-curve-data-20151104.csv',
                      'https://content.vexrobotics.com/motors/217-2000-cim/cim-peak-power-data-20151104.csv',
                      'https://content.vexrobotics.com/motors/217-2000-cim/cim-locked-rotor-data-20151104.zip'],
         'mini-cim': ['https://content.vexrobotics.com/motors/217-3371-mini-cim/mini-cim-motor-curve-data-20151207.csv',
                      'https://content.vexrobotics.com/motors/217-3371-mini-cim/mini-cim-peak-power-data-20151207.csv',
                      'https://content.vexrobotics.com/motors/217-3371-mini-cim/mini-cim-locked-rotor-data-20151209-2.zip'],
         '775pro':   ['https://content.vexrobotics.com/motors/217-4347-775pro/775pro-motor-curve-data-20151208.csv',
                      'https://content.vexrobotics.com/motors/217-4347-775pro/775pro-peak-power-data-20151210.csv',
                      'https://content.vexrobotics.com/motors/217-4347-775pro/775pro-locked-rotor-data-20151209.zip'],
         'bag':      ['https://content.vexrobotics.com/motors/217-3351-bag/bag-motor-curve-data-20151207.csv',
                      'https://content.vexrobotics.com/motors/217-3351-bag/bag-peak-power-data-20151207.csv',
                      'https://content.vexrobotics.com/motors/217-3351-bag/bag-locked-rotor-data-20151207.zip']}
# yapf: enable

def file_exists(file_path):
    try:
        if os.stat("file").st_size != 0:
            return True
    except FileNotFoundError:
        pass
    return False


def unzip_file(path):
    path = Path(path)
    if path.suffix == '.zip':
        logging.info('Unzipping %s to %s', path, path.parent)
        with zipfile.ZipFile(str(path), 'r') as zip_ref:
            zip_ref.extractall(str(path.parent))


def download_file(motor, url):
    # Gets just the '*.csv' part
    fname = Path(urlparse(url).path).name
    fpath = '{0}/{1}'.format(motor, fname)

    logging.info('Downloading %s to %s', url, fpath)

    if not file_exists(fname):
        r = requests.get(url)
        with open(fpath, 'wb') as dfile:
            dfile.write(r.content)
    return fpath


def download_files():
    for motor in files.keys():
        try:
            logging.info('Creating direcotry %s', str(motor))
            os.makedirs(motor)
        except FileExistsError:
            logging.info('Directory %s already exists', str(motor))
        for url in files[motor]:
            fpath = download_file(motor, url)
            unzip_file(fpath)


def main():
    download_files()


if __name__ == '__main__':
    main()
