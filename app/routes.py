from flask import Flask, render_template, request, jsonify, redirect, url_for, g
from flask.ext.pymongo import PyMongo
from time import time
from flaskext.markdown import Markdown

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
mongo = PyMongo(app)

Markdown(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/<page_id>')
def view(page_id):
    page = getPageById(page_id)

    return render_template('view.html', page=page)


@app.route('/edit/<page_id>', methods=["GET"])
def retrieve(page_id):
    page = getPageById(page_id)
    return render_template('edit.html', page=page)


@app.route('/edit/<page_id>', methods=["POST"])
def edit(page_id):
    if not page_id:
        return redirect(url_for('new'))
    g.page = {
        'id': page_id,
        'content': request.form['content'].strip()
    }
    updateContent(g.page)
    return jsonify(**request.form)


@app.route('/edit', methods=['POST', 'GET'])
def new():
    id = int(round(time() * 1000))
    if request.method == 'POST':
        updateContent(request.form)
    return redirect(url_for('edit', page_id=id))


def updateContent(page):
    mongo.db.pages.update({'id': page['id']}, {'id': page['id'], 'content': page['content']}, upsert=True)


def getPageById(id):
    return mongo.db.pages.find_one({'id': id})

if __name__ == '__main__':
    app.run(debug=True)
