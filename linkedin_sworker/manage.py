import os
import sys

from dotenv import load_dotenv

sys.path.append('..')
load_dotenv()

from django.conf import settings

os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')

# settings.configure(
#     INSTALLED_APPS=[
#         'django.contrib.admin',
#         'django.contrib.auth',
#         'django.contrib.contenttypes',
#         'django.contrib.sessions',
#         'django.contrib.messages',
#         'django.contrib.staticfiles',
#
#         'rest_framework',
#         'rest_framework.authtoken',
#
#         'linkedin_sworker',
#     ],
#     MIDDLEWARE=[
#         'django.middleware.security.SecurityMiddleware',
#         'django.contrib.sessions.middleware.SessionMiddleware',
#         'django.middleware.common.CommonMiddleware',
#         'django.middleware.csrf.CsrfViewMiddleware',
#         'django.contrib.auth.middleware.AuthenticationMiddleware',
#         'django.contrib.messages.middleware.MessageMiddleware',
#         'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     ],
#     REST_FRAMEWORK={
#         'DEFAULT_AUTHENTICATION_CLASSES': (
#             'rest_framework.authentication.TokenAuthentication',
#         ),
#     },
#     TEMPLATES=[
#         {
#             'BACKEND': 'django.template.backends.django.DjangoTemplates',
#             'APP_DIRS': True,
#             'OPTIONS': {
#                 'context_processors': [
#                     'django.template.context_processors.debug',
#                     'django.template.context_processors.request',
#                     'django.contrib.auth.context_processors.auth',
#                     'django.contrib.messages.context_processors.messages',
#                 ],
#             },
#         },
#     ],
#     DEBUG=True,
#     ROOT_URLCONF='urls',
#     SECRET_KEY='secret',
# )

import django

django.setup()

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)
