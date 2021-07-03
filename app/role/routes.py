import csv
from io import StringIO

from app import csrf
from app.integrations.flux_api import Grade, Organisation, Practice, Role
from app.role import role
from app.role.forms import RoleFilterForm, RoleForm
from flask import Response, flash, redirect, render_template, request, url_for


@role.route(
    "/<uuid:organisation_id>/roles/",
    methods=["GET", "POST"],
)
def list(organisation_id):
    """Get a list of Roles."""
    organisation = Organisation().get(organisation_id=organisation_id)
    grades = Grade().list(organisation_id=organisation_id)
    practices = Practice().list(organisation_id=organisation_id)

    form = RoleFilterForm()
    form.grade.choices += [(grade["id"], grade["name"]) for grade in grades]
    form.practice.choices += [(practice["id"], practice["name"]) for practice in practices]

    filters = {}
    if request.args.get("title"):
        filters["title"] = request.args.get("title", type=str)
        form.title.data = filters["title"]

    if request.args.get("grade"):
        filters["grade_id"] = request.args.get("grade", type=str)
        form.grade.data = filters["grade_id"]

    if request.args.get("practice"):
        filters["practice_id"] = request.args.get("practice", type=str)
        form.practice.data = filters["practice_id"]

    roles = Role().list(organisation_id=organisation_id, filters=filters)

    return render_template(
        "list_roles.html",
        title="Roles",
        organisation=organisation,
        roles=roles,
        form=form,
    )


@role.route(
    "/<uuid:organisation_id>/roles/new",
    methods=["GET", "POST"],
)
def create(organisation_id):
    """Create a new Role."""
    form = RoleForm()
    organisation = Organisation().get(organisation_id=organisation_id)

    grades = Grade().list(organisation_id=organisation_id)
    if grades:
        form.grade.choices = [(grade["id"], grade["name"]) for grade in grades]

    practices = Practice().list(organisation_id=organisation_id)
    if practices:
        form.practice.choices += [(practice["id"], practice["name"]) for practice in practices]

    if form.validate_on_submit():
        new_role = Role().create(
            title=form.title.data,
            grade_id=form.grade.data,
            practice_id=form.practice.data,
            organisation_id=organisation_id,
        )
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for(
                    "role.view",
                    organisation_id=organisation_id,
                    role_id=new_role["id"],
                ),
                new_role["title"],
            ),
            "success",
        )
        return redirect(url_for("role.list", organisation_id=organisation_id))

    return render_template(
        "create_role.html",
        title="Create a new role",
        organisation=organisation,
        form=form,
    )


@role.route(
    "/<uuid:organisation_id>/roles/<uuid:role_id>",
    methods=["GET"],
)
def view(organisation_id, role_id):
    """View a specific Role in an Role."""
    role = Role().get(organisation_id=organisation_id, role_id=role_id)

    return render_template(
        "view_role.html",
        title=role["title"],
        role=role,
    )


@role.route(
    "/<uuid:organisation_id>/roles/<uuid:role_id>/edit",
    methods=["GET", "POST"],
)
def edit(organisation_id, role_id):
    """Edit a specific Role in an Role."""
    role = Role().get(organisation_id=organisation_id, role_id=role_id)
    form = RoleForm()
    grades = Grade().list(organisation_id=organisation_id)
    if grades:
        form.grade.choices = [(grade["id"], grade["name"]) for grade in grades]

    practices = Practice().list(organisation_id=organisation_id)
    if practices:
        form.practice.choices += [(practice["id"], practice["name"]) for practice in practices]

    if form.validate_on_submit():
        changed_role = Role().edit(
            role_id=role_id,
            title=form.title.data,
            grade_id=form.grade.data,
            practice_id=form.practice.data,
            organisation_id=organisation_id,
        )
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for(
                    "role.view",
                    organisation_id=organisation_id,
                    role_id=role_id,
                ),
                changed_role["title"],
            ),
            "success",
        )
        return redirect(url_for("role.list", organisation_id=organisation_id))
    elif request.method == "GET":
        form.title.data = role["title"]
        form.grade.data = role["grade"]["id"]
        if role["practice"]:
            form.practice.data = role["practice"]["id"]

    return render_template(
        "edit_role.html",
        title=f"Edit {role['title']}",
        form=form,
        role=role,
    )


@role.route(
    "/<uuid:organisation_id>/roles/<uuid:role_id>/delete",
    methods=["GET", "POST"],
)
@csrf.exempt
def delete(organisation_id, role_id):
    """Delete a specific Role in an Role."""
    role = Role().get(organisation_id=organisation_id, role_id=role_id)

    if request.method == "GET":
        return render_template(
            "delete_role.html",
            title=f"Delete {role['title']}",
            role=role,
        )
    elif request.method == "POST":
        Role().delete(organisation_id=organisation_id, role_id=role_id)
        flash("{} has been deleted.".format(role["title"]), "success")
        return redirect(url_for("role.list", organisation_id=organisation_id))


@role.route("/<uuid:organisation_id>/roles/download", methods=["GET"])
def download(organisation_id):
    """Download a list of Roles in an Organisation in CSV format."""
    roles = Role().list(organisation_id=organisation_id)

    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(("TITLE", "GRADE", "PRACTICE"))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each item
        for role in roles:
            w.writerow(
                (
                    role["title"],
                    role["grade"]["name"],
                    role["practice"]["name"] if role["practice"] else None,
                )
            )
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    response = Response(generate(), mimetype="text/csv")
    response.headers.set("Content-Disposition", "attachment", filename="roles.csv")
    return response
