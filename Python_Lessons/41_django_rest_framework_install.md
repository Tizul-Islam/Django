# Django REST Framework (DRF) পরিচিতি ও ইনস্টলেশন 🚀🌐

এখন পর্যন্ত আমরা শিখেছি কীভাবে Django দিয়ে পূর্ণাঙ্গ ওয়েব অ্যাপ্লিকেশন তৈরি করা যায় যেখানে সার্ভার সরাসরি HTML টেমপ্লেট রেন্ডার করে।

কিন্তু আধুনিক ওয়েব ও মোবাইল প্রযুক্তিতে ফ্রন্টএন্ড (যেমন: **Next.js**, **React**, **Vue** বা **Flutter/React Native**) আলাদাভাবে চলে এবং ব্যাকএন্ডের সাথে ডেটা আদান-প্রদান করে **API (Application Programming Interface)** বা **JSON ডেটা**-র মাধ্যমে।

Django-কে একটি শক্তিশালী ও পূর্ণাঙ্গ RESTful API ব্যাকএন্ডে রূপান্তর করার জন্য বিশ্বব্যাপী সবচেয়ে জনপ্রিয় টুলকিট হলো **Django REST Framework (DRF)**।

---

## ১. সাধারণ Django বনাম Django REST Framework

```mermaid
graph TD
    subgraph ১. সাধারণ Django "Monolithic"
        A[Browser] --> B[Django View]
        B --> C[Django Templates HTML]
        C --> A
    end

    subgraph ২. Django REST Framework "API Architecture"
        D[Next.js / React / Mobile App] -->|HTTP Request| E[DRF API View]
        E -->|JSON Data| D
    end
```

| বৈশিষ্ট্য | সাধারণ Django | Django REST Framework (DRF) |
| :--- | :--- | :--- |
| **আউটপুট** | HTML ওয়েবপেজ রেন্ডার করে | পিওর **JSON** বা **XML** ডেটা রিটার্ন করে |
| **ক্লায়েন্ট** | শুধুমাত্র ওয়েব ব্রাউজার | ওয়েব, অ্যান্ড্রয়েড/আইওএস মোবাইল অ্যাপ, ডেস্কটপ অ্যাপ, স্মার্টওয়াচ |
| **ইউজার ইন্টারফেস** | Django Templates (HTML/CSS) | আলাদা আধুনিক ফ্রন্টএন্ড (Next.js, React, Tailwind) |
| **ডেটা প্রসেসিং** | Django Forms দিয়ে ভ্যালিডেশন | **Serializers** দিয়ে ভ্যালিডেশন ও ফরম্যাটিং |

---

## ২. কেন Django REST Framework বেছে নেবেন?

1. **The Browsable API (অসাধারণ ভিজ্যুয়াল ইন্টারফেস):** কোড লেখার পর কোনো Postman বা জটিল সফটওয়্যার ছাড়াই সরাসরি ওয়েব ব্রাউজারেই API টেস্ট করা, ডেটা দেখা ও POST রিকোয়েস্ট পাঠানোর চমৎকার বিল্ট-ইন UI থাকে।
2. **Serializers:** পাইথনের জটিল Model ও QuerySet ডেটাকে মুহূর্তেই JSON-এ কনভার্ট (Serialization) করা এবং আগত JSON ডেটাকে ভ্যালিডেট করে পাইথনে রূপান্তর (Deserialization) করার জন্য সবচেয়ে শক্তিশালী সিস্টেম।
3. **Authentication ও Permissions:** Session, Basic Auth, Token Authentication এবং আধুনিক **JWT (JSON Web Token)** সমর্থন করে।
4. **ViewSets ও Routers:** মাত্র কয়েক লাইন কোডে সম্পূর্ণ CRUD (Create, Read, Update, Delete) এপিআই এন্ডপয়েন্ট স্বয়ংক্রিয়ভাবে তৈরি হয়ে যায়।

---

## ৩. DRF ইনস্টলেশন প্রক্রিয়া (ধাপে ধাপে)

### ধাপ ১: লাইব্রেরি ইনস্টল করুন
আপনার প্রজেক্টের ভার্চুয়াল এনভায়রনমেন্ট সক্রিয় করে টার্মিনালে রান করুন:

```bash
pip install djangorestframework
```

*(ঐচ্ছিক কিন্তু প্রস্তাবিত: ব্রাউজেবল এপিআই-তে রিচ টেক্সট ফরম্যাটিংয়ের জন্য)*:
```bash
pip install markdown
```

---

### ধাপ ২: `settings.py`-এ `rest_framework` যুক্ত করুন

আপনার `config/settings.py`-এর `INSTALLED_APPS` তালিকায় `'rest_framework'` যোগ করুন:

```python
# config/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 🚀 Django REST Framework যুক্ত করা হলো:
    'rest_framework',

    # আপনার নিজস্ব অ্যাপসমূহ:
    'accounts',
]
```

---

### ধাপ ৩: Browsable API লগইন URL যুক্ত করুন (`urls.py`)

