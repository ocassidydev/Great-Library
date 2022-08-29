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

from datetime import datetime
import math

from textwrap import wrap

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

class Book:
    """
    Stores book data for easier recall and use
    """
    def __init__(self, bookdata):
        self.title = bookdata.get('title', 'title not found')
        self.author = bookdata.get('authors', 'author not found')[0]
        self.pages = bookdata.get('pageCount', 'page count not found')
        self.categories = ", ".join(bookdata.get('categories', ['genres not found']))
        description = bookdata.get('description', 'description not found')
        if len(description) >= 4*(curses.COLS - 22)-3:
            description = description[:4*(curses.COLS - 22)-3] + "..."
        self.description = description
        

class UserLibrary:
    """
    Stores the user's data as a list of dictionaries for displaying and editing
    Contains various methods for filtering, sorting, and displaying the library
    """
    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.worksheet = SHEET.worksheet(user).get_all_records()
        self.books = self.books.get_all_records()

    def add_book(self, book, input_data):
        """
        Adds new book both to the data structure and the google sheet.
        """
        book_dict = {}
        book_dict["Title"] = book.title
        book_dict["Author"] = book.author
        book_dict["Pages"] = book.pages
        book_dict["Genres"] = book.categories

        attrs = ["Rating", "Status", "Own Physical", "Own Audiobook"]:
        for attr, data in zip(attrs, input_data):
            book_dict[attr] = data

        self.books.append(book_dict)
        self.worksheet(list(book_dict.values()))
        
    #def sort(self, cat):

    #def filter(self, cat):

    #def edit(self, book):

    #def update_data(self):

#Works
class ConsoleUI:
    """
    Parent class of all interfaces in the program
    Contains render_heading method to display the interface titles
    """
    def __init__(self, stdscr, heading, message):
        self.scr = stdscr
        self.heading = heading
        self.message = message
    
    def render_heading(self):
        """
        Renders a figlet ASCII render of text at the top of the page
        """
        self.scr.clear()
        header = F.renderText(f"       {self.heading}")
        self.scr.addstr(header)

    def display_message(self):
        """
        Displays the main message of the interface to the user
        """
        self.scr.addstr(7, 0, self.message)

    def user_input(self, y, x):
        """
        Creates a textbox for the user to enter at position (x, y)
        Returns the user input
        """
        win = curses.newwin(1, curses.COLS-(x+1), y, x)
        box = Textbox(win)
        self.scr.refresh()
        box.edit()

        return box.gather().strip().lower()

    def render(self):
        """
        Displays the heading and main message in each UI
        """
        self.render_heading()
        self.display_message()

#Works
class LandingUI(ConsoleUI):
    """
    Class for landing page interface object
    """
    def __init__(self, stdscr, heading, message):
        super().__init__(stdscr, heading, message)

    def check_for_user(self):
        """
        Checks the gsheet for the name entered on the landing page
        If there's a match returns true, if no match returns false
        """
        worksheet_list = [worksheet.title for worksheet in SHEET.worksheets()]
        if self.user in worksheet_list:
            return True
        elif self.user not in worksheet_list:
            return False

    def error_check(self):
        """
        Checks user name for errors (use of reserved sheet name or empty submission)
        Returns false to cause recursion if failure, true to allow program to proceed on success
        """
        try:
            if self.name == "__template__":
                raise ValueError(
                    "'__template__' is a reserved user account. Enter a different name"
                )
            if self.name.strip() == "":
                raise ValueError(
                    "cannot accept an empty entry"
                )
        except ValueError as e:
            self.scr.addstr(12, 0, f"\tInvalid entry: {e}, please try again (any key to continue)")
            self.scr.move(14, 8)
            self.scr.getch()
            return False

        return True

    def response(self):
        """
        Displays the user input and prompts
        """
        self.scr.addstr(12, 0, f"\tWelcome {self.name.title()}!")
        self.user = self.name.replace(" ", "")

        if self.check_for_user():
            self.scr.addstr(13, 0, ("\tYou have an active account with "
                                    f"{len(SHEET.worksheet(self.user).get_all_values())-1} "
                                    "entries. Access your library? (y/n)"))
        else:
            self.scr.addstr(13, 0, ("\tYou have not yet created an account. "
                                    "Create a new account? (y/n)"))

        self.scr.move(15, 8)

    def user_control(self):
        """
        Allows user to use key inputs to decide what action to take
        """
        while True:
            key = self.scr.getkey()
            if key == "y":
                if not self.check_for_user():
                    #creates new sheet from template for user data
                    SHEET.duplicate_sheet(0,new_sheet_name=self.user)
                return
            elif key == "n":
                return self.render()

    def render(self):
        """
        Displays the landing page on program start
        Takes user's name as input to retrieve catalog or set up new one
        Returns user's name in proper format
        """
        super().render()
        self.name = self.user_input(10, 25)
        if not self.error_check():
            return self.render()
        self.response()
        self.user_control()

        return self.name, self.user

