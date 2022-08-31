# Great Library

[Great Library](https://github.com/ocassidydev/great-library) is a console-based application for cataloging books, enabling the user can rate the books they own, indicate which bopoks they want to read, are reading, and have read, and whether they own the books in print or audiobook format. The application allows viewing the user's entire library of books, their library sorted according to various categories, filtered by certain conditions, and for the user to update information about their book entries.

&nbsp;
## Features 

### Existing Features
- __Creating/accessing user account__

    - On initializing, the program prompts the user to enter their name.
    - In the program, this input is changed into a lower case token, to be used as a name for the user's worksheet in the program's google sheet.
    - The input is also changed to display a proper noun (eg. if I enter oran, the console ouput will display as Oran).
    - The program checks if a worksheet exists with the user's tokenized name. If it exists, it prompts the user to access their account, along with the number of books they have added
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
    - This allows the user to quit the program.
    - It is indicated that this "saves" their data, however this is all already done. This is only to indicate that they will be able to open the program again and still have their library there.
    - This adds value to the user, as it provides a means of closing the program and reassures them their data will still be there next time.
    \
    &nbsp;

&nbsp;
### Features Left to Implement

&nbsp;

***Username/password system***

I wanted to give the user the option to create a more formal account. 

&nbsp;

***Delete book***


&nbsp;

***Edit book description***

I also wanted to add a means of having the cards animate as they appeared, preferably by moving from something graphical element that is stylized like a deck and to flip over from face down. This could be acheived in css at least in part, however until I can get cards to play sequentially doing this is redundant, the game would just skip to the round end messages while the player is still seeing card dealing animations and it would be too confusing. The same redesign as mentioned above would need to be implemented first.

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
|   y                       |Opens home UI with user details                    |Opens home UI with user details                    |✔                     |
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
| t                 |Changes control window to search input|Changes control window to search input|✔                     |
| a                 |Changes control window to search input|Changes control window to search input|✔                     |
| p                 |Changes control window to search input|Changes control window to search input|✔                     |
| g                 |Goes back to starting state of home interface|Goes back to starting state of home interface|✔                     |

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
| n or arrow right  |displays next entry, unless at end of list, where it does nothing||✔                     |
||||✔                     |
||||✔                     |

\
&nbsp;

### Bugs 

    - Bug where if user's library contains no books that have ratings (ie. user has entered n/a on all of them), then sorting by rating will crash the program as the returned sorted library is empty
    - Bug where if the user's library contains no books fitting a certain criteria (ie. no books that have been finished), then filtering by that criteria will as the returned filtered library is empty  
    - Various bugs where windows would not display properly or empty. These varied in severity, from slightly breaking the interface to completely crashing the program.
    - Occasional bug in add interface where search results from google break in the window due to title being too long

&nbsp;
### Libraries 

    - 

&nbsp;
### Unfixed Bugs
   
&nbsp;
## Deployment

- This project was deployed using [heroku](https://heroku.com), using the following steps:

  - 

&nbsp;

- For local deployment, run the following command:

      git clone https://github.com/ocassidydev/blackjack.git

&nbsp;
## Credits 

### Code

- 
&nbsp;
