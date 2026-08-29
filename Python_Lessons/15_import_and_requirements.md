# Python: Import ও requirements.txt 📥📋

Python-এ অন্য কোড বা module ব্যবহার করতে হলে **import** করতে হয়। আর প্রজেক্টের সব dependency একটা ফাইলে রাখা হয় **requirements.txt** তে। আজকে দুটোই বিস্তারিত শিখবো।

---

## ১. Import কী এবং কেন দরকার?

আপনার প্রোগ্রামে যদি অন্য কোনো module-এর কোড (function, class, variable) ব্যবহার করতে হয়, তাহলে সেটা import করতে হয়।

Python-এ import এর সুবিধা:
- 🔁 একই কোড বারবার লিখতে হয় না
- 📦 বড় প্রজেক্টে কোড ছোট ছোট অংশে ভাগ করা যায়
- 🧩 অন্যদের তৈরি library ব্যবহার করা যায়

---

## ২. Import করার বিভিন্ন পদ্ধতি

### Method 1: পুরো Module Import করা

```python
import math

print(math.pi)        # 3.141592653589793
print(math.sqrt(16))  # 4.0
```

### Method 2: নির্দিষ্ট কিছু Import করা

```python
from math import pi, sqrt

print(pi)      # 3.141592653589793
print(sqrt(25))  # 5.0
```

### Method 3: সবকিছু Import করা (`*`)

```python
from math import *

print(pi)        # 3.14159...
print(factorial(5))  # 120
```

⚠️ **সাবধান:** `*` ব্যবহার করা ভালো না, কারণ কোনো নাম কোথা থেকে আসছে বোঝা কঠিন হয়।

### Method 4: Alias (নতুন নাম) দিয়ে Import

```python
import math as m

print(m.pi)        # 3.14159...
print(m.sqrt(9))   # 3.0

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

### Method 5: নির্দিষ্ট কিছুকে Alias দিয়ে Import

```python
from math import pi as PI, sqrt as square_root

print(PI)              # 3.14159...
print(square_root(16)) # 4.0
```

---

## ৩. Import করার কয়েকটা উদাহরণ

### Standard Library থেকে:

```python
import os
import sys
import json
import csv
import datetime
import random
import re
import collections
```

### Third-Party Package থেকে:

```python
import requests           # pip install requests
from django.db import models
from flask import Flask
import pandas as pd
import numpy as np
```

### নিজের তৈরি Module থেকে:

```python
# my_module.py ফাইল আছে অনুমান করি
import my_module
from my_module import my_function
from my_module import MyClass
```

---

## ৪. Import এর জন্য কোথা থেকে খোঁজে?

Python import করতে গেলে এই জায়গাগুলোতে খোঁজে:
1. বর্তমান directory
2. `PYTHONPATH` environment variable-এর path
3. Python ইনস্টলেশনের `site-packages` ফোল্ডার

`sys.path` দিয়ে দেখা যায় কোথা কোথা খোঁজছে:

```python
import sys
print(sys.path)
```

---

## ৫. Package থেকে Import

Package হলো একাধিক module-এর সংগ্রহ (একটা folder)।

### Package Structure:

```
my_package/
├── __init__.py
├── module1.py
├── module2.py
└── sub_package/
    ├── __init__.py
    └── module3.py
```

### Import করা:

```python
# package থেকে module import
from my_package import module1
from my_package.module1 import MyClass

# sub-package থেকে
from my_package.sub_package import module3
from my_package.sub_package.module3 import some_function
```

---

## ৬. Relative Import (আপেক্ষিক Import)

Package-এর ভেতরে এক module থেকে অন্য module import করতে relative import ব্যবহার করা হয়।

### `.` (dot) দিয়ে:

```
my_package/
├── __init__.py
├── parent.py
└── child.py
```

`child.py` থেকে `parent.py` import:

```python
# child.py
from . import parent
from .parent import some_function
```

### `..` (double dot) দিয়ে উপরের ফোল্ডারে:

```
my_package/
├── __init__.py
├── utils.py
└── sub/
    ├── __init__.py
    └── helper.py
```

`helper.py` থেকে `utils.py` import:

```python
# sub/helper.py
from .. import utils
from ..utils import helper_function
```

---

## ৭. Conditional Import (শর্ত অনুযায়ী Import)

কোনো package থাকলে import করা, না থাকলে অন্য কিছু ব্যবহার করা:

```python
try:
    import json
except ImportError:
    import simplejson as json
```

### Platform অনুযায়ী Import:

```python
import sys

