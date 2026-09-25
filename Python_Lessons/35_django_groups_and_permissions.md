# Django Groups ও Permissions 👥🛡️

ওয়েব অ্যাপ্লিকেশনে বিভিন্ন ব্যবহারকারীর জন্য আলাদা আলাদা ক্ষমতা ও প্রবেশাধিকার নির্ধারণ করার সবচেয়ে কার্যকর কাঠামো হলো **Role-Based Access Control (RBAC)**। Django-তে এটি পরিচালনার জন্য রয়েছে শক্তিশালী **Permissions** এবং **Groups** সিস্টেম।

এই পূর্ণাঙ্গ গাইডে আমরা শিখব পারমিশন ও গ্রুপ কীভাবে কাজ করে, কোড ও অ্যাডমিন প্যানেল দিয়ে এগুলো তৈরি ও পরিচালনা, ভিউ ও টেমপ্লেটে নিয়ন্ত্রণ এবং প্রজেক্টের শুরুতে স্বয়ংক্রিয়ভাবে ডিফল্ট গ্রুপ সেটআপ করার প্রফেশনাল টেকনিক।

---

## ১. Groups ও Permissions-এর মৌলিক ধারণা

```mermaid
graph TD
    subgraph ১. Permissions "সুনির্দিষ্ট কাজের অনুমতি"
        P1[blog.add_post]
        P2[blog.change_post]
        P3[blog.delete_post]
        P4[blog.view_post]
    end

    subgraph ২. Groups "ভূমিকা বা রোল Role"
        G1[Editors গ্রুপ]
        G2[Authors গ্রুপ]
        G3[Readers গ্রুপ]
    end

    subgraph ৩. Users "ব্যবহারকারীগণ"
        U1[Rahim]
        U2[Karim]
        U3[Fatima]
    end

    P1 & P2 & P3 --> G1
    P1 & P4 --> G2
    P4 --> G3

    G1 --> U1
    G2 --> U2
    G3 --> U3
```

* **Permission (অনুমতি):** সিস্টেমে একটি নির্দিষ্ট মডেলের ওপর কোনো সুনির্দিষ্ট কাজ করার অধিকার (যেমন: পোস্ট তৈরি, এডিট, ডিলিট বা দেখা)।
* **Group (দল / ভূমিকা):** একাধিক পারমিশনের একটি সংকলন বা ক্যাটাগরি (যেমন: *Editors*, *Moderators*, *Vendors*)। একজন ইউজারকে গ্রুপে যুক্ত করলে সে ওই গ্রুপের **সকল পারমিশন স্বয়ংক্রিয়ভাবে** পেয়ে যায়।

> 💡 **কেন গ্রুপ ব্যবহার করবেন?**
> যদি আপনার সাইটে ১০০ জন এডিটর থাকে এবং ভবিষ্যতে এডিটরদের একটি নতুন পারমিশন দিতে হয়, তবে ১০০ জন ইউজারকে আলাদাভাবে পারমিশন দেওয়ার বদলে শুধু *Editors* গ্রুপে ১ বার পারমিশন যোগ করলেই ১০০ জন তা স্বয়ংক্রিয়ভাবে পেয়ে যাবে!

---

## ২. Django-র Built-in Model Permissions

আপনি যখনই কোনো মডেল তৈরি করে `makemigrations` এবং `migrate` চালান, Django স্বয়ংক্রিয়ভাবে ৪টি পারমিশন তৈরি করে:

পারমিশনের ফরম্যাট: `<app_label>.<action>_<modelname>`

ধরা যাক `blog` অ্যাপে একটি `Article` মডেল আছে:

