import operator

from flask import Flask, jsonify, render_template, request

from .scrappers import tahlia_scrapper as ts
from .scrappers import weltbild_scrapper as ws

app = Flask(__name__)
app.config.from_object('bookworm.config.DevelopmentConfig')


@app.route('/')
def index():
    if 'q' in request.args:
        q = request.args.get('q')

        book_list = ts(q) + ws(q)

        book_list.sort(key=operator.itemgetter('price'))

        return render_template('books.html', books=book_list)

    return render_template('index.html')
