# -*- coding: utf-8 -*-
"""
增加本地当前分支名
"""
import subprocess

commit_msg_filepath = '.git/COMMIT_EDITMSG'

branch_name = subprocess.check_output('git symbolic-ref --short HEAD').strip()


with open(commit_msg_filepath, 'r') as f:
    raw_msg = f.read()

with open(commit_msg_filepath, 'w') as f:
    f.write("[%s]%s" % (branch_name, raw_msg))

