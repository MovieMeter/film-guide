import sqlite3
from Film.film import Film


class HomeDB:

    def __init__(self):
        self.conn = sqlite3.connect('/home/mehulagarwal/PycharmProjects/film-guide/database/movie_db.db')
        self.c = self.conn.cursor()

    def initialize_tables(self):
        try:
            with open('../schema/movie_table.sql', 'r') as fd:
                sql = fd.read()
                self.conn.executescript(sql)
        except IOError as err:
            print('Error : ' + str(err))

    # check if a particular movie is present in the database. Matches the movie name and year to confirm.
    def check_entry(self, film_obj):
        self.c.execute('''select * from movie_table where movie_table.name = ? COLLATE NOCASE
                            AND movie_table.year = ? COLLATE NOCASE''',
                       (film_obj.name, film_obj.year))
        row = self.c.fetchone()
        if row is None:
            return False
        else:
            return True

    # Adding entries to the database tables. Go about adding entries in all 3 tables to update.
    def add_entry_to_main(self, film_obj):
        if self.check_entry(film_obj):
            print('Movie already exists in database')
            return
        else:
            self.c.execute('''select MAX(id) as max_id from movie_tale''')
            max_id = self.c.fetchone()
            new_id = max_id + 1
            self.c.execute('''insert into movie_table values(?,?,?)''',
                           (new_id, film_obj.name, film_obj.year))

            if len(film_obj.genre) > 0:
                for item in film_obj.genre:
                    self.c.execute('''insert into genre_table values(?,?)''', (new_id, item))

        return

    # get row_id from the main table, by name + year
    def get_row_id(self, film_obj):
        self.c.execute('select id from movie_table where movie_table.name = ? AND movie_table.year = ?',
                       (film_obj.name, film_obj.year))

        row_id = self.c.fetchone()
        return row_id

    # Add genres for the movie
    def set_genre(self, film_obj):
        row_id = self.get_row_id(film_obj)
        if row_id is None:
            print('Error(set_genre()). Movie not found.')
            return

        self.c.execute('select COUNT(id) from genre_table where genre_table.id = ?',
                       (row_id, ))
        count = self.c.fetchone()
        if count is not None:
            print('Genres for this movie are already added. Sorry. Modification not available right now')
            return
        else:
            for item in film_obj.genre:
                self.c.execute('insert into genre_table values(?,?)',
                               (row_id, item))

    # Add ratings for the movie, including the database score
    def set_ratings(self, film_obj):
        row_id = self.get_row_id(film_obj)
        if row_id is None:
            print('Error(set_ratings()). Movie not found.')
            return

        self.c.execute('select COUNT(id) from rating_table where rating_table.id = ?',
                       (row_id, ))

        if self.c.fetchone() is not None:
            print('Ratings already present. Call update function')
            return
        else:
            movie_score = film_obj.score
            tuple = (row_id,
                     film_obj['imdb'],
                     film_obj['meta'],
                     film_obj['rotten'],
                     film_obj['audience'],
                     movie_score)

            self.c.execute('insert into rating_table values(?,?,?,?,?,?)', tuple)
