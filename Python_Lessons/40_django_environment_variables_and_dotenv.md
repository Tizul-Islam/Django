# Django Environment Variables ও .env 🔐🛡️

একটি আধুনিক ও নিরাপদ ওয়েব অ্যাপ্লিকেশনে কখনোই ডেটাবেজের পাসওয়ার্ড, সিক্রেট কি (Secret Key) বা এপিআই কি সরাসরি কোডের ভেতর লিখে (Hardcode) রাখা উচিত নয়।

কোড ও কনফিগারেশন আলাদা রাখাকে সফটওয়্যার ডেভেলপমেন্টে **12-Factor App Methodology (III. Config)** বলা হয়। এর জন্য পরিবেশ ভেরিয়েবল বা **Environment Variables** এবং **`.env`** ফাইল ব্যবহার করা হয়।

এই পূর্ণাঙ্গ গাইডে আমরা শিখব কেন `.env` ব্যবহার বাধ্যতামূলক, কীভাবে `python-dotenv` ও `django-environ` দিয়ে গোপন তথ্য সুরক্ষিত রাখতে হয় এবং গিটহাবে ভুলবশত পাসওয়ার্ড ফাঁস হওয়া রোধ করার সেরা কৌশল।

---

## ১. কেন Environment Variables ব্যবহার অপরিহার্য?

### কোডে সরাসরি পাসওয়ার্ড রাখলে কী কী বিপদ হতে পারে? 🚨
1. **GitHub-এ সিক্রেট ফাঁস:** যদি আপনার কোড গিটহাবে পুশ করেন (বিশেষ করে পাবলিক রিপোজিটরিতে), তবে বট ও হ্যাকাররা সেকেন্ডের মধ্যে আপনার `SECRET_KEY`, ডেটাবেজের পাসওয়ার্ড ও পেমেন্ট গেটওয়ের API Key চুরি করে নেবে।
2. **পরিবেশভেদে কনফিগারেশন পরিবর্তন:** আপনার লোকাল কম্পিউটারে `DEBUG = True` থাকতে পারে, কিন্তু প্রোডাকশন লাইভ সার্ভারে অবশ্যই `DEBUG = False` হতে হবে। লোকাল ও লাইভ সার্ভারে আলাদা আলাদা ডেটাবেজ থাকে। কোড পরিবর্তন না করে শুধু পরিবেশ ভেরিয়েবল বদলেই এটি ম্যানেজ করা যায়।
3. **টিমওয়ার্কে সুবিধা:** টিমের প্রত্যেক ডেভেলপার তার নিজস্ব কম্পিউটারের জন্য আলাদা `.env` ফাইল ব্যবহার করতে পারে, মূল কোডব্যাংক একই থাকে।

---

## ২. `.env` ফাইলের গঠন ও নিয়মাবলী

প্রজেক্টের রুট ডিরেক্টরিতে (যেখানে `manage.py` থাকে) একটি ফাইল তৈরি করা হয় যার নাম শুধুই **`.env`** (কোনো নাম নেই, শুধু এক্সটেনশন):

```bash
# .env ফাইলের নমুনা (KEY=VALUE ফরম্যাটে)

# Django Core Settings
SECRET_KEY=django-insecure-98@7!#example-secret-key-do-not-share
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database Settings
DB_NAME=my_project_db
DB_USER=postgres
DB_PASSWORD=my_secure_db_password123
DB_HOST=localhost
DB_PORT=5432

# Email Settings
EMAIL_HOST_USER=myemail@gmail.com
EMAIL_HOST_PASSWORD=my-16-digit-app-password

# Third-party APIs
STRIPE_SECRET_KEY=sk_test_51Mz...
CLOUDINARY_API_KEY=123456789
```

### ⚠️ `.env` লেখার ৩টি নিয়ম:
1. `=` চিহ্নের দুইপাশে কোনো স্পেস (Space) রাখা যাবে না (`KEY=VALUE` ✅, `KEY = VALUE` ❌)।
2. কোটেশনের প্রয়োজন নেই, তবে স্ট্রিংয়ে স্পেস থাকলে ডাবল কোটেশন ব্যবহার করা যায় (`SITE_NAME="My Great Site"`).
3. `#` দিয়ে কমেন্ট লেখা যায়।

---

## ৩. পদ্ধতি ১: `python-dotenv` দিয়ে বাস্তবায়ন (সহজ ও বহুল ব্যবহৃত)

### ধাপ ১: লাইব্রেরি ইনস্টল করুন
```bash
pip install python-dotenv
```

---

### ধাপ ২: `settings.py`-এ লোড করুন

