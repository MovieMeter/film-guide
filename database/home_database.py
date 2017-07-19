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
            return None
        else:
            self.c.execute('''select MAX(id) as max_id from movie_table''')
            max_id = self.c.fetchone()
            # print(max_id)
            if max_id[0] is None:
                new_id = 1
            else:
                new_id = max_id[0] + 1
            print('new_id = ' + str(new_id))
            self.c.execute('''insert into movie_table values(?,?,?)''',
                           (new_id, film_obj.name, film_obj.year))
            # self.conn.commit()
            if len(film_obj.genre) > 0:
                for item in film_obj.genre:
                    self.c.execute('''insert into genre_table values(?,?)''', (new_id, item))
            # self.conn.commit()
        return new_id

    # get row_id from the main table, by name + year
    def get_row_id(self, film_obj):
        self.c.execute('select id from movie_table where movie_table.name = ? AND movie_table.year = ?',
                       (film_obj.name, film_obj.year))

        row_id = self.c.fetchone()
        print(row_id)
        if row_id is None:
            return None
        return row_id[0]

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
        # self.conn.commit()

    # Add ratings for the movie, including the database score
    def set_ratings(self, film_obj):
        row_id = self.get_row_id(film_obj)
        print('row_id = ' + str(row_id))
        if row_id is None:
            print('Error(set_ratings()). Movie not found.')
            return

        self.c.execute('select COUNT(id) from rating_table where rating_table.id = ?',
                       (row_id, ))
        count = self.c.fetchone()[0]
        print(count)
        # exit()
        if count > 0:
            print('Ratings already present. Call update function')
            return
        else:
            movie_score = film_obj.score
            r_tuple = (row_id,
                     film_obj.ratings['imdb'],
                     film_obj.ratings['meta'],
                     film_obj.ratings['rt'],
                     film_obj.ratings['audience'],
                     movie_score)

            self.c.execute('insert into rating_table values(?,?,?,?,?,?)', r_tuple)
        # self.conn.commit()

    # view table (duh)
    def view_movies(self):
        # Right now this just prints the tuples. Formatting will be added later.
        cursor = self.c.execute('select * from movie_table')
        for row in cursor:
            print(row)

    def view_genres(self):
        # Tuples only.
        cursor = self.c.execute('select * from genre_table')
        for row in cursor:
            print(row)

    def view_ratings(self):
        # Tuples only.
        cursor = self.c.execute('select * from rating_table')
        for row in cursor:
            print(row)
