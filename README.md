# film-guide
Movie Database. (Getting started. Stay tuned.)


A movie recommendation application, with recommendation for movies based on genres and directors.
The Web Pages working right now include the home page, the search page, movie page and listings.
The movie page has a 'You May Like:' section which contains recommendations gathered from the database.
The home page has a list of currently popular movies, along with database top picks.

Pages render using HTML, CSS and Bootstrap mainly. Jinja2 template rendering has been used.
Some scripting on the back end is populating these movie lists and recommendations, along with the information
for each individual movie like Poster, Director, Casting (to be added), among others.

The database is stored in the 'database' directory.
The Flask application is in the 'launch' directory.
A few movie objects and scraping scripts are in the 'Film' directory.

Run the server by navigating to the root of the repo, and typing :

    export FLASK_APP=try_flask.py
    flask run

The server accepts requests at 

    127.0.0.1:5000
OR
 
    (LAN IP for the server machine):5000
    For testing on a simple LAN connection
Note:

A basic form of multi-threaded support is working (in-built Flask support), not very efficiently though.
The server WILL accept multiple requests at once, but might slow down in some cases.

Dependencies: 
1. python3
2. flask
3. BeautifulSoup
4. reqeusts


To install flask, open a terminal and type:

    pip install flask

requests :

    pip install requests

BeautifulSoup :

    pip install bs4
    

Find out and install python3 for your machine.
It might work on python2 if you modify the print statements, i have not tried it myself.
