buildbot-dzil-steps
===================

Buildbot build steps optimised for Perl's Dist::Zilla.

Usage
-----

Firstly, download or clone the code and put it somewhere near your buildmaster.

Then add the following (or similar):

    from dzil import DzilDependencies, DzilSmoke
    
    factory.addStep(DzilSmoke())

### DzilAuthorDependencies()

This will install/update the author dependecnies, by running `dzil authordeps | cpanm`.

It is a subclass of `ShellCommand`, and takes the same arguments.

### DzilDependencies()

This will install/update the distrbution dependecnies, by running `dzil listdeps | cpanm`.

It is a subclass of `ShellCommand`, and takes the same arguments.

### DzilSmoke()

This will run the `dzil smoke` command in the build directory. The output is then parsed to get the test results, which are then displayed in your waterfall.

It is a subclass of `Test`, and takes the same arguments.

### DzilSmokeVerbose()

Runs DzilSmoke() verbosely.

### DzilTest()

This is exactly the same as DzilSmoke(), but runs `dzil test`.


### DzilTestVerbose()

Runs DzilTest() verbosely.