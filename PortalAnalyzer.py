#! /usr/bin/python
"""Main portal analysis script.
"""
import utilities
import json
import logging
import argparse
import datetime

def run_online_analysis(outfile, config):
    """This function runs the online analyzer; it requires internet access.
    """
    id_getter = utilities.SocIdGetter(config.views_url, config.migrations_url)
    soc_ids = id_getter.get_ids()
    view_requester = utilities.ViewRequestHandler(config.request_url)
    analyzer = utilities.ViewAnalyzer()

    for fourby in soc_ids:
        view = view_requester.get_view(fourby)
        print("Processing {0}".format(fourby))
        if view == "null":
            continue
        analyzer.add_view(view)

    analyzer.make_csv(outfile)


def run_static_analysis(datafile, outfile):
    """This function runs the analyzer on a local JSON file.
    """
    views = []
    current_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    with open(datafile) as data_json:
        json_str = data_json.read()
        data_dict = json.loads(json_str)
        print data_dict
        views = [data_dict]
        for item in views:
            item['snapshot_time'] = current_time

    analyzer = utilities.ViewAnalyzer()

    for item in views:
        analyzer.add_view(item)

    analyzer.make_csv(outfile)


if __name__ == "__main__":
    desc = "ATX data portal analysis script."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("output_file", help="Name of CSV file to be created.")
    parser.add_argument("--static",
                        help="Read the views from a static file.")
    parser.add_argument("-c", "--config",
                        help="Specifies a configuration file to read options from.")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="Increase logfile verbosity to DEBUG")
    args = parser.parse_args()

    config = utilities.ConfigHelper(args.config)

    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARN
    logging.basicConfig(filename=config.log_file, filemode="w",
                        level=log_level)

    if args.static:
        run_static_analysis(args.static, args.output_file)
    else:
        run_online_analysis(args.output_file, config)