ব্রাউজারে এপিআই দেখার সময় সরাসরি ব্রাউজেবল এপিআই থেকেই যেন ইউজার লগইন ও লগআউট করা যায়, সেজন্য `config/urls.py`-এ DRF-এর নিজস্ব অথেনটিকেশন রুট যোগ করুন:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 🚀 DRF Browsable API Login & Logout
    path('api-auth/', include('rest_framework.urls')),
    path('', include('accounts.urls')),
]
```

---

## ৪. প্রথম REST API তৈরি (Hello World API) 🏁

চলুন একটি সহজ ফাংশন-ভিত্তিক API তৈরি করে পরীক্ষা করি।

### ধাপ ১: একটি সহজ API View লেখা (`views.py`)

```python
# accounts/views.py (অথবা api/views.py)
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello_api_view(request):
    """
    আমাদের প্রথম REST API এন্ডপয়েন্ট
    """
    data = {
        "status": "success",
        "message": "স্বাগতম! Django REST Framework সফলভাবে কাজ করছে।",
        "data": {
            "version": "1.0.0",
            "framework": "Django REST Framework 3.18+",
        }
    }
    return Response(data)
```

> 💡 **নোট:** সাধারণ ভিউতে আমরা `HttpResponse` বা `render()` ব্যবহার করি, কিন্তু DRF-এ আমরা সর্বদা **`Response()`** রিটার্ন করি। আর ফাংশনটিকে API হিসেবে চিহ্নিত করতে **`@api_view(['GET', 'POST'])`** ডেকোরেটর ব্যবহার করা হয়।

---

### ধাপ ২: URL কনফিগার করা (`urls.py`)

```python
# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # অন্যান্য URL...
    path('api/hello/', views.hello_api_view, name='hello_api'),
]
```

---

### ধাপ ৩: ব্রাউজারে টেস্ট করুন! 🌐

সার্ভার চালু করুন:
```bash
python manage.py runserver
```

এখন ব্রাউজারে যান: **http://127.0.0.1:8000/api/hello/**

দেখতে পাবেন Django-র বিখ্যাত **Browsable API Interface** ওপেন হয়েছে, যেখানে HTTP Status Code `200 OK` এবং সুন্দরভাবে ফরম্যাট করা JSON ডেটা দেখা যাচ্ছে!

---

## ৫. DRF গ্লোবাল সেটিংস (`settings.py`)

প্রজেক্টের সকল এপিআই-এর গ্লোবাল আচরণ (যেমন: ডিফল্ট পারমিশন, পেজিনেশন সাইজ) নিয়ন্ত্রণের জন্য `settings.py`-এ `REST_FRAMEWORK` কনফিগারেশন রাখা যায়:

```python
# config/settings.py

REST_FRAMEWORK = {
    # ১. ডিফল্ট পারমিশন (যেমন: লগইন না থাকলে শুধু রিড করতে পারবে)
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    # ২. ডিফল্ট অথেনটিকেশন মেথড
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],

    # ৩. ডিফল্ট পেজিনেশন (প্রতি পেজে ১০টি করে ডেটা পাঠাবে)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

---

## 🎯 আজকের Key Takeaways

1. **Django REST Framework (DRF)** হলো Django দিয়ে শক্তিশালী, মাপযোগ্য ও নিরাপদ Web API তৈরির ফ্রেমওয়ার্ক।
2. DRF-এর মূল লক্ষ্য হলো HTML-এর বদলে সুসংগঠিত **JSON ডেটা** আদান-প্রদান করা, যা Next.js বা মোবাইল অ্যাপস সহজেই পড়তে পারে।
3. `pip install djangorestframework` দিয়ে ইনস্টল করে `INSTALLED_APPS`-এ `'rest_framework'` যোগ করতে হয়।
4. DRF ভিউতে সাধারণ ডিকশনারি বা ডেটা রিটার্ন করতে `from rest_framework.response import Response` ব্যবহার করা হয়।
5. ফাংশন-ভিত্তিক API ভিউয়ের উপরে `@api_view(['GET', 'POST'])` ডেকোরেটর ব্যবহার করা বাধ্যতামূলক।
6. **Browsable API** পোস্টম্যান বা থার্ড-পার্টি টুলস ছাড়াই ব্রাউজারেই সরাসরি এপিআই টেস্ট ও ডিবাগ করার সুযোগ দেয়।

---

## ❓ অনুশীলনী প্রশ্ন

1. সাধারণ Django ওয়েব অ্যাপ্লিকেশন এবং Django REST Framework (DRF)-এর মধ্যে মূল পার্থক্য কী?
2. Next.js বা React-এর মতো আধুনিক ফ্রন্টএন্ড ফ্রেমওয়ার্কের সাথে Django ব্যাকএন্ড কানেক্ট করতে কেন DRF প্রয়োজন?
3. DRF-এর "Browsable API" কী এবং এটি ডেভেলপারদের কীভাবে সাহায্য করে?
4. `settings.py`-এর কোন তালিকায় `'rest_framework'` যুক্ত করতে হয়?
5. `urls.py`-এ `path('api-auth/', include('rest_framework.urls'))` যোগ করার সুবিধা কী?
6. DRF ভিউতে সাধারণ `HttpResponse` বা `render()`-এর পরিবর্তে কোন অবজেক্টটি রিটার্ন করা হয়?
7. ফাংশন-ভিত্তিক এপিআই ভিউতে `@api_view` ডেকোরেটরের ভূমিকা কী?
8. DRF-এ JSON ডেটা এবং পাইথন মডেল ডেটার রূপান্তর করতে কোন কম্পোনেন্ট ব্যবহার করা হয়?
9. `REST_FRAMEWORK` সেটিংসে `DEFAULT_PERMISSION_CLASSES`-এর কাজ কী?
10. `PAGE_SIZE = 10` সেট করলে এপিআই রেসপন্সে কী পরিবর্তন আসবে?
