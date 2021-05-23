from app import csrf
from app.integrations.flux_api import Organisation
from app.organisation import organisation
from app.organisation.forms import OrganisationForm
from flask import flash, redirect, render_template, request, url_for


@organisation.route("/", methods=["GET", "POST"])
def list():
    """Get a list of Organisations."""
    name_query = request.args.get("name", type=str)

    if name_query:
        organisations = Organisation().list(name=name_query)
    else:
        organisations = Organisation().list()

    return render_template(
        "list_organisations.html",
        title="Organisations",
        organisations=organisations,
    )


@organisation.route("/new", methods=["GET", "POST"])
def create():
    """Create a new Organisation."""
    form = OrganisationForm()

    if form.validate_on_submit():
        new_organisation = Organisation().create(name=form.name.data, domain=form.domain.data)
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for(
                    "organisation.view",
                    organisation_id=new_organisation["id"],
                ),
                new_organisation["name"],
            ),
            "success",
        )
        return redirect(url_for("organisation.list"))

    return render_template(
        "create_organisation.html",
        title="Create a new organisation",
        form=form,
    )


@organisation.route("/<uuid:organisation_id>", methods=["GET"])
def view(organisation_id):
    """View a Organisation with a specific ID."""
    organisation = Organisation().get(organisation_id=organisation_id)

    return render_template(
        "view_organisation.html",
        title=organisation["name"],
        organisation=organisation,
    )


@organisation.route("/<uuid:organisation_id>/edit", methods=["GET", "POST"])
def edit(organisation_id):
    """Edit a Organisation with a specific ID."""
    form = OrganisationForm()

    if form.validate_on_submit():
        changed_organisation = Organisation().edit(
            organisation_id=organisation_id,
            name=form.name.data,
            domain=form.domain.data,
        )
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for("organisation.view", organisation_id=organisation_id),
                changed_organisation["name"],
            ),
            "success",
        )
        return redirect(url_for("organisation.list"))
    elif request.method == "GET":
        organisation = Organisation().get(organisation_id=organisation_id)
        form.name.data = organisation["name"]
        form.domain.data = organisation["domain"]

    return render_template(
        "edit_organisation.html",
        title="Edit {}".format(organisation["name"]),
        form=form,
        organisation=organisation,
    )


@organisation.route("/<uuid:organisation_id>/delete", methods=["GET", "POST"])
@csrf.exempt
def delete(organisation_id):
    """Delete a Organisation with a specific ID."""
    organisation = Organisation().get(organisation_id=organisation_id)

    if request.method == "GET":
        return render_template(
            "delete_organisation.html",
            title="Delete {}".format(organisation["name"]),
            organisation=organisation,
        )
    elif request.method == "POST":
        Organisation().delete(organisation_id=organisation_id)
        flash("{} has been deleted.".format(organisation["name"]), "success")
        return redirect(url_for("organisation.list"))
