# Use this to search for movies from the internet.
# Gives exact title matches for movie names, along with the year for the movie.
# Use this name to search movie in the database.

import requests
from bs4 import BeautifulSoup, SoupStrainer


# Takes a movie name as input and returns the list of imdb titles matching that name.
def show_search(movie):
    base = 'https://www.google.co.in/search?'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

    term = movie + ' imdb'
    params = {
        'q': term,
        'oq': term
    }

    r = requests.get(base, params=params, headers=headers)
    print(r.url)
    soup = BeautifulSoup(r.content, 'lxml', parse_only=SoupStrainer('div', id='rcnt'))
    search_list = soup.find_all('div', class_='rc', limit=6)
    movie_list = []
    for item in search_list:
        mov = item.find('h3', class_='r')
        # print(mov)
        s1 = mov.text.strip()[:-7].strip()

        s2 = str(mov.a['href'])
        if s2[20:25] == 'title' and len(s2) < 40:
            print(s1)
            year = s1[-5:-1]
            bracket_index = s1.rfind('(')
            name = s1[:bracket_index].strip()
            # print('Name : ' + name + ', Year = ' + year)
            # print(s2)
            title = [name, year, s2]
            movie_list.append(title)
        # print(mov.text.strip() + ', ' + str(mov.a['href'][20:25]))
    # print(search_list)
    for item in movie_list:
        print(item)

    return movie_list

# name = input('Enter movie : ')
# show_search(name)
