# Django: Advanced Models & ORM Queries ⚡

এই লেসনে Django ORM-এর advanced features শিখবো — complex query, aggregation, annotation, Q objects, optimization, transactions ইত্যাদি।

---

## ১. QuerySet এর গঠন

QuerySet হলো Django-এর lazy object — তাঁরা সত্যিই database-এ query চালায় না যতক্ষণ না evaluate করা হয়।

### কখন evaluate হয়?

```python
# এখনো query চালায়নি
posts = Post.objects.filter(status="published")

# এই মুহূর্তে query চালাবে
for post in posts:
    print(post.title)

# অথবা
print(list(posts))
print(posts.count())
print(posts.first())
```

### QuerySet chain করা:

```python
# একাধিক filter chain করা যায়
posts = Post.objects.filter(status="published").filter(author__name="রহিম")
```

---

## ২. Field Lookups — Advanced

### সাধারণ Lookups:

```python
# exact (ডিফল্ট)
Post.objects.filter(id=1)

# iexact (case-insensitive)
Post.objects.filter(title__iexact="hello world")

# contains / icontains
Post.objects.filter(title__contains="পাইথন")
Post.objects.filter(title__icontains="python")

# gt, gte, lt, lte
Post.objects.filter(views__gt=100)
Post.objects.filter(created_at__gte="2024-01-01")

# in
Post.objects.filter(id__in=[1, 2, 3, 4, 5])

# startswith / endswith
Post.objects.filter(title__startswith="কিভাবে")
Post.objects.filter(slug__endswith="-tutorial")

# range
Post.objects.filter(created_at__range=("2024-01-01", "2024-12-31"))

# year, month, day, hour, minute, second
Post.objects.filter(created_at__year=2024)
Post.objects.filter(created_at__month=10)

# isnull
Post.objects.filter(published_at__isnull=True)

# regex / iregex
Post.objects.filter(title__regex=r"^\d+")
```

---

## ৩. Q Objects — Complex Query

`Q` object দিয়ে OR (`|`) এবং AND (`&`) দিয়ে complex query লেখা যায়।

### Import:

```python
from django.db.models import Q
```

### OR query:

```python
# status=published OR author=rahim
Post.objects.filter(Q(status="published") | Q(author__name="রহিম"))
```

### AND query:

```python
# status=published AND views>100
Post.objects.filter(Q(status="published") & Q(views__gt=100))
```

### NOT query:

```python
# status != draft
Post.objects.filter(~Q(status="draft"))
```

### Complex:

```python
# (published AND views>100) OR (featured=True)
Post.objects.filter(
    Q(status="published", views__gt=100) | Q(is_featured=True)
)
```

### Search bar-এর জন্য:

```python
def search_posts(query):
    return Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(author__name__icontains=query)
    )
```

---

## ৪. Aggregation — গাণিতিক গণনা

`aggregate()` দিয়ে গড়, যোগফল, সর্বোচ্চ, সর্বনিম্ন ইত্যাদি বের করা যায়।

### Import:

```python
from django.db.models import Avg, Sum, Count, Min, Max, Value
from django.db.models.functions import Coalesce
```

### উদাহরণ:

```python
from django.db.models import Avg, Sum, Count, Min, Max

# সব পোস্টের view-এর গড়
result = Post.objects.aggregate(avg_views=Avg("views"))
print(result)  # {'avg_views': 250.5}

# সব view-এর যোগফল
total_views = Post.objects.aggregate(total=Sum("views"))
print(total_views["total"])

# সর্বোচ্চ ও সর্বনিম্ন
stats = Post.objects.aggregate(
    max_views=Max("views"),
    min_views=Min("views"),
    total=Count("id"),
)
print(stats)
# {'max_views': 5000, 'min_views': 10, 'total': 50}
```

### Related object-এর aggregation:

```python
# প্রতিটা লেখকের কতগুলো পোস্ট আছে
authors = Author.objects.annotate(post_count=Count("posts"))

for author in authors:
    print(f"{author.name}: {author.post_count} পোস্ট")
```

---

## ৫. Annotation — নতুন field যোগ করা

