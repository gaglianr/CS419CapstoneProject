import sys
import curses
from CDBCore import CDBCore
from Label import Label
from Button import BaseButton
from BaseScreen import BaseScreen
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection
from DataTable import DataTable

class ViewTables(BaseScreen):
    def __init__(self, db_name=""):
        if db_name:
            CDBCore.CurrentDatabase = db_name

        elif not CDBCore.CurrentDatabase:
            raise Exception("No database selected.")

        BaseScreen.__init__(self)
            
    def Init(self):
        self.GetTables()
        self.PassiveWidgets.append(Label("Tables", 5, 5))

    # Retrieves a list of tables
    def GetTables(self):
        try:
            # Retrieve a list of tables
            result = CDBCore.Connection.QueryString("SHOW TABLES FROM " + CDBCore.CurrentDatabase)
            
            # Ensure there weren't any issues getting the list of tables.
            if not result.Success:
                raise Exception(result.Message)
            
            # Create a data table passing result as argument
            offset = 1
            for name in result.Data[1]:
                self.ActionWidgets.append(Button(name[0], self.SetDatabase, 10 + offset, 5))
                offset += 1

        except Exception as ex:
            # TODO: Add status update here
            msg = "Could not retrieve list of tables.\n" + str(ex)

    # # Sets the current table
    # def SetTable(self):
    #     try:
    #         name = self.ActionWidgets[self.CurrentWidget].Text
    #         CDBCore.Connection.Database = name
    #         result = CDBCore.Connection.QueryString("USE " + name)
    #         if result.Success:
    #             curses.ungetch('\n') # Notify the core to move to next screen
    #         else:
    #             raise Exception(result.Message)
    #     except Exception as ex:
    #         # TODO: Status and popup here with failure message
    #         self.ActionWidgets[self.CurrentWidget].selected = True
    #         self.ActionWidgets[self.CurrentWidget].Highlight()
    #         self.ActionWidgets[self.CurrentWidget].Active

    # TODO: Return the next screen
    def Next(self):
        return None