| Codename | অ্যাকশন | পারমিশন স্ট্রিং | বিবরণ |
| :--- | :--- | :--- | :--- |
| `add_article` | তৈরি | `blog.add_article` | নতুন আর্টিকেল তৈরি করার অনুমতি |
| `change_article`| সম্পাদনা | `blog.change_article` | বিদ্যমান আর্টিকেল এডিট করার অনুমতি |
| `delete_article`| মুছে ফেলা | `blog.delete_article` | আর্টিকেল মুছে ফেলার অনুমতি |
| `view_article`  | প্রদর্শন | `blog.view_article` | আর্টিকেল বিস্তারিত দেখার অনুমতি |

---

## ৩. কোড ও ORM দিয়ে Groups ও Permissions ব্যবস্থাপনা

Django-র `django.contrib.auth.models` মডিউল থেকে `Group` এবং `Permission` মডেল ব্যবহার করা হয়।

### ক. গ্রুপ তৈরি করা এবং পারমিশন যুক্ত করা:

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Article

# ১. গ্রুপ তৈরি করা (বা খুঁজে নেওয়া)
editor_group, created = Group.objects.get_or_create(name='Editors')

# ২. Article মডেলের জন্য ContentType বের করা
content_type = ContentType.objects.get_for_model(Article)

# ৩. Article মডেলের পারমিশনগুলো খুঁজে বের করা
article_permissions = Permission.objects.filter(
    content_type=content_type,
    codename__in=['add_article', 'change_article', 'view_article']
)

# ৪. গ্রুপে পারমিশনগুলো যোগ করা
editor_group.permissions.set(article_permissions)
# অথবা একটি করে যোগ করতে:
# editor_group.permissions.add(some_perm)
```

---

### খ. ব্যবহারকারীকে গ্রুপে যুক্ত বা অপসারণ করা:

```python
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='rahim')

# ইউজারকে Editors গ্রুপে যোগ করা
editor_group = Group.objects.get(name='Editors')
user.groups.add(editor_group)

# ইউজারকে গ্রুপ থেকে সরানো
user.groups.remove(editor_group)

# ইউজারের সব গ্রুপ ক্লিয়ার করা
user.groups.clear()
```

---

### গ. ব্যবহারকারীকে সরাসরি ব্যক্তিগত পারমিশন দেওয়া:

কোনো ইউজারকে কোনো গ্রুপে না দিয়েও সরাসরি নির্দিষ্ট পারমিশন দেওয়া যায় (`user_permissions`):

```python
perm = Permission.objects.get(codename='delete_article')
user.user_permissions.add(perm)
```

---

## ৪. কোডে পারমিশন ও গ্রুপ যাচাই করার নিয়ম

### ১. পারমিশন যাচাই (`has_perm`):

```python
user = request.user

# ১. একক পারমিশন যাচাই:
if user.has_perm('blog.delete_article'):
    print("ইউজার আর্টিকেল ডিলিট করতে পারবে")

# ২. একাধিক পারমিশন একসাথে যাচাই:
if user.has_perms(['blog.change_article', 'blog.delete_article']):
    print("ইউজার এডিট ও ডিলিট দুটোই করতে পারবে")
```

> ⚠️ **মনে রাখুন:** `user.has_perm()` ফাংশনটি ইউজারের ব্যক্তিগত পারমিশন এবং সে যে যে গ্রুপে আছে তার **উভয় পারমিশন মিলিয়ে** চেক করে। আর ইউজার যদি `is_superuser=True` হয়, তবে সে কোনো পারমিশন না থাকা সত্ত্বেও সর্বদা `True` পাবে।

---

### ২. গ্রুপ যাচাই:

```python
# ইউজার নির্দিষ্ট কোনো গ্রুপে আছে কিনা:
if user.groups.filter(name='Editors').exists():
    print("ইউজার একজন এডিটর")
