from app import csrf
from app.integrations.flux_api import Organisation, Grade, Programme
from app.organisation import bp
from app.organisation.forms import GradeForm, OrganisationForm, ProgrammeForm
from flask import flash, redirect, render_template, request, url_for


@bp.route("/", methods=["GET", "POST"])
def list_organisations():
    """Get a list of Organisations."""
    name_query = request.args.get("name", type=str)

    if name_query:
        organisations = Organisation().list(name=name_query)
    else:
        organisations = Organisation().list()

    return render_template(
        "organisation/list_organisations.html",
        title="Organisations",
        organisations=organisations,
    )


@bp.route("/new", methods=["GET", "POST"])
def create_organisation():
    """Create a new Organisation."""
    form = OrganisationForm()

    if form.validate_on_submit():
        new_organisation = Organisation().create(name=form.name.data, domain=form.domain.data)
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for(
                    "organisation.view_organisation",
                    organisation_id=new_organisation["id"],
                ),
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
    organisation = Organisation().get(organisation_id)

    return render_template(
        "organisation/view_organisation.html",
        title=organisation["name"],
        organisation=organisation,
    )


@bp.route("/<uuid:organisation_id>/edit", methods=["GET", "POST"])
def edit_organisation(organisation_id):
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
                url_for("organisation.view_organisation", organisation_id=organisation_id),
                changed_organisation["name"],
            ),
            "success",
        )
        return redirect(url_for("organisation.list_organisations"))
    elif request.method == "GET":
        organisation = Organisation().get(organisation_id)
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
    organisation = Organisation().get(organisation_id)

    if request.method == "GET":
        return render_template(
            "organisation/delete_organisation.html",
            title="Delete {}".format(organisation["name"]),
            organisation=organisation,
        )
    elif request.method == "POST":
        Organisation().delete(organisation_id)
        flash("{} has been deleted.".format(organisation["name"]), "success")
        return redirect(url_for("organisation.list_organisations"))


@bp.route("/<uuid:organisation_id>/programme", methods=["GET", "POST"])
def list_programmes(organisation_id):
    """Get a list of Programmes."""
    name_query = request.args.get("name", type=str)
    organisation = Organisation().get(organisation_id)

    if name_query:
        programmes = Programme().list(organisation_id=organisation_id, name=name_query)
    else:
        programmes = Programme().list(organisation_id=organisation_id)

    return render_template(
        "programme/list_programmes.html",
        title="Programmes",
        organisation=organisation,
        programmes=programmes,
    )


@bp.route("/<uuid:organisation_id>/programme/new", methods=["GET", "POST"])
def create_programme(organisation_id):
    """Create a new Programme."""
    form = ProgrammeForm()
    organisation = Organisation().get(organisation_id)

    if form.validate_on_submit():
        new_programme = Programme().create(
            organisation_id=organisation_id,
            name=form.name.data,
            programme_manager=form.programme_manager.data,
        )
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for(
                    "organisation.view_programme",
                    organisation_id=organisation_id,
                    programme_id=new_programme["id"],
                ),
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
    programme = Programme().get(organisation_id, programme_id)

    return render_template(
        "programme/view_programme.html",
        title=programme["name"],
        programme=programme,
    )


@bp.route(
    "/<uuid:organisation_id>/programme/<uuid:programme_id>/edit",
    methods=["GET", "POST"],
)
def edit_programme(organisation_id, programme_id):
    """Edit a specific Programme in an Organisation."""
    form = ProgrammeForm()

    if form.validate_on_submit():
        changed_programme = Programme().edit(
            organisation_id=organisation_id,
            programme_id=programme_id,
            name=form.name.data,
            programme_manager=form.programme_manager.data,
        )
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for(
                    "organisation.view_programme",
                    organisation_id=organisation_id,
                    programme_id=programme_id,
                ),
                changed_programme["name"],
            ),
            "success",
        )
        return redirect(url_for("organisation.list_programmes", organisation_id=organisation_id))
    elif request.method == "GET":
        programme = Programme().get(organisation_id, programme_id)
        form.name.data = programme["name"]
        form.programme_manager.data = programme["programme_manager"]

    return render_template(
        "programme/update_programme.html",
        title="Edit {}".format(programme["name"]),
        form=form,
        programme=programme,
    )


