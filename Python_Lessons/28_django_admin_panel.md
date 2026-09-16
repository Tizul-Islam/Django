# Django Admin Panel 🎛️

Django-এর **Admin Panel** হলো একটা built-in powerful interface যেখান থেকে model-এর data তৈরি, পড়া, আপডেট ও মুছা যায় — কোনো কোড না লিখেই।

---

## ১. Admin Panel কী এবং কেন দরকার?

Django Admin হলো একটা auto-generated admin interface যা model-এর উপর ভিত্তি করে তৈরি হয়।

### সুবিধা:
- 🚀 দ্রুত CRUD interface
- 🔐 Built-in authentication
- 🎨 Customize করা যায়
- 📊 Grouping, search, filter করা যায়
- 📱 Responsive UI

---

## ২. Admin Panel চালু করা

### ধাপ ১: `settings.py`-এ Admin app যুক্ত আছে কিনা চেক

```python
# settings.py
INSTALLED_APPS = [
    "django.contrib.admin",       # ✅
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
]
```

### ধাপ ২: `urls.py`-এ admin URL যুক্ত

```python
# config/urls.py
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]
```

### ধাপ ৩: Migrate করুন

```bash
python manage.py migrate
```

### ধাপ ৪: Superuser তৈরি করুন

```bash
python manage.py createsuperuser
```

```
Username: admin
Email address: admin@example.com
Password: **********
Password (again): **********
Superuser created successfully.
```

### ধাপ ৫: Server চালু করুন ও Admin-এ যান

```bash
python manage.py runserver
```

এখন browser-এ যান: **http://127.0.0.1:8000/admin/**

---

## ৩. Model-কে Admin-এ Register করা

### সবচেয়ে সহজ উপায়:

```python
# blog/admin.py
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

এখন Admin panel-এ Post model দেখা যাবে।

### একসাথে অনেক Model register:

```python
from .models import Post, Author, Category

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
```

---

## ৪. ModelAdmin — Customize করা

`ModelAdmin` দিয়ে Admin panel-কে পুরোপুরি customize করা যায়।

### বেসিক উদাহরণ:

```python
# blog/admin.py
from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")

admin.site.register(Post, PostAdmin)
```

### অথবা Decorator দিয়ে:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")
```

---

## ৫. ModelAdmin-এর প্রধান Options

### `list_display` — কোন ফিল্ড দেখাবে

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "views", "created_at")
```

> 💡 ForeignKey field দিলে সেই object-এর `__str__` দেখাবে।

### `list_filter` — ফিল্টার করা

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at")
    list_filter = ("status", "created_at", "author")
```

### `search_fields` — সার্চ করা

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    search_fields = ("title", "content", "author__name")
```

> 💡 `author__name` দিয়ে related field-এও সার্চ করা যায়।

### `ordering` — সাজানো

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    ordering = ("-created_at",)
```

### `list_per_page` — প্রতি পৃষ্ঠায় কয়টা

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_per_page = 10
```

### `list_editable` — সরাসরি এডিট

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "views")
    list_editable = ("status", "views")
```

> ⚠️ `list_editable`-এ থাকা field অবশ্যই `list_display`-এ থাকতে হবে।

### `list_select_related` — Optimization

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    list_select_related = ("author",)
```

---

## ৬. Detail Form Customize

### `fieldsets` — Form-এর গ্রুপ

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        ("মূল তথ্য", {
            "fields": ("title", "slug", "content")
        }),
        ("প্রকাশনা", {
            "fields": ("author", "status", "is_featured")
        }),
    )
```

### `fields` — শুধু নির্দিষ্ট field দেখানো

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ("title", "content", "author")
```

### `exclude` — কোন field গোপন রাখা

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ("views",)
```

### `readonly_fields` — শুধু দেখা যাবে, এডিট যাবে না

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
```

### `autocomplete_fields` — ForeignKey-এর জন্য

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    autocomplete_fields = ("author",)
```

> 💡 `autocomplete_fields` ব্যবহার করলে Author model-এও `search_fields` থাকতে হবে।

---

## ৭. Inline Model Admin

Related model-গুলোকে parent model-এর ভেতরে দেখানো।

### উদাহরণ — Author-এর ভেতরে Post:

```python
# blog/admin.py
from django.contrib import admin
from .models import Author, Post

class PostInline(admin.TabularInline):
    model = Post
    extra = 1  # কয়টা খালি form দেখাবে

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [PostInline]
```

### `StackedInline` vs `TabularInline`:

