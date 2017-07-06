from bs4 import BeautifulSoup, SoupStrainer
import requests
import sqlite3
from fake_useragent import UserAgent
import pickle


ua = UserAgent()
headers = {'User-Agent': ua.chrome}

base_url = 'http://www.imdb.com'

r = requests.get('http://www.imdb.com/chart/top', headers=headers)

soup = BeautifulSoup(r.content, 'lxml', parse_only=SoupStrainer('div', class_='seen-collection'))
table = soup.find('table', class_='chart full-width')
# print(table)

body = table.find('tbody')
rows = body.find_all('tr')
print(type(rows))


try:
    with open('data250', 'w') as f:
        f.write(str(body))
except IOError as err:
    print('Error : ' + str(err))

exit()

