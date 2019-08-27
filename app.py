from flask import Flask, render_template, url_for, request
import redis

import route
import models

app = Flask(__name__)

app.config['FLASK_HOST_PORT'] = '5000'

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', timeline=models.Tweet.simple_sort())


if __name__ == '__main__':
    app = route.init_app(app)
    app = models.init_app(app)
    app.run(debug=True)
