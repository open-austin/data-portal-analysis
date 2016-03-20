import sys
import os.path
from nose.tools import assert_equals
import utilities
import datetime
import json

    
def test_portal_analyzer_with_db():
    """test_portal_analyzer_with_db
    An approval test to verify the functionality of the modified ViewAnalyzer's csv generation.
    """
    views = []
    with open('tests/test_view_resource.json') as data_json:
        json_str = data_json.read()
        data_dict = json.loads(json_str)
        views = [data_dict]

    analyzer = utilities.ViewAnalyzer("sqlite:///tests/test.db")

    for item in views:
        analyzer.add_view(item)

    analyzer.make_csv('test_results_db.csv')

    with open('test_results_db.csv') as results_file:
        results_str = results_file.read()
    with open('tests/expected_out.csv', 'r') as test_file:
        expected_str = test_file.read()

    assert_equals(results_str, expected_str)
    os.remove('tests/test.db')

    
