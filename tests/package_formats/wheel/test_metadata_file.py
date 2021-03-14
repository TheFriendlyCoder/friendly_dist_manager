from friendly_dist_manager.package_formats.wheel.metadata_file import MetadataFile, Person


def test_properties():
    expected_name = "MyPackage"
    expected_ver = "1.2.3dev"
    obj = MetadataFile(expected_name, expected_ver)
    # Required parameters
    assert obj.file_version == "2.2"
    assert obj.distribution_name == expected_name
    assert obj.distribution_version == expected_ver

    # Default values
    assert isinstance(obj.project_urls, list)
    assert len(obj.project_urls) == 0
    assert obj.download_url == ""
    assert isinstance(obj.extra_requirements, list)
    assert len(obj.extra_requirements) == 0
    assert isinstance(obj.python_requirements, list)
    assert len(obj.python_requirements) == 0
    assert isinstance(obj.requirements, list)
    assert len(obj.requirements) == 0
    assert isinstance(obj.keywords, list)
    assert len(obj.keywords) == 0
    assert obj.license == ""
    assert obj.homepage == ""
    assert obj.summary == ""
    assert isinstance(obj.authors, list)
    assert len(obj.authors) == 0
    assert isinstance(obj.maintainers, list)
    assert len(obj.maintainers) == 0
    assert isinstance(obj.classifiers, list)
    assert len(obj.classifiers) == 0


def test_author_email_only():
    obj = MetadataFile("MyPackage", "1.2.3")
    expected_email = "jdoe@company.com"
    obj.authors.append(Person(None, expected_email))

    assert "Author:" not in obj.raw
    assert f"Author-email: {expected_email}" in obj.raw


def test_author_name_only():
    obj = MetadataFile("MyPackage", "1.2.3")
    expected_name = "John Doe"
    obj.authors.append(Person(expected_name, None))

    assert f"Author: {expected_name}" in obj.raw
    assert "Author-email:" not in obj.raw


def test_author_name_and_email():
    obj = MetadataFile("MyPackage", "1.2.3")
    expected_email = "jdoe@company.com"
    expected_name = "John Doe"
    obj.authors.append(Person(expected_name, expected_email))

    assert f"Author: {expected_name}" in obj.raw
    assert f'Author-email: "{expected_name}" <{expected_email}>' in obj.raw
