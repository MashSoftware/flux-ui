from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField
from wtforms.fields.core import DecimalField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length, NumberRange


class PersonForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[InputRequired(message="Enter a name")],
    )
    email_address = EmailField(
        "Email address",
        validators=[
            InputRequired(message="Enter an email address"),
            Email(granular_message=True, check_deliverability=True),
            Length(max=256, message="Email address must be 256 characters or fewer"),
        ],
    )
    role = SelectField(
        "Role",
        validators=[InputRequired(message="Select a role")],
    )
    employment = RadioField(
        "Employment",
        validators=[InputRequired(message="Select employment")],
        choices=[("permanent", "Permanent"), ("contract", "Contract")],
    )
    full_time_equivalent = DecimalField(
        "Full time equivalent (FTE)",
        validators=[
            InputRequired(message="Enter a full time equivalent"),
            NumberRange(min=0.1, max=1.0),
        ],
    )
    location = SelectField(
        "Location",
        validators=[InputRequired(message="Select a location")],
    )
