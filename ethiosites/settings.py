# ethiosites/settings.py
from ast import Delete
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-in-production'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*.local']

# Internationalization
LANGUAGE_CODE = 'en'

EXTRA_LANG_INFO = {
    'am': {
        'bidi': False,
        'code': 'am',
        'name': 'Amharic',
        'name_local': 'አማርኛ',
    },
}

# Add the extra languages to Django's LANG_INFO
import django.conf.locale
from django.conf.locale import LANG_INFO

django.conf.locale.LANG_INFO.update(EXTRA_LANG_INFO)
LANG_INFO.update(EXTRA_LANG_INFO)

LANGUAGES = [
    ('en', 'English'),
    ('am', 'Amharic'),
]

USE_I18N = True
USE_L10N = True

INSTALLED_APPS = [
    # Unfold must be first
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'django_ckeditor_5',
    'adminsortable2',
    'colorfield',
    'modeltranslation',
    # Your app
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ethiosites.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ethiosites.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

UNFOLD = {
    "SITE_TITLE": "EthioSites – Multi-Client CMS",
    "SITE_HEADER": "EthioSites",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "EN",
                "am": "AM",
            },
        },
    },
    "ACTIONS": {
        "delete": True,
        "confirm_delete": True,
    },
}

customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
        {
            'color': 'hsl(221, 17%, 65%)',
            'label': 'Gray'
        }
    ]
# CKEDITOR_5_CUSTOM_CSS is handled in the base template
# CKEDITOR_5_FILE_STORAGE is set below


# ethiosites/settings.py (Updated CKEDITOR_5_CONFIGS)

CKEDITOR_5_CONFIGS = {
        # 'default': {
    #     'toolbar': [
    #         'heading', 
    #         '|', 
    #         'bold', 
    #         'italic', 
    #         'link', 
    #         'bulletedList', 
    #         'numberedList', 
    #         'blockQuote',
    #         'outdent',
    #         'indent'
    #     ],
    #     'heading': {
    #         'options': [
    #             {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
    #             {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
    #             {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
    #             {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'}
    #         ]
    #     },
    #     'link': {
    #         'decorators': [
    #             {
    #                 'mode': 'manual',
    #                 'label': 'Open in a new tab',
    #                 'attributes': {
    #                     'target': '_blank',
    #                     'rel': 'noopener noreferrer'
    #                 }
    #             }
    #         ]
    #     },
    #     'height': 300,
    #     'width': '100%',
    # },
    'default': {
        'toolbar': {
            'items': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
                      'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                      'bulletedList', 'numberedList', 'todoList', '|', 'blockQuote', 'imageUpload', '|',
                      'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                      'insertTable',
                      ],
            'shouldNotGroupWhenFull': 'true'
        },
        
        # 🔑 START OF NEW REQUIRED CONFIGURATION FOR FONT FEATURES 🔑
        'fontFamily': {
            'options': [
                'default',
                'Arial, Helvetica, sans-serif',
                'Courier New, Courier, monospace',
                'Georgia, serif',
                'Lucida Sans Unicode, Lucida Grande, sans-serif',
                'Tahoma, Geneva, sans-serif',
                'Times New Roman, Times, serif',
                'Trebuchet MS, Helvetica, sans-serif',
                'Verdana, Geneva, sans-serif'
            ],
            'supportAllValues': True
        },
        'fontSize': {
            'options': [
                10, 12, 14, 'default', 16, 18, 20, 24, 30
            ],
            'unit': 'px'
        },
        'fontColor': {
            # You can define a custom color palette here, or use 'colors' option
            'colors': customColorPalette 
        },
        'fontBackgroundColor': {
            'colors': customColorPalette
        },
        # 🔑 END OF NEW REQUIRED CONFIGURATION 🔑
        
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]
        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        },
        'mediaEmbed': {
            'previews': {
                'previewType': 'iframe'
            },
            'removeProviders': ['instagram', 'twitter', 'googleMaps', 'flickr', 'facebook'],
            'extraProviders': [
                {
                    'name': 'youtube',
                    'url': '^https?://(www\\.)?(youtube\\.com/(watch\\?v=|embed/)|youtu\\.be/)([\\w-]+)',
                    'html': '<div style="position: relative; padding-bottom: 100%; height: 0; padding-bottom: 56.2493%;"><iframe src="https://www.youtube.com/embed/{match[4]}" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0;" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>'
                }
            ]
        }
    },

    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}

# CKEditor 5 file storage
CKEDITOR_5_FILE_STORAGE = "core.storage.CustomStorage"
CUSTOM_FILE_STORAGE = "core.storage.CustomStorage"