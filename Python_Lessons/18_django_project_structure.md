# Django: Project Structure 📂

Django প্রজেক্ট তৈরি করার পর কোন ফাইল কোন কাজ করে তা জানা জরুরি। এই লেসনে Django-এর পুরো project structure বিস্তারিত শিখবো।

---

## ১. Django Project Structure Overview

একটা সাধারণ Django প্রজেক্ট এরকম দেখায়:

```
my_django_project/          # প্রজেক্টের রুট ফোল্ডার
├── venv/                   # Virtual Environment
├── config/                 # Project configuration (startproject ফোল্ডার)
│   ├── __init__.py
│   ├── settings.py         # সব কনফিগারেশন
│   ├── urls.py             # মূল URL routing
│   ├── wsgi.py             # WSGI (production)
│   └── asgi.py             # ASGI (async)
├── blog/                   # App (startapp ফোল্ডার)
│   ├── __init__.py
│   ├── admin.py            # Admin panel register
│   ├── apps.py             # App config
│   ├── migrations/         # Database migrations
│   │   └── __init__.py
│   ├── models.py           # Database models
│   ├── tests.py            # Tests
│   ├── urls.py             # App-এর URLs (নিজে তৈরি করতে হয়)
│   └── views.py            # Views / logic
├── db.sqlite3              # SQLite Database
├── manage.py               # Django command tool
├── requirements.txt        # Dependencies
└── .gitignore
```

---

## ২. প্রতিটা ফোল্ডার ও ফাইলের কাজ

### 🔹 `venv/` — Virtual Environment

Python ও pip-এর আলাদা পরিবেশ। কখনো git-এ যাবে না।

---

### 🔹 `config/` — Project Configuration

`django-admin startproject config .` দিয়ে তৈরি হয়।

#### `__init__.py`

এই ফাইলটা প্রিজেন্ট থাকলে Python বুঝে যে এই ফোল্ডারটা একটা package। খালি থাকতে পারে।

#### `settings.py`

প্রজেক্টের সব কনফিগারেশন এখানে:
- Installed apps
- Database config
- Templates
- Static files
- Security settings
- Middleware

#### `urls.py`

প্রজেক্টের মূল URL routing। কোন URL-এ কোন view চলবে তা এখানে লেখা হয়।

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
]
```

#### `wsgi.py`

**Web Server Gateway Interface**। Production-এ Django চালানোর জন্য ব্যবহৃত হয় (Apache, Nginx-সহ)।

#### `asgi.py`

**Asynchronous Server Gateway Interface**। Async support-এর জন্য (Django 3.0+)।

---

### 🔹 `blog/` — App Folder

`python manage.py startapp blog` দিয়ে তৈরি হয়।

#### `__init__.py`

App-কে Python package হিসেবে চিহ্নিত করে।

#### `admin.py`

Django Admin panel-এ model register করার জন্য।

```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

#### `apps.py`

App-এর কনফিগারেশন।

```python
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
```

#### `migrations/`

Database-এ পরিবর্তন আসলে (নতুন table, নতুন column) এখানে migration ফাইল তৈরি হয়।

```
migrations/
├── __init__.py
├── 0001_initial.py
├── 0002_post_slug.py
└── ...
```

#### `models.py`

Database table তৈরি করার জন্য model লেখা হয়।

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

#### `tests.py`

App-এর টেস্ট লেখা হয় এখানে।

```python
from django.test import TestCase
from .models import Post

class PostModelTest(TestCase):
    def test_create_post(self):
        post = Post.objects.create(title="টেস্ট", content="কন্টেন্ট")
        self.assertEqual(post.title, "টেস্ট")
```

#### `views.py`

ব্যবহারকারীর request পেয়ে response দেওয়ার লজিক এখানে।

```python
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>স্বাগতম</h1>")
```

#### `urls.py` (নিজে তৈরি করতে হয়)

App-এর URL routing। প্রজেক্টের `urls.py` থেকে include করা হয়।

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
]
```

#### `templates/` (নিজে তৈরি করতে হয়)

HTML template ফাইল থাকে এখানে।

```
blog/
└── templates/
    └── blog/
        ├── base.html
        ├── home.html
        └── post_detail.html
```

#### `static/` (নিজে তৈরি করতে হয়)

CSS, JS, images থাকে এখানে।

```
blog/
└── static/
    └── blog/
        ├── css/
        ├── js/
        └── images/
```

---

### 🔹 `db.sqlite3` — Database

SQLite database ফাইল। Development-এ ব্যবহৃত হয়। Production-এ PostgreSQL বা MySQL ব্যবহার করা হয়।

> ⚠️ এটা কখনো git-এ commit করা উচিত না।

---

### 🔹 `manage.py` — Django Command Tool

Django-এর সব command চালানোর জন্য ব্যবহৃত হয়।

```bash
python manage.py runserver          # Server চালু
python manage.py migrate            # Migration apply
python manage.py makemigrations     # নতুন migration
python manage.py createsuperuser    # Admin user
python manage.py startapp blog      # নতুন app
python manage.py shell              # Django shell
python manage.py collectstatic      # Static files collect
python manage.py test               # টেস্ট চালু
```

---

### 🔹 `requirements.txt` — Dependencies

প্রজেক্টের সব package ও version।

```
Django==4.2.0
djangorestframework==3.14.0
```

---

### 🔹 `.gitignore`

যে ফাইলগুলো git-এ যাবে না তা এখানে লেখা।

```gitignore
venv/
__pycache__/
*.pyc
db.sqlite3
.env
```

---

## ৩. MTV Architecture

Django **MTV (Model-Template-View)** pattern অনুসরণ করে।

```
URL → View → Model
           ↓
        Template
           ↓
       Response
