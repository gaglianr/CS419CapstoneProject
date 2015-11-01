#########################################################
# Initial take on program flow. will be tested and
# modified once screens are made.
#
# We can discuss during our meeting on Sunday.
#
# Jeff -- Reoriented to standard class style
#
#########################################################

import curses
import atexit

class CDBCore:
    def __init__(self):
        # Contains the main curses window
        self.stdscr = ""
      
        # TODO: set to base connection string object
        self.ConnectionString = ""
        
        # TODO: Set to home screen
        self.CurrentScreen = ""
        
        # TODO: Create menu screen
        self.MenuScreen = ""
        
        # TODO: Create status screen
        self.StatusScreen = ""
        
        # Stores the history of screens the user has visited
        self.History = []
    
    # Processes any actions from the user.  These actions are
    # passed through curses.ungetch(ch).
    def ProcessAction(self):
        key = CDBCore.stdscr.getch()
        # TAB denotes move to next widget
        if key in [ord('\t'), 9]:
            self.CurrentScreen.NextWidget()
        # ENTER denotes move to next screen
        # TODO: Decide if this needs to be expanded for screens with
        #       multiple exit points, or if this will be handled within
        #       the screen itself
        elif key in [curses.KEY_ENTER, ord('\n'), 10]:
            self.History.append(self.CurrentScreen)
            self.CurrentScreen.Hide()
            self.CurrentScreen = self.CurrentScreen.Next()
            self.CurrentScreen.Show()
        # CTRL + TAB denotes go back to previous screen if there is one
        elif key in [1]: # TODO: identify CTRL+TAB key possibilities
            if len(self.History) > 0:
                self.CurrentScreen.Hide()
                self.CurrentScreen = self.History.pop()
                self.CurrentScreen.Show()
        else:
            # TODO: Popup to notify user before exitting application that an issue occured
            pass
    
    # Main method is the entry point of the application
    def Main(self):      
        # Prepare curses for use
        #InitCurses()
        
        # Show the home screen
        self.CurrentScreen.Show()
        
        # Process any further actions from the user
        while True:
            self.ProcessAction()
    
    # Cleans up curses on exit
    def CleanupCurses(self):
        try:
            curses.curs_set(0)
            curses.nocbreak()
            self.stdscr.keypad(0)
            curses.echo()
            curses.endwin()
        except:
            # TODO: add universal logging (especially for dev)
            pass # exit anyways
    
    # Initializes the curses library for use, and registers cleanup
    def InitCurses(self):
        # First register proper cleanup of curses
        atexit.register(self.CleanupCurses)
        
        # Next initialize curses for use
        self.stdscr = curses.initscr()
        try:
            # Not all terminals support hiding the cursor
            curses.curs_set(1)
        except:
            pass
        curses.cbreak()
        curses.noecho()
        self.stdscr.keypad(1)

