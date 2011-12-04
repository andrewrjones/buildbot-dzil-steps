import dzil

from twisted.trial import unittest
from buildbot.status.results import SKIPPED, SUCCESS, WARNINGS, FAILURE
from buildbot.test.util import steps, compat

class FakeLogFile:
    def __init__(self, text):
        self.text = text

    def getText(self):
        return self.text

class FakeCmd:
    def __init__(self, stdout, stderr, rc=0):
        self.logs = {'stdout': FakeLogFile(stdout),
                     'stderr': FakeLogFile(stderr)}
        self.rc = rc

class TestDzilSmoke(steps.BuildStepMixin, unittest.TestCase):

    def setUp(self):
        return self.setUpBuildStep()

    def tearDown(self):
        return self.tearDownBuildStep()
        
    def test_dzilPass(self):
        step = self.setupStep(dzil.DzilSmoke())
        
        log = """[DZ] building test distribution under .build/7Qxmbdz_7c
[DZ] beginning to build App-gcal
[DZ] guessing dist's main_module is lib/App/gcal.pm
[DZ] extracting distribution abstract from lib/App/gcal.pm
[@ARJONES/@Basic/ExtraTests] rewriting release test xt/release/pod-syntax.t
[@ARJONES/@Basic/ExtraTests] rewriting author test xt/author/critic.t
[DZ] writing App-gcal in .build/7Qxmbdz_7c
Checking if your kit is complete...
Looks good
Writing Makefile for App::gcal
Writing MYMETA.yml and MYMETA.json
cp lib/App/gcal.pm blib/lib/App/gcal.pm
cp bin/gcal blib/script/gcal
/Users/ajones/perl5/perlbrew/perls/perl-5.12.1/bin/perl -MExtUtils::MY -e 'MY->fixin(shift)' -- blib/script/gcal
Manifying blib/man1/gcal.1
Manifying blib/man3/App::gcal.3
PERL_DL_NONLAZY=1 /Users/ajones/perl5/perlbrew/perls/perl-5.12.1/bin/perl "-MExtUtils::Command::MM" "-e" "test_harness(0, 'blib/lib', 'blib/arch')" t/*.t
t/01.t .................. ok     
t/author-critic.t ....... skipped: these tests are for testing by the author
t/release-pod-syntax.t .. skipped: these tests are for release candidate testing
All tests successful.
Files=3, Tests=16,  1 wallclock secs ( 0.03 usr  0.01 sys +  0.44 cusr  0.05 csys =  0.53 CPU)
Result: PASS
[DZ] all's well; removing .build/7Qxmbdz_7c"""
        step.addCompleteLog('stdio', log)

        rc = step.evaluateCommand(FakeCmd("", ""))
        
        self.assertEqual(rc, SUCCESS)
        self.assertEqual(self.step_statistics, {
            'tests-total' : 16,
            'tests-failed' : 0,
            'tests-passed' : 16,
            'tests-warnings' : 0,
        })
        
    def test_dzilFailure(self):
        step = self.setupStep(dzil.DzilSmoke())
        
        log = """[DZ] building test distribution under .build/1BJmbaW_hz
[DZ] beginning to build App-gcal
[DZ] guessing dist's main_module is lib/App/gcal.pm
[DZ] extracting distribution abstract from lib/App/gcal.pm
[@ARJONES/@Basic/ExtraTests] rewriting release test xt/release/pod-syntax.t
[@ARJONES/@Basic/ExtraTests] rewriting author test xt/author/critic.t
[DZ] writing App-gcal in .build/1BJmbaW_hz
Checking if your kit is complete...
Looks good
Writing Makefile for App::gcal
Writing MYMETA.yml and MYMETA.json
cp lib/App/gcal.pm blib/lib/App/gcal.pm
cp bin/gcal blib/script/gcal
/Users/ajones/perl5/perlbrew/perls/perl-5.12.1/bin/perl -MExtUtils::MY -e 'MY->fixin(shift)' -- blib/script/gcal
Manifying blib/man1/gcal.1
Manifying blib/man3/App::gcal.3
PERL_DL_NONLAZY=1 /Users/ajones/perl5/perlbrew/perls/perl-5.12.1/bin/perl "-MExtUtils::Command::MM" "-e" "test_harness(0, 'blib/lib', 'blib/arch')" t/*.t
t/01.t .................. 1/16 
#   Failed test at t/01.t line 14.
#                   'rror parsing /Users/ajones/dev/perl/gcal/.build/1BJmbaW_hz/t/../dist.ini'
#     doesn't match '(?-xism:error parsing)'

#   Failed test at t/01.t line 42.
#                   'rror parsing /Users/ajones/dev/perl/gcal/.build/1BJmbaW_hz/t/../dist.ini'
#     doesn't match '(?-xism:error parsing)'

#   Failed test at t/01.t line 47.
#                   'rror parsing /Users/ajones/dev/perl/gcal/.build/1BJmbaW_hz/t/../dist.ini'
#     doesn't match '(?-xism:error parsing)'
# Looks like you failed 3 tests of 16.
t/01.t .................. Dubious, test returned 3 (wstat 768, 0x300)
Failed 3/16 subtests 
t/author-critic.t ....... skipped: these tests are for testing by the author
t/release-pod-syntax.t .. skipped: these tests are for release candidate testing

Test Summary Report
-------------------
t/01.t                (Wstat: 768 Tests: 16 Failed: 3)
  Failed tests:  4, 14, 16
  Non-zero exit status: 3
Files=3, Tests=16,  1 wallclock secs ( 0.03 usr  0.01 sys +  0.43 cusr  0.05 csys =  0.52 CPU)
Result: FAIL
Failed 1/3 test programs. 3/16 subtests failed.
make: *** [test_dynamic] Error 255
error running make test"""
        step.addCompleteLog('stdio', log)
        
        rc = step.evaluateCommand(FakeCmd("", ""))
        
        self.assertEqual(rc, FAILURE)
        self.assertEqual(self.step_statistics, {
            'tests-total' : 16,
            'tests-failed' : 3,
            'tests-passed' : 13,
            'tests-warnings' : 0,
        })
