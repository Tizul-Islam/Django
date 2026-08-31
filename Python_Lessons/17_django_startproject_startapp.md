# Django: startproject ও startapp 🚀

Django install হয়ে গেলে পরের ধাপ হলো প্রজেক্ট তৈরি করা। এই লেসনে শিখবো `django-admin startproject` ও `python manage.py startapp` দিয়ে প্রজেক্ট ও app তৈরি করা।

---

## ১. startproject — Django প্রজেক্ট তৈরি

### `django-admin startproject` কী?

এটা একটা command যা Django-এর একটা নতুন প্রজেক্ট তৈরি করে। প্রজেক্ট হলো পুরো ওয়েবসাইট/অ্যাপ্লিকেশনের কনফিগারেশন।

### সিনট্যাক্স:

```bash
django-admin startproject project_name
```

### উদাহরণ:

```bash
django-admin startproject myproject
```

এই কমান্ডটা নিচের কাঠামো তৈরি করবে:

```
myproject/
├── manage.py
└── myproject/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

### প্রতিটা ফাইলের কাজ:

| ফাইল | কাজ |
|------|------|
| `manage.py` | Django-এর কমান্ড লাইন টুল (runserver, migrate ইত্যাদি) |
| `__init__.py` | এই ফোল্ডারকে Python package হিসেবে চিহ্নিত করে |
| `settings.py` | প্রজেক্টের সব কনফিগারেশন (database, installed apps, templates) |
| `urls.py` | URL routing — কোন URL-এ কোন view চলবে |
| `wsgi.py` | Web Server Gateway Interface (production-এ ব্যবহৃত) |
| `asgi.py` | Asynchronous Server Gateway Interface (async support) |

---

## ২. startproject করার বিভিন্ন উপায়

### Method 1: বর্তমান ফোল্ডারে প্রজেক্ট তৈরি (`.` দিয়ে)

বর্তমান directory-তেই প্রজেক্ট ফাইলগুলো তৈরি করতে চাইলে শেষে `.` ব্যবহার করুন:

```bash
django-admin startproject config .
```

ফলাফল:
```
আপনার_ফোল্ডার/
├── manage.py
└── config/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

> 💡 এই পদ্ধতিটা বেশি ব্যবহৃত হয়, কারণ প্রজেক্টের নাম `config` রাখলে বোঝা সহজ হয় এটা configuration ফোল্ডার।

### Method 2: আলাদা ফোল্ডারে তৈরি

```bash
django-admin startproject myproject
```

ফলাফল:
```
আপনার_ফোল্ডার/
└── myproject/
    ├── manage.py
    └── myproject/
        ├── settings.py
        └── ...
```

---

## ৩. Development Server চালু করা

প্রজেক্ট তৈরি হওয়ার পর চেক করুন সব ঠিক আছে কিনা:

```bash
python manage.py runserver
```

ব্রাউজারে খুলুন: **http://127.0.0.1:8000/**

Django-এর স্বাগতম পেজ দেখা যাবে।

### অন্য Port-এ চালু:

```bash
python manage.py runserver 8080
```

### নির্দিষ্ট IP দিয়ে:

```bash
python manage.py runserver 0.0.0.0:8000
```

### Server বন্ধ:

`Ctrl + C` চাপুন।

---

## ৪. startapp — Django App তৈরি

### App কী?

Django প্রজেক্টে **App** হলো একটা নির্দিষ্ট ফিচার বা ফাংশনালিটির জন্য আলাদা মডিউল। যেমন:
- `blog` — ব্লগ পোস্টের জন্য
- `accounts` — ব্যবহারকারী authentication এর জন্য
- `shop` — ই-কমার্স এর জন্য

একটা প্রজেক্টে একাধিক app থাকতে পারে।

### সিনট্যাক্স:

```bash
python manage.py startapp app_name
```

### উদাহরণ:

```bash
python manage.py startapp blog
```

ফলাফল:
```
blog/
├── __init__.py
├── admin.py
├── apps.py
├── migrations/
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

### প্রতিটা ফাইলের কাজ:

| ফাইল | কাজ |
|------|------|
| `__init__.py` | Python package হিসেবে চিহ্নিত |
| `admin.py` | Django Admin panel-এ model register করা |
| `apps.py` | App-এর কনফিগারেশন |
| `migrations/` | Database migrations থাকে এখানে |
| `models.py` | Database table (model) তৈরি করা |
| `tests.py` | App-এর টেস্ট লেখা |
| `views.py` | ব্যবহারকারীকে কী দেখাবে তা নির্ধারণ (logic) |

---

## ৫. App-কে প্রজেক্টে যুক্ত করা

App তৈরি করার পর `settings.py`-এর `INSTALLED_APPS` এ যোগ করতে হবে।

### `settings.py` খুলুন:

```python
# config/settings.py

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # আমাদের তৈরি করা app
    "blog",
]
```

> ⚠️ অবশ্যই নতুন app এর নাম যোগ করতে হবে, না করলে app কাজ করবে না।

---

## ৬. প্রথম View তৈরি করা

`blog/views.py`-এ একটা view লিখুন:

```python
# blog/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>স্বাগতম! আমাদের ব্লগে</h1>")
```

### URL যুক্ত করা:

প্রথমে `blog/urls.py` ফাইল তৈরি করুন:

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
]
```

তারপর প্রজেক্টের `config/urls.py`-এ যুক্ত করুন:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
]
```

এখন `http://127.0.0.1:8000/` এ গেলে আপনার বার্তা দেখা যাবে।

---

## ৭. পুরো প্রক্রিয়া একসাথে (Step-by-Step)

