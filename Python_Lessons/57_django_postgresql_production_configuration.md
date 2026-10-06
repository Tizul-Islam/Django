# Lesson 57: Django-তে PostgreSQL Production Configuration 🐘⚙️

লোকাল ডেভেলপমেন্টে ডিফল্ট `sqlite3` ব্যবহার করা সহজ হলেও লাইভ প্রোডাকশনে এটি ব্যবহার করা চরম ঝুঁকিপূর্ণ। কারণ SQLite একটি ফাইল-ভিত্তিক ডেটাবেজ যা কোনো ডেটা লেখার (Write) সময় পুরো ফাইলটি লক করে ফেলে। ফলে একাধিক ব্যবহারকারী একসাথে রিকোয়েস্ট পাঠালে `database is locked` এরর তৈরি হয়।

প্রোডাকশনে Django-র জন্য বিশ্বজুড়ে সবচেয়ে জনপ্রিয় ও নির্ভরযোগ্য ডেটাবেজ হলো **PostgreSQL**। এটি ওপেন সোর্স, উচ্চ কনকারেন্সি সম্পন্ন, ACID কমপ্লায়েন্ট এবং এতে নেটিভ `JSONField`, ফুল-টেক্সট সার্চ ও উন্নত ইনডেক্সিং সাপোর্ট রয়েছে।

---

## ১. আর্কিটেকচার: প্রোডাকশন ডেটাবেজ রিকোয়েস্ট ফ্লো

```mermaid
flowchart LR
    Browser[ক্লায়েন্ট / ব্রাউজার] --> Nginx[Nginx Reverse Proxy]
    Nginx --> Gunicorn[Gunicorn / WSGI Workers]
    
    subgraph DjangoApp [Django Backend]
        CONN[CONN_MAX_AGE\nPersistent Connection]
    end
    
    Gunicorn --> CONN
    
    subgraph DatabaseLayer [PostgreSQL Production]
        PgBouncer[PgBouncer\nConnection Pooler]
        Postgres[(PostgreSQL Engine\nMaster / Replica)]
    end
    
    CONN -->|উচ্চ ট্রাফিক হলে| PgBouncer
    PgBouncer --> Postgres
    CONN -.->|সাধারণ ট্রাফিক হলে সরাসরি| Postgres
```

---

## ২. প্রয়োজনীয় প্যাকেজ ইনস্টলেশন

PostgreSQL-এর সাথে Django-র যোগাযোগের জন্য পাইথন ড্রাইভার এবং এনভায়রনমেন্ট ভেরিয়েবল হ্যান্ডলার প্রয়োজন:

```bash
# ১. আধুনিক PostgreSQL ৩ ড্রাইভার (Django 4.2+ এর জন্য সেরা)
pip install "psycopg[binary]"

# অথবা ট্রেডিশনাল ড্রাইভার:
# pip install psycopg2-binary

# ২. ১২-ফ্যাক্টর কনফিগ ও DATABASE_URL পার্সিং লাইব্রেরি
pip install dj-database-url python-dotenv
```

---

## ৩. `settings.py`-তে প্রোডাকশন কনফিগারেশন

পেশাদার প্রোডাকশন অ্যাপ্লিকেশনে ডেটাবেজের ক্রেডেনশিয়ালস (ইউজারনেম, পাসওয়ার্ড) কখনোই কোডে হার্ডকোড করা যাবে না। এগুলো `.env` ফাইল থেকে লোড করতে হয়।

### ক. `.env` ফাইলে ডেটাবেজ কনফিগ:
```env
# .env ফাইল
DB_NAME=my_production_db
DB_USER=django_user
DB_PASSWORD=SuperSecurePassword123!
DB_HOST=127.0.0.1
DB_PORT=5432

# অথবা সম্পূর্ণ কানেকশন স্ট্রিং (Docker / AWS RDS / Heroku স্টাইল):
DATABASE_URL=postgres://django_user:SuperSecurePassword123!@127.0.0.1:5432/my_production_db
```

### খ. `config/settings.py` ফাইলে প্রোডাকশন ডিকশনারি:

