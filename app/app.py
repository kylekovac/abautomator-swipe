from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)