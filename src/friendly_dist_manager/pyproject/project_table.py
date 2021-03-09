"""Primitives for manipulating the 'project' table in a pyproject.toml file"""


class ProjectTable:
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
