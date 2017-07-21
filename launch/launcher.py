from flask import Flask, session

app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, 'micro_blog.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

from launch import views

if __name__ == '__main__':
    app.run(debug=True)



