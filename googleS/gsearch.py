import requests
from bs4 import BeautifulSoup


def search(term):
    # print('IP Test : ')
    # print(requests.get('http://ipecho.net/plain').text)

    # term = input('Enter : ')
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }

    params = {
        'q': term,
        'oq': term
    }

    r = requests.get('https://www.google.co.in/search?', params=params, headers=header)
    # print(r.url)

    soup = BeautifulSoup(r.content, 'lxml')
    with open('output', 'w') as f:
        f.write(str(soup.prettify()))
    # exit()
    # print(soup)
    result_container = soup.find('div', id='res')
    r1 = result_container.find('div', class_='kv')
    cite = r1.find('cite')
    # r1 = result_container.find('div', class_='_NId')
    # print(result_container)
    # a  = result_container.find('a')
    # print(a)
    # print(cite.text)
    link = cite.text
    if link[0] == 'w':
        new_link = 'http://' + link
    else:
        new_link = link
    return new_link