```python
# StackedInline — একে অপরের নিচে
class PostInline(admin.StackedInline):
    model = Post

# TabularInline — টেবিল আকারে
class PostInline(admin.TabularInline):
    model = Post
```

### Inline Options:

```python
class PostInline(admin.TabularInline):
    model = Post
    extra = 2
    max_num = 5
    fields = ("title", "status")
    readonly_fields = ("created_at",)
    can_delete = True
```

---

## ৮. Custom Actions

Admin list view-এ বাল্ক অ্যাকশন যোগ করা যায়।

### উদাহরণ — প্রকাশ করা:

```python
from django.contrib import admin

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status")
    actions = ["make_published", "make_draft"]

    @admin.action(description="নির্বাচিত পোস্ট প্রকাশ করুন")
    def make_published(self, request, queryset):
        queryset.update(status="published")

    @admin.action(description="নির্বাচিত পোস্ট ড্রাফট করুন")
    def make_draft(self, request, queryset):
        queryset.update(status="draft")
```

---

## ৯. Custom Method in list_display

নিজের method বানিয়ে list_display-এ দেখানো যায়।

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "short_content", "is_popular")

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    short_content.short_description = "সংক্ষিপ্ত কন্টেন্ট"

    def is_popular(self, obj):
        return obj.views > 100
    is_popular.boolean = True
    is_popular.short_description = "জনপ্রিয়?"
```

---

## ১০. Date Hierarchy

তারিখ অনুযায়ী Drill-down করা:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    date_hierarchy = "created_at"
```

---

## ১১. Save Model Override

Save-এর সময় custom logic যোগ করা:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author")

    def save_model(self, request, obj, form, change):
        if not change:  # নতুন object
            obj.author = request.user
        super().save_model(request, obj, form, change)
```

---

## ১২. Full Example — Blog Admin

### models.py:

```python
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "ড্রাফট"),
        ("published", "প্রকাশিত"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="posts")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    views = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    text = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.post.title}"
```

### admin.py:

```python
from django.contrib import admin
from .models import Author, Category, Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ("created_at",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "post_count")
    search_fields = ("name", "email")
    inlines = [CommentInline]  # আসলে PostInline হওয়ার কথা

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "মোট পোস্ট"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "views", "is_featured", "created_at")
    list_filter = ("status", "is_featured", "created_at", "category")
    search_fields = ("title", "content", "author__name")
    ordering = ("-created_at",)
    list_per_page = 15
    list_editable = ("status", "is_featured")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        ("মূল তথ্য", {
            "fields": ("title", "slug", "content"),
        }),
        ("প্রকাশনা", {
            "fields": ("author", "category", "status", "is_featured", "views"),
            "classes": ("collapse",),
        }),
        ("তারিখ", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    actions = ["make_published", "make_draft", "increase_views"]

    @admin.action(description="নির্বাচিত পোস্ট প্রকাশ করুন")
    def make_published(self, request, queryset):
        queryset.update(status="published")

    @admin.action(description="নির্বাচিত পোস্ট ড্রাফট করুন")
    def make_draft(self, request, queryset):
        queryset.update(status="draft")

    @admin.action(description="ভিউ ১০০ করে বাড়ান")
    def increase_views(self, request, queryset):
        queryset.update(views=models.F("views") + 100)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("name", "text", "post__title")
    actions = ["approve_comments"]

    @admin.action(description="নির্বাচিত কমেন্ট অনুমোদন করুন")
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
```

---

## ১৩. Admin Customization — পুরো Panel

### Admin Site Title ও Header পরিবর্তন:

```python
# blog/admin.py বা নতুন একটা ফাইলে
admin.site.site_header = "My Blog Admin"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "স্বাগতম"
```

### অথবা urls.py-এ:

```python
from django.contrib import admin

admin.site.site_header = "My Blog Admin"
admin.site.site_title = "Blog Admin Portal"
admin.site.index_title = "Dashboard"
```

---

## ১৪. Admin URL Customize

```python
# config/urls.py
from django.contrib import admin

urlpatterns = [
    path("my-admin/", admin.site.urls),  # /admin/ এর বদলে /my-admin/
]
```

---

## ১৫. Permission — কে কী দেখতে পারবে

Admin-এ ব্যবহারকারীর permission দেওয়া যায়।

### User Types:

| Type | কাজ করতে পারে |
|------|---------------|
| **Superuser** | সবকিছু |
| **Staff** | Admin panel-এ ঢুকতে পারে, কিন্তু permission অনুযায়ী কাজ |
| **Active** | সাধারণ ব্যবহারকারী |

### Permission দেওয়া:

Admin panel → Users → নির্দিষ্ট user → Permissions section-এ:
- ✅ Staff status
- ✅ Specific permissions (যেমন: Can view post, Can change post)

---

## ১৬. Admin Template Override

### লোগো বা CSS পরিবর্তন:

```python
# settings.py
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        ...
    }
]
```

### Custom Admin Template:

```html
<!-- templates/admin/base_site.html -->
{% extends "admin/base_site.html" %}

{% block title %}My Admin{% endblock %}

{% block branding %}
<h1 id="site-name"><a href="{% url 'admin:index' %}">My Blog Admin</a></h1>
{% endblock %}
```

---

## ১৭. সেরা প্র্যাকটিস

1. ✅ প্রতিটা model-এর জন্য `ModelAdmin` তৈরি করুন
2. ✅ `list_display`, `list_filter`, `search_fields` যোগ করুন
3. ✅ `prepopulated_fields` দিয়ে slug auto-generate করুন
4. ✅ `readonly_fields` দিয়ে created_at/updated_at গোপন রাখুন
5. ✅ `inlines` দিয়ে related model দেখান
6. ✅ Custom actions যোগ করুন
7. ✅ `list_select_related` দিয়ে query optimize করুন
8. ❌ Production-এ default `admin/` URL রাখবেন না
9. ❌ সাধারণ user-কে superuser বানাবেন না

---

## ১৮. Common Options Reference

| Option | কাজ |
|--------|------|
| `list_display` | List view-এ কোন field দেখাবে |
| `list_filter` | ফিল্টার করার জন্য field |
| `search_fields` | সার্চ করার জন্য field |
| `ordering` | Default ordering |
| `list_per_page` | প্রতি পৃষ্ঠায় কয়টা item |
| `list_editable` | সরাসরি এডিট করার field |
| `fieldsets` | Form-এর গ্রুপ |
| `fields` | শুধু নির্দিষ্ট field |
| `exclude` | বাদ দেওয়া field |
| `readonly_fields` | শুধু দেখা যাবে |
| `autocomplete_fields` | Auto-complete dropdown |
| `prepopulated_fields` | Auto-generate (slug) |
| `inlines` | Related model inline |
| `actions` | Custom actions |
| `date_hierarchy` | Date drill-down |
| `list_select_related` | Query optimization |

---

## ১৯. Practical Exercise

```python
# blog/admin.py

from django.contrib import admin
from .models import Author, Category, Post, Comment


# ============ Exercise 1: Basic Registration ============
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


# ============ Exercise 2: Advanced Post Admin ============
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "views", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "content", "author__name")
    ordering = ("-created_at",)
    list_per_page = 10
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    actions = ["publish_posts"]

    @admin.action(description="প্রকাশ করুন")
    def publish_posts(self, request, queryset):
        queryset.update(status="published")


# ============ Exercise 3: Inline ============
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name",)
    inlines = [CommentInline]
```

---

## 🎯 আজকের Key Takeaways

1. **Admin Panel** = built-in CRUD interface
2. `createsuperuser` দিয়ে admin user তৈরি করুন
3. `admin.site.register(Model)` দিয়ে register করুন
4. **ModelAdmin** দিয়ে customize করুন:
   - `list_display` — কি দেখাবে
   - `list_filter` — ফিল্টার
   - `search_fields` — সার্চ
   - `fieldsets` — form গ্রুপ
   - `readonly_fields` — গোপন field
   - `actions` — বাল্ক অ্যাকশন
5. **Inline** দিয়ে related model parent-এ দেখান
6. **Custom Method** দিয়ে নতুন column যোগ করা যায়
7. Production-এ admin URL পরিবর্তন করুন
8. Permission সঠিকভাবে দিন

---

## ❓ অনুশীলনী প্রশ্ন

1. Django Admin Panel কী এবং কেন দরকার?
2. Superuser কীভাবে তৈরি করা যায়?
3. Model-কে Admin-এ কীভাবে register করা যায়?
4. `list_display`, `list_filter`, `search_fields` এর কাজ কী?
5. `prepopulated_fields` দিয়ে কী করা যায়?
6. Inline ModelAdmin কী এবং কখন ব্যবহার করা হয়?
7. Custom Action কীভাবে তৈরি করা যায়?
8. `readonly_fields` এর কাজ কী?
9. Admin site-এর title ও header কীভাবে পরিবর্তন করা যায়?
10. Production-এ Admin Panel নিরাপদ রাখার উপায় কী কী?
