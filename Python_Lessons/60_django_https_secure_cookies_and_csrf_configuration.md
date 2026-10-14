# Lesson 60: HTTPS, Secure Cookies এবং CSRF Production Configuration 🔒🛡️

প্রোডাকশন এনভায়রনমেন্টে যখন কোনো ব্যবহারকারী পাসওয়ার্ড দিয়ে লগইন করেন বা ব্যক্তিগত ডেটা আদান-প্রদান করেন, তখন ক্লায়েন্ট ও সার্ভারের মধ্যবর্তী নেটওয়ার্ক সংযোগটি অবশ্যই ক্রিপ্টোগ্রাফিক্যালি এনক্রিপ্টেড (HTTPS) হতে হবে।

যদি HTTPS এবং সিকিউর কুকি সঠিকভাবে কনফিগার না করা থাকে, তবে যে কেউ একই ওয়াইফাই বা নেটওয়ার্কে থাকা অবস্থায় **Man-in-the-Middle (MITM)** আক্রমণের মাধ্যমে ব্যবহারকারীর সেশন কুকি চুরি করে অ্যাকাউন্ট হাইজ্যাক করে নিতে পারে।

এই পাঠে আমরা শিখব:
1. Django-তে সম্পূর্ণ ট্রাফিক HTTPS-এ রিডাইরেক্ট করার নিয়ম
2. **HSTS (HTTP Strict Transport Security)** বাস্তবায়ন
3. **Secure Cookies** (`HttpOnly`, `Secure`, `SameSite`) ফ্ল্যাগের কাজ
4. Django 4.0+ এ **`CSRF_TRUSTED_ORIGINS`** এবং HTTPS CSRF কনফিগারেশন
5. Nginx রিভার্স প্রক্সির সাথে SSL হেডার সিঙ্ক করা

---

## ১. কীভাবে এনক্রিপশন ও কুকি কাজ করে?

```mermaid
sequenceDiagram
    autonumber
    actor User as ব্যবহারকারী (Browser)
    participant Nginx as Nginx (SSL Termination)
    participant Django as Django Application

    User->>Nginx: ১. সাধারণ HTTP রিকোয়েস্ট (http://myshop.com)
    Nginx-->>User: ২. 301 Permanent Redirect (https://myshop.com)
    User->>Nginx: ৩. এনক্রিপ্টেড HTTPS রিকোয়েস্ট
    Nginx->>Django: ৪. X-Forwarded-Proto: https হেডার সহ রিকোয়েস্ট পাঠায়
    Django->>Django: ৫. SECURE_PROXY_SSL_HEADER চেক করে নিশ্চিত হয়
    Django-->>User: ৬. Set-Cookie: sessionid=...; Secure; HttpOnly; SameSite=Lax
    Note over User, Django: ৭. কুকি শুধুমাত্র HTTPS দিয়ে যাবে এবং কোনো ক্ষতিকর JS এটি পড়তে পারবে না! 🛡️
```

---

## ২. HTTPS ও SSL রিডাইরেকশন কনফিগারেশন

