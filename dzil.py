import re
from twisted.python import log

from buildbot.status.results import SUCCESS, FAILURE, WARNINGS, SKIPPED
from buildbot.steps.shell import Test

class DzilSmoke(Test):
    command=["dzil", "smoke"]

    def evaluateCommand(self, cmd):

        return SUCCESS
