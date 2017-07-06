import sqlite3
from Film.film import Film

class HomeDB():

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

    def check_entry(self, film_obj):
        self.c.execute('''select * from movie_table where movie_table.name = ? COLLATE NOCASE
                            AND movie_table.year = ? COLLATE NOCASE''',
                       (film_obj.name, film_obj.year))
        row = self.c.fetchone()
        if row is None:
            return False
        else:
            return True

    def add_entry(self, film_obj):
        if self.check_entry(film_obj):
            print('Movie already exists in database')
            return
        else:
            self.c.execute('''select MAX(id) as max_id from movie_tale''')
            max_id = self.c.fetchone()
            new_id = max_id + 1
            self.c.execute('''insert into movie_table values(?,?,?,?)''',
                           (new_id, film_obj.name, film_obj.year, film_obj.score))

            