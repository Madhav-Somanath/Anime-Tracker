from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddAnimeForm(FlaskForm):
    anime_name = StringField("Anime name:", validators=[DataRequired()])
    current_episode = StringField("Current Episode:", validators=[DataRequired()])
    total_episodes = StringField("Total Episodes:", validators=[DataRequired()])
    submit = SubmitField("Submit")
