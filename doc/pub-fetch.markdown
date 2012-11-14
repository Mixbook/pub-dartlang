---
title: "Command: Fetch"
---

    $ pub fetch

This command installs all the dependencies listed in the
[`pubspec.yaml`](pubspec.html) file in the current working directory, as well as
their [transitive dependencies](glossary.html#transitive-dependency), to a
`packages` directory located next to the pubspec. For example:

    $ pub fetch
    Dependencies installed!

Once the dependencies are fetched, they may be referenced in Dart code. For
example, if a package depends on `unittest`:

{% highlight dart %}
import "package:unittest/unittest.dart;
{% endhighlight %}

When `pub fetch` fetches new dependencies, it writes a
[pin file](glossary.html#pin-file) to ensure that future fetches will use the
same versions of those dependencies. Application packages should check in the
pin file to source control; this ensures the application will use the exact same
versions of all dependencies for all developers and when deployed to production.
Library packages should not check in the pin file, though, since they're
expected to work with a range of dependency versions.

If a pin file already exists, `pub fetch` uses the versions of dependencies
pinned in it if possible. If a dependency isn't pinned, pub will fetch the
latest version of that dependency that satisfies all the [version
constraints](glossary.html#version-constraint). This is the primary difference
between `pub fetch` and [`pub upgrade`](pub-upgrade.html), which always tries
to use the latest versions of all dependencies.

## Fetching a new dependency

If a dependency is added to the pubspec and then `pub fetch` is run, it will
fetch the new dependency and any of its transitive dependencies and place them
in the `packages` directory. However, it won't change the versions of any
already-fetched dependencies unless that's necessary to use the new dependency.

## Removing a dependency

If a dependency is removed from the pubspec and then `pub fetch` is run, it
will remove the dependency from the `packages` directory, thus making it
unavailable for importing. Any transitive dependencies of the removed dependency
will also be removed, as long as no remaining immediate dependencies also depend
on them. Removing a dependency will never change the versions of any
already-installed dependencies.

## Linked `packages` directories

Every [entrypoint](glossary.html#entrypoint) in a package needs to be next to a
`packages` directory in order for it to import packages installed by Pub.
However, it's not convenient to put every entrypoint at the top level of the
package alongside the main `packages` directory. You may have example scripts or
tests that you want to be able to run from subdirectories.

`pub fetch` solves this issue by creating additional `packages` directories
that link to the main `packages` directory at the root of your package. It
assumes your package is laid out according to the [package layout
guide](package-layout.html), and creates a linked `packages` directory in
`bin/`, `test/`, and `example/`, as well as their subdirectories.

## The system package cache

Dependencies are not stored directly in the `packages` directory when they're
fetched. Dependencies downloaded over the internet, such as those from Git and
[pub.dartlang.org](http://pub.dartlang.org), are stored in a
[system-wide cache](glossary.html#system-cache) and linked to from the
`packages` directory. This means that if multiple packages use the same version
of the same dependency, it will only need to be downloaded and stored locally
once. It also means that it's safe to delete the `packages` directory without
worrying about re-downloading packages.
