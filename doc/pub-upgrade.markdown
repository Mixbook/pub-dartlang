---
title: "Command: Upgrade"
---

    $ pub upgrade [PACKAGE]

Without any additional arguments, `pub upgrade` installs the latest versions of
all the dependencies listed in the [`pubspec.yaml`](pubspec.html) file in the
current working directory, as well as their [transitive
dependencies](glossary.html#transitive-dependencies), to the `packages`
directory located next to the pubspec. For example:

    $ pub upgrade
    Dependencies upgraded!

When `pub upgrade` updates dependency versions, it writes a
[pinned versions file](glossary.html#pin-file) to ensure that future [`pub
fetch`es](pub-fetch.html) will use the same versions of those dependencies.
Application packages should check in the pin file to source control; this
ensures the application will use the exact same versions of all dependencies for
all developers and when deployed to production. Library packages should not
check in the pin file, though, since they're expected to work with a range of
dependency versions.

If a pin file already exists, `pub upgrade` will ignore it and generate a new
one from scratch using the latest versions of all dependencies. This is the
primary difference between `pub upgrade` and `pub fetch`, which always tries
to install the dependency versions specified in the existing pin file.

## Updating specific dependencies

It's possible to tell `pub upgrade` to update specific dependencies to the
latest version while leaving the rest of the dependencies alone as much as
possible. For example:

    $ pub upgrade unittest args
    Dependencies upgraded!

Upgrading a dependency upgrades its transitive dependencies to their latest
versions as well. Usually, no other dependencies are upgraded; they stay at the
versions that are pinned in the pin file. However, if the requested upgrades
cause incompatibilities with these pinned versions, they will be selectively
unpinned until a compatible set of versions is found.

## Adding a new dependency

If a dependency is added to the pubspec before `pub upgrade` is run, it will
install the new dependency and any of its transitive dependencies to the
`packages` directory. This is the same behavior as `pub fetch`.

## Removing a dependency

If a dependency is removed from the pubspec before `pub upgrade` is run, it
will remove the dependency from the `packages` directory, thus making it
unavailable for importing. Any transitive dependencies of the removed dependency
will also be removed, as long as no remaining immediate dependencies also depend
on them. This is the same behavior as `pub fetch`.
