from app import csrf
from app.integrations.flux_api import FluxAPI
from app.organisation import bp
from app.organisation.forms import OrganisationForm, ProgrammeForm
from flask import flash, redirect, render_template, request, url_for


@bp.route("/", methods=["GET", "POST"])
def list_organisations():
    """Get a list of Organisations."""
    flux_api = FluxAPI()
    name_query = request.args.get("name", type=str)

    if name_query:
        organisations = flux_api.list_organisations(name=name_query)
    else:
        organisations = flux_api.list_organisations()

    return render_template(
        "organisation/list_organisations.html",
        title="Organisations",
        organisations=organisations,
    )


@bp.route("/new", methods=["GET", "POST"])
def create_organisation():
    """Create a new Organisation."""
    flux_api = FluxAPI()
    form = OrganisationForm()

    if form.validate_on_submit():
        new_organisation = flux_api.create_organisation(name=form.name.data, domain=form.domain.data)
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for("organisation.view_organisation", organisation_id=new_organisation["id"]),
                new_organisation["name"],
            ),
            "success",
        )
        return redirect(url_for("organisation.list_organisations"))

    return render_template(
        "organisation/create_organisation.html",
        title="Create a new organisation",
        form=form,
    )


@bp.route("/<uuid:organisation_id>", methods=["GET"])
def view_organisation(organisation_id):
    """View a Organisation with a specific ID."""
    flux_api = FluxAPI()
    organisation = flux_api.get_organisation(organisation_id)

    return render_template(
        "organisation/view_organisation.html",
        title=organisation["name"],
        organisation=organisation,
    )


@bp.route("/<uuid:organisation_id>/edit", methods=["GET", "POST"])
def edit_organisation(organisation_id):
    """Edit a Organisation with a specific ID."""
    flux_api = FluxAPI()
    organisation = flux_api.get_organisation(organisation_id)
    form = OrganisationForm()

    if form.validate_on_submit():
        changed_organisation = flux_api.edit_organisation(
            organisation_id=organisation_id, name=form.name.data, domain=form.domain.data
        )
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for("organisation.view_organisation", organisation_id=organisation_id),
                changed_organisation["name"],
            ),
            "success",
        )
        return redirect(url_for("organisation.list_organisations"))
    elif request.method == "GET":
        form.name.data = organisation["name"]
        form.domain.data = organisation["domain"]

    return render_template(
        "organisation/update_organisation.html",
        title="Edit {}".format(organisation["name"]),
        form=form,
        organisation=organisation,
    )


@bp.route("/<uuid:organisation_id>/delete", methods=["GET", "POST"])
@csrf.exempt
def delete_organisation(organisation_id):
    """Delete a Organisation with a specific ID."""
    flux_api = FluxAPI()
    organisation = flux_api.get_organisation(organisation_id)

    if request.method == "GET":
        return render_template(
            "organisation/delete_organisation.html",
            title="Delete {}".format(organisation["name"]),
            organisation=organisation,
        )
    elif request.method == "POST":
        flux_api.delete_organisation(organisation_id)
        flash("{} has been deleted.".format(organisation["name"]), "success")
        return redirect(url_for("organisation.list_organisations"))


@bp.route("/<uuid:organisation_id>/programme", methods=["GET", "POST"])
def list_programmes(organisation_id):
    """Get a list of Programmes."""
    flux_api = FluxAPI()
    name_query = request.args.get("name", type=str)
    organisation = flux_api.get_organisation(organisation_id)

    if name_query:
        programmes = flux_api.list_programmes(organisation_id=organisation_id, name=name_query)
    else:
        programmes = flux_api.list_programmes(organisation_id=organisation_id)

    return render_template(
        "programme/list_programmes.html",
        title="Programmes",
        organisation=organisation,
        programmes=programmes,
    )


@bp.route("/<uuid:organisation_id>/programme/new", methods=["GET", "POST"])
def create_programme(organisation_id):
    """Create a new Programme."""
    flux_api = FluxAPI()
    form = ProgrammeForm()
    organisation = flux_api.get_organisation(organisation_id)

    if form.validate_on_submit():
        new_programme = flux_api.create_programme(organisation_id=organisation_id, name=form.name.data)
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for("organisation.view_programme", organisation_id=organisation_id, programme_id=new_programme["id"]),
                new_programme["name"],
            ),
            "success",
        )
        return redirect(url_for("organisation.list_programmes", organisation_id=organisation_id))

    return render_template(
        "programme/create_programme.html",
        title="Create a new programme",
        organisation=organisation,
        form=form,
    )


@bp.route("/<uuid:organisation_id>/programme/<uuid:programme_id>", methods=["GET"])
def view_programme(organisation_id, programme_id):
    """View a specific Programme in an Organisation."""
    flux_api = FluxAPI()
    programme = flux_api.get_programme(organisation_id, programme_id)

    return render_template(
        "programme/view_programme.html",
        title=programme["name"],
        programme=programme,
    )


@bp.route("/<uuid:organisation_id>/programme/<uuid:programme_id>/edit", methods=["GET", "POST"])
def edit_programme(organisation_id, programme_id):
    """Edit a specific Programme in an Organisation."""
    flux_api = FluxAPI()
    programme = flux_api.get_programme(organisation_id, programme_id)
    form = ProgrammeForm()

    if form.validate_on_submit():
        changed_programme = flux_api.edit_programme(
            organisation_id=organisation_id, programme_id=programme_id, name=form.name.data
        )
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for("organisation.view_programme", organisation_id=organisation_id, programme_id=programme_id),
                changed_programme["name"],
            ),
            "success",
        )
        return redirect(url_for("organisation.list_programmes", organisation_id=organisation_id))
    elif request.method == "GET":
        form.name.data = programme["name"]

    return render_template(
        "programme/update_programme.html",
        title="Edit {}".format(programme["name"]),
        form=form,
        programme=programme,
    )


@bp.route("/<uuid:organisation_id>/programme/<uuid:programme_id>/delete", methods=["GET", "POST"])
@csrf.exempt
def delete_programme(organisation_id, programme_id):
    """Delete a specific Programme in an Organisation."""
    flux_api = FluxAPI()
    programme = flux_api.get_programme(organisation_id, programme_id)

    if request.method == "GET":
        return render_template(
            "programme/delete_programme.html",
            title="Delete {}".format(programme["name"]),
            programme=programme,
        )
    elif request.method == "POST":
        flux_api.delete_programme(organisation_id, programme_id)
        flash("{} has been deleted.".format(programme["name"]), "success")
        return redirect(url_for("organisation.list_programmes", organisation_id=organisation_id))