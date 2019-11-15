import operator

from flask import Flask, jsonify, render_template, request

from scrappers import ThaliaScrapper, WeltbildScrapper

app = Flask(__name__)
app.config.from_object('bookworm.config.DevelopmentConfig')


@app.route('/')
def index():
    if 'q' in request.args:
        q = request.args.get('q')

        ts = ThaliaScrapper(q)
        ws = WeltbildScrapper(q)

        book_list = ts.scrap_the_data() + ws.scrap_the_data()

        book_list.sort(key=operator.itemgetter('price'))

        return render_template('books.html', books=book_list)

    return render_template('index.html')
