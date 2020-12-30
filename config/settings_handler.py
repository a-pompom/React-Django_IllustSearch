from typing import TypedDict, List, Tuple, Any

TypeOPTIONS = TypedDict("TypeOPTIONS", { "context_processors": List[str] })
TypeTEMPLATES = TypedDict("TypeTEMPLATES", { "BACKEND": str, "DIRS": List[Any], "APP_DIRS": bool, "OPTIONS": TypeOPTIONS })
TypeRESTFRAMEWORK = TypedDict("TypeRESTFRAMEWORK", { "EXCEPTION_HANDLER": str })
TypeDjangoDbBackends = TypedDict("TypeDjangoDbBackends", { "handlers": List[str], "level": str })
TypeLoggers = TypedDict("TypeLoggers", { "django.db.backends": TypeDjangoDbBackends })
TypeConsole = TypedDict("TypeConsole", { "level": str, "class": str })
TypeHandlers = TypedDict("TypeHandlers", { "console": TypeConsole })
TypeLOGGING = TypedDict("TypeLOGGING", { "version": int, "disable_existing_loggers": bool, "handlers": TypeHandlers, "loggers": TypeLoggers })
TypeTEST = TypedDict("TypeTEST", { "CHARSET": None, "COLLATION": None, "NAME": None, "MIRROR": None })
TypeOPTIONS = TypedDict("TypeOPTIONS", {  })
TypeDefault = TypedDict("TypeDefault", { "ENGINE": str, "NAME": str, "ATOMIC_REQUESTS": bool, "AUTOCOMMIT": bool, "CONN_MAX_AGE": int, "OPTIONS": TypeOPTIONS, "TIME_ZONE": None, "USER": str, "PASSWORD": str, "HOST": str, "PORT": str, "TEST": TypeTEST })
TypeDATABASES = TypedDict("TypeDATABASES", { "default": TypeDefault })
TypeAUTHPASSWORDVALIDATORS = TypedDict("TypeAUTHPASSWORDVALIDATORS", { "NAME": str })
TypeSetting = TypedDict("TypeSetting", { "ALLOWED_HOSTS": List[str], "AUTHENTICATION_BACKENDS": List[str], "AUTH_PASSWORD_VALIDATORS": List[TypeAUTHPASSWORDVALIDATORS], "AUTH_USER_MODEL": str, "BASE_DIR": str, "CORS_ALLOW_CREDENTIALS": bool, "CORS_ORIGIN_WHITELIST": List[str], "DATABASES": TypeDATABASES, "DEBUG": bool, "INSTALLED_APPS": List[str], "LANGUAGE_CODE": str, "LOGGING": TypeLOGGING, "MIDDLEWARE": List[str], "RECORDS_PER_PAGE": int, "REST_FRAMEWORK": TypeRESTFRAMEWORK, "ROOT_URLCONF": str, "SECRET_KEY": str, "STATIC_URL": str, "TEMPLATES": List[TypeTEMPLATES], "TIME_ZONE": str, "USE_I18N": bool, "USE_L10N": bool, "USE_TZ": bool, "WSGI_APPLICATION": str })

setting_dict : TypeSetting = {
    "ALLOWED_HOSTS": ['localhost', 'testserver', 'testserver'],
    "AUTHENTICATION_BACKENDS": ['app_login.backend.AuthBackend'],
    "AUTH_PASSWORD_VALIDATORS": [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}],
    "AUTH_USER_MODEL": 'app_login.User',
    "BASE_DIR": '/Users/aoi/Desktop/works/django_illust_search',
    "CORS_ALLOW_CREDENTIALS": True,
    "CORS_ORIGIN_WHITELIST": ['http://localhost:30001'],
    "DATABASES": {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': '/Users/aoi/Desktop/works/django_illust_search/db.sqlite3', 'ATOMIC_REQUESTS': False, 'AUTOCOMMIT': True, 'CONN_MAX_AGE': 0, 'OPTIONS': {}, 'TIME_ZONE': None, 'USER': '', 'PASSWORD': '', 'HOST': '', 'PORT': '', 'TEST': {'CHARSET': None, 'COLLATION': None, 'NAME': None, 'MIRROR': None}}},
    "DEBUG": False,
    "INSTALLED_APPS": ['app_common.apps.AppCommonConfig', 'app_login.apps.AppLoginConfig', 'app_illust_list.apps.AppIllustListConfig', 'corsheaders', 'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'rest_framework'],
    "LANGUAGE_CODE": 'ja-jp',
    "LOGGING": {'version': 1, 'disable_existing_loggers': False, 'handlers': {'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler'}}, 'loggers': {'django.db.backends': {'handlers': ['console'], 'level': 'DEBUG'}}},
    "MIDDLEWARE": ['corsheaders.middleware.CorsMiddleware', 'django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware'],
    "RECORDS_PER_PAGE": 5,
    "REST_FRAMEWORK": {'EXCEPTION_HANDLER': 'common.exception_handler.handle_exception'},
    "ROOT_URLCONF": 'config.urls',
    "SECRET_KEY": 'umpmr_+t1^==vk9x8lf-0iid&u4&x+zxh14**+#w1m_(ezvq%x',
    "STATIC_URL": '/static/',
    "TEMPLATES": [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}],
    "TIME_ZONE": 'JAPAN',
    "USE_I18N": True,
    "USE_L10N": True,
    "USE_TZ": True,
    "WSGI_APPLICATION": 'config.wsgi.application',
}

def get_setting_dict() -> TypeSetting:
    return setting_dict