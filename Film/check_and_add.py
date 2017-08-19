# This module checks for a movie inside the home database.
# If not present, it adds it to the database.
# This is to be called anytime the app comes across a movie.

# import requests
from database.home_database import HomeDB
from Film.get_content import add_details, load_url, imdb_meta, rotten, get_score
from Film.film import Film
from Film import review_info1
# from bs4 import BeautifulSoup
import sys


# my_db = HomeDB()


def check(film):
    db = HomeDB()
    is_present = db.check_entry(film)
    db.conn.close()
    if is_present is True:
        # Movie already present.
        return True
    return False


def add_new(film):
    db = HomeDB()
    db.add_entry_to_main(film)
    db.set_ratings(film)
    row_id = db.get_row_id(film)
    db.add_director(film, row_id)
    db.add_links(film, row_id)
    db.conn.commit()
    db.conn.close()


# def add(film):
#     # verify(film)
#     rotten(film)
#     get_score(film)
#     db = HomeDB()
#     db.add_entry_to_main(film)
#     db.set_ratings(film)
#     db.conn.commit()
#     db.conn.close()

#
# def verify(film):
#     load_url(film)
#     imdb_meta(film)
def load_info(film):
    print('Loading film information.')
    db = HomeDB()
    row_id = db.get_row_id(film)

    if film.imdb_link is None:
        im = db.conn.execute('''SELECT imdb_link from link_table
                                  where id = ?''', (row_id,)).fetchone()[0]
        film.imdb_link = im
        print('Loaded imdb link.')
    if film.rotten_link is None:
        # rot = db.conn.execute('''SELECT rotten_link from links_table where name =''')
        rot = db.conn.execute('''SELECT rotten_link from link_table 
                                  where id = ?''', (row_id,)).fetchone()[0]
        film.rotten_link = rot
        print('Loaded rt.')
    if film.score is None:
        film.score = db.conn.execute('''SELECT ROUND(score) from rating_table WHERE
                                          id = ?''', (row_id,)).fetchone()[0]
        print('Loaded score.')
    if len(film.ratings) < 4:
        rating_row = db.conn.execute('''SELECT imdb, meta, rotten, audience from rating_table
                                        where id = ?''', (row_id,)).fetchone()
        film.ratings['imdb'] = rating_row[0]
        film.ratings['meta'] = rating_row[1]
        film.ratings['rt'] = rating_row[2]
        film.ratings['audience'] = rating_row[3]
        print('Loaded ratings..')
    if len(film.genre) == 0:
        genres = db.conn.execute('''SELECT genre from genre_table
                                      where id = ?''', (row_id,)).fetchall()
        for tup in genres:
            film.genre.append(tup[0])
        print('Loaded genres.')
    if film.director is None:
        film.director = db.conn.execute('''SELECT director from director_table
                                  where id = ?''', (row_id,)).fetchone()[0]
        print('Loaded director.')
    db.conn.close()
    # except:
    #     print(sys.exc_info()[0])
    #     print('Error in loading data.')
    #     db.conn.close()
    #     return


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
        if check(film) is not True:
            print('Movie Not present in database. Adding..')
            review_info1.imdb_content(film)
            print(film.genre)
            review_info1.get_rotten_link(film)
            review_info1.rotten(film)
            review_info1.get_score(film)
            add_new(film)
            print('Added.')
            return
        else:
            db = HomeDB()
            row_id = db.get_row_id(film)
            # These snippets could be written as separate functions in order to improve functionality.
            # Checking for links
            if db.check_links(film) is None:
                print('Links not present in the database. Adding.')
                if film.imdb_link is None:
                    review_info1.load_imdb_url(film)
                review_info1.get_rotten_link(film)
                db.add_links(film, row_id)
                db.conn.commit()
                print('Added new links for the movie.')
            else:
                print('Links present in the database.')
            # Checking for director
            if db.check_director(film) is None:
                print('Director not present. Adding.. ')
                review_info1.get_director(film)
                db.add_director(film, row_id)
                db.conn.commit()
            db.conn.close()
            load_info(film)
            print('Done verifying..')
            return
        # verify(film)
        # print('Checking database for the movie..')
        # if check(film) is True:
        #     print('Movie present in database.')
        #     return
        # else:
        #     print('Not found, adding to database.. Please Wait.')
        #     add(film)
        #     print('Done.')