if sys.platform == "win32":
    import winreg
else:
    import fcntl
```

---

## ৮. `importlib` দিয়ে Dynamic Import

রানটাইমে string থেকে module import করা যায়:

```python
import importlib

module_name = "math"
math_module = importlib.import_module(module_name)
print(math_module.sqrt(25))   # 5.0
```

---

## ৯. requirements.txt কী এবং কেন দরকার?

**requirements.txt** হলো একটা টেক্সট ফাইল যেখানে প্রজেক্টের সব dependency (package) এবং তাদের version লেখা থাকে।

**সুবিধা:**
- 📦 অন্য ডেভেলপাররা এক command-এ সব dependency ইনস্টল করতে পারবে
- ☁️ Hosting/deploy করার সময় দরকার হয়
- 📋 কোন কোন version ব্যবহার করছেন তা জানা যায়
- 🔒 version conflict এড়ানো যায়

---

## ১০. requirements.txt তৈরি করা

### Method 1: `pip freeze` দিয়ে (সব package)

```bash
pip freeze > requirements.txt
```

ফাইলের কন্টেন্ট:
```
asgiref==3.12.1
Django==6.1.2
sqlparse==0.6.0
tzdata==2026.5
```

### Method 2: ম্যানুয়ালি লেখা

```txt
# ফাইলের নাম: requirements.txt
django==4.2.0
djangorestframework==3.14.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
python-dotenv==1.0.0
pillow==10.1.0
requests==2.31.0
```

### Method 3: নির্দিষ্ট package দিয়ে

```bash
pip freeze | grep django > requirements.txt
```

---

## ১১. requirements.txt থেকে ইনস্টল করা

### সব package ইনস্টল:

```bash
pip install -r requirements.txt
```

### একটা নির্দিষ্ট ফাইল থেকে:

```bash
pip install -r requirements/dev.txt
```

### আপডেট করে ইনস্টল:

```bash
pip install --upgrade -r requirements.txt
```

---

## ১২. Version Specification

requirements.txt-এ version specify করার বিভিন্ন উপায়:

| সিম্বল | মানে | উদাহরণ |
|--------|------|--------|
| `==` | ঠিক এই version | `django==4.2.0` |
| `>=` | এই version বা তার উপরে | `django>=4.0` |
| `<=` | এই version বা তার নিচে | `django<=4.2` |
| `>` | এর উপরে | `django>4.0` |
| `<` | এর নিচে | `django<5.0` |
| `~=` | compatible release | `django~=4.2` (4.2.x) |
| `*` | wildcard | `django==4.2.*` |

### উদাহরণ:

```txt
# ঠিক 4.2.0
django==4.2.0

# 4.0 বা উপরে
django>=4.0

# 4.0 থেকে 5.0 এর মধ্যে
django>=4.0,<5.0

# 4.2.x series
django~=4.2
```

---

## ১৩. Environment অনুযায়ী আলাদা requirements

বড় প্রজেক্টে আলাদা আলাদা environment-এর জন্য আলাদা requirements ফাইল রাখা হয়।

### Directory Structure:

```
requirements/
├── base.txt
├── dev.txt
├── prod.txt
└── test.txt
```

### `base.txt`:

```txt
django==4.2.0
djangorestframework==3.14.0
psycopg2-binary==2.9.9
```

### `dev.txt`:

```txt
-r base.txt
django-debug-toolbar==4.2.0
pytest==7.4.0
pytest-django==4.5.0
```

### `prod.txt`:

```txt
-r base.txt
gunicorn==21.2.0
whitenoise==6.5.0
```

### ইনস্টল করা:

```bash
# Development
pip install -r requirements/dev.txt

# Production
pip install -r requirements/prod.txt
```

---

## ১৪. requirements.txt-এ কমেন্ট

`#` দিয়ে কমেন্ট লেখা যায়:

```txt
# Core dependencies
django==4.2.0
djangorestframework==3.14.0

# Database
psycopg2-binary==2.9.9

# File handling
pillow==10.1.0
```

---

## ১৫. pip-tools দিয়ে ভালোভাবে ম্যানেজ করা

`pip-tools` দিয়ে dependency ভালোভাবে ম্যানেজ করা যায়।

### ইনস্টল:

```bash
pip install pip-tools
```

### `requirements.in` তৈরি:

```txt
# requirements.in
django
djangorestframework
requests
```

### `requirements.txt` compile করা:

```bash
pip-compile requirements.in
```

### ইনস্টল:

```bash
pip-sync requirements.txt
```

---

