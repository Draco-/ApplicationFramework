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
 
ApplicationStatus.py
#=====================================================================================================
Module to controll the application's status bar.
This module is dynamically loaded by the application and provides methods
and signal slots to show appropriate status information in the status bar of
the application
"""
#=====================================================================================================
# Import section
#=====================================================================================================
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui

#=====================================================================================================
# Dynamic loadable module
#=====================================================================================================
def get_object(application):
    """
    This is required for a module, that can be dynamically loaded by the application class of application framework.
    the function returns a instantiated 'main' object, that builds the core of the module
    """
    # instantiate an object from the application status class
    object = ApplicationStatus()
    # connect the application's module controll signals to the object
    application.sigInitializeModule.connect(object.initialize)
    application.sigCloseModule.connect(object.prepareClose)
    # return the object
    return object


#=====================================================================================================
# Class ApplicationStatus
#=====================================================================================================
class ApplicationStatus(QtCore.QObject):
    """
    Class to take the status line widget from an application and use it to show common information
    about the application's status
    """
    #=================================================================================================
    # signals for class ApplicationStatus
    #=================================================================================================
    # request a reference to the applications status bar
    sigRequestStatusBar = QtCore.pyqtSignal()
   
    #=================================================================================================
    # initializing the ApplicationStatus class
    #=================================================================================================
    def __init__(self):
        """
        The python constructor method, to initialize an object of ApplicationStatus class
        """
        # call __init__ method of superclass
        QtCore.QObject.__init__(self)
        # predfine all other instance variables
        self.statusBar = None
        self.canClose = False
        
    def initialize(self, application):
        """
        Slot method, that receives the signal to initialize itself from the application, that 
        holds an object of this class.
        The 'application' parameter is a reference to the application and can be used to
        connect signals from the application and signals to the application
        """
        #print 'Application Status is going to initialize itself'

        # do the required signal connections for the ApplicationStatus object
        self.sigRequestStatusBar.connect(application.slotGetStatusBar)
        application.sigStatusBar.connect(self.slotSetStatusBar)

        # request the reference to the status bar
        self.sigRequestStatusBar.emit()
        
    def prepareClose(self):
        """
        Slot method required by dynamically loadable module to prepare the closing of the
        application. Method must cleanup module and set variabel 'canClose' to true
        """
        self.canClose = True
        
        
    def slotSetStatusBar(self, statusWidget):
        """
        Slot method, that receives the signal containing a reference to the application's
        status bar and sets the object variable accordingly
        """
        self.statusBar = statusWidget
        self.slotShowReady()
    
    def slotShowReady(self):
        """
        Show the message 'Ready...' in the status bar
        """
        self.statusBar.showMessage('Ready...')
        
    def slotShowMessage(self, message):
        """
        Show the given message text in the status bar
        """
        self.statusBar.showMessage(message)
    

