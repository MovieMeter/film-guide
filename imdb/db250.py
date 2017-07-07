# DataBase class, for communicating with the IMDb 250 database.

import sqlite3


class DataBase:

    def __init__(self):
        self.conn = sqlite3.connect('/home/mehulagarwal/PycharmProjects/film-guide/imdb/imdb250.db')
        self.c = self.conn.cursor()

        self.c.execute('''create table if not exists movies (
            id integer primary key autoincrement,
            name text not null,
            year integer not null,
            link text,
            rating real
            )''')

    def add_entry(self, name, year, ref, rating):
        self.c.execute('''insert into movies(name, year, link, rating) values(?,?,?,?)''', (name, year, ref, rating))

    def view_table(self):
        for row in self.c.execute('select * from movies'):
            print(row)

    def del_entry(self, name):
        self.c.execute('delete from movies where name = ?', (name,))

    def drop_table(self):
        self.c.execute('drop table if exists movies')

    def create_table(self):
        self.c.execute('''create table if not exists movies (
                    id integer primary key autoincrement,
                    name text not null,
                    year integer not null,
                    link text,
                    rating real
                    )''')

    def commit_db(self):
        self.conn.commit()

    def close_db(self):
        self.conn.close()

    def get_row_by_id(self, id):
        rows = self.c.execute('select * from movies where id = ?', (id,))
        # if(len(rows) > 1):
        #     return None
        # print(type(rows))

        return rows.fetchone()




