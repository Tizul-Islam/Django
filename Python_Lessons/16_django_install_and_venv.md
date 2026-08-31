# Django: Install ও Virtual Environment 🐍🌐

Django শেখার শুরুতে প্রথমে Environment সেটআপ করতে হয়। এই লেসনে শিখবো কীভাবে Virtual Environment তৈরি করে Django install করা যায়।

---

## ১. Django কী?

**Django** হলো Python-এর একটা জনপ্রিয় **Web Framework**। এর মাধ্যমে দ্রুত ও নিরাপদে ওয়েবসাইট বা ওয়েব অ্যাপ্লিকেশন বানানো যায়।

### Django-এর বৈশিষ্ট্য:
- 🚀 **Fast** — দ্রুত ডেভেলপমেন্ট
- 🔒 **Secure** — built-in security features
- 📦 **Batteries-included** — ORM, Admin, Auth ইত্যাদি built-in
- 📱 **Scalable** — বড় প্রজেক্টেও কাজ করে
- 🧩 **MTV Architecture** — Model, Template, View

### Django দিয়ে কী কী বানানো যায়?
- ব্লগ ওয়েবসাইট
- ই-কমার্স সাইট
- সোশ্যাল মিডিয়া অ্যাপ
- REST API
- Dashboard / Admin Panel
- SaaS অ্যাপ্লিকেশন

---

## ২. Django install করার আগের প্রস্তুতি

### প্রয়োজনীয় জিনিস:
1. ✅ Python ইনস্টল থাকতে হবে (3.8+)
2. ✅ pip থাকতে হবে
3. ✅ Virtual Environment ব্যবহার করা ভালো

### Python চেক:

```bash
python --version
# Python 3.12.0
```

### pip চেক:

```bash
pip --version
# pip 24.0 from ... (python 3.12)
```

---

## ৩. Virtual Environment তৈরি করা

### ধাপ ১: প্রজেক্ট ফোল্ডার তৈরি

```bash
mkdir my_django_project
cd my_django_project
```

### ধাপ ২: Virtual Environment তৈরি

```bash
python -m venv venv
```

এই কমান্ডটা `venv` নামে একটা ফোল্ডার তৈরি করবে যেখানে Python ও pip থাকবে।

### ধাপ ৩: Virtual Environment Activate

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

Activate হওয়ার পর টার্মিনালের শুরুতে `(venv)` দেখাবে:

```
(venv) C:\Users\name\my_django_project>
```

### ধাপ ৪: pip আপডেট করা (optional কিন্তু ভালো)

```bash
python -m pip install --upgrade pip
```

---

## ৪. Django ইনস্টল করা

### সর্বশেষ Version ইনস্টল:

```bash
pip install django
```

### নির্দিষ্ট Version ইনস্টল:

```bash
pip install django==4.2.0
```

### Version চেক:

```bash
python -m django --version
# 4.2.0
```

অথবা Python দিয়ে:

```python
import django
print(django.get_version())
# 4.2.0
```

---

## ৫. পুরো সেটআপ একসাথে

### Windows-এ পুরো প্রক্রিয়া:

```bash
# ১. ফোল্ডার তৈরি ও প্রবেশ
mkdir my_django_project
cd my_django_project

# ২. Virtual Environment তৈরি
python -m venv venv

# ৩. Activate
venv\Scripts\activate

# ৪. pip আপডেট
python -m pip install --upgrade pip

# ৫. Django ইনস্টল
pip install django

# ৬. Version চেক
python -m django --version

# ৭. requirements.txt তৈরি
pip freeze > requirements.txt
```

### macOS/Linux-এ পুরো প্রক্রিয়া:

```bash
# ১. ফোল্ডার তৈরি ও প্রবেশ
mkdir my_django_project
cd my_django_project

# ২. Virtual Environment তৈরি
python3 -m venv venv

# ৩. Activate
source venv/bin/activate

# ৪. pip আপডেট
pip install --upgrade pip

# ৫. Django ইনস্টল
pip install django

# ৬. Version চেক
python -m django --version

# ৭. requirements.txt তৈরি
pip freeze > requirements.txt
```

---

## ৬. requirements.txt

