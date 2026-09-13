# Django Models 🗄️

Django-এ **Model** হলো database table-এর Python প্রতিনিধিত্ব। Django ORM (Object-Relational Mapping) দিয়ে SQL না লিখেই Python কোড দিয়ে database-এ data তৈরি, পড়া, আপডেট ও মুছা যায়।

---

## ১. Model কী এবং কেন দরকার?

Model হলো একটা Python class যা `django.db.models.Model` থেকে inherit করে। প্রতিটা model একটা database table-কে বোঝায়।

### সুবিধা:
- 🐍 SQL না লিখেই Python দিয়ে database কাজ করা যায়
- 🔄 database পরিবর্তন (SQLite → PostgreSQL) করলে কোড পরিবর্তন করতে হয় না
- 🛡️ SQL injection থেকে সুরক্ষিত
- 📋 migrations দিয়ে schema পরিবর্তন ট্র্যাক করা যায়

---

## ২. প্রথম Model তৈরি করা

```python
# blog/models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

এই model টা `blog_post` নামে একটা table তৈরি করবে যার columns: `id`, `title`, `content`, `created_at`।

---

## ৩. Field Types (Field প্রকারভেদ)

Django-এ বিভিন্ন ধরনের field আছে। প্রতিটা field একটা database column-কে বোঝায়।

### সাধারণ Field Types:

| Field | বিবরণ | উদাহরণ |
|-------|--------|--------|
| `CharField` | ছোট স্ট্রিং (max_length দরকার) | `name = models.CharField(max_length=100)` |
| `TextField` | বড় টেক্সট | `content = models.TextField()` |
| `IntegerField` | পূর্ণ সংখ্যা | `age = models.IntegerField()` |
| `FloatField` | দশমিক সংখ্যা | `price = models.FloatField()` |
| `DecimalField` | নির্দিষ্ট দশমিক সংখ্যা | `price = models.DecimalField(max_digits=10, decimal_places=2)` |
| `BooleanField` | True/False | `is_active = models.BooleanField(default=True)` |
| `DateField` | তারিখ | `birth_date = models.DateField()` |
| `DateTimeField` | তারিখ + সময় | `created_at = models.DateTimeField(auto_now_add=True)` |
| `EmailField` | ইমেইল | `email = models.EmailField()` |
| `URLField` | URL | `website = models.URLField()` |
| `ImageField` | ইমেজ ফাইল | `image = models.ImageField(upload_to="images/")` |
| `FileField` | ফাইল | `file = models.FileField(upload_to="files/")` |
| `SlugField` | URL-friendly string | `slug = models.SlugField(max_length=200)` |
| `UUIDField` | UUID | `id = models.UUIDField(primary_key=True, default=uuid.uuid4)` |
| `JSONField` | JSON data | `data = models.JSONField()` |

---

## ৪. Field Options (Field অপশন)

প্রতিটা field-এ বিভিন্ন অপশন দেওয়া যায়।

### সাধারণ Options:

| Option | বিবরণ |
|--------|--------|
| `max_length` | সর্বোচ্চ দৈর্ঘ্য (CharField-এ বাধ্যতামূলক) |
| `default` | ডিফল্ট মান |
| `null` | database-এ `NULL` থাকতে পারবে (ডিফল্ট False) |
| `blank` | form-এ খালি রাখা যাবে (ডিফল্ট False) |
| `choices` | নির্দিষ্ট মানগুলোর বেছে নেওয়া |
| `primary_key` | primary key হিসেবে ব্যবহার |
| `unique` | একই মান দুবার থাকবে না |
| `verbose_name` | Admin panel-এ দেখানো নাম |
| `help_text` | সাহায্যকারী টেক্সট |
| `auto_now` | প্রতিবার save-এ বর্তমান সময় |
| `auto_now_add` | শুধু প্রথমবার তৈরির সময় |
| `upload_to` | FileField/ImageField-এর জন্য path |

### উদাহরণ:

```python
class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name="নাম")
    email = models.EmailField(unique=True)
    age = models.IntegerField(default=18)
    bio = models.TextField(blank=True, help_text="সংক্ষিপ্ত পরিচিতি")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### `null` vs `blank`:

