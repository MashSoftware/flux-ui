import csv
from io import StringIO

from app import csrf
from app.integrations.flux_api import Organisation, Location
from app.location import location
from app.location.forms import LocationForm
from flask import Response, flash, redirect, render_template, request, url_for


@location.route("/<uuid:organisation_id>/locations/", methods=["GET", "POST"])
def list(organisation_id):
    """Get a list of Locations in an Organisation."""
    name_query = request.args.get("name", type=str)
    organisation = Organisation().get(organisation_id=organisation_id)

    if name_query:
        locations = Location().list(organisation_id=organisation_id, name=name_query)
    else:
        locations = Location().list(organisation_id=organisation_id)

    return render_template(
        "list_locations.html",
        title="Locations",
        organisation=organisation,
        locations=locations,
    )


@location.route("/<uuid:organisation_id>/locations/new", methods=["GET", "POST"])
def create(organisation_id):
    """Create a new Location in an Organisation."""
    form = LocationForm()
    organisation = Organisation().get(organisation_id=organisation_id)

    if form.validate_on_submit():
        new_location = Location().create(
            organisation_id=organisation_id,
            name=form.name.data,
            address=form.address.data,
        )
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for(
                    "location.view",
                    organisation_id=organisation_id,
                    location_id=new_location["id"],
                ),
                new_location["name"],
            ),
            "success",
        )
        return redirect(url_for("location.list", organisation_id=organisation_id))

    return render_template(
        "create_location.html",
        title="Create a new location",
        organisation=organisation,
        form=form,
    )


@location.route("/<uuid:organisation_id>/locations/<uuid:location_id>", methods=["GET"])
def view(organisation_id, location_id):
    """View a specific Location in an Organisation."""
    location = Location().get(organisation_id=organisation_id, location_id=location_id)

    return render_template(
        "view_location.html",
        title=location["name"],
        location=location,
    )


@location.route(
    "/<uuid:organisation_id>/locations/<uuid:location_id>/edit",
    methods=["GET", "POST"],
)
def edit(organisation_id, location_id):
    """Edit a specific Location in an Organisation."""
    location = Location().get(organisation_id=organisation_id, location_id=location_id)
    form = LocationForm()

    if form.validate_on_submit():
        changed_location = Location().edit(
            organisation_id=organisation_id,
            location_id=location_id,
            name=form.name.data,
            address=form.address.data,
        )
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for(
                    "location.view",
                    organisation_id=organisation_id,
                    location_id=location_id,
                ),
                changed_location["name"],
            ),
            "success",
        )
        return redirect(url_for("location.list", organisation_id=organisation_id))
    elif request.method == "GET":
        form.name.data = location["name"]
        form.address.data = location["address"]

    return render_template(
        "update_location.html",
        title=f"Edit {location['name']}",
        form=form,
        location=location,
    )


@location.route(
    "/<uuid:organisation_id>/locations/<uuid:location_id>/delete",
    methods=["GET", "POST"],
)
@csrf.exempt
def delete(organisation_id, location_id):
    """Delete a specific Location in an Organisation."""
    location = Location().get(organisation_id=organisation_id, location_id=location_id)

    if request.method == "GET":
        return render_template(
            "delete_location.html",
            title=f"Delete {location['name']}",
            location=location,
        )
    elif request.method == "POST":
        Location().delete(organisation_id=organisation_id, location_id=location_id)
        flash("{} has been deleted.".format(location["name"]), "success")
        return redirect(url_for("location.list", organisation_id=organisation_id))


@location.route("/<uuid:organisation_id>/locations/download", methods=["GET"])
def download(organisation_id):
    """Download a list of Locations in an Organisation in CSV format."""
    locations = Location().list(organisation_id=organisation_id)

    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(("NAME", "ADDRESS"))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each item
        for location in locations:
            w.writerow(
                (
                    location["name"],
                    location["address"],
                )
            )
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    response = Response(generate(), mimetype="text/csv")
    response.headers.set("Content-Disposition", "attachment", filename="locations.csv")
    return response
