import sys
import os.path
sys.path.append(os.path.dirname(__file__))
from nose.tools import *
from utilities import *


test_reader = FileUtils.JsonFileReader('tests/test_view_resource.json')
test_set = test_reader.get_all_datasets()[0]
#test_set = test_sets[0]

def test_json_file_reader():
    assert_equals(test_set['id'], u'abcd-1234')


def test_add_dataset():
    analyzer = PortalUtils.DatasetAnalyzer()
    analyzer.add_dataset(test_set)
    assert_equals(analyzer._datasets[0], u'abcd-1234')

def test_get_dataset_info():
    expected = [u"abcd-1234", u"Test Dataset",
                u"Test Department", u"1970-01-01T0:00:00"]
    analyzer = PortalUtils.DatasetAnalyzer()
    result = analyzer._get_dataset_info(test_set)
    assert_equals(result, expected)

def test_get_column_info():
    expected = [1, u'First Column', u'first_column', 1, 1, u'text', u'text']
    analyzer = PortalUtils.DatasetAnalyzer()
    result = analyzer._get_column_info(test_set['columns'][0])
    assert_equals(result, expected)
