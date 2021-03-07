import logging
from .utils import log_dir, temp_dir, test_id, cd, test_env
import pytest
import shutil


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= FIXTURES
@pytest.fixture(scope="session", autouse=True)
def clean_logs():
    """Fixture that deletes logs from previous test runs"""
    shutil.rmtree(log_dir())


@pytest.fixture(scope="function", autouse=True)
def config_logger(request):
    """Fixture that configures a custom logger for recording test output

    Args:
        request(pytest.fixtures.SubRequest):
            metadata associated with currently running test
    """
    global_log = logging.getLogger()
    global_log.setLevel(logging.DEBUG)

    verbose_format = "%(asctime)s(%(levelname)s->%(name)s:%(funcName)s):%(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    fmt = logging.Formatter(verbose_format, date_format)

    log_file = log_dir() / f"{test_id(request)}.log"
    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    global_log.addHandler(file_handler)


@pytest.fixture(scope="function", autouse=True)
def isolated_environment(request, tmp_path):
    """Fixture that sets up a clean, isolated environment for each test

    Args:
        request (pytest.fixtures.SubRequest):
            metadata associated with currently running test
        tmp_path (Path):
            temporary folder customized for the current test as
            generated by pytest
    """
    preserve = request.config.option.preserve
    if preserve:
        # If we've been asked to preserve unit test output, create a
        # temporary folder in the local workspace to make it easier to
        # locate and review the test data
        work_dir = temp_dir() / test_id(request)
        if work_dir.exists():
            shutil.rmtree(work_dir)
        work_dir.mkdir(parents=True)
    else:
        # If we are not asked to preserve unit test data then use the
        # autogenerated temp folder provided by pytest
        work_dir = tmp_path

    # Set some custom environment variables to control the test behavior
    # See the _config_logger() helper method in the main __init__.py of
    # the friendly_dist_manager package for details
    new_vars = dict()
    new_vars["TFC_LOG_FILE"] = str(log_dir() / f"{test_id(request)}.log")
    new_vars["TFC_LOG_LEVEL"] = logging.getLevelName(logging.DEBUG)
    if preserve:
        new_vars["TFC_TEMP_DIR"] = str(work_dir)

    # change the current working folder to our temp folder before
    # returning control back to the unit test
    with cd(work_dir):
        # Set up some custom environment variables to control the
        # behavior of the package manager
        with test_env(new_vars):
            yield

    # Once the test execution is complete, see if we've been asked
    # to preserve test output. If so, don't bother with cleanup
    if preserve:
        return

    # purge temporary folder unless instructed otherwise
    if work_dir.exists():
        shutil.rmtree(work_dir)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= PYTEST CONFIGURATION
def pytest_addoption(parser):
    parser.addoption("--preserve", action="store_true",
                     help="preserve data generate by tests")