`annotate()` দিয়ে queryset-এ প্রতিটা object-এ নতুন temporary field যোগ করা যায়।

### Count annotation:

```python
from django.db.models import Count

# প্রতিটা লেখকের পোস্ট সংখ্যা
authors = Author.objects.annotate(post_count=Count("posts"))

# পোস্ট সংখ্যা অনুযায়ী সাজানো
authors = Author.objects.annotate(post_count=Count("posts")).order_by("-post_count")
```

### Sum annotation:

```python
from django.db.models import Sum

# প্রতিটা লেখকের মোট view
authors = Author.objects.annotate(total_views=Sum("posts__views"))
```

### Conditional annotation:

```python
from django.db.models import Count, Q

# প্রকাশিত ও ড্রাফট পোস্ট আলাদাভাবে গণনা
authors = Author.objects.annotate(
    published_count=Count("posts", filter=Q(posts__status="published")),
    draft_count=Count("posts", filter=Q(posts__status="draft")),
)
```

---

## ৬. `values()` ও `values_list()`

Dictionary বা tuple হিসেবে data নেওয়ার জন্য।

### `values()` — Dictionary:

```python
# শুধু title ও created_at
posts = Post.objects.values("title", "created_at")
# <QuerySet [{'title': '...', 'created_at': datetime(...)}, ...]>

# annotation সহ
posts = Post.objects.values("author__name").annotate(total=Count("id"))
```

### `values_list()` — Tuple:

```python
# tuple হিসেবে
posts = Post.objects.values_list("title", "views")
# <QuerySet [('টেস্ট', 100), ('পোস্ট', 200)]>

# flat=True — শুধু একটা field হলে list
titles = Post.objects.values_list("title", flat=True)
# <QuerySet ['টেস্ট', 'পোস্ট', ...]>

# list-এ রূপান্তর
title_list = list(titles)
```

---

## ৭. `select_related` ও `prefetch_related` — Query Optimization

### N+1 Problem:

```python
# ❌ খারাপ — প্রতিটা পোস্টের জন্য আলাদা query (N+1 query)
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # প্রতিটা জন্য নতুন query
```

### `select_related` — ForeignKey/OneToOne:

`JOIN` দিয়ে এক query-এ related object আনে।

```python
# ✅ ভালো — এক query-এ সব
posts = Post.objects.select_related("author").all()
for post in posts:
    print(post.author.name)  # আর নতুন query হবে না
```

### `prefetch_related` — ManyToMany/Reverse ForeignKey:

আলাদা query চালিয়ে related object আনে।

```python
# প্রতিটা লেখকের সব পোস্ট একসাথে আনা
authors = Author.objects.prefetch_related("posts").all()
for author in authors:
    print(author.posts.all())  # আর নতুন query হবে না
```

### একসাথে ব্যবহার:

```python
posts = Post.objects.select_related("author", "category").prefetch_related("comments", "tags").all()
```

### `prefetch_related`-এ filter:

```python
from django.db.models import Prefetch

# শুধু প্রকাশিত পোস্ট আনুন
authors = Author.objects.prefetch_related(
    Prefetch("posts", queryset=Post.objects.filter(status="published"))
).all()
```

---

## ৮. `F` Expressions — Field দিয়ে গণনা

`F` দিয়ে এক field-এর মান অন্য field-এর সাথে তুলনা বা গণনা করা যায়।

### Import:

```python
from django.db.models import F
```

### উদাহরণ:

```python
from django.db.models import F

# views >= likes এর পোস্ট
Post.objects.filter(views__gte=F("likes"))

# সব পোস্টের views 10 করে বাড়ান
Post.objects.update(views=F("views") + 10)

# annotation-এ ব্যবহার
posts = Post.objects.annotate(
    engagement=F("views") + F("likes") + F("comments_count")
)
```

---

## ৯. Conditional Expressions — `Case` ও `When`

SQL-এর CASE WHEN এর মতো কাজ করে।

### Import:

```python
from django.db.models import Case, When, Value, CharField
```

### উদাহরণ:

