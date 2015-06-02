#! /bin/bash

#create a link to django admin media directory
LINK_TARGET="static/admin"
if [ -h $LINK_TARGET ]; then
        echo "Link file to admin media is already EXISTS!!! Please remove it manually"
        exit 1
fi

ADMIN_MEDIA_DIR=`python <<XMONITOR_END
import django
import os
abs_django_path = os.path.abspath(os.path.dirname(django.__file__))
print os.path.join(abs_django_path, 'contrib/admin/static/admin')
XMONITOR_END`
echo "link $LINK_TARGET to $ADMIN_MEDIA_DIR"
ln -s $ADMIN_MEDIA_DIR $LINK_TARGET

if [ -h $LINK_TARGET ]; then
        echo "create link file to admin media dir SUCCESS"
else
        echo "create link file to admin media dir FAILED"
fi
