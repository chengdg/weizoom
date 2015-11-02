#!/bin/bash

a=`git branch -r|grep origin/.*$1|awk -F '/' '{print $2}'`
echo [in bash] checkout origin/$a
git checkout origin/$a -fB $a
echo [in bash] push origin_history $a
git push origin_history $a:$a
echo [in bash] delete origin/$a
git push origin :$a
echo [in bash] delete locale/$a
git checkout master
git branch -D $a