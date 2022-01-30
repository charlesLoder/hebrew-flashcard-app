import os
import importlib
from flask import Flask, render_template, request, send_file, after_this_request
from flashcards import create_csv

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

site_title = "Hebrew Flashcards"

f = open('./hebrew-vocab-tools/books.txt', 'r')
books = f.read()
f.close()

lines = books.split("\n")

def getBook(line):
    return line.split(' ')[0]

book_list = list(map(getBook,lines))

@app.route("/")
def index():
    return render_template('index.html', title=site_title, book_list=book_list)


@app.route("/about")
def about():
    return render_template('about.html', title=site_title)


@app.route("/flashcards", methods=['POST'])
def flashcards():
    data = request.get_json()
    book, count = data['book'], int(data['count'])
    chap_start = int(data['chap_start']) if data['chap_start'] else None
    chap_end = int(data['chap_end']) if data['chap_end'] else None
    file = create_csv(book, count, chap_start, chap_end)
    file_path = file.name

    @after_this_request
    def delete_file(response):
        try:
            os.remove(file_path)
        except Exception as error:
            print(error)
        return response

    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(port=port, debug=True)
