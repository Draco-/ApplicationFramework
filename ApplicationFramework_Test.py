# coding=utf8
"""
 Copyright (C) 2012 Jürgen Baumeister

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
ApplicationFramework_Test.py
#=====================================================================================================
The test suite for the application class defined in ApplicationFramework.py
The definition of the test suite also is used a documentation point to describe, how the whole thing is meant to work.
"""

#=====================================================================================================
# Import section
#=====================================================================================================
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui

import unittest

# importing the module under Test
from ApplicationFramework import *

#=====================================================================================================
# Class Application_Test 
#=====================================================================================================
class Application_Test(unittest.TestCase):
    """
    The test class for calss Application (defined in ApplicationFramework.py
    """
    
    def setUp(self):
        """
        Implement the sourrounding for class application, to do the functional testing.
        As the other, surrounding classes are not yet implemented, we use stub classes for the surrounding
        """
        print 'Setup test environment for class Application'
        
        """
        As class Application will be a subclass of QMainWindow, we also need to instantiate an object of class QApplication.
        This is necessary for the QT library to setup a proper environment to be able to instantiate a window class.
        For this test case the instantiated QApplication object is not used.
        """
        self._application = QtGui.QApplication([])

    def tearDown(self):
        """
        Clean environment before exit
        """
        print 'Tear down test environment for class Application'

    def checkInstantiation(self):
        """
        Check the instantiation of an object of class Application and do some basic testing for the
        attributes of the object
        """
        print 'Test instantiation of class Application'
        
        """
        Instantiate an object of class Application and check, if the instantiation really produces an object
        of the correct type
        """
        test_object = None
        test_object = Application()
        assert test_object != None,  'Instantiation of an Application object did not do anything'
        assert test_object.__class__.__name__ == 'Application',  'Instantiation of an Application object did not produce an object of type Application'
    
#=====================================================================================================
# Test Suite -- The stuff to collect tests in a testsuite
#=====================================================================================================
def suite():
    testSuite=unittest.TestSuite()
    testSuite.addTest(Application_Test("checkInstantiation"))
    return testSuite
    
def main():
    print 'Start Application Test'
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__=="__main__":
    main()
