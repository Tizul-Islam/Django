# Django: Templates ও Template Language 🎨

Django-এ **Template** হলো HTML ফাইল যেখানে Django-এর ট্যাগ ও ফিল্টার ব্যবহার করে dynamic কন্টেন্ট দেখানো হয়। এটা Django-এর MTV architecture-এর T (Template) অংশ।

---

## ১. Template কী এবং কেন দরকার?

Template হলো এমন একটা ফাইল যেখানে static HTML থাকে এবং Django-এর স্পেশাল সিনট্যাক্স (`{{ }}` এবং `{% %}`) ব্যবহার করে dynamic data দেখানো যায়।

### সুবিধা:
- 🎨 HTML ও Python আলাদা থাকে
- 🔁 একই template বারবার ব্যবহার করা যায় (reusable)
- 📊 database থেকে data সহজে দেখানো যায়
- 🧩 template inheritance দিয়ে code reuse

---

## ২. Template ফোল্ডার সেটআপ

### App-level Template:

প্রতিটা app-এর মধ্যে `templates` ফোল্ডার থাকতে হবে।

```
blog/
├── templates/
│   └── blog/
│       ├── base.html
│       ├── home.html
│       └── post_list.html
├── views.py
└── models.py
```

### Project-level Template:

সব app-এর জন্য common template রাখতে প্রজেক্ট রুটে `templates` ফোল্ডার।

```
my_project/
├── templates/
│   ├── base.html
│   └── 404.html
├── blog/
│   └── templates/
│       └── blog/
│           └── ...
└── config/
    └── settings.py
```

### settings.py-এ config:

```python
# config/settings.py
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # project-level templates
        "APP_DIRS": True,                   # app-level templates
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

---

## ৩. প্রথম Template তৈরি করা

### ধাপ ১: Template ফাইল তৈরি করুন

`blog/templates/blog/home.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>আমার ব্লগ</title>
</head>
<body>
    <h1>স্বাগতম! আমাদের ব্লগে</h1>
    <p>এটা আমাদের প্রথম Django template।</p>
</body>
</html>
```

### ধাপ ২: View থেকে render করুন

```python
# blog/views.py
from django.shortcuts import render

def home(request):
    return render(request, "blog/home.html")
```

### ধাপ ৩: URL যুক্ত করুন

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
]
```

এখন `http://127.0.0.1:8000/` এ গেলে template দেখা যাবে।

---

## ৪. Template Language — মূল সিনট্যাক্স

Django Template Language-এ মূলত তিন ধরনের সিনট্যাক্স:

### ১. Variable: `{{ variable }}` — মান দেখানো

```html
<p>নাম: {{ name }}</p>
<p>বয়স: {{ age }}</p>
```

### ২. Tag: `{% tag %}` — লজিক (if, for, block)

```html
{% if user.is_authenticated %}
    <p>স্বাগতম, {{ user.username }}!</p>
{% else %}
    <p>লগইন করুন</p>
{% endif %}

{% for post in posts %}
    <h2>{{ post.title }}</h2>
{% endfor %}
```

### ৩. Comment: `{# comment #}` — মন্তব্য

```html
{# এটা একটা কমেন্ট, ব্রাউজারে দেখাবে না #}
```

---

## ৫. Variables দিয়ে Data দেখানো

### View থেকে data পাঠানো:

```python
def home(request):
    context = {
        "name": "রহিম",
        "age": 25,
        "city": "ঢাকা",
    }
    return render(request, "blog/home.html", context)
```

### Template-এ দেখানো:

```html
<h1>নাম: {{ name }}</h1>
<p>বয়স: {{ age }}</p>
<p>শহর: {{ city }}</p>
```

### Object-এর attribute:

```python
context = {
    "user": {"name": "রহিম", "email": "rahim@example.com"},
}
```

```html
<p>{{ user.name }}</p>
<p>{{ user.email }}</p>
```

### List element:

```python
context = {
    "fruits": ["আপেল", "কমলা", "আম"],
}
```

```html
<p>{{ fruits.0 }}</p>  <!-- আপেল -->
<p>{{ fruits.1 }}</p>  <!-- কমলা -->
```

---

## ৬. Template Tags

### ১. `{% if %}` — শর্ত

```html
{% if age >= 18 %}
    <p>আপনি প্রাপ্তবয়স্ক</p>
{% elif age >= 13 %}
    <p>আপনি কিশোর</p>
{% else %}
    <p>আপনি শিশু</p>
{% endif %}
```

### ২. `{% for %}` — loop

```html
<ul>
{% for post in posts %}
    <li>{{ post.title }}</li>
{% endfor %}
</ul>
```

### `empty` দিয়ে খালি list:

```html
<ul>
{% for post in posts %}
    <li>{{ post.title }}</li>
{% empty %}
    <li>কোনো পোস্ট নেই</li>
{% endfor %}
</ul>
```

### `forloop` variable:

```html
{% for post in posts %}
    <p>{{ forloop.counter }}. {{ post.title }}</p>
{% endfor %}
```

| Variable | মানে |
|----------|------|
| `forloop.counter` | ১ থেকে শুরু |
| `forloop.counter0` | ০ থেকে শুরু |
| `forloop.revcounter` | উল্টো গণনা |
| `forloop.first` | প্রথম হলে True |
| `forloop.last` | শেষ হলে True |

---

## ৭. Filters

Filter হলো variable-এর মান পরিবর্তন করার জন্য। `|` দিয়ে ব্যবহার করা হয়।

### সাধারণ Filters:

| Filter | কাজ | উদাহরণ |
|--------|------|--------|
| `upper` | বড় অক্ষর | `{{ name|upper }}` |
| `lower` | ছোট অক্ষর | `{{ name|lower }}` |
| `title` | প্রতিটা শব্দের প্রথম অক্ষর বড় | `{{ name|title }}` |
| `length` | দৈর্ঘ্য | `{{ list|length }}` |
| `date` | তারিখ ফরম্যাট | `{{ date|date:"d/m/Y" }}` |
| `truncatewords` | নির্দিষ্ট শব্দ পর্যন্ত | `{{ text|truncatewords:10 }}` |
| `truncatechars` | নির্দিষ্ট অক্ষর পর্যন্ত | `{{ text|truncatechars:50 }}` |
| `default` | ডিফল্ট মান | `{{ value|default:"N/A" }}` |
| `safe` | HTML escape না করা | `{{ html|safe }}` |
| `linebreaks` | newline কে `<br>`-এ রূপান্তর | `{{ text|linebreaks }}` |
| `cut` | নির্দিষ্ট অক্ষর মুছে ফেলা | `{{ text|cut:" " }}` |
| `join` | list-কে string-এ যোগ | `{{ list|join:", " }}` |

### উদাহরণ:

```html
<p>{{ name|upper }}</p>
<p>{{ bio|truncatewords:20 }}</p>
<p>{{ created_at|date:"F j, Y" }}</p>
<p>{{ description|default:"কোনো বিবরণ নেই" }}</p>
```

### Filter chain করা:

```html
<p>{{ name|upper|truncatewords:5 }}</p>
```

---

## ৮. Template Inheritance (উত্তরাধিকার)

Template inheritance মানে একটা base template থেকে child template বানানো। এতে কোড পুনরায় ব্যবহার করা যায়।

### base.html (Parent):

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}আমার সাইট{% endblock %}</title>
</head>
<body>
    <header>
        <nav>
            <a href="/">হোম</a>
            <a href="/about/">আমাদের সম্পর্কে</a>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 আমার সাইট</p>
    </footer>
</body>
</html>
```

### home.html (Child):

```html
<!-- blog/templates/blog/home.html -->
{% extends "base.html" %}

{% block title %}হোম{% endblock %}

{% block content %}
<h1>স্বাগতম!</h1>
<p>এটা হোম পেজ।</p>
{% endblock %}
```

### `{% block %}` — কন্টেন্টের জায়গা

`{% block name %} ... {% endblock %} দিয়ে child template কন্টেন্ট বসানোর জায়গা তৈরি করা হয়।

```html
{% block content %}
ডিফল্ট কন্টেন্ট (child না দিলে এটা দেখাবে)
{% endblock %}
```

### `{{ block.super }}` — Parent-এর কন্টেন্ট দেখানো

```html
{% block content %}
{{ block.super }}
<p>অতিরিক্ত কন্টেন্ট</p>
{% endblock %}
```

---

## ৯. `{% include %}` — Template যুক্ত করা

একটা template-এ অন্য template যুক্ত করার জন্য।

### sidebar.html:

```html
<!-- blog/templates/blog/sidebar.html -->
<aside>
    <h3>জনপ্রিয় পোস্ট</h3>
    <ul>
        <li>পোস্ট ১</li>
        <li>পোস্ট ২</li>
    </ul>
</aside>
```

### home.html:

```html
{% extends "base.html" %}

{% block content %}
<div class="main">
    <h1>হোম</h1>
</div>
{% include "blog/sidebar.html" %}
{% endblock %}
```

---

## ১০. `{% url %}` — URL reverse

Template-এ URL তৈরি করার জন্য hardcoded URL না লিখে `{% url %}` ব্যবহার করা ভালো।

```html
<a href="{% url 'home' %}">হোম</a>
<a href="{% url 'post_detail' post.id %}">বিস্তারিত</a>
```

### Namespace সহ:

```html
<a href="{% url 'blog:post_detail' post.id %}">বিস্তারিত</a>
```

---

## ১১. `{% csrf_token %}` — CSRF Protection

POST form-এ অবশ্যই `{% csrf_token %}` যোগ করতে হবে।

```html
<form method="POST">
    {% csrf_token %}
    <input type="text" name="name">
    <button type="submit">সাবমিট</button>
</form>
```

> ⚠️ এটা না থাকলে POST request কাজ করবে না।

---

## ১২. `{% static %}` — Static Files

CSS, JS, Images লোড করার জন্য।

### Template-এর শুরুতে:

```html
{% load static %}
```

### ব্যবহার:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/script.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

---

## ১৩. `{% load %}` — Custom Tags ও Filters লোড

```html
{% load static %}
{% load humanize %}  <!-- humanize app-এর filters -->
```

---

## ১৪. Conditional Expressions

### `{% if %}`-এ operators:

```html
{% if user.is_authenticated and user.is_staff %}
    <p>আপনি admin</p>
{% endif %}

{% if posts|length > 5 %}
    <p>অনেক পোস্ট আছে</p>
{% endif %}
```

### `{% ifequal %}`:

```html
{% ifequal status "active" %}
    <p>সক্রিয়</p>
{% endifequal %}
```

---

## ১৫. একটা সম্পূর্ণ উদাহরণ — Blog List Page

### base.html:

```html
<!-- templates/base.html -->
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}আমার ব্লগ{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <header>
        <h1><a href="{% url 'blog:home' %}">আমার ব্লগ</a></h1>
        <nav>
            <a href="{% url 'blog:home' %}">হোম</a>
            <a href="{% url 'blog:about' %}">আমাদের সম্পর্কে</a>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 আমার ব্লগ</p>
    </footer>
</body>
</html>
```

### post_list.html:

```html
<!-- blog/templates/blog/post_list.html -->
{% extends "base.html" %}

{% block title %}সব পোস্ট{% endblock %}

{% block content %}
<h1>সব পোস্ট</h1>

{% for post in posts %}
    <article>
        <h2>
            <a href="{% url 'blog:post_detail' post.id %}">{{ post.title }}</a>
        </h2>
        <p class="date">{{ post.created_at|date:"F j, Y" }}</p>
        <p>{{ post.content|truncatewords:30 }}</p>
    </article>
{% empty %}
    <p>কোনো পোস্ট নেই।</p>
{% endfor %}
{% endblock %}
```

### post_detail.html:

```html
<!-- blog/templates/blog/post_detail.html -->
{% extends "base.html" %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
<article>
    <h1>{{ post.title }}</h1>
    <p class="date">{{ post.created_at|date:"F j, Y" }}</p>
    <div class="content">{{ post.content|linebreaks }}</div>
</article>

<p><a href="{% url 'blog:post_list' %}">← সব পোস্ট</a></p>
{% endblock %}
```

### views.py:

```python
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/post_detail.html", {"post": post})
```

---

## ১৬. সেরা প্র্যাকটিস (Best Practices)

1. ✅ সব template-এর জন্য base template ব্যবহার করুন
2. ✅ `{% url %}` দিয়ে লিঙ্ক দিন (hardcoded না)
3. ✅ POST form-এ `{% csrf_token %}` যোগ করুন
4. ✅ static files-এর জন্য `{% static %}` ব্যবহার করুন
5. ✅ app-level template-এর নাম `app_name/template_name.html রাখুন
6. ✅ filters ব্যবহার করে data ফরম্যাট করুন
7. ❌ template-এ জটিল লজিক লিখবেন না (view/model-এ রাখুন)
8. ❌ template-এ raw Python কোড লিখবেন না

---

## ১৭. Practical Exercise

```html
{# ============ Exercise 1: Variable ============ #}
<p>নাম: {{ name }}</p>
<p>বয়স: {{ age }}</p>

{# ============ Exercise 2: Filter ============ #}
<p>{{ name|upper }}</p>
<p>{{ bio|truncatewords:10 }}</p>
<p>{{ date|date:"d/m/Y" }}</p>

{# ============ Exercise 3: if ============ #}
{% if age >= 18 %}
    <p>প্রাপ্তবয়স্ক</p>
{% else %}
    <p>অপ্রাপ্তবয়স্ক</p>
{% endif %}

{# ============ Exercise 4: for ============ #}
<ul>
{% for item in items %}
    <li>{{ forloop.counter }}. {{ item }}</li>
{% empty %}
    <li>কিছু নেই</li>
{% endfor %}
</ul>

{# ============ Exercise 5: Template Inheritance ============ #}
{# base.html #}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}সাইট{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

{# child.html #}
{% extends "base.html" %}
{% block title %}চাইল্ড{% endblock %}
{% block content %}
<h1>চাইল্ড কন্টেন্ট</h1>
{% endblock %}

{# ============ Exercise 6: Form ============ #}
<form method="POST">
    {% csrf_token %}
    <input type="text" name="name">
    <button type="submit">সাবমিট</button>
</form>

{# ============ Exercise 7: URL ============ #}
<a href="{% url 'home' %}">হোম</a>
<a href="{% url 'post_detail' post.id %}">বিস্তারিত</a>

{# ============ Exercise 8: Static ============ #}
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

---

## 🎯 আজকের Key Takeaways

1. **Template** = HTML + Django স্পেশাল সিনট্যাক্স
2. **`{{ variable }}`** — মান দেখানো
3. **`{% tag %}`** — লজিক (if, for, block)
4. **`{# comment #}`** — কমেন্ট
5. **Filters** — `|` দিয়ে variable পরিবর্তন (`upper`, `date`, `truncatewords`)
6. **Template Inheritance** — `{% extends %}` + `{% block %}`
7. **`{% include %}`** — অন্য template যুক্ত করা
8. **`{% url %}`** — URL reverse
9. **`{% csrf_token %}`** — POST form-এ বাধ্যতামূলক
10. **`{% static %}`** — static files লোড
11. **base.html** — সব template-এর parent

---

## ❓ অনুশীলনী প্রশ্ন

1. Django Template কী?
2. `{{ }}` এবং `{% %}` এর পার্থক্য কী?
3. Template Inheritance কী? কেন দরকার?
4. `{% block %}` এর কাজ কী?
5. কয়েকটা গুরুত্বপূর্ণ filter-এর নাম বলুন
6. `{% csrf_token %}` কেন দরকার?
7. `{% url %}` ব্যবহারের সুবিধা কী?
8. `{% include %}` এবং `{% extends %}` এর পার্থক্য কী?
9. `{{ block.super }}` এর কাজ কী?
10. একটা blog list template তৈরি করুন যেখানে প্রতিটা পোস্টের title ও date দেখাবে
