# Copyright (c) 2012, the Dart project authors.  Please see the AUTHORS file
# for details. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.

import cgi

from google.appengine.api import users
from google.appengine.ext import db

import models
from pubspec import Pubspec

class Package(db.Model):
    """The model for a package.

    A package contains only metadata that applies to every version of the
    package, such as its name and uploader. Each individual version of the
    package is represented by a PackageVersion model.
    """

    MAX_SIZE = 10 * 2**20 # 10MB
    """The maximum package size, in bytes."""

    # TODO(nweiz): This property is deprecated. "uploaders" should be used
    # instead.
    owner = db.UserProperty(auto_current_user_add=True)
    """The user who is allowed to upload new versions of the package."""

    # TODO(nweiz): This should have "validator=models.validate_not_empty" once
    # all packages have migrated to use uploaders rather than owner.
    uploaders = db.ListProperty(users.User)
    """The users who are allowed to upload new versions of the package."""

    name = db.StringProperty(required=True)
    """The name of the package."""

    created = db.DateTimeProperty(auto_now_add=True)
    """When the package was created."""

    downloads = db.IntegerProperty(required=True, default=0)
    """The number of times any version of this package has been downloaded."""

    # This should only reference a PackageVersion, but cyclic imports aren't
    # allowed so we can't import PackageVersion here.
    latest_version = db.ReferenceProperty()
    """The most recent non-prerelease version of this package."""

    @property
    def description(self):
        """The short description of the package."""
        if self.latest_version is None: return None
        return self.latest_version.pubspec.get('description')

    _MAX_DESCRIPTION_CHARS = 200

    @property
    def ellipsized_description(self):
        """The short description of the package, truncated if necessary."""
        description = self.description
        if description is None: return None
        return models.ellipsize(description, Package._MAX_DESCRIPTION_CHARS)

    @property
    def homepage(self):
        """The home page URL for the package, or None."""
        if self.latest_version is None: return None
        return self.latest_version.pubspec.get('homepage')

    @property
    def authors_title(self):
        """The title for the authors list of the package."""
        return 'Author' if len(self.latest_version.pubspec.authors) == 1 \
            else 'Authors'

    @property
    def authors_html(self):
        """Inline HTML for the authors of this package."""
        if self.latest_version is None: return ''

        def author_html((author, email)):
            if email is None: return cgi.escape(author)
            return '''<span class="author">%s
                <a href="mailto:%s" title="Email %s">
                    <i class="icon-envelope">Email %s</i>
                </a></span>''' % \
                (cgi.escape(author), cgi.escape(email), cgi.escape(email),
                 cgi.escape(email))

        return ', '.join(map(author_html, self.latest_version.pubspec.authors))

    @property
    def uploaders_title(self):
        """The title for the uploaders list of the package."""
        return 'Uploader' if len(self.latest_version.pubspec.authors) == 1 \
            else 'Uploaders'

    @property
    def uploaders_html(self):
        """Inline HTML for the uploaders of this package."""
        return ', '.join(cgi.escape(uploader.nickname())
                         for uploader in self.uploaders)

    @property
    def short_updated(self):
        """The short updated time of the package."""
        return self.updated.strftime('%b %d, %Y')

    @classmethod
    def new(cls, **kwargs):
        """Construct a new package.

        Unlike __init__, this infers some properties from others. In particular:

        - The key name is inferred from the package name.
        """

        if not 'key_name' in kwargs and not 'key' in kwargs:
            kwargs['key_name'] = kwargs['name']

        return cls(**kwargs)

    @db.ComputedProperty
    def updated(self):
        """When the latest version of this package was uploaded.

        This only counts latest_version; pre-release versions and older versions
        will not affect this field."""
        return self.latest_version and self.latest_version.created

    @classmethod
    def exists(cls, name):
        """Determine whether a package with the given name exists."""
        return cls.get_by_key_name(name) is not None

    def has_version(self, version):
        """Determine whether this package has a given version uploaded."""
        from package_version import PackageVersion
        version = PackageVersion.get_by_name_and_version(
            self.name, str(version))
        return version is not None
