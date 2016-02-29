from .base import *     # noqa

SECRET_KEY = 'pk3v^+%-#ca$7=q=u@2pjw7a5*t2u94ow9*(ii(45_$t@w((&r'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
    }
}
