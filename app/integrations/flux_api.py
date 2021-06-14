import json
from datetime import datetime
from urllib.parse import urlencode

import requests
from flask import current_app
from werkzeug.exceptions import (
    BadRequest,
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
                return json.loads(response.text)
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
    def create(self, name, manager_id, organisation_id):
        """Create a new Programme."""
        url = "{0}/{1}/organisations/{2}/programmes".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        new_programme = {"name": name}
        if manager_id:
            new_programme["manager_id"] = manager_id

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
        """Get a list of Programmes."""
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
                return json.loads(response.text)
            elif response.status_code == 204:
                return None
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def get(self, programme_id, organisation_id):
        """Get a specific Programme."""
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

    def edit(self, programme_id, name, manager_id, organisation_id):
        """Edit a Programme with a specific ID."""
        url = "{0}/{1}/organisations/{2}/programmes/{3}".format(self.url, self.version, organisation_id, programme_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        changed_programme = {"name": name}
        if manager_id:
            changed_programme["manager_id"] = manager_id

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

    def delete(self, programme_id, organisation_id):
        """Delete a Programme with a specific ID."""
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


class Project(FluxAPI):
    def create(self, name, manager_id, programme_id, organisation_id):
        """Create a new Project."""
        url = "{0}/{1}/organisations/{2}/projects".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        new_project = {"name": name, "programme_id": programme_id}
        if manager_id:
            new_project["manager_id"] = manager_id

        try:
            response = requests.post(
                url,
                data=json.dumps(new_project),
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
        """Get a list of Projects."""
        if kwargs:
            args = {"name": kwargs.get("name", ""), "programme_id": kwargs.get("programme_id", "")}
            qs = urlencode(args)
            url = "{0}/{1}/organisations/{2}/projects?{3}".format(self.url, self.version, organisation_id, qs)
        else:
            url = "{0}/{1}/organisations/{2}/projects".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                return json.loads(response.text)
            elif response.status_code == 204:
                return None
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def get(self, project_id, organisation_id):
        """Get a specific Project."""
        url = "{0}/{1}/organisations/{2}/projects/{3}".format(self.url, self.version, organisation_id, project_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                project = json.loads(response.text)
                project["created_at"] = datetime.strptime(project["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if project["updated_at"]:
                    project["updated_at"] = datetime.strptime(project["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return project
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def edit(self, project_id, name, manager_id, programme_id, organisation_id):
        """Edit a Project with a specific ID."""
        url = "{0}/{1}/organisations/{2}/projects/{3}".format(self.url, self.version, organisation_id, project_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        changed_project = {"name": name, "programme_id": programme_id}
        if manager_id:
            changed_project["manager_id"] = manager_id

        try:
            response = requests.put(
                url,
                data=json.dumps(changed_project),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                project = json.loads(response.text)
                project["created_at"] = datetime.strptime(project["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if project["updated_at"]:
                    project["updated_at"] = datetime.strptime(project["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return project
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def delete(self, project_id, organisation_id):
        """Delete a Project with a specific ID."""
        url = "{0}/{1}/organisations/{2}/projects/{3}".format(self.url, self.version, organisation_id, project_id)
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
    def create(self, name, organisation_id):
        """Create a new Grade."""
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
        """Get a list of Grades."""
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
                return json.loads(response.text)
            elif response.status_code == 204:
                return None
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def get(self, grade_id, organisation_id):
        """Get a specific Grade."""
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

    def edit(self, grade_id, name, organisation_id):
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

    def delete(self, grade_id, organisation_id):
        """Delete a Grade with a specific ID."""
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


class Practice(FluxAPI):
    def create(self, name, head_id, organisation_id):
        """Create a new Practice."""
        url = "{0}/{1}/organisations/{2}/practices".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        new_practice = {"name": name}
        if head_id:
            new_practice["head_id"] = head_id

        try:
            response = requests.post(
                url,
                data=json.dumps(new_practice),
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
        """Get a list of Practices."""
        if kwargs:
            args = {"name": kwargs.get("name", "")}
            qs = urlencode(args)
            url = "{0}/{1}/organisations/{2}/practices?{3}".format(self.url, self.version, organisation_id, qs)
        else:
            url = "{0}/{1}/organisations/{2}/practices".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                return json.loads(response.text)
            elif response.status_code == 204:
                return None
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def get(self, practice_id, organisation_id):
        """Get a specific Practice."""
        url = "{0}/{1}/organisations/{2}/practices/{3}".format(self.url, self.version, organisation_id, practice_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                practice = json.loads(response.text)
                practice["created_at"] = datetime.strptime(practice["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if practice["updated_at"]:
                    practice["updated_at"] = datetime.strptime(practice["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return practice
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def edit(self, practice_id, name, head_id, organisation_id):
        """Edit a Practice with a specific ID."""
        url = "{0}/{1}/organisations/{2}/practices/{3}".format(self.url, self.version, organisation_id, practice_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        changed_practice = {"name": name}
        if head_id:
            changed_practice["head_id"] = head_id

        try:
            response = requests.put(
                url,
                data=json.dumps(changed_practice),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                practice = json.loads(response.text)
                practice["created_at"] = datetime.strptime(practice["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if practice["updated_at"]:
                    practice["updated_at"] = datetime.strptime(practice["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return practice
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def delete(self, practice_id, organisation_id):
        """Delete a Practice with a specific ID."""
        url = "{0}/{1}/organisations/{2}/practices/{3}".format(self.url, self.version, organisation_id, practice_id)
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


class Role(FluxAPI):
    def create(self, title, grade_id, practice_id, organisation_id):
        """Create a new Role."""
        url = "{0}/{1}/organisations/{2}/roles".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        new_role = {"title": title, "grade_id": grade_id}
        if practice_id:
            new_role["practice_id"] = practice_id

        try:
            response = requests.post(
                url,
                data=json.dumps(new_role),
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
        """Get a list of Roles."""
        if kwargs:
            args = {"title": kwargs.get("title", "")}
            qs = urlencode(args)
            url = "{0}/{1}/organisations/{2}/roles?{3}".format(self.url, self.version, organisation_id, qs)
        else:
            url = "{0}/{1}/organisations/{2}/roles".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                return json.loads(response.text)
            elif response.status_code == 204:
                return None
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def get(self, role_id, organisation_id):
        """Get a specific Role."""
        url = "{0}/{1}/organisations/{2}/roles/{3}".format(self.url, self.version, organisation_id, role_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                role = json.loads(response.text)
                role["created_at"] = datetime.strptime(role["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if role["updated_at"]:
                    role["updated_at"] = datetime.strptime(role["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return role
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def edit(self, role_id, title, grade_id, practice_id, organisation_id):
        """Edit a Role with a specific ID."""
        url = "{0}/{1}/organisations/{2}/roles/{3}".format(self.url, self.version, organisation_id, role_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        changed_role = {"title": title, "grade_id": grade_id}
        if practice_id:
            changed_role["practice_id"] = practice_id

        try:
            response = requests.put(
                url,
                data=json.dumps(changed_role),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                role = json.loads(response.text)
                role["created_at"] = datetime.strptime(role["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if role["updated_at"]:
                    role["updated_at"] = datetime.strptime(role["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return role
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def delete(self, role_id, organisation_id):
        """Delete a Role with a specific ID."""
        url = "{0}/{1}/organisations/{2}/roles/{3}".format(self.url, self.version, organisation_id, role_id)
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


class Person(FluxAPI):
    def create(
        self,
        name,
        role_id,
        email_address,
        full_time_equivalent,
        location,
        employment,
        organisation_id,
    ):
        """Create a new Person."""
        url = "{0}/{1}/organisations/{2}/people".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        new_person = {
            "name": name,
            "role_id": role_id,
            "email_address": email_address,
            "full_time_equivalent": float(full_time_equivalent),
            "location": location,
            "employment": employment,
        }

        try:
            response = requests.post(
                url,
                data=json.dumps(new_person),
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
            elif response.status_code == 400:
                raise BadRequest
            else:
                raise InternalServerError

    def list(self, organisation_id, **kwargs):
        """Get a list of People."""
        if kwargs:
            args = {"name": kwargs.get("name", "")}
            qs = urlencode(args)
            url = "{0}/{1}/organisations/{2}/people?{3}".format(self.url, self.version, organisation_id, qs)
        else:
            url = "{0}/{1}/organisations/{2}/people".format(self.url, self.version, organisation_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                return json.loads(response.text)
            elif response.status_code == 204:
                return None
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def get(self, person_id, organisation_id):
        """Get a specific Person."""
        url = "{0}/{1}/organisations/{2}/people/{3}".format(self.url, self.version, organisation_id, person_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                person = json.loads(response.text)
                person["created_at"] = datetime.strptime(person["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if person["updated_at"]:
                    person["updated_at"] = datetime.strptime(person["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return person
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def edit(
        self,
        person_id,
        name,
        role_id,
        email_address,
        full_time_equivalent,
        location,
        employment,
        organisation_id,
    ):
        """Edit a Person with a specific ID."""
        url = "{0}/{1}/organisations/{2}/people/{3}".format(self.url, self.version, organisation_id, person_id)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        changed_person = {
            "name": name,
            "role_id": role_id,
            "email_address": email_address,
            "full_time_equivalent": float(full_time_equivalent),
            "location": location,
            "employment": employment,
        }

        try:
            response = requests.put(
                url,
                data=json.dumps(changed_person),
                headers=headers,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise RequestTimeout
        except requests.exceptions.ConnectionError:
            raise InternalServerError
        else:
            if response.status_code == 200:
                person = json.loads(response.text)
                person["created_at"] = datetime.strptime(person["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                if person["updated_at"]:
                    person["updated_at"] = datetime.strptime(person["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                return person
            elif response.status_code == 404:
                raise NotFound
            elif response.status_code == 429:
                raise TooManyRequests
            else:
                raise InternalServerError

    def delete(self, person_id, organisation_id):
        """Delete a Person with a specific ID."""
        url = "{0}/{1}/organisations/{2}/people/{3}".format(self.url, self.version, organisation_id, person_id)
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