| Option | কাজ |
|--------|------|
| `null=True` | database column-এ NULL থাকতে পারবে |
| `blank=True` | form-এ ফাঁকা রাখা যাবে (validation) |

```python
# CharField/TextField-এ null=True দেওয়ার দরকার নেই, blank=True যথেষ্ট
name = models.CharField(max_length=100, blank=True)  # ✅
name = models.CharField(max_length=100, null=True, blank=True)  # ❌ খারাপ

# অন্য field-এ দুটোই দিতে হয়
birth_date = models.DateField(null=True, blank=True)  # ✅
```

---

## ৫. Relationship (সম্পর্ক)

Django-এ modelগুলোর মধ্যে সম্পর্ক তৈরি করা যায়।

### ১. ForeignKey (এক-থেকে-অনেক)

একটা object অন্য object-এর সাথে যুক্ত।

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
```

একজন Author-এর অনেকগুলো Book থাকতে পারে।

### `on_delete` অপশন:

| Option | কাজ |
|--------|------|
| `CASCADE` | parent মুছলে child-ও মুছে যাবে |
| `PROTECT` | child থাকলে parent মুছা যাবে না |
| `SET_NULL` | parent মুছলে child-এর field NULL হবে |
| `SET_DEFAULT` | ডিফল্ট মান সেট হবে |
| `DO_NOTHING` | কিছুই করবে না |

### ২. OneToOneField (এক-থেকে-এক)

```python
class User(models.Model):
    name = models.CharField(max_length=100)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
