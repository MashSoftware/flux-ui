import csv
from io import StringIO

from app import csrf
from app.integrations.flux_api import Organisation, Person, Practice
from app.practice import practice
from app.practice.forms import PracticeForm
from flask import Response, flash, redirect, render_template, request, url_for


@practice.route(
    "/<uuid:organisation_id>/practices/",
    methods=["GET", "POST"],
)
def list(organisation_id):
    """Get a list of Practices in an Organisation."""
    name_query = request.args.get("name", type=str)
    organisation = Organisation().get(organisation_id)

    if name_query:
        practices = Practice().list(organisation_id=organisation_id, name=name_query)
    else:
        practices = Practice().list(organisation_id=organisation_id)

    return render_template(
        "list_practices.html",
        title="Practices",
        organisation=organisation,
        practices=practices,
    )


@practice.route(
    "/<uuid:organisation_id>/practices/new",
    methods=["GET", "POST"],
)
def create(organisation_id):
    """Create a new Practice in an Organisation."""
    form = PracticeForm()
    organisation = Organisation().get(organisation_id=organisation_id)
    people = Person().list(organisation_id=organisation_id)
    if people:
        form.head.choices += [(person["id"], person["name"]) for person in people]

    if form.validate_on_submit():
        new_practice = Practice().create(organisation_id=organisation_id, name=form.name.data, head_id=form.head.data)
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for(
                    "practice.view",
                    organisation_id=organisation_id,
                    practice_id=new_practice["id"],
                ),
                new_practice["name"],
            ),
            "success",
        )
        return redirect(url_for("practice.list", organisation_id=organisation_id))

    return render_template(
        "create_practice.html",
        title="Create a new practice",
        organisation=organisation,
        form=form,
    )


@practice.route(
    "/<uuid:organisation_id>/practices/<uuid:practice_id>",
    methods=["GET"],
)
def view(organisation_id, practice_id):
    """View a specific Practice in an Organisation."""
    practice = Practice().get(organisation_id=organisation_id, practice_id=practice_id)

    return render_template(
        "view_practice.html",
        title=practice["name"],
        practice=practice,
    )


@practice.route(
    "/<uuid:organisation_id>/practices/<uuid:practice_id>/edit",
    methods=["GET", "POST"],
)
def edit(organisation_id, practice_id):
    """Edit a specific Practice in an Organisation."""
    practice = Practice().get(organisation_id=organisation_id, practice_id=practice_id)
    people = Person().list(organisation_id=organisation_id)
    form = PracticeForm()
    if people:
        form.head.choices += [(person["id"], person["name"]) for person in people]

    if form.validate_on_submit():
        changed_practice = Practice().edit(
            organisation_id=organisation_id,
            practice_id=practice_id,
            name=form.name.data,
            head_id=form.head.data,
        )
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for(
                    "practice.view",
                    organisation_id=organisation_id,
                    practice_id=practice_id,
                ),
                changed_practice["name"],
            ),
            "success",
        )
        return redirect(url_for("practice.list", organisation_id=organisation_id))
    elif request.method == "GET":
        form.name.data = practice["name"]
        if practice["head"]:
            form.head.data = practice["head"]["id"]

    return render_template(
        "edit_practice.html",
        title="Edit {}".format(practice["name"]),
        form=form,
        practice=practice,
    )


@practice.route(
    "/<uuid:organisation_id>/practices/<uuid:practice_id>/delete",
    methods=["GET", "POST"],
)
@csrf.exempt
def delete(organisation_id, practice_id):
    """Delete a specific Practice in an Organisation."""
    practice = Practice().get(organisation_id=organisation_id, practice_id=practice_id)

    if request.method == "GET":
        return render_template(
            "delete_practice.html",
            title="Delete {}".format(practice["name"]),
            practice=practice,
        )
    elif request.method == "POST":
        Practice().delete(organisation_id=organisation_id, practice_id=practice_id)
        flash("{} has been deleted.".format(practice["name"]), "success")
        return redirect(url_for("practice.list", organisation_id=organisation_id))


@practice.route("/<uuid:organisation_id>/practices/download", methods=["GET"])
def download(organisation_id):
    """Download a list of Practices in an Organisation in CSV format."""
    practices = Practice().list(organisation_id=organisation_id)

    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(("name", "head"))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each item
        for practice in practices:
            w.writerow(
                (
                    practice["name"],
                    practice["head"]["name"] if practice["head"] else None,
                )
            )
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    response = Response(generate(), mimetype="text/csv")
    response.headers.set("Content-Disposition", "attachment", filename="practices.csv")
    return response
