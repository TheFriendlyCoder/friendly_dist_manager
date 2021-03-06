import friendly_dist_manager as package


def test_version():
    assert hasattr(package, "__version__")
    ver = package.__version__
    assert isinstance(ver, str)
    parts = ver.split(".")
    assert len(parts) == 3
    for cur_part in parts:
        assert cur_part.isnumeric()