"""Primitives for manipulating Python wheel files"""
import zipfile
import hashlib
from pathlib import Path
import shutil
from base64 import urlsafe_b64encode
from textwrap import dedent
import tempfile
from os import environ
from friendly_dist_manager import __version__


class WheelFile:  # pylint: disable=too-many-instance-attributes
    """Abstraction around a Python wheel file

    References:
        * (Latest Spec) https://packaging.python.org/specifications/binary-distribution-format/
        * (Accepted PEP) https://www.python.org/dev/peps/pep-0427/
        * (Proposed PEP) https://www.python.org/dev/peps/pep-0491/
    """
    def __init__(self, dist_name, version):
        self._file_version = "1.0"
        self._dist_name = dist_name
        self._dist_version = version
        self._python_tag = "py3"
        self._abi_tag = "none"
        self._platform_tag = "any"
        self._build_tag = None
        self._temp_dir_cache = tempfile.TemporaryDirectory()

    @property
    def _temp_dir(self):
        """pathlib.Path: Gets a reference to the temporary folder where this object
        stores package data for building"""
        if "TFC_TEMP_DIR" not in environ:
            return Path(self._temp_dir_cache.name)

        retval = Path(environ["TFC_TEMP_DIR"])  # pragma: no cover
        if not retval.exists():  # pragma: no cover
            retval.mkdir()
        return retval  # pragma: no cover

    @property
    def filename(self):
        """str: gets the fully qualified file name of the wheel file to be generated"""
        if self._build_tag:
            return f"{self._dist_name}-{self._dist_version}-{self._build_tag}-{self._python_tag}-" \
                   f"{self._abi_tag}-{self._platform_tag}.whl"

        return f"{self._dist_name}-{self._dist_version}-{self._python_tag}-" \
               f"{self._abi_tag}-{self._platform_tag}.whl"

    def add_file(self, src_file, target_path):
        """Adds a new file to the package

        Args:
            src_file (pathlib.Path):
                reference to the source file to be packaged
            target_path (pathlib.Path):
                location, relative to the root of the wheel
                file, where this new file should be deployed
        """
        temp = self._temp_dir / target_path
        if not temp.exists():
            temp.mkdir(parents=True)
        shutil.copy(src_file, temp)

    @staticmethod
    def _sha_256(src_file):
        """Calculates the SHA256 checksum for a file

        Args:
            src_file (pathlib.Path):
                reference to the source file to process

        Returns:
            str:
                b64 encoded SHA256 hash of the file, in UTF-8 format
                suitable for writing to disk in certain metadata files
        """
        retval = hashlib.sha256()
        with src_file.open("rb") as src:
            buffer = src.read(1024 * 8)
            while buffer:
                retval.update(buffer)
                buffer = src.read(1024 * 8)

        return urlsafe_b64encode(retval.digest()).decode("utf-8").rstrip("=")

    @staticmethod
    def _clean_data(data):
        """Cleans text data before writing to a metadata file

        * Removes blank lines
        * left-justifies all data blocks

        Args:
            data (str):
                raw character string data to be written to disk

        Returns:
            str:
                cleaned and processed text data that is safe to write to disk
        """
        return dedent("\n".join(line for line in data.split("\n") if line))

    def _make_dist_info(self):
        """Constructs the dist-info folder for the wheel file"""
        info_dir = self._temp_dir / f"{self._dist_name}-{self._dist_version}.dist-info"
        wheel_file = info_dir / "WHEEL"
        meta_file = info_dir / "METADATA"
        record_file = info_dir / "RECORD"

        info_dir.mkdir(parents=True)

        dist_name = __name__.split(".")[0]
        wheel_data = f"""
            Wheel-Version: {self._file_version}
            Generator: {dist_name} ({__version__})
            Root-Is-Purelib: true
            Tag: {self._python_tag}-{self._abi_tag}-{self._platform_tag}
        """

        wheel_file.write_text(self._clean_data(wheel_data))

        meta_data = f"""
            Metadata-Version: 2.1
            Name: {self._dist_name}
            Version: {self._dist_version}
            Summary: UNKNOWN
            Home-page: UNKNOWN
            Author: UNKNOWN
            Author-email: UNKNOWN
            License: UNKNOWN
            Platform: UNKNOWN
        """
        meta_file.write_text(self._clean_data(meta_data))

        record_data = ""
        for cur_file in self._temp_dir.glob("**/*"):
            if cur_file.is_dir():
                continue

            record_data += f"{cur_file.relative_to(self._temp_dir)}," \
                           f"sha256={self._sha_256(cur_file)}," \
                           f"{cur_file.stat().st_size}\n"

        # We have to include the RECORD file itself in the index but
        # we need to exclude the hash and size fields
        record_data += f"{record_file.relative_to(self._temp_dir)},,\n"
        record_file.write_text(record_data)

    def build(self, output_path):
        """Constructs a wheel file from the metadata stored in this class

        Args:
            output_path (pathlib.Path):
                folder where the wheel file should be generated

        Returns:
            pathlib.Path:
                Reference to the newly generated wheel file
        """
        output_file = output_path / self.filename
        if output_file.exists():
            raise FileExistsError(f"File already exists: {output_file}")

        self._make_dist_info()
        with zipfile.ZipFile(output_file, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            for cur_file in self._temp_dir.glob("**/*"):
                if cur_file.is_dir():
                    continue
                rel_path = cur_file.relative_to(self._temp_dir)
                zinfo = zipfile.ZipInfo(str(rel_path))
                with cur_file.open("rb") as src:
                    zip_file.writestr(zinfo, src.read(), compress_type=zipfile.ZIP_DEFLATED)
        return output_file