```python
import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ১. DATABASE_URL থাকলে তা থেকে অটোমেটিক কনফিগ নেবে, না থাকলে ম্যানুয়াল সেটিংস
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,       # ১০ মিনিট (৬০০ সেকেন্ড) কানেকশন পুনঃব্যবহার করবে
        conn_health_checks=True # Django 4.1+: কানেকশন ড্রপ হয়েছে কিনা চেক করবে
    ) if os.getenv('DATABASE_URL') else {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'django_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        
        # ২. Persistent Connection (কানেকশন পুলিং)
        # ডিফল্ট 0 মানে প্রতি রিকোয়েস্টে নতুন কানেকশন খোলে ও বন্ধ করে (ধীরগতির)।
        # মান ৬০০ দিলে একটি কানেকশন ১০ মিনিট সচল থাকবে।
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,

        # ৩. অতিরিক্ত সিকিউরিটি ও টাইমআউট অপশনস
        'OPTIONS': {
            # SSL সংযোগ বাধ্যতামূলক করা (AWS RDS বা রিমোট ডেটাবেজের জন্য)
            'sslmode': 'require' if not DEBUG else 'prefer',
            
            # কুয়েরি টাইমআউট (কোনো কোয়েরি ৫ সেকেন্ডের বেশি ঝুললে কিল করবে)
            'options': '-c statement_timeout=5000ms -c search_path=public',
            'connect_timeout': 5,
        }
    }
}
```

---

## ৪. `CONN_MAX_AGE` এবং `CONN_HEALTH_CHECKS` কী এবং কেন জরুরি?

ডিফল্টভাবে Django প্রতিবার রিকোয়েস্ট আসার পর নতুন একটি ডেটাবেজ কানেকশন খোলে এবং রিকোয়েস্ট শেষে তা বন্ধ করে দেয়। একটি PostgreSQL কানেকশন তৈরি করতে TCP Handshake এবং SSL ভ্যালিডেশনে **২০-৫০ মিলি-সেকেন্ড** অপচয় হয়।

- **`CONN_MAX_AGE = 600`**: এটি চালু করলে Django সেই কানেকশনটি বন্ধ না করে ৬০০ সেকেন্ড (১০ মিনিট) মেমরিতে বাঁচিয়ে রাখে এবং পরবর্তী রিকোয়েস্টগুলোতে পুনঃব্যবহার (Reuse) করে। ফলে রেসপন্স টাইম নিমেষেই ৩০-৪০% ফাস্ট হয়ে যায়!
- **`CONN_HEALTH_CHECKS = True`**: অনেক সময় ডেটাবেজ রিস্টার্ট বা নেটওয়ার্ক গ্লিচের কারণে দীর্ঘস্থায়ী কানেকশন ডেড হয়ে যেতে পারে। এই অপশনটি নিশ্চিত করে যে Django পুরোনো কানেকশন ব্যবহারের আগে ছোট্ট একটি পিং দিয়ে দেখে নেয় যে কানেকশনটি এখনো জীবিত আছে কি না।

---

## ৫. এক্সটারনাল কানেকশন পুলার (PgBouncer) ও তার সেটিংস

যদি আপনার ওয়েবসাইটে প্রচুর ট্রাফিক থাকে এবং আপনি Gunicorn দিয়ে বহু কর্মী (Worker) চালান, তবে শত শত কানেকশন সরাসরি PostgreSQL-এ গিয়ে ডেটাবেজের RAM শেষ করে ফেলতে পারে। 

এজন্য প্রোডাকশনে **PgBouncer** ব্যবহার করা হয়। এটি সামনে থেকে হাজার হাজার ক্লায়েন্ট কানেকশন রিসিভ করে এবং ডেটাবেজে মাত্র ২০-৩০টি শক্তিশালী কানেকশনের মাধ্যমে সমস্ত কোয়েরি পরিবেশন করে।

```python
# PgBouncer (Transaction Pooling) ব্যবহার করলে settings.py-তে এই অপশন আবশ্যক:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # ... অন্যান্য সেটিংস ...
        'DISABLE_SERVER_SIDE_CURSORS': True,  # PgBouncer এর সাথে ট্রানজেকশন পুলে ক্র্যাশ রোধ করে
    }
}
```

---

## ৬. সার্ভার লেভেলে PostgreSQL টিউনিং (`postgresql.conf`)

