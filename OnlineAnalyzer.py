#! /usr/env/python
"""Makes HTTP requests for datasets as JSON objects, 
then creates a CSV file containing the results.

Script usage
------------
user@host: python OnlineAnalyzer.py <fourby_list> <destination_file>

"""
import sys
import utilities
import logging
import re

logging.basicConfig(filename="online_analyzer.log", filemode="w", level=logging.DEBUG)


if __name__ == "__main__":
    docstring = """USAGE: python OnlineAnalyzer.py <fourby_list> <destination_file>
    """
    if len(sys.argv) < 3:
        sys.exit(docstring)
    datafile = sys.argv[1]
    outfile = sys.argv[2]

    with open(datafile) as infile:
        fours_file = infile.read()
    soc_ids = re.findall('[0-9a-z]{4}-[0-9a-z]{4}?', fours_file, re.DOTALL)
    for soc in soc_ids:
        print "soc:", soc
    Requester = utilities.ViewRequestHandler()
    Analyzer = utilities.DatasetAnalyzer()

    for fourby in soc_ids:
        dataset = Requester.get_view(fourby)
        print "Processing %s" % fourby
        if dataset == "null":
            continue
        Analyzer.add_dataset(dataset)

    Analyzer.make_csv(outfile)
