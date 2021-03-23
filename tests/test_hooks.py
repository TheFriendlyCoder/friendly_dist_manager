from .utils import run_pip, cd
from pathlib import Path
import pytest

DEFAULT_BACKEND = "friendly_dist_manager.hooks:PEP517"


def test_minimal_wheel():
    sample_toml = f"""
        [build-system]
        requires = ['wheel']
        build-backend = "{DEFAULT_BACKEND}"
        
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


def test_complete_wheel():
    expected_name = "FuBar"
    expected_version = "4.5.6"
    expected_desc = "My Cool Library"
    expected_readme = "My readme for my super cool library"
    Path("README.rst").write_text(expected_readme)
    expected_python = ">=3.6"
    expected_license = "BSD style license here"
    expected_author_name = "John Doe"
    expected_author_email = "jdoe@someplace.com"
    expected_maintainer_name = "Jane Doe"
    expected_maintainer_email = "jane@someplace.com"
    expected_keywords = ["some", "keyword", "args"]
    toml_keywords = ",".join([f'"{i}"' for i in expected_keywords])
    expected_classifiers = ["fu", "bar"]
    toml_classifiers = ",".join([f'"{i}"' for i in expected_classifiers])
    expected_homepage = "https://fubar.company.com"
    expected_docs_url = "https://docs.company.com"
    expected_repo_url = "https://github.com/fubar"
    expected_changelog_url = "https://docs.company.com/changes"
    expected_download_url = "https://www.pypi.org/fubar/fubar4.5.6.whl"
    expected_console_script = "fubar.entry"
    expected_ref1 = "library:main"
    expected_gui_script = "fubar.gui.entry"
    expected_ref2 = "library:gui_main"
    expected_custom_entrypoint = "MyPlugin"
    expected_custom_script = "fubar.plugin.entry"
    expected_ref3 = "library:plugin_main"
    expected_dependency = "requests>=2.0"
    expected_dev_dependency = "pytest"
    expected_custom_depencency = "dev"

    sample_toml = f"""
        [build-system]
        requires = ['wheel', 'setuptools']
        build-backend = "{DEFAULT_BACKEND}"

        [project]
        name = "{expected_name}"
        version = "{expected_version}"
        description = "{expected_desc}"
        readme = "README.rst"
        requires-python = "{expected_python}"
        license = {{"text" = "{expected_license}"}}
        keywords = [{toml_keywords}]
        classifiers = [{toml_classifiers}]
        dependencies = ["{expected_dependency}"]
        optional-dependencies.{expected_custom_depencency} = ["{expected_dev_dependency}"]

        [[project.authors]]
        name = "{expected_author_name}"
        email = "{expected_author_email}"

        [[project.maintainers]]
        name = "{expected_maintainer_name}"
        email = "{expected_maintainer_email}"

        [project.urls] 
        homepage = "{expected_homepage}"
        documentation = "{expected_docs_url}"
        repository = "{expected_repo_url}"
        changelog = "{expected_changelog_url}"
        download = "{expected_download_url}"
        
        [project.scripts]
        "{expected_console_script}" = "{expected_ref1}"

        [project.gui-scripts]
        "{expected_gui_script}" = "{expected_ref2}"

        [project.entry-point.{expected_custom_entrypoint}]
        "{expected_custom_script}" = "{expected_ref3}"

    """

    pyproj = Path("pyproject.toml")
    pyproj.write_text(sample_toml)
    proj_dir = Path("sample")
    proj_dir.mkdir()
    init_file = proj_dir / "__init__.py"
    init_file.write_text(F"__version__='{expected_version}'")
    args = f"install --no-build-isolation .[{expected_custom_depencency}]"
    run_pip(args)

    # TODO: validate that install worked correctly
    # TODO: test that optional dependencies are installed when requested
