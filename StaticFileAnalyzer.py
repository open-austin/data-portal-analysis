#! /usr/env/python
"""Extracts information from a file containing datasets as JSON objects, 
then creates a CSV file containing the results.

Script usage
------------
user@host: python StaticFileAnalyzer.py <input_file> <destination_file>

"""
import sys
import utilities
import logging

logging.basicConfig(filename="static_analyzer.log", filemode="w", level=logging.DEBUG)


if __name__ == "__main__":
    docstring = """USAGE: python StaticFileAnalyzer.py <input_file> <output_file>
    """
    if len(sys.argv) < 3:
        sys.exit(docstring)
    datafile = sys.argv[1]
    outfile = sys.argv[2]

    Reader = utilities.JsonFileReader(datafile)
    datasets = Reader.get_all_datasets()
    Analyzer = utilities.DatasetAnalyzer()

    for item in datasets:
        Analyzer.add_dataset(item)
    Analyzer.make_csv(outfile)
