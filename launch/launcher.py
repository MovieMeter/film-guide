from flask import Flask, session

app = Flask(__name__)

from launch import views

if __name__ == '__main__':
    app.run(debug=True)



