from database.home_database import HomeDB
from Film.film import Film
from Film.get_content import load_url, imdb_meta, rotten, get_score
import sys


db = HomeDB()

db.initialize_tables()

# choice = input('Press 1 to add an entry : ')
# if int(choice) == 1:
#     film = Film()
#     name = input('Enter name : ')
#     year = input('Year : ')
#     film.name = name
#     film.year = year
#     load_url(film)
#     imdb_meta(film)
#     rotten(film)
#     get_score(film)
#
#     db.add_entry_to_main(film)
#     db.set_ratings(film)
# # db.view_movies()
print('Welcome to film-guide!')
print('''Menu :
1)  Search for a movie.
2)  View current popular movies.
3)  Have a look at top movies.
4)  Critic favourites.
5)  View movies by genre.
10) Exit\n''')
choice = -99
while choice != 10:
    try:
        choice = int(input('Enter choice : '))
        if choice == 1:
            # Auro module
            continue
        elif choice == 2:
            pop_list = db.conn.execute('''select * from popular_now''').fetchall()
            print('Current Popular Movies : ')
            for item in pop_list:
                print(str(item[0]) + ') ' + item[1] + ' (' + str(item[2]) + ')')
            continue
        elif choice == 3:
            lim = int(input('Enter number of movies to display. '))
            count = 0
            m_list = db.conn.execute('''select movie_table.id, movie_table.name, movie_table.year, rating_table.score from movie_table, rating_table where movie_table.id = rating_table.id order by rating_table.score desc;
    ''').fetchall()
            print('Top Movies : ')
            for item in m_list:
                count = count + 1
                if count > lim:
                    break
                # print(item)
                print(str(item[0]) + ') ' + str(item[1]) + ' (' + str(item[2]) + '). Score : ' + str(item[3]))
            continue
        elif choice == 4:
            # Auro Table
            continue
        elif choice == 5:
            gc = input('Enter genre : ').strip()
            count = 0
            m_list = db.conn.execute('''select movie_table.id, 
                                          movie_table.name, 
                                          movie_table.year, 
                                          rating_table.score 
                                          from movie_table, rating_table, genre_table 
                                          where movie_table.id = rating_table.id 
                                          and movie_table.id = genre_table.id 
                                          and genre_table.genre = ? COLLATE NOCASE 
                                          order by rating_table.score desc;''', (gc,))
            for item in m_list:
                print(str(item[0]) + ') ' + item[1] + ' (' + str(item[2]) + '). Score : ' + str(item[3]))
            continue
        elif choice != 10:
            print('Enter a valid choice please.')
        else:
            print('Exiting App..')
    except:
        print(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])

db.conn.commit()
db.conn.close()
