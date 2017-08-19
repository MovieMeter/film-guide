from database.home_database import HomeDB


db = HomeDB()
genres = db.conn.execute ('''SELECT genre from genre_table
                                          where id = ?''', (10,)).fetchall()

print(genres)