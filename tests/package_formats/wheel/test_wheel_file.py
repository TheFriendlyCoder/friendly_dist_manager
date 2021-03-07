import zipfile
from pathlib import Path
from tests.utils import run_pip
from friendly_dist_manager.package_formats.wheel.wheel_file import WheelFile
import pytest


def test_properties():
    dist_name = "MyDist"
    dist_ver = "1.2.3"
    obj = WheelFile(dist_name, dist_ver)
    assert dist_name in obj.filename
    assert dist_ver in obj.filename
    assert obj.filename.endswith(".whl")


def test_build_overwrite():
    dist_name = "MyDist"
    dist_ver = "1.2.3"
    obj = WheelFile(dist_name, dist_ver)
    # Create a file in the current folder with the same name
    # as our output file
    Path(obj.filename).touch()

    # This should result in a build failure
    with pytest.raises(FileExistsError):
        obj.build(Path())


def test_build_empty_package():
    dist_name = "MyDist"
    dist_ver = "1.2.3"
    obj = WheelFile(dist_name, dist_ver)
    obj.build(Path())
    res = list(Path().glob("*.whl"))
    assert len(res) == 1
    with zipfile.ZipFile(res[0], mode="r", compression=zipfile.ZIP_DEFLATED) as zf:
        assert f"{dist_name}-{dist_ver}.dist-info/METADATA" in zf.namelist()
        assert f"{dist_name}-{dist_ver}.dist-info/RECORD" in zf.namelist()
        assert f"{dist_name}-{dist_ver}.dist-info/WHEEL" in zf.namelist()


def test_add_file_to_build():
    dist_name = "MyDist"
    dist_ver = "1.2.3"
    obj = WheelFile(dist_name, dist_ver)

    ver_file = Path("version.py")
    ver_file.touch()
    obj.add_file(ver_file, Path(""))

    obj.build(Path())
    res = list(Path().glob("*.whl"))
    assert len(res) == 1
    with zipfile.ZipFile(res[0], mode="r", compression=zipfile.ZIP_DEFLATED) as zf:
        assert f"{ver_file}" in zf.namelist()


def test_pip_empty_package():
    dist_name = "MyDist"
    dist_ver = "1.2.3"
    obj = WheelFile(dist_name, dist_ver)
    obj.build(Path())
    wf = next(Path().glob("*.whl"))
    args = f"install --no-build-isolation ./{wf}"
    run_pip(args)
