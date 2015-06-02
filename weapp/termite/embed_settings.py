# Django settings for termite project.
import os

PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))


TEMPLATE_LOADERS = [
    'termite.core.stripper.Loader',
]

MIDDLEWARE_CLASSES = [
    #'termite.core.middleware.BuilderDetectorMiddleware',
    'termite.core.middleware.DesignModeDetectorMiddleware',
    'termite.core.middleware.ProjectMiddleware',
    'termite.core.middleware.ModifyStaticMiddleware'
]


TEMPLATE_CONTEXT_PROCESSORS = [
    'termite.core.context_processors.termite_dialogs',
]

TEMPLATE_DIRS = [
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/termite_templates' % PROJECT_HOME,
    '%s/templates' % PROJECT_HOME,
    '%s/static/termite_js/app' % PROJECT_HOME,
    '%s/static/js' % PROJECT_HOME,
]

INSTALLED_APPS = [
    'termite.workbench',
]

exports = {
    'COMPONENTS_DIR': os.path.join(PROJECT_HOME, './static', 'termite_js/app/component'),
    'PAGE_TEMPLATE_IMAGE_DIR': os.path.join(PROJECT_HOME, '../static/upload', 'custom_template'),
    'PROJECT_JS_DIR': os.path.join(PROJECT_HOME, './static', 'js'),
    'TERMITE_HOME': os.path.join(PROJECT_HOME, './static'),
    'DOWNLOAD_HOME': os.path.join(PROJECT_HOME, './static'),

    'PAGE_STORE_SERVER_HOST': 'mongo.weapp.com',
    'PAGE_STORE_SERVER_PORT': 27017,
    'PAGE_STORE_DB': 'termite',

    'TERMITE_WEB_DIALOG_DIRS': [
        ('static', '%s/static/' % PROJECT_HOME)
    ]
}