from contextlib import contextmanager
from pathlib import Path
from os import chdir, environ
import subprocess
import sys
import shlex
import logging

TEST_DIR = Path(__file__).parent
WORKSPACE_DIR = TEST_DIR.parent


@contextmanager
def cd(new_path):
    """Changes working folder for the duration of a test

    When this context manager goes out of scope the original
    working folder will be restored

    Args:
        new_path (Path):
            folder to change the current working directory to
    """
    old_dir = Path.cwd()
    try:
        chdir(new_path)
        yield
    finally:
        chdir(old_dir)


def log_dir():
    """Path: gets path to the unit test log folder"""
    retval = WORKSPACE_DIR / "logs"
    if not retval.exists():
        retval.mkdir()
    return retval


def temp_dir():
    """Path: Helper that creates a temporary folder to run a test within"""
    retval = WORKSPACE_DIR / "temp"
    if not retval.exists():
        retval.mkdir()
    return retval


def test_id(request):
    """Generates a unique identifier for a test.

    Used for marking up logs and workspaces used by a test
    so the generated artifacts can be isolated from other tests

    Args:
        request (pytest.fixture.SubRequest):
            metadata describing the currently running tests

    Returns:
        str:
            unique ID for the specified test
    """
    test_prefix = ".".join(request.module.__name__.split(".")[1:])
    return f"{test_prefix}.{request.node.name}"


@contextmanager
def test_env(new_vars):
    """Injects custom environment variables into the test environment

    If env vars with the same names as those provided already exist in
    the environment, they will be restored to their original values
    once the context manager goes out of scope

    Args:
        new_vars (dict):
            mapping of environment variables to their values
    """
    old_vars = dict()
    for var_name, var_val in new_vars.items():
        # Preserve values for any env vars that already exist
        # so they can be restored after the test finishes
        # NOTE: we store 'None' for any env var that didn't
        # previously exist so we can delete those vars after
        # the test finishes, ensuring we leave the environment
        # clean for the next test
        old_vars[var_name] = environ.get(var_name)
        environ[var_name] = var_val

    try:
        # Return control back to the caller
        yield
    finally:
        # Once the context manager goes out of scope, restore
        # the environment back to what it was prior to the test
        for var_name, var_val in old_vars.items():
            if var_val:
                # Restore the value for variables that were defined
                # prior to running the test
                environ[var_name] = var_val
            else:
                # Remove any env vars that were unique just for this
                # test run
                del environ[var_name]


def run_pip(options):
    """Executes a 'pip' operation within the test environment

    Args:
        options(str):
            command line options to pass to pip
    """
    args = shlex.split(f"{sys.executable} -m pip {options}")
    results = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    log = logging.getLogger(__name__)
    log.debug(results.stdout)
    if results.stderr:
        log.error(results.stderr)
    results.check_returncode()