ডিফল্ট PostgreSQL কনফিগারেশন খুব দুর্বল হার্ডওয়্যারের (৫১২MB RAM) জন্য তৈরি থাকে। আধুনিক প্রোডাকশন সার্ভারে (যেমন ৪ কোর CPU, ৮ GB RAM) পারফরম্যান্স বহুগুণ বাড়াতে `postgresql.conf` ফাইলে নিচের প্যারামিটারগুলো অপ্টিমাইজ করুন:

| প্যারামিটার | ডিফল্ট মান | প্রোডাকশন সুপারিশ (8GB RAM) | ব্যাখ্যা |
| :--- | :---: | :---: | :--- |
| **`shared_buffers`** | 128MB | `2GB` (RAM-এর ২৫%) | ডেটা ক্যাশিংয়ের জন্য ডেডিকেটেড মেমরি |
| **`effective_cache_size`** | 4GB | `6GB` (RAM-এর ৭৫%) | OS ক্যাশ ও ডেটাবেজ ক্যাশের সম্মিলিত অনুমান |
| **`work_mem`** | 4MB | `32MB` | প্রতি সর্ট বা জটিল কুয়েরির জন্য মেমরি |
| **`maintenance_work_mem`**| 64MB | `512MB` | ইনডেক্সিং এবং ভ্যাকুয়াম (VACUUM) স্পিড |
| **`max_connections`** | 100 | `100 - 200` | সরাসরি কানেকশন সীমা (বেশি লাগলে PgBouncer ব্যবহার্য) |

> 🛠️ **টুল সুপারিশ:** আপনার সার্ভারের হার্ডওয়্যারের স্পেক অনুযায়ী পারফেক্ট কনফিগারেশন পেতে [PGTune](https://pgtune.leopard.in.ua/) টুলটি ব্যবহার করতে পারেন।

---

## ৭. ডেটাবেজ মাইগ্রেশন ও ব্যাকআপ স্ট্র্যাটেজি

### ক. জিরো-ডাউনটাইম ডিপ্লয়মেন্ট মাইগ্রেশন:
প্রোডাকশনে কোড পুশ করার সময় কখনই অ্যাপ্লিকেশন রান অবস্থায় মাইগ্রেশন চালাবেন না। ডিপ্লয়মেন্ট স্ক্রিপ্টে এই ক্রম অনুসরণ করুন:
```bash
# ১. ডিপ্লয়মেন্টের পূর্বে মাইগ্রেশন চালানো
python manage.py migrate --noinput

# ২. তারপর অ্যাপ্লিকেশন সার্ভার রিস্টার্ট করা
sudo systemctl restart gunicorn
```

### খ. অটোমেটেড ব্যাকআপ (Automated Backup Script):
প্রতিদিন স্বয়ংক্রিয়ভাবে ডেটাবেজ ব্যাকআপ নেওয়ার জন্য একটি ক্রন জব (Cron Job) সেট করুন:
```bash
# প্রতিদিন রাত ২টায় ব্যাকআপ নেবে
0 2 * * * pg_dump -U django_user -h 127.0.0.1 my_production_db | gzip > /backups/db_$(date +\%F).sql.gz
```

---

## প্রোডাকশন চেকলিস্ট 📋

1. ✅ **`DEBUG = False`** এবং সমস্ত ডেটাবেজ ক্রেডেনশিয়াল `.env` থেকে আসছে।
2. ✅ **`psycopg[binary]`** অথবা **`psycopg`** ড্রাইভার সঠিকভাবে ইনস্টল হয়েছে।
3. ✅ **`CONN_MAX_AGE = 600`** এবং **`CONN_HEALTH_CHECKS = True`** সক্রিয় করা হয়েছে।
4. ✅ রিমোট বা ক্লাউড ডেটাবেজে (AWS RDS / DigitalOcean) **`sslmode: 'require'`** নিশ্চিত করা হয়েছে।
5. ✅ কোয়েরি আটকে যাওয়া রোধ করতে **`statement_timeout`** (যেমন ৫ সেকেন্ড) সেট করা হয়েছে।
6. ✅ নিয়মিত ডেটাবেজ ব্যাকআপ (`pg_dump` বা ক্লাউড অটোমেটেড স্ন্যাপশট) চালু আছে।