```

একজন User-এর একটাই Profile থাকবে।

### ৩. ManyToManyField (অনেক-থেকে-অনেক)

```python
class Student(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name="courses")
```

একজন Student অনেকগুলো Course নিতে পারে, একটা Course-এ অনেক Student থাকতে পারে।

---

## ৬. `__str__` Method

Model-এর object-এর মানুষপাঠ্য প্রতিনিধিত্ব।

```python
class Post(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
```

Admin panel ও shell-এ এই নাম দেখাবে।

---

## ৭. Meta Class

Model-এর কনফিগারেশন (ordering, table name ইত্যাদি)।

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]          # নতুন আগে
        verbose_name = "পোস্ট"
        verbose_name_plural = "পোস্টগুলো"
        db_table = "blog_posts"              # table name
        unique_together = ["title", "author"]  # একসাথে unique
```

### সাধারণ Meta Options:

| Option | কাজ |
|--------|------|
| `ordering` | default ordering |
| `verbose_name` | singular নাম |
| `verbose_name_plural` | plural নাম |
| `db_table` | database table name |
| `unique_together` | একসাথে unique |
| `permissions` | custom permissions |

---

## ৮. ORM — Database অপারেশন

Django ORM দিয়ে database-এ CRUD (Create, Read, Update, Delete) অপারেশন করা যায়।

### Create (তৈরি):

```python
# Method 1: create()
post = Post.objects.create(title="প্রথম পোস্ট", content="কন্টেন্ট")

# Method 2: instantiate + save()
post = Post(title="দ্বিতীয় পোস্ট", content="কন্টেন্ট")
post.save()
```

### Read (পড়া):

```python
# সব object
posts = Post.objects.all()

# নির্দিষ্ট একটা (id দিয়ে)
post = Post.objects.get(id=1)

# filter করা
posts = Post.objects.filter(title__contains="প্রথম")

# first / last
first_post = Post.objects.first()
last_post = Post.objects.last()

# count
total = Post.objects.count()

# ordering
posts = Post.objects.order_by("-created_at")
```

### Update (আপডেট):

```python
# Method 1: object পরিবর্তন + save
post = Post.objects.get(id=1)
post.title = "নতুন শিরোনাম"
post.save()

# Method 2: update()
Post.objects.filter(id=1).update(title="নতুন শিরোনাম")
```

### Delete (মুছা):

```python
# একটা object মুছা
post = Post.objects.get(id=1)
post.delete()

# অনেকগুলো মুছা
Post.objects.filter(title__contains="পুরনো").delete()
```

---

## ৯. QuerySet Methods

| Method | কাজ |
|--------|------|
| `all()` | সব object |
| `filter(**kwargs)` | শর্ত অনুযায়ী |
| `get(**kwargs)` | একটা object (না পেলে error) |
| `exclude(**kwargs)` | শর্ত বাদ দিয়ে |
| `order_by(*fields)` | সাজানো |
| `count()` | সংখ্যা |
| `first()` / `last()` | প্রথম/শেষ |
| `exists()` | আছে কিনা |
| `values()` | dictionary হিসেবে |
| `values_list()` | tuple হিসেবে |
| `distinct()` | unique |
| `delete()` | মুছা |
| `update()` | আপডেট |
| `create()` | তৈরি |

### Field Lookups:

| Lookup | মানে | উদাহরণ |
|--------|------|--------|
| `exact` | সমান | `filter(id=1)` |
| `iexact` | সমান (case-insensitive) | `filter(name__iexact="rahim")` |
| `contains` | আছে | `filter(title__contains="প্রথম")` |
| `icontains` | আছে (case-insensitive) | `filter(title__icontains="first")` |
| `gt` | বড় | `filter(age__gt=18)` |
| `gte` | বড় বা সমান | `filter(age__gte=18)` |
| `lt` | ছোট | `filter(age__lt=18)` |
| `lte` | ছোট বা সমান | `filter(age__lte=18)` |
| `in` | ভেতরে | `filter(id__in=[1,2,3])` |
| `startswith` | দিয়ে শুরু | `filter(name__startswith="র")` |
| `endswith` | দিয়ে শেষ | `filter(name__endswith="ম")` |
| `isnull` | NULL কিনা | `filter(email__isnull=True)` |

---

## ১০. Related Objects (সম্পর্কিত object)

### ForeignKey দিয়ে access:

```python
book = Book.objects.get(id=1)
print(book.author.name)        # author-এর নাম
print(book.author.books.all())  # author-এর সব বই (related_name)
```

### `related_name`:

```python
class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

# access
author = Author.objects.get(id=1)
author.books.all()  # এই author-এর সব বই
```

---

## ১১. Migrations

Model পরিবর্তন হলে database-এ apply করতে migrations দরকার।

### Migration তৈরি:

```bash
python manage.py makemigrations
```

### Migration apply:

```bash
python manage.py migrate
```

### Migration দেখা:

```bash
python manage.py showmigrations
```

### SQL দেখা:

```bash
python manage.py sqlmigrate blog 0001
```

---

## ১২. Django Shell দিয়ে চেক

```bash
python manage.py shell
```

```python
from blog.models import Post

# তৈরি
post = Post.objects.create(title="টেস্ট", content="কন্টেন্ট")

# দেখা
print(Post.objects.all())

# আপডেট
post.title = "নতুন"
post.save()

# মুছা
post.delete()
```

---

## ১৩. একটা সম্পূর্ণ উদাহরণ — Blog App

### models.py:

```python
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="নাম")
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name = "লেখক"
        verbose_name_plural = "লেখকগণ"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="ক্যাটাগরি")
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "ক্যাটাগরি"
        verbose_name_plural = "ক্যাটাগরি"

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "ড্রাফট"),
        ("published", "প্রকাশিত"),
    ]

    title = models.CharField(max_length=200, verbose_name="শিরোনাম")
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField(verbose_name="কন্টেন্ট")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="posts")
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    is_featured = models.BooleanField(default=False, verbose_name="ফিচার্ড")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="আপডেট")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "পোস্ট"
        verbose_name_plural = "পোস্টগুলো"

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.post.title}"
```

### Migration:

```bash
python manage.py makemigrations
python manage.py migrate
```

### ORM ব্যবহার:

```python
# Author তৈরি
author = Author.objects.create(name="রহিম", email="rahim@example.com")

# Category তৈরি
tech = Category.objects.create(name="টেকনোলজি", slug="technology")

# Post তৈরি
post = Post.objects.create(
    title="পাইথন শিখুন",
    slug="python-shikhun",
    content="পাইথন একটা সহজ ভাষা...",
    author=author,
    category=tech,
    status="published",
)

# সব প্রকাশিত পোস্ট
published = Post.objects.filter(status="published")

# ক্যাটাগরি অনুযায়ী
tech_posts = Post.objects.filter(category=tech)

# লেখকের সব পোস্ট
author_posts = author.posts.all()

# পোস্টের সব কমেন্ট
comments = post.comments.all()
```

---

## ১৪. সেরা প্র্যাকটিস (Best Practices)

1. ✅ প্রতিটা model-এ `__str__` method যোগ করুন
2. ✅ `CharField`-এ `max_length` সঠিকভাবে দিন
3. ✅ `DateTimeField`-এ `auto_now_add` ও `auto_now` ব্যবহার করুন
4. ✅ `related_name` দিন যাতে reverse query সহজ হয়
5. ✅ `Meta` class-এ `ordering` ও `verbose_name` সেট করুন
6. ✅ `null=True` ও `blank=True` সঠিকভাবে ব্যবহার করুন
7. ✅ Model পরিবর্তন করার পর `makemigrations` ও `migrate` চালান
8. ❌ `__init__` method model-এ লিখবেন না (use `__str__`)

---

## ১৫. Practical Exercise

```python
# ============ Exercise 1: Basic Model ============
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    email = models.EmailField()
    department = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    admission_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


# ============ Exercise 2: ForeignKey ============
class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="teachers")
    email = models.EmailField()

    def __str__(self):
        return self.name


# ============ Exercise 3: ManyToMany ============
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    students = models.ManyToManyField(Student, related_name="courses")

    def __str__(self):
        return self.name


# ============ Exercise 4: ORM Queries ============
# shell-এ চালান:
# from blog.models import Student, Department, Teacher, Course

# # তৈরি
# cse = Department.objects.create(name="CSE", code="CSE101")
# teacher = Teacher.objects.create(name="রহিম", department=cse, email="rahim@cse.com")

# # পড়া
# teachers = Teacher.objects.filter(department=cse)
# print(teachers)

# # আপডেট
# teacher.name = "রহিম আহমেদ"
# teacher.save()

# # মুছা
# teacher.delete()
```

---

## 🎯 আজকের Key Takeaways

1. **Model** = database table-এর Python প্রতিনিধিত্ব
2. **Field Types**: CharField, TextField, IntegerField, DateTimeField, EmailField ইত্যাদি
3. **Field Options**: max_length, default, null, blank, unique, verbose_name
4. **Relationship**: ForeignKey, OneToOneField, ManyToManyField
5. **`__str__`** — object-এর মানুষপাঠ্য নাম
6. **Meta Class** — ordering, verbose_name, db_table
7. **ORM** — `objects.all()`, `filter()`, `get()`, `create()`, `update()`, `delete()`
8. **Field Lookups**: `__gt`, `__lt`, `__contains`, `__in` ইত্যাদি
9. **Migrations** — `makemigrations` + `migrate`
10. **`related_name`** — reverse query-এর জন্য

---

## ❓ অনুশীলনী প্রশ্ন

1. Django Model কী?
2. `CharField` ও `TextField` এর পার্থক্য কী?
3. `null=True` ও `blank=True` এর পার্থক্য কী?
4. ForeignKey, OneToOneField ও ManyToManyField এর পার্থক্য কী?
5. `on_delete=models.CASCADE` এর কাজ কী?
6. `__str__` method কেন লেখা হয়?
7. Meta class-এর গুরুত্ব কী?
8. ORM দিয়ে কীভাবে data create/read/update/delete করা যায়?
9. `filter()` ও `get()` এর পার্থক্য কী?
10. Migration কী? কেন দরকার?
