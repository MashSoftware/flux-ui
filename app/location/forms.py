from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import InputRequired


class LocationForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[InputRequired(message="Enter a name")],
        description="The name of the location",
    )
    address = StringField(
        "Address",
        validators=[InputRequired(message="Enter an address")],
    )
