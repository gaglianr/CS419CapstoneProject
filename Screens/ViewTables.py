import sys
import curses
from CDBCore import CDBCore
from Label import BaseLabel
from Button import BaseButton
from BaseScreen import BaseScreen
from ResultStatus import ResultStatus
from MySQLConnection import MySQLConnection
from DataTable import DataTable

_PAGESIZE_ = 5

class ViewTables(BaseScreen):
    def __init__(self, DBName=""):
        if DBName:
            CDBCore.Connection.Database = DBName

        elif not CDBCore.Connection.Database:
            raise Exception("No database selected.")

        BaseScreen.__init__(self)
            
    def Init(self):
        self.CurrentPage = 0
        self.NumTables = 0

        self.GetTables()
        self.PassiveWidgets.append(BaseLabel("View Tables", 2, len("View Tables") + 2, 5, 20, attr=
            {
             'bottom_border' : True, 
             'x_offset' : 1 
            }
        ))


    # Retrieves a list of tables
    def GetTables(self):
        try:
            # Retrieve a list of tables
            result = CDBCore.Connection.QueryString("SHOW TABLES FROM " + CDBCore.Connection.Database)
            
            # Ensure there weren't any issues getting the list of tables.
            if not result.Success:
                sys.exit(result.Message) # FOR TESTING

            else:
                self.Data = result.Data[1]

            # Set NumTables
            self.NumTables = len(self.Data)
            
            # Create a column of Buttons for each table
            self.AddTables()

        except Exception as ex:
            # TODO: Add status update here
            sys.exit(str(ex)) # FOR TESTING

    def AddTables(self):
            self.ActionWidgets = []

            start = self.CurrentPage * _PAGESIZE_
            end = min((self.CurrentPage + 1) * _PAGESIZE_, self.NumTables )

            for offset, name in enumerate(self.Data[start:end]):
                self.ActionWidgets.append(BaseButton(name[0], self.SetTable, 3, 40, 8 + offset * 2, 20,
                    attr={
                        "vert_border" : True,
                        "text_x_center" : True,
                        "y_offset" : 1
                    }
                ))

            # Back button goes back 1 page
            backButton = BaseButton("Back", self.BackFunc(), 3, 6, 16, 10,
                attr={
                    "boxed" : True,
                    "text_x_center" : True,
                    "y_offset" : 1
                }
            )

            # Next button goes forward 1 page
            nextButton = BaseButton("Next", self.NextFunc(), 3, 6, 16, 64,
                attr={
                    "boxed" : True,
                    "text_x_center" : True,
                    "y_offset" : 1
                }
            )

            self.ActionWidgets.append(backButton)
            self.ActionWidgets.append(nextButton)

    def BackFunc(self):
        def EmptyMethod():
            pass

        def BackMethod():
            self.CurrentPage -= 1
            self.AddTables()

        if self.CurrentPage == 0:
            return EmptyMethod

        else:
            return BackMethod


    def NextFunc(self):
        def EmptyMethod():
            pass

        def NextMethod():
            self.CurrentPage += 1
            self.AddTables()

        if (self.CurrentPage + 1) * _PAGESIZE_ >= self.NumTables:
            return EmptyMethod

        else:
            return NextMethod

    # Sets Connection.Table to current table/advances to QueryTable
    def SetTable(self):
        pass

    # TODO: Return the next screen
    def Next(self):
        return None
