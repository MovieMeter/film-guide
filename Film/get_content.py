from google import search
import requests
from bs4 import BeautifulSoup, SoupStrainer
from fake_useragent import UserAgent
from ratings.calculate import score
import sys


# Assign imdb and rt links to the film object.
def load_url(film):
    name = film.name
    year = film.year
    imdb_url = rotten_url = None
    for url in search(name + ' ' + str(year) + ' imdb', stop=1):
        imdb_url = url
        break
    film.imdb_link = imdb_url

    for url in search(name + ' ' + str(year) + ' rottentomatoes', stop=1):
        rotten_url = url
        break
    film.rotten_link = rotten_url


# Load the imdb ratings, meta score, and the genres to the movie by referencing its IMDb page.
# Also set the name and year properly, just in case.
def imdb_meta(film):
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}
    url = film.imdb_link
    # url = 'http://www.imdb.com/title/tt1375666/'
    fd = open('log_file', 'a')

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, 'lxml', parse_only=SoupStrainer('div', id='pagecontent'))
    try:
        rating = soup.find('span', itemprop='ratingValue')
        # print(rating.text)

        meta_score = soup.find('div', class_='metacriticScore')
        # print(meta_score.text)

        imdb_rating = int(float(rating.text) * 10)
        if meta_score is not None:
            meta_rating = int(meta_score.text)
        else:
            meta_rating = 0
        film.ratings['imdb'] = imdb_rating
        film.ratings['meta'] = meta_rating
    except:
        print(sys.exc_info()[0])
        film.ratings['imdb'] = -400
        film.ratings['meta'] = -400
        fd.write(str(sys.exc_info()[0]) + '\n')

    fd.close()
    # return imdb_rating, meta_rating
    # Getting genres.
    subtext = soup.find('div', class_='subtext')
    # print(subtext)
    # print(type(subtext))
    genre_list = subtext.find_all('a')
    # print(genre_list)
    # genres = []
    count = 1
    length = len(genre_list)
    for item in genre_list:
        if count == length:
            break
        film.genre.append(item.text)
        count = count + 1

    # Setting name and year field properly
    title_bar = soup.find('div', class_='title_wrapper')

    name_tag = title_bar.find('h1')
    st1 = name_tag.text
    pos = st1.index('(')
    name = st1[:pos].strip()
    year = int(st1[pos + 1:pos + 5].strip())
    film.name = name
    film.year = year


# Load the rotten and audience ratings for the film object.
def rotten(film):
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}
    url = film.rotten_link
    r = requests.get(url, headers=headers)
    fd = open('log_file', 'a')
    soup = BeautifulSoup(r.content, 'lxml', parse_only=SoupStrainer('div', class_='body_main container'))

    main = soup.find('div', id='mainColumn')
    # print(main)
    # exit()
    try:
        score_panel = main.find('div', id='scorePanel')

        link = score_panel.find('a', id='tomato_meter_link')
        span = link.find('span', class_='meter-value superPageFontColor')
        rating = span.text[:len(span.text)-1]

        # print(rating)

        audience = soup.find('div', class_='audience-score meter')
        value = audience.find('div', class_='meter-value')
        # print(value.text[:len(value.text)-1])
        temp1 = value.text.strip()
        audience_score = temp1[:len(temp1) - 1]
        meter_score = int(rating)
        a_score = int(audience_score)
        film.ratings['rt'] = meter_score
        film.ratings['audience'] = a_score
    except:
        print(sys.exc_info()[0])
        film.ratings['rt'] = -400
        film.ratings['audience'] = -400
        fd.write(str(sys.exc_info()[0]) + '\n')
    # return meter_score, a_score
    fd.close()


# Load the movie score based on the ratings.
def get_score(film):
    film_score = score(film.ratings['imdb'],
                       film.ratings['meta'],
                       film.ratings['rt'],
                       film.ratings['audience'])
    film.score = film_score


def add_details(film):
    load_url(film)
    imdb_meta(film)
    rotten(film)
    get_score(film)
    # return film

