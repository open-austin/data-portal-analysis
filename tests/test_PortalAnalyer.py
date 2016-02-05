import sys
import os.path
from nose.tools import assert_equals
import utilities
import datetime
import json

def test_portal_analyzer():
    datasets = []
    current_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    with open('tests/test_view_resource.json') as data_json:
        json_str = data_json.read()
        data_dict = json.loads(json_str)
        print data_dict
        datasets = [data_dict]
        for item in datasets:
            item['snapshot_time'] = current_time

    analyzer = utilities.DatasetAnalyzer()
    analyzer._creation_time = 'null' # Avoids timestamp conflict

    for item in datasets:
        analyzer.add_dataset(item)

    analyzer.make_csv('test_results.csv')

    with open('test_results.csv') as results_file:
        results_str = results_file.read()
    with open('tests/expected_out.csv', 'r') as test_file:
        expected_str = test_file.read()

    assert_equals(results_str, expected_str)
