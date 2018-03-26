from flask.ext.wtf import Form
from wtforms.fields import StringField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url


class BookmarkForm(Form):
    url = URLField('url', valdators=[DataRequired(), url()])
    description = StringField('description')
