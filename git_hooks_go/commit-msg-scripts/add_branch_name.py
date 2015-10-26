# -*- coding: utf-8 -*-
"""
增加本地当前分支名
"""
import subprocess

commit_msg_filepath = '.git/COMMIT_EDITMSG'

branch = subprocess.check_output('git symbolic-ref HEAD', universal_newlines=True).strip()
try:
    if 'refs/heads' in branch:
        branch_name = branch.split('/')[-1]
    else:
        branch_name = None
except:
    branch_name = None

with open(commit_msg_filepath, 'r') as f:
    raw_msg = f.read()

with open(commit_msg_filepath, 'w') as f:
    f.write("[%s]%s" % (branch_name, raw_msg))

