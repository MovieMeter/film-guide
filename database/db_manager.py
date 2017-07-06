from database.home_database import HomeDB
from Film.film import Film

db = HomeDB()

db.initialize_tables()

film = Film()
film.name = 'The Dark Knight'
film.year = 2008

db.add_entry_to_main(film)
db.view_movies()

db.conn.commit()
db.conn.close()
