import requests
from bs4 import BeautifulSoup
from database.home_database import HomeDB
import random
import os


def poster(movie=None, year=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
               }

    url = 'http://www.ipecho.net/plain'
    # r = requests.get(url, headers=headers)

    # print(r.text)
    # db = HomeDB()
    # max_id = db.conn.execute('SELECT MAX(id) from movie_table').fetchone()[0]
    # print(max_id)
    # m_id = random.randint(0,max_id)
    # row = None
    # while row is None:
    #     row = db.conn.execute('SELECT name, year from movie_table where id = ?', (m_id,)).fetchone()
    # print(row)
    # db.conn.close()
    # exit()
    # movie = input('Enter movie : ')
    # year = input('Enter year : ')
    # movie = str(row[0])
    # year = str(row[1])
    query = movie + ' ' + year + ' wikipedia'
    params = {
        'q': query,
        'oq': query
    }

    url = 'http://www.google.com/search?'
    r = requests.get(url, headers=headers, params=params)

    print(r.url)
    # print(r.content)
    soup = BeautifulSoup(r.content, 'lxml')
    h3 = soup.find('h3', class_='r')

    a = h3.find('a')
    print(a)
    link = a['href']

    r = requests.get(link, headers=headers)
    print(r.url)

    soup = BeautifulSoup(r.content, 'lxml')
    a = soup.find('a', class_='image')
    ref = 'http://www.wikipedia.org' + a['href']
    print(ref)

    r = requests.get(ref, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    div = soup.find('div', id='file')
    img = div.find('img')
    link = 'http:' + img['src']
    print(link)
    return link
    r = requests.get(link, headers=headers)
    try:
        path = os.path.join(os.getcwd(), 'launch/static/images')
    except:
        path = os.path.dirname(os.path.realpath(__file__))
    image = os.path.join(path, 'image')
    try:
        with open(image, 'wb') as f:
            f.write(r.content)
    except IOError as err:
        print('Error while writing, ' + str(err))

# poster()
#
# url = 'http://www.google.com/search?'
# movie = input('Enter movie : ')
#
#
# movie = movie + ' movie poster'
# params = {
#     'q': movie,
#     'oq': movie
# }
# r = requests.get(url, params=params, headers=headers)
# print(r.url)
#
# soup = BeautifulSoup(r.content, 'lxml')
# image = soup.find('a', class_='bia uh_rl')
# ref = str(image['href']).strip()
#
# link = 'http://www.google.com' + ref
#
# print(link)
#
# r = requests.get(link, headers=headers)
# soup = BeautifulSoup(r.content, 'lxml')
#
# image = soup.find('a', class_='irc_fsl irc_but i3596')
# print(image)
# link = image['href']
# print(link)
