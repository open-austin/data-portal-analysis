import sys
import os.path
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__) + '/tests')
from nose.tools import *
from utilities import *

def printpath():
    print sys.path
    return
