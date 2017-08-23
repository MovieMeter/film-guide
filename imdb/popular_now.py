from bs4 import BeautifulSoup
import requests
import sys
from fake_useragent import UserAgent
from Film.film import Film
from Film.get_content import imdb_meta, rotten, get_score, load_url, add_details
from database.home_database import HomeDB
import sys
from check_and_add import check_movie
import time


url = 'http://www.imdb.com/chart/moviemeter'
base_url = 'http://www.imdb.com'
ua = UserAgent()
headers = {'User-Agent': ua.chrome}

r = requests.get(url, headers=headers)
count = 0
soup = BeautifulSoup(r.content, 'lxml')
tbody = soup.find('tbody', class_='lister-list')
db = HomeDB()

with open('../schema/popular.sql', 'r') as sq:
    sql = sq.read()
    db.conn.executescript(sql)

# db.conn.close()
# exit()
# db.conn.close()
# exit()
for tr in tbody.find_all('tr'):
    try:
        if count > 20:
            break
        count = count + 1
        ch = tr.find('td', class_='ratingColumn imdbRating')
        t = ch.text.strip()
        print('Tag = ' + str(t))
        print(len(t))
        if len(t) < 1:
            continue
        film = Film()
        td = tr.find('td', class_='titleColumn')
        data = td.find('a')
        # print(data)
        link = data['href']
        # print(link)
        inx = link.index('?')
        film.imdb_link = base_url + link[:inx]
        print(film.imdb_link)

        # print(data)
        # exit()
        print('Movie : ' + str(data.text), end='')
        # continue
        film.name = data.text.strip()
        # next_t = data.next_sibling
        next_t = td.find('span')
        # print(next_t)
        # exit()
        print(', Year : ' + str(next_t.text))
        temp = next_t.text.strip()
        film.year = int(temp[1:5])
        print(film.year)
        # continue
        check_movie(film)
        row_id = db.get_row_id(film)
        # print('printing : ', end='')
        # print(row_id)
        # add_details(film)

        # row_id = db.add_entry_to_main(film)
        # print('ello')
        # db.set_ratings(film)
        # print('there')
        db.conn.execute('''INSERT INTO popular_now VALUES(?,?,?)''', (row_id, film.name, film.year))
        db.conn.commit()
        time.sleep(3)
    except:
        err = sys.exc_info()
        print('Error(popular_now) : ')
        print(str(err[0]))
        print(str(err[1]))
        print(str(err[2]))

# db.conn.commit()
db.conn.close()
