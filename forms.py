from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    query = StringField('q', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('submit')
