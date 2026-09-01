# Django: settings.py ও INSTALLED_APPS ⚙️

Django প্রজেক্টের সব কনফিগারেশন `settings.py`-এ থাকে। এই লেসনে `settings.py`-এর গুরুত্বপূর্ণ অংশ ও `INSTALLED_APPS` বিস্তারিত শিখবো।

---

## ১. settings.py কী?

`settings.py` হলো Django প্রজেক্টের মূল কনফিগারেশন ফাইল। এখানে প্রজেক্টের সব সেটিংস থাকে:
- কোন apps চালু আছে
- কোন database ব্যবহার হচ্ছে
- templates কোথায় আছে
- static files কোথায় আছে
- security settings
- timezone ও language

### ফাইলের অবস্থান:

```
config/settings.py
```

---

## ২. settings.py-এর মূল অংশসমূহ

`settings.py`-এর গুরুত্বপূর্ণ সেকশনগুলো নিচে আলোচনা করা হলো।

---

### ১. BASE_DIR — প্রজেক্টের রুট পাথ

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
```

এটা প্রজেক্টের রুট ডিরেক্টরির পথ। অন্যান্য পাথ এটা দিয়ে তৈরি করা হয়।

---

### ২. SECRET_KEY — গোপন চাবি

```python
SECRET_KEY = "django-insecure-xxxxxxxxxxxxxxxxxxxx"
```

Django-এর security-এর জন্য ব্যবহৃত হয়। এটা কখনো公开 করা উচিত না।

⚠️ **Production-এ:** `.env` ফাইলে রাখুন:

```python
import os
SECRET_KEY = os.environ.get("SECRET_KEY")
```

---

### ৩. DEBUG — ডিবাগ মোড

```python
DEBUG = True
```

- `True` হলে error page দেখায় (development)
- `False` হলে generic error page (production)

⚠️ **Production-এ অবশ্যই `False` রাখুন!**

---

### ৪. ALLOWED_HOSTS — অনুমোদিত হোস্ট

```python
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
```

কোন কোন domain/IP থেকে request আসতে পারবে তা নির্ধারণ করে।

Production-এ:
```python
ALLOWED_HOSTS = ["yourdomain.com", "www.yourdomain.com"]
```

---

### ৫. INSTALLED_APPS — চালু করা Apps

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

এখানে যেসব app লেখা থাকবে সেগুলো Django চালু করবে। নিজের তৈরি করা app ও এখানে যোগ করতে হয়।

---

### ৬. MIDDLEWARE — মিডলওয়্যার

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

Request-এর আগে-পরে যে কোডগুলো চলে তা এখানে।

---

### ৭. ROOT_URLCONF — মূল URL ফাইল

```python
ROOT_URLCONF = "config.urls"
```

Django-কে বলে কোন ফাইলে URL routing আছে।

---

### ৮. TEMPLATES — টেমপ্লেট কনফিগারেশন

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # project-level templates
        "APP_DIRS": True,                    # app-level templates
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

- `DIRS` — project-level templates ফোল্ডার
- `APP_DIRS: True` — প্রতিটা app-এর `templates/` ফোল্ডার ও ও ও

---

### ৯. WSGI_APPLICATION — WSGI অ্যাপ

```python
WSGI_APPLICATION = "config.wsgi.application"
```

Production server-এর জন্য WSGI অ্যাপ্লিকেশনের পথ।

---

### ১০. DATABASES — ডেটাবেস কনফিগারেশন

Default SQLite:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

PostgreSQL:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydatabase",
        "USER": "myuser",
        "PASSWORD": "mypassword",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

MySQL:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mydatabase",
        "USER": "myuser",
        "PASSWORD": "mypassword",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

---

### ১১. AUTH_PASSWORD_VALIDATORS — পাসওয়ার্ড ভ্যালিডেশন

```python
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
```

পাসওয়ার্ড কতটা শক্তিশালী হতে হবে তা নির্ধারণ করে।

---

### ১২. LANGUAGE_CODE ও TIME_ZONE

```python
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
```

বাংলা ও ঢাকার টাইমজোন:

```python
LANGUAGE_CODE = "bn"
TIME_ZONE = "Asia/Dhaka"
```

---

### ১৩. USE_I18N ও USE_L10N ও USE_TZ

```python
USE_I18N = True    # Internationalization
USE_L10N = True    # Localization (Django 4.0+ এ সরানো হয়েছে)
USE_TZ = True      # Timezone support
```

---

### ১৪. STATIC_URL — Static Files

```python
STATIC_URL = "static/"
```

Project-level static files:

```python
STATICFILES_DIRS = [BASE_DIR / "static"]
```

Production collect static:

```python
STATIC_ROOT = BASE_DIR / "staticfiles"
```

---

### ১৫. DEFAULT_AUTO_FIELD

```python
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

