"""Primitives for manipulating the 'build-system' table in a pyproject.toml file"""


class BuildSystemTable:
    """Abstraction around the 'build-system' table from a pyproject.toml file

    References:
        * (Add support custom build backends) https://www.python.org/dev/peps/pep-0518/
        * (Original Proposal) https://www.python.org/dev/peps/pep-0517/
    """
    def __init__(self, data):
        """
        Args:
            data (dict):
                TOML data parsed from a pyproject.toml config file
        """
        self._data = data

    @property
    def backend(self):
        """str: module name for the build backend to use for this project"""
        return self._data["build-backend"]

    @property
    def requirements(self):
        """list (str): list of packages required to run the build system backend"""
        return self._data["requires"]
