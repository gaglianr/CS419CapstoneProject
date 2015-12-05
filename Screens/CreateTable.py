###############################################################################
# Author:		Rich Gagliano
# Date Created:		11/21/2015
# Date Modified:	11/23/2015
# File Name:		CreateTable.py
#
# Overview:
#
#
###############################################################################

import sys
import curses
from CDBCore import CDBCore
from Label import Label
from TextBox import TextBox
from Button import Button
from BaseScreen import BaseScreen
from CheckBox import CheckBox
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection
from PostgresConnection import PostgresConnection
from CreateTableColumns import CreateTableColumns

class CreateTable(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)
        self.Name = ""
        self.Columns = 0
    
    def Init(self):
        self.PassiveWidgets.append(Label("Table Name:", CDBCore.MAIN_SCREEN_Y + 3, 3))
        self.PassiveWidgets.append(Label("Number of Columns:", CDBCore.MAIN_SCREEN_Y + 6, 3))
        self.ActionWidgets.append(TextBox(1, 16, CDBCore.MAIN_SCREEN_Y + 3, 25))
        self.ActionWidgets.append(TextBox(1, 16, CDBCore.MAIN_SCREEN_Y + 6, 25))
        self.ActionWidgets.append(Button("Next", self.CheckValues, CDBCore.STATUS_SCREEN_Y - 3, 63))
    
    # Checks if a table already exists under the requested name
    def CheckName(self):
        try:
            # Retrieve listing of tables
            result = CDBCore.Connection.GetTables()
            
            # Ensure that the query was successful
            if not result.Success:
                raise Exception(result.Message)
            
            # Check for the table name
            for existing_name in result.Data[1]:
                if existing_name[0].lower() == self.Name.lower():
                    msg = "Table name " + str(self.Name) + " already exists."
                    CDBCore.StatusScreen.AddStatusMessage(msg)
                    return False
            
            # This is a new table name
            return True
        except Exception as ex:
            # TODO: Replace with error once multi line is supported
            msg = "Could not retrieve list of tables."
            CDBCore.StatusScreen.AddStatusMessage(msg)
            return False
    
    def CheckValues(self):
        try:
            self.Name = self.ActionWidgets[0].Text
            self.Columns = int(self.ActionWidgets[1].Text)
            
            # For now impose limit on columns until pagination
            if self.Columns > 10 or self.Columns < 1:
                # TODO: Remove and include pagination
                msg = "Arbitrary limitation of 1-10 columns not met!"
                CDBCore.StatusScreen.AddStatusMessage(msg)
                self.Columns = 0
                self.Name = ""
                self.ActionWidgets[0].selected = True
                self.ActionWidgets[0].Highlight()
                self.ActionWidgets[0].Active()
                return
            
            # Check to see if the table name already exists
            if not self.CheckName():
                self.Columns = 0
                self.Name = ""
                self.ActionWidgets[0].selected = True
                self.ActionWidgets[0].Highlight()
                self.ActionWidgets[0].Active()
                return
            
            # Move on to CreateTableColumn
            curses.ungetch('\n')
            
        except Exception as ex:
            # TODO: Replace with error once multi line is supported
            msg = "Failed to validate db name, or column size:"
            CDBCore.StatusScreen.AddStatusMessage(msg)
            self.Columns = 0
            self.Name = ""
            self.ActionWidgets[0].selected = True
            self.ActionWidgets[0].Highlight()
            self.ActionWidgets[0].Active()
            return
    
    # Move on to CreateTableColumn
    def Next(self):
        return CreateTableColumns(self.Name, self.Columns)

if __name__ == "__main__":
    db = raw_input('Database type (p for Postgres, m for MySQL: ')
    user = raw_input('Enter the db user: ')
    password = raw_input('Enter the db user password: ')
    database = raw_input('Enter the db database: ')
    my = None
    if db == "m":
        my = MySQLConnection(user, password, "127.0.0.1", 3306, database)
    else:
        my = PostgresConnection(user, password, database)
    result = my.Connect()
    if result.Success:
        CDBCore.InitCurses(True)
        CDBCore.InitColor()
        CDBCore.InitScreens()
        CDBCore.Connection = my
        CDBCore.CurrentScreen.Hide()
        CDBCore.CurrentScreen = CreateTable()
        CDBCore.Main()
    else:
        print "Could not log in: " + result.Message