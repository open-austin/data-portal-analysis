#! /usr/bin/python
"""Main portal analysis script.

"""
import sys
import utilities
import logging
import re
import argparse


def run_online_analysis(outfile):
    IdGetter = utilities.SocIdGetter()
    soc_ids = IdGetter.fourby_list
    ViewRequester = utilities.ViewRequestHandler()
    Analyzer = utilities.DatasetAnalyzer()

    for fourby in soc_ids:
        dataset = ViewRequester.get_view(fourby)
        print "Processing %s" % fourby
        if dataset == "null":
            continue
        Analyzer.add_dataset(dataset)

    Analyzer.make_csv(outfile)


def run_static_analysis(datafile, outfile):
    Reader = utilities.JsonFileReader(datafile)
    datasets = Reader.get_all_datasets()
    Analyzer = utilities.DatasetAnalyzer()

    for item in datasets:
        Analyzer.add_dataset(item)

    Analyzer.make_csv(outfile)


if __name__ == "__main__":
    desc = "ATX data portal analysis script."
    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument("output_file", help = "Name of CSV file to be created.")
    parser.add_argument("--static",
                        help = "Read the datasets from a static file.")
    parser.add_argument("-v","--verbose",
                        action="store_true",
                        help = "Increase logfile verbosity to DEBUG")
    args = parser.parse_args()
    
    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARN
    logging.basicConfig(filename="portal_analyzer.log", filemode="w",
                    level=log_level)

    
    if args.static:
        run_static_analysis(args.static, args.output_file)
    else:
        run_online_analysis(args.output_file)
