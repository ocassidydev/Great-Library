# GOOGLE DRIVE/SHEETS API
import gspread
from google.oauth2.service_account import Credentials
# GOOGLE BOOKS API
from urllib.request import urlopen
import json
# CONSOLE TOOLS
from pyfiglet import Figlet
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

from datetime import datetime

from textwrap import wrap

# Plugging in APIs
# DRIVE AND SHEET
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('great_library')

# GOOGLE BOOKS
GBOOKS = "https://www.googleapis.com/books/v1/volumes?q=intitle:"

# FIGLET
F = Figlet()


class Book:
    """
    Stores book data for easier recall and use.
    Has two distinct calls through search_bool, 
    either from raw API data or clean in-house data.
    """
    def __init__(self, bookdata, search_bool=False):
        if search_bool:
            self.title = bookdata.get('title', 'title not found')
            self.author = bookdata.get('authors', 'author not found')[0]
            self.pages = bookdata.get('pageCount', 'page count not found')
            self.categories = ", ".join(bookdata.get('categories', ['genres not found']))
            description = bookdata.get('description', 'description not found')
            if len(description) >= 4*(curses.COLS - 22)-3:
                description = description[:4*(curses.COLS - 22)-3] + "..."
            self.description = description
        else:
            self.title = bookdata["Title"]
            self.author = bookdata["Author"]
            self.pages = bookdata["Pages"]
            self.categories = bookdata["Genres"]
            self.description = bookdata["Description"]
            self.rating = bookdata["Rating"]
            self.status = bookdata["Status"]
            self.ownphys = bookdata["Own Physical"]
            self.ownaud = bookdata["Own Audiobook"]


class UserLibrary:
    """
    Stores the user's data as a list of dictionaries for displaying and editing.
    Contains various methods for filtering, sorting, and displaying the library.
    """
    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.worksheet = SHEET.worksheet(user)
        self.books = self.worksheet.get_all_records()
    
    attrs = ["Rating", "Status", "Own Physical", "Own Audiobook"]

    def add_book(self, book, input_data):
        """
        Adds new book both to the data structure and the google sheet.
        """
        book_dict = {}
        book_dict["Title"] = book.title
        book_dict["Author"] = book.author
        book_dict["Pages"] = book.pages
        book_dict["Genres"] = book.categories
        book_dict["Description"] = book.description

        for attr, data in zip(self.attrs, input_data):
            book_dict[attr] = data

        self.books.append(book_dict)
        self.worksheet.append_row(list(book_dict.values()))
        
    def edit_book(self, index, input_data):
        """
        Updates a book entry with user input
        """
        for i, (attr, data) in enumerate(zip(self.attrs, input_data)):
            self.books[index][attr] = data
            self.worksheet.update_cell(index+2, i+6, data)
        
    def sort(self, cat):
        """
        Function that returns an ordered list of book entry dictionaries corresponding
        to a library sorted by the input category.
        """
        #avoids soft copying
        sort_attrs = [book[cat].replace("The ", "") for book in self.books]
        sort_attrs.sort()
        attrs = [book[cat].replace("The ", "") for book in self.books]

        sorted_books = []
        for s_attr in sort_attrs:
            i = attrs.index(s_attr)
            sorted_books.append(self.books[i])

        return sorted_books

    def filter(self, cat, filter):
        """
        Functions that returns a list of book entries satisfying a certain
        criteria for a particular category.
        """
        filtered_books = [book for book in self.books if book[cat] == filter]
        return filtered_books

    def search(self, cat, search):
        search = search.replace(" ", "+")
        searched_books = []
        for book in self.books:
            term = book[cat].strip().lower().replace(" ", "+")
            if search in term:
                searched_books.append(book)

        return searched_books    


