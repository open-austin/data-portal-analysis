#! /usr/env/python
"""Makes HTTP requests for datasets as JSON objects, 
then creates a CSV file containing the results.

Script usage
------------
user@host: python OnlineAnalyzer.py <fourby_list> <destination_file>

"""

import sys
import utils
import logging

if __name__ == "__main__":
    docstring = """USAGE: python OnlineAnalyzer.py <fourby_list> <destination_file>
    """
    if len(sys.argv) < 3:
        sys.exit(docstring)
    datafile = sys.argv[1]
    outfile = sys.argv[2]

    with open(datafile) as infile:
        fours = infile.read()
    soc_ids = fours.split('\n')

    Requester = utils.ViewRequestHandler()
    Analyzer = utils.DatasetAnalyzer()

    for fourby in soc_ids:
        dataset = Requester.get_view(fourby)
        print "Processing %s" % fourby
        if dataset == "null":
            continue
        Analyzer.add_dataset(dataset)

    Analyzer.make_csv(outfile)
