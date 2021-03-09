"""PIP hooks for triggering build operations"""
import logging
from pathlib import Path
from .pyproject_parser import PyProjectParser
from .package_formats.wheel.wheel_file import WheelFile


class PEP517:
    """Hooks related to the PEP517 standard

    https://www.python.org/dev/peps/pep-0517/
    """
    @staticmethod
    def build_wheel(wheel_directory, _config_settings=None, _metadata_directory=None):
        """Hook triggered when user has requested a Python Wheel to be generated

        https://www.python.org/dev/peps/pep-0517/#build-wheel

        Args:
            wheel_directory (str):
                Path where the generated wheel file should be placed
            _config_settings (dict):
                optional settings provided by the caller to customize
                the behavior of the wheel file creation
            _metadata_directory (str):
                Path to folder where metadata describing the contents
                of the wheel file can be found

        Returns:
            str:
                Path to the generated wheel file
        """
        log = logging.getLogger(__name__)
        proj = Path("pyproject.toml")
        if not proj.exists():
            raise Exception("pyproject.toml configuration file not found")

        proj_file = PyProjectParser.from_file(proj)

        obj = WheelFile(proj_file.project_name, proj_file.project_version)
        for cur in Path(".").glob("**/*.py"):
            log.debug(f"Adding file {cur} to path {cur.parent}..")
            obj.add_file(cur, cur.parent)
        retval = obj.build(Path(wheel_directory))
        log.debug(f"Generated wheel file {retval}")
        return retval
