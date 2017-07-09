from bs4 import BeautifulSoup, NavigableString, Tag
import requests
from fake_useragent import UserAgent
from Film.get_content import imdb_meta, rotten, get_score, load_url
from database.home_database import HomeDB
from Film.film import Film
import sys
import time


def parse(text):
    name_start = text.index('.')
    name_end = text.index('(')
    name = text[name_start+1:name_end].strip()
    year_end = len(text)-1
    year_start = year_end - 4
    year = int(text[year_start:year_end].strip())
    return name, year


# movie_name = input('Enter movie name : ')
url = 'http://www.bbc.com/culture/story/20160819-the-21st-centurys-100-greatest-films'
ua = UserAgent()
headers = {'User-Agent': ua.chrome}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'lxml',)

gl = soup.find('div', class_='body-content')
db = HomeDB()
count = 0
fp = open('logfile', 'w')
film_list = gl.select('p:nth-of-type(7)')[0]
# fp.close()
# db.conn.close()
# exit()
# print(film_list)
for br in film_list.find_all('br'):
    try:
        next_s = br.next_sibling
        count = count + 1
        if count < 87:
            continue
        print('Count : ' + str(count))
        if not(next_s and isinstance(next_s, NavigableString)):
            continue
        next2_s = next_s.next_sibling
        if next2_s and isinstance(next2_s, Tag) and next2_s.name == 'br':
            text = str(next_s).strip()
            if text:
                (name, year) = parse(text)
                print('Adding ' + name + ', ' + str(year) + '..')
                film = Film()
                film.name = name
                film.year = year
                load_url(film)
                imdb_meta(film)
                rotten(film)
                get_score(film)
                db.add_entry_to_main(film)
                db.set_ratings(film)
                if count % 10 == 0:
                    db.conn.commit()
                print('Added.')
                time.sleep(3)
    except:
        print(sys.exc_info()[0])
        # db.conn.commit()
        # db.conn.close()
        fp.write(str(sys.exc_info()[0]) + '\n')

print('Added all movies.')
db.conn.commit()
fp.close()
db.conn.close()
# print(br.next_sibling.strip())


