from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash, get_flashed_messages
from flask.ext.wtf import Form
from wtforms.fields import StringField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url


class BookmarkForm(Form):
    url = URLField('url', validators=[DataRequired(), url()])
    description = StringField('description')

    def validate(self):
        if not self.url.data.startswith("http://") or \
                self.url.data.startswith("https://"):
            self.url.data = "http://" + self.url.data
        if not Form.validate(self):
            return False
        if not self.description.data:
            self.description.data = self.url.data

        return True


app = Flask(__name__)
app.config["SECRET_KEY"] = b'Cg\xa1W\x86\x0c\x1bl\xb1]\xbd\xaf\x89\xd7\xc06\xfa\xd8 \xfd\x8e\x975C'

bookmarks = []


def store_bookmark(url, description):
    bookmarks.append(dict(
        url=url,
        description=description,
        user="Muhannad",
        date=datetime.utcnow()
    ))


def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', new_bookmarks=new_bookmarks(5))


@app.route('/add', methods=['GET', 'POST'])
def addBookmark():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        store_bookmark(url, description)
        flash('Stored url: "{}"'.format(url))
        flash('Description: "{}"'.format(description))
        return redirect(url_for('index'))
    return render_template("add.html", form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