### ধাপ ১: Environment সেটআপ

```bash
# venv তৈরি
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Django install
pip install django
```

### ধাপ ২: Project তৈরি

```bash
django-admin startproject config .
```

### ধাপ ৩: App তৈরি

```bash
python manage.py startapp blog
```

### ধাপ ৪: App register করা

`config/settings.py` খুলে `INSTALLED_APPS` এ `blog` যোগ করুন।

### ধাপ ৫: Migration চালানো

```bash
python manage.py migrate
```

### ধাপ ৬: Server চালু

```bash
python manage.py runserver
```

ব্রাউজারে: **http://127.0.0.1:8000/**

---

## ৮. Django Project Structure (Final)

সব ঠিকঠাক হলে আপনার প্রজেক্ট এরকম দেখাবে:

```
my_django_project/
├── venv/                    # Virtual Environment
├── config/                  # Project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── blog/                    # আপনার App
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py              # নতুন তৈরি করা
│   └── views.py
├── db.sqlite3               # SQLite Database
├── manage.py
├── .gitignore
└── requirements.txt
```

---

## ৯. গুরুত্বপূর্ণ manage.py কমান্ডসমূহ

| কমান্ড | কাজ |
|--------|------|
| `python manage.py runserver` | Development server চালু |
| `python manage.py startapp blog` | নতুন app তৈরি |
| `python manage.py migrate` | Database-এ migrations apply করা |
| `python manage.py makemigrations` | নতুন migration ফাইল তৈরি |
| `python manage.py createsuperuser` | Admin user তৈরি |
| `python manage.py shell` | Django shell চালু |
| `python manage.py collectstatic` | Static files collect করা |
| `python manage.py check` | প্রজেক্টে সমস্যা আছে কিনা চেক |
| `python manage.py test` | টেস্ট চালানো |

---

## ১০. সাধারণ ভুল ও সমাধান

### ভুল ১: `django-admin` command পাওয়া যাচ্ছে না

**কারণ:** Django install হয়নি অথবা venv activate হয়নি।

**সমাধান:**
```bash
pip install django
# অথবা
python -m django startproject myproject
```

### ভুল ২: App কাজ করছে না

**কারণ:** `settings.py`-এ `INSTALLED_APPS` এ app যোগ করা হয়নি।

**সমাধান:** `INSTALLED_APPS` এ app এর নাম যোগ করুন।

### ভুল ৩: `python manage.py runserver` চলছে না

**কারণ:** `manage.py` ফাইলের directory তে নেই।

**সমাধান:** `manage.py` যে ফোল্ডারে আছে সেখানে যান, অথবা `cd` দিয়ে সেই ফোল্ডারে প্রবেশ করুন।

### ভুল ৪: Port already in use

**কারণ:** অন্য server ওই port-এ চলছে।

**সমাধান:** অন্য port ব্যবহার করুন:
```bash
python manage.py runserver 8080
```

---

## ১১. Practical Exercise

নিচের ধাপগুলো করে দেখুন:

```bash
# ১. নতুন ফোল্ডার তৈরি ও প্রবেশ
mkdir my_blog
cd my_blog

# ২. Virtual Environment তৈরি ও Activate
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac

# ৩. Django install
pip install django

# ৪. Project তৈরি (বর্তমান ফোল্ডারে)
django-admin startproject config .

# ৫. Blog app তৈরি
python manage.py startapp blog

# ৬. settings.py-এ blog যোগ করুন (ম্যানুয়ালি)

# ৭. Migration চালান
python manage.py migrate

# ৮. Server চালু
python manage.py runserver

# ৯. ব্রাউজারে দেখুন: http://127.0.0.1:8000/
```

এখন একটা সহজ view যোগ করুন:

```python
# blog/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>আমার প্রথম Django পেজ!</h1>")
```

```python
# blog/urls.py (নতুন ফাইল তৈরি করুন)
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
]
```

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
]
```

এখন `http://127.0.0.1:8000/` খুলুন — আপনার বার্তা দেখা যাবে! 🎉

---

## 🎯 আজকের Key Takeaways

### startproject:
1. `django-admin startproject project_name` — নতুন প্রজেক্ট তৈরি
2. `django-admin startproject config .` — বর্তমান ফোল্ডারে প্রজেক্ট তৈরি
3. `manage.py` — Django-এর কমান্ড লাইন টুল
4. `settings.py` — প্রজেক্টের কনফিগারেশন
5. `urls.py` — URL routing

### startapp:
1. `python manage.py startapp app_name` — নতুন app তৈরি
2. App তৈরির পর `settings.py`-এ `INSTALLED_APPS` এ যোগ করতে হবে
3. `models.py` — Database table
4. `views.py` — লজিক/রেসপন্স
5. `admin.py` — Admin panel register

### অন্যান্য:
1. `python manage.py runserver` — Server চালু
2. `python manage.py migrate` — Database migration
3. `python manage.py createsuperuser` — Admin user তৈরি

---

## ❓ অনুশীলনী প্রশ্ন

1. `django-admin startproject` এর কাজ কী?
2. `manage.py` ফাইলের গুরুত্ব কী?
3. `settings.py`-এ `INSTALLED_APPS` এর কাজ কী?
4. `python manage.py startapp` দিয়ে কী তৈরি হয়?
5. App তৈরির পর কী কাজ করতে হয়?
6. `python manage.py runserver` কমান্ডের কাজ কী?
7. `migrate` কমান্ড কী করে?
8. একটা Django প্রজেক্ট তৈরি করে তার মধ্যে `accounts` নামে একটা app যোগ করুন
