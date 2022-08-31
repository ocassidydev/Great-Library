from urllib.request import urlopen
import json
import pprint

GBOOKS = "https://www.googleapis.com/books/v1/volumes?q=intitle:"

resp = urlopen(f"{GBOOKS}+10+days+to+motivation")
book_data = json.load(resp)
pprint.pprint(book_data['items'])

#book_data['items'][i]['volumeInfo'].get('title', 'Title not found')[:curses.COLS-17]