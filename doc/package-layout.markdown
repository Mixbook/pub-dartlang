---
title: "Pub: Package layout conventions"
---

# {{ page.title }}

Part of a healthy code ecosystem is consistent conventions. When we all do the
same thing the same way, it makes it easier for us to learn our way around
each other's work. It also makes it easier to write tools that can automatically
do stuff for us.

When you build a Pub package, we have a set of conventions we encourage you to
follow. They describe how you organize the files and directories within your
package, and how to name things. You don't have to have every single thing
these guidelines specify. If your package doesn't have binaries, it doesn't
need a directory for them. But if it does, you'll make everyone's life easier
if you call it `bin`.

To give you a picture of the whole enchilada, here's what a complete package
(conveniently named `enchilada`) that uses every corner of these guidelines
would look like:

    enchilada/
      pubspec.yaml
      pubspec.lock *
      README.md
      LICENSE
      enchilada.dart
      tortilla.dart
      bin/
        enchilada
        packages/ **
      doc/
        getting_started.md
      example/
        lunch.dart
        packages/ **
      lib/
        beans.dart
        queso.dart
      packages/ **
      test/
        enchilada_test.dart
        tortilla_test.dart
        packages/ **

\* The `pubspec.lock` will only be in source control if the package is an
application package.

\** The `packages` directories will exist locally after you're run
`pub install`, but won't be checked into source control.

## The basics

    enchilada/
      pubspec.yaml
      pubspec.lock

Every package will have a [**pubspec**](pubspec.html), a file named
`pubspec.yaml`, in the root directory of the package. That's what *makes* it a
package.

Once you've run [`pub install`](pub-install.html) or
[`pub update`](pub-update.html) on the package, you will also have a
**lockfile**, named `pubspec.lock`. If your package is an application package,
this will be checked into source control. Otherwise, it won't be.

    enchilada/
      packages/
        ...

Running pub will also generate a `packages` directory. You will *not* check
this into source control, and you won't need to worry too much about its
contents. Consider it pub magic, but not scary magic.

    enchilada/
      README.md

The open source community has a few other files that commonly appear at the top
level of a project: `README`, `LICENSE`, `AUTHORS`, etc. If you use any of
those, they can go in the top level of the package too. The specific ones you
use are up to you, but please do have a README.

## Public libraries

    enchilada/
      enchilada.dart
      tortilla.dart

Many packages are *library packages*: they define Dart libraries that other
packages can import and use. These public Dart library files go directly in the
top level directory for the package.

Most packages will define a single library that users can import. In that case,
its name should usually be the same as the name of the package, like
`enchilada.dart` in the example here. But you can also define other libraries
with whatever names make sense for your package.

When you do, users can import these libraries using the name of the package and
the library file, like so:

{% highlight dart %}
#import("package:enchilada/enchilada.dart");
#import("package:enchilada/tortilla.dart");
{% endhighlight %}

## Implementation files

    enchilada/
      lib/
        beans.dart
        queso.dart

The top level of a package contains files that are "publicly" visible: other
packages are free to import them. But much of a package's code is internal
implementation libraries that should only be imported and used by the package
itself. Those go inside a directory called `lib`. You can create subdirectories
in there if it helps you organize things.

Other Dart files within this package (like top-level ones, scripts in `bin`,
and tests) can import stuff from `lib`, but nothing outside the package should.

<!-- TODO(rnystrom): Re-enable this when #4820 is fixed.
For files within the package, they can still use `"package:"` to import these
libraries. This is a perfectly valid way to get to files in your *own* package:

{% highlight dart %}
#import("package:enchilada/lib/beans.dart");
{% endhighlight %}
-->

## Tests

    enchilada/
      test/
        enchilada_test.dart
        tortilla_test.dart

Every self-respecting package should have tests. With pub, the convention is
that these go in a `test` directory (or some directory inside it if you like)
and have `_test` at the end of their file names.

Typically, these use the [unittest](http://api.dartlang.org/unittest.html)
package but you can use whatever testing system that gets you excited.

## Documentation

    enchilada/
      doc/
        getting_started.md

If you've got code and tests, the next piece you need to maximize your karma
is good documentation. That goes inside a directory named `doc`.

We don't currently have any guidelines about format or organization within that.
Use whatever markup format you like and be happy that you're actually writing
docs.

## Examples

    enchilada/
      example/
        lunch.dart

At this point, you're going for the brass ring. Code, tests, docs, what else
could your users want? Standalone example programs that use your package, of
course! Those go inside the `example` directory. If the examples are complex
and use multiple files, consider making a directory for each example. Otherwise,
you can place each one right inside `example`.

This is an important place to consider using `package:` to import files from
your own package. That ensures the example code in your package looks exactly
like code outside of your package would look.

## Shell scripts

    enchilada/
      bin/
        enchilada

Some packages define shell scripts, programs that can be run directly from the
command line. These can be scripts written in an actual shell language, or any
other scripting language, including Dart. The `pub` application itself is one
example: it's a simple shell script that invokes `pub.dart`.

If your package defines stuff like this, put it in a directory named `bin`.

<aside class="alert alert-note">

At some point, pub will support automatically adding that directory to your
system path so that these scripts can be easily invoked.

</aside>
