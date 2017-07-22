# film-guide
Movie Database. (Getting started. Stay tuned.)


Just beginning to add html pages, which are more like terminal print commands at the moment.
Basically, no style added at all.



Run the server by navigating to the root of the repo, and typing :

    export FLASK_APP=try_flask.py
    flask run

The server accepts requests at 

    127.0.0.1:5000
OR
 
    (Your LAN IP for the server machine):5000
    For testing on a simple LAN connection
Note:

A basic form of multi-threaded support is working, not very efficiently though.
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
