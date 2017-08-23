from launch.launcher import app
from database.home_database import HomeDB
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from Film.review_info1 import get_info
from Film.check_and_add import check_movie
from Film.mov import get_review
from Film.get_poster import poster
from Film.film import Film
import sys
from googleS import gsearch
from Film.search_film import show_search


@app.route('/top')
def show_movies():
    db = HomeDB()
    m_list = db.conn.execute('select * from movie_table where id <= 20').fetchall()
    db.conn.close()
    return render_template('result.html', m_list=m_list)


@app.route('/')
def home():
    db = HomeDB()
    popular_list = []

    count = 0
    movies = db.conn.execute('''SELECT * from popular_now''').fetchall()
    for item in movies:
        movie = [item[0], item[1], item[2]]
        # print(movie)
        posters = db.conn.execute('''SELECT * from poster_table where id = ?''',
                                 (movie[0],)).fetchone()
        if posters is not None:
            poster = posters[1]
        else:
            poster = None
        # print(poster)
        movie.append(poster)
        popular_list.append(movie)
        count = count + 1
        if count == 3:
            break
    print(popular_list)
    # db.conn.close()
        
    return render_template('home.html', popular_list=popular_list)


@app.route('/search', methods=['GET', 'POST'])
def search():
    error = None
    if request.method == 'POST':
        # Get data from form
        # Call Script review_info1.py
        # session.clear()
        movie = request.form['title']

        # Calling the search script
        movie_list = show_search(movie)
        return render_template('movie_list.html', movie_list=movie_list)

    return render_template('search.html', error=error)


@app.route('/get_result')
def get_result():
    print('called')
    movie = request.args.get('name')
    year = request.args.get('year')
    # return 'Name = ' + str(name) + ', Year = ' + str(year)
    film = Film()
    film.name = movie
    film.year = year
    film.imdb_link = request.args.get('link')
    check_movie(film)
    print(str(film.name) + ', ' + str(film.year))
    print(film.ratings)
    params = obj_to_dict(film)
    try:
        params['summary'] = str(get_review(film.name))[:511]
    except:
        params['summary'] = None

    session['params'] = params
    session.modified = True
    # params = get_info(film)
    # # review = get_review(params[0])
    # # print(review)
    # # print(type(params))
    # # params.append(review)
    # # More stuff
    # print('Checking movie in database, wait')
    # check_movie(name=params['name'], year=params['year'])
    # # check_movie(name=params[0], year=params[1])
    # session.pop('params', None)
    # print('no params')
    # session['params'] = params
    # # session.modified = True
    # movie = params['name']
    # # movie = params[0]
    # year = params['year']
    # year = params[1]
    # print(str(movie) + ', ' + str(year))
    # link = poster(movie, year)
    # if review is not None:
    #     session['review'] = review[:511] + '...'
    # session.modified = True
    # print('search : ' + str(session.modified))
    # print(session['review'])
    # print(session)
    return redirect(url_for('result'))


@app.route('/movie/show')
def show_movie():
    film = Film()
    film.name = request.args.get('name')
    film.year = request.args.get('year')
    check_movie(film)
    params = get_info(film)
    # session.clear()
    # check_movie(name=params[0], year=params[1])
    # session.pop('params', None)
    session['params'] = params
    session.modified = True
    # print(session['params'])
    movie = params['name']
    # movie = params[0]
    year = params['year']
    # year = params[1]
    print(str(movie) + ', ' + str(year))
    review = get_review(film.name)
    if review is not None:
        session['review'] = review[:511] + '...'
    session.modified = True
    # print('show_movie : ' + str(session.modified))
    # print(session)
    return redirect(url_for('result'))


@app.route('/result')
def result():
    # print(request.cookies)
    # print(session)
    params = session['params']
    db = HomeDB()
    # print(params[0])
    # print(params[1])
    print(type(params))
    print(params)
    movie = params['name'].strip()
    year = str(params['year']).strip()
    # movie = params[0].strip()
    # year = str(params[1]).strip()
    print(str(movie) + ', ' + str(year))
    # scores = db.conn.execute('''SELECT round(rating_table.score) from rating_table''')
    # score = db.conn.execute('''SELECT round(rating_table.score) from rating_table, movie_table
    #                           where movie_table.id = rating_table.id
    #                           and movie_table.name = ? COLLATE NOCASE
    #                           and movie_table.year = ? COLLATE NOCASE''', (movie, year)).fetchone()[0]
    score = params['score']
    print('Score : ' + str(score))

    movie_id = db.conn.execute('''SELECT movie_table.id from movie_table where
                                  movie_table.name = ? COLLATE NOCASE
                                  and movie_table.year = ? COLLATE NOCASE''',
                               (movie, year)).fetchone()[0]
    comp_year = int(year) - 20

    # Getting poster
    link = poster(params['name'], params['year'], movie_id)
    params['link'] = link
    # Getting recommendations
    temp_list = get_similar(params['genres'], comp_year)
    # temp_list = get_similar(params[6], comp_year)
    recom = []

    for item in temp_list:
        if item != movie_id:
            tup = db.conn.execute('''SELECT movie_table.name, movie_table.year,
                                    round(rating_table.score) from movie_table, rating_table
                                    where movie_table.id = rating_table.id AND 
                                    movie_table.id = ?''', (item,)).fetchone()
            recom.append(tup)
            print(tup)
    print('List gathered : ')
    print(temp_list)
    del temp_list
    db.conn.close()
    # get_similar(params[6])
    # params['score'] = score
    # params.append(score)
    if params['summary'] is None:
        review = 'No summary available'
    else:
        review = params['summary']
    # if 'review' in session:
    #     review = session['review'][:511] + '....'
    # else:
    #     review = 'No summary available.'
    # return params[0]
    # print(review)
    return render_template('movie.html', params=params, review=review, recom=recom)


