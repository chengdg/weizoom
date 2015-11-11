# -*- coding: utf-8 -*-
import subprocess

commit_msg_filepath = '.git/COMMIT_EDITMSG'

branch_name = subprocess.check_output('git symbolic-ref --short HEAD').strip()

if branch_name == 'master':
    print('Commit failed! DO not commit on master!')
    exit(1)
