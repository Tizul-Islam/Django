# Lesson 64: Production Logging ও Real-time Error Monitoring 📜🚨

একটি লাইভ প্রোডাকশন অ্যাপ্লিকেশনে ব্যবহারকারী কোনো ক্র্যাশের সম্মুখীন হলে ডেভেলপারকে নিজে থেকে সেই তথ্য জানতে হয়—কখনোই ব্যবহারকারীর অভিযোগের ওপর নির্ভর করা যায় না। 

সাধারণ টেক্সট ফাইল ভিত্তিক লগিং লোকাল কম্পিউটারের জন্য ভালো হলেও ক্লাউড বা ডকার এনভায়রনমেন্টে তা হারিয়ে যায়। আধুনিক ব্যাকএন্ড আর্কিটেকচারে প্রয়োজন **Structured JSON Logging**, **সেন্ট্রাল লগিং**, এবং **Sentry**-এর মতো রিয়েল-টাইম এরর মনিটরিং টুলস।

এই গাইডে আমরা শিখব:
1. সাধারণ লগের সীমাবদ্ধতা ও **Structured JSON Logging**-এর গুরুত্ব
2. রিকোয়েস্ট ট্র্যাকিংয়ের জন্য **Request-ID Middleware** তৈরি
3. **Sentry** দিয়ে রিয়েল-টাইম ক্র্যাশ ট্র্যাকিং ও পারফরম্যান্স মনিটরিং (APM)
4. ডেটাবেজ ও ক্যাশ ভ্যালিডেশন সহ প্রোডাকশন **Health Check Endpoint** তৈরি
5. অ্যালার্ট ফ্যাটিগ (Alert Fatigue) রোধ করার সেরা কৌশল

---

## ১. প্রোডাকশন এরর মনিটরিং আর্কিটেকচার

```mermaid
flowchart TD
    User[ব্যবহারকারী] -->|রিকোয়েস্ট ক্র্যাশ করল (500 Error)| Django[Django Backend]
    
    subgraph MonitoringStack [প্রোডাকশন মনিটরিং স্ট্যাক]
        Django -->|১. পূর্ণাঙ্গ Stacktrace ও Breadcrumbs পাঠায়| Sentry[Sentry Dashboard]
        Django -->|২. Structured JSON Log স্ট্রিম করে| Loki[Grafana Loki / Datadog]
        Sentry -->|৩. তাৎক্ষণিক নোটিফিকেশন| Slack[Slack / Discord / Email]
    end
    
    subgraph UptimeMonitoring [আপটাইম ও হেলথ চেক]
        UptimeRobot[UptimeRobot / BetterStack] -->|প্রতি ১ মিনিটে পিং পাঠায়| HealthCheck[/health/ Endpoint]
        HealthCheck -->|DB & Redis সচল আছে কি?| Django
    end
```

---

## ২. Structured JSON Logging (মেশিন-রিডেবল লগিং) 🧩

প্রোডাকশন সার্ভারে লক্ষ লক্ষ লগ লাইনের ভেতর থেকে সার্চ করতে হলে লগগুলো JSON ফরম্যাটে থাকা আবশ্যক:

```bash
pip install python-json-logger
```