class DisplayBookMixin():
    """
    Mixin for a commonly used method of displaying information on the book 
    object on the screen and taking user input on book data.
    """
    queries = ["","How would you rate this book out of 5? Hit enter if n/a.",
                ("Is this a book that you: want to read (w), are "
                "currently reading (r), or have finished (f)?"),
                "Do you own a physical copy? (y/n)",
                "Do you own an audiobook of this book? (y/n)", ""]

    def display_book(self, book):
        self.attr_win = curses.newwin(13, curses.COLS-9, 7, 8)
        self.detail_win = curses.newwin(13, curses.COLS - 22, 7, 21)
        self.scr.refresh()

        self.refresh_win(self.attr_win, ("Title: \n"
                                    "Author: \n"
                                    "Pages: \n"
                                    "Genres: \n"
                                    "Description: "))
        self.refresh_win(self.detail_win, (f"{book.title}\n"
                                        f"{book.author}\n"
                                        f"{book.pages}\n"
                                        f"{book.categories}\n"
                                        f"{book.description}"))
        self.scr.move(22, 8)

        self.attr_win.refresh()
        self.detail_win.refresh()
        return

    def user_entry_input(self):
        """
        Takes user key inputs for variety of information about 
        the book entry they're adding/editing
        """
        self.inputs = []
        for query in self.queries:
            self.refresh_win(self.query_win, query)
            self.scr.move(11, 8)

            if query == "":
                continue
            
            while True:
                key = self.scr.getkey()

                if "out of 5?" in query:
                    if key.isnumeric():
                        if int(key) in list(range(1,6)):
                            self.inputs.append(f"{key}/5")
                            break
                    elif key == "\n":
                        self.inputs.append("n/a")
                        break

                elif "have finished (f)?" in query:
                    if key == "w":
                        self.inputs.append("Want to read")
                        break
                    elif key == "r":
                        self.inputs.append("Currently reading")
                        break
                    elif key == "f":
                        self.inputs.append("Finished")
                        break

                elif "physical copy?" or "audiobook" in query:
                    if key == "y":
                        self.inputs.append("Yes")
                        break
                    elif key == "n":
                        self.inputs.append("No")
                        break


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

    def refresh_win(self, win, string):
        """
        Clears a window, prints a string to it, and refreshes
        """
        win.clear()
        win.addstr(string)
        win.refresh()

    def clear_page(self):
        """
        Clears the page, reprinting the heading
        """
        self.render_heading()
        self.scr.refresh()

    def render(self):
        """
        Displays the heading and main message in each UI
        """
        self.render_heading()
        self.display_message()


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


class AddUI(DisplayBookMixin, ConsoleUI):
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

    def add_new_book(self):
        """
        Allows user to input their data on the book and then store the data
        """
        self.clear_page()

        self.scr.addstr(7, 8, self.add_book.title)
        self.query_win = curses.newwin(curses.LINES - 10, curses.COLS - 9, 9, 8)
        self.user_entry_input()
        
        self.refresh_win(self.query_win, "Adding book to library...")
        # Checks if book is already in user's library
        if self.add_book.title in [book["Title"] for book in self.library.books]:
            self.refresh_win(self.query_win, f"{self.add_book.title} is already in your library!"
                                            "Press any key to return to add book interface.")
            
            self.scr.getch()
            return self.render()
        else:
            self.library.add_book(self.add_book, self.inputs)
            self.refresh_win(self.query_win, "Added book! Press any key to return to homepage.")

            self.scr.getch()
            return

    def main_user_control(self):
        i = 0 
        prev_i = -1

        while True:
            if i != prev_i:
                self.refresh_win(self.results_win, 
                                ("Title: "
                                f"{self.book_data['items'][i]['volumeInfo'].get('title', 'title not found')}"
                                "\nAuthor: "
                                f"{self.book_data['items'][i]['volumeInfo'].get('authors','author not found')[0]}"))
                
                self.scr.move(20, 8)
                prev_i = i
            
            key = self.scr.getkey()
            if key == "\n":
                self.add_book = Book(self.book_data['items'][i]['volumeInfo'], True)
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
                return self.add_new_book()
            elif key == "b":
                return self.render()
            elif key == "q":
                return

    def confirm_ui(self):
        """
        Brings up more detailed information about book before user confirms
        they wish to add it.
        """
        self.display_book(self.add_book)
        self.input_win = curses.newwin(5, curses.COLS-9, 16, 8)
        self.refresh_win(self.input_win,("Are these details correct?\n\n"
                                        "Enter - confirm\nb - return "
                                        "to search\nq - quit"))
        return self.confirm_user_control()

    def render(self):
        super().render()
        self.query = self.user_input(9, 8).replace(" ", "+")
        self.search()
        self.search_ui()
        self.main_user_control()
        return