class AddUI(ConsoleUI):
    """
    For displaying the add book UI to the user.
    Initiated and called in home.main_user_control()
    """
    def __init__(self, stdscr, heading, message, library):
        super().__init__(stdscr, heading, message)
        self.library = library

    def search(self):
        resp = urlopen(f"{GBOOKS}{self.query}")
        self.book_data = json.load(resp)

    def search_ui(self):
        self.results_win = curses.newwin(2, curses.COLS-9, 9, 8)
        self.scr.addstr(12, 0, ("\tIs this the title you wish to add?\n\n"
                                "\tEnter - confirm\n\tn - next result\n"
                                "\tp - prev result\n\ts - enter new search"
                                "\n\tq - quit"))                      

    def add_book(self):
        """
        Allows user to input their data on the book and then store the data
        """
        self.scr.clear()
        self.render_heading()
        query_win = curses.newwin(1, curses.COLS - 9, 7, 8)
        queries = ["How would you rate this book out of 5?",
                ("Is this a book that you: want to read (w), are "
                "currently reading(r), or have read(h)"),
                "Do you own a physical copy? (y/n)",
                "Do you own an audiobook of this book? (y/n)"]

        inputs = []

        for query in queries:
            query_win.clear()
            query_win.addstr(query)
            query_win.refresh()
            inputs.append(self.user_input(9, 8))
            self.library.add_book(self.add_book)

        query_win.clear()
        query_win.addstr("Adding book to library...")
        query_win.refresh()
        self.library.add_book(self.add_book)
        query_win.clear()
        query_win.addstr("Added book! Press any key to return to homepage.")
        query_win.refresh()
        self.scr.getch()
        return

    def main_user_control(self):
        i = 0 
        prev_i = -1

        while True:
            if i != prev_i:
                self.results_win.clear()
                self.results_win.addstr(("Title: "
                                        f"{self.book_data['items'][i]['volumeInfo'].get('title', 'title not found')}"
                                        "\nAuthor: "
                                        f"{self.book_data['items'][i]['volumeInfo'].get('authors','author not found')[0]}"))
                self.results_win.refresh()
                self.scr.move(20, 8)
                prev_i == i
            
            key = self.scr.getkey()
            if key == "\n":
                self.add_book = Book(self.book_data['items'][i]['volumeInfo'])
                return self.confirm_ui()
            elif key == "n":
                if not i == len(self.book_data['items'])-1:
                    i += 1
            elif key == "p":
                if not i == 0:
                    i -= 1
            elif key == "s":
                return self.render()
            elif key == "q":
                return

    def confirm_user_control(self):
        """
        Allows user to control what they want to do when they are viewing detailed book description
        """
        while True:
            key = self.scr.getkey()
            if key == "\n":
                return self.add_book()
            elif key == "b":
                return self.render()

    def confirm_ui(self):
        """
        Brings up more detailed information about book before user confirms
        they wish to add it.
        """
        self.attr_win = curses.newwin(5, curses.COLS-9, 5, 8)
        self.detail_win = curses.newwin(5, curses.COLS - 22, 8, 21)

        #bug if user hit ctrl+x
        self.attr_win.addstr(("Title: \n"
                        "Author: \n"
                        "Pages: \n"
                        "Genres: \n"
                        "Description: "))
        self.detail_win.addstr((f"{self.add_book.title}\n"
                                f"{self.add_book.author}\n"
                                f"{self.add_book.pages}\n"
                                f"{self.add_book.categories}\n"
                                f"{self.add_book.description}"))
        self.scr.addstr(17, 0, ("\tAre these details correct?\n\nEnter - confirm\n"
                                "\tb - return to search\n\tq - quit"))
        self.attr_win.refresh()
        self.detail_win.refresh()
        return self.confirm_user_control()

    def render(self):
        super().render()
        self.query = self.user_input(9, 8).replace(" ", "+")
        self.search()
        self.search_ui()
        self.main_user_control()
        return

