#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   GEOParserRunner.py
@Time    :   2022/11/07 20:52:57
@Author  :   Xin Dong
@Contact :   xindong9511@gmail.com
@License :   (C)Copyright 2020-2022, XinDong
'''

import argparse
# from optparse import OptionParser
# import os
import sys
# import django
# import pickle as p
# import env
from src.scrna_parser_from_gse import _sync_gse, sync_samples_from_gse_factor, getLocalGeo
from src.utilities import print_log, convert_time


def add_new_parser(subparsers):

    new_parser = subparsers.add_parser(
        "new",  help="parse new sample", description="Parse new data from GEO.")
    new_parser.add_argument('-d', dest='date_region', type=str, required=False,
                            help='Parser will get the pubic samples in this given date region, Please use the format: 2016/01/01-2017/01/01. Default is the recent 100000 entries in GEO.')
    new_parser.add_argument('-o', dest='fsave', type=str, required=False, default='New_collection.xls', 
                            help='The table you want to save the new sample information, the default is "New_collection.xls" which will be built in the working directory.')
    new_parser.add_argument('-fi', dest='fill', action="store_true", default=False,
                            help="currently not used!!! This option should be given or not. add this option means parse the new samples from GEO and add in MySQL database at same time, or means just parse new samples save in outside table, default is False.")
    new_parser.add_argument('-el', dest='exclude', metavar="FILE", required=False,
                            help="a one-column file contains Accession number that has been parsed")


def add_known_parser(subparsers):

    known_parser = subparsers.add_parser('known', help='Add samples, known gsm id.',
                                         description='add samples to CistromeDB MySQL database, those samples are with known gsm id and facotr names.')
    known_parser.add_argument('-i', dest='infile', type=str, required=True,
                              help='The file contains at least two column, one is gsm id, one is factor name with offical gene symbol.')
    known_parser.add_argument('-gc', dest='gsm_col', type=int, required=True,
                              help='The column for gsm id in the -i table, start with 0.')
    known_parser.add_argument('-fi', dest='fill', action="store_true", default=False,
                              help="currently not used!!!  This option should be given or not. add this option means parse the new samples from GEO and add in MySQL database at same time, or means just parse new samples save in outside table, default is False.")
    known_parser.add_argument('-o', dest='fsave', type=str, required=False,
                              help='The table you want to save the new sample information, the default is "singleCell_new_collection.xls" which will be built in the working directory.')
    known_parser.add_argument('-p', dest="path_of_xml", type=str, required=False,
                              help='The folder path contain all the xml files, eg: "./geo", the xml storage format should be: "./geo/GSE1000/GSE1000102.xml".')
    known_parser.add_argument('-rf', dest="refresh", action="store_true", default=False,
                              help='currently not used!!!  whether you want to update if gsmid existed already. Optional.')
    known_parser.add_argument('-el', dest='exclude', metavar="FILE", required=False,
                              help="a one-column file contains Accession number that has been parsed")


def add_local_parser(subparsers):
    local_parser = subparsers.add_parser(
        'local', help="Go through the XML files in the given path, and parse the detail sample information.")
    local_parser.add_argument('-p', dest="path_of_xml", type=str, required=True,
                              help='The folder path contain all the xml files, eg: "./geo", the xml storage format should be: "./geo/GSE1000/GSE1000102.xml".')
    local_parser.add_argument('-fi', dest='fill', action="store_true", default=False,
                              help="currently not used!!!  This option should be given or not. add this option means parse the new samples from GEO and add in MySQL database at same time, or means just parse new samples save in outside table, default is False.")
    local_parser.add_argument('-o', dest='fsave', type=str, required=False,
                              help='The table you want to save the new sample information, the default is "singleCell_new_collection.xls" which will be built in the working directory.')


def run_new(args):
    dregion, file_save, fill_or_not, excludes = args.date_region, args.fsave, args.fill, args.exclude
    # check date region
    if not dregion:
        print_log("No date region setting!")
        dregion = False
    else:
        checkTime = convert_time(dregion)
    # check save file
    # if not file_save:
    #     file_save = './singleCell_new_collection.xls'

    for oneTime in checkTime:
        dregion = oneTime
        print_log("New Collection in %s" % dregion)
        if fill_or_not:
            print_log('parse new sample and add in database')
            _sync_gse(file_save, fill_or_not, dregion,
                      exludeFile=excludes, refresh=True)
        elif not fill_or_not:
            print_log("parse new samples and do not add in database")
            _sync_gse(file_save, fill_or_not, dregion,
                      exludeFile=excludes, refresh=True)
        else:
            print_log('unrecognized -fi option')
            sys.exit(1)


def run_known(args):
    print('fresh database or not: ' + str(args.refresh))
    infile, gsm_col, path, fill_or_not, file_save, excludes = args.infile, args.gsm_col, args.path_of_xml, args.fill, args.fsave, args.exclude

    if not file_save:
        file_save = 'singleCell_result_from_known.xls'

    if path:
        sync_samples_from_gse_factor(infile, gsm_col, fsave=file_save,
                                     xmlPath=path, fill_or_not=fill_or_not, refresh=args.refresh)
    else:
        sync_samples_from_gse_factor(
            infile=infile, gsm_col=gsm_col, fsave=file_save, fill_or_not=fill_or_not, refresh=args.refresh)


def run_local(args):
    file_save, fill_or_not, path, typo, excludes = args.fsave, args.fill, args.path_of_xml, True, False
    if not file_save:
        file_save = './singleCell_new_collection.xls'

    getLocalGeo(file_save, fill_or_not, path, typo, refresh=True)


def main():
    argparser = prepare_argparser()
    args = argparser.parse_args()

    subcommand  = args.subcommand

    if subcommand == "new":
        try:
            run_new(args)
        except MemoryError:
            sys.exit( "MemoryError occurred.")
    elif subcommand == "known":
        try:
            run_known(args)
        except MemoryError:
            sys.exit("MemoryError occurred.")
    elif subcommand == "local":
        try:
            run_local(args)
        except MemoryError:
            sys.exit("MemoryError occurred.")
    return

def prepare_argparser():
    description = "%(prog)s"
    epilog = "For command line options of each command, type: %(prog)s COMMAND -h"
    argparser = argparse.ArgumentParser(description = description, epilog = epilog)

    subparsers = argparser.add_subparsers( dest = 'subcommand' )
    # sub_parsers = parser.add_subparsers(help = "sub-command help", dest = "sub_command")
    subparsers.required = True

    add_new_parser(subparsers)
    add_known_parser(subparsers)
    add_local_parser(subparsers)
    return argparser


            


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupted!\n")
        sys.exit(0)