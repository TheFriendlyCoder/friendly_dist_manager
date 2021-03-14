import pytest
from pathlib import Path
from friendly_dist_manager.pyproject.parser import PyProjectParser

DEFAULT_BACKEND = "friendly_dist_manager.hooks:PEP517"


def test_minimal_config():
    expected_name = "FuBar"
    expected_version = "4.5.6"

    sample_toml = f"""
        [build-system]
        requires = ['wheel', 'setuptools']
        build-backend = "{DEFAULT_BACKEND}"
        
        [project]
        name = "{expected_name}"
        version = "{expected_version}"
    """
    obj = PyProjectParser(sample_toml)
    assert obj.build_system.backend == DEFAULT_BACKEND
    assert len(obj.build_system.requirements) == 2
    assert "wheel" in obj.build_system.requirements
    assert "setuptools" in obj.build_system.requirements
    assert obj.project.version == expected_version
    assert obj.project.name == expected_name

    assert obj.project.description == ""
    assert obj.project.readme_file is None
    assert obj.project.readme == ""
    assert obj.project.python_requirement == ""
    assert obj.project.license == ""
    assert isinstance(obj.project.authors, list)
    assert len(obj.project.authors) == 0
    assert isinstance(obj.project.maintainers, list)
    assert len(obj.project.maintainers) == 0
    assert isinstance(obj.project.keywords, list)
    assert len(obj.project.keywords) == 0
    assert isinstance(obj.project.classifiers, list)
    assert len(obj.project.classifiers) == 0
    assert isinstance(obj.project.urls, list)
    assert len(obj.project.urls) == 0
    assert isinstance(obj.project.console_scripts, list)
    assert len(obj.project.console_scripts) == 0
    assert isinstance(obj.project.gui_scripts, list)
    assert len(obj.project.gui_scripts) == 0
    assert isinstance(obj.project.entrypoint_identifiers, list)
    assert len(obj.project.entrypoint_identifiers) == 0
    assert isinstance(obj.project.dependencies, list)
    assert len(obj.project.dependencies) == 0
    assert isinstance(obj.project.optional_dependency_identifiers, list)
    assert len(obj.project.optional_dependency_identifiers) == 0


def test_load_from_disk():
    sample_toml = f"""
        [build-system]
        requires = ['wheel', 'setuptools']
        build-backend = "{DEFAULT_BACKEND}"
    """
    toml_file = Path("pyproject.toml")
    toml_file.write_text(sample_toml)
    obj = PyProjectParser.from_file(toml_file)
    assert obj.build_system.backend == DEFAULT_BACKEND
    assert len(obj.build_system.requirements) == 2
    assert "wheel" in obj.build_system.requirements
    assert "setuptools" in obj.build_system.requirements


