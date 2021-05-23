from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import InputRequired


class ProgrammeForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[InputRequired(message="Enter a name")],
        description="The name of the programme",
    )
    programme_manager = StringField(
        "Programme manager",
        validators=[InputRequired(message="Enter a programme manager")],
        description="The name of the programme manager",
    )