Model-এর primary key-এর ডিফল্ট টাইপ।

---

### ১৬. MEDIA_URL ও MEDIA_ROOT — User Uploaded Files

```python
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
```

---

## ৩. INSTALLED_APPS বিস্তারিত

`INSTALLED_APPS` হলো Django-র সবচেয়ে গুরুত্বপূর্ণ সেটিং। এখানে যেসব app লেখা থাকবে সেগুলো Django চালু করবে।

### Built-in Apps (ডিফল্ট):

| App | কাজ |
|-----|------|
| `django.contrib.admin` | Admin panel |
| `django.contrib.auth` | Authentication (login, user) |
| `django.contrib.contenttypes` | Content type framework |
| `django.contrib.sessions` | Session management |
| `django.contrib.messages` | Flash messages |
| `django.contrib.staticfiles` | Static files management |

### নিজের App যোগ করা:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # আমাদের apps
    "blog",
    "accounts",
]
```

### Third-party App যোগ করা:

```python
INSTALLED_APPS = [
    # ...
    # Third-party
    "rest_framework",        # Django REST Framework
    "corsheaders",           # CORS
    "ckeditor",              # Rich text editor
    "django_filters",        # Filtering

    # আমাদের apps
    "blog",
]
```

### App Config দিয়ে যোগ করা:

আরো স্পেসিফিকভাবে AppConfig দিয়েও যোগ করা যায়:

```python
INSTALLED_APPS = [
    # ...
    "blog.apps.BlogConfig",
    "accounts.apps.AccountsConfig",
]
```

`apps.py` ফাইলে:

```python
# blog/apps.py
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
    verbose_name = "ব্লগ"  # Admin panel-এ দেখানো নাম
```

---

## ৪. একটা সম্পূর্ণ settings.py উদাহরণ

```python
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-default-key-for-dev")

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",

    # Local
    "blog",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

LANGUAGE_CODE = "bn"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
```

---

## ৫. Multiple Settings Files (বড় প্রজেক্টের জন্য)

বড় প্রজেক্টে আলাদা আলাদা environment-এর জন্য আলাদা settings ফাইল রাখা হয়:

```
config/
├── settings/
│   ├── __init__.py
│   ├── base.py        # সব environment-এর জন্য common
│   ├── dev.py         # Development
│   ├── prod.py        # Production
│   └── test.py        # Testing
├── urls.py
└── wsgi.py
```

### `base.py`:

```python
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
]

# ... common settings
```

### `dev.py`:

```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

### `prod.py`:

```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = ["yourdomain.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": "5432",
    }
}
```

### ব্যবহার:

```bash
# Development
python manage.py runserver --settings=config.settings.dev

# Production
python manage.py runserver --settings=config.settings.prod
```

অথবা `manage.py` তে সেট করুন:

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
```

---

## ৬. Environment Variables (.env)

সেনসিটিভ ডেটা (SECRET_KEY, DB password) `.env` ফাইলে রাখা হয়।

### `python-dotenv` ইনস্টল:

```bash
pip install python-dotenv
```

### `.env` ফাইল:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypassword
```

### `settings.py`-এ:

```python
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True") == "True"
```

`.env` কখনো git-এ যাবে না!

---

## ৭. সাধারণ ভুল ও সমাধান

### ভুল ১: App যোগ করা হয়নি

**সমস্যা:** `ImportError: No module named blog`

**সমাধান:** `INSTALLED_APPS` এ `blog` যোগ করুন।

