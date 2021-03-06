###############################################################################
# ConnectionWizard
#
# Collets user connection information and connects to db
#
###############################################################################

import sys
import curses
import CDBCore
from Label import Label
from TextBox import TextBox
from Button import Button
from BaseScreen import BaseScreen
from CheckBox import CheckBox
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection
from PostgresConnection import PostgresConnection
import StatusScreen
import SelectTaskScreen

class ConnectionWizard(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self, screen_type="ConnectionWizard")
    
    def Init(self):
        # Tracking variables for retrieving entries
        self.Items = ["User Name", "Password", "Host", "Port", "Database (Optional)", "MySQL", "PostgreSQL"]        
        self.Input = {}
        for i in range(len(self.Items)):
            self.Input[self.Items[i]] = i
        
        # Spacing
        yoffset = 0
        ystart = 3
        xlabel = 3
        xaction = 25
        
        # Passive widgets
        for i in range(len(self.Items)):
            y = (ystart * (i + 1)) + CDBCore.CDBCore.MAIN_SCREEN_Y
            if y >= 21:
                y = (ystart * (i + 1 - 5)) + CDBCore.CDBCore.MAIN_SCREEN_Y
                self.PassiveWidgets.append(Label(self.Items[i], y, xlabel + 40))
            else:
                self.PassiveWidgets.append(Label(self.Items[i], y, xlabel))
        
        # Active widgets
        self.ActionWidgets.append(TextBox(1, 16, 3 + CDBCore.CDBCore.MAIN_SCREEN_Y, xaction))
        self.ActionWidgets.append(TextBox(1, 16, 6 + CDBCore.CDBCore.MAIN_SCREEN_Y, xaction))
        self.ActionWidgets.append(TextBox(1, 16, 9 + CDBCore.CDBCore.MAIN_SCREEN_Y, xaction))
        self.ActionWidgets.append(TextBox(1, 16, 12 + CDBCore.CDBCore.MAIN_SCREEN_Y, xaction))
        self.ActionWidgets.append(TextBox(1, 16, 15 + CDBCore.CDBCore.MAIN_SCREEN_Y, xaction))
        self.ActionWidgets.append(CheckBox('X', ' ', 3 + CDBCore.CDBCore.MAIN_SCREEN_Y, xaction + 40))
        self.ActionWidgets.append(CheckBox('X', ' ', 6 + CDBCore.CDBCore.MAIN_SCREEN_Y, xaction + 40))
        self.ActionWidgets.append(Button("Connect", self.TestConnection, CDBCore.CDBCore.STATUS_SCREEN_Y - 3, 63))
    
    def ResetScreen(self, message):
        CDBCore.CDBCore.StatusScreen.AddStatusMessage(message)
        self.MakeActive()
    
    # Test the user entered information to ensure a connection
    # can be established
    def TestConnection(self):
        # Check that either MySQL or Postgre has been checked        
        if self.ActionWidgets[self.Input["MySQL"]].Value() and self.ActionWidgets[self.Input["PostgreSQL"]].Value():
            self.ResetScreen("Check either MySQL or PostgresSQL, not both.")
            return
            
        if not self.ActionWidgets[self.Input["MySQL"]].Value() and not self.ActionWidgets[self.Input["PostgreSQL"]].Value():
            self.ResetScreen("Must select MySQL or PostgresSQL.")
            return
                
        isMySQL = False
        if self.ActionWidgets[self.Input["MySQL"]].Value():
            isMySQL = True
                
        # Retrieve the database if one has been provided
        database = None
        if len(self.ActionWidgets[self.Input["Database (Optional)"]].Text) > 0:
            database = self.ActionWidgets[self.Input["Database (Optional)"]].Text
        
        # If Postgres, make sure a database has been provided
        if not isMySQL and database == None:
            self.ResetScreen("Database required for PostgreSQL connection.")
            return
        
        # Get the port
        port = 0
        try:
            port = int(self.ActionWidgets[self.Input["Port"]].Text)
        except ValueError:
            pass
        
        # Create the connection
        con = None
        
        if isMySQL:
            con = MySQLConnection(self.ActionWidgets[self.Input["User Name"]].Text,
                                  self.ActionWidgets[self.Input["Password"]].Text,
                                  self.ActionWidgets[self.Input["Host"]].Text,
                                  port,
                                  database)
        else:
            con = PostgresConnection(self.ActionWidgets[self.Input["User Name"]].Text,
                                     self.ActionWidgets[self.Input["Password"]].Text,
                                     database,
                                     self.ActionWidgets[self.Input["Host"]].Text,
                                     port)
        
        # Attempt to connect with the given information
        CDBCore.CDBCore.StatusScreen.AddStatusMessage("Attempting to Connect to Database...")
        results = con.Connect()
        if results.Success:
            CDBCore.CDBCore.Connection = con
            CDBCore.CDBCore.StatusScreen.AddStatusMessage("Connection established.")
            curses.ungetch('\n') # Notify the core to move to next screen
            return
        else:
            CDBCore.CDBCore.StatusScreen.AddStatusMessage(results.Message)
            msg = "Could not connect to database."
            self.ResetScreen(msg)
            return
    
    # Go back to the selection screen
    def Next(self):
        return SelectTaskScreen.SelectTaskScreen()
        
if __name__ == "__main__":
    CDBCore.CDBCore.InitCurses(True)
    CDBCore.CDBCore.InitColor()
    CDBCore.CDBCore.InitScreens()
    CDBCore.CDBCore.CurrentScreen.Hide()
    CDBCore.CDBCore.CurrentScreen = ConnectionWizard()
    CDBCore.CDBCore.Main()