```

---

## ৫. কাস্টম পারমিশন (Custom Permissions) তৈরি করা

বিল্ট-ইন ৪টি কাজের বাইরে যদি বিশেষ কোনো অ্যাকশনের অনুমতি লাগে (যেমন: আর্টিকেল পাবলিশ করা, ফিচার্ড করা বা আর্কাইভ করা), তা মডেলের `Meta` ক্লাসে লিখতে হয়:

```python
# blog/models.py
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("can_publish_article", "আর্টিকেল প্রকাশ (Publish) করার অনুমতি"),
            ("can_archive_article", "আর্টিকেল সংরক্ষণ (Archive) করার অনুমতি"),
        ]
```

মাইগ্রেশন কমান্ড চালালে এই পারমিশনগুলো ডেটাবেজে নিবন্ধিত হবে:
```bash
python manage.py makemigrations
python manage.py migrate
```

এখন এটি কোডে সাধারণ পারমিশনের মতোই ব্যবহারযোগ্য:
```python
if user.has_perm('blog.can_publish_article'):
    article.is_published = True
    article.save()
```

---

## ৬. Views-এ অ্যাক্সেস কন্ট্রোল প্রয়োগ

### ১. `@permission_required` ডেকোরেটর (FBV)

```python
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article

# raise_exception=True দিলে অনুমতি না থাকলে 403 Forbidden এরর ছুড়ে দেবে
@permission_required('blog.delete_article', raise_exception=True)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('article_list')
```

---

### ২. `@user_passes_test` ডেকোরেটর (গ্রুপ ও কাস্টম শর্ত)

```python
from django.contrib.auth.decorators import user_passes_test

# শর্ত: শুধুমাত্র এডিটর বা সুপারইউজার
def is_editor(user):
    return user.is_authenticated and (user.groups.filter(name='Editors').exists() or user.is_superuser)

@user_passes_test(is_editor, login_url='access_denied')
def editor_dashboard(request):
    return render(request, 'editor_dashboard.html')
```

---

### ৩. Class-Based Views-এ পারমিশন (`PermissionRequiredMixin`)

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import Article

class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    permission_required = 'blog.delete_article'
    # অনুমতি না থাকলে লগইনে না পাঠিয়ে 403 Forbidden দেখানো ভালো:
    raise_exception = True
    success_url = reverse_lazy('article_list')
```

---

## ৭. Templates-এ `perms` দিয়ে শর্তাধীন UI

Django টেমপ্লেটে একটি বিশেষ অবজেক্ট থাকে: **`perms`**। এটি দিয়ে ব্রাউজারে বাটন দেখানো বা লুকানো যায়:

```html
<!-- templates/article_detail.html -->
<div class="card p-4">
    <h2>{{ article.title }}</h2>
    <p>{{ article.content }}</p>

    <div class="d-flex gap-2 mt-4">
        <a href="{% url 'article_list' %}" class="btn btn-secondary">তালিকায় ফিরুন</a>

        <!-- শুধুমাত্র change_article পারমিশন থাকলে এডিট বাটন দেখাবে -->
        {% if perms.blog.change_article %}
            <a href="{% url 'article_edit' article.pk %}" class="btn btn-warning">
                <i class="bi bi-pencil"></i> সম্পাদনা
            </a>
        {% endif %}

        <!-- শুধুমাত্র delete_article পারমিশন থাকলে ডিলিট বাটন দেখাবে -->
        {% if perms.blog.delete_article %}
            <a href="{% url 'article_delete' article.pk %}" class="btn btn-danger">
                <i class="bi bi-trash"></i> মুছুন
            </a>
        {% endif %}

        <!-- কাস্টম পারমিশন: can_publish_article -->
        {% if perms.blog.can_publish_article and not article.is_published %}
            <a href="{% url 'article_publish' article.pk %}" class="btn btn-success">
                <i class="bi bi-check-circle"></i> পাবলিশ করুন
            </a>
        {% endif %}
    </div>
</div>
```

---

## ৮. প্রো-টিপ: Data Migration দিয়ে ডিফল্ট Groups তৈরি

