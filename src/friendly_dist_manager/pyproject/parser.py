"""Primitives for operating on pyproject.toml files"""
import toml
from .project_table import ProjectTable
from .build_system_table import BuildSystemTable


class PyProjectParser:
    """Interface for parsing and manipulating data stored in a TOML formatted
     configuration file

    Each section, or table, within the TOML configuration file is defined by
    it's own independent PEP standard. As such this primary entry point defers
    the handling of specific tables to supporting classes.

    References:
        * (TOML Spec) https://toml.io/en/
    """
    def __init__(self, toml_data):
        """
        Args:
            toml_data (str):
                Raw text loaded from a TOML formatted configuration file
        """
        self._data = toml.loads(toml_data)

    @classmethod
    def from_file(cls, file_path):
        """Factory method used to instantiate instances of this
        class from a disk-based file

        Args:
            file_path (pathlib.Path):
                path to the TOML file to load

        Returns:
            PyProjectParser:
                reference to the class instance created
        """
        return PyProjectParser(file_path.read_text())

    @property
    def build_system(self):
        """BuildSystemTable: returns the 'build-system' table from the config file"""
        return BuildSystemTable(self._data["build-system"])

    @property
    def project(self):
        """ProjectTable: returns the 'project' table from the config file"""
        return ProjectTable(self._data["project"])
