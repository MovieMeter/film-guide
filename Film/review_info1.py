from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import sys


def get_info(movie):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    # movie = input('Enter movie? ')
    base = "https://www.google.co.in/search?"
    movie_imdb = movie+" movie imdb"
    params = {'q': movie_imdb,'oq':movie_imdb}
    r3 = requests.get(base,params=params, headers=headers)
    soup3=BeautifulSoup(r3.content, 'lxml')
    tag3=soup3.find('div', class_='rc').a['href']

    r4=requests.get(tag3,headers=headers)
    soup4=BeautifulSoup(r4.content, 'lxml')
    name_year=soup4.find('h1', itemprop="name").get_text().strip()
    name=name_year[0:len(name_year)-6]
    # print(str(name))
    year=name_year[len(name_year)-5:len(name_year)-1]
    # print(year)
    rate=soup4.find('div', class_="imdbRating").div.get_text().strip()
    # print(rate)
    director=soup4.find('span', itemprop="director").get_text().strip()
    # print(director)
    meta=soup4.find('div', class_="titleReviewBarItem")
    if meta!=None:
        meta=meta.div.get_text().strip()
        # print("meta score:" +str(meta))
    # else:
        # print("meta score not available")
    genre_list=soup4.find_all('span', class_="itemprop", itemprop="genre")
    for item in genre_list:
        item=item.get_text().strip()
        # print(item)



    index=0
    actor=list()
    character=list()
    for item in soup4.find_all('span',class_="itemprop"):
        actor.append(item.get_text())
        index+=1
        if index>=9:
            break
    index=0
    for item in soup4.find_all('td', class_="character"):
        character.append(item.get_text())
        index+=1
        if index>=9:
            break
    # for index in range(0, len(actor)):
        # print(str(actor[index])+'\t'+str(character[index]))
        #fp.write('\n'+actor[index]+'\t'+ character[index]+'\n')
    #fp.close()

    movie_rotten=movie+" movie rottentomatoes"
    params={'q':movie_rotten,'oq':movie_rotten}
    r5=requests.get(base,params=params,headers=headers)
    soup5=BeautifulSoup(r5.content,'lxml')
    tag4=soup5.find('div', class_='rc').a['href']
    r6=requests.get(tag4, headers=headers)
    #print r6.url
    soup6=BeautifulSoup(r6.content, 'lxml')
    score=soup6.find('div', class_='critic-score meter')
    # print(score.get_text().strip())

    score_val = score.text.strip()
    params = [name, year, rate, director, score_val]
    return params


def hello():
    print('Hello')




