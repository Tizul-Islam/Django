# Django REST Framework JWT Authentication (Simple JWT) 🪙🔐

আধুনিক ওয়েব ডেভেলপমেন্টে (যেমন: **Next.js**, **React**, **Vue**) এবং মোবাইল অ্যাপ্লিকেশনে (যেমন: **Flutter**, **React Native**) প্রমাণীকরণের (Authentication) বৈশ্বিক গোল্ড স্ট্যান্ডার্ড হলো **JWT (JSON Web Token)**।

Django-র ডিফল্ট সেশন অথেনটিকেশন ব্রাউজারের কুকির ওপর নির্ভরশীল হওয়ায় মোবাইল অ্যাপ বা আলাদা ডোমেইনের ফ্রন্টএন্ডে কাজ করা জটিল ও ত্রুটিপ্রবণ হয়। **Simple JWT** ব্যবহারের মাধ্যমে আমরা সম্পূর্ণ স্ট্যাটলেস (Stateless) এবং নিরাপদে ক্রস-প্ল্যাটফর্ম প্রমাণীকরণ নিশ্চিত করতে পারি।

---

## ১. Session Authentication বনাম JWT Authentication

```mermaid
graph TD
    subgraph ১. Session-based "Stateful"
        A[Client] -->|Login| B[Django Server]
        B -->|Database Query| C[(Session DB Table)]
        B -->|Set-Cookie: sessionid| A
        A -->|Cookie পাঠায়| B
    end

    subgraph ২. JWT "Stateless - কোনো DB কোয়েরি লাগে না"
        D[Next.js / Mobile App] -->|Login| E[Django Server]
        E -->|ক্রিপ্টোগ্রাফিক সাইন করে| F[Access + Refresh Token]
        F --> D
        D -->|Authorization: Bearer Token| E
        E -->|গোপন কী দিয়ে অফলাইনে ভেরিফাই| G[ইউজার অ্যাক্সেস পায়]
    end
```

| বৈশিষ্ট্য | Session Authentication | JWT (Simple JWT) |
| :--- | :--- | :--- |
| **স্টোরেজ** | সার্ভার ডেটাবেজে (`django_session`) জমা থাকে | সম্পূর্ণ স্ট্যাটলেস (ক্লায়েন্ট বা ব্রাউজারে টোকেন থাকে) |
| **স্কেলেবিলিটি** | ক্লাউডে মাল্টিপল সার্ভার হলে সেশন শেয়ার করা কঠিন | যেকোনো সার্ভারে একই Secret Key দিয়ে ভেরিফাই হয় |
| **মোবাইল ও API** | মোবাইল অ্যাপে কুকি ম্যানেজমেন্ট জটিল | মোবাইলে নেটিভভাবে `Authorization: Bearer` কাজ করে |
| **ডেটাবেজ লোড** | প্রতিটি রিকোয়েস্টে সেশন টেবিল থেকে ইউজার খুঁজতে হয় | কোনো DB কোয়েরি ছাড়া ক্রিপ্টোগ্রাফিক সিগনেচার চেক হয় |

---

## ২. JWT-এর অভ্যন্তরীণ গঠন

একটি JWT টোকেন দেখতে তিনটি অংশের সমষ্টি, যা ডট (`.`) দিয়ে বিভক্ত থাকে:
`header.payload.signature`

1. **Header (হেডার):** টোকেনের ধরন (`JWT`) এবং অ্যালগরিদম (`HS256`) ধারণ করে।
2. **Payload (পে-লোড):** ইউজারের তথ্য (যেমন: `user_id`, `username`, এক্সপায়ার ডেট `exp`) ধারণ করে।
3. **Signature (সিগনেচার):** সার্ভারের গোপন `SECRET_KEY` দিয়ে হ্যাশ করা হয়, যাতে কেউ পে-লোডের ডেটা পরিবর্তন করলে টোকেনটি স্বয়ংক্রিয়ভাবে বাতিল হয়ে যায়!

---

## ৩. Access Token বনাম Refresh Token আর্কিটেকচার

