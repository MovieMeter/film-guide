from imdb.db250 import DataBase
from database.home_database import HomeDB
import time
from Film.film import Film
from Film.get_content import load_url, imdb_meta, rotten, get_score
import sys


# The IMDb 250 database
db = DataBase()

# The home database
home_db = HomeDB()
row_id = 6
print('Loading movies from IMDb 250 to Database..')
print('Beginning..')
try:
    while row_id <= 250:
        print('Adding ' + str(row_id) + '..')
        row = db.get_row_by_id(row_id)
        row_id = row_id + 1
        film = Film()
        film.name = row[1]
        film.year = row[2]
        load_url(film)
        imdb_meta(film)
        rotten(film)
        get_score(film)
        home_db.add_entry_to_main(film)
        home_db.set_ratings(film)

        del film
        print('Added ')
        time.sleep(3)
        if row_id % 10 == 0:
            home_db.conn.commit()

except:
    print(sys.exc_info()[0])


print('Added movies to database.')
home_db.conn.commit()
home_db.conn.close()
db.conn.close()
# print(row[2])
