from flask_wtf import FlaskForm
from wtforms.fields import StringField, SelectField
from wtforms.validators import InputRequired, Optional


class ProgrammeForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[InputRequired(message="Enter a name")],
        description="The name of the programme",
    )
    manager = SelectField(
        "Programme manager",
        validators=[Optional()],
        choices=[("", "None")],
    )
