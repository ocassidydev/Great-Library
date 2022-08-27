import gspread
from google.oauth2.service_account import Credentials
from urllib.request import urlopen
import json

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
api = "https://www.googleapis.com/books/v1/volumes?q=intitle:"
search = input("What book are you looking for?\n")

resp = urlopen(f"{api}{search}")
book_data = json.load(resp)

print(book_data['items'][0]['volumeInfo'])

