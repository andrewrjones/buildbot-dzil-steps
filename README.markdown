buildbot-dzil-steps
===================

Buildbot build steps optimised for Perl's Dist::Zilla.

Currently only 'test' and 'smoke' are implemented.

Usage
-----

Firstly, download or clone the code and put it somewhere near your buildmaster.

Then add the following (or similar):

    from dzil import DzilSmoke

### DzilSmoke()

You can use this as follows:

    factory.addStep(DzilSmoke())

It will run the `dzil smoke` command in the build directory. The output is then parsed to get the test results, which are then displayed in your waterfall.

It is a subclass of `Test`, and takes the same arguments.

### DzilTest()

This is exactly the same as DzilSmoke(), but runs `dzil test`.

TODO
----
- Support dependency builds
