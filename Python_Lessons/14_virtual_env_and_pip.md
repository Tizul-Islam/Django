# Python: Virtual Environment ও pip 📦🔧

Python প্রজেক্টের সবচেয়ে গুরুত্বপূর্ণ বিষয় হলো **Virtual Environment (venv)** এবং **pip**। এগুলো ছাড়া বড় কোনো প্রজেক্টের কাজ করা কঠিন।

---

## ১. pip কী?

**pip** হলো Python-এর package manager। এর মাধ্যমে Python-এর বাইরের প্যাকেজ (library) ইনস্টল করা যায়।

### কেন pip দরকার?

Python-এর নিজে কিছু built-in module আছে (math, random, datetime ইত্যাদি), কিন্তু অনেক কাজের জন্য বাইরের প্যাকেজ দরকার হয়। যেমন:
- Web framework: Django, Flask
- Data science: NumPy, Pandas, Matplotlib
- HTTP request: requests
- GUI: PyQt, Tkinter

---

## ২. pip এর মূল কমান্ড

### Package ইনস্টল করা:

```bash
pip install package_name
```

উদাহরণ:
```bash
pip install django
pip install requests
pip install pandas
```

### নির্দিষ্ট Version ইনস্টল:

```bash
pip install django==4.2.0
pip install "django>=4.0,<5.0"
```

### Package আপডেট:

```bash
pip install --upgrade package_name
```

### Package আনইনস্টল:

```bash
pip uninstall package_name
```

### ইনস্টলড Package দেখা:

```bash
pip list
```

### Package-এর তথ্য দেখা:

```bash
pip show django
```

আউটপুট:
```
Name: Django
Version: 4.2.0
Summary: A high-level Python Web framework
...
```

### Package খোঁজা:

```bash
pip search package_name
```

---

## ৩. Virtual Environment কী এবং কেন দরকার?

**Virtual Environment (venv)** হলো Python-এর একটা আলাদা পরিবেশ যেখানে একটা নির্দিষ্ট প্রজেক্টের জন্য প্যাকেজ ইনস্টল করা হয়।

### কেন venv দরকার?

ধরুন আপনার দুটো প্রজেক্ট আছে:
- **Project A** — Django 3.2 ব্যবহার করে
- **Project B** — Django 4.2 ব্যবহার করে

যদি একটাই environment থাকে, তাহলে দুটো Django version একসাথে থাকতে পারবে না। venv দিয়ে প্রতিটা প্রজেক্টের জন্য আলাদা পরিবেশ তৈরি করা যায়।

**সুবিধা:**
- 🔒 প্রতিটা প্রজেক্টের নিজস্ব dependency
- 📦 version conflict এড়ানো যায়
- 🧹 global Python পরিষ্কার থাকে
- 📋 সহজে dependency শেয়ার করা যায়

---

## ৪. Virtual Environment তৈরি করা

### Windows-এ:

```bash
# venv তৈরি
python -m venv venv

# Activate
venv\Scripts\activate

# Deactivate
deactivate
```

### macOS/Linux-এ:

```bash
# venv তৈরি
python3 -m venv venv

# Activate
source venv/bin/activate

# Deactivate
deactivate
```

### Activate হওয়ার পর:

Terminal-এ `(venv)` দেখাবে:
```
(venv) user@computer:~/project$
```

এখন যেকোনো pip command দিলে শুধু এই venv-এ ইনস্টল হবে।

---

## ৫. venv দিয়ে কাজ করার পুরো প্রক্রিয়া

### ধাপ ১: প্রজেক্ট ফোল্ডারে যান

```bash
cd my_project
```

### ধাপ ২: venv তৈরি করুন

```bash
python -m venv venv
```

### ধাপ ৩: venv Activate করুন

Windows:
```bash
venv\Scripts\activate
```

### ধাপ ৪: প্রয়োজনীয় প্যাকেজ ইনস্টল করুন

```bash
pip install django
pip install requests
```

### ধাপ ৫: কাজ শেষে deactivate করুন

```bash
deactivate
```

---

## ৬. requirements.txt ফাইল

আপনার প্রজেক্টের সব dependency একটা ফাইলে লিখে রাখা যায়, যাতে অন্যরা সহজে ইনস্টল করতে পারে।

### requirements.txt তৈরি করা:

```bash
pip freeze > requirements.txt
```

### requirements.txt এর কন্টেন্ট:

```
asgiref==3.12.1
Django==6.1.2
sqlparse==0.6.0
tzdata==2026.5
```

### requirements.txt থেকে ইনস্টল করা:

```bash
pip install -r requirements.txt
```

### কেন দরকার?

- 📦 অন্য ডেভেলপাররা এক command-এ সব dependency ইনস্টল করতে পারবে
- ☁️ Hosting/deploy করার সময় দরকার হয়
- 📋 কোন কোন version ব্যবহার করছেন তা জানা যায়

---

## ৭. বিভিন্ন Python Package Manager

pip ছাড়াও কিছু জনপ্রিয় package manager আছে:

| Tool | বিবরণ |
|------|--------|
| `pip` | অফিসিয়াল, সবচেয়ে জনপ্রিয় |
| `pipenv` | pip + virtualenv একসাথে |
| `poetry` | আধুনিক, dependency management ভালো |
| `conda` | Data science-এর জন্য জনপ্রিয় |

### Poetry দ্রুত দেখে নিই:

