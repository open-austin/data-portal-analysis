import sys
import os.path
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__) + '/tests')
from nose.tools import *
from utilities import *


test_sets = FileUtils.JsonFileReader('test_view_resource.json')
test_dict = test_sets.get_all_datasets()[0]

def test_json_file_reader():
    assert_equals(test_dict['id'], u'abcd-1234')


def test_add_dataset():
    analyzer = PortalUtils.DatasetAnalyzer()
    analyzer.add_dataset(test_sets)
    assert_equals(analyzer._datasets[0] == u'abcd-123')
    
    
