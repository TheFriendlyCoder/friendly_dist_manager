"""Primitives for manipulating the 'project' table in a pyproject.toml file"""
from pathlib import Path
from collections import namedtuple

# TODO: add support for dynamic metadata sub-table

Person = namedtuple("Person", ["name", "email"])
Entrypoint = namedtuple("Entrypoint", ["name", "ref"])


class ProjectTable:  # pylint: disable=too-many-public-methods
    """Abstraction around the 'project' table from a pyproject.toml file

    References:
        * https://www.python.org/dev/peps/pep-0621/
    """
    def __init__(self, data):
        """
        Args:
            data (dict):
                TOML data parsed from a pyproject.toml config file
        """
        self._data = data

    @property
    def name(self):
        """str: name of the distribution being built"""
        return self._data["name"]

    @property
    def version(self):
        """str: version of the distribution being built"""
        return self._data["version"]

    @property
    def description(self):
        """str: descriptive name summarizing the purpose of the distribution"""
        return self._data.get("description", "")

    @property
    def readme_file(self):
        """pathlib.Path: reference to the readme file associated with the project,
        or None if no readme file provided"""
        if "readme" not in self._data:
            return None
        return Path(self._data["readme"])

    @property
    def readme(self):
        """str: text formatted data loaded from the mentioned readme file
        associated with the project"""
        if not self.readme_file:
            return ""

        if not self.readme_file.exists():
            raise FileNotFoundError(f"Readme file {self.readme_file} does not exist")
        return self.readme_file.read_text(encoding="UTF-8")

    @property
    def python_requirement(self):
        """str: the Python runtime version identifier indicating the range of
        versions supported by this project"""
        return self._data.get("requires-python", "")

    @property
    def license(self):
        """str: text explaining the licensing details associated with the project"""
        if "license" not in self._data:
            return ""

        if "text" in self._data["license"]:
            return self._data["license"]["text"]
        lic_file = Path(self._data["license"]["file"])
        if not lic_file.exists():
            raise FileNotFoundError(f"License file not found: {lic_file}")
        return lic_file.read_text(encoding="UTF-8")

    @property
    def authors(self):
        """list(Person): list of people who are considered 'authors' of the project

        Note: each person may have a name and/or an email address, but either one may
        be omitted
        """
        retval = list()
        for cur_per in self._data.get("authors", list()):
            retval.append(Person(cur_per.get("name"), cur_per.get("email")))
        return retval

    @property
    def maintainers(self):
        """list(Person): list of people who are considered 'maintainers' of the project

        Note: each person may have a name and/or an email address, but either one may
        be omitted
        """
        retval = list()
        for cur_per in self._data.get("maintainers", list()):
            retval.append(Person(cur_per.get("name"), cur_per.get("email")))
        return retval

    @property
    def keywords(self):
        """list (str): descriptive keywords used when searching for project on pypi"""
        return self._data.get("keywords", list())

    @property
    def classifiers(self):
        """list (str): trove classifiers describing properties of the project

        https://pypi.org/classifiers/
        """
        return self._data.get("classifiers", list())

    @property
    def _urls(self):
        """dict: mapping table containing keys / IDs of different URLs associated
        with the project, mapped to their respective URLs"""
        return self._data.get("urls", dict())

    @property
    def homepage(self):
        """str: URL of the project homepage. May be an empty string if undefined."""
        return self._urls.get("homepage", "")

    @property
    def documentation(self):
        """str: URL of the project documentation. May be an empty string if undefined."""
        return self._urls.get("documentation", "")

    @property
    def repository(self):
        """str: URL of the source repository of the project. May be an empty string if undefined."""
        return self._urls.get("repository", "")

    @property
    def changelog(self):
        """str: URL of the change log for the project. May be an empty string if undefined."""
        return self._urls.get("changelog", "")

    @property
    def console_scripts(self):
        """list (Entrypoint): list of entry points for console / shell scripts exposed by the project"""
        retval = list()
        for ep_name, ep_ref in self._data.get("scripts", dict()).items():
            retval.append(Entrypoint(ep_name, ep_ref))
        return retval

    @property
    def gui_scripts(self):
        """list (Entrypoint): list of application entry points for GUI based projects"""
        retval = list()
        for ep_name, ep_ref in self._data.get("gui-scripts", dict()).items():
            retval.append(Entrypoint(ep_name, ep_ref))
        return retval

    @property
    def _entrypoints(self):
        """dict: mapping of custom entrypoint identifiers to the set of entrypoints associated
        with each ID"""
        return self._data.get("entry-point", dict())

    @property
    def entrypoint_identifiers(self):
        """list (str): list of custom entrypoint identifiers associated with the project"""
        return list(self._entrypoints.keys())

    def get_entrypoint(self, entrypoint_id):
        """Gets definition for a custom entrypoint associated with the project

        Args:
            entrypoint_id (str):
                ID of the entrypoint to retrieve. See :meth:`entrypoint_identifiers`
                for supported values

        Returns:
            list (Entrypoint):
                list of entrypoints associated with the entrypoint identifier
        """
        retval = list()
        for ep_name, ep_ref in self._entrypoints.get(entrypoint_id, dict()).items():
            retval.append(Entrypoint(ep_name, ep_ref))
        return retval

    @property
    def dependencies(self):
        """list (str): list of package dependencies associated with this project

        References:
            * https://www.python.org/dev/peps/pep-0508/
        """
        return self._data.get("dependencies", list())

    @property
    def _optional_dependencies(self):
        """dict: mapping table linking IDs of sets of optional package dependencies, to
        the list of dependency definitions associated with them"""
        return self._data.get("optional-dependencies", dict())

    @property
    def optional_dependency_identifiers(self):
        """list (str): list of IDs associated with groups of optional package dependencies
        associated with the project"""
        return list(self._optional_dependencies.keys())

    def get_optional_dependencies(self, dependency_id):
        """Set of dependencies associated with a specific group ID

        References:
            * https://www.python.org/dev/peps/pep-0508/

        Args:
            dependency_id (str):
                identifier for a specific group of optional dependencies associated
                with the project. See :meth:`optional_dependency_identifiers` for list
                of valid options

        Returns:
            list (str):
                list of dependency definitions for the optional dependencies associated
                with the specified ID
        """
        return self._optional_dependencies.get(dependency_id, list())