#class EditUI(ConsoleUI):

#class SearchUI(ConsoleUI):

#Class SortUI(ConsoleUI):

#class BrowseUI(ConsoleUI):

class Time():
    """
    Class for storing the information on the time for calling in the home UI message
    """
    def __init__(self):
        self.now = datetime.now()

        hour = self.now.hour
        self.am_pm = "am" if hour < 12 else "pm"
        self.hour = 12 if hour == 0 else hour if hour <= 12 else hour - 12
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.day = self.now.day
        self.day_suffix = "st" if self.day%10 == 1 else "nd" if self.day%10 == 2 else "th"
        self.month = self.now.strftime("%B")

class HomeUI(ConsoleUI):
    """
    Class for user home interface object
    """
    def __init__(self, stdscr, heading, message):
        super().__init__(stdscr, heading, message, library)

    def display_controls(self, type):
        if type == "main":
            controls = curses.newwin(9, 32, 12, 8)
            self.scr.refresh()
            controls.addstr(("a - add new title\ne - edit catalog"
                            "\n\ns - search\no - sort catalog by"
                            "\nb - browse entire catalog\n\n"
                            "q - save and quit"))
            controls.refresh()
            self.scr.move(21, 8)

    def main_user_control(self):
        """
        Allows user to use key inputs to decide what action to take
        """
        while True:
            key = self.scr.getkey()
            if key == "a":
                add = AddUI(self.scr, "Add book", ("\tPlease enter the title"
                            " of the book you wish to add:"), self.library)
                add.render()
                return self.render()
            elif key == "e":
                pass
                #edit = EditUI(self.scr, "", "", self.library)
                #edit.render()
                #return self.render()
            elif key == "s":
                pass
                #search = SearchUI(self.scr, "", "", self.library)
                #search.render()
                #return self.render()
            elif key == "o":
                pass
                #sort = SortUI(self.scr, "", "", self.library)
                #sort.render()
                #return self.render()
            elif key == "b":
                pass
                #browse = BrowseUI(self.scr, "", "", self.library)
                #browse.render()
                #return self.render()
            elif key == "q":
                #library.save
                return

    def render(self):
        """
        Displays the users home page on accessing or creating account
        Provides options for which interface the user would like to access
        Returns on user quitting
        """
        super().render()
        self.display_controls("main")
        self.main_user_control()

        return

def display_landing(stdscr):
    """
    Displays the landing page on program start
    Takes user's name as input to retrieve catalog or set up new one
    Returns user's name in proper format
    """
    landing = LandingUI(stdscr, "Great Library", 
                        ("\tWelcome to the great library,"
                        "a console-based catalog of all\n"
                        "\tthe books you have read, "
                        "and want to read!\n\n\tEnter your name: "))

    name, user = landing.render()
    return name, user    

def display_home(stdscr, library):
    """
    Displays the user's home page
    From here they can navigate to the other interfaces
    """
    time = Time()
    home = HomeUI(stdscr, "Library Home", 
                (f"\tWelcome, {library.name.title()}.\n\tThe time is currently "
                f"{time.hour:02d}:{time.now.minute:02d} {time.am_pm}, "
                f"{time.days[time.now.weekday()]} the {time.day}{time.day_suffix} of "
                f"{time.month}, {time.now.year}.\n\n\tHow would you like to access "
                "your library today?"), library)
    home.render()

def main(stdscr):
    #CONFIGURE COLORS
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_AND_BLACK = curses.color_pair(1)
    stdscr.attron(GREEN_AND_BLACK)
    
    name, user = display_landing(stdscr)
    library = UserLibrary(name, user)
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