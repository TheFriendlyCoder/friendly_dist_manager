from .utils import run_pip, cd
from pathlib import Path
import pytest


def test_wheel():
    sample_toml = """
        [build-system]
        requires = ['wheel']
        build-backend = "friendly_dist_manager.hooks:PEP517"
        
        [project]
        name = "sample"
        version = "1.2.3"
    """

    pyproj = Path("pyproject.toml")
    pyproj.write_text(sample_toml)
    proj_dir = Path("sample")
    proj_dir.mkdir()
    init_file = proj_dir / "__init__.py"
    init_file.write_text("__version__='1.0.0'")
    args = f"install --no-build-isolation ."
    run_pip(args)

    # TODO: validate that install worked correctly
