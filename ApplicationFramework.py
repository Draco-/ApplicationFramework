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
    # To module
    sigResetModule = QtCore.pyqtSignal()                                      # signal all modules to do a reset of the modul
    sigCloseModule = QtCore.pyqtSignal()                                      # signal all modules to prepare for shut down of application

    sigInfoSignals = QtCore.pyqtSignal(object)                                # send dictionary (reference) of info signals
    sigBoundSignals = QtCore.pyqtSignal(object)                               # send dictionary (reference) of bound signals
    sigStatusBar = QtCore.pyqtSignal(object)                                  # send a reference to the applications status bar



    # From module
    sigSetServiceMessages = QtCore.pyqtSignal(object, object, object)         # receive a list of available signals from the modules main object
                                                                              # this signal is meant to be emitted by the modules main object
                                                                              # to informa ApplicationFramework about the possibilities of the 
                                                                              # new service.
                                                                              # the firt object is the service name of the module
                                                                              # the second object is a dictionary of signals, the modules main object
                                                                              # uses as information signals. These should be bound to the slots
                                                                              # of interested objects
                                                                              # the third object is a dictionary of signals, the module has bound to its
                                                                              # own slots to perform some action
    sigRequestStatusBar = QtCore.pyqtSignal()                                 # request a reference to the ApplicationFrameworks status bar.
                                                                              # the ApplicationFramework will emit sigStatusBar with the reference
    sigRequestInfoSignals = QtCore.pyqtSignal(object)                         # request the dictionary of info signals for a given service
    sigRequestBoundSignals = QtCore.pyqtSignal(object)                        # request the dictionary of bound signals for a given service
    
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
        
        # Bind signals for the module system
        self.sigSetServiceMessages.connect(self.slotSetServiceMessages)
        self.sigRequestStatusBar.connect(self.slotGetStatusBar)
        self.sigRequestInfoSignals.connect(self.slotGetInfoSignals)
        self.sigRequestBoundSignals.connect(self.slotGetBoundSignals)

        # Register application services to the application itself
        self.services['application_obj'] = self
        self.services['application_infosignals'] = self.get_InfoSignals()
        self.services['application_boundsignals'] = self.get_BoundSignals()
        
        # Load all requires service modules and thell them to start
        for service in AppConfig._serviceList:
            # load module initialize it and get a main object from the module
            moduleobject = self.loadModule(service)
            # register the loaded module (the main object of the module
            self.services[service[2]+'_obj'] = moduleobject
            
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
    # get and set methods for ApplcationFramework
    #=================================================================================================
    def get_InfoSignals(self):
        """
        Return a dictionary of info signals for the dynamically loaded modules
        """
        infoSignals = {'Reset': self.sigResetModule,                      # application requests all modules to reset themselves
                       'Close': self.sigCloseModule,                      # application requests all modules to close themselves
                       'StatusBar': self.sigStatusBar}                    # application sends a reference to its status bar to the modules
        return infoSignals
    
    def get_BoundSignals(self):
        """
        Return a dictionary of bound signals for the dynamically loaded modules
        These signals are bound to the ApplicationFrameworks slot methods and are meant for the
        modules to send signals to the ApplcationFramework
        """
        boundSignals = {'SetServiceMessages':self.sigSetServiceMessages,  # module sends dictionary of action signals for the module
                        'RequestStatusBar':self.sigRequestStatusBar,      # module requests a reference to the status bar of the application
                        'RequestInfoSignals':self.sigRequestInfoSignals,  # module requests the dictionary with info signals for a specific service
                        'RequestBoundSignals':self.sigRequestBoundSignals}# module requests the dictionary with bound signals for a specific service
        return boundSignals
                        
    def set_ServiceMessages(self, service, infosignals, boundsignals):
        """
        Set the list of service messages for a given service
        """
        self.services[service + '_infosignals'] = infosignals
        self.services[service + '_boundsignals'] = boundsignals
        print 'Setting message list for ' + str(service)

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
        
    def slotGetInfoSignals(self, service):
        """
        Slot is part of the dynamic module management system.
        Provides a reference to the dictionary providing the info signals for the service
        """
        result = self.services[service + '_infosignals']
        self.sigInfoSignals.emit(result)

    def slotGetBoundSignals(self, service):
        """
        Slot is part of the dynamic module management system.
        Provides a reference to the dictionary providing the bound signals for the service
        """
        result = self.services[service + '_boundsignals']
        self.sigBoundSignals.emit(result)

    def slotSetServiceMessages(self, service, infosignals, boundsignals):
        """
        Receive sigSetServiceMessages and call method get_ServiceMessages with these parameters
        """
        self.set_ServiceMessages(service, infosignals, boundsignals)
        
        
    def slotTestAction(self):
        #TODO: remove 'testAction', when it is no longer needed
        print 'Test Action is triggered'
        
        # Test module Application Status by sending the ShowMessage signal
        signal = self.services['StatusBar_boundsignals']['ShowMessage']
        signal.emit('Testmessage')
        
    #=================================================================================================
    # hooks and helper methods for ApplicationFramework
    #=================================================================================================
    def loadModule(self, moduleinfo):
        """
        Load a module given by modleinfo (a list containing the name of the module and
        a path to find the module
        The module is loaded and a main object, the main object of the module is instantiated
        and returned
        """
        # try to load module dynamically
        try:
            # find the appropriate module, using information from moduleinfo
            mod1, mod2, mod3 = imp.find_module(moduleinfo[0], moduleinfo[1])
            #print mod1, mod2, mod3
            # load the module found above
            dynmod = imp.load_module(moduleinfo[0], mod1, mod2, mod3)
            # every dynamically lodable module needs a function 'get_object'
            # that returns a main object for the module
            modobj = dynmod.get_object(self)
            mod1.close()        # I'm not shure, if this is necessary
        except:
            print 'Something went wrong'
        finally:
            mod1.close()
        
        return modobj
        
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
