# Django: Migrations — makemigrations ও migrate 🔄

Django-এ **Migration** হলো database schema-এর পরিবর্তন সংরক্ষণ ও apply করার প্রক্রিয়া। Model পরিবর্তন করলে migration দিয়ে database-এ update করা হয়।

---

## ১. Migration কী এবং কেন দরকার?

Django-এ database table-এর structure model class দিয়ে তৈরি করা হয়। কিন্তু model পরিবর্তন করলে database-এ সেই পরিবর্তন apply করতে migration দরকার।

### Migration-এর কাজ:
- 📝 Model পরিবর্তন ট্র্যাক করা
- 🗄️ Database schema আপডেট করা
- 🔄 পুরনো অবস্থায় ফিরে যাওয়া (rollback)
- 🤝 টিমের সাথে database পরিবর্তন শেয়ার করা

### ছাড়া Migration কেমন হতো?
- প্রতিবার model পরিবর্তন করলে ম্যানুয়ালি SQL লিখতে হতো
- টিমের সবাইকে একই SQL দিতে হতো
- ভুল হলে database নষ্ট হতে পারতো

---

## ২. Migration-এর মূল কমান্ডসমূহ

| কমান্ড | কাজ |
|--------|------|
| `makemigrations` | নতুন migration ফাইল তৈরি |
| `migrate` | Migration database-এ apply করা |
| `showmigrations` | সব migration-এর অবস্থা দেখা |
| `sqlmigrate` | Migration-এর SQL দেখা |
| `migrate --fake` | Migration fake করা (database-এ apply ছাড়াই) |
| `migrate app_name zero` | একটা app-এর সব migration rollback |
| `squashmigrations` | একাধিক migration একসাথে জমা |

---

## ৩. makemigrations — Migration ফাইল তৈরি

### কীভাবে কাজ করে?

`makemigrations` model-এর পরিবর্তন দেখে নতুন migration ফাইল তৈরি করে।

```bash
python manage.py makemigrations
```

আউটপুট:
```
Migrations for 'blog':
  blog/migrations/0002_post_slug.py
    - Add field slug to post
```

### নির্দিষ্ট app-এর জন্য:

```bash
python manage.py makemigrations blog
```

### Dry-run (শুধু দেখা, ফাইল তৈরি না করা):

```bash
python manage.py makemigrations --dry-run
```

### Name দিয়ে:

```bash
python manage.py makemigrations blog --name add_slug_to_post
```

### Empty migration তৈরি:

```bash
python manage.py makemigrations blog --empty
```

---

## ৪. migrate — Database-এ Apply করা

### কীভাবে কাজ করে?

`migrate` migration ফাইলগুলো database-এ apply করে।

```bash
python manage.py migrate
```

আউটপুট:
```
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying blog.0002_post_slug... OK
```

### নির্দিষ্ট app-এর জন্য:

```bash
python manage.py migrate blog
```

### নির্দিষ্ট migration পর্যন্ত:

```bash
python manage.py migrate blog 0001
```

### Rollback (পিছনে যাওয়া):

```bash
# প্রথম migration-এ ফিরে যাওয়া
python manage.py migrate blog 0001

# সব migration মুছে ফেলা
python manage.py migrate blog zero
```

---

## ৫. Migration ফাইলের কাঠামো

Migration ফাইল Python কোড, SQL না। এটা `migrations/` ফোল্ডারে থাকে।

### উদাহরণ:

```python
# blog/migrations/0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
```

### অংশসমূহ:

| অংশ | কাজ |
|------|------|
| `dependencies` | আগের migration-এর উপর নির্ভরশীলতা |
| `operations` | কী পরিবর্তন হবে তা লিস্ট |
| `initial` | এটা প্রথম migration কিনা |

---

## ৬. Migration Operations

Migration-এ বিভিন্ন operation আছে:

| Operation | কাজ |
|-----------|------|
| `CreateModel` | নতুন table তৈরি |
| `DeleteModel` | Table মুছে ফেলা |
| `AddField` | নতুন column যোগ |
| `RemoveField` | Column মুছে ফেলা |
| `AlterField` | Column-এর ধরন পরিবর্তন |
| `RenameField` | Column-এর নাম পরিবর্তন |
| `AddIndex` | নতুন index যোগ |
| `AlterUniqueTogether` | Unique constraint পরিবর্তন |
| `RunSQL` | সরাসরি SQL চালানো |
| `RunPython` | Python কোড চালানো |

### AddField উদাহরণ:

```python
# blog/migrations/0002_post_slug.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="slug",
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
```

---

## ৭. Migration-এর পুরো প্রক্রিয়া

### ধাপ ১: Model পরিবর্তন করুন

```python
# blog/models.py
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)  # নতুন field
    created_at = models.DateTimeField(auto_now_add=True)
```

### ধাপ ২: makemigrations চালান

```bash
python manage.py makemigrations
```

ফাইল তৈরি হবে: `blog/migrations/0002_post_slug.py`

### ধাপ ৩: SQL দেখুন (ঐচ্ছিক)

```bash
python manage.py sqlmigrate blog 0002
```

আউটপুট:
```sql
ALTER TABLE "blog_post" ADD COLUMN "slug" varchar(200) NOT NULL UNIQUE;
```

### ধাপ ৪: migrate চালান

```bash
python manage.py migrate
```

Database-এ পরিবর্তন apply হবে।

---

## ৮. showmigrations — অবস্থা দেখা

```bash
python manage.py showmigrations
```

আউটপুট:
```
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
blog
 [X] 0001_initial
 [ ] 0002_post_slug    # ❌ apply হয়নি
```

- `[X]` = apply হয়েছে
- `[ ]` = apply হয়নি

### নির্দিষ্ট app:

```bash
python manage.py showmigrations blog
```

---

## ৯. sqlmigrate — SQL দেখা

```bash
python manage.py sqlmigrate blog 0002
```

আউটপুট:
```sql
BEGIN;
--
-- Add field slug to post
--
ALTER TABLE "blog_post" ADD COLUMN "slug" varchar(200) NOT NULL;
ALTER TABLE "blog_post" ADD CONSTRAINT "blog_post_slug_key" UNIQUE ("slug");
COMMIT;
```

---

## ১০. নতুন field যোগ করার সময় সমস্যা

নতুন `NOT NULL` field যোগ করলে Django প্রম্পট দেয়:

```bash
python manage.py makemigrations
```

আউটপুট:
```
It is impossible to add a non-nullable field 'slug' to post without specifying a default.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows)
 2) Quit and manually define a default value in models.py.
```

### সমাধান ১: Default দিন

```python
slug = models.SlugField(max_length=200, unique=True, default="")
```

### সমাধান ২: Nullable করুন

```python
slug = models.SlugField(max_length=200, unique=True, null=True)
```

### সমাধান ৩: One-off default দিন

প্রম্পটে `1` সিলেক্ট করে একটা মান দিন।

---

## ১১. Data Migration — RunPython

Data migration দিয়ে existing data পরিবর্তন করা যায়।

### উদাহরণ — slug generate করা:

```python
# blog/migrations/0003_generate_slugs.py
from django.db import migrations
from django.utils.text import slugify

def generate_slugs(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    for post in Post.objects.all():
        post.slug = slugify(post.title)
        post.save()

class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_post_slug"),
    ]

    operations = [
        migrations.RunPython(generate_slugs, migrations.RunPython.noop),
    ]
```

> 💡 `apps.get_model()` ব্যবহার করুন — সরাসরি model import করবেন না।

---

## ১২. Rollback — পিছনে যাওয়া

### নির্দিষ্ট migration-এ ফিরে যাওয়া:

```bash
python manage.py migrate blog 0001
```

এটা `0002` এবং তার পরের migrations revert করবে।

### সব migration মুছে ফেলা:

```bash
python manage.py migrate blog zero
```