আপনার `config/settings.py` ফাইলের একদম শীর্ষে নিচের কোড যুক্ত করুন:

```python
# config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# BASE_DIR পাথ
BASE_DIR = Path(__file__).resolve().parent.parent

# 🚀 .env ফাইল লোড করা
load_dotenv(BASE_DIR / '.env')

# ১. Secret Key লোড করা
SECRET_KEY = os.getenv('SECRET_KEY')

# ২. DEBUG মোড লোড করা (স্ট্রিং থেকে বুলিয়ানে রূপান্তর)
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# ৩. ALLOWED_HOSTS লোড করা (কমা দিয়ে আলাদা করে লিস্টে রূপান্তর)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
```

> 💡 **নোট:** `os.getenv('KEY', 'Default_Value')` ব্যবহার করলে `.env`-এ মান না পেলেও ডিফল্ট মান ব্যবহার হবে, ফলে সার্ভার ক্র্যাশ করবে না।

---

## ৪. পদ্ধতি ২: `django-environ` দিয়ে বাস্তবায়ন (প্রোডাকশন স্ট্যান্ডার্ড 🏆)

`django-environ` হলো Django-র জন্য সবচেয়ে চমৎকার প্যাকেজ। এটি স্বয়ংক্রিয়ভাবে টাইপ কাস্টিং (Boolean, List, Integer) করে এবং এমনকি এক লাইনে পুরো Database URL পার্স করতে পারে!

### ধাপ ১: লাইব্রেরি ইনস্টল করুন
```bash
pip install django-environ
```

---

### ধাপ ২: `settings.py` কনফিগার করুন

```python
# config/settings.py
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# environ শুরু করা
env = environ.Env(
    # ডিফল্ট ভ্যালু ও টাইপ কাস্টিং ডিফাইন করা
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['127.0.0.1', 'localhost'])
)

# .env ফাইল রিড করা
environ.Env.read_env(BASE_DIR / '.env')

# ভেরিয়েবল অ্যাক্সেস করা:
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')  # স্বয়ংক্রিয়ভাবে True বা False বুলিয়ান হবে
ALLOWED_HOSTS = env('ALLOWED_HOSTS')  # স্বয়ংক্রিয়ভাবে লিস্ট হবে

# 🔥 এক লাইনে Database কনফিগারেশন:
DATABASES = {
    # .env তে DATABASE_URL=postgres://user:pass@localhost:5432/dbname থাকলে অটো পার্স করে
    'default': env.db('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}
```

---

## ৫. `.gitignore` এবং `.env.example`-এর গুরুত্ব 🛡️

### ১. `.gitignore`-এ `.env` যুক্ত রাখা:
কখনোই যেন `.env` ফাইল গিটহাবে পুশ না হয়, সেজন্য আপনার প্রজেক্টের `.gitignore` ফাইলে এটি থাকা আবশ্যক:

```gitignore
# .gitignore
.env
.env.local
venv/
db.sqlite3
```

---

### ২. `.env.example` তৈরি করা (টিম ও ওপেন সোর্স প্যাটার্ন):
যেহেতু `.env` গিটহাবে যাবে না, তাই আপনার প্রজেক্টটি ডাউনলোড করা অন্য কোনো ডেভেলপার কীভাবে বুঝবে কোন কোন ভেরিয়েবল প্রয়োজন?

এর জন্য আসল পাসওয়ার্ড **বাদ দিয়ে** একটি ডামি ফাইল তৈরি করা হয়: **`.env.example`** (যা গিটহাবে কমিট করা হয়):

```bash
# .env.example (নমুনা ফাইল - কোনো আসল পাসওয়ার্ড থাকবে না)
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=database_name
DB_USER=database_user
DB_PASSWORD=database_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
```

যেকোনো নতুন ডেভেলপার প্রজেক্ট ক্লোন করে শুধু রান করবে:
```bash
cp .env.example .env
```
এরপর সে তার নিজের কম্পিউটারের তথ্য `.env`-এ বসিয়ে নেবে।

---

## ৬. প্রোডাকশন সার্ভারে Environment Variables কীভাবে সেট করে?

প্রোডাকশন সার্ভারে সাধারণত কোনো ফাইলে পাসওয়ার্ড না রেখে সার্ভারের নিজস্ব এনভায়রনমেন্টে সেট করা হয়:

### ক. লিনাক্স সার্ভার (Ubuntu / Nginx / Gunicorn):
সিস্টেম সার্ভিস ফাইলে (`/etc/systemd/system/gunicorn.service`):
```ini
[Service]
Environment="SECRET_KEY=super-secret-key-123"
Environment="DEBUG=False"
Environment="ALLOWED_HOSTS=example.com,www.example.com"
```

