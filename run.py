#GOOGLE DRIVE/SHEETS API
import gspread
from google.oauth2.service_account import Credentials
#GOOGLE BOOKS API
from urllib.request import urlopen
import json
#CONSOLE TOOLS
from pyfiglet import print_figlet
from colorama import init
init()
from colorama import Fore, Back, Style

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

# search = input("What book are you looking for?\n")

# resp = urlopen(f"{api}{search}")
# book_data = json.load(resp)

# print(book_data['items'][0]['volumeInfo'])

#Testing console display features
#FIGLET
print_figlet("Hello")

#COLORAMA
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background' + Back.RESET)

print(Style.DIM + 'and in dim text')
print(Style.BRIGHT + 'and in bright text')
print(Style.RESET_ALL + 'back to normal now')