## ১৬. সেরা প্র্যাকটিস (Best Practices)

### Import-এর জন্য:

1. ✅ সব import ফাইলের শুরুতে রাখুন
2. ✅ import-এর ক্রম: Standard Library → Third-Party → Local
3. ✅ `*` import এড়িয়ে চলুন
4. ✅ alias ব্যবহার করুন যেখানে দরকার
5. ❌ এক লাইনে অনেক import করবেন না

### ভালো উদাহরণ:

```python
# Standard library
import os
import sys
import json
from datetime import datetime

# Third-party
import requests
from django.db import models
from rest_framework import serializers

# Local
from .models import User
from .utils import helper_function
```

### requirements.txt-এর জন্য:

1. ✅ সব dependency লিখুন
2. ✅ নির্দিষ্ট version উল্লেখ করুন
3. ✅ environment অনুযায়ী আলাদা ফাইল রাখুন
4. ✅ কমেন্ট দিয়ে স্পষ্ট করুন
5. ✅ নিয়মিত আপডেট করুন

---

## ১৭. Practical Exercise

```python
# ============ Exercise 1: Import Practice ============

# ১. math module import করে sqrt ব্যবহার করুন
import math
print(math.sqrt(81))   # 9.0

# ২. random থেকে randint import করুন
from random import randint
print(randint(1, 100))

# ৩. datetime থেকে datetime import করুন
from datetime import datetime
print(datetime.now())

# ৪. json module-কে alias দিয়ে import করুন
import json as j
data = j.dumps({"name": "রহিম"})
print(data)

# ৫. os থেকে path import করুন
from os import path
print(path.exists("requirements.txt"))


# ============ Exercise 2: নিজের Module ============
# নিচের কোডটা `calc.py` ফাইলে সেভ করুন:
"""
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

PI = 3.14159
"""

# এবং আরেকটা ফাইলে import করুন:
# from calc import add, subtract, PI
# print(add(10, 5))
# print(PI)


# ============ Exercise 3: Conditional Import ============
try:
    import requests
    print("requests প্যাকেজ আছে")
except ImportError:
    print("requests প্যাকেজ নেই, ইনস্টল করুন: pip install requests")


# ============ Exercise 4: requirements.txt বানানো ============
# টার্মিনালে রান করুন:
# pip freeze > requirements.txt
# এবং ফাইলটা দেখুন
```

### requirements.txt উদাহরণ তৈরি করুন:

নিজের একটা `requirements.txt` ফাইল বানান:

```txt
# requirements.txt

# Web Framework
django==4.2.0
djangorestframework==3.14.0

# Database
psycopg2-binary==2.9.9

# API
requests==2.31.0

# Authentication
djangorestframework-simplejwt==5.3.0

# File handling
pillow==10.1.0

# Environment
python-dotenv==1.0.0

# Development
django-debug-toolbar==4.2.0
```

---

## 🎯 আজকের Key Takeaways

### Import:
1. `import module` — পুরো module import
2. `from module import func` — নির্দিষ্ট function import
3. `import module as alias` — নতুন নাম দিয়ে
4. `from module import *` — সবকিছু (এড়িয়ে চলুন)
5. Relative import: `.` (এক ফোল্ডারে), `..` (উপরের ফোল্ডারে)
6. Import ক্রম: Standard → Third-party → Local
7. `try-except ImportError` দিয়ে conditional import

### requirements.txt:
1. সব package ও version এক ফাইলে
2. `pip freeze > requirements.txt` দিয়ে তৈরি
3. `pip install -r requirements.txt` দিয়ে ইনস্টল
4. Version specify: `==`, `>=`, `<=`, `~=`
5. Environment অনুযায়ী আলাদা ফাইল রাখুন
6. `#` দিয়ে কমেন্ট লেখা যায়

---

## ❓ অনুশীলনী প্রশ্ন

1. `import math` এবং `from math import sqrt` এর পার্থক্য কী?
2. Alias দিয়ে import কীভাবে করা যায়? উদাহরণ দিন
3. `*` দিয়ে import করা কেন ভালো না?
4. Relative Import কী? `.` এবং `..` এর মানে কী?
5. requirements.txt ফাইলের গুরুত্ব কী?
6. `pip freeze` কমান্ডের কাজ কী?
7. requirements.txt থেকে package ইনস্টল করার কমান্ড কী?
8. `django==4.2.0` এবং `django>=4.0` এর পার্থক্য কী?
9. Environment অনুযায়ী আলাদা requirements ফাইল কেন রাখা হয়?
