from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import InputRequired


class PracticeForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[InputRequired(message="Enter a name")],
        description="The name of the practice",
    )
    head = StringField(
        "Head of practice",
        validators=[InputRequired(message="Enter a head of practice")],
        description="The name of the head of practice",
    )
