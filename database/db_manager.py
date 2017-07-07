from database.home_database import HomeDB
from Film.film import Film
from Film.get_content import load_url, imdb_meta, rotten, get_score


db = HomeDB()

db.initialize_tables()

choice = input('Press 1 to add an entry : ')
if int(choice) == 1:
    film = Film()
    name = input('Enter name : ')
    year = input('Year : ')
    film.name = name
    film.year = year
    load_url(film)
    imdb_meta(film)
    rotten(film)
    get_score(film)

    db.add_entry_to_main(film)
    db.set_ratings(film)
db.view_movies()


db.conn.commit()
db.conn.close()
