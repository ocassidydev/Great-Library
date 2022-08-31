# Great Library

[Great Library](https://github.com/ocassidydev/great-library) is a console-based application for cataloging books, enabling the user to rate books, record which books they want to read, are reading, and have read, and whether they own the books in print or audiobook format. The application allows viewing the user's entire library of books, their library sorted according to various categories, filtered by certain conditions, and for the user to update information about their book entries. The program uses a [Google Sheet](https://docs.google.com/spreadsheets/d/15-ZM3D7ZH2NcnCf3NG3w2YhyYDXDlKf4xA415rN88O8/edit?usp=sharing) to store and retrieve library data. This is an excellent organising tool for people who can have books stored across a wide variety of formats, but are not prepared to use more time-consuming and busy interfaces to catalog their collection such as goodreads or google books.

## Features 

### Existing Features
- __Creating/accessing user account__

    - On initializing, the program prompts the user to enter their name.
    - In the program, this input is changed into a lower case token, to be used as a name for the user's worksheet in the program's google sheet.
    - The input is also changed to display a proper noun (eg. if I enter oran, the console ouput will display as Oran).
    - The program checks if a worksheet exists with the user's tokenized name. If it exists, it prompts the user to access their account, along with the number of books they have added.
    - If such a worksheet does not exist, it will prompt the user to create a new account. This will duplicate a template worksheet to create a worksheet to store the user's books.
    - This will be valuable to the user, as it allows them to create a unique repository for their books, which they can later access on subsequently running the app.
    \
    &nbsp;

&nbsp;
- __Home interface__

    - On accessing a user account or creating a new account, the program display a home interface. 
    - This greets the user, and tells them the current time in GMT, and the current date.
    - It also prompts the user with their available controls for accessing their library, which it takes as key inputs.
    - This will be valuable to the user, as it offers a straightforward home interface to navigate to all other parts of the program from.
    \
    &nbsp;


&nbsp;
- __Add book interface__

    - This is one of the options from the home menu the user may access. The program displays it on the user pressing 'a'.
    - The program prompts the user to enter the title of the book that they wish to add.
    - The program then changes this input into a search query which is called using the Google Books API.
    - The title and author data from the search results are then displayed to the terminal, with an interface enabling the user to select the book to add, navigate through the different results, to enter a new search, and to quit back to the main menu.
    - If the user selects a book to add, the program brings up a confirmation interface, displaying the full details on the book, and prompting the user if this information is correct. The user is shown keys they can use to control this screen, either to confirm the details, enter a new search, or to quit to the main menu. 
    - If the user confirms, the program will then bring up an interface to enter the user's data on the book (how they rate it, is it a book they want to read or have read, do they own a physical copy etc.)
    - The user progresses through this interface when they hit keys that they are prompted to. 
    - When the user has input all information, the program will add this information to their worksheet in the programs Google sheet, and they will then get a screen confirming their book has been added, and prompting a key press to return to the home interface.
    - This will be valuable to the user, as it offers a straightforward, relatively low effort method of adding a large amount of infromation about a book to their library.
    \
    &nbsp;

&nbsp;
- __Browse interface__ 

    - When the user has at least one book in their library, they will have the options on the home interface to browse their library in a variety of ways.
    - These are all facilitated through the browse interface, which displays the full information on each book entry, as well as providing the user with controls to navigate through the books in their library.
    - The user also has the option of editing the entry. This brings up an interface similar to the add book interface, which allows the user to change their rating, whether they want to read/are reading/have read the book, do they own a physical copy, etc. 
    - The inputs from this will be then input in the user's spreadsheet in the Google sheet, and then they will get a confirmation message which prompts a key press to return to the browse interface. 
    - The user also has the option to quit to the home interface. 
    - This is a valuable feature to the user, as it allows them to navigate their library, and update information on individual books that they have.
    \
    &nbsp;

&nbsp;
- __Search option__

    - This is a part of the home interface. When the user presses 's', the program changes the home interface to accept user controls on what category they which to search the book by.
    - They can search by title, author, or genre. 
    - When the user has selected which category they which to search by, the interface changes again to take a user input of search terms.
    - This is then changed into a search query, which all books in the library with matching data for the selected category are returned as search results of.
    - These search results are then displayed to the user using the browse interface.
    - The user can also hit q to go back to the main home interface.
    - This is valuable to the user, as it enables them to find specific book(s) in their library to either display or edit.
    \
    &nbsp;

&nbsp;
- __Sort option__ 

    - This is also a part of the home interface. When the user presses 'o', the program changes the home interface to take user confrols on what category they wish to sort books by.
    - They can sort by title alphabetically, sort by author alphabetically, sort by the number of pages, sort by genres alphabetically, and sort by rating. 
    - Any of these options returns a sorted library of books, which is then displayed to the user using the browse interface.
    - The user can also quit to the main home interface. 
    - This is valuable to the user, as it allows the them to browse a sorted list of books according to a variety of attributes. 
    \
    &nbsp;

&nbsp;
- __Filter option__

    - This is a further part of the home interface. When the user presses 'f', the program changes the home interface to take user controls on which category they wish to filter books by.
    - They can filter by the read status, do they own a physical copy, do they own an audiobook. 
    - When an option is selected, the interface further prompts which of these they want to display (eg. only display books they have finished)
    - Taking the user's desired inputs, the program then returns a subtended library of only books that pass the user's desired filter. 
    - This is displayed using the browse interface, which the user is still capable of editing the library from. 
    - This is valuable to the user, as it allows them to only browse books fiting certain criteria (eg. books on their to read list).
    \
    &nbsp;

- __Quit option__
    - This allows the user to quit the program to return to the landing interface.
    - It is indicated that this "saves" their data, however this is all already done. This is only to indicate that they will be able to open the program again and still have their library there.
    - This adds value to the user, as it provides a means of closing the program out to the landing interface and reassures them their data will still be there next time.
    \
    &nbsp;

&nbsp;
### Features Left to Implement

&nbsp;

***Username/password system***

I wanted to give the user the option to create a more formal account with a proper username and password. However, I decided against implementing this owing to the wish to make this program simple to debug and minimize complexity of running it each time, along with wanting to make a system that can flexibly handle string inputs to find user accounts.

&nbsp;

***Delete book***

I also want to implement functionality that would enable the user to delete book entries, likely contained within the browse books interface similar to the edit functionality. This would be straightforward to implement by taking the existing logic for the edit functionality. However, I also would want to include some kind of confirmation screen for this, in order to prevent the user accidentally deleting books by errant key presses.

&nbsp;

***Edit book description***
Another feature I considered was a means to update book descriptions. Often, the google books data is incomplete, with the description either entirely missing or in a less than presentable format for the program. My idea is to use the curses module that I use to give the user a live edit window where they can alter the existing description of the book, so that they don't need to completely retype all the information if some there is still useable. However, this was not implemented due to the large complexity in realising an interface for this. 

&nbsp;

## Testing 
### Landing interface
- The following table goes through each text input in the landing interface, listing the expected behavior and what actually occurs. 

|Text input                |Expected Behavior                                 |What Occurs                            |Working as intended?   |
|:------------------------|:-------------------------------------------------|:--------------------------------------|:---------------------:|
|Enter empty text         |Returns invalid entry, tells user to any key to any key to try again|Returns invalid entry, tells user to any key to any key to try again|✔                     |
|Enter name (existing user)|Displays welcome and how many books user has, prompting key to enter account|Displays welcome and how many books user has, prompting key to enter account|✔                     |
|Enter name (new user)|Displays welcome and tells user they do not have account, prompts key enter to create one|Displays welcome and tells user they do not have account, prompts key enter to create one|✔                     |

\
&nbsp;
- The following table goes through each key input in the landing interface, listing the expected behavior and what actually occurs. 

|Key input                  |Expected Behavior                                  |What Occurs                                        |Working as intended?   |
|:--------------------------|:--------------------------------------------------|:--------------------------------------------------|:---------------------:|
|   y or enter              |Opens home UI with user details                    |Opens home UI with user details                    |✔                     |
|   n                       |Reopens landing UI from start                      |Reopens landing UI from start                      |✔                     |

\
&nbsp;

### Home interface
- The following table goes through each possible key input in the home interface, listing expected behavior and what actually occurs.

|Key input          |Expected Behavior     |What Occurs             |Working as intended?   |
|:------------------|:---------------------|:-----------------------|:---------------------:|
| b                 |Opens browse libary UI|Opens browse library UI |✔                     |
| a                 |Opens add book UI     |Opens add book UI       |✔                     |
| s                 |Changes control window to search options|Changes control window to search options|✔                     |
| o                 |Changes control window to sort options|Changes control window to sort options|✔                     |
| f                 |Changes control window to filter options|Changes control window to filter options|✔                     |
| q                 |Closes out to landing UI|Closes out to landing UI|✔                     |

\
&nbsp;
#### Home interface - search options
- The following table goes through each possible key input in the search options part of the home interface, listing expected behavior and what actually occurs.

|Key input          |Expected Behavior     |What Occurs             |Working as intended?   |
|:------------------|:---------------------|:-----------------------|:---------------------:|
| t                 |Changes control window to search input|Changes control window to search input|✔                     |
| a                 |Changes control window to search input|Changes control window to search input|✔                     |
| g                 |Changes control window to search input|Changes control window to search input|✔                     |
| q                 |Goes back to starting state of home interface|Goes back to starting state of home interface|✔                     |

\
&nbsp;
#### Home interface - search
- The following table goes through each possible text input in the search part of the home interface, listing expected behavior and what actually occurs.

|Text input          |Expected Behavior     |What Occurs             |Working as intended?   |
|:------------------|:---------------------|:-----------------------|:---------------------:|
|Text with a match in library|Brings up browse interface to display books that match search|Brings up browse interface to display books that match search|✔                     |
|Text with no match in library|Informs user there is no match, any keys to start search from search option interface|Informs user there is no match, any keys to start search from search option interface|✔                     |
|Empty text|Goes back to starting state of home interface|Goes back to starting state of home interface|✔                     |

\
&nbsp;
#### Home interface - sort options
- The following table goes through each possible key input in the sort options part of the home interface, listing expected behavior and what actually occurs.

|Key input          |Expected Behavior     |What Occurs             |Working as intended?   |
|:------------------|:---------------------|:-----------------------|:---------------------:|
| t                 |Displays browse interface of books in alphabetical order by title|Displays browse interface of books in alphabetical order by title|✔                     |
| a                 |Displays browse interface of books in alphabetical order by author first name|Displays browse interface of books in alphabetical order by author first name|✔                     |
| p                 |Displays browse interface of books in ascending order of pages|Displays browse interface of books in ascending order of pages|✔                     |
| g                 |Displays browse interface of books in alphabetical order by genres|Displays browse interface of books in alphabetical order by genres|✔                     |
| r                 |Displays browse interface of books in descending order by rating|Displays browse interface of books in descending order by rating|✔                     |
| q                 |Goes back to starting state of home interface|Goes back to starting state of home interface|✔                     |

\
&nbsp;
#### Home interface - filter options
- The following table goes through each possible key input in the filter options part of the home interface, listing expected behavior and what actually occurs.

|Key input          |Expected Behavior     |What Occurs             |Working as intended?   |
|:------------------|:---------------------|:-----------------------|:---------------------:|
| r                 |Changes control window to select read status options|Changes control window to select read status options|✔                     |
| o                 |Changes control window to select ownership status options|Changes control window to select ownership status options|✔                     |
| a                 |Changes control window to select ownership status options|Changes control window to search input select ownership status options|✔                     |
| q                 |Goes back to starting state of home interface|Goes back to starting state of home interface|✔                     |

\
&nbsp;
#### Home interface - filter options
- The following table goes through each possible key input in the filter parameters part of the home interface, listing expected behavior and what actually occurs.

|Key input          |Expected Behavior     |What Occurs             |Working as intended?   |
|:------------------|:---------------------|:-----------------------|:---------------------:|
| w                 |displays browse interface with only books that the user wants to read|displays browse interface with only books that the user wants to read|✔                     |
| r                 |displays browse interface with only books that the user is reading|displays browse interface with only books that the user is reading|✔                     |
| f                 |displays browse interface with only books that the user has finished|displays browse interface with only books that the user has finished|✔                     |
| o                 |displays browse interface with only books that the user owns physically|displays browse interface with only books that the user owns physically|✔                     |
| d                 |displays browse interface with only books that the user owns as an audiobook|displays browse interface with only books that the user owns as an audiobook|✔                     |
| q                 |Goes back to starting state of home interface|Goes back to starting state of home interface|✔                     |

\
&nbsp;
### Browse interface
- The following table goes through each possible key input in the browse interface, listing expected behavior and what actually occurs.

|Key input          |Expected Behavior     |What Occurs             |Working as intended?   |
|:------------------|:---------------------|:-----------------------|:---------------------:|
| n or arrow right  |displays next entry, unless at end of list, where it does nothing|displays next entry, unless at end of list, where it does nothing|✔                     |
| p or arrow left  |displays previous entry, unless at beginning of list, where it does nothing|displays previous entry, unless at beginning of list, where it does nothing|✔                     |
| e                 |initiates user input sequence|initiates user input sequence|✔                     |
| q                 |quits to home interface|quits to home interface|✔                     |


\
&nbsp;

### Add interface
- The following table goes through each possible text input in the search part of the add interface, listing expected behavior and what actually occurs.

|Text input          |Expected Behavior     |What Occurs             |Working as intended?   |
|:------------------|:---------------------|:-----------------------|:---------------------:|
|Any input text     |Brings up relevant search results|Brings up relevant search result|✔                     |
|Empty text input   |Closes out to home interface|Closes out to home interface|✔                     |

\
&nbsp;
- The following table goes through each possible key input in the search results part of the add interface, listing expected behavior and what actually occurs.

|Key input          |Expected Behavior     |What Occurs         |Working as intended?   |
|:------------------|:---------------------|:-------------------|:---------------------:|
| n or arrow right  |displays next entry, unless at end of list, where it does nothing|displays next entry, unless at end of list, where it does nothing|✔                     |
| p or arrow left  |displays previous entry, unless at beginning of list, where it does nothing|displays previous entry, unless at beginning of list, where it does nothing|✔                     |
| enter             |brings up confirm interface|brings up confirm interface|✔                     |
| s                 |goes back to start of add interface|goes back to start of add interface|✔                     |
| q                 |quits to home interface|quits to home interface|✔                     |

\
&nbsp;
#### Add interface - confirm screen
- The following table goes through each possible key input in the confirmation part of the add interface, listing expected behavior and what actually occurs.
|Key input          |Expected Behavior     |What Occurs         |Working as intended?   |
|:------------------|:---------------------|:-------------------|:---------------------:|
| enter             |initiates user input sequence|initiates user input sequence|✔                     |
| b                 |returns to beginning of add interface|returns to beginning of add interface|✔                     |
| q                 |quits to home interface|quits to home interface|✔                     |

\
&nbsp;
### User input sequence/edit interface
- The following table goes through each part of the user input sequence that happens in the add interface and when the user edits entries in their library
|Sequence part         |Expected Behavior     |What Occurs         |Working as intended?   |
|:---------------------|:---------------------|:-------------------|:---------------------:|
| rating               |updates gsheet with number from key press|updates gsheet with number from key press|✔                     |
| read status          |updates gsheet with option from key press|updates gsheet with option from key press|✔                     |
| own physical         |updates gsheet with option from key press|updates gsheet with option from key press|✔                     |
| own audiobook        |updates gsheet with option from key press|updates gsheet with option from key press|✔                     |

\
&nbsp;
### Bugs 

    - Bug where if user's library contains no books that have ratings (ie. user has entered n/a on all of them), then sorting by rating will crash the program as the returned sorted library is empty.
    - Bug where if the user's library contains no books fitting a certain criteria (ie. no books that have been finished), then filtering by that criteria will as the returned filtered library is empty.  
    - Various bugs where windows would not display properly or empty. These varied in severity, from slightly breaking the interface to completely crashing the program.
    - Occasional bug in add interface where search results from google break in the window due to title being too long.
    - Rare bug in add interface for certain book titles where the process of parsing the title string into a book object crashes program.

&nbsp;
### APIs

    - This project used the [Google Sheets API](https://developers.google.com/sheets/api/) along with the [Google Drive API](https://developers.google.com/drive/api) in order to store and retrieve user's book data. 
    - This project also made use of the [Google Books API](https://developers.google.com/books/) to retrieve infromation about books the user wished to add. 

&nbsp;
### Libraries 

    - This project heavily relied on the [curses](https://docs.python.org/3/library/curses.html#module-curses) module. This module is useful for handling a dynamic console-based interface, as it allows not only to clear the console, but to create windows within the console area that can be dynamically updated without affecting any text outside of them.
    - In order to display ASCII art-style headings, the [pyfiglet](http://www.figlet.org/) module was used. This enables rendering strings as a ASCII-style text.
    - To access the Google Sheets API and use the spreadsheet I created for the project, gspread and google.oauth2 were used. google.oauth2 authenticates my credentials from the creds.json to access the Google sheet, while gspread enables insertion and retrieval of data to and from the sheet.
    - To use the google books API, urllib and json were also used. urllib was used to retrieve a json object from the search query link that would be generated from user input, and json would then return the search results as a ditionary. 
    - datetime was also used to display the time and date on the home interface.

&nbsp;
### Unfixed Bugs

    - It is very likely that there are google book entries out there with data that can crash the program completely. I handled some edge cases when it came to long book titles and long descriptions, however it's difficult to know if that fully covers all possibilities. An author name wider than the console size would crash the add interface, for example. This is a downside to using curses, as any console output outside of where it's expected will raise an error.

&nbsp;
## Deployment

- This project was deployed using [heroku](https://heroku.com), using the following steps:

- In the workspace:
    - before any commits were made, "creds.json" was added to .gitignore
    - run "pip3 freeze > requirements.txt"

- On heroku:
    - On the dashboard "New">"Create new app"
    - Entered "great-library" for the app name, selected "Europe" as the region
    - Clicked "Create app"
    - In "Settings">"Reveal Config Vars" entered 2 creds
    - PORT - 8000 
    - CREDS - the contents of the creds.json file
    - In "Settings">"Add buildpack" added 2 buildpacks, in order
    - heroku/python
    - heroku/nodejs
    - In "Deploy">"Deployment Method" selected Github
    - Entered "great-library" into repo name field
    - Ensured main was the branch selected to deploy, and then clicked "Enable Automatic Deploys" to sync with git pushes

&nbsp;

- For local deployment, run the following command:

      git clone https://github.com/ocassidydev/blackjack.git

&nbsp;
## Credits 

### Code
- The [curses documentation](https://docs.python.org/3/library/curses.html#module-curses) was useful in providing an easy reference point for the many objects and method needed to build a UI. 
- The [gspread documentation](https://docs.gspread.org/en/latest/user-guide.html#updating-cells) was used at mutliple points throughout the project to figure out how to store and retrieve data on the sheet.
- [Tech With Tim's](https://www.youtube.com/c/TechWithTim) video series of tutorials on using the curses library was very helpful in getting used to using the module.
- Throughout the project, I refreshed myself on number of concepts on [GeeksforGeeks](https://www.geeksforgeeks.org/), [StackOverflow](https://stackoverflow.com/) and [freeCodeCamp](https://www.freecodecamp.org).
&nbsp;
