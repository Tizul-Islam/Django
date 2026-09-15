# Django ORM: filter, get, create, update, delete 📊

Django ORM-এর মূল চারটি অপারেশন হলো **Create, Read, Update, Delete (CRUD)**। এই লেসনে প্রতিটি অপারেশন বিস্তারিত শিখবো।

---

## ১. ORM কী?

**ORM (Object-Relational Mapping)** হলো Python object ও database table-এর মাঝে সেতু বানায়। SQL না লিখেই Python কোড দিয়ে database-এ data তৈরি, পড়া, আপডেট ও মুছা যায়।

### কেন ORM?
- 🐍 SQL না জানলেও database কাজ করা যায়
- 🔄 SQLite থেকে PostgreSQL-এ স্যুইচ করলে কোড পরিবর্তন করতে হয় না
- 🛡️ SQL Injection থেকে সুরক্ষিত
- 📦 Code reuse ও maintain সহজ

---

## ২. Demo Model

এই লেসনে এই model দিয়ে উদাহরণ দেখানো হবে:

```python
# blog/models.py
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "ড্রাফট"),
        ("published", "প্রকাশিত"),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

---

## ৩. CREATE — Data তৈরি করা

### Method 1: `Model.objects.create()`

সরাসরি এক লাইনে তৈরি ও save:

```python
from blog.models import Author, Post

author = Author.objects.create(name="রহিম", email="rahim@example.com")
print(author)  # রহিম
print(author.id)  # 1
```

### Method 2: Instantiate + `save()`

আগে object তৈরি, পরে save:

```python
author = Author(name="করিম", email="karim@example.com")
author.save()
print(author.id)  # 2
```

### Method 3: `get_or_create()`

না থাকলে তৈরি, থাকলে নিয়ে আসে:

```python
obj, created = Author.objects.get_or_create(
    name="রহিম",
    defaults={"email": "rahim@example.com"},
)
print(obj)      # রহিম
print(created)  # False (আগে থেকেই আছে)
```

### Method 4: `bulk_create()` — একসাথে অনেকগুলো

এক query-এ অনেক object তৈরি:

```python
authors = [
    Author(name="সালাম", email="salam@example.com"),
    Author(name="জামাল", email="jamal@example.com"),
    Author(name="কামাল", email="kamal@example.com"),
]
Author.objects.bulk_create(authors)
```

> ⚠️ `bulk_create()`-এ `save()` method চলে না, signals চলে না।

### Related object তৈরি (ForeignKey):

```python
# Method 1: সরাসরি
post = Post.objects.create(
    title="প্রথম পোস্ট",
    content="কন্টেন্ট",
    author=author,
)

# Method 2: related_name দিয়ে
post = author.posts.create(
    title="লেখকের পোস্ট",
    content="কন্টেন্ট",
)
```

---

## ৪. READ — Data পড়া

### `all()` — সব object

```python
all_posts = Post.objects.all()
for post in all_posts:
    print(post.title)
```

> 💡 `all()` lazy — যতক্ষণ iterate না করবেন ততক্ষণ query চলবে না।

### `get()` — একটা নির্দিষ্ট object

```python
# id দিয়ে
post = Post.objects.get(id=1)
print(post.title)

# অন্য field দিয়ে
author = Author.objects.get(email="rahim@example.com")
```

⚠️ `get()`-এর নিয়ম:
- একাধিক object পেলে `MultipleObjectsReturned` error
- কোনো object না পেলে `DoesNotExist` error

```python
from blog.models import Post

try:
    post = Post.objects.get(id=999)
except Post.DoesNotExist:
    print("পোস্ট পাওয়া যায়নি")
```

### `filter()` — একাধিক object

শর্ত অনুযায়ী object গুলো দেয় (QuerySet):

```python
# সব published পোস্ট
published = Post.objects.filter(status="published")

# একাধিক শর্ত
posts = Post.objects.filter(status="published", views__gt=100)
```

> 💡 `filter()` সবসময় QuerySet দেয়, খালি হলেও error হয় না।

### `exclude()` — বাদ দিয়ে

```python
# draft ছাড়া সব পোস্ট
not_draft = Post.objects.exclude(status="draft")

# views 100 এর কম বাদ
high_views = Post.objects.exclude(views__lt=100)
```

### `first()` ও `last()` — প্রথম/শেষ

```python
first_post = Post.objects.first()
last_post = Post.objects.last()
```

### `order_by()` — সাজানো

```python
# views অনুযায়ী বড় থেকে ছোট
popular = Post.objects.order_by("-views")

# title অনুযায়ী A-Z
sorted_posts = Post.objects.order_by("title")