```bash
# ইনস্টল
pip install poetry

# নতুন প্রজেক্ট
poetry new my_project

# প্যাকেজ যোগ
poetry add django

# Activate
poetry shell
```

---

## ৮. সাধারণ সমস্যা ও সমাধান

### সমস্যা ১: `pip` command পাওয়া যাচ্ছে না

সমাধান:
```bash
python -m pip install package_name
```

### সমস্যা ২: Permission denied

সমাধান: `--user` ব্যবহার করুন (venv ব্যবহার করলে এই সমস্যা হয় না):
```bash
pip install --user package_name
```

### সমস্যা ৩: venv Activate হচ্ছে না (Windows)

PowerShell-এ execution policy সমস্যা হতে পারে:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### সমস্যা ৪: কোন package কোন version আছে?

```bash
pip show package_name
```

### সমস্যা ৫: বহু package একসাথে আনইনস্টল

```bash
pip uninstall -r requirements.txt -y
```

---

## ৯. .gitignore এর সাথে venv

venv ফোল্ডার কখনো git-এ commit করা উচিত না। তাই `.gitignore` এ যোগ করতে হবে:

```gitignore
# Virtual Environment
venv/
env/
.venv/

# Byte-compiled files
__pycache__/
*.pyc

# Database
db.sqlite3

# Environment variables
.env
```

---

## ১০. সেরা প্র্যাকটিস (Best Practices)

1. ✅ **প্রতিটা প্রজেক্টের জন্য আলাদা venv** ব্যবহার করুন
2. ✅ **venv নাম `venv`** রাখুন (স্ট্যান্ডার্ড)
3. ✅ **`requirements.txt`** ব্যবহার করুন
4. ✅ **venv git-এ push করবেন না**
5. ✅ **নির্দিষ্ট version** install করুন (যেমন `django==4.2.0`)
6. ❌ venv ছাড়া global Python-এ package ইনস্টল করবেন না

---

## ১১. বাস্তব উদাহরণ — একটা Django প্রজেক্ট সেটআপ

```bash
# ১. প্রজেক্ট ফোল্ডার তৈরি
mkdir my_django_project
cd my_django_project

# ২. Virtual Environment তৈরি
python -m venv venv

# ৩. Activate (Windows)
venv\Scripts\activate

# ৪. Django ইনস্টল
pip install django

# ৫. requirements.txt তৈরি
pip freeze > requirements.txt

# ৬. Django প্রজেক্ট তৈরি
django-admin startproject myproject .

# ৭. Development server চালু
python manage.py runserver

# ৮. কাজ শেষে deactivate
deactivate
```

---

## ১২. Practical Exercise

নিচের ধাপগুলো করে দেখুন:

```bash
# ============ Exercise 1: pip basics ============
# একটা package ইনস্টল করুন
pip install requests

# ইনস্টলড package দেখুন
pip list

# package-এর তথ্য দেখুন
pip show requests

# package আনইনস্টল করুন
pip uninstall requests -y


# ============ Exercise 2: Virtual Environment ============
# একটা নতুন ফোল্ডারে venv তৈরি করুন
mkdir test_venv
cd test_venv
python -m venv venv

# Activate করুন (Windows)
venv\Scripts\activate

# venv-এ কিছু package ইনস্টল করুন
pip install requests flask

# ইনস্টলড package দেখুন (venv-এর)
pip list

# requirements.txt তৈরি করুন
pip freeze > requirements.txt

# requirements.txt দেখুন
type requirements.txt   # Windows
# cat requirements.txt  # Linux/Mac

# Deactivate করুন
deactivate

# Global Python-এ package দেখুন (আলাদা হবে)
pip list


# ============ Exercise 3: requirements.txt থেকে ইনস্টল ============
# নতুন venv তৈরি করুন
python -m venv venv2
venv2\Scripts\activate

# আগের requirements.txt থেকে ইনস্টল করুন
pip install -r requirements.txt

# যাচাই করুন
pip list

deactivate
```

---

## 🎯 আজকের Key Takeaways

1. **pip** — Python package manager, বাইরের প্যাকেজ ইনস্টল করার জন্য
2. `pip install package` — package ইনস্টল
3. `pip uninstall package` — package আনইনস্টল
4. `pip list` — ইনস্টলড package দেখা
5. **Virtual Environment (venv)** — প্রতিটা প্রজেক্টের আলাদা পরিবেশ
6. `python -m venv venv` — venv তৈরি
7. `venv\Scripts\activate` — venv চালু (Windows)
8. `source venv/bin/activate` — venv চালু (Linux/Mac)
9. `deactivate` — venv বন্ধ
10. **`requirements.txt`** — সব dependency এক ফাইলে
11. `pip freeze > requirements.txt` — requirements তৈরি
12. `pip install -r requirements.txt` — requirements থেকে ইনস্টল
13. venv কখনো git-এ commit করবেন না

---

## ❓ অনুশীলনী প্রশ্ন

1. pip কী এবং কেন ব্যবহার করা হয়?
2. Virtual Environment কী এবং কেন দরকার?
3. venv তৈরি করার কমান্ড কী?
4. Windows-এ venv activate করার কমান্ড কী?
5. `requirements.txt` ফাইলের গুরুত্ব কী?
6. `pip freeze` কমান্ডের কাজ কী?
7. venv কেন git-এ commit করা উচিত না?
8. একটা নতুন প্রজেক্টে Django ইনস্টল করার পুরো প্রক্রিয়া লিখুন
