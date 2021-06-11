from flask_wtf import FlaskForm
from wtforms.fields import StringField, SelectField
from wtforms.validators import InputRequired, Optional


class ProjectForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[InputRequired(message="Enter a name")],
        description="The name of the project",
    )
    manager = SelectField(
        "Project manager",
        validators=[Optional()],
        choices=[("", "None")],
    )
    programme = SelectField(
        "Programme",
        validators=[Optional()],
        description="The programme to which this project belongs",
    )
