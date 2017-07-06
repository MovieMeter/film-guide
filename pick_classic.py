
# Chooses a random movie from the IMDb 250, and displays its score.
# Run this module to get a random movie picked from the IMDb 250.


from imdb.db250 import DataBase
from film_score import get_movie_score
import random


db = DataBase()
row_id = random.randint(1, 250)

row = db.get_row_by_id(row_id)

movie_name = row[1]
print('Recommended movie : ' + movie_name)
movie_score = get_movie_score(movie_name)