```python
from django.db.models import Case, When, Value, IntegerField

# popularity level অনুযায়ী বিভাগ
posts = Post.objects.annotate(
    popularity=Case(
        When(views__gt=1000, then=Value("জনপ্রিয়")),
        When(views__gt=500, then=Value("মাঝারি")),
        default=Value("সাধারণ"),
        output_field=CharField(),
    )
)
```

### Update-এ ব্যবহার:

```python
# status অনুযায়ী views বাড়ান
Post.objects.update(
    views=Case(
        When(status="published", then=F("views") + 100),
        default=F("views"),
    )
)
```

---

## ১০. `exists()`, `count()`, `in_bulk()`

### `exists()`:

```python
if Post.objects.filter(author=author).exists():
    print("লেখকের পোস্ট আছে")
```

### `count()`:

```python
total = Post.objects.count()
published = Post.objects.filter(status="published").count()
```

### `in_bulk()`:

```python
# id দিয়ে একসাথে অনেক object আনা
posts = Post.objects.in_bulk([1, 2, 3, 4, 5])
# {1: <Post 1>, 2: <Post 2>, ...}

print(posts[1].title)
```

### `bulk_create()` ও `bulk_update()`:

```python
# একসাথে অনেক object তৈরি (এক query)
posts = [Post(title=f"পোস্ট {i}", content="কন্টেন্ট") for i in range(100)]
Post.objects.bulk_create(posts)

# একসাথে অনেক object আপডেট
posts = list(Post.objects.filter(status="draft"))
for post in posts:
    post.status = "published"
Post.objects.bulk_update(posts, ["status"])
```

---

## ১১. `only()` ও `defer()` — Selected Fields

### `only()` — শুধু নির্দিষ্ট field আনা:

```python
# শুধু title আনুন, বাকি field পরে চাইলে আলাদা query
posts = Post.objects.only("title")
```

### `defer()` — নির্দিষ্ট field বাদ দেওয়া:

```python
# content field বাদে সব আনুন
posts = Post.objects.defer("content")
```

> ⚠️ এগুলো শুধু তখনই ব্যবহার করুন যখন নির্দিষ্ট field বেশি বড় এবং দরকার নেই।

---

## ১২. Raw SQL — `raw()` ও `cursor`

কখনও কখনো জটিল query-র জন্য raw SQL লিখতে হয়।

### `raw()`:

```python
# raw SQL দিয়ে query
posts = Post.objects.raw("SELECT * FROM blog_post WHERE status = %s", ["published"])

for post in posts:
    print(post.title)
```

### `cursor()` দিয়ে:

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT title, views FROM blog_post WHERE status = %s", ["published"])
    rows = cursor.fetchall()

for row in rows:
    print(row)  # ('টেস্ট', 100)
```

### `cursor()` দিয়ে dictionary:

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT title, views FROM blog_post")
    columns = [col[0] for col in cursor.description]
    result = [dict(zip(columns, row)) for row in cursor.fetchall()]
```

---

## ১৩. Transactions

একাধিক database অপারেশনকে একক একক হিসেবে চালানো। কোনোটা fail হলে সব rollback হবে।

### `transaction.atomic()`:

```python
from django.db import transaction

try:
    with transaction.atomic():
        # সব কাজ একসাথে হবে
        author = Author.objects.create(name="রহিম")
        Post.objects.create(title="পোস্ট", content="কন্টেন্ট", author=author)
        # কোনোটা error দিলে সব rollback হবে
except Exception as e:
    print(f"সমস্যা: {e}")
```

### Decorator হিসেবে:

```python
from django.db import transaction

@transaction.atomic
def create_post_with_author(name, title):
    author = Author.objects.create(name=name)
    Post.objects.create(title=title, content="কন্টেন্ট", author=author)
```

### Savepoint:

```python
from django.db import transaction

with transaction.atomic():
    author = Author.objects.create(name="রহিম")
    try:
        with transaction.atomic():
            # এই block টা fail হলে শুধু এইটা rollback হবে
            Post.objects.create(title="", author=author)  # error
    except Exception:
        pass  # author থাকবে, পোস্ট হবে না
```

---