def test_properties():
    expected_name = "FuBar"
    expected_version = "4.5.6"
    expected_desc = "My Cool Library"
    expected_readme = "My readme for my super cool library"
    Path("README.rst").write_text(expected_readme)
    expected_python = "python>=3.6"
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
        
        [project.scripts]
        "{expected_console_script}" = "{expected_ref1}"
        
        [project.gui-scripts]
        "{expected_gui_script}" = "{expected_ref2}"
        
        [project.entry-point.{expected_custom_entrypoint}]
        "{expected_custom_script}" = "{expected_ref3}"
        
    """
    obj = PyProjectParser(sample_toml)
    assert obj.build_system.backend == DEFAULT_BACKEND
    assert len(obj.build_system.requirements) == 2
    assert "wheel" in obj.build_system.requirements
    assert "setuptools" in obj.build_system.requirements
    assert obj.project.version == expected_version
    assert obj.project.name == expected_name

    assert obj.project.description == expected_desc
    assert isinstance(obj.project.readme_file, Path)
    assert obj.project.readme_file.stem == "README"
    assert obj.project.readme == expected_readme
    assert obj.project.python_requirement == expected_python
    assert obj.project.license == expected_license
    assert isinstance(obj.project.authors, list)
    assert len(obj.project.authors) == 1
    assert obj.project.authors[0].name == expected_author_name
    assert obj.project.authors[0].email == expected_author_email
    assert isinstance(obj.project.maintainers, list)
    assert len(obj.project.maintainers) == 1
    assert obj.project.maintainers[0].name == expected_maintainer_name
    assert obj.project.maintainers[0].email == expected_maintainer_email
    assert isinstance(obj.project.keywords, list)
    assert len(obj.project.keywords) == len(set(obj.project.keywords))  # make sure there are no duplicates
    assert len(obj.project.keywords) == len(expected_keywords)
    assert all([i in expected_keywords for i in obj.project.keywords])
    assert isinstance(obj.project.classifiers, list)
    assert len(obj.project.classifiers) == len(set(obj.project.classifiers))
    assert len(obj.project.classifiers) == len(expected_classifiers)
    assert all([i in expected_classifiers for i in obj.project.classifiers])
    urls = obj.project.urls
    assert isinstance(urls, list)
    assert len(urls) == 1
    assert urls[0].label == "homepage"
    assert urls[0].url == expected_homepage
    assert isinstance(obj.project.console_scripts, list)
    assert len(obj.project.console_scripts) == 1
    assert obj.project.console_scripts[0].name == expected_console_script
    assert obj.project.console_scripts[0].ref == expected_ref1
    assert isinstance(obj.project.gui_scripts, list)
    assert len(obj.project.gui_scripts) == 1
    assert obj.project.gui_scripts[0].name == expected_gui_script
    assert obj.project.gui_scripts[0].ref == expected_ref2
    assert isinstance(obj.project.entrypoint_identifiers, list)
    assert len(obj.project.entrypoint_identifiers) == 1
    assert obj.project.entrypoint_identifiers[0] == expected_custom_entrypoint
    ep = obj.project.get_entrypoint(expected_custom_entrypoint)
    assert isinstance(ep, list)
    assert len(ep) == 1
    assert ep[0].name == expected_custom_script
    assert ep[0].ref == expected_ref3
    assert isinstance(obj.project.dependencies, list)
    assert len(obj.project.dependencies) == 1
    assert obj.project.dependencies[0] == expected_dependency
    assert isinstance(obj.project.optional_dependency_identifiers, list)
    assert len(obj.project.optional_dependency_identifiers) == 1
    assert obj.project.optional_dependency_identifiers[0] == expected_custom_depencency
    dep = obj.project.get_optional_dependencies(expected_custom_depencency)
    assert isinstance(dep, list)
    assert len(dep) == 1
    assert dep[0] == expected_dev_dependency


def test_readme_not_exists():
    expected_name = "FuBar"
    expected_version = "4.5.6"

    sample_toml = f"""
        [build-system]
        requires = ['wheel', 'setuptools']
        build-backend = "{DEFAULT_BACKEND}"

        [project]
        name = "{expected_name}"
        version = "{expected_version}"
        readme = "README.rst"
    """
    obj = PyProjectParser(sample_toml)
    with pytest.raises(FileNotFoundError):
        obj.project.readme


def test_file_based_license():
    expected_name = "FuBar"
    expected_version = "4.5.6"
    expected_license = "My license is like BSD but not"
    Path("license.txt").write_text(expected_license)
    sample_toml = f"""
        [build-system]
        requires = ['wheel', 'setuptools']
        build-backend = "{DEFAULT_BACKEND}"

        [project]
        name = "{expected_name}"
        version = "{expected_version}"
        license = {{"file" = "license.txt"}}
    """
    obj = PyProjectParser(sample_toml)
    assert obj.project.license == expected_license


def test_license_file_not_found():
    expected_name = "FuBar"
    expected_version = "4.5.6"

    sample_toml = f"""
        [build-system]
        requires = ['wheel', 'setuptools']
        build-backend = "{DEFAULT_BACKEND}"

        [project]
        name = "{expected_name}"
        version = "{expected_version}"
        license = {{"file" = "license.txt"}}
    """
    obj = PyProjectParser(sample_toml)
    with pytest.raises(FileNotFoundError):
        obj.project.license