@bp.route(
    "/<uuid:organisation_id>/programme/<uuid:programme_id>/delete",
    methods=["GET", "POST"],
)
@csrf.exempt
def delete_programme(organisation_id, programme_id):
    """Delete a specific Programme in an Organisation."""
    programme = Programme().get(organisation_id, programme_id)

    if request.method == "GET":
        return render_template(
            "programme/delete_programme.html",
            title="Delete {}".format(programme["name"]),
            programme=programme,
        )
    elif request.method == "POST":
        Programme().delete(organisation_id, programme_id)
        flash("{} has been deleted.".format(programme["name"]), "success")
        return redirect(url_for("organisation.list_programmes", organisation_id=organisation_id))


@bp.route("/<uuid:organisation_id>/grade", methods=["GET", "POST"])
def list_grades(organisation_id):
    """Get a list of Grades."""
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


@bp.route("/<uuid:organisation_id>/grade/new", methods=["GET", "POST"])
def create_grade(organisation_id):
    """Create a new Grade."""
    form = GradeForm()
    organisation = Organisation().get(organisation_id)

    if form.validate_on_submit():
        new_grade = Grade().create(organisation_id=organisation_id, name=form.name.data)
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for(
                    "organisation.view_grade",
                    organisation_id=organisation_id,
                    grade_id=new_grade["id"],
                ),
                new_grade["name"],
            ),
            "success",
        )
        return redirect(url_for("organisation.list_grades", organisation_id=organisation_id))

    return render_template(
        "grade/create_grade.html",
        title="Create a new grade",
        organisation=organisation,
        form=form,
    )


@bp.route("/<uuid:organisation_id>/grade/<uuid:grade_id>", methods=["GET"])
def view_grade(organisation_id, grade_id):
    """View a specific Grade in an Organisation."""
    grade = Grade().get(organisation_id, grade_id)

    return render_template(
        "grade/view_grade.html",
        title=grade["name"],
        grade=grade,
    )


@bp.route(
    "/<uuid:organisation_id>/grade/<uuid:grade_id>/edit",
    methods=["GET", "POST"],
)
def edit_grade(organisation_id, grade_id):
    """Edit a specific Grade in an Organisation."""
    form = GradeForm()

    if form.validate_on_submit():
        changed_grade = Grade().edit(organisation_id=organisation_id, grade_id=grade_id, name=form.name.data)
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for(
                    "organisation.view_grade",
                    organisation_id=organisation_id,
                    grade_id=grade_id,
                ),
                changed_grade["name"],
            ),
            "success",
        )
        return redirect(url_for("organisation.list_grades", organisation_id=organisation_id))
    elif request.method == "GET":
        grade = Grade().get(organisation_id, grade_id)
        form.name.data = grade["name"]

    return render_template(
        "grade/update_grade.html",
        title="Edit {}".format(grade["name"]),
        form=form,
        grade=grade,
    )


@bp.route(
    "/<uuid:organisation_id>/grade/<uuid:grade_id>/delete",
    methods=["GET", "POST"],
)
@csrf.exempt
def delete_grade(organisation_id, grade_id):
    """Delete a specific Grade in an Organisation."""
    grade = Grade().get(organisation_id, grade_id)

    if request.method == "GET":
        return render_template(
            "grade/delete_grade.html",
            title="Delete {}".format(grade["name"]),
            grade=grade,
        )
    elif request.method == "POST":
        Grade().delete(organisation_id, grade_id)
        flash("{} has been deleted.".format(grade["name"]), "success")
        return redirect(url_for("organisation.list_grades", organisation_id=organisation_id))