@app.route('/genre', methods=['GET', 'POST'])
def genre_search():
    error = None
    if request.method == 'POST' or 'genre_name' in request.args:
        # Get genre
        if 'genre_name' in request.args:
            genre = request.args['genre_name']
        else:
            genre = request.form['genre']
        db = HomeDB()
        m_list = db.conn.execute('''SELECT movie_table.id, 
                                            movie_table.name, 
                                            movie_table.year,
                                            ROUND(rating_table.score)
                                             FROM MOVIE_TABLE, GENRE_TABLE, RATING_TABLE
                                             WHERE MOVIE_TABLE.id = GENRE_TABLE.id
                                             AND MOVIE_TABLE.id = RATING_TABLE.id
                                             AND Genre_table.genre = ? COLLATE NOCASE
                                             ORDER BY RATING_TABLE.score DESC''',
                                 (genre,))
        return render_template('view_genre.html', genre=genre, m_list=m_list)
    return render_template('get_genre.html', error=error)


@app.route('/review')
def show_review():

    try:
        params = session['params']
    except:
        print(sys.exc_info()[0])
        # info = ['None', 'None']
    review = get_review(params['name'])
    # review = get_review(params[0])
    if review is None:
        review = 'No review available at the moment, sorry.'
    return render_template('show_review.html', review=review, params=params)


@app.route('/director/<director>')
def show_director(director):
    # url = 'http://www.google.com/search?'
    # params = {
    #     'q': director,
    #     'oq': director
    # }
    # r = requests.get(url, params=params)
    term = str(director) + ' wikipedia'
    url = gsearch.search(term=term)
    return redirect(url)

    # return redirect('http://www.google.com/search?', q='John Glen')


def get_similar(genre_list, comp_year):
    movie_list = []
    db = HomeDB()
    cursors = []
    my_dict = {}
    for item in genre_list:
        g1 = db.conn.execute('''select movie_table.id, round(rating_table.score)
                                  from movie_table, rating_table, genre_table
                                  where movie_table.id = rating_table.id 
                                  and movie_table.year > ?
                                  and movie_table.id = genre_table.id 
                                  and genre_table.genre = ? collate nocase
                                  order by rating_table.score DESC''',
                                 (comp_year, item)).fetchall()
        l1 = list(g1)
        for item in l1:
            if item[0] not in my_dict:
                add_list = [1, item[1]]
                my_dict[item[0]] = add_list
            else:
                # print('Count = ' + str(my_dict[[item[0]]][0]))
                my_dict[item[0]][0] = my_dict[item[0]][0]+1

    # print(my_dict)
    sorted_dict = sorted(my_dict, key=my_dict.__getitem__, reverse=True)
    print('Sorted dictionary : ')
    print(type(sorted_dict))
    return sorted_dict[:8]
    # print(sorted_dict)
    # for item in genre_list:
    #     g1 = db.conn.execute('''select movie_table.id, movie_table.name, movie_table.year, round(rating_table.score)
    #                             from movie_table, rating_table, genre_table
    #                             where movie_table.id = rating_table.id
    #                             and movie_table.id = genre_table.id
    #                             and genre_table.genre = ? collate nocase
    #                             order by rating_table.score DESC''',
    #                          (item,)).fetchall()
    #     l1 = list(g1)
    #     cursors.append(l1)
    # db.conn.close()
    # print(cursors)
    # length = len(cursors)
    # count = 0
    # while(len(movie_list) < 5):
    #     id = cursors[count][0]
    #     for cursor in cursors:
    #         cursor.remove(id)
    #


def obj_to_dict(film):
    params2 = {
        'name': film.name,
        'year': film.year,
        'rotten': film.ratings['rt'],
        'imdb': film.ratings['imdb'],
        'meta': film.ratings['meta'],
        'director': film.director,
        'genres': film.genre,
        'score': film.score
        # 'link': link,
        # 'summary': film.summary
    }
    return params2
