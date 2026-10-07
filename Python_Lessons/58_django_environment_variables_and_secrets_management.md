# Lesson 58: Production Secrets ও Environment Variables Management 🔐🛡️

অ্যাপ্লিকেশনের আকার বৃদ্ধির সাথে সাথে পাসওয়ার্ড, এপিআই কি এবং সিক্রেটগুলো শুধুমাত্র একটি সাধারণ `.env` ফাইলে রাখার চেয়ে আরও কাঠামোগত এবং নিরাপদ উপায়ে পরিচালনা করা প্রয়োজন। বিশেষ করে প্রোডাকশন ক্লাউড এনভায়রনমেন্টে, ডকার কন্টেইনারে এবং সিআই/সিডি (CI/CD) পাইপলাইনে সংবেদনশীল ডেটা হ্যান্ডেল করার বিশেষ কলাকৌশল রয়েছে।

এই পাঠে আমরা শিখব:
1. **Config vs Secrets**-এর পার্থক্য
2. **`django-environ`** বনাম **`python-decouple`** দিয়ে টাইপ-সেফ ভেরিয়েবল পার্সিং
3. Django 4.1+ এর জিরো-ডাউনটাইম **`SECRET_KEY_FALLBACKS`** রোটেশন
4. প্রোডাকশনে লিনাক্স ও ডকার সিক্রেটস ম্যানেজমেন্ট
5. অসাবধানতাবশত লগ ফাইলে পাসওয়ার্ড ফাঁস রোধ (`@sensitive_variables`)
6. গিটহাবে সিক্রেট লিক প্রতিরোধ ও অডিটিং (`gitleaks`, `detect-secrets`)

---

## ১. Config বনাম Secrets: পার্থক্য কী?

| ক্যাটাগরি | কী কী অন্তর্ভুক্ত? | লিক হলে ঝুঁকি | স্টোরেজ কৌশল |
| :--- | :--- | :---: | :--- |
| **Config (কনফিগারেশন)** | `PORT`, `ALLOWED_HOSTS`, `PAGE_SIZE`, `LOG_LEVEL` | 🟡 কম (অ্যাপ্লিকেশনের আচরণ নির্ধারণ করে) | সাধারণ `.env` বা ডিপ্লয়মেন্ট ভেরিয়েবল |
| **Secrets (গোপন তথ্য)** | `SECRET_KEY`, `DB_PASSWORD`, Stripe/AWS Keys, JWT Secret | 🔴 মারাত্মক (সিস্টেম হ্যাক ও ডেটাবেজ লিক) | এনক্রিপ্টেড ভল্ট / সুরক্ষিত পরিবেশ |

---

## ২. টাইপ-সেফ ভেরিয়েবল পার্সিং: `django-environ`

সাধারণ `os.getenv()` সবকিছুকে স্ট্রিং হিসেবে লোড করে। যেমন: `os.getenv('DEBUG')` রিটার্ন করবে `"False"` (স্ট্রিং), যা পাইথনে ট্রু (`bool("False") == True`) হিসেবে কাজ করে! এটি প্রোডাকশনে মারাত্মক বিপদের কারণ হয়।

এজন্য ইন্ডাস্ট্রি স্ট্যান্ডার্ড সমাধান হলো **`django-environ`**:

```bash
pip install django-environ
```

### `config/settings.py`-তে বাস্তবায়ন:

```python
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ১. environ ইনিশিয়ালাইজ করা
env = environ.Env(
    # টাইপ এবং ডিফল্ট ভ্যালু কাস্টিং
    DEBUG=(bool, False),
    PORT=(int, 8000),
    ALLOWED_HOSTS=(list, ['127.0.0.1', 'localhost']),
)

# ২. .env ফাইল রিড করা (যদি থাকে)
environ.Env.read_env(BASE_DIR / '.env')

# ৩. নিরাপদভাবে ভেরিয়েবল ব্যবহার:
DEBUG = env('DEBUG')  # স্ট্রিং "False" থাকলে সঠিকভাবে boolean False বানাবে
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# ৪. ডেটাবেজ ও ক্যাশ এক লাইনে পার্সিং:
DATABASES = {
    'default': env.db('DATABASE_URL')  # postgres://user:pass@host:5432/dbname
}

CACHES = {
    'default': env.cache('REDIS_URL', 'redis://127.0.0.1:6379/1')
}
```

