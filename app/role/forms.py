from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField
from wtforms.validators import InputRequired, Optional


class RoleForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[InputRequired(message="Enter a title")],
        description="The role or job title",
    )
    grade = SelectField(
        "Grade",
        validators=[InputRequired(message="Select a grade")],
        description="The pay grade of the role",
    )
    practice = SelectField(
        "Practice",
        validators=[Optional()],
        description="The practice to which this role belongs",
        choices=[("", "None")],
    )
