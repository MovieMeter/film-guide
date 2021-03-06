from bs4 import BeautifulSoup, SoupStrainer
from fake_useragent import UserAgent
import requests
import sys
# from Film.mov import get_review
from Film.film import Film
from database.home_database import HomeDB
from ratings.calculate import score
from googleS.gsearch import search


def get_score(film):
    film.score = round(score(film.ratings['imdb'],
                       film.ratings['meta'],
                       film.ratings['rt'],
                       film.ratings['audience']), 2)


def load_imdb_url(film):
    # For existing movies (ofcourse :/)
    imdb_url = search(film.name + ' ' + str(film.year) + ' imdb')
    film.imdb_link = imdb_url


def imdb_content(film):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    r4 = requests.get(film.imdb_link, headers=headers)
    soup4 = BeautifulSoup(r4.content, 'lxml')
    # IMDb_rating
    rate = soup4.find('div', class_="imdbRating").div.get_text().strip()
    r2 = int(float(rate[:rate.index('/')]) * 10)
    print(r2)
    # Director
    director = soup4.find('span', itemprop="director").get_text().strip()
    film.director = director
    film.ratings['imdb'] = r2
    # Meta_Score
    meta = soup4.find('div', class_="titleReviewBarItem")
    if meta is not None:
        #     meta = str(meta.div.get_text().strip())
        # film.ratings['meta'] = soup4.find('div', class_="titleReviewBarItem")
        film.ratings['meta'] = int(str(meta.div.get_text().strip()))
    else:
        film.ratings['meta'] = 0
    # Genres
    genres = []
    genre_list = soup4.find_all('span', class_="itemprop", itemprop="genre")
    for item in genre_list:
        item = item.get_text().strip()
        # print(item)
        genres.append(item)
    film.genre = genres
    # try:
    #     summary = soup4.find('div', class_='summary_text', itemprop='description').text
    # except:
    #     summary = None
    # film.summary = summary


def get_director(film):
    # For cases of existing movies..
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    r4 = requests.get(film.imdb_link, headers=headers)
    soup4 = BeautifulSoup(r4.content, 'lxml')
    director = soup4.find('span', itemprop="director").get_text().strip()
    film.director = director


def get_cast(film):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    r4 = requests.get (film.imdb_link, headers=headers)
    soup4 = BeautifulSoup(r4.content, 'lxml')
    index = 0
    actor = list()
    character = list()
    for item in soup4.find_all('span', class_="itemprop"):
        actor.append(item.get_text())
        index += 1
        if index >= 9:
            break
    index = 0
    for item in soup4.find_all('td', class_="character"):
        character.append(item.get_text())
        index = index + 1
        if index >= 9:
            break
    return actor, character


def get_rotten_link(film):
    base = "https://www.google.co.in/search?"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    movie_rotten = film.name + " " + str(film.year) + " movie rottentomatoes"
    params = {'q': movie_rotten, 'oq': movie_rotten}
    r5 = requests.get(base, params=params, headers=headers)
    soup5 = BeautifulSoup(r5.content, 'lxml')
    tag4 = soup5.find('div', class_='rc').a['href']
    film.rotten_link = tag4


def rotten(film):
    # ua = UserAgent()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    url = film.rotten_link
    r = requests.get(url, headers=headers)
    # fd = open('log_file', 'a')
    soup = BeautifulSoup(r.content, 'lxml', parse_only=SoupStrainer('div', class_='body_main container'))

    # main = soup.find('div', id='mainColumn')
    # print(main)
    # exit()
    try:
        cr = soup.find('div', id='scoreStats')
        rf = cr.find('div', class_='superPageFontColor')
        rating = rf.text
        print(rating)
        # except:
        #     print(sys.exc_info()[0])
        pos = rating.index(':')
        avg = rating[pos + 1:].strip()
        pos = avg.index('/')
        meter_score = int(float(avg[:pos]) * 10)
        # print()
        # avg = avg.strip()
        cr = soup.find('div', class_='audience-info hidden-xs superPageFontColor')
        rf = cr.find('div')
        # print(rf.text)
        rating = rf.text
        print(rating)

        pos = rating.index(':')
        avg = rating[pos + 1:].strip()
        pos = avg.index('/')
        a_score = int(float(avg[:pos]) * 20)
        # print(rt2)
        film.ratings['rt'] = int(meter_score)
        film.ratings['audience'] = int(a_score)
    except:
        print(sys.exc_info()[0])
        film.ratings['rt'] = -400
        film.ratings['audience'] = -400
        # fd.write(str(sys.exc_info()[0]) + '\n')
    # return meter_score, a_score
    # fd.close()


