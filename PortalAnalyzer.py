#! /usr/bin/python
"""Main portal analysis script.

"""
import utilities
import json
import logging
import argparse
import datetime

def run_online_analysis(outfile):
    """This function runs the online analyzer; it requires internet access.
    """
    idGetter = utilities.SocIdGetter()
    soc_ids = idGetter.fourby_list
    viewRequester = utilities.ViewRequestHandler()
    analyzer = utilities.DatasetAnalyzer()

    for fourby in soc_ids:
        dataset = viewRequester.get_view(fourby)
        print("Processing %s" % fourby)
        if dataset == "null":
            continue
        analyzer.add_dataset(dataset)

    analyzer.make_csv(outfile)


def run_static_analysis(datafile, outfile):
    """This function runs the analyzer on a local JSON file.
    """
    datasets = []
    current_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    with open(datafile) as data_json:
        json_str = data_json.read()
        data_dict = json.loads(json_str)
        print data_dict
        datasets = [data_dict]
        for item in datasets:
            item['snapshot_time'] = current_time

    analyzer = utilities.DatasetAnalyzer()

    for item in datasets:
        analyzer.add_dataset(item)

    analyzer.make_csv(outfile)


if __name__ == "__main__":
    desc = "ATX data portal analysis script."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("output_file", help="Name of CSV file to be created.")
    parser.add_argument("--static",
                        help="Read the datasets from a static file.")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Increase logfile verbosity to DEBUG")
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
