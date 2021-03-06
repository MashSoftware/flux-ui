import csv
from io import StringIO

from app import csrf
from app.integrations.flux_api import Organisation, Person, Programme, Project
from app.project import project
from app.project.forms import ProjectFilterForm, ProjectForm
from flask import Response, flash, redirect, render_template, request, url_for


@project.route("/<uuid:organisation_id>/projects/", methods=["GET", "POST"])
@csrf.exempt
def list(organisation_id):
    """Get a list of Projects in an Organisation."""
    organisation = Organisation().get(organisation_id=organisation_id)
    managers = Project().managers(organisation_id=organisation_id)
    programmes = Programme().list(organisation_id=organisation_id)

    form = ProjectFilterForm()
    form.manager.choices += [(manager["id"], manager["name"]) for manager in managers]
    form.programme.choices += [(programme["id"], programme["name"]) for programme in programmes]

    filters = {}
    if request.args.get("name"):
        filters["name"] = request.args.get("name", type=str)
        form.name.data = filters["name"]

    if request.args.get("manager"):
        filters["manager_id"] = request.args.get("manager", type=str)
        form.manager.data = filters["manager_id"]

    if request.args.get("programme"):
        filters["programme_id"] = request.args.get("programme", type=str)
        form.programme.data = filters["programme_id"]

    if request.args.get("status"):
        filters["status"] = request.args.get("status", type=str)
        form.status.data = filters["status"]

    projects = Project().list(organisation_id=organisation_id, filters=filters)

    return render_template(
        "list_projects.html",
        title="Projects",
        organisation=organisation,
        projects=projects,
        form=form,
    )


@project.route("/<uuid:organisation_id>/projects/new", methods=["GET", "POST"])
def create(organisation_id):
    """Create a new Project in an Organisation."""
    form = ProjectForm()
    organisation = Organisation().get(organisation_id=organisation_id)
    people = Person().list(organisation_id=organisation_id)
    if people:
        form.manager.choices += [(manager["id"], manager["name"]) for manager in people]
    programmes = Programme().list(organisation_id=organisation_id)
    if people:
        form.programme.choices += [(programme["id"], programme["name"]) for programme in programmes]

    if form.validate_on_submit():
        new_project = Project().create(
            organisation_id=organisation_id,
            name=form.name.data,
            manager_id=form.manager.data,
            programme_id=form.programme.data,
            status=form.status.data,
        )
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for(
                    "project.view",
                    organisation_id=organisation_id,
                    project_id=new_project["id"],
                ),
                new_project["name"],
            ),
            "success",
        )
        return redirect(url_for("project.list", organisation_id=organisation_id))

    return render_template(
        "create_project.html",
        title="Create a new project",
        organisation=organisation,
        form=form,
    )


@project.route("/<uuid:organisation_id>/projects/<uuid:project_id>", methods=["GET"])
def view(organisation_id, project_id):
    """View a specific Project in an Organisation."""
    project = Project().get(organisation_id=organisation_id, project_id=project_id)

    return render_template(
        "view_project.html",
        title=project["name"],
        project=project,
    )


@project.route(
    "/<uuid:organisation_id>/projects/<uuid:project_id>/edit",
    methods=["GET", "POST"],
)
def edit(organisation_id, project_id):
    """Edit a specific Project in an Organisation."""
    project = Project().get(organisation_id=organisation_id, project_id=project_id)
    people = Person().list(organisation_id=organisation_id)
    programmes = Programme().list(organisation_id=organisation_id)
    form = ProjectForm()
    if people:
        form.manager.choices += [(manager["id"], manager["name"]) for manager in people]
    if people:
        form.programme.choices += [(programme["id"], programme["name"]) for programme in programmes]

    if form.validate_on_submit():
        changed_project = Project().edit(
            organisation_id=organisation_id,
            project_id=project_id,
            name=form.name.data,
            manager_id=form.manager.data,
            programme_id=form.programme.data,
            status=form.status.data,
        )
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for(
                    "project.view",
                    organisation_id=organisation_id,
                    project_id=project_id,
                ),
                changed_project["name"],
            ),
            "success",
        )
        return redirect(url_for("project.list", organisation_id=organisation_id))
    elif request.method == "GET":
        form.name.data = project["name"]
        if project["manager"]:
            form.manager.data = project["manager"]["id"]
        if project["programme"]:
            form.programme.data = project["programme"]["id"]
        form.status.data = project["status"]

    return render_template(
        "update_project.html",
        title=f"Edit {project['name']}",
        form=form,
        project=project,
    )


@project.route(
    "/<uuid:organisation_id>/projects/<uuid:project_id>/delete",
    methods=["GET", "POST"],
)
@csrf.exempt
def delete(organisation_id, project_id):
    """Delete a specific Project in an Organisation."""
    project = Project().get(organisation_id=organisation_id, project_id=project_id)

    if request.method == "GET":
        return render_template(
            "delete_project.html",
            title=f"Delete {project['name']}",
            project=project,
        )
    elif request.method == "POST":
        Project().delete(organisation_id=organisation_id, project_id=project_id)
        flash("{} has been deleted.".format(project["name"]), "success")
        return redirect(url_for("project.list", organisation_id=organisation_id))


@project.route("/<uuid:organisation_id>/projects/download", methods=["GET"])
def download(organisation_id):
    """Download a list of Projects in an Organisation in CSV format."""
    projects = Project().list(organisation_id=organisation_id)

    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(
            (
                "NAME",
                "MANAGER",
                "PROGRAMME",
                "STATUS",
            )
        )
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each item
        for project in projects:
            w.writerow(
                (
                    project["name"],
                    project["manager"]["name"] if project["manager"] else None,
                    project["programme"]["name"] if project["programme"] else None,
                    project["status"],
                )
            )
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    response = Response(generate(), mimetype="text/csv")
    response.headers.set("Content-Disposition", "attachment", filename="projects.csv")
    return response
