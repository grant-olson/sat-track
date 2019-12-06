import curses

class CursesDisplay:
    def __init__(self):
        self.screen = curses.initscr()
        self.window = curses.newwin(25,80)

        self.row_headers = {"STATUS": 1}

        self.writeline(0, "           SAT TRACK")

        self.update_status("STATUS", "LOADING...")
        
    def writeline(self, row, string):
        self.window.addstr(row,0,string)
        self.window.refresh()
    
    def set_header(self, row, header):
        self.row_headers[header] = row

    def update_status(self, status, string):
        row = self.row_headers[status]
        self.writeline(row, "%s: %s" % (status, string))
        
    def __del__(self):
        curses.endwin()

