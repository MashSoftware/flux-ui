from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField
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


class GradeForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[InputRequired(message="Enter a name")],
        description="The name of the grade",
    )


class PracticeForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[InputRequired(message="Enter a name")],
        description="The name of the practice",
    )
    head = StringField(
        "Head of practice",
        validators=[InputRequired(message="Enter a head of practice")],
        description="The name of the head of practice",
    )


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
