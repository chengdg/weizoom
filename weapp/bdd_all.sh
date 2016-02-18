#!/bin/bash
DIR=`dirname $0`
cd $DIR
behave --no-skipped --tags @mall2 --tags ~@ui --tags ~@ignore