# একাধিক field দিয়ে
posts = Post.objects.order_by("status", "-created_at")
```

### `count()` — সংখ্যা

```python
total = Post.objects.count()
published_count = Post.objects.filter(status="published").count()
```

### `exists()` — আছে কিনা

```python
if Post.objects.filter(title="প্রথম পোস্ট").exists():
    print("পোস্টটা আছে")
```

### `values()` — Dictionary হিসেবে

```python
posts = Post.objects.values("title", "views")
# <QuerySet [{'title': '...', 'views': 100}, ...]>
```

### `values_list()` — Tuple হিসেবে

```python
# tuple হিসেবে
posts = Post.objects.values_list("title", "views")
# <QuerySet [('প্রথম পোস্ট', 100), ...]>

# flat=True — শুধু একটা field
titles = Post.objects.values_list("title", flat=True)
# <QuerySet ['প্রথম পোস্ট', ...]>
```

### `in_bulk()` — ID দিয়ে একসাথে

```python
posts = Post.objects.in_bulk([1, 2, 3])
# {1: <Post 1>, 2: <Post 2>, 3: <Post 3>}
print(posts[1].title)
```

### `latest()` ও `earliest()` — তারিখ অনুযায়ী

```python
latest = Post.objects.latest("created_at")
earliest = Post.objects.earliest("created_at")
```

### Field Lookups — `filter()`-এ শর্ত

```python
# exact (ডিফল্ট)
Post.objects.filter(id=1)

# contains / icontains
Post.objects.filter(title__contains="পাইথন")
Post.objects.filter(title__icontains="python")

# gt, gte, lt, lte
Post.objects.filter(views__gt=100)
Post.objects.filter(views__gte=100)
Post.objects.filter(views__lt=50)

# in
Post.objects.filter(id__in=[1, 2, 3])

# range
Post.objects.filter(views__range=(10, 100))

# year, month, day
Post.objects.filter(created_at__year=2024)
Post.objects.filter(created_at__month=10)

# startswith / endswith
Post.objects.filter(title__startswith="কিভাবে")
Post.objects.filter(title__endswith="টিউটোরিয়াল")

# isnull
Post.objects.filter(author__isnull=True)
```

---

## ৫. UPDATE — Data আপডেট করা

### Method 1: Object পরিবর্তন + `save()`

```python
post = Post.objects.get(id=1)
post.title = "নতুন শিরোনাম"
post.views = 200
post.save()
```

### Method 2: `update()` — একাধিক object একসাথে

```python
# সব published পোস্টের views 10 করে বাড়ান
Post.objects.filter(status="published").update(views=200)

# নির্দিষ্ট একটা
Post.objects.filter(id=1).update(title="আপডেটেড শিরোনাম")
```

> 💡 `update()` এক query-এ কাজ করে, `save()` method চলে না।

### Method 3: `update_or_create()`

থাকলে আপডেট, না থাকলে তৈরি:

```python
obj, created = Post.objects.update_or_create(
    title="টেস্ট পোস্ট",
    defaults={"content": "নতুন কন্টেন্ট", "status": "published"},
)
```

### Method 4: F Expression দিয়ে আপডেট

Field-এর বর্তমান মান দিয়ে গণনা:

```python
from django.db.models import F

# সব views 10 করে বাড়ান
Post.objects.all().update(views=F("views") + 10)

# views = views * 2
Post.objects.all().update(views=F("views") * 2)
```

### Method 5: `bulk_update()` — একসাথে অনেক আপডেট

```python
posts = list(Post.objects.filter(status="draft"))
for post in posts:
    post.status = "published"

Post.objects.bulk_update(posts, ["status"])
```

---

## ৬. DELETE — Data মুছা

### Method 1: Object-এর `delete()`

```python
post = Post.objects.get(id=1)
post.delete()
```

### Method 2: QuerySet-এর `delete()`

```python
# সব draft পোস্ট মুছুন
Post.objects.filter(status="draft").delete()

# নির্দিষ্ট author-এর সব পোস্ট মুছুন
Post.objects.filter(author__name="রহিম").delete()
```

> 💡 `delete()` কতগুলো object মুছেছে তা রিটার্ন করে: `(deleted_count, {model: count})`

```python
result = Post.objects.filter(status="draft").delete()
print(result)
# (5, {'blog.Post': 5})
```

### Related object মুছে ফেলা (on_delete):

ForeignKey-এ `on_delete` দিয়ে নির্ধারণ করা হয় parent মুছলে child কী হবে:

```python
# CASCADE — parent মুছলে child-ও মুছে যাবে
author = models.ForeignKey(Author, on_delete=models.CASCADE)

