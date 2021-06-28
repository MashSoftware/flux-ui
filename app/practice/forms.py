from flask_wtf import FlaskForm
from wtforms.fields import StringField, SelectField
from wtforms.validators import InputRequired, Optional


class PracticeForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[InputRequired(message="Enter a name")],
        description="The name of the practice",
    )
    head = SelectField(
        "Head of practice",
        validators=[Optional()],
        choices=[("", "None")],
    )
    cost_centre = StringField(
        "Cost centre",
        validators=[Optional()],
    )
