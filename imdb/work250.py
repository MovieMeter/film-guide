from bs4 import BeautifulSoup, SoupStrainer
import requests
import sqlite3
from imdb.db250 import DataBase


soup = BeautifulSoup(open('data250'), 'lxml')
base_url = 'http://www.imdb.com'

# print(soup)
print(type(soup))

body = soup.find('tbody')
print(type(body))

rows = body.find_all('tr')
print(len(rows))

# row = rows[3]
db = DataBase()
db.drop_table()
db.create_table()

for row in rows:
    # print(row)
    name_col = row.find('td', class_='titleColumn')

    # print(name_col)
    link = name_col.find('a')
    name = link.text
    year_info = name_col.find('span')
    # print(year_info)

    print(year_info.text)
    year = year_info.text[1:5]
    print(year)

    ref = base_url + link['href']
    print(type(ref))
    print(ref)

    rate_col = row.find('td', class_='imdbRating')
    rating = float(rate_col.text)
    print(rating)
    print(name)

    db.add_entry(name, year, ref, rating)

db.conn.commit()
db.conn.close()


