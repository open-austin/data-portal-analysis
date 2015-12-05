import sys
import os.path
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__) + '/tests')
from nose.tools import *
from utilities import *

def printpath():
    print sys.path
    return


def test_json_file_reader():
    test_sets = FileUtils.JsonFileReader('test_view_resource.json')
    test_dict = test_sets.get_all_datasets()[0]
    assert_equals(test_dict['id'], u'abcd-1234')
    assert_equals(test_dict['name'], u'Test Dataset')
    assert_equals(test_dict['tableId'], 7654321)

    
