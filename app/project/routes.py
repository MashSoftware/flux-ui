from app import csrf
from app.integrations.flux_api import Organisation, Person, Programme, Project
from app.project import project
from app.project.forms import ProjectForm
from flask import flash, redirect, render_template, request, url_for


@project.route("/<uuid:organisation_id>/projects/", methods=["GET", "POST"])
def list(organisation_id):
    """Get a list of Projects in an Organisation."""
    name_query = request.args.get("name", type=str)
    organisation = Organisation().get(organisation_id=organisation_id)

    if name_query:
        projects = Project().list(organisation_id=organisation_id, name=name_query)
    else:
        projects = Project().list(organisation_id=organisation_id)

    return render_template(
        "list_projects.html",
        title="Projects",
        organisation=organisation,
        projects=projects,
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

    return render_template(
        "update_project.html",
        title="Edit {}".format(project["name"]),
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
            title="Delete {}".format(project["name"]),
            project=project,
        )
    elif request.method == "POST":
        Project().delete(organisation_id=organisation_id, project_id=project_id)
        flash("{} has been deleted.".format(project["name"]), "success")
        return redirect(url_for("project.list", organisation_id=organisation_id))