[config/settings.py](file:///d:/Next%20Level%202/next.js/Django/config/settings.py) ফাইলে প্রোডাকশনের জন্য নিচের সিকিউরিটি ফ্ল্যাগগুলো যুক্ত করতে হয়:

```python
# ১. সমস্ত সাধারণ HTTP রিকোয়েস্টকে স্বয়ংক্রিয়ভাবে HTTPS-এ রিডাইরেক্ট করবে
SECURE_SSL_REDIRECT = True if not DEBUG else False

# ২. রিভার্স প্রক্সি (Nginx / AWS ALB / Cloudflare) এর পেছনে থাকলে আবশ্যক:
# ক্লায়েন্ট যে HTTPS দিয়ে এসেছে তা Nginx এই হেডারের মাধ্যমে Django-কে জানায়
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### HTTP Strict Transport Security (HSTS)
HSTS ব্রাউজারকে নির্দেশ দেয় যে পরবর্তী ১ বছরের মধ্যে এই ডোমেনে ব্যবহারকারী ভুলেও যেন কোনোদিন আন-এনক্রিপ্টেড HTTP দিয়ে প্রবেশের চেষ্টা না করে। ব্রাউজার নিজে থেকেই সরাসরি HTTPS ব্যবহার করবে।

```python
# ৩. HSTS সেটিংস (শুধুমাত্র প্রোডাকশনে কার্যকর করবেন!)
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000             # ১ বছর (Seconds)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True       # সমস্ত সাবডোমেনও HTTPS এ বাধ্য থাকবে
    SECURE_HSTS_PRELOAD = True                  # ব্রাউজারের গ্লোবাল HSTS প্রি-লোড লিস্টের জন্য
```

> ⚠️ **সতর্কতা:** লোকাল মেশিনে বা টেস্টিং ডোমেনে কখনও `SECURE_HSTS_SECONDS` চালু করবেন না। কারণ একবার ব্রাউজার এটি ক্যাশ করে ফেললে SSL সার্টিফিকেট ছাড়া ঐ ডোমেন আর লোকাল পিসিতে খুলবে না!

---

## ৩. Secure Cookies কনফিগারেশন (Session & CSRF) 🍪

কুকি হলো ব্রাউজারে সংরক্ষিত সেশন কি। একে সুরক্ষিত করার জন্য ৩টি প্রধান ফ্ল্যাগ রয়েছে:

| ফ্ল্যাগ | কী কাজ করে? | সম্ভাব্য আক্রমণ যা প্রতিরোধ করে |
| :--- | :--- | :--- |
| **`Secure`** | ব্রাউজারকে নির্দেশ দেয় কুকিটি **শুধুমাত্র HTTPS** সংযোগেই পাঠাতে হবে। সাধারণ HTTP-তে এই কুকি কোনোভাবেই যাবে না। | Sniffing / Man-in-the-Middle (MITM) |
| **`HttpOnly`** | কোনো ক্লায়েন্ট-সাইড JavaScript (`document.cookie`) যাতে এই কুকি পড়তে না পারে। | XSS (Cross-Site Scripting) সেশন হাইজ্যাকিং |
| **`SameSite`** | থার্ড-পার্টি অন্য কোনো সাইট থেকে রিকোয়েস্ট এলে এই কুকি পাঠানো হবে কিনা তা নিয়ন্ত্রণ করে। | CSRF (Cross-Site Request Forgery) |

### `settings.py`-তে কুকি সেটিংস:

```python
# ১. সেশন কুকি সেটিংস
SESSION_COOKIE_SECURE = True if not DEBUG else False    # কেবল HTTPS দিয়ে যাবে
SESSION_COOKIE_HTTPONLY = True                          # জাভাস্ক্রিপ্ট এক্সেস ব্লক (ডিফল্ট True)
SESSION_COOKIE_SAMESITE = 'Lax'                         # CSRF প্রতিরক্ষা (Lax বা Strict)
SESSION_COOKIE_AGE = 1209600                            # ২ সপ্তাহ মেয়াদ (Seconds)

# ২. CSRF কুকি সেটিংস
CSRF_COOKIE_SECURE = True if not DEBUG else False       # কেবল HTTPS দিয়ে যাবে
CSRF_COOKIE_HTTPONLY = False                            # AJAX/React এ কুকি পড়তে লাগলে False, অন্যথায় True
CSRF_COOKIE_SAMESITE = 'Lax'
```

---

## ৪. Django 4.0+ এ `CSRF_TRUSTED_ORIGINS` কনফিগারেশন 🚨

Django 4.0 সংস্করণ থেকে HTTPS সাইটে POST ফর্ম সাবমিট করার সময় Django অতিরিক্ত নিরাপত্তা হিসেবে `Origin` এবং `Referer` হেডার যাচাই করে। 

যদি আপনার ডোমেনটি `CSRF_TRUSTED_ORIGINS` তালিকায় না থাকে, তবে ব্যবহারকারী ফর্ম সাবমিট করলেই **`403 Forbidden: CSRF verification failed. Request aborted.`** এরর দেখতে পাবে!

```python
# settings.py - প্রোটোকল (https://) সহ ডোমেন নাম দিতে হয়:
CSRF_TRUSTED_ORIGINS = [
    'https://myshop.com',
    'https://www.myshop.com',
    'https://*.myshop.com',  # ওয়াইল্ডকার্ড দিয়ে সব সাবডোমেন
]
```

> 📌 **মনে রাখবেন:** `ALLOWED_HOSTS`-এ প্রোটোকল দেওয়া যায় না (`'myshop.com'`), কিন্তু `CSRF_TRUSTED_ORIGINS`-এ অবশ্যই **`https://`** সহ ডোমেন নাম উল্লেখ করতে হয়!

---

## ৫. Nginx রিভার্স প্রক্সি কনফিগারেশন

Nginx-এ SSL সার্টিফিকেট ইনস্টল করার পর Django-র কাছে সঠিক হেডার পৌঁছানো নিশ্চিত করতে নিচের ব্লকটি থাকতে হবে:

```nginx
# /etc/nginx/sites-available/django
server {
    listen 443 ssl http2;
    server_name myshop.com www.myshop.com;

    ssl_certificate /etc/letsencrypt/live/myshop.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myshop.com/privkey.pem;

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        
        # এই হেডারগুলো Django SecurityMiddleware-এর জন্য অত্যাবশ্যক:
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;  # Django SECURE_PROXY_SSL_HEADER এর জন্য
    }
}

# সাধারণ HTTP (Port 80) কে স্বয়ংক্রিয় HTTPS এ রিডাইরেক্ট করা
server {
    listen 80;
    server_name myshop.com www.myshop.com;
    return 301 https://$host$request_uri;
}
```

---

## ৬. সম্পূর্ণ প্রোডাকশন সিকিউরিটি ব্লক (Ready-to-use)

আপনার `config/settings.py` ফাইলের নিচে যুক্ত করার জন্য একটি আদর্শ প্রোডাকশন ব্লক:

```python
# ==========================================
# PRODUCTION SECURITY CONFIGURATION
# ==========================================
if not DEBUG:
    # HTTPS / SSL
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # HSTS
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Secure Cookies
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'

    # Browser Defense Headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

    # CSRF Origins
    CSRF_TRUSTED_ORIGINS = [
        'https://' + host for host in ALLOWED_HOSTS if host not in ['127.0.0.1', 'localhost', '*']
    ]
```

---

## ৭. ডেপ্লয়মেন্ট ভেরিফিকেশন (`check --deploy`)

সমস্ত সেটিংস ঠিকমতো কনফিগার হয়েছে কিনা তা যাচাই করতে টার্মিনালে রান করুন:

```bash
python manage.py check --deploy
```

যদি সব সিকিউরিটি ফ্ল্যাগ সক্রিয় থাকে, Django কোনো ওয়ার্নিং দেবে না এবং দেখাবে:
```text
System check identified no issues (0 silenced).
```
