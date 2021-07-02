from flask_wtf import FlaskForm
from wtforms.fields import RadioField, SelectField, StringField
from wtforms.validators import InputRequired, Optional


class ProjectForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(message="Enter a name")])
    manager = SelectField(
        "Project manager",
        validators=[Optional()],
        choices=[("", "None")],
    )
    programme = SelectField(
        "Programme",
        validators=[Optional()],
        choices=[("", "None")],
    )
    status = RadioField(
        "Status",
        validators=[InputRequired(message="Select a status")],
        choices=[("active", "Active"), ("paused", "Paused"), ("closed", "Closed")],
    )


class ProjectFilterForm(FlaskForm):
    name = StringField("Name", validators=[Optional()])
    manager = RadioField("Project manager", validators=[Optional()], choices=[("", "All")], default="")
    programme = RadioField("Programme", validators=[Optional()], choices=[("", "All")], default="")
    status = RadioField(
        "Status",
        validators=[Optional()],
        choices=[
            ("", "All"),
            ("active", "Active"),
            ("paused", "Paused"),
            ("closed", "Closed"),
        ],
        default="",
    )