def get_info(film):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    # movie = input('Enter movie? ')
    base = "https://www.google.co.in/search?"
    movie = film.name
    year = film.year
    imdb_link = film.imdb_link
    # db = HomeDB()
    # if db.check_entry(film) is True:
    movie_imdb = movie+" movie imdb"
    params = {'q': movie_imdb, 'oq': movie_imdb}
    r3 = requests.get(base, params=params, headers=headers)
    soup3 = BeautifulSoup(r3.content, 'lxml')
    tag3 = soup3.find('div', class_='rc').a['href']

    # tag3 is imdb_link

    r4 = requests.get(tag3, headers=headers)
    soup4 = BeautifulSoup(r4.content, 'lxml')
    name_year = soup4.find('h1', itemprop="name").get_text().strip()
    name = name_year[0:len(name_year)-6]
    # print(str(name))
    year = name_year[len(name_year)-5:len(name_year)-1]
    # print(year)
    rate = soup4.find('div', class_="imdbRating").div.get_text().strip()
    # print(rate)
    director = soup4.find('span', itemprop="director").get_text().strip()
    # print(director)
    meta = soup4.find('div', class_="titleReviewBarItem")
    # print('Tag Found!')
    if meta is not None:
        meta = str(meta.div.get_text().strip())
        # print("meta score:" +str(meta))
    # else:
        # print("meta score not available")
    genres = []
    genre_list = soup4.find_all('span', class_="itemprop", itemprop="genre")
    for item in genre_list:
        item = item.get_text().strip()
        # print(item)
        genres.append(item)

    index = 0
    actor = list()
    character = list()
    for item in soup4.find_all('span', class_="itemprop"):
        actor.append(item.get_text())
        index += 1
        if index >= 9:
            break
    index = 0
    for item in soup4.find_all('td', class_="character"):
        character.append(item.get_text())
        index = index + 1
        if index >= 9:
            break
    # for index in range(0, len(actor)):
        # print(str(actor[index])+'\t'+str(character[index]))
        #fp.write('\n'+actor[index]+'\t'+ character[index]+'\n')
    #fp.close()
    try:
        summary = soup4.find('div', class_='summary_text', itemprop='description').text
    except:
        summary = None
    movie_rotten=movie+" movie rottentomatoes"
    params={'q':movie_rotten,'oq':movie_rotten}
    r5=requests.get(base,params=params,headers=headers)
    print(r5.url)
    soup5=BeautifulSoup(r5.content,'lxml')
    tag4=soup5.find('div', class_='rc').a['href']
    r6=requests.get(tag4, headers=headers)
    print(tag4)
    # print r6.url
    soup6 = BeautifulSoup(r6.content, 'lxml')
    score = soup6.find('div', class_='critic-score meter').get_text().strip()
    # print(score.get_text().strip())
    # review = get_review(name)
    # score_val = score.text.strip()
    # link = poster(name, year)
    params2 = {
        'name': name,
        'year': year,
        'rotten': score,
        'imdb': rate,
        'meta': meta,
        'director': director,
        'genres': genres,
        # 'link': link,
        'summary': summary
    }
    # params = [name, year, rate, score, meta, director, genres, link, summary]
    return params2


def hello():
    print('Hello')




