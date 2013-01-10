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
    the function returns an instantiated 'main' object, that builds the core of the module
    """
    # instantiate an object from the application status class
    object = ApplicationStatus()
    # connect the application's module controll signals to the object
    object.initialize(application.get_InfoSignals(), application.get_BoundSignals())
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
    # to application
    sigRequestStatusBar = QtCore.pyqtSignal()                 # request a reference to the applications status bar
    
    #from application
    sigStatusMessage = QtCore.pyqtSignal(object)              # Show a text message in the status bar
   
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
        #self.initialize(application)
            
    def initialize(self, infoSignals, boundSignals):
        print 'Initializing ApplicationStatus'
        
        # Get the reference to the applications status bar
        infoSignals['StatusBar'].connect(self.slotSetStatusBar)      # bind status bar signal from application to its own slot
        boundSignals['RequestStatusBar'].emit()                      # request a referenct to the status bar from application
        
        # Connect action signals provided by the module to its slots
        self.sigStatusMessage.connect(self.slotShowMessage)        
        # use the 'SetServiceMessages' signal form application to register the own signals to the
        # application
        boundSignals['SetServiceMessages'].emit('StatusBar', self.get_InfoSignals(), self.get_BoundSignals())
            
    #=================================================================================================
    # get and set methods for the class
    #=================================================================================================
    def get_InfoSignals(self):
        result = {'RequestStatusBar': self.sigRequestStatusBar}
        return result
        
    def get_BoundSignals(self):
        result = {'ShowMessage': self.sigStatusMessage}
        return result
 
 
    def slotPrepareClose(self):
        """
        slot method required by dynamically loadable module to prepare the closing of the
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
    

