import csv
from io import StringIO

from app import csrf
from app.grade import grade
from app.grade.forms import GradeForm
from app.integrations.flux_api import Grade, Organisation
from flask import Response, flash, redirect, render_template, request, url_for


@grade.route("/<uuid:organisation_id>/grades", methods=["GET", "POST"])
def list(organisation_id):
    """Get a list of Grades in an Organisation."""
    name_query = request.args.get("name", type=str)
    organisation = Organisation().get(organisation_id)

    if name_query:
        grades = Grade().list(organisation_id=organisation_id, name=name_query)
    else:
        grades = Grade().list(organisation_id=organisation_id)

    return render_template(
        "grade/list_grades.html",
        title="Grades",
        organisation=organisation,
        grades=grades,
    )


@grade.route("/<uuid:organisation_id>/grades/new", methods=["GET", "POST"])
def create(organisation_id):
    """Create a new Grade in an Organisation."""
    form = GradeForm()
    organisation = Organisation().get(organisation_id)

    if form.validate_on_submit():
        new_grade = Grade().create(organisation_id=organisation_id, name=form.name.data)
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for(
                    "grade.view",
                    organisation_id=organisation_id,
                    grade_id=new_grade["id"],
                ),
                new_grade["name"],
            ),
            "success",
        )
        return redirect(url_for("grade.list", organisation_id=organisation_id))

    return render_template(
        "grade/create_grade.html",
        title="Create a new grade",
        organisation=organisation,
        form=form,
    )


@grade.route("/<uuid:organisation_id>/grades/<uuid:grade_id>", methods=["GET"])
def view(organisation_id, grade_id):
    """View a specific Grade in an Organisation."""
    grade = Grade().get(organisation_id=organisation_id, grade_id=grade_id)

    return render_template(
        "grade/view_grade.html",
        title=grade["name"],
        grade=grade,
    )


@grade.route(
    "/<uuid:organisation_id>/grades/<uuid:grade_id>/edit",
    methods=["GET", "POST"],
)
def edit(organisation_id, grade_id):
    """Edit a specific Grade in an Organisation."""
    grade = Grade().get(organisation_id=organisation_id, grade_id=grade_id)
    form = GradeForm()

    if form.validate_on_submit():
        changed_grade = Grade().edit(organisation_id=organisation_id, grade_id=grade_id, name=form.name.data)
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for(
                    "grade.view",
                    organisation_id=organisation_id,
                    grade_id=grade_id,
                ),
                changed_grade["name"],
            ),
            "success",
        )
        return redirect(url_for("grade.list", organisation_id=organisation_id))
    elif request.method == "GET":
        form.name.data = grade["name"]

    return render_template(
        "grade/edit_grade.html",
        title="Edit {}".format(grade["name"]),
        form=form,
        grade=grade,
    )


@grade.route(
    "/<uuid:organisation_id>/grades/<uuid:grade_id>/delete",
    methods=["GET", "POST"],
)
@csrf.exempt
def delete(organisation_id, grade_id):
    """Delete a specific Grade in an Organisation."""
    grade = Grade().get(organisation_id=organisation_id, grade_id=grade_id)

    if request.method == "GET":
        return render_template(
            "grade/delete_grade.html",
            title="Delete {}".format(grade["name"]),
            grade=grade,
        )
    elif request.method == "POST":
        Grade().delete(organisation_id=organisation_id, grade_id=grade_id)
        flash("{} has been deleted.".format(grade["name"]), "success")
        return redirect(url_for("grade.list", organisation_id=organisation_id))


@grade.route("/<uuid:organisation_id>/grades/download", methods=["GET"])
def download(organisation_id):
    """Download a list of Grades in an Organisation in CSV format."""
    grades = Grade().list(organisation_id=organisation_id)

    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(("id", "name"))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each item
        for grade in grades:
            w.writerow((grade["id"], grade["name"]))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    response = Response(generate(), mimetype="text/csv")
    response.headers.set("Content-Disposition", "attachment", filename="grades.csv")
    return response
