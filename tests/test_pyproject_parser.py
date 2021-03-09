from pathlib import Path
from friendly_dist_manager.pyproject_parser import PyProjectParser

DEFAULT_BACKEND = "friendly_dist_manager.hooks:PEP517"


def test_properties():
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
    assert obj.build_backend == DEFAULT_BACKEND
    assert len(obj.build_requirements) == 2
    assert "wheel" in obj.build_requirements
    assert "setuptools" in obj.build_requirements
    assert expected_version == obj.project_version
    assert expected_name == obj.project_name


def test_load_from_disk():
    sample_toml = f"""
        [build-system]
        requires = ['wheel', 'setuptools']
        build-backend = "{DEFAULT_BACKEND}"
    """
    toml_file = Path("pyproject.toml")
    toml_file.write_text(sample_toml)
    obj = PyProjectParser.from_file(toml_file)
    assert obj.build_backend == DEFAULT_BACKEND
    assert len(obj.build_requirements) == 2
    assert "wheel" in obj.build_requirements
    assert "setuptools" in obj.build_requirements