# PROTECT — child থাকলে parent মুছা যাবে না
author = models.ForeignKey(Author, on_delete=models.PROTECT)

# SET_NULL — parent মুছলে child-এর field NULL হবে
author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
```

---

## ৭. QuerySet Chaining

একাধিক method একসাথে চেইন করা যায়:

```python
# published পোস্ট, views অনুযায়ী সাজানো, প্রথম ৫টা
top_posts = (
    Post.objects
    .filter(status="published")
    .order_by("-views")
    [:5]
)
```

### Slicing:

```python
# প্রথম ৫টা
first_5 = Post.objects.all()[:5]

# ৬ষ্ঠ থেকে ১০তম
next_5 = Post.objects.all()[5:10]

# শুধু ৩য় পোস্ট
third = Post.objects.all()[2]
```

---

## ৮. Related Object Access

### Forward (ForeignKey থেকে parent):

```python
post = Post.objects.get(id=1)
print(post.author.name)  # লেখকের নাম
```

### Reverse (parent থেকে child):

```python
author = Author.objects.get(id=1)

# related_name দিয়ে
posts = author.posts.all()

# related_name না থাকলে _set
posts = author.post_set.all()
```

### Filter through relation:

```python
# রহিম-এর সব published পোস্ট
posts = Post.objects.filter(author__name="রহিম", status="published")
```

---

## ৯. একটা সম্পূর্ণ CRUD উদাহরণ

### Shell-এ চালান:

```bash
python manage.py shell
```

```python
from blog.models import Author, Post

# ============ CREATE ============
print("=== CREATE ===")
author = Author.objects.create(name="রহিম", email="rahim@example.com")
print(f"লেখক তৈরি: {author}")

post = Post.objects.create(
    title="পাইথন শিখুন",
    content="পাইথন একটা সহজ ভাষা",
    author=author,
    status="published",
)
print(f"পোস্ট তৈরি: {post}")


# ============ READ ============
print("\n=== READ ===")
all_posts = Post.objects.all()
print(f"মোট পোস্ট: {all_posts.count()}")

published = Post.objects.filter(status="published")
print(f"প্রকাশিত পোস্ট: {published.count()}")

post = Post.objects.get(id=1)
print(f"পোস্ট ১: {post.title}")


# ============ UPDATE ============
print("\n=== UPDATE ===")
post.title = "পাইথন শিখুন (আপডেটেড)"
post.save()
print(f"আপডেটেড: {post.title}")

Post.objects.filter(id=1).update(views=100)
print(f"Views: {Post.objects.get(id=1).views}")


# ============ DELETE ============
print("\n=== DELETE ===")
post.delete()
print(f"এখন মোট পোস্ট: {Post.objects.count()}")
```

---

## ১০. সাধারণ ভুল ও সমাধান

### ভুল ১: `get()` দিয়ে একাধিক object চাওয়া

```python
# ❌ MultipleObjectsReturned error
post = Post.objects.get(status="published")

# ✅ filter ব্যবহার করুন
posts = Post.objects.filter(status="published")
```

### ভুল ২: খালি QuerySet-এ `get()`

```python
# ❌ DoesNotExist error
post = Post.objects.get(id=999)

# ✅ try-except বা filter + first
post = Post.objects.filter(id=999).first()
if post:
    print(post.title)
```

### ভুল ৩: `save()` না করা

```python
# ❌ পরিবর্তন save হবে না
post = Post.objects.get(id=1)
post.title = "নতুন"

# ✅ save করুন
post.save()
```

### ভুল ৪: QuerySet-এর মাঝে modify করা

```python
# ❌ এটা কাজ করবে না
Post.objects.filter(status="draft").status = "published"

