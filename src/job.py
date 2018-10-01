import os

USER_AGENTS = os.path.expanduser('~/Library/LaunchAgents')
ADMIN_AGENTS = '/Library/LaunchAgents'
OS_AGENTS = '/System/Library/LaunchAgents'


def job_type(j):
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
