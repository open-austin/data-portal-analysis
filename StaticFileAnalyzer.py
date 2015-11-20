#! /usr/env/python
"""Extract information from a file containing datasets as JSON objects.

Script usage:

    $ python StaticFileAnalyzer.py <input_file> <destination_file>

"""

import sys
import utils.PortalUtils as utils

if __name__ == "__main__":
    docstring = """USAGE: python StaticFileAnalyzer.py <input_file> <output_file>
    """
    if len(sys.argv) < 3:
        sys.exit(docstring)
    datafile = sys.argv[1]
    outfile = sys.argv[2]

    Handler = utils.JsonFileHandler(datafile)
    datasets = Handler.get_all()
    Analyzer = utils.DatasetAnalyzer()
    for item in datasets:
        Analyzer.add_dataset(item)
    Analyzer.make_csv(outfile)
