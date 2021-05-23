from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import InputRequired


class OrganisationForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            InputRequired(message="Enter a name"),
        ],
        description="The name of the organsation, company or business",
    )
    domain = StringField(
        "Domain",
        validators=[InputRequired(message="Enter a domain")],
        description="The domain of the organisations email addresses, e.g: 'example.com'.",
    )
