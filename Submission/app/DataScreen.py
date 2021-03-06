###############################################################################
# DataScreen
#
# Collection of widgets that emulates a data table
#
###############################################################################

import curses
import curses.panel
from Label import BaseLabel
from Button import BaseButton
from TextBox import ModTextBox
from BaseScreen import BaseScreen

""" DataScreen """
class DataScreen(BaseScreen):

    default_attributes = {
        "start_y" : 9,
        "start_x" : 15,
        "column_size" : 10, # Not below 3 if bordered
        "display_cols" : 5,
        "display_rows" : 4,
        "header_border" : False,
        "field_border" : True
    }

    def __init__(self, resultsObj, dataMethod=None, attr=None, majorScreen="QueryTable"):
        if dataMethod:
            self.DataMethod = dataMethod
        else:
            self.DataMethod = None

        if attr:
            merged_attributes = DataScreen.default_attributes.copy()
            merged_attributes.update(attr)
            self.Attr = merged_attributes
        else:
            self.Attr = DataScreen.default_attributes

        self.Result = resultsObj

        self.MajorScreen = majorScreen

        BaseScreen.__init__(self, screen_type="DataScreen")

        if self.MajorScreen == "QueryTable" or self.MajorScreen == "ViewTables":
            self.LoadResult()

        elif self.MajorScreen == "AlterTable":
            self.LoadAlterTable()

    def Init(self):
        self.StartX = self.Attr["start_x"]
        self.StartY = self.Attr["start_y"]
        self.ColSize = self.Attr["column_size"]
        self.HeadBorder = self.Attr["header_border"]
        self.FieldBorder = self.Attr["field_border"]
        self.TotalCols = len(self.Result[0])
        self.TotalRows = len(self.Result[1])
        self.DisplayCols = min(self.TotalCols, self.Attr["display_cols"])
        self.DisplayRows = min(self.TotalRows, self.Attr["display_rows"])

        if self.TotalCols < 5:
            self.ColSize = (50/self.TotalCols)
        else:
            self.ColSize = self.Attr["column_size"]

        self.DataX = 0
        self.DataY = 0
        self.CursorX = 0
        self.CursorY = 0

    def LoadResult(self, reset=False):
        if reset:
            self.TotalCols = len(self.Result[0])
            self.TotalRows = len(self.Result[1])
            self.DisplayCols = min(self.TotalCols, self.Attr["display_cols"])
            self.DisplayRows = min(self.TotalRows, self.Attr["display_rows"])

            if self.TotalCols < 5:
                self.ColSize = (50/self.TotalCols)
            else:
                self.ColSize = self.Attr["column_size"]

            self.DataX = 0
            self.DataY = 0
            self.CursorX = 0
            self.CursorY = 0  
            self.CurrentWidget = 0      

            self.Hide()

        # Empty widget containers
        self.PassiveWidgets = []
        self.ActionWidgets = []

        # Define padding variables based on border attributes
        if self.HeadBorder:
            self.HeadPadding = 2
        else:
            self.HeadPadding = 1

        if self.FieldBorder:
            self.FieldPadding = 2
        else:
            self.FieldPadding = 1

        # Iterate through self.Result to create header labels
        for xidx, x in enumerate(range(self.DataX, min(self.TotalCols, self.DataX + self.DisplayCols))):

            # Define header attributes
            headerX = self.StartX + (self.ColSize) * xidx
            headerY = self.StartY
            headerHeight = self.HeadPadding + 1
            headerWidth = self.ColSize

            # Ensure that text is string
            headerText = str(self.Result[0][x])

            if self.HeadBorder:
                attr = {
                    "nocorner_border" : True,
                    "y_offset" : 1,
                    "x_offset" : 1,
                    "text_x_center" : True
                }
            else:
                attr = {
                    "text_x_center" : True
                }

            # Create label based on defined attributes
            headerLabel = BaseLabel(headerText, headerHeight, headerWidth, headerY, headerX, attr)

            # Add header label to passive widgets
            self.PassiveWidgets.append(headerLabel)

        # Iterate through self.Result to create field buttons
        for xidx, x in enumerate(range(self.DataX, min(self.TotalCols, self.DataX + self.DisplayCols))):
            for yidx, y in enumerate(range(self.DataY, min(self.TotalRows, self.DataY + self.DisplayRows))):

                # Define field attributes
                fieldX = self.StartX + (self.ColSize) * xidx
                fieldY = self.StartY + (self.HeadPadding) + (self.FieldPadding) * yidx
                fieldHeight = self.FieldPadding + 1
                fieldWidth = self.ColSize
                fieldText = str(self.Result[1][y][x])
                fieldMethod = self.DataMethod

                if self.FieldBorder:
                    attr = {
                        "nocorner_border" : True,
                        "y_offset" : 1,
                        "x_offset" : 1,
                    }
                else:
                    attr = {

                    }

                # Create button based on defined attributes
                fieldButton = BaseButton(fieldText, fieldMethod, fieldHeight, fieldWidth, fieldY, fieldX, attr)

                # Add field button to action widgets
                self.ActionWidgets.append(fieldButton)

    def LoadAlterTable(self, reset=False):
        if reset:
            self.TotalCols = len(self.Result[0])
            self.TotalRows = len(self.Result[1])
            self.DisplayCols = min(self.TotalCols, self.Attr["display_cols"])
            self.DisplayRows = min(self.TotalRows, self.Attr["display_rows"])
            self.DataX = 0
            self.DataY = 0
            self.CursorX = 0
            self.CursorY = 0  
            self.CurrentWidget = 0

            # Hide pre-existing widgets
            self.Hide()      

        # Empty widget containers
        self.PassiveWidgets = []
        self.ActionWidgets = []

        # Define padding variables based on border attributes
        if self.HeadBorder:
            self.HeadPadding = 2
        else:
            self.HeadPadding = 1

        if self.FieldBorder:
            self.FieldPadding = 2
        else:
            self.FieldPadding = 1

        # Iterate through self.Result to create header labels
        for xidx, x in enumerate(range(self.DataX, min(self.TotalCols, self.DataX + self.DisplayCols))):

            # Define header attributes
            headerX = self.StartX + (self.ColSize) * xidx
            headerY = self.StartY
            headerHeight = self.HeadPadding + 1
            headerWidth = self.ColSize

            # Ensure that text is string
            headerText = str(self.Result[0][x])

            if self.HeadBorder:
                attr = {
                    "nocorner_border" : True,
                    "y_offset" : 1,
                    "x_offset" : 1,
                    "text_x_center" : True
                }
            else:
                attr = {
                    "text_x_center" : True
                }

            # Create label based on defined attributes
            headerLabel = BaseLabel(headerText, headerHeight, headerWidth, headerY, headerX, attr)

            # Add header label to passive widgets
            self.PassiveWidgets.append(headerLabel)

        self.AlterWidgets = []
        # Iterate through self.Result to create field text boxes
        for xidx, x in enumerate(range(self.DataX, min(self.TotalCols, self.DataX + self.DisplayCols))):

            for yidx, y in enumerate(range(self.DataY, min(self.TotalRows, self.DataY + self.DisplayRows))):

                self.AlterWidgets.append([])

                # Define field attributes
                fieldX = self.StartX + (self.ColSize) * xidx
                fieldY = self.StartY + (self.HeadPadding) + (self.FieldPadding) * yidx
                fieldHeight = self.FieldPadding + 1
                fieldWidth = self.ColSize
                fieldText = str(self.Result[1][y][x])

                if self.FieldBorder:
                    attr = {
                        "nocorner_border" : True,
                        "y_offset" : 1,
                        "x_offset" : 1,
                    }
                else:
                    attr = {

                    }

                if x == 0:
                    fieldButton = BaseButton(fieldText, None, fieldHeight,
                                             fieldWidth, fieldY, fieldX, attr)
                    fieldButton.UpdateDisplay()
                    self.ActionWidgets.append(fieldButton)

                    self.AlterWidgets[yidx].append(fieldButton)

                if x == 1:
                    # Create textbox based on defined attributes
                    fieldTextBox = ModTextBox(fieldHeight, fieldWidth, fieldY, fieldX, attr)
                    fieldTextBox.Text = fieldText
                    fieldTextBox.UpdateDisplay()

                    # Add field textbox to action widgets
                    self.ActionWidgets.append(fieldTextBox)

                    self.AlterWidgets[yidx].append(fieldTextBox)

                # Load Alter Method
                if x == 2:
                    alterButton = BaseButton(fieldText, self.DataMethod[0], fieldHeight,
                                             fieldWidth, fieldY, fieldX, attr)
                    alterButton.UpdateDisplay()
                    alterButton.Row = yidx
                    self.ActionWidgets.append(alterButton)

                    self.AlterWidgets[yidx].append(alterButton)


                # Load Drop Method
                elif x == 3:
                    dropButton = BaseButton(fieldText, self.DataMethod[1], fieldHeight,
                                            fieldWidth, fieldY, fieldX, attr)
                    dropButton.UpdateDisplay()
                    dropButton.Row = yidx
                    self.ActionWidgets.append(dropButton)

                    self.AlterWidgets[yidx].append(dropButton)

    # Load with WASD/arrow-key movement
    def Active(self):
        if self.MajorScreen == "AlterTable":
            loadFunc = self.LoadAlterTable
        else:
            loadFunc = self.LoadResult

        if not self.ActionWidgets:
            capturing = False

        else:
            self.ActionWidgets[self.CurrentWidget].Highlight()
            capturing = True

        while capturing:
            key = self.ActionWidgets[self.CurrentWidget].Win.getch()

            if key in [curses.KEY_DOWN, ord('s')]:
                if self.CursorY == self.DisplayRows - 1 and (self.DataY + self.DisplayRows - 1) == self.TotalRows - 1:
                    pass
                elif self.CursorY == self.DisplayRows - 1:
                    self.DataY += 1
                    loadFunc()
                    self.SetCurrent()
                else:
                    self.CursorY += 1
                    self.SetCurrent()

            # Up key action
            elif key in [curses.KEY_UP, ord('w')]:
                if self.CursorY == 0 and self.DataY == 0:
                    pass
                elif self.CursorY == 0:
                    self.DataY -= 1
                    loadFunc()
                    self.SetCurrent()
                else:
                    self.CursorY -= 1
                    self.SetCurrent()

            # Right key action
            elif key in [curses.KEY_RIGHT, ord('d')]:
                if self.CursorX == self.DisplayCols - 1 and (self.DataX + self.DisplayCols - 1) == self.TotalCols - 1:
                    pass
                elif self.CursorX == self.DisplayCols - 1:
                    self.DataX += 1
                    loadFunc()
                    self.SetCurrent()
                else:
                    self.CursorX += 1
                    self.SetCurrent()

            # Left key action
            elif key in [curses.KEY_LEFT, ord('a')]:
                if self.CursorX == 0 and self.DataX == 0:
                    pass
                elif self.CursorX == 0:
                    self.DataX -= 1
                    loadFunc()
                    self.SetCurrent()
                else:
                    self.CursorX -= 1
                    self.SetCurrent()

            # tab
            elif key in [ord('\t'), 9]:  
                if self.ActionWidgets[self.CurrentWidget].Type == "TextBox":
                    if self.ActionWidgets[self.CurrentWidget].IsActive:
                        self.ActionWidgets[self.CurrentWidget].IsActive = False

                self.ActionWidgets[self.CurrentWidget].UnHighlight()
                curses.ungetch("\t")
                capturing = False

            # enter - context dependent for textbox/button
            elif key in [curses.KEY_ENTER, ord('\n'), 10]:
                capturing = False

                if self.ActionWidgets:
                    if self.ActionWidgets[self.CurrentWidget].Type == "TextBox":
                        if not self.ActionWidgets[self.CurrentWidget].IsActive:
                            self.ActionWidgets[self.CurrentWidget].IsActive = True
                            self.ActionWidgets[self.CurrentWidget].Active()
                            capturing = True
                        else:
                            self.ActionWidgets[self.CurrentWidget].IsActive = False
                            capturing = True
                    elif self.ActionWidgets[self.CurrentWidget].Type == "Button":
                        if self.ActionWidgets[self.CurrentWidget].CallMethod:
                            self.ActionWidgets[self.CurrentWidget].CallMethod()
                        else:
                            capturing = True

            # menu key
            elif key in [curses.KEY_F1, 77]:
                capturing = False
                curses.ungetch(77)

            # status screen key
            elif key in [curses.KEY_F8, 76]:
                capturing = False
                curses.ungetch(76)

    # Helper function determines Current Widget/Field
    def SetCurrent(self):
        if self.ActionWidgets:
            self.ActionWidgets[self.CurrentWidget].UnHighlight()
            self.CurrentWidget = self.CursorY + self.CursorX * self.DisplayRows
            self.ActionWidgets[self.CurrentWidget].Highlight()

    # UpdateDisplay updates all widgets
    def UpdateDisplay(self):
        for w in self.PassiveWidgets:
            w.UpdateDisplay()
        for w in self.ActionWidgets:
            w.UpdateDisplay()

    # On the other hand, highlight highlights only the current widget
    def Highlight(self):
        if self.ActionWidgets:
            self.ActionWidgets[self.CurrentWidget].Highlight()
