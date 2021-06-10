from app import csrf
from app.integrations.flux_api import Organisation, Programme, Person
from app.programme import programme
from app.programme.forms import ProgrammeForm
from flask import flash, redirect, render_template, request, url_for


@programme.route("/<uuid:organisation_id>/programmes/", methods=["GET", "POST"])
def list(organisation_id):
    """Get a list of Programmes in an Organisation."""
    name_query = request.args.get("name", type=str)
    organisation = Organisation().get(organisation_id=organisation_id)

    if name_query:
        programmes = Programme().list(organisation_id=organisation_id, name=name_query)
    else:
        programmes = Programme().list(organisation_id=organisation_id)

    return render_template(
        "list_programmes.html",
        title="Programmes",
        organisation=organisation,
        programmes=programmes,
    )


@programme.route("/<uuid:organisation_id>/programmes/new", methods=["GET", "POST"])
def create(organisation_id):
    """Create a new Programme in an Organisation."""
    form = ProgrammeForm()
    organisation = Organisation().get(organisation_id=organisation_id)
    people = Person().list(organisation_id=organisation_id)
    if people:
        form.manager.choices += [(manager["id"], manager["name"]) for manager in people]

    if form.validate_on_submit():
        new_programme = Programme().create(
            organisation_id=organisation_id,
            name=form.name.data,
            manager_id=form.manager.data,
        )
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for(
                    "programme.view",
                    organisation_id=organisation_id,
                    programme_id=new_programme["id"],
                ),
                new_programme["name"],
            ),
            "success",
        )
        return redirect(url_for("programme.list", organisation_id=organisation_id))

    return render_template(
        "create_programme.html",
        title="Create a new programme",
        organisation=organisation,
        form=form,
    )


@programme.route("/<uuid:organisation_id>/programmes/<uuid:programme_id>", methods=["GET"])
def view(organisation_id, programme_id):
    """View a specific Programme in an Organisation."""
    programme = Programme().get(organisation_id=organisation_id, programme_id=programme_id)

    return render_template(
        "view_programme.html",
        title=programme["name"],
        programme=programme,
    )


@programme.route(
    "/<uuid:organisation_id>/programmes/<uuid:programme_id>/edit",
    methods=["GET", "POST"],
)
def edit(organisation_id, programme_id):
    """Edit a specific Programme in an Organisation."""
    programme = Programme().get(organisation_id=organisation_id, programme_id=programme_id)
    people = Person().list(organisation_id=organisation_id)
    form = ProgrammeForm()
    if people:
        form.manager.choices += [(manager["id"], manager["name"]) for manager in people]

    if form.validate_on_submit():
        changed_programme = Programme().edit(
            organisation_id=organisation_id,
            programme_id=programme_id,
            name=form.name.data,
            manager_id=form.manager.data,
        )
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for(
                    "programme.view",
                    organisation_id=organisation_id,
                    programme_id=programme_id,
                ),
                changed_programme["name"],
            ),
            "success",
        )
        return redirect(url_for("programme.list", organisation_id=organisation_id))
    elif request.method == "GET":
        form.name.data = programme["name"]
        if programme["manager"]:
            form.manager.data = programme["manager"]["id"]

    return render_template(
        "update_programme.html",
        title="Edit {}".format(programme["name"]),
        form=form,
        programme=programme,
    )


@programme.route(
    "/<uuid:organisation_id>/programmes/<uuid:programme_id>/delete",
    methods=["GET", "POST"],
)
@csrf.exempt
def delete(organisation_id, programme_id):
    """Delete a specific Programme in an Organisation."""
    programme = Programme().get(organisation_id=organisation_id, programme_id=programme_id)

    if request.method == "GET":
        return render_template(
            "delete_programme.html",
            title="Delete {}".format(programme["name"]),
            programme=programme,
        )
    elif request.method == "POST":
        Programme().delete(organisation_id=organisation_id, programme_id=programme_id)
        flash("{} has been deleted.".format(programme["name"]), "success")
        return redirect(url_for("programme.list", organisation_id=organisation_id))
