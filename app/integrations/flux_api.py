import json
from datetime import datetime
from urllib.parse import urlencode

import requests
from flask import current_app
from werkzeug.exceptions import (
    Conflict,
    InternalServerError,
    NotFound,
    RequestTimeout,
    TooManyRequests,
)


class FluxAPI:
    def __init__(self):
        self.url = current_app.config["FLUX_API_URL"]
        self.version = current_app.config["FLUX_API_VERSION"]
        self.timeout = current_app.config["TIMEOUT"]


class Organisation(FluxAPI):
    def create(self, name, domain):
        """Create a new Organisation."""
        url = "{0}/{1}/organisations".format(self.url, self.version)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        new_organisation = {"name": name, "domain": domain}

        try:
            response = requests.post(
                url,
                data=json.dumps(new_organisation),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 201:
                organisation = json.loads(response.text)
                organisation["created_at"] = datetime.strptime(organisation["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if organisation["updated_at"]:
                    organisation["updated_at"] = datetime.strptime(organisation["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return organisation
            elif response.status_code == 409:
                raise Conflict
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def list(self, **kwargs):
        """Get a list of Organisations."""
        if kwargs:
            args = {"name": kwargs.get("name", "")}
            qs = urlencode(args)
            url = "{0}/{1}/organisations?{2}".format(self.url, self.version, qs)
        else:
            url = "{0}/{1}/organisations".format(self.url, self.version)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                organisations = json.loads(response.text)
                for organisation in organisations:
                    organisation["created_at"] = datetime.strptime(organisation["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    if organisation["updated_at"]:
                        organisation["updated_at"] = datetime.strptime(
                            organisation["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
                        )
                return organisations
            elif response.status_code == 204:
                return None
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def get(self, organisation_id):
        """Get a Organisation with a specific ID."""
        url = "{0}/{1}/organisations/{2}".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                organisation = json.loads(response.text)
                organisation["created_at"] = datetime.strptime(organisation["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if organisation["updated_at"]:
                    organisation["updated_at"] = datetime.strptime(organisation["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return organisation
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def edit(self, organisation_id, name, domain):
        """Edit a Organisation with a specific ID."""
        url = "{0}/{1}/organisations/{2}".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        changed_organisation = {"name": name, "domain": domain}

        try:
            response = requests.put(
                url,
                data=json.dumps(changed_organisation),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                organisation = json.loads(response.text)
                organisation["created_at"] = datetime.strptime(organisation["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if organisation["updated_at"]:
                    organisation["updated_at"] = datetime.strptime(organisation["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return organisation
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def delete(self, organisation_id):
        """Delete a Organisation with a specific ID."""
        url = "{0}/{1}/organisations/{2}".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.delete(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 204:
                return None
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError


class Programme(FluxAPI):
    def create(self, organisation_id, name, programme_manager):
        """Create a new Programme in an Organisation."""
        url = "{0}/{1}/organisations/{2}/programmes".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        new_programme = {"name": name, "programme_manager": programme_manager}

        try:
            response = requests.post(
                url,
                data=json.dumps(new_programme),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 201:
                organisation = json.loads(response.text)
                organisation["created_at"] = datetime.strptime(organisation["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if organisation["updated_at"]:
                    organisation["updated_at"] = datetime.strptime(organisation["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return organisation
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def list(self, organisation_id, **kwargs):
        """Get a list of Programmes in an Organisation."""
        if kwargs:
            args = {"name": kwargs.get("name", "")}
            qs = urlencode(args)
            url = "{0}/{1}/organisations/{2}/programmes?{3}".format(self.url, self.version, organisation_id, qs)
        else:
            url = "{0}/{1}/organisations/{2}/programmes".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                programmes = json.loads(response.text)
                for programme in programmes:
                    programme["created_at"] = datetime.strptime(programme["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    if programme["updated_at"]:
                        programme["updated_at"] = datetime.strptime(programme["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return programmes
            elif response.status_code == 204:
                return None
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def get(self, organisation_id, programme_id):
        """Get a specific Programme in an Organisation."""
        url = "{0}/{1}/organisations/{2}/programmes/{3}".format(self.url, self.version, organisation_id, programme_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                programme = json.loads(response.text)
                programme["created_at"] = datetime.strptime(programme["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if programme["updated_at"]:
                    programme["updated_at"] = datetime.strptime(programme["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return programme
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def edit(self, organisation_id, programme_id, name, programme_manager):
        """Edit a Programme with a specific ID."""
        url = "{0}/{1}/organisations/{2}/programmes/{3}".format(self.url, self.version, organisation_id, programme_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        changed_programme = {"name": name, "programme_manager": programme_manager}

        try:
            response = requests.put(
                url,
                data=json.dumps(changed_programme),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                programme = json.loads(response.text)
                programme["created_at"] = datetime.strptime(programme["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if programme["updated_at"]:
                    programme["updated_at"] = datetime.strptime(programme["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return programme
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def delete(self, organisation_id, programme_id):
        """Delete a Organisation with a specific ID."""
        url = "{0}/{1}/organisations/{2}/programmes/{3}".format(self.url, self.version, organisation_id, programme_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.delete(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 204:
                return None
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError


class Grade(FluxAPI):
    def create(self, organisation_id, name):
        """Create a new Grade in an Organisation."""
        url = "{0}/{1}/organisations/{2}/grades".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        new_grade = {"name": name}

        try:
            response = requests.post(
                url,
                data=json.dumps(new_grade),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 201:
                organisation = json.loads(response.text)
                organisation["created_at"] = datetime.strptime(organisation["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if organisation["updated_at"]:
                    organisation["updated_at"] = datetime.strptime(organisation["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return organisation
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def list(self, organisation_id, **kwargs):
        """Get a list of Grades in an Organisation."""
        if kwargs:
            args = {"name": kwargs.get("name", "")}
            qs = urlencode(args)
            url = "{0}/{1}/organisations/{2}/grades?{3}".format(self.url, self.version, organisation_id, qs)
        else:
            url = "{0}/{1}/organisations/{2}/grades".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                grades = json.loads(response.text)
                for grade in grades:
                    grade["created_at"] = datetime.strptime(grade["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    if grade["updated_at"]:
                        grade["updated_at"] = datetime.strptime(grade["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return grades
            elif response.status_code == 204:
                return None
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def get(self, organisation_id, grade_id):
        """Get a specific Grade in an Organisation."""
        url = "{0}/{1}/organisations/{2}/grades/{3}".format(self.url, self.version, organisation_id, grade_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                grade = json.loads(response.text)
                grade["created_at"] = datetime.strptime(grade["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if grade["updated_at"]:
                    grade["updated_at"] = datetime.strptime(grade["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return grade
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def edit(self, organisation_id, grade_id, name):
        """Edit a Grade with a specific ID."""
        url = "{0}/{1}/organisations/{2}/grades/{3}".format(self.url, self.version, organisation_id, grade_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        changed_grade = {"name": name}

        try:
            response = requests.put(
                url,
                data=json.dumps(changed_grade),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                grade = json.loads(response.text)
                grade["created_at"] = datetime.strptime(grade["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if grade["updated_at"]:
                    grade["updated_at"] = datetime.strptime(grade["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return grade
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def delete(self, organisation_id, grade_id):
        """Delete a Organisation with a specific ID."""
        url = "{0}/{1}/organisations/{2}/grades/{3}".format(self.url, self.version, organisation_id, grade_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.delete(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 204:
                return None
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError
