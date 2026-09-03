# Django: urls.py ও URL Routing 🌐

Django-এ URL routing মানে হলো কোন URL-এ কোন view (পেজ) দেখাবে তা নির্ধারণ করা। এটা Django-এর request-response চক্রের প্রথম ধাপ।

---

## ১. URL Routing কী এবং কেন দরকার?

কোনো ব্যবহারকারী যখন browser-এ কোনো URL টাইপ করে (যেমন `http://127.0.0.1:8000/blog/`), তখন Django সেই URL-কে মিলিয়ে দেখে কোন view function-কে কল করতে হবে।

### Request Flow:

```
User → URL → urls.py → View → Response
```

Django-এ URL mapping-এর কাজ করে `urls.py` ফাইল।

---

## ২. urls.py এর ধরন

Django-এ দুই ধরনের `urls.py` থাকে:

### ১. Project-level urls.py

`django-admin startproject` দিয়ে তৈরি হয়। প্রজেক্টের মূল URL routing এখানে।

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
]
```

### ২. App-level urls.py

প্রতিটা app-এর জন্য আলাদা `urls.py` তৈরি করতে হয়। Project-level থেকে `include()` দিয়ে যুক্ত করা হয়।

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
]
```

---

## ৩. `path()` ফাংশন

`path()` হলো URL pattern তৈরি করার মূল ফাংশন।

### সিনট্যাক্স:

```python
path(route, view, kwargs=None, name=None)
```

| প্যারামিটার | বিবরণ |
|------------|--------|
| `route` | URL pattern string |
| `view` | URL-এর জন্য view function |
| `kwargs` | view-এ extra arguments পাঠানো |
| `name` | URL-এর নাম (reverse lookup-এর জন্য) |

### উদাহরণ:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
```

---

## ৪. URL Patterns তৈরি করা

### সহজ URL:

```python
path("", views.home, name="home")           # http://127.0.0.1:8000/
path("about/", views.about, name="about")   # http://127.0.0.1:8000/about/
```

### URL-এ parameter (Dynamic URL):

```python
# int parameter
path("post/<int:post_id>/", views.post_detail, name="post_detail")
# http://127.0.0.1:8000/post/5/

# str parameter
path("profile/<str:username>/", views.profile, name="profile")
# http://127.0.0.1:8000/profile/rahim/

# slug parameter
path("article/<slug:article_slug>/", views.article, name="article")
# http://127.0.0.1:8000/article/my-first-post/
```

### Path Converters:

| Converter | বিবরণ | উদাহরণ |
|-----------|--------|--------|
| `str` | যেকোনো string (`/` ছাড়া) | `abc` |
| `int` | পূর্ণ সংখ্যা | `123` |
| `slug` | slug (letters, numbers, `-`, `_`) | `my-post` |
| `uuid` | UUID format | `075194d3-6885-417e-a8a8-6c931e272f00` |
| `path` | পুরো path including `/` | `a/b/c` |

### উদাহরণ:

```python
urlpatterns = [
    path("post/<int:id>/", views.post_detail),
    path("user/<str:username>/", views.user_profile),
    path("page/<slug:slug>/", views.page),
    path("docs/<path:subpath>/", views.docs),
]
```

---

## ৫. `include()` দিয়ে App URLs যুক্ত করা

বড় প্রজেক্টে প্রতিটা app-এর আলাদা `urls.py` থাকে। Project-level থেকে `include()` দিয়ে যুক্ত করা হয়।

### Project urls.py:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("accounts/", include("accounts.urls")),
]
```

### App urls.py (blog):

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),           # /blog/
    path("post/<int:id>/", views.post_detail),   # /blog/post/5/
    path("about/", views.about, name="about"),   # /blog/about/
]
```

### App urls.py (accounts):

```python
# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),     # /accounts/login/
    path("logout/", views.logout, name="logout"),  # /accounts/logout/
    path("register/", views.register, name="register"),  # /accounts/register/
]
```

---

## ৬. View Function এবং URL Parameter

URL থেকে parameter আসলে view function সেটা গ্রহণ করে।

```python
# blog/urls.py
path("post/<int:post_id>/", views.post_detail, name="post_detail")
```

```python
# blog/views.py
from django.http import HttpResponse

def post_detail(request, post_id):
    return HttpResponse(f"পোস্ট নম্বর: {post_id}")
```

`http://127.0.0.1:8000/blog/post/5/` এ গেলে দেখাবে: **পোস্ট নম্বর: 5**

### একাধিক Parameter:

```python
# urls.py
path("post/<int:year>/<int:month>/", views.post_archive, name="post_archive")
```

```python
# views.py
def post_archive(request, year, month):
    return HttpResponse(f"বছর: {year}, মাস: {month}")
```

---

## ৭. `name` এবং `reverse()` দিয়ে URL খোঁজা

URL-এর `name` দিয়ে anywhere থেকে URL খোঁজা যায়। যাতে URL পরিবর্তন করলে সব জায়গায় পরিবর্তন করতে না হয়।

### template-এ `{% url %}`:

```html
<a href="{% url 'home' %}">হোম</a>
<a href="{% url 'post_detail' post_id=5 %}">পোস্ট ৫</a>
```

### Python-এ `reverse()`:

```python
from django.urls import reverse

url = reverse("home")
# "/"

url = reverse("post_detail", kwargs={"post_id": 5})
# "/blog/post/5/"
```

### `redirect()`-এ ব্যবহার:

```python
from django.shortcuts import redirect, reverse

def my_view(request):
    return redirect(reverse("home"))
    # অথবা সরাসরি name দিয়ে:
    return redirect("home")
```

---

## ৮. Extra Arguments — `kwargs`

`path()`-এ `kwargs` দিয়ে view-এ অতিরিক্ত argument পাঠানো যায়।

```python
# urls.py
path("page/", views.page, kwargs={"page_name": "About"}, name="about_page")
```

```python
# views.py
def page(request, page_name):
    return HttpResponse(f"পেজ: {page_name}")
```

---

## ৯. `re_path()` — Regular Expression দিয়ে URL

জটিল URL pattern-এর জন্য regular expression ব্যবহার করা যায়।

```python
from django.urls import re_path

urlpatterns = [
    re_path(r"^post/(?P<year>[0-9]{4})/$", views.post_by_year),
    # http://127.0.0.1:8000/post/2023/
]
```

### সাধারণ regex:

| Pattern | মানে |
|---------|------|
| `^` | শুরু |
| `$` | শেষ |
| `[0-9]` | ০-৯ যেকোনো সংখ্যা |
| `[a-z]` | ছোট অক্ষর |
| `{4}` | ঠিক ৪টি অক্ষর |
| `+` | এক বা একাধিক |
| `*` | শূন্য বা একাধিক |

---

## ১০. URL Namespacing

একাধিক app-এ একই নামের URL থাকলে namespace ব্যবহার করা হয়।

### Project urls.py:

```python
urlpatterns = [
    path("blog/", include("blog.urls", namespace="blog")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
]
```

### App urls.py:

```python
# blog/urls.py
app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
]
```

### ব্যবহার:

```python
reverse("blog:home")          # /blog/
reverse("accounts:login")     # /accounts/login/
```

Template-এ:

```html
<a href="{% url 'blog:home' %}">ব্লগ হোম</a>
<a href="{% url 'accounts:login' %}">লগইন</a>
```

---

## ১১. Static ও Media Files-এর URL

Development-এ static ও media files serve করার জন্য URL যোগ করতে হয়।

```python
# config/urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
]

# Development-এর জন্য
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## ১২. 404 Error Page

যদি কোনো URL match না করে, Django 404 error দেয়।

### Custom 404 View:

```python
# config/urls.py
handler404 = "myapp.views.custom_404"
```

```python
# myapp/views.py
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, "404.html", status=404)
```

`settings.py`-এ `DEBUG = False` হলে কাজ করবে।

---

## ১৩. একটা সম্পূর্ণ উদাহরণ

### Project urls.py:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
]
```

### Blog urls.py:

```python
# blog/urls.py
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("post/<int:year>/<int:month>/", views.post_archive, name="post_archive"),
    path("profile/<str:username>/", views.profile, name="profile"),
]
```

### Blog views.py:

```python
# blog/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>স্বাগতম! আমাদের ব্লগে</h1>")

def about(request):
    return HttpResponse("<h1>আমাদের সম্পর্কে</h1>")

def contact(request):
    return HttpResponse("<h1>যোগাযোগ করুন</h1>")

def post_detail(request, post_id):
    return HttpResponse(f"<h1>পোস্ট নম্বর: {post_id}</h1>")

def post_archive(request, year, month):
    return HttpResponse(f"<h1>আর্কাইভ: {year} - {month}</h1>")

def profile(request, username):
    return HttpResponse(f"<h1>প্রোফাইল: {username}</h1>")
```

### URL Mapping:

| URL | View |
|-----|------|
| `/` | `home` |
| `/about/` | `about` |
| `/contact/` | `contact` |
| `/post/5/` | `post_detail` (post_id=5) |
| `/post/2023/10/` | `post_archive` (year=2023, month=10) |
| `/profile/rahim/` | `profile` (username=rahim) |

---

## ১৪. `urls.py` চেক করা

সব ঠিক আছে কিনা চেক করতে:

```bash
python manage.py check
```

সব URL pattern দেখতে:

```python
# Django shell-এ
from django.urls import get_resolver
resolver = get_resolver()
for url_pattern in resolver.url_patterns:
    print(url_pattern.pattern)
```

---

## ১৫. সেরা প্র্যাকটিস (Best Practices)

1. ✅ প্রতিটা app-এর আলাদা `urls.py` রাখুন
2. ✅ সব URL-এর `name` দিন
3. ✅ `namespace` ব্যবহার করুন একাধিক app-এ
4. ✅ Trailing slash (`/`) ব্যবহার করুন
5. ✅ Dynamic URL-এর জন্য path converter ব্যবহার করুন
6. ✅ `{% url %}` দিয়ে template-এ লিঙ্ক দিন
7. ❌ hardcoded URL লিখবেন না

---

## ১৬. Practical Exercise

```python
# ============ Exercise 1: Basic URLs ============
# blog/urls.py তৈরি করুন
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]

# blog/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("হোম পেজ")

def about(request):
    return HttpResponse("আমাদের সম্পর্কে")

def contact(request):
    return HttpResponse("যোগাযোগ")

# config/urls.py-এ যুক্ত করুন
# path("", include("blog.urls"))


# ============ Exercise 2: Dynamic URLs ============
# blog/urls.py
urlpatterns = [
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("user/<str:username>/", views.user_profile, name="user_profile"),
    path("date/<int:year>/<int:month>/", views.date_archive, name="date_archive"),
]

# blog/views.py
def post_detail(request, post_id):
    return HttpResponse(f"পোস্ট: {post_id}")

def user_profile(request, username):
    return HttpResponse(f"ইউজার: {username}")

def date_archive(request, year, month):
    return HttpResponse(f"তারিখ: {year}/{month}")


# ============ Exercise 3: Namespace ============
# config/urls.py
urlpatterns = [
    path("blog/", include("blog.urls", namespace="blog")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
]

# blog/urls.py
app_name = "blog"
urlpatterns = [
    path("", views.home, name="home"),
]

# accounts/urls.py
app_name = "accounts"
urlpatterns = [
    path("login/", views.login, name="login"),
]

# ব্যবহার
# reverse("blog:home") → /blog/
# reverse("accounts:login") → /accounts/login/
```

---

## 🎯 আজকের Key Takeaways

1. **URL Routing** — কোন URL-এ কোন view চলবে তা নির্ধারণ
2. **Project-level urls.py** — মূল routing, `include()` দিয়ে app যুক্ত
3. **App-level urls.py** — প্রতিটা app-এর আলাদা
4. **`path()`** — URL pattern তৈরি করা
5. **Path converters**: `int`, `str`, `slug`, `uuid`, `path`
6. **`include()`** — app-এর urls যুক্ত করা
7. **`name`** — URL-এর নাম, `reverse()` দিয়ে খোঁজা যায়
8. **`namespace`** — একাধিক app-এ একই নাম থাকলে ব্যবহার
9. **`kwargs`** — view-এ extra argument পাঠানো
10. **`re_path()`** — regular expression দিয়ে URL
11. **Trailing slash** — শেষে `/` রাখা ভালো

---

## ❓ অনুশীলনী প্রশ্ন

1. URL Routing কী?
2. Project-level ও App-level urls.py এর পার্থক্য কী?
3. `path()` ফাংশনের প্যারামিটারগুলো কী কী?
4. Path converters কী কী? উদাহরণ সহ বলুন
5. `include()` ফাংশনের কাজ কী?
6. URL-এর `name` attribute এর গুরুত্ব কী?
7. `reverse()` ফাংশন কীভাবে কাজ করে?
8. Namespace কেন ব্যবহার করা হয়?
9. Dynamic URL তৈরি করার নিয়ম কী?
10. একটা blog app তৈরি করুন যেখানে `post/<int:id>/` URL থাকবে এবং সেই id অনুযায়ী পোস্ট দেখাবে
