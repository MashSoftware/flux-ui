import csv
from io import StringIO

from app import csrf
from app.integrations.flux_api import Location, Organisation, Person, Role
from app.person import person
from app.person.forms import PersonForm
from flask import Response, flash, redirect, render_template, request, url_for


@person.route(
    "/<uuid:organisation_id>/people/",
    methods=["GET", "POST"],
)
def list(organisation_id):
    """Get a list of People."""
    name_query = request.args.get("name", type=str)
    role_filter = request.args.get("role_id", type=str)
    location_filter =  request.args.get("location_id", type=str)
    organisation = Organisation().get(organisation_id=organisation_id)

    if name_query:
        people = Person().list(organisation_id=organisation_id, name=name_query)
    elif role_filter:
        people = Person().list(organisation_id=organisation_id, role_id=role_filter)
    elif location_filter:
        people = Person().list(organisation_id=organisation_id, location_id=location_filter)
    else:
        people = Person().list(
            organisation_id=organisation_id,
        )

    return render_template(
        "list_people.html",
        title="People",
        organisation=organisation,
        people=people,
    )


@person.route(
    "/<uuid:organisation_id>/people/new",
    methods=["GET", "POST"],
)
def create(organisation_id):
    """Create a new Person."""
    form = PersonForm()
    organisation = Organisation().get(organisation_id=organisation_id)
    roles = Role().list(organisation_id=organisation_id)
    form.role.choices = [(role["id"], role["title"]) for role in roles if roles]

    locations = Location().list(organisation_id=organisation_id)
    form.location.choices = [(location["id"], location["name"]) for location in locations if locations]

    if form.validate_on_submit():
        new_person = Person().create(
            name=form.name.data,
            email_address=form.email_address.data,
            role_id=form.role.data,
            employment=form.employment.data,
            full_time_equivalent=form.full_time_equivalent.data,
            location_id=form.location.data,
            organisation_id=organisation_id,
        )
        flash(
            "<a href='{}' class='alert-link'>{}</a> has been created.".format(
                url_for(
                    "person.view",
                    organisation_id=organisation_id,
                    person_id=new_person["id"],
                ),
                new_person["name"],
            ),
            "success",
        )
        return redirect(url_for("person.list", organisation_id=organisation_id))
    elif request.method == "GET":
        form.email_address.data = f"@{organisation['domain']}"
    
    return render_template(
        "create_person.html",
        title="Create a new person",
        organisation=organisation,
        form=form,
    )


@person.route(
    "/<uuid:organisation_id>/people/<uuid:person_id>",
    methods=["GET"],
)
def view(organisation_id, person_id):
    """View a specific Person in an Person."""
    person = Person().get(organisation_id=organisation_id, person_id=person_id)

    return render_template(
        "view_person.html",
        title=person["name"],
        person=person,
    )


@person.route(
    "/<uuid:organisation_id>/people/<uuid:person_id>/edit",
    methods=["GET", "POST"],
)
def edit(organisation_id, person_id):
    """Edit a specific Person in an Person."""
    person = Person().get(organisation_id=organisation_id, person_id=person_id)
    roles = Role().list(organisation_id=organisation_id)
    locations = Location().list(organisation_id=organisation_id)
    
    form = PersonForm()
    form.role.choices = [(role["id"], role["title"]) for role in roles if roles]
    form.location.choices = [(location["id"], location["name"]) for location in locations if locations]

    if form.validate_on_submit():
        changed_person = Person().edit(
            person_id=person_id,
            name=form.name.data,
            email_address=form.email_address.data,
            role_id=form.role.data,
            employment=form.employment.data,
            full_time_equivalent=form.full_time_equivalent.data,
            location_id=form.location.data,
            organisation_id=organisation_id,
        )
        flash(
            "Your changes to <a href='{}' class='alert-link'>{}</a> have been saved.".format(
                url_for(
                    "person.view",
                    organisation_id=organisation_id,
                    person_id=person_id,
                ),
                changed_person["name"],
            ),
            "success",
        )
        return redirect(url_for("person.list", organisation_id=organisation_id))
    elif request.method == "GET":
        form.name.data = person["name"]
        form.email_address.data = person["email_address"]
        form.role.data = person["role"]["id"]
        form.employment.data = person["employment"]
        form.full_time_equivalent.data = person["full_time_equivalent"]
        form.location.data = person["location"]["id"]

    return render_template(
        "edit_person.html",
        title=f"Edit {person['name']}",
        form=form,
        person=person,
    )


@person.route(
    "/<uuid:organisation_id>/people/<uuid:person_id>/delete",
    methods=["GET", "POST"],
)
@csrf.exempt
def delete(organisation_id, person_id):
    """Delete a specific Person in an Person."""
    person = Person().get(organisation_id=organisation_id, person_id=person_id)

    if request.method == "GET":
        return render_template(
            "delete_person.html",
            title=f"Delete {person['name']}",
            person=person,
        )
    elif request.method == "POST":
        Person().delete(organisation_id=organisation_id, person_id=person_id)
        flash("{} has been deleted.".format(person["name"]), "success")
        return redirect(url_for("person.list", organisation_id=organisation_id))


@person.route("/<uuid:organisation_id>/people/download", methods=["GET"])
def download(organisation_id):
    """Download a list of People in an Organisation in CSV format."""
    people = Person().list(organisation_id=organisation_id)

    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(
            (
                "NAME",
                "ROLE",
                "GRADE",
                "PRACTICE",
            )
        )
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each item
        for person in people:
            w.writerow(
                (
                    person["name"],
                    person["role"]["title"] if person["role"] else None,
                    person["role"]["grade"]["name"] if person["role"] else None,
                    person["role"]["practice"]["name"] if person["role"]["practice"] else None,
                )
            )
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    response = Response(generate(), mimetype="text/csv")
    response.headers.set("Content-Disposition", "attachment", filename="people.csv")
    return response
