from bs4 import BeautifulSoup, SoupStrainer
import requests
import urllib.parse
import urllib.request
from fake_useragent import UserAgent
from google import search
ua = UserAgent()
headers = {'User-Agent': ua.chrome}


for url in search('dark knight imdb', stop=5):
    print(url)


# base_url = 'https://www.rottentomatoes.com/search/?'
#
# movie_name = input('Enter movie Name : ').strip()
# movie_name = movie_name.lower()
# data = {
#     'search': movie_name
# }
# query = urllib.parse.urlencode(data)
# # r = requests.get(base_url, {'search': movie_name}, headers=headers)
# r = urllib.request.urlopen(base_url+query)
# print(r.url)
# print(type(r))
# # soup = BeautifulSoup(r.content, 'lxml', parse_only=SoupStrainer('div', class_='col col-left-center col-full-xs'))
# soup = BeautifulSoup(r.read(), 'lxml', parse_only=SoupStrainer('div', id='search-results-root'))
# print(soup)
# m_list = soup.find('ul', class_='results_ul')
# #
# print(m_list)
#
# script = soup.find('script')
# print(type(script))
# print(str(script).strip())
#

