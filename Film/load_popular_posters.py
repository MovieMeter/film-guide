from database.home_database import HomeDB
from Film.get_poster import poster


db = HomeDB()
movie_list = db.conn.execute('''SELECT * from popular_now''').fetchall()

for item in movie_list:
    link = poster(item[1], item[2], item[0])
    print(link)