### Rollback SQL দেখা:

```bash
python manage.py sqlmigrate blog 0001 --backwards
```

---

## ১৩. Fake Migration

কখনও কখনো database-এ আগে থেকেই table আছে, কিন্তু Django migration ট্র্যাক করছে না। তখন `--fake` ব্যবহার করা হয়।

```bash
python manage.py migrate blog --fake
```

এটা database-এ কোনো পরিবর্তন করবে না, কিন্তু migration applied হিসেবে চিহ্নিত করবে।

### নির্দিষ্ট migration fake করা:

```bash
python manage.py migrate blog 0001 --fake
```

---

## ১৪. Squash Migrations

অনেক migration জমে গেলে একটাতে জমা করা যায়।

```bash
python manage.py squashmigrations blog 0001 0005
```

এটা `0001` থেকে `0005` পর্যন্ত সব migration একসাথে জমা করবে।

আউটপুট:
```
Will squash the following migrations:
 - 0001_initial
 - 0002_post_slug
 - 0003_post_featured
 - 0004_post_views
 - 0005_post_author
Do you wish to proceed? [y/N]
```

---

## ১৫. Migration Conflict

দুই বা ততোধিক developer একই app-এ একই সময়ে migration তৈরি করলে conflict হতে পারে।

### Conflict দেখা:

```bash
python manage.py makemigrations --check
```

আউটপুট:
```
CommandError: System check identified some issues:

ERRORS:
blog: (admin.E005) The value of 'raw_id_fields' refers to 'blog.Post', which has more than one field with 'primary_key=True'.
```

### সমাধান — Merge:

```bash
python manage.py makemigrations --merge
```

অথবা ম্যানুয়ালি dependencies ঠিক করুন।

---

## ১৬. Migration কখনো কখনো মুছে ফেলা?

⚠️ **সাবধান:** প্রোডাকশনে migration কখনো মুছবেন না।

### Development-এ মুছে ফেলার নিয়ম:

1. Database-এ data গুরুত্বপূর্ণ না
2. সবাই নতুন শুরু করছে

### ধাপ:

```bash
# ১. database মুছুন
rm db.sqlite3

# ২. migration ফাইলগুলো মুছুন (শুধু __init__.py ছাড়া)
rm blog/migrations/0*.py

# ৩. নতুন migration তৈরি করুন
python manage.py makemigrations

# ৪. migrate করুন
python manage.py migrate
```

> ⚠️ এটা শুধু development-এ করুন। Production-এ কখনো করবেন না।

---

## ১৭. Production-এ Migration

Production-এ migration করার সময় সতর্ক থাকুন।

### কাজের ক্রম:

```bash
# ১. Backup নিন
pg_dump dbname > backup.sql  # PostgreSQL

# ২. Maintenance mode চালু করুন

# ৩. Migration চালান
python manage.py migrate

# ৪. Static files collect করুন
python manage.py collectstatic

# ৫. Server restart করুন
```

### Migration-এর সেরা প্র্যাকটিস:
1. ✅ Migration করার আগে backup নিন
2. ✅ Batching করে migration চালান
3. ✅ Downtime কমানোর চেষ্টা করুন
4. ✅ Rollback plan রাখুন
5. ❌ Production-এ migration মুছবেন না
6. ❌ Production-এ `--fake` সাবধানে ব্যবহার করুন

---

## ১৮. সাধারণ সমস্যা ও সমাধান

### সমস্যা ১: `No migrations to apply`

**কারণ:** সব migration আগে থেকেই apply হয়েছে।

**সমাধান:** কিছু করতে হবে না।

### সমস্যা ২: `Table already exists`

**কারণ:** Database-এ table আছে, কিন্তু migration ট্র্যাক করছে না।

**সমাধান:**
```bash
python manage.py migrate --fake
```

### সমস্যা ৩: `Migration has been modified`

**কারণ:** আগের migration ফাইল পরিবর্তন করা হয়েছে।

