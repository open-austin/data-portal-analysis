import sys
import os
from nose.tools import assert_equals
import utilities
import json
import dataset

def test_add_view():
    with open('tests/test_view_resource.json') as data_json:
        json_str = data_json.read()
        test_view = json.loads(json_str)

    analyzer = utilities.ViewAnalyzer("sqlite:///tests/test.db")
    analyzer.add_view(test_view)

    with dataset.connect('sqlite:///tests/test.db') as db:
        views_table = db['unnormalized']
        for current_record in views_table.all():
            assert_equals(current_record['last_modified'], 0)
            assert_equals(current_record['view_name'], u'Test Dataset')

    os.remove('tests/test.db')


def test_update_view():
    with open('tests/test_view_resource.json') as data_json:
        json_str = data_json.read()
        test_view = json.loads(json_str)

    with open('tests/newer_test_view_resource.json') as data_json:
        json_str = data_json.read()
        newer_test_view = json.loads(json_str)

    analyzer = utilities.ViewAnalyzer("sqlite:///tests/test.db")
    analyzer.add_view(test_view)

    with dataset.connect('sqlite:///tests/test.db') as db:
        views_table = db['unnormalized']
        current_record = views_table.find_one(view_id = u'abcd-1234')
        assert_equals(current_record['last_modified'], 0)

    analyzer.add_view(newer_test_view)

    with dataset.connect('sqlite:///tests/test.db') as db:
        views_table = db['unnormalized']
        current_record = views_table.find_one(view_id = u'abcd-1234')
        assert_equals(current_record['last_modified'], 10)

    os.remove('tests/test.db')
        


    
