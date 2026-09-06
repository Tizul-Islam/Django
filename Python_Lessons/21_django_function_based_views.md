# Django: Function-Based Views (FBV) 🎯

Django-এ **View** হলো এমন একটা ফাংশন বা ক্লাস যা user-এর request পায় এবং response দেয়। Function-Based View মানে সাধারণ Python function দিয়ে view তৈরি করা।

---

## ১. View কী এবং কেন দরকার?

View হলো request-response চক্রের মূল অংশ। এটা:
- User-এর request গ্রহণ করে
- প্রয়োজনীয় লজিক চালায় (database থেকে data আনা, calculation ইত্যাদি)
- User-কে response দেয় (HTML page, JSON, redirect ইত্যাদি)

### Request → View → Response

```
Browser → URL → urls.py → View → Response (HTML/JSON)
```

---

## ২. Function-Based View এর মৌলিক কাঠামো

```python
from django.http import HttpResponse

def my_view(request):
    # লজিক এখানে
    return HttpResponse("হ্যালো, Django!")
```

### অংশসমূহ:
1. **`request`** — user-এর request object (HTTP method, headers, data ইত্যাদি)
2. **লজিক** — database query, calculation ইত্যাদি
3. **`return HttpResponse()`** — response ফেরত দেওয়া

---

## ৩. প্রথম FBV তৈরি করা

### ধাপ ১: View লিখুন

```python
# blog/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>স্বাগতম! আমাদের ব্লগে</h1>")
```

### ধাপ ২: URL যুক্ত করুন

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
]
```

### ধাপ ৩: Project urls.py-এ include করুন

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

## ৪. Response-এর প্রকারভেদ

Django-এ বিভিন্ন ধরনের response ফেরত দেওয়া যায়।

### ১. HttpResponse (সাধারণ টেক্সট/HTML)

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>হ্যালো</h1>")
```

### ২. render (Template সহ)

```python
from django.shortcuts import render

def home(request):
    return render(request, "home.html")
```

### ৩. JsonResponse (JSON data)

```python
from django.http import JsonResponse

def api_data(request):
    data = {"name": "রহিম", "age": 25}
    return JsonResponse(data)
```

### ৪. redirect (অন্য URL-এ পাঠানো)

```python
from django.shortcuts import redirect, reverse

def old_page(request):
    return redirect("home")  # URL name
    # অথবা সরাসরি URL:
    # return redirect("/about/")
```

### ৫. HttpResponseNotFound (404)

```python
from django.http import HttpResponseNotFound

def not_found(request):
    return HttpResponseNotFound("<h1>৪০৪: পেজ পাওয়া যায়নি</h1>")
```

---

## ৫. Request Object

`request` object-এ user-এর request-এর সব তথ্য থাকে।

### request-এর গুরুত্বপূর্ণ attribute:

| Attribute | বিবরণ | উদাহরণ |
|-----------|--------|--------|
| `request.method` | HTTP method | `"GET"` বা `"POST"` |
| `request.GET` | GET parameters | `request.GET.get("id")` |
| `request.POST` | POST data | `request.POST.get("name")` |
| `request.user` | logged-in user | `request.user.username` |
| `request.path` | URL path | `"/blog/post/5/"` |
| `request.headers` | HTTP headers | `request.headers["User-Agent"]` |
| `request.COOKIES` | cookies | `request.COOKIES.get("sessionid")` |

### উদাহরণ:

```python
def post_detail(request, post_id):
    print(request.method)      # GET
    print(request.path)        # /blog/post/5/
    print(request.GET.get("tab"))  # ?tab=comments হলে comments
    return HttpResponse(f"পোস্ট: {post_id}")
```

---

## ৬. URL থেকে Parameter গ্রহণ

```python
# urls.py
path("post/<int:post_id>/", views.post_detail, name="post_detail")
path("user/<str:username>/", views.profile, name="profile")
```

```python
# views.py
def post_detail(request, post_id):
    return HttpResponse(f"পোস্ট নম্বর: {post_id}")

def profile(request, username):
    return HttpResponse(f"ইউজার: {username}")
```

---

## ৭. GET ও POST Method হ্যান্ডেল

### GET Request:

```python
def search(request):
    query = request.GET.get("q", "")
    return HttpResponse(f"সার্চ: {query}")
```

URL: `http://127.0.0.1:8000/search/?q=django`

### POST Request:

```python
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        # database-এ save করার লজিক
        return HttpResponse(f"পোস্ট তৈরি হয়েছে: {title}")
    else:
        return HttpResponse("GET request")
```

### Method অনুযায়ী আলাদা কাজ:

```python
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        # ইমেইল পাঠানো বা database-এ save
        return HttpResponse(f"ধন্যবাদ {name}! আপনার বার্তা পেয়েছি।")
    else:
        return HttpResponse("যোগাযোগ ফর্ম")
```

---

## ৮. Context দিয়ে Template Render

`render()` দিয়ে template-এ data পাঠানো যায়।

### বেসিক:

```python
from django.shortcuts import render

def home(request):
    context = {
        "name": "রহিম",
        "age": 25,
        "city": "ঢাকা",
    }
    return render(request, "home.html", context)
```

### Template (home.html):

```html
<h1>নাম: {{ name }}</h1>
<p>বয়স: {{ age }}</p>
<p>শহর: {{ city }}</p>
```

### Database থেকে data:

```python
from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "post_list.html", context)
```

---

## ৯. `render()` ফাংশন বিস্তারিত

### সিনট্যাক্স:

```python
render(request, template_name, context=None, content_type=None, status=None, using=None)
```

| প্যারামিটার | বিবরণ |
|------------|--------|
| `request` | request object |
| `template_name` | template ফাইলের নাম |
| `context` | template-এ পাঠানো data (dictionary) |
| `status` | HTTP status code (ডিফল্ট 200) |

### উদাহরণ:

```python
def custom_404(request):
    return render(request, "404.html", status=404)
```

---

## ১০. `get_object_or_404()` — সহজে 404

কোনো object না পেলে স্বয়ংক্রিয়ভাবে 404 error দেয়।

```python
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "post_detail.html", {"post": post})
```

`Post` model-এ id=post_id আছে কিনা চেক করে, না থাকলে 404 page দেখায়।

### ছাড়া এটা কেমন হতো:

```python
from django.http import Http404

def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("পোস্ট পাওয়া যায়নি")
    return render(request, "post_detail.html", {"post": post})
```

---

## ১১. `redirect()` — পেজ সরানো

```python
from django.shortcuts import redirect, reverse
from .models import Post

def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        post = Post.objects.create(title=title)
        # নতুন পোস্টের detail পেজে পাঠান
        return redirect("post_detail", post_id=post.id)
    return render(request, "create_post.html")
```

### redirect-এর প্রকারভেদ:

```python
# URL name দিয়ে
return redirect("home")

# URL name + parameter
return redirect("post_detail", post_id=5)

# সরাসরি URL
return redirect("/about/")

# full URL
return redirect("https://example.com")
```

---

## ১২. Decorators — View-এর জন্য

Django-এ কিছু built-in decorator view-এর আচরণ পরিবর্তন করে।

### `@require_http_methods` — নির্দিষ্ট method:

```python
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def my_view(request):
    pass
```

### `@require_GET` ও `@require_POST`:

```python
from django.views.decorators.http import require_GET, require_POST

@require_GET
def only_get(request):
    pass

@require_POST
def only_post(request):
    pass
```

### `@login_required` — login বাধ্যতামূলক:

```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "dashboard.html")
```

Login না করলে login page-এ পাঠাবে।

### `@staff_member_required` — admin/staff:

```python
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_report(request):
    return render(request, "admin_report.html")
```

---

## ১৩. একটা সম্পূর্ণ উদাহরণ — Blog App

### models.py:

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

### views.py:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/post_detail.html", {"post": post})

def post_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        post = Post.objects.create(title=title, content=content)
        return redirect("post_detail", post_id=post.id)
    return render(request, "blog/post_create.html")

@require_POST
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect("post_list")
```

### urls.py:

```python
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("post/create/", views.post_create, name="post_create"),
    path("post/<int:post_id>/delete/", views.post_delete, name="post_delete"),
]
```

### Templates:

`blog/post_list.html`:
```html
<h1>সব পোস্ট</h1>
{% for post in posts %}
    <div>
        <h2>{{ post.title }}</h2>
        <p>{{ post.content|truncatewords:30 }}</p>
        <a href="{% url 'blog:post_detail' post.id %}">বিস্তারিত</a>
    </div>
{% endfor %}
```

`blog/post_detail.html`:
```html
<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>
<p>তারিখ: {{ post.created_at }}</p>
<form method="POST" action="{% url 'blog:post_delete' post.id %}">
    {% csrf_token %}
    <button type="submit">মুছুন</button>
</form>
```

`blog/post_create.html`:
```html
<h1>নতুন পোস্ট</h1>
<form method="POST">
    {% csrf_token %}
    <input type="text" name="title" placeholder="শিরোনাম">
    <textarea name="content" placeholder="কন্টেন্ট"></textarea>
    <button type="submit">প্রকাশ করুন</button>
</form>
```

---

## ১৪. সাধারণ ভুল ও সমাধান

### ভুল ১: `request` parameter না দেওয়া

```python
# ❌ ভুল
def home():
    return HttpResponse("হ্যালো")

# ✅ সঠিক
def home(request):
    return HttpResponse("হ্যালো")
```

### ভুল ২: Template পাওয়া যাচ্ছে না

`settings.py`-এ `TEMPLATES`-এর `APP_DIRS: True` রাখুন অথবা `DIRS` এ path যোগ করুন।

### ভুল ৩: `render` না ব্যবহার করে string ফেরত দেওয়া

```python
# ❌ ভুল
def home(request):
    return "<h1>হ্যালো</h1>"  # এটা response নয়

# ✅ সঠিক
from django.http import HttpResponse
def home(request):
    return HttpResponse("<h1>হ্যালো</h1>")
```

---

## ১৫. সেরা প্র্যাকটিস (Best Practices)

1. ✅ প্রতিটা view-এর নাম অর্থপূর্ণ রাখুন
2. ✅ `get_object_or_404()` ব্যবহার করুন
3. ✅ Method অনুযায়ী আলাদা করুন (GET/POST)
4. ✅ CSRF token ফর্মে যোগ করুন
5. ✅ Decorators ব্যবহার করুন (login_required ইত্যাদি)
6. ✅ View-এ কম লজিক রাখুন, বেশি লজিক model বা service-এ
7. ❌ এক view-এ অনেক কিছু করবেন না

---

## ১৬. Practical Exercise

```python
# ============ Exercise 1: Basic FBV ============
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>স্বাগতম</h1>")


# ============ Exercise 2: Dynamic URL ============
def user_profile(request, username):
    return HttpResponse(f"<h1>ইউজার: {username}</h1>")


# ============ Exercise 3: GET parameters ============
def search(request):
    query = request.GET.get("q", "")
    return HttpResponse(f"সার্চ করছি: {query}")


# ============ Exercise 4: POST handler ============
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        return HttpResponse(f"ধন্যবাদ {name}!")
    return HttpResponse("যোগাযোগ করুন")


# ============ Exercise 5: Template render ============
from django.shortcuts import render

def about(request):
    context = {"team": ["রহিম", "করিম", "সালাম"]}
    return render(request, "about.html", context)


# ============ Exercise 6: get_object_or_404 ============
from django.shortcuts import get_object_or_404

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "post_detail.html", {"post": post})


# ============ Exercise 7: redirect ============
from django.shortcuts import redirect

def old_url(request):
    return redirect("home")


# ============ Exercise 8: login_required ============
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "dashboard.html")
```

---

## 🎯 আজকের Key Takeaways

1. **FBV** — সাধারণ Python function দিয়ে view তৈরি
2. **`request`** — user-এর request object
3. **Response প্রকার**: `HttpResponse`, `render`, `JsonResponse`, `redirect`
4. **GET/POST** — `request.method` দিয়ে চেক করা
5. **URL parameter** — view-এ parameter হিসেবে আসে
6. **`render()`** — template সহ response
7. **`get_object_or_404()`** — object না পেলে 404
8. **`redirect()`** — অন্য URL-এ পাঠানো
9. **Decorators**: `@login_required`, `@require_POST` ইত্যাদি
10. **Context** — template-এ data পাঠানো (dictionary)

---

## ❓ অনুশীলনী প্রশ্ন

1. Function-Based View কী?
2. View-এর কাজ কী?
3. `request` object-এর গুরুত্বপূর্ণ attribute কী কী?
4. `HttpResponse` ও `render` এর পার্থক্য কী?
5. GET ও POST request কীভাবে হ্যান্ডেল করা যায়?
6. `get_object_or_404()` এর কাজ কী?
7. `redirect()` কীভাবে কাজ করে?
8. `@login_required` decorator এর কাজ কী?
9. Context কী এবং কেন ব্যবহার করা হয়?
10. একটা blog app তৈরি করুন যেখানে post list, detail, create ও delete view থাকবে