```

| উপাদান | কাজ |
|--------|-----|
| **Model** | Database-এর সাথে কথা বলে (`models.py`) |
| **Template** | User-কে দেখানো HTML (`templates/`) |
| **View** | লজিক, request process করে response দেয় (`views.py`) |
| **URL** | কোন URL-এ কোন view চলবে (`urls.py`) |

### Request Flow:

1. User URL-এ request পাঠায়
2. `urls.py` URL-কে view-এর সাথে match করে
3. View model থেকে data নেয়
4. View template-এ data পাঠায়
5. Template HTML render করে
6. View response হিসেবে user-কে দেয়

---

## ৪. একাধিক App সহ Project Structure

বড় প্রজেক্টে একাধিক app থাকে:

```
my_project/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── accounts/               # User authentication
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/accounts/
├── blog/                   # Blog posts
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/blog/
├── shop/                   # E-commerce
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/shop/
├── templates/              # Project-level templates (base.html)
├── static/                 # Project-level static files
├── media/                  # User-uploaded files
├── manage.py
└── requirements.txt
```

---

## ৫. Project-level vs App-level

### Project-level:

```
config/
├── settings.py        # সব config
├── urls.py            # মূল routing
templates/             # সকল app-এর জন্য common templates
static/                # common CSS/JS
media/                 # user uploads
```

### App-level:

```
blog/
├── models.py          # blog-এর models
├── views.py           # blog-এর views
├── urls.py            # blog-এর URLs
├── templates/blog/    # blog-এর templates
└── static/blog/       # blog-এর static files
```

---

## ৬. Templates Structure

Django-এ templates সাজানোর সেরা পদ্ধতি:

```
templates/
├── base.html              # সব template-এর parent
├── blog/
│   ├── post_list.html
│   └── post_detail.html
├── accounts/
│   ├── login.html
│   └── register.html
└── shop/
    ├── product_list.html
    └── product_detail.html
```

### base.html:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

### child template:

```html
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
<h1>স্বাগতম</h1>
{% endblock %}
```

---

## ৭. Static Files Structure

```
static/
├── css/
│   ├── base.css
│   └── style.css
├── js/
│   ├── main.js
│   └── script.js
└── images/
    ├── logo.png
    └── banner.jpg
```

### `settings.py`-এ:

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
```

---

## ৮. সেরা প্র্যাকটিস (Best Practices)

1. ✅ প্রতিটা ফিচারের জন্য আলাদা app বানান
2. ✅ App-এর নাম ছোট ও অর্থপূর্ণ রাখুন (blog, accounts, shop)
3. ✅ `templates/` এবং `static/` ফোল্ডার app-এর ভেতরে রাখুন
4. ✅ Project-level `templates/`-এ `base.html` রাখুন
5. ✅ `db.sqlite3` git-এ যাবে না
6. ✅ `requirements.txt` আপডেট রাখুন
7. ❌ সব কিছু একটা app-এ ভরে ফেলবেন না

---

## ৯. Practical Exercise

নিচের structure অনুযায়ী একটা প্রজেক্ট তৈরি করুন:

```
my_blog_project/
├── venv/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── blog/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   │   └── blog/
│   │       ├── base.html
│   │       └── home.html
│   └── static/
│       └── blog/
│           └── css/
│               └── style.css
├── templates/
│   └── base.html
├── static/
│   ├── css/
│   └── images/
├── manage.py
├── requirements.txt
└── .gitignore
```

ধাপগুলো:

```bash
# ১. প্রজেক্ট তৈরি
django-admin startproject config .

# ২. App তৈরি
python manage.py startapp blog

# ৩. App register (settings.py-এ)
# INSTALLED_APPS এ "blog" যোগ করুন

# ৪. App-এর templates ও static ফোল্ডার তৈরি
mkdir blog\templates\blog
mkdir blog\static\blog\css

# ৫. Project-level templates ও static তৈরি
mkdir templates
mkdir static\css
mkdir static\images

# ৬. blog/urls.py তৈরি করুন

# ৭. config/urls.py-এ include করুন
```

---

## 🎯 আজকের Key Takeaways

1. **`config/`** — প্রজেক্টের কনফিগারেশন (settings, urls, wsgi, asgi)
2. **App folder** — প্রতিটা ফিচারের জন্য আলাদা (models, views, admin, tests)
3. **`manage.py`** — Django-এর সব command চালানোর টুল
4. **`db.sqlite3`** — Development database
5. **`templates/`** — HTML ফাইল
6. **`static/`** — CSS, JS, images
7. **MTV Architecture** — Model, Template, View
8. একাধিক app-এ প্রজেক্ট ভাগ করা ভালো প্র্যাকটিস
9. Project-level ও App-level আলাদা থাকে

---

## ❓ অনুশীলনী প্রশ্ন

1. Django প্রজেক্টের মূল ফোল্ডারগুলো কী কী?
2. `config/` ফোল্ডারের কাজ কী?
3. `manage.py` দিয়ে কী কী কাজ করা যায়?
4. App-এর মধ্যে কোন কোন ফাইল থাকে?
5. `migrations/` ফোল্ডারের কাজ কী?
6. MTV Architecture কী?
7. Project-level ও App-level templates এর পার্থক্য কী?
8. `db.sqlite3` কেন git-এ commit করা উচিত না?