[config/settings.py](file:///d:/Next%20Level%202/next.js/Django/config/settings.py)-এ কনফিগারেশন:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s %(user_id)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

### আউটপুট (JSON ফরম্যাটে):
```json
{
  "asctime": "2026-06-01 11:30:15",
  "levelname": "ERROR",
  "name": "accounts.views",
  "message": "Payment gateway timeout occurred",
  "request_id": "8f3b92-4c2a",
  "user_id": 142
}
```
> 💡 **সুবিধা:** Datadog বা Grafana-তে আপনি মুহূর্তের মধ্যে ফিল্টার করতে পারবেন: `user_id == 142` এবং `levelname == "ERROR"`।

---

## ৩. Request-ID ট্র্যাকিং Middleware (Distributed Tracing) 🔍

একটি ব্যবহারকারী যখন কোনো বাটন চাপেন, তখন তার সেই নির্দিষ্ট রিকোয়েস্টের সাথে একটি ইউনিক `X-Request-ID` জুড়ে দিলে পুরো সিস্টেমে ঐ রিকোয়েস্টের সমস্ত লগ সহজে ফিল্টার করা যায়:

```python
# accounts/middleware.py
import uuid
import threading

_request_locals = threading.local()

def get_current_request_id():
    return getattr(_request_locals, 'request_id', 'unknown')

class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # হেডার থেকে এক্সিস্টিং আইডি নিন অথবা নতুন UUID তৈরি করুন
        request_id = request.headers.get('X-Request-ID', str(uuid.uuid4())[:8])
        request.request_id = request_id
        _request_locals.request_id = request_id

        response = self.get_response(request)
        
        # রেসপন্স হেডারেও আইডি ফেরত দিন (ডিবাগিংয়ের জন্য)
        response['X-Request-ID'] = request_id
        return response
```

---

## ৪. ইন্ডাস্ট্রি গোল্ড স্ট্যান্ডার্ড: Sentry রিয়েল-টাইম মনিটরিং 🛡️

**Sentry** আপনাকে কোনো ব্যবহারকারী এরর দেখার সাথে সাথে স্ল্যাক বা ইমেইলে অ্যালার্ট পাঠায়। এর সবচেয়ে জাদুকরী সুবিধা হলো: এটি হুবহু কোন লাইনে ক্র্যাশ করেছে, কোন লোকাল ভেরিয়েবলে কী মান ছিল এবং ক্র্যাশ করার আগে ইউজার কোন কোন বাটনে ক্লিক করেছিল (Breadcrumbs)—সবকিছু রেকর্ড করে।

### ধাপ ১: লাইব্রেরি ইনস্টল করুন
```bash
pip install "sentry-sdk[django]"
```

### ধাপ ২: `config/settings.py`-তে Sentry ইনিশিয়ালাইজেশন:

```python
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_DSN = os.getenv('SENTRY_DSN')

if SENTRY_DSN and not DEBUG:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment=os.getenv('ENVIRONMENT', 'production'),
        
        # APM (Application Performance Monitoring) স্যাম্পল রেট
        # ১.০ মানে ১০০% ট্রানজেকশনের পারফরম্যান্স ট্র্যাক করবে (বড় সাইটে ০.১ বা ০.২ দেওয়া ভালো)
        traces_sample_rate=0.2,
        
        # সংবেদনশীল পাসওয়ার্ড/কার্ড ডেটা ফিল্টার করা
        send_default_pii=False,
    )
```

### কোডে ম্যানুয়ালি এক্সেপশন পাঠানো:
```python
import sentry_sdk

try:
    process_payment()
except Exception as e:
    # ব্যাকগ্রাউন্ডে হ্যান্ডেল করলেও Sentry ড্যাশবোর্ডে পাঠাতে:
    sentry_sdk.capture_exception(e)
```

---

## ৫. প্রোডাকশন Health Check Endpoint তৈরি (/health/) 🩺

লোড ব্যালেন্সার (AWS ALB, Kubernetes) এবং আপটাইম মনিটর (UptimeRobot, BetterStack) প্রতি ৩০-৬০ সেকেন্ড পর পর চেক করে আপনার সাইট জীবিত আছে কিনা।

শুধুমাত্র HTTP 200 রিটার্ন করাই যথেষ্ট নয়; ডেটাবেজ ও ক্যাশ সচল আছে কি না তাও যাচাই করতে হয়:

```python
# accounts/views.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import time

def health_check_view(request):
    health_status = {
        'status': 'healthy',
        'timestamp': time.time(),
        'services': {}
    }
    status_code = 200

    # ১. ডেটাবেজ কানেকশন চেক
    try:
        connection.ensure_connection()
        health_status['services']['database'] = 'connected'
    except Exception as e:
        health_status['services']['database'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
        status_code = 503

    # ২. Redis / Cache চেক
    try:
        cache.set('healthz_ping', 'ok', timeout=5)
        if cache.get('healthz_ping') == 'ok':
            health_status['services']['cache'] = 'connected'
        else:
            raise Exception("Cache write failed")
    except Exception as e:
        health_status['services']['cache'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
        status_code = 503

    return JsonResponse(health_status, status=status_code)
```

`config/urls.py`-তে রাউট যোগ করুন:
```python
path('health/', views.health_check_view, name='health_check'),
```

---

## ৬. অ্যালার্ট ফ্যাটিগ (Alert Fatigue) রোধ করার সেরা কৌশল 🔕

যদি প্রতিদিন স্ল্যাকে ১০০টি অপ্রয়োজনীয় ওয়ার্নিং আসে, তবে ডেভেলপাররা আসল বিপজ্জনক ক্র্যাশও অবহেলা করবেন। একে বলা হয় **Alert Fatigue**।

### সুরক্ষার ৪টি নিয়ম:
1. **404 Page Not Found এরর কখনোই মনিটরিং ড্যাশবোর্ডে পাঠাবেন না** (বটরা প্রতিনিয়ত র‍্যান্ডম URL স্ক্যান করে)।
2. **এক্সেপশন গ্রুপিং:** একই ডেটাবেজ ডাউন এরর ১০০ বার ঘটলে Sentry সেটিকে ১টি ইস্যুতে গ্রুপ করে।
3. **স্ন্যুজিং ও থ্রেশহোল্ড:** "যদি ১ মিনিটে ৫টির বেশি 500 এরর হয়, তবেই ইমার্জেন্সি অ্যালার্ট পাঠাও"।
4. **ডেভেলপমেন্ট ও স্টেজিং আলাদা রাখুন:** `environment='production'` এবং `environment='staging'` ফিল্টার করে নিন।

---

## সারসংক্ষেপ চেকলিস্ট 📋

1. ✅ ক্লাউড এনভায়রনমেন্টে ফাইল লগের বদলে কনসোলে **Structured JSON Log** স্ট্রিম করা হয়েছে।
2. ✅ প্রতিটি রিকোয়েস্টে **Request-ID** ট্যাগ করার ব্যবস্থা রাখা হয়েছে।
3. ✅ লাইভ ক্র্যাশ মনিটরিংয়ের জন্য **Sentry SDK** কনফিগার করা হয়েছে।
4. ✅ লোড ব্যালেন্সারের জন্য ডেটাবেজ ও ক্যাশ যুক্ত **`/health/`** এন্ডপয়েন্ট তৈরি আছে।
5. ✅ সংবেদনশীল তথ্য যাতে মনিটরিং ড্যাশবোর্ডে লিক না হয় (`send_default_pii=False`) তা নিশ্চিত করা হয়েছে।