---

## ৩. জিরো-ডাউনটাইম SECRET_KEY রোটেশন (`SECRET_KEY_FALLBACKS`) 🔄

Django-র `SECRET_KEY` ব্যবহার করে সেশন কুকি, পাসওয়ার্ড রিসেট টোকেন এবং সাইনড মেসেজ ক্রিপ্টোগ্রাফিক্যালি হ্যাশ করা হয়। কোনো কারণে যদি আপনার সিক্রেট কি আপস (Compromise) হয়, তবে তা পরিবর্তন করতে হবে।

কিন্তু পুরোনো নিয়মে সরাসরি `SECRET_KEY` পরিবর্তন করলে সমস্ত অ্যাক্টিভ লগইন করা ব্যবহারকারী সাথে সাথে লগআউট হয়ে যেত!

Django 4.1+ সংস্করণে এসেছে **`SECRET_KEY_FALLBACKS`**:

```python
# settings.py
# নতুন সিক্রেট কি যা দিয়ে সব নতুন টোকেন ও সেশন সাইন হবে
SECRET_KEY = env('SECRET_KEY')

# পুরোনো সিক্রেট কিগুলোর তালিকা (রোটেশনের সময় পুরোনো সেশনগুলো ভ্যালিড রাখতে)
SECRET_KEY_FALLBACKS = env.list('SECRET_KEY_FALLBACKS', default=[])
```

`.env` ফাইল:
```env
# নতুন কি
SECRET_KEY=new-super-secret-key-2026-xyz

# পুরোনো কি (ব্যবহারকারীদের লগআউট হওয়া রোধ করতে সাময়িকভাবে রাখা)
SECRET_KEY_FALLBACKS=old-key-2025-abc,older-key-2024-def
```
> 💡 **কাজের ধরণ:** Django নতুন সেশন তৈরির সময় মূল `SECRET_KEY` ব্যবহার করবে। কিন্তু ব্যবহারকারীর কাছ থেকে পুরোনো কোনো কুকি এলে তা `SECRET_KEY_FALLBACKS`-এর সাথে মিলিয়ে যাচাই করে তাকে লগইন রাখবে! কয়েক সপ্তাহ পর পুরোনো কি মুছে ফেলা যায়।

---

## ৪. প্রোডাকশন সার্ভারে সিক্রেটস ফাইল সুরক্ষিত করা (Linux Permissions)

প্রোডাকশন লিনাক্স (Ubuntu/Debian) সার্ভারে `.env` ফাইল যাতে সার্ভারের অন্য কোনো প্রোগ্রাম বা আনঅথরাইজড ব্যবহারকারী রিড করতে না পারে, সেজন্য ফাইল পারমিশন লক করতে হয়:

```bash
# শুধুমাত্র ফাইল মালিক (যেমন www-data বা django ইউজার) পড়তে ও লিখতে পারবে
chmod 600 /home/ubuntu/myproject/.env

# মালিকানা নিশ্চিত করুন
chown ubuntu:www-data /home/ubuntu/myproject/.env
```

### Systemd সার্ভিস ফাইলে সিক্রেটস ইনজেকশন:
সার্ভার রিস্টার্টের সময় Gunicorn-এ পরিবেশ ভেরিয়েবল লোড করার আদর্শ উপায়:

```ini
# /etc/systemd/system/gunicorn.service
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/myproject
# সিস্টেমডি সরাসরি সুরক্ষিত এনভায়রনমেন্ট ফাইল পড়বে
EnvironmentFile=/home/ubuntu/myproject/.env
ExecStart=/home/ubuntu/myproject/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock config.wsgi:application
```

---

## ৫. ডকার কন্টেইনারে সিক্রেটস (Docker Compose ও Secrets)

