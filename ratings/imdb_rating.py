# Gets the IMDb and Metacritic Score from a movie page on IMDb.

from bs4 import BeautifulSoup, SoupStrainer
import requests
from fake_useragent import UserAgent


def imdb_meta(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}

    # url = 'http://www.imdb.com/title/tt1375666/'

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, 'lxml', parse_only=SoupStrainer('div', id='pagecontent'))

    rating = soup.find('span', itemprop='ratingValue')
    # print(rating.text)

    meta_score = soup.find('div', class_='metacriticScore')
    # print(meta_score.text)

    imdb_rating = int(float(rating.text) * 10)
    if meta_score is not None:
        meta_rating = int(meta_score.text)
    else:
        meta_rating = 0
    return imdb_rating, meta_rating