### খ. ক্লাউড প্ল্যাটফর্ম (Render, Railway, Heroku, DigitalOcean):
ওয়েবসাইট ড্যাশবোর্ডের **"Environment"** বা **"Config Vars"** সেকশনে গিয়ে `KEY` এবং `VALUE` আকারে ইনপুট দিতে হয়। সেখানে কোনো `.env` ফাইল আপলোড করার দরকার হয় না; প্ল্যাটফর্ম স্বয়ংক্রিয়ভাবে তা সার্ভারে ইনজেক্ট করে।

---

## ৭. ভুলবশত গিটহাবে পাসওয়ার্ড পুশ হয়ে গেলে কী করবেন? 🚨

যদি অসাবধানতাবশত `.env` গিটহাবে পুশ করে ফেলেন:
1. **তাৎক্ষণিক ব্যবস্থা:** অবিলম্বে ডেটাবেজ, জিমেইল অ্যাপ পাসওয়ার্ড বা স্ট্রাইপের এপিআই কি রিসেট বা পরিবর্তন করুন (Revoke Keys)। গিটহাব থেকে ডিলিট করলেও পুরোনো হিস্টোরিতে কি থেকে যায়।
2. **গিট ক্যাশ থেকে রিমুভ করা:**
   ```bash
   git rm --cached .env
   git commit -m "Remove .env from tracking"
   git push origin main
   ```
3. **গিট হিস্টোরি ক্লিন করতে:** `git-filter-repo` অথবা `BFG Repo-Cleaner` টুল ব্যবহার করে হিস্টোরি থেকে সম্পূর্ণ মুছে ফেলতে হয়।

---

## 🎯 আজকের Key Takeaways

1. **Environment Variables** কোড ও সিক্রেট কনফিগারেশন আলাদা রেখে অ্যাপ্লিকেশনের সর্বোচ্চ নিরাপত্তা নিশ্চিত করে (12-Factor App)।
2. কখনো আসল পাসওয়ার্ড বা সিক্রেট কি সরাসরি পাইথন ফাইলে হার্ডকোড করবেন না।
3. `.env` ফাইলে কোনো স্পেস রাখা যাবে না এবং এটি অবশ্যই `.gitignore`-এ যুক্ত রাখতে হবে।
4. টিমের অন্যদের সুবিধার্থে ডামি কি সহ একটি `.env.example` ফাইল তৈরি করে গিটহাবে রাখতে হয়।
5. `python-dotenv` দিয়ে সহজে `os.getenv()` এবং `django-environ` দিয়ে টাইপ-কাস্টিং সহ প্রফেশনাল কনফিগারেশন করা যায়।
6. লাইভ সার্ভারে অবশ্যই `DEBUG=False` হতে হবে এবং ডোমেইন নেম `ALLOWED_HOSTS`-এ অন্তর্ভুক্ত থাকতে হবে।

---

## ❓ অনুশীলনী প্রশ্ন

1. Environment Variables কী এবং এটি ব্যবহারের প্রধান সুবিধাগুলো কী কী?
2. Django-র `SECRET_KEY` সরাসরি গিটহাবে ফাঁস হলে একজন হ্যাকার কী কী ক্ষতি করতে পারে?
3. `.env` ফাইলে ভেরিয়েবল লেখার ফরম্যাট কেমন হওয়া উচিত?
4. `.gitignore` ফাইলে `.env` না রাখলে কী মারাত্মক ঝুঁকি তৈরি হয়?
5. `.env.example` ফাইল কী এবং এটি কেন তৈরি করা ইন্ডাস্ট্রি স্ট্যান্ডার্ড?
6. `os.getenv('DEBUG')` সরাসরি বসালে কেন সমস্যা হতে পারে এবং কীভাবে এটি সঠিকভাবে হ্যান্ডেল করতে হয়?
7. `django-environ` লাইব্রেরি ব্যবহারের দুটি বিশেষ সুবিধা কী কী?
8. প্রোডাকশন লাইভ সার্ভারে `DEBUG=False` করার সাথে সাথে `ALLOWED_HOSTS`-এ কী কনফিগারেশন করতে হয়?
9. ভুলবশত গিটহাবে কোনো সেনসিটিভ পাসওয়ার্ড পুশ হয়ে গেলে সর্বপ্রথম কী পদক্ষেপ নেওয়া উচিত?
10. ক্লাউড হোস্টিংয়ে (যেমন: Render বা Heroku) কীভাবে Environment Variables কনফিগার করা হয়?
