#!/sbin/bash

cd weapp

/usr/local/python/bin/python manage.py test -v2  -- -c=unit_nose2.cfg --with-cov --cov-report=html -B --cov-config=.coveragerc --no-user-config -v --log-level=30 utils

modules=`ls -l | egrep '^d' | awk '{print $9}'`
for module in $modules; do
        /usr/local/python/bin/pylint --rcfile=pylint.ini $module
done

cd -