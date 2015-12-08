import sys
import os.path
from nose.tools import *
import utilities

def test_portal_analyzer():
    Reader = utilities.JsonFileReader('tests/test_view_resource.json')
    datasets = Reader.get_all_datasets()
    Analyzer = utilities.DatasetAnalyzer()
    Analyzer._creation_time = 'null' # Avoids timestamp conflict

    for item in datasets:
        Analyzer.add_dataset(item)

    Analyzer.make_csv('test_results.csv')

    with open('test_results.csv') as results_file:
        results_str = results_file.read()
    with open('tests/expected_out.csv', 'r') as test_file:
        expected_str = test_file.read()

    assert_equals(results_str, expected_str)
