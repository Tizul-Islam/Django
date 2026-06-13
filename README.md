# 🚀 Django & DRF Enterprise Application

[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.1-092E20.svg?logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.18-A30000.svg)](https://www.django-rest-framework.org)
[![JWT](https://img.shields.io/badge/Auth-SimpleJWT-black.svg)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

একটি আধুনিক, নিরাপদ এবং স্কেলেবল Django ও Django REST Framework (DRF) ওয়েব অ্যাপ্লিকেশন। এতে রয়েছে সম্পূর্ণ ইউজার অথেনটিকেশন, টাস্ক ম্যানেজমেন্ট REST APIs, JWT সিকিউরিটি এবং একটি পূর্ণাঙ্গ ৬৭-পাঠের পাইথন ও জ্যাঙ্গো মাস্টারক্লাস সিলেবাস।

---

## ✨ Features

- 🔐 **Dual Authentication System:**
  - **Session-Based:** ব্রাউজারের জন্য নিরাপদ সেশন অথেনটিকেশন (Login, Register, Password Change, Password Reset Flow)।
  - **Token-Based:** মোবাইল ও সিঙ্গেল পেজ অ্যাপ্লিকেশনের (React/Next.js) জন্য `SimpleJWT` (Access, Refresh & Blacklist টোকেন)।
- ⚡ **RESTful APIs:**
  - `DefaultRouter` ও `ModelViewSet` সমন্বিত টাস্ক ম্যানেজমেন্ট CRUD API (`/api/v1/tasks/`)।
  - ফিল্টারিং, সার্চিং এবং সর্টিং সুবিধা (`django-filter` ও `SearchFilter`)।
- 🛡️ **Security Hardened:**
  - CSRF, XSS, SQL Injection প্রতিরোধ।
  - Secure Cookies, Password Validators ও ডায়নামিক `ALLOWED_HOSTS`।
- 🚀 **Performance Optimized:**
  - `select_related()` ও `prefetch_related()` দিয়ে N+1 কোয়েরি অপ্টিমাইজেশন।
  - ক্যাশিং আর্কিটেকচার এবং প্রোডাকশন-রেডি ডেটাবেজ কনফিগারেশন।
- 🧪 **Automated Testing:**
  - `TestCase` এবং `APITestCase` দিয়ে পূর্ণাঙ্গ ইউনিট টেস্ট ও API ইন্টিগ্রেশন টেস্ট।
- 📚 **Comprehensive Learning Curriculum:**
  - [Python_Lessons/](Python_Lessons/) ফোল্ডারে পাইথনের বেসিক থেকে শুরু করে ডকার, সিআই/সিডি এবং ক্লাউড ডিপ্লয়মেন্ট পর্যন্ত ৬৭টি বিস্তারিত পাঠ।

---

## 🛠️ Tech Stack

- **Backend Framework:** Django 6.1.2
- **API Framework:** Django REST Framework 3.18.3
- **Authentication:** Django Auth + `djangorestframework-simplejwt`
- **Database:** SQLite (Development) / PostgreSQL (Production ready)
- **Frontend / Templates:** Django Templates + Bootstrap 5 + Bootstrap Icons
- **Testing:** Django Test Runner + `APITestCase`

---

## 🚀 Getting Started (Local Setup)

### ১. ক্লোন ও প্রজেক্ট ডিরেক্টরিতে প্রবেশ:
```bash
git clone https://github.com/Tizul-Islam/Django.git
cd Django
```

### ২. ভার্চুয়াল এনভায়রনমেন্ট তৈরি ও সক্রিয়করণ:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### ৩. ডিপেন্ডেন্সি ইনস্টল করুন:
```bash
pip install -r requirements.txt
```

### ৪. মাইগ্রেশন রান করুন:
```bash
python manage.py migrate
```

### ৫. সুপারইউজার (Admin) তৈরি করুন:
```bash
python manage.py createsuperuser
```

### ৬. ডেভেলপমেন্ট সার্ভার চালু করুন:
```bash
python manage.py runserver
```

এখন ব্রাউজারে প্রবেশ করুন:
- 🌐 **হোমপেজ / ড্যাশবোর্ড:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 🔐 **অ্যাডমিন প্যানেল:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- 📡 **API রুট:** [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)

---

## 📡 API Endpoints Overview

| Method | Endpoint | বিবরণ | Authentication |
| :---: | :--- | :--- | :---: |
| **POST** | `/api/token/` | JWT Access ও Refresh টোকেন গ্রহণ | পাবলিক |
| **POST** | `/api/token/refresh/` | রিফ্রেশ টোকেন দিয়ে নতুন Access টোকেন নেওয়া | পাবলিক |
| **GET** | `/api/v1/tasks/` | ব্যবহারকারীর সমস্ত টাস্কের লিস্ট | Bearer Token / Session |
| **POST** | `/api/v1/tasks/` | নতুন টাস্ক তৈরি করা | Bearer Token / Session |
| **GET** | `/api/v1/tasks/{id}/` | নির্দিষ্ট টাস্কের বিস্তারিত দেখা | Bearer Token / Session |
| **PUT/PATCH** | `/api/v1/tasks/{id}/` | টাস্ক আপডেট বা কমপ্লিট মার্ক করা | Bearer Token / Session |
| **DELETE** | `/api/v1/tasks/{id}/` | টাস্ক ডিলিট করা | Bearer Token / Session |
| **GET** | `/api/v1/task-stats/` | টাস্কের সারাংশ ও পরিসংখ্যান API | Bearer Token / Session |

---

## 🧪 Running Automated Tests

প্রজেক্টের সমস্ত ভিউ, অথেনটিকেশন ফ্লো এবং API ইন্টিগ্রেশন টেস্ট রান করতে:

```bash
# টেস্ট চালানো
python manage.py test

# শুধুমাত্র accounts অ্যাপের টেস্ট চালানো
python manage.py test accounts
```

---

## 📚 Complete Learning Curriculum

এই রিপোজিটরির [Python_Lessons/](Python_Lessons/) ফোল্ডারে রয়েছে ৬৭টি সুবিন্যস্ত গাইড:

- **01 - 15:** পাইথন ফান্ডামেন্টালস (Variables, Loops, Functions, OOP, Exception Handling)
- **16 - 39:** Django কোর (Views, Templates, Models, ORM, Forms, Auth, Middleware, Signals)
- **40 - 49:** Django REST Framework (Serializers, ViewSets, Routers, JWT, Filters)
- **50 - 56:** অ্যাডভান্সড আর্কিটেকচার (Messages, Logging, Caching, Query Optimization, Security, Testing)
- **57 - 67:** প্রোডাকশন ইঞ্জিনিয়ারিং (PostgreSQL, Secrets, HTTPS, WhiteNoise, Docker, CI/CD, Rollback, API Docs)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
