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
 
ApplicationFramework.py
#=====================================================================================================
The main script for an application framework.
This file keeps an application class, that defines the basic elements of the application and the
'boilerplate' stuff to start an application.
"""

#=====================================================================================================
# Import section
#=====================================================================================================
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui

#=====================================================================================================
# Class Application
#=====================================================================================================
class Application(QtGui.QMainWindow):
    """
    This class is used as the MainWindow of the application. It sets up the MainWindow and defines other important basics,
    that are needed in the application. See __init__ method for the implementation details
    """
 #=================================================================================================
    # initializing the application class
    #=================================================================================================
    def __init__(self,  *args):
        """
        Initialize the MainWindow and the basic elements.
        This method keeps just the boilerplate stuff and calls methods for the several initialisation steps.
        Application specific stuff is placed within these methods
        """
        
        # call __init__ method of superclass
        QtGui.QMainWindow.__init__(self,  *args)   
    

