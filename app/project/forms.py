from flask_wtf import FlaskForm
from wtforms.fields import RadioField, SelectField, StringField
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
        choices=[("", "None")],
    )
    status = RadioField(
        "Status",
        validators=[InputRequired(message="Select a status")],
        description="The current status of the project",
        choices=[("active", "Active"), ("paused", "Paused"), ("closed", "Closed")],
    )


class ProjectFilterForm(FlaskForm):
    name = StringField("Name", validators=[Optional()])
    manager = RadioField("Project manager", choices=[("", "All")])
    programme = RadioField("Programme", choices=[("", "All")])
    status = RadioField(
        "Status",
        choices=[
            ("", "All"),
            ("active", "Active"),
            ("paused", "Paused"),
            ("closed", "Closed"),
        ],
    )
