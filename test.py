from urllib.request import urlopen
import json
import pprint

GBOOKS = "https://www.googleapis.com/books/v1/volumes?q=intitle:"

resp = urlopen(f"{GBOOKS}confessions+of+an+economic+hitman")
book_data = json.load(resp)

pprint.pprint(book_data)