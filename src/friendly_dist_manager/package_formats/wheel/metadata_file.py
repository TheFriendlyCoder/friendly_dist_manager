"""Primitives for manipulating distutils metadata files"""
from collections import namedtuple

Person = namedtuple("Person", ["name", "email"])
ProjectURL = namedtuple("ProjectURL", ["label", "url"])
ExtraRequirement = namedtuple("ExtraRequirement", ["label", "req"])


class MetadataFile:  # pylint: disable=too-many-instance-attributes
    """Abstraction around a distutils metadata file

    References:
        * (Latest Spec): https://packaging.python.org/specifications/core-metadata/
        * (v2.1 Proposed PEP) https://www.python.org/dev/peps/pep-0566/
        * (v1.2 Accepted PEP) https://www.python.org/dev/peps/pep-0345/
        * (V1.1 Accepted PEP) https://www.python.org/dev/peps/pep-0314/
        * (V1.0 Accepted PEP) https://www.python.org/dev/peps/pep-0241/
    """
    def __init__(self, dist_name, version):
        """
        Args:
            dist_name (str):
                Name of the distribution being described
            version (str):
                Version of the distribution being described
        """
        self._file_version = "2.2"
        self._dist_name = dist_name
        self._dist_version = version
        self._summary = None
        self._homepage = None
        self._authors = list()
        self._license = None
        self._keywords = list()
        self._classifiers = list()
        self._download_url = None
        self._maintainers = list()
        self._requirements = list()
        self._python_requirements = list()
        self._project_urls = list()
        self._extra_requirements = list()

    @property
    def file_version(self):
        """str: the metadata file version / schema version used by this file"""
        return self._file_version

    @property
    def distribution_name(self):
        """str: name of the distribution being built"""
        return self._dist_name

    @property
    def distribution_version(self):
        """str: version of the package being built"""
        return self._dist_version

    @property
    def summary(self):
        """str: description of the package"""
        return self._summary or ""

    @summary.setter
    def summary(self, value):
        self._summary = value

    @property
    def homepage(self):
        """str: URL of the project homepage"""
        return self._homepage or ""

    @homepage.setter
    def homepage(self, value):
        self._homepage = value

    @property
    def authors(self):
        """list (Person): authors of the project"""
        return self._authors

    @authors.setter
    def authors(self, value):
        self._authors = value

    @property
    def maintainers(self):
        """list (Person): maintainers of the project"""
        return self._maintainers

    @maintainers.setter
    def maintainers(self, value):
        self._maintainers = value

    @property
    def license(self):
        """str: text describing the licensing terms for the project"""
        return self._license or ""

    @license.setter
    def license(self, value):
        self._license = value

    @property
    def keywords(self):
        """list (str): labels users can search for when looking for distributions
        like this one"""
        return self._keywords

    @keywords.setter
    def keywords(self, value):
        self._keywords = value

    @property
    def classifiers(self):
        """list (str): list of distribution classifiers"""
        return self._classifiers

    @classifiers.setter
    def classifiers(self, value):
        self._classifiers = value

    @property
    def download_url(self):
        """str: URL where the distribution package can be downloaded"""
        return self._download_url or ""

    @download_url.setter
    def download_url(self, value):
        self._download_url = value

    @property
    def requirements(self):
        """list(str): package definitions describing other distributions this
        one depends on"""
        return self._requirements

    @requirements.setter
    def requirements(self, value):
        self._requirements = value

    @property
    def python_requirements(self):
        """list(str): Python version identifiers describing the supported Python
        runtime versions supported by this distribution package"""
        return self._python_requirements

    @python_requirements.setter
    def python_requirements(self, value):
        self._python_requirements = value

    @property
    def project_urls(self):
        """list (ProjectURL): Support URLs associated with the distribution"""
        return self._project_urls

    @project_urls.setter
    def project_urls(self, value):
        self._project_urls = value

    @property
    def extra_requirements(self):
        """list (ExtraRequirement): list of optional requirements that users of
        the distribution may select to enable additional features"""
        return self._extra_requirements

    @extra_requirements.setter
    def extra_requirements(self, value):
        self._extra_requirements = value

    @staticmethod
    def _encode_user(user_defs, user_key, email_key):
        """Helper method for encoding author and maintainer information in a format
        compatible with the metadata file format

        Args:
            user_defs (list (Person)):
                list of users to be encoded
            user_key (str):
                attribute key for the field to be populated with
                user information (ie: "Author" or "Maintainer")
            email_key (str):
                attribute key for the field to be populated with
                email contact information for the user data
                (ie: "Author-email" or "Maintainer-email")

        Returns:
            list (str):
                list of encoded user definitions for inclusion
                in the metadata output, each element representing
                a single line in the output file
        """
        retval = list()
        # according to the metadata spec, the Author field is intended to only
        # contain contact information for a single author, so we arbitrarily
        # select the first author with a name defined in our list of authors
        names = [usr.name for usr in user_defs if usr.name]
        if names:
            retval.append(f"{user_key}: {names[0]}")

        # For author emails, they may take the form of '"John Doe" <jdoe@company.com>'
        # if the author has a valid name defined, otherwise they will take the format
        # of 'jdoe@company.com'. Multiple emails are then separated by commas
        emails = list()
        for usr in user_defs:
            if not usr.email:
                continue
            if usr.name:
                emails.append(f'"{usr.name}" <{usr.email}>')
            else:
                emails.append(usr.email)
        if emails:
            retval.append(f"{email_key}: {','.join(emails)}")
        return retval

    @staticmethod
    def _encode_property(prop_key, prop_value):
        """Formats an optional attribute in a compatible way for storage
        in a metadata file

        Args:
            prop_key (str):
                the attribute key associated with the property to encode
            prop_value (str):
                value for the property to encode. May be empty or None if
                the property is not defined

        Returns:
            list (str):
                encoded representation of the specified property data in a
                format compatible with the metadata file format. May return
                an empty list if the provided property data was empty.
        """
        retval = list()
        if prop_value:
            retval.append(f"{prop_key}: {prop_value}")
        return retval

    @property
    def raw(self):
        """str: the raw text content of the metadata file"""
        lines = list()
        # Required fields
        lines.append(f"Metadata-Version: {self.file_version}")
        lines.append(f"Name: {self.distribution_name}")
        lines.append(f"Version: {self.distribution_version}")

        # Optional fields
        lines.extend(self._encode_user(self.authors, "Author", "Author-email"))
        lines.extend(self._encode_user(self.maintainers, "Maintainer", "Maintainer-email"))
        lines.extend(self._encode_property("Summary", self.summary))
        lines.extend(self._encode_property("Home-page", self.homepage))
        lines.extend(self._encode_property("License", self.license))
        lines.extend(self._encode_property("Keywords", ','.join(self.keywords)))
        lines.extend(self._encode_property("Download-url", self.download_url))

        for cur_proj_url in self.project_urls:
            if cur_proj_url.label:
                url_text = f"{cur_proj_url.label}, {cur_proj_url.url}"
            else:
                url_text = f"{cur_proj_url.url}"
            lines.append(f"Project-URL: {url_text}")
        for cur_classifier in self.classifiers:
            lines.append(f"Classifier: {cur_classifier}")
        for cur_req in self.python_requirements:
            lines.append(f"Requires-Python: {cur_req}")
        extras = set(extra.label for extra in self.extra_requirements)
        for cur_extra in extras:
            lines.append(f"Provides-Extra: {cur_extra}")
        for cur_extra in self.extra_requirements:
            lines.append(f"Requires-Dist: {cur_extra.req}; extra == '{cur_extra.label}'")
        for cur_req in self.requirements:
            lines.append(f"Requires-Dist: {cur_req}")

        return "\n".join(lines)
