"""Primitives for operating on pyproject.toml files"""
import toml


class PyProjectParser:
    """Interface for parsing and manipulating data stored in a TOML formatted
     configuration file

     References:
         * (TOML Format PEP) https://www.python.org/dev/peps/pep-0621/
         * (Build System PEP) https://www.python.org/dev/peps/pep-0517/
         * (Build System Reqs PEP) https://www.python.org/dev/peps/pep-0518/
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
    def build_backend(self):
        """str: module name for the build backend to use for this project"""
        return self._data["build-system"]["build-backend"]

    @property
    def build_requirements(self):
        """list (str): list of packages required to run the build system backend"""
        return self._data["build-system"]["requires"]

    @property
    def project_name(self):
        """str: name of the distribution being built"""
        return self._data["project"]["name"]

    @property
    def project_version(self):
        """str: version of the distribution being built"""
        return self._data["project"]["version"]
