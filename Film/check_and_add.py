# This module checks for a movie inside the home database.
# If not present, it adds it to the database.
# This is to be called anytime the app comes across a movie.

# import requests
from database.home_database import HomeDB
from Film.get_content import add_details, load_url, imdb_meta, rotten, get_score
from Film.film import Film
# from bs4 import BeautifulSoup


def check(film):
    db = HomeDB()
    is_present = db.check_entry(film)
    db.conn.close()
    if is_present is True:
        # Movie already present.
        return True
    return False


def add(film):
    rotten(film)
    get_score(film)
    db = HomeDB()
    db.add_entry_to_main(film)
    db.set_ratings(film)
    db.conn.commit()
    db.conn.close()


def verify(film):
    load_url(film)
    imdb_meta(film)


def check_movie(film=None, name=None, year=None):
    # name = film.name
    # year = film.year
    if name is not None:
        f = Film()
        f.name = name
        f.year = year
        check_movie(film=f)
    else:
        print('Validating movie information..')
        verify(film)
        print('Checking database for the movie..')
        if check(film) is True:
            print('Movie present in database.')
            return
        else:
            print('Not found, adding to database.. Please Wait.')
            add(film)
            print('Done.')