প্রোডাকশন সার্ভারে প্রতিবার ম্যানুয়ালি অ্যাডমিন প্যানেলে গিয়ে গ্রুপ ও পারমিশন সেট না করে, একটি **Data Migration** তৈরি করে রাখা সবচেয়ে প্রফেশনাল পদ্ধতি:

```bash
python manage.py makemigrations --empty accounts
```

তৈরি হওয়া মাইগ্রেশন ফাইলে লিখুন:

```python
# accounts/migrations/0002_create_default_groups.py
from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # গ্রুপ তৈরি
    editor_group, _ = Group.objects.get_or_create(name='Editors')
    author_group, _ = Group.objects.get_or_create(name='Authors')

    # পারমিশন যুক্ত করা
    change_art = Permission.objects.filter(codename='change_article')
    add_art = Permission.objects.filter(codename='add_article')

    editor_group.permissions.set(change_art | add_art)
    author_group.permissions.set(add_art)

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
```

এখন যেকোনো মেশিনে বা প্রোডাকশন সার্ভারে `python manage.py migrate` চালালেই অটোমেটিক গ্রুপগুলো তৈরি হয়ে যাবে!

---

## 🎯 আজকের Key Takeaways

1. **Permission** একক মডেল অ্যাকশন নিয়ন্ত্রণ করে; আর **Group** হলো একাধিক পারমিশনের দলীয় সংকলন (Role)।
2. Django স্বয়ংক্রিয়ভাবে ৪টি পারমিশন তৈরি করে: `add`, `change`, `delete`, `view`।
3. পারমিশন স্ট্রিং ফরম্যাট: `<app_label>.<action>_<modelname>` (যেমন: `blog.delete_article`)।
4. কোডে পারমিশন চেক করতে `user.has_perm()` এবং টেমপ্লেটে `perms.app_label.codename` ব্যবহার করুন।
5. `is_superuser=True` হলে ইউজার কোনো পারমিশন অ্যাসাইন করা ছাড়াই সকল ক্ষমতা পায়।
6. মডেলের `class Meta: permissions = [...]` দিয়ে কাস্টম পারমিশন তৈরি করা যায়।
7. ভিউ সুরক্ষায় `@permission_required(..., raise_exception=True)` ব্যবহার করুন যাতে অননুমোদিত ইউজার সরাসরি 403 Forbidden পায়।

---

## ❓ অনুশীলনী প্রশ্ন

1. Django-তে Groups ব্যবহারের প্রধান সুবিধা কী?
2. একটি নতুন মডেল তৈরি করলে Django স্বয়ংক্রিয়ভাবে কোন ৪টি পারমিশন তৈরি করে?
3. `user.has_perm()` মেথড কীভাবে ইউজারের ব্যক্তিগত এবং গ্রুপ পারমিশন মিলিয়ে রেজাল্ট দেয়?
4. কাস্টম পারমিশন ডিক্লেয়ার করার জন্য মডেলের কোন ক্লাসে কোড লিখতে হয়?
5. `raise_exception=True` আর্গুমেন্টটি `@permission_required` ডেকোরেটরে কেন ব্যবহার করা উচিত?
6. টেমপ্লেটে শুধুমাত্র যাদের `can_publish` পারমিশন আছে তাদের বাটন দেখানোর DTL সিনট্যাক্স কী?
7. একজন ইউজারকে একটি নির্দিষ্ট গ্রুপে যোগ করার এবং গ্রুপ থেকে সরানোর ORM কমান্ড কী?
8. একজন ইউজার সুপারইউজার হলে `user.has_perm('non_existing_perm')` কী রিটার্ন করবে এবং কেন?
9. `user.groups.filter(name='Moderators').exists()` কী কাজ করে?
10. প্রোডাকশনে নতুন সার্ভার ডেপ্লয়ের সময় গ্রুপ ও পারমিশন স্বয়ংক্রিয়ভাবে তৈরি করার সেরা উপায় কী?
