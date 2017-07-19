from bs4 import BeautifulSoup
import requests
from database.home_database import HomeDB
from Film.film import Film
from fake_useragent import UserAgent
from google import search
import sys
from ratings.calculate import score
import time
import os


db = HomeDB()
ua = UserAgent()
headers = {'User-Agent': ua.chrome}
movies = db.conn.execute('select * from movie_table')
# print(movie_list.fetchall())
movie_list = movies.fetchall()
count = 0
rotten_url = None
fp = open('conversion_log.txt', 'a')
fp.write('\nBeginning Log Record.. \n')
for item in movie_list:
    try:
        count = count + 1
        # if count > 5:
        #     break
        # time.sleep(3)
        # if count > 3:
        #     break
        id = item[0]
        if count != 335:
            continue
        fp.write('Count ' + str(count) + '... id : ' + str(id) + '.. ')
        name = item[1]
        year = item[2]
        print('Name : ' + name)
        print('Year : ' + str(year))

        for url in search(name + ' ' + str(year) + ' rottentomatoes', stop=1):
            rotten_url = url
            break
        # rotten_link = rotten_url
        print(rotten_url)
        r = requests.get(rotten_url, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        cr = soup.find('div', id='scoreStats')
        rf = cr.find('div', class_='superPageFontColor')
        rating = rf.text
        # print(rating)
        # except:
        #     print(sys.exc_info()[0])
        print('New ratings .. ')
        pos = rating.index(':')
        avg = rating[pos+1:].strip()
        pos = avg.index('/')
        rt1 = int(float(avg[:pos]) * 10)
        print(rt1)
        # avg = avg.strip()
        cr = soup.find('div', class_='audience-info hidden-xs superPageFontColor')
        rf = cr.find('div')
        # print(rf.text)
        rating = rf.text
        # print(rating)

        pos = rating.index(':')
        avg = rating[pos + 1:].strip()
        pos = avg.index('/')
        rt2 = int(float(avg[:pos]) * 20)
        print(rt2)
        r_row = db.conn.execute('select * from rating_table where id = ?', (id,)).fetchone()
        imdb = r_row[1]
        meta = r_row[2]
        if rt1 == r_row[3] and rt2 == r_row[4]:
            fp.write('Up to date.\n')
            fp.flush()
            continue
        # print(imdb, meta)
        new_score = score(imdb, meta, rt1, rt2)
        db.conn.execute('''update rating_table
                            set rotten = ?, audience = ?, score = ?
                            where id = ?''', (rt1, rt2, new_score, id))
        db.conn.commit()
        fp.write('ok\n')
        fp.flush()
        # os.fsync(fp)
    except:
        print('Error(convert.py) : ' + str(sys.exc_info()[0]))
        fp.write('Error : ' + str(sys.exc_info()[0]) + '\n')


fp.close()
db.conn.close()
