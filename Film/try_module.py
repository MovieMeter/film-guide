from Film.film import Film
from Film.get_content import load_url, imdb_meta, rotten, get_score


film = Film()
name = input('Enter name : ')
year = input('Year : ')
film.name = name
film.year = year

# Loading the URLs..
load_url(film)

print('IMDb URL : ' + str(film.imdb_link))
print('RT URL : ' + str(film.rotten_link))


# Loading the content from IMDb..
imdb_meta(film)

print('Genres : ')
print(film.genre)

# Loading content from RT..
rotten(film)

print('Ratings dictionary : ')
print(film.ratings)

# Setting score..
get_score(film)

print('Movie Score : ' + str(film.score))
