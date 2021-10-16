import os
from flask import Flask, render_template, request, send_file, after_this_request
from flashcards import create_csv

app = Flask(__name__)

site_title = "Hebrew Flashcards"


@app.route("/")
def index():
    return render_template('index.html', title=site_title)


@app.route("/about")
def about():
    return render_template('about.html', title=site_title)


@app.route("/flashcards", methods=['POST'])
def flashcards():
    data = request.get_json()
    book, count = data['book'], int(data['count'])
    file = create_csv(book, count)
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
    app.run(debug=True)