# ✅ update() ব্যবহার করুন
Post.objects.filter(status="draft").update(status="published")
```

---

## ১১. সেরা প্র্যাকটিস

1. ✅ একটা object দরকার হলে `get()`, না থাকলে error হতে পারে — `try-except` ব্যবহার করুন
2. ✅ একাধিক object দরকার হলে `filter()` ব্যবহার করুন
3. ✅ একাধিক আপডেট/ডিলিট-এর জন্য `update()`/`delete()` QuerySet-এ ব্যবহার করুন (loop নয়)
4. ✅ `exists()` দিয়ে আগে চেক করুন
5. ✅ `count()` দিয়ে সংখ্যা নিন (len() নয়)
6. ✅ `select_related` ও `prefetch_related` দিয়ে N+1 problem এড়িয়ে চলুন
7. ❌ `all()` ব্যবহার করার পর `filter()` করবেন না — সরাসরি ফিল্টার করুন
8. ❌ loop-এর ভেতরে query চালাবেন না

---

## ১২. Quick Reference Cheat Sheet

| Operation | Method | উদাহরণ |
|-----------|--------|--------|
| Create | `create()` | `Post.objects.create(title="x")` |
| Create | instantiate + `save()` | `p = Post(title="x"); p.save()` |
| Create or Get | `get_or_create()` | `Post.objects.get_or_create(...)` |
| Read All | `all()` | `Post.objects.all()` |
| Read One | `get()` | `Post.objects.get(id=1)` |
| Read Many | `filter()` | `Post.objects.filter(status="pub")` |
| Exclude | `exclude()` | `Post.objects.exclude(status="draft")` |
| Order | `order_by()` | `Post.objects.order_by("-views")` |
| Count | `count()` | `Post.objects.count()` |
| Exists | `exists()` | `qs.exists()` |
| First | `first()` | `Post.objects.first()` |
| Update One | `obj.field = x; obj.save()` | |
| Update Many | `update()` | `qs.update(views=100)` |
| Update or Create | `update_or_create()` | |
| Delete One | `obj.delete()` | |
| Delete Many | `qs.delete()` | |

---

## ১৩. Practical Exercise

```python
# blog/models.py দিয়ে কাজ করুন

from blog.models import Author, Post

# ============ 1. CREATE ============
# ৩জন লেখক তৈরি করুন
Author.objects.create(name="রহিম", email="rahim@test.com")
Author.objects.create(name="করিম", email="karim@test.com")
Author.objects.create(name="সালাম", email="salam@test.com")

# প্রত্যেকের জন্য ২টি করে পোস্ট তৈরি করুন
rahim = Author.objects.get(name="রহিম")
Post.objects.create(title="পোস্ট ১", content="কন্টেন্ট", author=rahim, status="published")
Post.objects.create(title="পোস্ট ২", content="কন্টেন্ট", author=rahim, status="draft")


# ============ 2. READ ============
# সব লেখক দেখুন
print(Author.objects.all())

# রহিম-এর সব পোস্ট
print(rahim.posts.all())

# সব published পোস্ট
print(Post.objects.filter(status="published"))

# views > 50 এমন পোস্ট
print(Post.objects.filter(views__gt=50))


# ============ 3. UPDATE ============
# রহিম-এর সব পোস্ট published করুন
Post.objects.filter(author=rahim).update(status="published")

# সব পোস্টের views 10 বাড়ান
from django.db.models import F
Post.objects.all().update(views=F("views") + 10)


# ============ 4. DELETE ============
# সব draft পোস্ট মুছুন
Post.objects.filter(status="draft").delete()

# রহিম-এর একটা নির্দিষ্ট পোস্ট মুছুন
post = Post.objects.filter(author=rahim).first()
if post:
    post.delete()
```

---

## 🎯 আজকের Key Takeaways

### CREATE:
1. `objects.create()` — সরাসরি তৈরি
2. instantiate + `save()` — আলাদাভাবে
3. `get_or_create()` — না থাকলে তৈরি
4. `bulk_create()` — একসাথে অনেক

### READ:
1. `all()` — সব
2. `get()` — একটা (error হতে পারে)
3. `filter()` — একাধিক (শর্ত অনুযায়ী)
4. `exclude()` — বাদ দিয়ে
5. `order_by()`, `count()`, `exists()`, `first()`, `last()`

### UPDATE:
1. `obj.field = x; obj.save()` — একটা
2. `queryset.update(field=x)` — একাধিক
3. `F()` expression — field দিয়ে গণনা
4. `update_or_create()` — থাকলে আপডেট, না থাকলে তৈরি

### DELETE:
1. `obj.delete()` — একটা
2. `queryset.delete()` — একাধিক
3. `on_delete` — related object-এর আচরণ নির্ধারণ

---

## ❓ অনুশীলনী প্রশ্ন

1. `create()` ও instantiate + `save()` এর পার্থক্য কী?
2. `get()` ও `filter()` এর পার্থক্য কী?
3. `get_or_create()` কীভাবে কাজ করে?
4. `update()` কেন `save()` এর চেয়ে ভালো (বহু object-এর ক্ষেত্রে)?
5. `F()` expression কী এবং কেন ব্যবহার করা হয়?
6. `delete()` কী রিটার্ন করে?
7. `on_delete=models.CASCADE` এর কাজ কী?
8. N+1 problem কী? কীভাবে সমাধান করা যায়?
9. `exists()` ও `count()` কখন ব্যবহার করা ভালো?
10. একটা blog app-এর জন্য CRUD operations লিখুন (Post model দিয়ে)
