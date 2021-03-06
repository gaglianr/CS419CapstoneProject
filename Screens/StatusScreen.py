###############################################################################
# StatusScreen
#
# Overview:         
#	StatusScreen displays messages from the system to the user in a 
#	scrolling log format.
#
###############################################################################

import curses, sys
import CDBCore
from BaseWidget import BaseWidget
from Label import Label
from BaseScreen import BaseScreen
from PopUp import PopUpOk

class StatusScreen(BaseScreen):

    def __init__(self):
        BaseScreen.__init__(self, screen_type="StatusScreen")
        
    def Init(self):
        # log for status messages, array of strings
        self.Log = []
        
        # screen settings & spacing variables
        self.ScreenStartY = 20
        self.ScreenHeight = 4       # Status Screen will be 4 tiles high including it's border
        self.TotalLabelsInScreen = 2  # number of logs displayed in screen at a time
        
        self.logLabelY = self.ScreenStartY + 1
        self.logLabelX = 30
        genLabelY = self.ScreenStartY + 1
        genLabelX = 1
        
        self.LogDisplayPos = 0      # index of self.Log to be displayed on bottom line of screen
        self.CursorPos = 0          # index of self.Log that the cursor is currently on
        self.CursorActive = False
        
        # blank widget for drawing a border around the entirety of the Status Screen
        self.PassiveWidgets.append(BaseWidget(self.ScreenHeight,
                                              80,
                                              self.ScreenStartY,
                                              0,
                                              attr={'boxed' : True}))
        # self.PassiveWidgets[0].Win.border('|', '|', '-', '-', '+', '+', '+', '+')
        self.PassiveWidgets[0].UpdateDisplay()
        self.PassiveWidgets[0].ToBottom()
        
        # label widget for persistent messages
        self.PassiveWidgets.append(Label("Shift-M: Main Menu", genLabelY, genLabelX))
        self.PassiveWidgets.append(Label("Shift-L: Message Log", genLabelY + 1, genLabelX))
        self.PassiveWidgets[1].ToTop()
        
        # label widgets for logged system messages
        for y in range(0, self.TotalLabelsInScreen):
            self.PassiveWidgets.append(Label(" " * (80 - self.logLabelX - 2),
                                             self.logLabelY + y,
                                             self.logLabelX))
            self.PassiveWidgets[y + 2].ToTop()
        self.Show()
        
    def AddStatusMessage(self, msgString):
        # put new message at beginning of list
        msgString = self.FitMessageToSpace(msgString, 7, 48)
        self.Log.insert(0, msgString)
        self.UpdateLogLabels()
        
    #automatically assigns new lines characters 
    def FitMessageToSpace(self, msg, y, x):
        linesTaken = 0
        msgIdx = 0
        fitMsg = ""
        while (linesTaken != y):
            linesTaken += 1
            # enough chars left in screen to display rest of msg
            if len(msg[msgIdx:]) < x:
                fitMsg += msg[msgIdx:]
                break
                
            # if on last line available, just display what we can
            elif linesTaken == y:
                fitMsg += msg[msgIdx:msgIdx + x]
            # otherwise make newline character at last possible space before we run out of room
            else:
                maxLine = msg[msgIdx:msgIdx + x]
                lastSpaceIdx = maxLine.rfind(" ")
                nextLine = msg[msgIdx:msgIdx + lastSpaceIdx]
                fitMsg += nextLine
                fitMsg += '\n'
                msgIdx += lastSpaceIdx + 1
        return fitMsg
            
                
        
    def UpdateLogLabels(self):
        # updates the labels on screen to show the last X messages
        # PassiveWidgets[0] = screen border
        # PassiveWidgets[1] = Persistent Messaging
        # PassiveWidgets[2..X] = Log Labels, from top to bottom.
        # PassiveWidgets[X] holds most recent message, [X-1] next most recent, etc.
        
        # if self.Log is empty do nothing
        if not self.Log:
            return
        
        lblIdx = self.TotalLabelsInScreen + 2   # index of first PassiveWidgets to display from top to bottom
        for msgIdx in range(min(self.TotalLabelsInScreen, len(self.Log))):
            # x width available for label messages
            charsAvailable = 80 - self.logLabelX - 2
            lblMsg = self.Log[msgIdx + self.LogDisplayPos][:charsAvailable].replace('\n', ' ')
            fillerChars = charsAvailable - len(lblMsg)
            lblMsg += (" " * fillerChars)
            # clear and redraw the label
            self.PassiveWidgets[lblIdx].Win.erase()
            self.PassiveWidgets[lblIdx] = Label(lblMsg, self.logLabelY + lblIdx - 3, self.logLabelX)
            # HIGHLIGHT TEXT if the label is the current cursor position, and messages are being scrolled
            if self.CursorActive and self.CursorPos == msgIdx + self.LogDisplayPos:
                self.PassiveWidgets[lblIdx].Highlight()
            self.PassiveWidgets[lblIdx].ToTop()
            lblIdx -= 1
        self.Show()
        
    def UpdatePersistentMessage(self, msgString, n=1):
        if (n == 1) or (n == 2):
            # updates the persistent message screen
            self.PassiveWidgets[n] = Label(msgString[:28], self.ScreenStartY + n, 1)
            self.PassiveWidgets[n].ToTop()
            self.Show()
        
    # overwrite BaseScreen function
    def MakeActive(self):
        self.CursorActive = True
        self.UpdateLogLabels()
        
        while self.CursorActive:
            currentLabelIndex = 1 + self.TotalLabelsInScreen - (self.CursorPos - self.LogDisplayPos)
            try:
                key = self.PassiveWidgets[currentLabelIndex].Win.getch()
            except:
                CDBCore.CDBCore.StatusScreen.AddStatusMessage("Error displaying messages.  Exiting message log")
                self.CursorPos = 0
                self.CursorActive = False
                self.UpdateLogLabels()
                curses.ungetch(key);
                return
            
            if key in [curses.KEY_DOWN, ord('s')]:
                if self.CursorPos > 0:
                    self.CursorPos -= 1
                    if self.LogDisplayPos > self.CursorPos:
                        self.LogDisplayPos = self.CursorPos
                self.UpdateLogLabels()
            elif key in [curses.KEY_UP, ord('w')]:
                if self.CursorPos < (len(self.Log) - 1):
                    self.CursorPos += 1
                    if self.LogDisplayPos < self.CursorPos - self.TotalLabelsInScreen + 1:
                        self.LogDisplayPos += 1
                self.UpdateLogLabels()
            elif key in [curses.KEY_F8, 76]:     # SHIFT-L or F8 all exit message log
                # exit for screen
                self.CursorPos = 0
                self.CursorActive = False
                self.UpdateLogLabels()
                curses.ungetch(key);
            elif key in [ord('\n'), 10]:    # ENTER
                if len(self.Log) > 0:
                    self.DisplayPopUpMessage(self.Log[self.CursorPos])
                    self.UpdateLogLabels()
                
                
    def DisplayPopUpMessage(self, msg):
        CDBCore.CDBCore.PopUp = PopUpOk(msg)
        CDBCore.CDBCore.PopUp.MakeActive()
        

    # Overwrite Unhighlight to work with log labels
    def UnHighlight(self):
        self.UpdateLogLabels()