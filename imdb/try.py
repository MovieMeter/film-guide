from imdb.db250 import DataBase

db = DataBase()

# Enter function here

# db.drop_table()


db.conn.commit()
db.conn.close()

