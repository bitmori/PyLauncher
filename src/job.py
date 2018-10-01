import os

import launchd

USER_AGENTS = os.path.expanduser('~/Library/LaunchAgents')
ADMIN_AGENTS = '/Library/LaunchAgents'
OS_AGENTS = '/System/Library/LaunchAgents'


def _job_type(j):
    pname = j.plistfilename
    if not pname:
        return 0
    if pname.startswith(USER_AGENTS):
        return 1
    elif pname.startswith(ADMIN_AGENTS):
        return 2
    elif pname.startswith(OS_AGENTS):
        return 3
    else:
        return 0


def get_user_agents():
    return filter(lambda j: _job_type(j) == 1, launchd.jobs())