## ১৪. Signal — Model Event

Model-এর create/update/delete-এর আগে-পরে কোড চালানো।

### Import:

```python
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
```

### উদাহরণ — Post save-এ Profile তৈরি:

```python
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
```

### Signal-এর প্রকার:

| Signal | কখন চালায় |
|--------|-----------|
| `pre_save` | save-এর আগে |
| `post_save` | save-এর পরে |
| `pre_delete` | delete-এর আগে |
| `post_delete` | delete-এর পরে |
| `m2m_changed` | ManyToMany পরিবর্তন হলে |

---

## ১৫. `get_or_create()` ও `update_or_create()`

### `get_or_create()`:

না থাকলে তৈরি করবে, থাকলে নিয়ে আসবে।

```python
obj, created = Post.objects.get_or_create(
    title="টেস্ট",
    defaults={"content": "কন্টেন্ট", "status": "draft"},
)
# obj: object
# created: True (নতুন) / False (পুরনো)
```

### `update_or_create()`:

থাকলে আপডেট করবে, না থাকলে তৈরি করবে।

```python
obj, created = Post.objects.update_or_create(
    title="টেস্ট",
    defaults={"content": "নতুন কন্টেন্ট", "status": "published"},
)
```

---

## ১৬. Manager — Custom QuerySet

### Custom Manager:

```python
from django.db import models

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")

class Post(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=10, default="draft")

    objects = models.Manager()        # ডিফল্ট manager
    published = PublishedManager()    # custom manager

# ব্যবহার
Post.published.all()  # শুধু প্রকাশিত পোস্ট
Post.objects.all()    # সব পোস্ট
```

### Method যোগ করা:

```python
class PostManager(models.Manager):
    def popular(self):
        return self.get_queryset().filter(views__gt=1000)

    def by_author(self, author_name):
        return self.get_queryset().filter(author__name=author_name)

class Post(models.Model):
    # ...
    objects = PostManager()

# ব্যবহার
Post.objects.popular()
Post.objects.by_author("রহিম")
```

---

## ১৭. একটা সম্পূর্ণ উদাহরণ — Blog Analytics

```python
from django.db.models import Count, Sum, Avg, Q, F, Prefetch

# ১. জনপ্রিয় লেখক (পোস্ট সংখ্যা অনুযায়ী)
top_authors = Author.objects.annotate(
    post_count=Count("posts"),
    total_views=Sum("posts__views"),
).order_by("-post_count")[:5]

# ২. বছরের সেরা পোস্ট
best_posts = Post.objects.filter(
    created_at__year=2024,
    status="published"
).order_by("-views")[:10]

# ৩. সার্চ ফাংশন
def search(query):
    return Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()

# ৪. engagement অনুযায়ী সাজানো
engaging_posts = Post.objects.annotate(
    engagement=F("views") + F("likes") * 10 + Count("comments") * 5
).order_by("-engagement")

# ৫. প্রতি মাসের পোস্ট সংখ্যা
monthly_stats = Post.objects.values(
    "created_at__year", "created_at__month"
).annotate(
    count=Count("id")
).order_by("created_at__year", "created_at__month")

# ৬. Optimization সহ সব পোস্ট
posts = Post.objects.select_related(
    "author", "category"
).prefetch_related(
    "comments", "tags"
).filter(status="published")
```

---

## ১৮. সেরা প্র্যাকটিস (Best Practices)

1. ✅ N+1 query এড়াতে `select_related` ও `prefetch_related` ব্যবহার করুন
2. ✅ বড় queryset-এর জন্য `iterator()` ব্যবহার করুন
3. ✅ `exists()`, `count()`, `in_bulk()` ব্যবহার করুন যেখানে দরকার
4. ✅ জটিল query-র জন্য `Q` objects ব্যবহার করুন
5. ✅ Aggregation-এর জন্য `aggregate()` ও `annotate()` ব্যবহার করুন
6. ✅ একাধিক database অপারেশন-এর জন্য `transaction.atomic()` ব্যবহার করুন
7. ✅ `get_or_create()` ও `update_or_create()` ব্যবহার করুন
8. ✅ Raw SQL শুধু তখনই ব্যবহার করুন যখন ORM দিয়ে সম্ভব না
9. ❌ loop-এর ভেতরে query চালাবেন না (N+1 problem)
10. ❌ প্রয়োজন ছাড়া `all()` ব্যবহার করবেন না

