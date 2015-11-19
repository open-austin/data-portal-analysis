#! /usr/env/python
"""Extract information from Austin's datasets.

Script usage:

    $ python PortalAnalytics.py <input_file> <destination_file>

"""

import sys
import utils.PortalUtils as utils

if __name__ == "__main__":
    docstring = """USAGE: python PortalAnalytics.py <input_file> <output_file>
    """
    if len(sys.argv) < 3:
        sys.exit(docstring)
    datafile = sys.argv[1]
    outfile = sys.argv[2]

    Handler = utils.DatasetHandler(datafile)
    datasets = Handler.get_all()
    Analyzer = utils.DatasetAnalyzer(datasets)
    Analyzer.make_csv(outfile)
