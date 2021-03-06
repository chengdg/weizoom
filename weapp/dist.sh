#!/bin/bash
cd ..
SRC_DIR="weapp"
DST_DIR="deploy_dist"

DIR_NAME=`dirname $0`
cd $DIR_NAME

# this script is used to dist weapp web
if [ -d $DST_DIR ]; then
	echo "remove old $DST_DIR"
	rm -rf $DST_DIR
fi

mkdir -p $DST_DIR

echo "copy files from $SRC_DIR to $DST_DIR"
cp -rf $SRC_DIR $DST_DIR

echo "remove unnecessary files"
find $DST_DIR -name ".svn" | xargs rm -rf
find $DST_DIR -name "*.pyc" | xargs rm -rf

echo "change shell script's permission"
find $DST_DIR -name "*.sh" | xargs chmod +x

cd $DST_DIR/weapp
echo "now enter `pwd`"
python disttool/dist.py --deleteJs --compress