---

## ১৯. Practical Exercise

```python
# ============ Exercise 1: Q Objects ============
from django.db.models import Q

# জনপ্রিয় পোস্ট (views>1000) অথবা ফিচার্ড
popular = Post.objects.filter(
    Q(views__gt=1000) | Q(is_featured=True)
)

# ড্রাফট নয় এমন সব পোস্ট
not_draft = Post.objects.filter(~Q(status="draft"))


# ============ Exercise 2: Aggregation ============
from django.db.models import Avg, Sum, Count, Max

stats = Post.objects.aggregate(
    total_posts=Count("id"),
    avg_views=Avg("views"),
    total_views=Sum("views"),
    max_views=Max("views"),
)
print(stats)


# ============ Exercise 3: Annotation ============
# প্রতিটা লেখকের পোস্ট সংখ্যা
authors = Author.objects.annotate(
    post_count=Count("posts")
).order_by("-post_count")

for author in authors:
    print(f"{author.name}: {author.post_count}")


# ============ Exercise 4: Optimization ============
# select_related (ForeignKey)
posts = Post.objects.select_related("author", "category").all()

# prefetch_related (ManyToMany)
posts = Post.objects.prefetch_related("tags", "comments").all()


# ============ Exercise 5: F Expression ============
from django.db.models import F

# views >= likes
Post.objects.filter(views__gte=F("likes"))

# সব views 10 বাড়ান
Post.objects.update(views=F("views") + 10)


# ============ Exercise 6: Transaction ============
from django.db import transaction

try:
    with transaction.atomic():
        author = Author.objects.create(name="নতুন লেখক")
        Post.objects.create(
            title="নতুন পোস্ট",
            content="কন্টেন্ট",
            author=author,
        )
    print("সফল!")
except Exception as e:
    print(f"সমস্যা: {e}")


# ============ Exercise 7: get_or_create ============
obj, created = Post.objects.get_or_create(
    title="টেস্ট পোস্ট",
    defaults={"content": "কন্টেন্ট", "status": "draft"},
)
print(f"তৈরি হয়েছে: {created}")
```

---

## 🎯 আজকের Key Takeaways

1. **QuerySet lazy** — যতক্ষণ evaluate না হবে ততক্ষণ query চালায় না
2. **Q Objects** — `|` (OR), `&` (AND), `~` (NOT) দিয়ে complex query
3. **Aggregation** — `aggregate()` দিয়ে `Avg`, `Sum`, `Count`, `Min`, `Max`
4. **Annotation** — `annotate()` দিয়ে নতুন field যোগ
5. **Optimization**:
   - `select_related` — ForeignKey/OneToOne (JOIN)
   - `prefetch_related` — ManyToMany/Reverse (আলাদা query)
6. **F Expression** — field দিয়ে গণনা ও তুলনা
7. **Case/When** — conditional logic
8. **Transaction** — `transaction.atomic()` দিয়ে একক একক অপারেশন
9. **Signals** — model event-এ কোড চালানো
10. **`get_or_create()` / `update_or_create()`** — সহজ create/update
11. **Custom Manager** — নিজের query method তৈরি

---

## ❓ অনুশীলনী প্রশ্ন

1. QuerySet কেন lazy বলা হয়?
2. Q Object দিয়ে OR query কীভাবে লেখা যায়?
3. `aggregate()` ও `annotate()` এর পার্থক্য কী?
4. `select_related` ও `prefetch_related` এর পার্থক্য কী?
5. N+1 problem কী? কীভাবে সমাধান করা যায়?
6. F Expression এর কাজ কী?
7. Transaction কী এবং কেন দরকার?
8. Signal কী? কখন ব্যবহার করা হয়?
9. `get_or_create()` কীভাবে কাজ করে?
10. Custom Manager কীভাবে তৈরি করা যায়?