**সমাধান:** Migration ফাইল কখনো পরিবর্তন করবেন না। নতুন migration তৈরি করুন।

### সমস্যা ৪: `InconsistentMigrationHistory`

**কারণ:** কোনো migration apply হয়েছে কিন্তু তার dependency হয়নি।

**সমাধান:**
```bash
python manage.py migrate --fake
```

---

## ১৯. Migration-এর সেরা প্র্যাকটিস

1. ✅ প্রতিটা পরিবর্তনের জন্য আলাদা migration তৈরি করুন
2. ✅ Migration ফাইল কখনো এডিট করবেন না
3. ✅ Migration commit করুন git-এ
4. ✅ `makemigrations`-এর পর `migrate` চালান
5. ✅ `sqlmigrate` দিয়ে SQL পরীক্ষা করুন
6. ✅ `showmigrations` দিয়ে অবস্থা চেক করুন
7. ✅ Production-এ backup নিন
8. ❌ Production-এ migration মুছবেন না
9. ❌ Migration ফাইল এডিট করবেন না
10. ❌ একসাথে অনেক বড় migration করবেন না

---

## ২০. Practical Exercise

```bash
# ============ Exercise 1: Basic Migration ============
# ১. একটা নতুন field যোগ করুন models.py-এ
# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200, unique=True)  # নতুন

# ২. migration তৈরি করুন
python manage.py makemigrations

# ৩. SQL দেখুন
python manage.py sqlmigrate blog 0002

# ৪. apply করুন
python manage.py migrate

# ৫. অবস্থা দেখুন
python manage.py showmigrations blog


# ============ Exercise 2: Data Migration ============
# নতুন migration তৈরি করুন
python manage.py makemigrations blog --empty --name generate_slugs

# ফাইলে RunPython যোগ করুন
# from django.utils.text import slugify
# def generate_slugs(apps, schema_editor):
#     Post = apps.get_model("blog", "Post")
#     for post in Post.objects.all():
#         post.slug = slugify(post.title)
#         post.save()

# apply করুন
python manage.py migrate


# ============ Exercise 3: Rollback ============
# 0001-এ ফিরে যান
python manage.py migrate blog 0001

# আবার সব apply করুন
python manage.py migrate


# ============ Exercise 4: Show & SQL ============
# সব migration দেখুন
python manage.py showmigrations

# নির্দিষ্ট migration-এর SQL
python manage.py sqlmigrate blog 0002
```

---

## 🎯 আজকের Key Takeaways

1. **Migration** = database schema-এর পরিবর্তন ট্র্যাক ও apply
2. **`makemigrations`** — নতুন migration ফাইল তৈরি
3. **`migrate`** — database-এ apply
4. **`showmigrations`** — অবস্থা দেখা
5. **`sqlmigrate`** — SQL দেখা
6. **Migration Operations**: CreateModel, AddField, RemoveField, RunPython
7. **Data Migration** — `RunPython` দিয়ে existing data পরিবর্তন
8. **Rollback** — `migrate app 0001` বা `migrate app zero`
9. **Fake** — `--fake` দিয়ে কিন্তু apply না করেই ট্র্যাক
10. **Squash** — অনেক migration একসাথে জমা
11. Production-এ সাবধানে কাজ করুন

---

## ❓ অনুশীলনী প্রশ্ন

1. Migration কী এবং কেন দরকার?
2. `makemigrations` ও `migrate` এর পার্থক্য কী?
3. `showmigrations` কমান্ডের কাজ কী?
4. `sqlmigrate` দিয়ে কী দেখা যায়?
5. নতুন `NOT NULL` field যোগ করলে কী সমস্যা হয় এবং কীভাবে সমাধান করা যায়?
6. Data Migration কী? কখন ব্যবহার করা হয়?
7. Rollback কীভাবে করা যায়?
8. `--fake` কখন ব্যবহার করা হয়?
9. Production-এ migration করার সেরা প্র্যাকটিস কী কী?
10. Migration ফাইল কখনো এডিট করা উচিত না কেন?
