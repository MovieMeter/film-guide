
# Get IMDB, RT, Meta and Audience scores for a movie by name.
# Run this module from the terminal to enter a movie name and see its score.


from ratings.get_score import get_score
from google import search
import requests
from bs4 import BeautifulSoup

movie = input('Enter movie name : ')
imdb_url = rotten_url = None

# print('imdb:')
count = 0
for url in search(movie+' imdb', stop=1):
    imdb_url = url
    break

# print('IMDb URL : ' + imdb_url)


# print('\nRT:')
for url in search(movie+' rottentomatoes', stop=1):
    rotten_url = url
    break
#
print('IMDb URL : ' + str(imdb_url))
print('RT URL : ' + str(rotten_url))
# exit()

movie_score = get_score(imdb_url, rotten_url)
print('Film Score : ' + str(movie_score))

