import re
from twisted.python import log

from buildbot.status.results import SUCCESS, FAILURE, WARNINGS, SKIPPED
from buildbot.steps.shell import WarningCountingShellCommand, Test

class DzilAuthorDependencies(WarningCountingShellCommand):
    name = "author dependencies"
    description = ["updating", "author", "dependencies"]
    descriptionDone = ["updated", "author", "dependencies"]

    command="dzil authordeps | cpanm"

class DzilDependencies(WarningCountingShellCommand):
    name = "dependencies"
    description = ["updating", "dependencies"]
    descriptionDone = ["updated", "dependencies"]

    command="dzil listdeps | cpanm"

class DzilSmoke(Test):
    command=["dzil", "smoke"]

    def evaluateCommand(self, cmd):
        # Get stdio, stripping pesky newlines etc.
        lines = map(
            lambda line : line.replace('\r\n','').replace('\r','').replace('\n',''),
            self.getLog('stdio').readlines()
            )

        total = 0
        passed = 0
        failed = 0
        rc = SUCCESS
        if cmd.rc > 0:
            rc = FAILURE

        re_test_result = re.compile("^Result: (\w+)")

        mos = map(lambda line: re_test_result.search(line), lines)
        test_result_lines = [mo.groups() for mo in mos if mo]

        if test_result_lines:
            test_result_line = test_result_lines[0]
            
            if(test_result_line[0] == 'PASS'):
                
                re_test_totals = re.compile("^Files=(\d+), Tests=(\d+)")
                mos = map(lambda line: re_test_totals.search(line), lines)
                test_totals_lines = [mo.groups() for mo in mos if mo]
                
                if test_totals_lines:
                    test_totals_line = test_totals_lines[0]
                    
                    total = int(test_totals_line[1])
                    passed = total
                
            else:
                rc = FAILURE
                
                re_test_totals = re.compile("^Failed (\d+)/(\d+) test programs. (\d+)/(\d+)")
                mos = map(lambda line: re_test_totals.search(line), lines)
                test_totals_lines = [mo.groups() for mo in mos if mo]
                
                if test_totals_lines:
                    test_totals_line = test_totals_lines[0]
                    
                    total = int(test_totals_line[3])
                    failed = int(test_totals_line[2])
                    passed = total - failed

        warnings = 0
        if self.warningPattern:
            wre = self.warningPattern
            if isinstance(wre, str):
                wre = re.compile(wre)

            warnings = len([l for l in lines if wre.search(l)])

            if rc == SUCCESS and warnings:
                rc = WARNINGS

        self.setTestResults(total=total, failed=failed, passed=passed,
                            warnings=warnings)

        return rc

class DzilTest(DzilSmoke):
    command=["dzil", "test"]
