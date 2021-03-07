from .utils import run_pip
from pathlib import Path
import pytest


@pytest.mark.skip(reason="To be fixed")
def test_wheel():
    sample_toml = """
        [build-system]
        requires = ['wheel']
        build-backend = "friendly_dist_manager.hooks:PEP517"
    """

    pyproj = Path("pyproject.toml")
    pyproj.write_text(sample_toml)
    proj_dir = Path("sample")
    proj_dir.mkdir()
    init_file = proj_dir / "__init__.py"
    init_file.write_text("__version__='1.0.0'")
    args = "install --no-build-isolation ."
    run_pip(args)