ডকার ইমেজের ভেতর কখনই পাসওয়ার্ড `COPY` বা `ENV` আকারে হার্ডকোড করবেন না।

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    env_file:
      - .env.production  # হোস্টে থাকা ফাইল থেকে রানটাইমে ইনজেক্ট হবে
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
```

---

## ৬. লগ ফাইলে সংবেদনশীল তথ্য ফাঁস রোধ (`@sensitive_variables`) 🛡️

কোনো ভিউতে এরর হলে Django লগ ফাইলে লোকাল ভেরিয়েবলগুলো লিখে ফেলে। যদি ভিউতে ব্যবহারকারীর পাসওয়ার্ড বা ক্রেডিট কার্ডের নম্বর থাকে, তা লগে উন্মুক্ত হয়ে যেতে পারে।

Django-র বিল্ট-ইন সিকিউরিটি ডেকোরেটর এটি ঠেকায়:

```python
# accounts/views.py
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
from django.shortcuts import render

# ১. POST প্যারামিটার থেকে পাসওয়ার্ড লগে প্রদর্শন বন্ধ করা
@sensitive_post_parameters('password', 'old_password')
# ২. ফাংশনের ভেতরের ভেরিয়েবলগুলো এরর রিপোর্টে ফিল্টার করা
@sensitive_variables('auth_token', 'user_pin')
def process_user_credentials(request):
    auth_token = request.headers.get('Authorization')
    user_pin = request.POST.get('pin')
    
    # এখানে কোনো ক্র্যাশ বা এরর হলেও 
    # লগে auth_token ও user_pin এর মান দেখাবে '********************'
    
    return render(request, 'success.html')
```

---

## ৭. ক্লাউড সিক্রেট ম্যানেজার (AWS / Vault)

বড় এন্টারপ্রাইজ সিস্টেমে কোনো ফাইল সার্ভারেও রাখা হয় না। তখন সেন্ট্রালাইজড ক্লাউড সিক্রেট ম্যানেজার ব্যবহার করা হয়:

```mermaid
flowchart LR
    DjangoApp[Django Startup] -->|API Request with IAM Role| AWS[AWS Secrets Manager / HashiCorp Vault]
    AWS -->|Encrypted JSON Secrets| DjangoApp
    DjangoApp -->|Memory-তে ভেরিয়েবল লোড করে| Execution[প্রোডাকশন এক্সিকিউশন]
```

---

## ৮. গিটহাবে ভুলবশত সিক্রেট লিক হলে কী করবেন? 🚨

যদি কোনো কারণে পাসওয়ার্ড বা `SECRET_KEY` গিটহাবে পুশ হয়ে যায়:

1. **তাৎক্ষণিক ইনভ্যালিডেশন (Invalidate Immediately):** শুধু কোড থেকে লাইনটি মুছে নতুন কমিট করলে হবে না; গিট হিস্টোরিতে কি-টি থেকে যায়। সাথে সাথে ডেটাবেজের পাসওয়ার্ড বা এপিআই কি প্রোভাইডারের প্যানেল থেকে বাতিল/রিসেট করুন।
2. **গিট হিস্টোরি থেকে পার্মানেন্ট মুছে ফেলা:**
   ```bash
   pip install git-filter-repo
   git filter-repo --invert-paths --path .env
   git push origin --force --all
   ```
3. **লোকাল প্রি-কমিট হুক (`gitleaks`):** কমিট করার পূর্বেই সিক্রেট ডিটেক্ট করার জন্য টুল:
   ```bash
   # গিটলীক্স দিয়ে স্ক্যান করা
   gitleaks detect --source . -v
   ```

---

## প্রোডাকশন চেকলিস্ট 📋

1. ✅ `.gitignore` ফাইলে `.env`, `.env.*`, `*.pem`, `*.key` অন্তর্ভুক্ত আছে।
2. ✅ কোডে কোনো জায়গায় হার্ডকোডেড ক্রেডেনশিয়াল নেই, সবকিছু `django-environ` দিয়ে টাইপ-কাস্ট করা।
3. ✅ প্রোডাকশন লিনাক্স সার্ভারে `.env`-এর পারমিশন `chmod 600` করা।
4. ✅ পাসওয়ার্ড ও কার্ড ইনপুট নেওয়ার ভিউতে `@sensitive_post_parameters` ব্যবহৃত হয়েছে।
5. ✅ `SECRET_KEY_FALLBACKS` কনফিগার করে জিরো-ডাউনটাইম কি রোটেশনের সুযোগ রাখা হয়েছে।
