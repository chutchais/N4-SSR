from equipment_rental.settings import *


ALLOWED_HOSTS = ['*']
DEBUG = True
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': env.db('SQLITE_URL', default='sqlite:////db.sqlite3')
}


# Local Static_root
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')