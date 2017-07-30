from launch.launcher import app
from database.home_database import HomeDB
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from Film.review_info1 import get_info
from Film.check_and_add import check_movie
from Film.mov import get_review
# from Film.get_poster import poster
import sys


@app.route('/top')
def show_movies():
    db = HomeDB()
    m_list = db.conn.execute('select * from movie_table where id <= 20').fetchall()
    db.conn.close()
    return render_template('result.html', m_list=m_list)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    error = None
    if request.method == 'POST':
        # Get data from form
        # Call Script review_info1.py
        # session.clear()
        movie = request.form['title']
        params = get_info(movie)
        review = get_review(params[0])
        # print(review)
        # print(type(params))
        # params.append(review)
        # More stuff
        print('Checking movie in database, wait')
        check_movie(name=params[0], year=params[1])
        session.pop('params', None)
        print('no params')
        session['params'] = params
        # session.modified = True
        movie = params[0]
        year = params[1]
        print(str(movie) + ', ' + str(year))
        # link = poster(movie, year)
        if review is not None:
            session['review'] = review[:511] + '...'
        session.modified = True
        # print('search : ' + str(session.modified))
        # print(session['review'])
        # print(session)
        return redirect(url_for('result'))

    return render_template('search.html', error=error)


@app.route('/movie/<name>')
def show_movie(name):
    params = get_info(name)
    # session.clear()
    # check_movie(name=params[0], year=params[1])
    # session.pop('params', None)
    session['params'] = params
    session.modified = True
    # print(session['params'])
    movie = params[0]
    year = params[1]
    print(str(movie) + ', ' + str(year))
    review = get_review(name)
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

    if 'review' in session:
        review = session['review'][:511] + '....'
    else:
        review = 'No summary available.'
    # return params[0]
    # print(review)
    return render_template('movie.html', params=params, review=review)


@app.route('/genre', methods=['GET', 'POST'])
def genre_search():
    error = None
    if request.method == 'POST':
        # Get genre
        genre = request.form['genre']
        db = HomeDB()
        m_list = db.conn.execute('''SELECT movie_table.id, 
                                            movie_table.name, 
                                            movie_table.year,
                                            ROUND(rating_table.score, 2)
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
    review = get_review (params[0])
    if review is None:
        review = 'No review available at the moment, sorry.'
    return render_template('show_review.html', review=review, params=params)