### ভুল ২: Template পাওয়া যাচ্ছে না

**সমস্যা:** `TemplateDoesNotExist`

**সমাধান:** `TEMPLATES`-এর `DIRS` এ `BASE_DIR / "templates"` যোগ করুন, অথবা `APP_DIRS: True` রাখুন।

### ভুল ৩: Database error

**সমস্যা:** `OperationalError: no such table`

**সমাধান:** `python manage.py migrate` চালান।

### ভুল ৪: Static files লোড হচ্ছে না

**সমাধান:** `STATICFILES_DIRS` ও `STATIC_ROOT` সঠিকভাবে সেট করুন।

---

## ৮. সেরা প্র্যাকটিস (Best Practices)

1. ✅ `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` production-এ সঠিকভাবে সেট করুন
2. ✅ সেনসিটিভ ডেটা `.env` ফাইলে রাখুন
3. ✅ বড় প্রজেক্টে multiple settings ফাইল ব্যবহার করুন
4. ✅ নিজের app গুলো সবসময় `INSTALLED_APPS`-এ যোগ করুন
5. ✅ Timezone ঢাকা সেট করুন (`Asia/Dhaka`)
6. ✅ নতুন app যোগ করার পর migration চালান
7. ❌ `SECRET_KEY` কখনো公开 করবেন না
8. ❌ Production-এ `DEBUG = True` রাখবেন না

---

## ৯. Practical Exercise

নিচের কাজগুলো করে দেখুন:

```bash
# ১. একটা নতুন app তৈরি করুন
python manage.py startapp accounts

# ২. settings.py-এ accounts যোগ করুন
# INSTALLED_APPS এ "accounts" যোগ করুন

# ৩. Timezone ঢাকা সেট করুন
# TIME_ZONE = "Asia/Dhaka"

# ৪. LANGUAGE_CODE বাংলা করুন
# LANGUAGE_CODE = "bn"

# ৫. Static files config করুন
# STATICFILES_DIRS = [BASE_DIR / "static"]

# ৬. MEDIA config করুন
# MEDIA_URL = "media/"
# MEDIA_ROOT = BASE_DIR / "media"

# ৭. Migration চালান
python manage.py migrate

# ৮. Server চালু
python manage.py runserver
```

---

## 🎯 আজকের Key Takeaways

### settings.py:
1. **`BASE_DIR`** — প্রজেক্টের রুট পাথ
2. **`SECRET_KEY`** — গোপন চাবি (কখনো公开 করবেন না)
3. **`DEBUG`** — `True` dev, `False` prod
4. **`ALLOWED_HOSTS`** — অনুমোদিত domain/IP
5. **`INSTALLED_APPS`** — চালু করা apps
6. **`DATABASES`** — database কনফিগারেশন
7. **`TIME_ZONE`** — `Asia/Dhaka`
8. **`STATIC_URL`** ও **`MEDIA_URL`** — static ও media files

### INSTALLED_APPS:
1. নিজের app সবসময় এখানে যোগ করতে হবে
2. Built-in apps: admin, auth, contenttypes, sessions, messages, staticfiles
3. Third-party apps: rest_framework, corsheaders ইত্যাদি
4. AppConfig দিয়েও যোগ করা যায় (`blog.apps.BlogConfig`)

### Advanced:
1. Multiple settings files (dev, prod, test)
2. `.env` দিয়ে environment variables
3. Production-এ `DEBUG = False` অবশ্যই

---

## ❓ অনুশীলনী প্রশ্ন

1. `settings.py` ফাইলের গুরুত্ব কী?
2. `INSTALLED_APPS`-এর কাজ কী?
3. `DEBUG = True` কখন ব্যবহার করা উচিত?
4. `ALLOWED_HOSTS` এর কাজ কী?
5. `SECRET_KEY` কেন গোপন রাখতে হয়?
6. SQLite থেকে PostgreSQL-এ পরিবর্তন করতে কী করতে হবে?
7. `TIME_ZONE = "Asia/Dhaka"` সেট করলে কী হয়?
8. Multiple settings files কেন ব্যবহার করা হয়?
9. `.env` ফাইলের গুরুত্ব কী?