class BrowseUI(DisplayBookMixin, ConsoleUI):
    def __init__(self, stdscr, heading, message, library, ordered_library=None, category=None, filter_opt=None):
        super().__init__(stdscr, heading, message)
        self.library = library
        self.ordered_library = ordered_library
        self.category = category
        self.filter_opt = filter_opt

    def edit_book(self, i):
        """
        Allows user to input their new data on the book and then store the data
        """
        if self.ordered_library:
            i = self.library.books.index(self.ordered_library[i])

        self.clear_page()
        self.scr.addstr(7, 8, self.library.books[i]["Title"])
        self.query_win = curses.newwin(curses.LINES - 10, curses.COLS - 9, 9, 8)
        self.user_entry_input()
        
        self.refresh_win(self.query_win, "Editing book entry in library...")
        self.library.edit_book(i, self.inputs)
        self.refresh_win(self.query_win, "Edited entry! Press any key to return to browse.")

        if "Filter" in self.heading:
            self.ordered_library = self.library.filter(self.category, self.filter_opt)

        self.scr.getch()

        return

    def browse_display_book(self):
        """
        Version of display_book that contains extra user input information
        """
        self.display_book(self.book)
        self.attr_win.addstr(8, 0, ("Rating: \n"
                                    "Status: \n"
                                    "Own print: \n"
                                    "Audiobook: \n"))
        self.detail_win.addstr(8, 0, (f"{self.book.rating}\n"
                                    f"{self.book.status}\n"
                                    f"{self.book.ownphys}\n"
                                    f"{self.book.ownaud}\n"))
        self.scr.move(23, 8)

        self.attr_win.refresh()
        self.detail_win.refresh()
        return

    def scroll_books(self):
        """
        Displays book information from the library to the screen and allows
        the user to iterate through their library using the arrow keys
        """
        if self.ordered_library is None:
            books = self.library.books
        else:
            books = self.ordered_library

        i = 0
        prev_i = -1

        while True:
            if i != prev_i:
                self.book = Book(books[i])
                self.browse_display_book()
                
                prev_i = i

            key = self.scr.getkey()
            
            if key == "KEY_RIGHT":
                if not i == len(books)-1:
                    i += 1
            elif key == "KEY_LEFT":
                if not i == 0:
                    i -= 1
            elif key == "e":
                self.edit_book(i)
                return self.render()
            elif key == "q":
                return

    def render(self):
        super().render()
        self.scr.addstr(21, 8, "arrow right/left - navigate entries\te - edit entry\tq - quit")
        self.scroll_books()
        return


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
    def __init__(self, stdscr, heading, message, library):
        super().__init__(stdscr, heading, message)
        self.library = library
        self.main_control = ("b - browse and edit\na - add book"
                            "\n\ns - search book\no - sort books by\n"
                            "f - filter books by\n\nq - save and quit")
        self.sort_control = ("t - sort by title\na - sort by author\n"
                            "p - sort by pages\ng - sort by genres\n"
                            "r - sort by rating\n\nq - quit")
        self.filter_control = ("r - filter by read status\n"
                                "o - filter by physical ownership\n"
                                "a - filter by audiobook ownership\n\n"
                                "q - quit")
        self.search_control = ("t - search by title\na - search by author\n"
                                "\ng - search by genres\n\nq - quit")

    def update_time(self):
        """
        Updates the main message on the home screen each time
        it is rendered so the time stays accurate each time the
        home is rendered.
        """
        time = Time()
        self.message = (f"\tWelcome, {self.library.name.title()}.\n\tThe time is currently "
                        f"{time.hour:02d}:{time.now.minute:02d} {time.am_pm}, "
                        f"{time.days[time.now.weekday()]} the {time.day}{time.day_suffix} of "
                        f"{time.month}, {time.now.year}.\n\n\tHow would you like to access "
                        "your library today?")

    def panel(self, lines, cols, string):
        """
        Creates the panel of user controls based on user input
        """
        x, y = 8, 12
        self.controls = curses.newwin(lines, cols, y, x)
        self.scr.refresh()
        self.refresh_win(self.controls, string)
        self.scr.move(y + lines + 1, x)

    def display_controls(self, type):
        """
        Displays the different types of controls to the main panel.
        """
        if type == "main":
            self.panel(8, 20, self.main_control)
        elif type == "search":
            self.panel(6, 21, self.search_control)
        elif type == "sort":
            self.panel(7, 19, self.sort_control)
        elif type == "filter":
            self.panel(5, 34, self.filter_control)

    def search_user_control(self):
        """
        Allows user to use key inputs to decide what action to take
        """
        while True:
            key = self.scr.getkey()
            if key == "b":
                browse = BrowseUI(self.scr, "Library browse", "", self.library)
                browse.render()
                return self.render()
            elif key == "a":
                add = AddUI(self.scr, "Add book", ("\tPlease enter the title"
                            " of the book you wish to add:"), self.library)
                add.render()
                return self.render()
            elif key == "s":
                self.refresh_win(self.controls, "")
                self.display_controls("search")
                return self.render()
            elif key == "o":
                self.refresh_win(self.controls, "")
                self.display_controls("sort")
                return self.render()
            elif key == "f":
                self.refresh_win(self. controls, "")
                self.display_
            elif key == "q":
                return

    def sort(self, sortstring):
        """
        Refactor to avoid repetition in sort_user_control
        """
        sort_library = self.library.sort(sortstring.capitalize())
        browse = BrowseUI(self.scr, f"Sort by {sortstring}", "", self.library, sort_library)
        return browse.render()

    def sort_user_control(self):
        """
        Allows user to use key inputs to decide how they want to sort library.
        """
        while True:
            key = self.scr.getkey()
            if key == "t":
                return self.sort("title")
            elif key == "a":
                return self.sort("author")
            elif key == "p":
                return self.sort("pages")
            elif key == "g":
                return self.sort("genres") 
            elif key == "r":
                return self.sort("rating")
            elif key == "q":
                return 
    
    def get_filter_input(self):
        """
        Gets the filter the user wants to impose on their chosen category
        """
        if "Status" in self.category:
            self.panel(7, 44, ("Which read status do you want to filter by?\n"
                            "\nw - books you want to read\nr - books you are"
                            " reading\nf - books you have finished\n\nq - quit"))
            while True:
                key = self.scr.getkey()
                if key == "w":
                    return "Want to read"
                elif key == "r":
                    return "Currently reading"
                elif key == "f":
                    return "Finished"
        else:
            phys_aud = self.category.split(" ")[1].lower()
            self.panel(6, 60, (f"Which {phys_aud} ownership status do you want to "
                            f"display by?\n\no - own {phys_aud}\nd - don't own "
                            f"{phys_aud}\n\nq - quit"))
            while True:
                key = self.scr.getkey()
                if key == "o":
                    return "Yes"
                elif key == "d":
                    return "No"

    def filter(self):
        """
        Filters library by chosen category
        """
        if self.category == "Status":
            cat_string = "read status"
        else:
            cat_string = "own"

        self.filter_opt = self.get_filter_input()
        filter_library = self.library.filter(self.category, self.filter_opt)
        browse = BrowseUI(self.scr, f"Filter by {cat_string}", "", self.library, filter_library, self.category, self.filter_opt)
        return browse.render()

    def filter_user_control(self):
        """
        Allows user to use key inputs to decide what they want to filter by
        """
        while True:
            key = self.scr.getkey()
            if key == "r":
                self.category = "Status"
                return self.filter()
            elif key == "o":
                self.category = "Own Physical"
                return self.filter()
            elif key == "a":
                self.catgory = "Own Audiobook"
                return self.filter()
            elif key == "q":
                return

    def search(self):
        """
        Takes users search term, call
        """
        self.refresh_win(self.controls, "")
        self.panel(2, 51, ("(Note: mispelled searches will not return results)\n"
                        "Enter your search terms:"))
        search = self.user_input(13, 34)
        searched_library = self.library.search(self.category, search)

        # Handles case where no results of search query
        if len(searched_library) == 0:
            self.refresh_win(self.controls, "No Results found! Press any key to try another search")
            self.scr.move(9, 8)
            self.scr.getch()
            self.change_main_panel("search")
            self.search_user_control()
            return
        
        browse = BrowseUI(self.scr, "Search", "", self.library, searched_library)
        return browse.render()

    def search_user_control(self):
        """
        Displays search options to user and gets key input to find 
        which category user wishes to search
        """
        while True:
            key = self.scr.getkey()
            if key == "t":
                self.category = "Title"
                return self.search()
            elif key == "a":
                self.category = "Author"
                return self.search()
            elif key == "g":
                self.category = "Genres"
                return self.search()
            elif key == "q":
                return

    def change_main_panel(self, string):
        """
        Refactor to avoid repetition in main_user_controls
        """
        self.refresh_win(self.controls, "")
        self.display_controls(string)

    def main_user_control(self):
        """
        Allows user to use key inputs to decide what action to take
        """
        while True:
            key = self.scr.getkey()
            if key == "b":
                browse = BrowseUI(self.scr, "Library browse", "", self.library)
                browse.render()
                return self.render()
            elif key == "a": 
                add = AddUI(self.scr, "Add book", ("\tPlease enter the title"
                            " of the book you wish to add:"), self.library)
                add.render()
                return self.render()
            elif key == "s":
                self.change_main_panel("search")
                self.search_user_control()
                return self.render()
            elif key == "o":
                self.change_main_panel("sort")
                self.sort_user_control()
                return self.render()
            elif key == "f":
                self.change_main_panel("filter")
                self.filter_user_control()
                return self.render()
            elif key == "q":
                return

    def render(self):
        """
        Displays the users home page on accessing or creating account.
        Provides options for which interface the user would like to access.
        Returns on user quitting.
        """
        self.update_time()
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
    home = HomeUI(stdscr, "Library Home", "", library)
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

# try:
#     wrapper(main)
# except Exception, err:
#     print(f"Program failed, error: {str(err)}. Click 'run program' to restart")