#GOOGLE DRIVE/SHEETS API
from time import strftime
import gspread
from google.oauth2.service_account import Credentials
#GOOGLE BOOKS API
from urllib.request import urlopen
import json
#CONSOLE TOOLS
from pyfiglet import Figlet
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

from datetime import datetime

#Plugging in APIs
#DRIVE AND SHEET
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('great_library')

#GOOGLE BOOKS
GBOOKS = "https://www.googleapis.com/books/v1/volumes?q=intitle:"

#FIGLET
F = Figlet()

# search = input("What book are you looking for?\n")

# resp = urlopen(f"{api}{search}")
# book_data = json.load(resp)

# print(book_data['items'][0]['volumeInfo'])

class UserLibrary:
    """
    Stores the user's data as a list of dictionaries for displaying and editing
    Contains various methods for filtering, sorting, and displaying the library
    """
    def __init__(self, name):
        self.name = name
        self.books = SHEET.worksheet(name).get_all_records()

    #def sort(self, cat):

    #def filter(self, cat):

    #def edit(self, book):

    #def update_data(self):

def check_for_user(name):
    """
    Checks the gsheet for the name entered on the landing page
    If there's a match returns true, if no match returns false
    """
    worksheet_list = [worksheet.title for worksheet in SHEET.worksheets()]
    if name in worksheet_list:
        return True
    elif name not in worksheet_list:
        return False

def display_landing(stdscr):
    """
    Displays the landing page on program start
    Takes user's name as input to retrieve catalog or set up new one
    """
    stdscr.clear()
    header = F.renderText("    Great Library")
    stdscr.addstr(header)
    stdscr.addstr(7, 0, "\tWelcome to the great library, a console-based catalog of all\n\tthe books you have read, and want to read!\n\n\tEnter your name: ")

    win = curses.newwin(1, 20, 10, 25)
    box = Textbox(win)
    stdscr.refresh()
    box.edit()

    #Try except is to prevent user from accessing a reserved sheet for templating all other sheets and entering an empty name
    try:
        name = box.gather().strip().lower()
        if name == "__template__":
            raise ValueError(
                "'__template__' is a reserved user account. Enter a different name"
            )
        if name.strip() == "":
            raise ValueError(
                "cannot accept an empty entry"
            )
    except ValueError as e:
        stdscr.addstr(11, 0, f"\tInvalid entry: {e}, please try again (any key to continue)")
        stdscr.getch()
        return display_landing(stdscr)

    stdscr.addstr(12, 0, f"\tWelcome {name.title()}!")
    name = name.replace(" ", "")

    if check_for_user(name):
        stdscr.addstr(13, 0, f"\tYou have an active account with {len(SHEET.worksheet(name).get_all_values())-1} entries. Access your library? (y/n)\n\t")
    else:
        stdscr.addstr(13, 0, "\tYou have not yet created an account. Create a new account? (y/n)")

    stdscr.move(15, 8)

    while True:
        key = stdscr.getkey()
        if key == "y":
            if not check_for_user(name):
                #creates new sheet from template for user data
                SHEET.duplicate_sheet(0,new_sheet_name=name)
                stdscr.getch()
            return name
        elif key == "n":
            return display_landing(stdscr)

def display_home(stdscr, library):
    """
    Displays the user's home page
    From here they can navigate to the other interfaces
    """
    stdscr.clear()
    header = F.renderText("    Library Home")
    stdscr.addstr(header)

    now = datetime.now()
    hour = now.hour
    am_pm = "am" if hour < 12 else "pm"
    hour = 12 if hour == 0 else hour if hour <= 12 else hour - 12
    day = now.day
    day_suffix = "st" if day%10 == 1 else "nd" if day%10 == 2 else "th"
    month = now.strftime("%B")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    stdscr.addstr(7, 0, (f"\tWelcome, {library.name.title()}.\n\tThe time is currently {hour}:{now.minute} {am_pm}, "
                        f"{days[now.weekday()]} the {day}{day_suffix} of {month}, {now.year}.\n\n\tHow would you like "
                        "to access your library today?"))
    
    controls = curses.newwin(9, 32, 12, 8)
    stdscr.refresh()
    controls.addstr("a - add new title\ne - edit catalog\n\ns - search\no - sort catalog by\nb - browse entire catalog\n\nq - save and quit")
    controls.refresh()
    stdscr.move(21, 8)

    while True:
        key = stdscr.getkey()
        if key == "a":
            pass
            #display_add_ui(stdscr, library)
        elif key == "e":
            pass
            #display_edit_ui(stdscr, library)
        elif key == "s":
            pass
            #search_options(stdscr, controls, library)
        elif key == "o":
            pass
            #sort_options(stdscr, controls, library)
        elif key == "b":
            pass
            #display_book_list(stdscr, library.books)
        elif key == "q":
            return