ইনস্টল হওয়া সব package ও তাদের version একটা ফাইলে সেভ করা যায়।

### তৈরি করা:

```bash
pip freeze > requirements.txt
```

### ফাইলের কন্টেন্ট:

```
asgiref==3.12.1
Django==4.2.0
sqlparse==0.6.0
tzdata==2024.1
```

### requirements.txt থেকে ইনস্টল:

```bash
pip install -r requirements.txt
```

### কেন দরকার?
- অন্য ডেভেলপাররা এক command-এ সব package ইনস্টল করতে পারবে
- Hosting/deploy করার সময় দরকার হয়
- কোন version ব্যবহার করছেন তা জানা যায়

---

## ৭. venv Deactivate করা

কাজ শেষে venv বন্ধ করতে:

```bash
deactivate
```

---

## ৮. সাধারণ সমস্যা ও সমাধান

### সমস্যা ১: `pip` command পাওয়া যাচ্ছে না

সমাধান:
```bash
python -m pip install django
```

### সমস্যা ২: venv Activate হচ্ছে না (Windows PowerShell)

সমাধান:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

তারপর আবার `venv\Scripts\activate` চালান।

### সমস্যা ৩: `python` command কাজ করছে না

সমাধান: `python` এর বদলে `python3` চেষ্টা করুন (Linux/Mac):
```bash
python3 -m venv venv
```

### সমস্যা ৪: Permission Error

venv ব্যবহার করলে এই সমস্যা হয় না। তবে global এ install করতে হলে:
```bash
pip install --user django
```

### সমস্যা ৫: কোন Django Version ইনস্টল আছে?

```bash
pip show django
```

---

## ৯. .gitignore ফাইল

venv ও অন্যান্য অপ্রয়োজনীয় ফাইল git-এ যেন না যায়, `.gitignore` ফাইল তৈরি করুন:

```gitignore
# Virtual Environment
venv/
env/
.venv/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Database
db.sqlite3
db.sqlite3-journal

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/

# Django
*.log
staticfiles/
media/
```

---

## ১০. সেরা প্র্যাকটিস (Best Practices)

1. ✅ প্রতিটা প্রজেক্টের জন্য আলাদা venv ব্যবহার করুন
2. ✅ venv কখনো git-এ commit করবেন না
3. ✅ `requirements.txt` ব্যবহার করুন
4. ✅ নির্দিষ্ট Django version install করুন
5. ✅ নিয়মিত `pip freeze > requirements.txt` চালান
6. ❌ venv ছাড়া global Python-এ Django install করবেন না

---

## ১১. Quick Reference Cheat Sheet

| কাজ | কমান্ড |
|-----|--------|
| venv তৈরি | `python -m venv venv` |
| Activate (Win) | `venv\Scripts\activate` |
| Activate (Mac/Linux) | `source venv/bin/activate` |
| Deactivate | `deactivate` |
| Django install | `pip install django` |
| নির্দিষ্ট version | `pip install django==4.2.0` |
| Version চেক | `python -m django --version` |
| requirements তৈরি | `pip freeze > requirements.txt` |
| requirements থেকে ইনস্টল | `pip install -r requirements.txt` |

---

## 🎯 আজকের Key Takeaways

1. **Django** — Python-এর ওয়েব framework
2. প্রথমে **Virtual Environment** তৈরি করতে হয়
3. `python -m venv venv` — venv তৈরি
4. `venv\Scripts\activate` — Activate (Windows)
5. `source venv/bin/activate` — Activate (Linux/Mac)
6. `pip install django` — Django ইনস্টল
7. `pip freeze > requirements.txt` — dependency সেভ
8. venv কখনো git-এ যাবে না (`.gitignore` দিয়ে)

---

## ❓ অনুশীলনী প্রশ্ন

1. Django কী এবং কেন ব্যবহার করা হয়?
2. Virtual Environment কেন দরকার?
3. Windows-এ venv activate করার কমান্ড কী?
4. Django install করার কমান্ড কী?
5. `pip freeze > requirements.txt` এর কাজ কী?
6. venv কেন git-এ commit করা উচিত না?
7. একটা নতুন Django প্রজেক্টের Environment সেটআপের পুরো প্রক্রিয়া লিখুন