```mermaid
sequenceDiagram
    autonumber
    actor Client as ক্লায়েন্ট (Next.js / Mobile)
    participant Auth as Django SimpleJWT Server
    participant API as Protected API (/api/v1/tasks/)

    Note over Client, Auth: ১. লগইন পর্যায়
    Client->>Auth: POST /api/token/ (username + password)
    Auth-->>Client: Access Token (মেয়াদ: ১ ঘণ্টা) + Refresh Token (মেয়াদ: ৭ দিন)

    Note over Client, API: ২. সুরক্ষিত এপিআই কল
    Client->>API: GET /api/v1/tasks/ (Header: Bearer <Access Token>)
    API-->>Client: 200 OK (ডেটা প্রদর্শিত)

    Note over Client, Auth: ৩. Access Token-এর মেয়াদ শেষ হলে (Expired)
    Client->>API: GET /api/v1/tasks/ (Header: Expired Access Token)
    API-->>Client: 401 Unauthorized (Token is invalid or expired)

    Note over Client, Auth: ৪. রিফ্রেশ টোকেন দিয়ে নতুন টোকেন সংগ্রহ
    Client->>Auth: POST /api/token/refresh/ (body: {refresh: Refresh Token})
    Auth-->>Client: New Access Token (ইউজারকে আবার পাসওয়ার্ড দিতে হয় না!)
    Client->>API: GET /api/v1/tasks/ (Header: Bearer <New Access Token>)
    API-->>Client: 200 OK
```

* **Access Token (অল্প মেয়াদী):** API অ্যাক্সেস করার জন্য ব্যবহৃত হয় (যেমন: ৫ মিনিট থেকে ১ ঘণ্টা)। এটি চুরি হলেও অল্প সময় পর অকেজো হয়ে যায়।
* **Refresh Token (দীর্ঘ মেয়াদী):** নতুন Access Token ইস্যু করার জন্য ব্যবহৃত হয় (যেমন: ৭ দিন থেকে ৩০ দিন)।

---

## ৪. `djangorestframework-simplejwt` ইনস্টলেশন ও কনফিগারেশন

### ধাপ ১: লাইব্রেরি ইনস্টল করুন
```bash
pip install djangorestframework-simplejwt
```

---

### ধাপ ২: `settings.py`-এ কনফিগার করুন

```python
# config/settings.py
from datetime import timedelta

INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',  # 👈 টোকেন ব্লকলিস্ট বা লগআউট সাপোর্ট
    'accounts',
]

# ১. DRF ডিফল্ট অথেনটিকেশন হিসেবে Simple JWT সেট করা
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

# ২. Simple JWT ফাইন-টিউনিং কনফিগারেশন
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),   # ১ ঘণ্টা
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # ৭ দিন
    'ROTATE_REFRESH_TOKENS': True,                   # রিফ্রেশ করলে নতুন রিফ্রেশ টোকেনও ইস্যু হবে
    'BLACKLIST_AFTER_ROTATION': True,                # পুরোনো রিফ্রেশ টোকেনটি সাথে সাথে ব্লকলিস্ট হবে
    'UPDATE_LAST_LOGIN': True,                       # টোকেন নিলে ইউজারের last_login আপডেট হবে
    'AUTH_HEADER_TYPES': ('Bearer',),                # হেডারে 'Bearer <token>' যাবে
}
```

মাইগ্রেশন চালান:
```bash
python manage.py migrate
```

---

### ধাপ ৩: URL কনফিগার করা (`urls.py`)

Simple JWT-এর রেডিমেড ৩টি ভিউ রাউটারে যুক্ত করতে হয়:

```python
# accounts/urls.py (বা config/urls.py)
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # ১. ইউজারনেম ও পাসওয়ার্ড দিয়ে টোকেন সংগ্রহ (লগইন)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # ২. রিফ্রেশ টোকেন দিয়ে নতুন অ্যাক্সেস টোকেন নেওয়া
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ৩. টোকেন এখনো বৈধ কিনা তা যাচাই করা
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
```

---

## ৫. কাস্টম টোকেন ক্লেইমস (Custom Token Payload) 🎨

ডিফল্টভাবে Simple JWT টোকেনের ভেতর শুধু `user_id` রাখে। কিন্তু ফ্রন্টএন্ডের সুবিধার জন্য আপনি যদি টোকেনের পে-লোডের ভেতরেই ইউজারের `username`, `email` বা `role` পাঠিয়ে দিতে চান:

```python
# accounts/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 🚀 কাস্টম ক্লেইমস যোগ করা:
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        return token

# কাস্টম ভিউ:
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
```

এখন টোকেন ডিকোড করলেই ফ্রন্টএন্ড ইউজারের তথ্য পেয়ে যাবে, আলাদা করে `/api/me/` কল করতে হবে না!

---

## ৬. ফ্রন্টএন্ড বা ক্লায়েন্ট কীভাবে JWT ব্যবহার করবে?

### ১. টোকেন সংগ্রহ (Login):
* **POST** `http://127.0.0.1:8000/api/token/`
* **Body (JSON):**
  ```json
  {
      "username": "admin",
      "password": "adminpassword123"
  }
  ```
* **রেসপন্স:**
  ```json
  {
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIi...",
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCI..."
  }
  ```

---

### ২. সুরক্ষিত API রিকোয়েস্ট পাঠানো (Authorization Header):
যেকোনো সুরক্ষিত এন্ডপয়েন্টে (যেমন: `/api/v1/tasks/`) রিকোয়েস্ট পাঠাতে **HTTP Header**-এ টোকেন যুক্ত করতে হয়:

```http
GET /api/v1/tasks/ HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### ৩. টোকেন রিফ্রেশ করা:
* **POST** `http://127.0.0.1:8000/api/token/refresh/`
* **Body (JSON):**
  ```json
  {
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCI..."
  }
  ```
* **রেসপন্স:** নতুন `access` টোকেন পাওয়া যাবে।

---

## 🎯 আজকের Key Takeaways

1. **JWT** হলো স্ট্যাটলেস অথেনটিকেশন যা কোনো ডেটাবেজ সেশন ছাড়াই ক্রিপ্টোগ্রাফিক সিগনেচারের মাধ্যমে ইউজার প্রমাণীকরণ করে।
2. **Access Token** অল্প মেয়াদের জন্য API রিকোয়েস্টে `Authorization: Bearer <token>` হেডারে ব্যবহৃত হয়।
3. **Refresh Token** দীর্ঘ মেয়াদের জন্য ব্যবহৃত হয় যা দিয়ে পাসওয়ার্ড ছাড়া নতুন Access Token তৈরি করা যায়।
4. `ROTATE_REFRESH_TOKENS = True` এবং `BLACKLIST_AFTER_ROTATION = True` সেট করলে টোকেন হ্যাকিংয়ের ঝুঁকি বহুলাংশে কমে যায়।
5. `TokenObtainPairSerializer`-এর `get_token` মেথড ওভাররাইড করে টোকেনের পে-লোডে কাস্টম ডেটা ইনজেক্ট করা যায়।

---

## ❓ অনুশীলনী প্রশ্ন

1. সেশন-ভিত্তিক প্রমাণীকরণের চেয়ে মোবাইল অ্যাপ ও Next.js ফ্রন্টএন্ডে JWT কেন বেশি সুবিধাজনক?
2. একটি JWT টোকেনের তিনটি অংশের নাম কী এবং ডট দিয়ে কীভাবে বিভক্ত থাকে?
3. Access Token এবং Refresh Token-এর জীবনকাল (Lifetime)-এর মধ্যে আদর্শ পার্থক্য কী?
4. সার্ভারের `SECRET_KEY` পরিবর্তন করলে ইতিমধ্যে ইউজারদের দেওয়া অ্যাক্টিভ JWT টোকেনগুলোর কী হবে এবং কেন?
5. `Authorization: Bearer <token>` হেডারে 'Bearer' শব্দটির তাৎপর্য কী?
6. Refresh Token Rotation বলতে কী বোঝায় এবং এটি কেন নিরাপদ?
7. টোকেন পে-লোডে কাস্টম ফিল্ড (যেমন: ইমেইল বা রোল) যুক্ত করার পদ্ধতি কী?
8. JWT টোকেন স্টোর করার জন্য ব্রাউজারের `localStorage`-এর চেয়ে `HttpOnly Cookie` কেন বেশি নিরাপদ?
9. `/api/token/verify/` এন্ডপয়েন্টটি কোন কাজে ব্যবহৃত হয়?
10. একজন ইউজার সাইনআউট (Logout) করলে রিফ্রেশ টোকেনটিকে কীভাবে ব্লক করা হয়?
