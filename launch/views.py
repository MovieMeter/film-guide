from launch.launcher import app
from database.home_database import HomeDB
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from Film.review_info1 import get_info
from Film.check_and_add import check_movie


@app.route('/top')
def show_movies():
    db = HomeDB()
    m_list = db.conn.execute('select * from movie_table where id <= 20').fetchall()
    db.conn.close()
    return render_template('result.html', m_list=m_list)


@app.route('/')
def home():
    return 'Home Page'



@app.route('/search', methods=['GET', 'POST'])
def search():
    error = None
    if request.method == 'POST':
        # Get data from form
        # Call Script review_info1.py
        movie = request.form['title']
        params = get_info(movie)
        # More stuff
        print('Checking movie in database, wait')
        check_movie(name=params[0], year=params[1])
        session['params'] = params
        return redirect(url_for('result'))

    return render_template('search.html', error=error)


@app.route('/result')
def result():
    params = session['params']
    # return params[0]
    return render_template('movie.html', params=params)