#def display_add_ui(stdscr)

#def display_edit_ui(stdscr, library)

#def search_options(stdscr, controls, library)

#def sort_options(stdscr, controls, library)

#def display_book_list(stdscr, books):

def main(stdscr):
    #CONFIGURE COLORS
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_AND_BLACK = curses.color_pair(1)
    stdscr.attron(GREEN_AND_BLACK)
    
    name = display_landing(stdscr)
    library = UserLibrary(name)
    display_home(stdscr, library)

    #ECHO USER KEYSTROKES
    #curses.echo()

    #CREATE BORDER
    # stdscr.attron(RED_AND_WHITE)
    # stdscr.border()
    # stdscr.attroff(RED_AND_WHITE)

    #DISPLAY RECTANGLE
    # stdscr.attron(GREEN_AND_BLACK)
    # rectangle(stdscr, 1, 1, 5, 20)
    # stdscr.attroff(GREEN_AND_BLACK)
    # stdscr.addstr(5, 30, "Hello world!")

    #MOVE CURSOR
    # stdscr.move(10, 20)
    # stdscr.refresh()

    #USE WITH ECHO TO DISPLAY USER OUTPUT
    # while True:
    #     key = stdscr.getkey()
    #     if key == 'q':
    #         break

    #CREATE TEXTBOX AND GET USER INPUT
    # win = curses.newwin(3, 18, 2, 2)
    # box = Textbox(win)
    # box.edit()
    # text = box.gather().strip().replace("\n","")
    # stdscr.addstr(10, 40, text)

    #PAD
    # pad = curses.newpad(100, 100)
    # stdscr.refresh()

    # for i in range(100):
    #     for j in range(26):
    #         char = chr(65 + j)
    #         pad.addstr(char, GREEN_AND_BLACK)

    #GET TERMINAL DIMENSIONS
    #(curses.LINES -1, curses.COLS -1)

    #SCROLL PADS
    # for i in range(100):
    #     stdscr.clear()
    #     stdscr.refresh()
    #     pad.refresh(i, 0, 0, 0, 20, 20)
    #     time.sleep(0.2)

    #NEW WINDOW
    # counter_win = curses.newwin(1, 20, 10, 10)
    # stdscr.addstr("hello world!")
    # stdscr.refresh()

    #COUNTDOWN
    # for i in range(100):
    #     counter_win.clear()
    #     if i % 2 == 0:
    #         color = GREEN_AND_BLACK
    #     else:
    #         color = BLUE_AND_YELLOW
        
    #     counter_win.addstr(f"Count: {i}", color)
    #     counter_win.refresh()
    #     time.sleep(0.1)
    
    #CURSOR
    # x, y = 0, 0
    # while True:
    #     try:
    #         key = stdscr.getkey()
    #     except:
    #         key = None
        
    #     if key == "KEY_LEFT":
    #         if x != 0:
    #             x -= 1
    #     elif key == "KEY_RIGHT":
    #         if x != curses.COLS -1:
    #             x += 1
    #     elif key == "KEY_UP":
    #         if y != 0:
    #             y -= 1
    #     elif key == "KEY_DOWN":
    #         if y != curses.LINES -1:
    #             y += 1

    #     stdscr.clear()
    #     stdscr.addstr(y, x, "0")
    #     stdscr.refresh()


wrapper(main)