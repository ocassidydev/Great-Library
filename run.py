#GOOGLE DRIVE/SHEETS API
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

import time

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
f = Figlet()
HEADER = f.renderText("    Great Library")

# search = input("What book are you looking for?\n")

# resp = urlopen(f"{api}{search}")
# book_data = json.load(resp)

# print(book_data['items'][0]['volumeInfo'])

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
    stdscr.addstr(HEADER)
    stdscr.addstr(7, 0, "\tWelcome to the great library, a console-based catalog of all\n\tthe books you have read and want to read!\n\n\tEnter your name: ")

    win = curses.newwin(1, 20, 10, 25)
    box = Textbox(win)
    stdscr.refresh()
    box.edit()

    name = box.gather().strip().lower()
    stdscr.addstr(11, 0, f"\tWelcome {name.title()}!")
    name = name.replace(" ", "")

    if check_for_user(name):
        stdscr.addstr(12, 0, f"\tYou have an active account with {len(SHEET.worksheet(name).get_all_values())-1} entries. Access your library? (y/n)")
    else:
        stdscr.addstr(12, 0, "\tYou have not yet created an account. Create a new account? (y/n)")

    while True:
        key = stdscr.getkey()
        if key == "y":
            # if not check_for_user(name):
            #     create_new_user(name)
            return name
        elif key == "n":
            display_landing(stdscr)

def main(stdscr):
    #CONFIGURE COLORS
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
    BLUE_AND_WHITE = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    RED_AND_WHITE = curses.color_pair(3)
    stdscr.attron(GREEN_AND_BLACK)
    name = display_landing(stdscr)
    print(name)
    stdscr.getch()

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