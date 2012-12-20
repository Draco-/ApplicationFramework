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
import sys,  imp
from PyQt4 import QtCore
from PyQt4 import QtGui

from ApplicationConfig import AppConfig
import ApplicationConfig

from services.ApplicationStatus import ApplicationStatus

#=====================================================================================================
# Class Application
#=====================================================================================================
class Application(QtGui.QMainWindow):
    """
    This class is used as the MainWindow of the application. It sets up the MainWindow and defines other important basics,
    that are needed in the application. See __init__ method for the implementation details
    """
    #=================================================================================================
    # signals for class Application
    #=================================================================================================
    # Signals to controll dynamically loaded modules
    sigInitializeModule = QtCore.pyqtSignal(object)                       # ask a dynamically loaded module to do its own initialisation
    sigCloseModule = QtCore.pyqtSignal()                                      # singal the module to prepare for shut down of application
    
    # Signals that build a generic acess model to the application
    sigStatusBar = QtCore.pyqtSignal(object)                                # send a reference to the application's status bar
    
    # Action signals of the application
    sigStatusMessage = QtCore.pyqtSignal(object)                       # send a text information about the application's status

    
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
        # set geometry of the main window
        self.setGeometry(AppConfig.app_geometry_xpos, 
                                     AppConfig.app_geometry_ypos,
                                     AppConfig.app_geometry_width,
                                     AppConfig.app_geometry_height   )  
 
        # initialize all application services required for the application
        self._initApplicationServices()
        self._initActions()
        
        self._initToolBar()
        
        
    def _initApplicationServices(self):
        """
        Initialize all application services, that are required by the application.
        
        For each service, that is provided by the application framework, there is one service object, that offers the
        appropriate methods. These methods also can be used as slots for signals from other objects of the application.
        All service objects are collected in a dictionary with the name of the service as the key for the dictionary
        
        The available and required services are retrieved from the serviceList, wich is part of the
        ApplicationConfig class
        """
        # Dictionary of available services
        self.services = {}
        
        # Load all requires service modules and thell them to start
        for service in AppConfig._serviceList:
            # try to load module dynamically
            try:
                # find the appropriate module, using information from serviceList
                mod1, mod2, mod3 = imp.find_module(service[0], service[1])
                #print mod1, mod2, mod3
                # load the module found above
                dynmod = imp.load_module(service[0], mod1, mod2, mod3)
                mod1.close()        # I'm not shure, if this is necessary
            except:
                print 'Something went wrong'
            finally:
                mod1.close()
            # create, bind and initialize a service object from the dynamically loaded module
            self.services[service[2]] = dynmod.get_object(self)
            self.sigInitializeModule.emit(self)
            
    def _initActions(self):
        """
        Setup and prepare a list of application actions (to be performed from the top level
        of the application.
        An exit action is already implemented as an example
        Other actions. that will performed from other parts of the application will be added by
        using the slot_addAction(action) method
        """
        # Dictionary of actions
        self.actions = {}
        
        # exitApp - exit the application (end of application programme)
        self.actions['exitApp'] = QtGui.QAction(QtGui.QIcon('icons/exitApp.png'), 
                                                'Exit', 
                                                 self)
        self.actions['exitApp'].setShortcut('Ctrl+Q')
        self.actions['exitApp'].triggered.connect(self.slotExitApp)
        
        # Add another action 'testAction', that is jused to test other parts of application
        self.actions['testAction'] = QtGui.QAction(QtGui.QIcon('icons/default.png'), 
                                                         'Test Action', 
                                                         self)
        self.actions['testAction'].setShortcut('Ctrl+T')
        self.actions['testAction'].triggered.connect(self.slotTestAction)
        #TODO: remove 'testAction', when it is no longer needed
    
    
    def _initToolBar(self):
        self.fileToolBar = self.addToolBar('File')
        self.fileToolBar.addAction(self.actions['exitApp'])
        # Make the 'testAction' available for triggering by user
        self.fileToolBar.addAction(self.actions['testAction'])
        #TODO: remove 'testAction', when it is no longer needed

    #=================================================================================================
    # slot implementations for the application
    #=================================================================================================
    def slotExitApp(self):
        """
        Exit the application
        """
        QtGui.qApp.quit()
        
    def slotGetStatusBar(self):
        """
        Slot is part of the dynamic module management system.
        Provides a reference to the application's status bar
        """
        print 'Got request for status bar'
        self.sigStatusBar.emit(self.statusBar())
        
        
    def slotTestAction(self):
        #TODO: remove 'testAction', when it is no longer needed
        print 'Test Action is triggered'
        for a in self.actions:
            print a
        self.sigStatusMessage.connect(self.services['StatusBar'].slotShowMessage)
        self.sigStatusMessage.emit('Testmessage an die Statuszeile')
        

    #=================================================================================================
    # END OF CLASS Application
    #=================================================================================================

#=====================================================================================================
# main function stuff
#=====================================================================================================
def main(args):
    """
    The main function of the module.
    This function starts up the application
    """
    # Like given in the Qt documentation we generate
    # a QApplication object, give it a view and let it go
    app = QtGui.QApplication(args)
    appView = Application()
    appView.show()
    
    sys.exit(app.exec_())
 
# Python idiom to start the application, when this 
# module is loaded by itself
if __name__ == '__main__':
    main(sys.argv)
