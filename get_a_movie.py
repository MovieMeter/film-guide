# Module for trying out function calls and updating database.


from imdb.db250 import DataBase
import random

db = DataBase()

id = random.randint(1, 250)

row = db.get_row_by_id(id)

print(row)

print(type(row))
print(str(row[1]) + ', Released on : ' + str(row[2]) + ', Rated : ' + str(row[4]))

rows = db.conn.execute('select * from movies where rating > 8.5')
count = 0

for row in rows:
    print(row[1])
    count = count + 1

print(count)

db.close_db()

