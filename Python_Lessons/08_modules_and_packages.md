# Python: Modules ও Packages 📦

Python-এ **Module** হলো একটা `.py` ফাইল যেখানে কিছু কোড (function, class, variable) আছে। **Package** হলো একাধিক module-এর একটা সংগ্রহ (folder)। এগুলো দিয়ে কোডকে সুস্থ ও পুনরায় ব্যবহারযোগ্য করা যায়।

---

## ১. Module কী এবং কেন দরকার?

বড় প্রোগ্রামে সব কোড একটা ফাইলে লিখলে সেটা বিশাল হয়ে যায় এবং পরিচালনা করা কঠিন হয়। Module দিয়ে কোডকে ছোট ছোট অংশে ভাগ করা যায়।

**সুবিধা:**
- 📂 কোড সুস্থ ও সংগঠিত থাকে
- 🔁 একই কোড বারবার ব্যবহার করা যায়
- 🧩 দলের কাজ সহজ হয়

---

## ২. Module তৈরি করা

নতুন একটা `.py` ফাইল তৈরি করে সেখানে কোড লিখলেই সেটা একটা module হয়ে যায়।

### উদাহরণ: `math_operations.py`

```python
# math_operations.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "ভাগশেষ শূন্য দিয়ে ভাগ করা যায় না"
    return a / b

PI = 3.14159
```

---

## ৩. Module Import করা

আরেকটা ফাইল থেকে module import করে ব্যবহার করা যায়।

### Method 1: পুরো module import

```python
import math_operations

result = math_operations.add(10, 5)
print(result)   # 15

print(math_operations.PI)   # 3.14159
```

### Method 2: নির্দিষ্ট কিছু import করা

```python
from math_operations import add, subtract

print(add(10, 5))        # 15
print(subtract(10, 5))   # 5
```

### Method 3: সবকিছু import করা (`*`)

```python
from math_operations import *

print(multiply(3, 4))   # 12
print(PI)               # 3.14159
```

⚠️ সাবধান: `*` দিয়ে সবকিছু import করা ভালো না, কারণ কোনো নাম কোথা থেকে আসছে তা বোঝা কঠিন হয়।

### Method 4: Alias (নতুন নাম) দিয়ে import

```python
import math_operations as mo

print(mo.add(10, 5))    # 15
print(mo.PI)            # 3.14159
```

---

## ৪. Built-in Modules

Python-এ অনেক built-in module আগে থেকেই আছে। কিছু গুরুত্বপূর্ণ:

| Module | কাজ |
|--------|------|
| `math` | গাণিতিক অপারেশন |
| `random` | র্যান্ডম সংখ্যা তৈরি |
| `datetime` | তারিখ ও সময় |
| `os` | অপারেটিং সিস্টেমের সাথে কাজ |
| `sys` | সিস্টেম সেটিংস |
| `json` | JSON ডেটা হ্যান্ডেল |
| `re` | রেগুলার এক্সপ্রেশন |
| `collections` | উন্নত ডেটা স্ট্রাকচার |

### `math` Module:

```python
import math

print(math.pi)                  # 3.141592653589793
print(math.sqrt(16))            # 4.0
print(math.pow(2, 3))           # 8.0
print(math.ceil(4.2))           # 5  (উপরের দিকে round)
print(math.floor(4.8))          # 4  (নিচের দিকে round)
print(math.factorial(5))        # 120
print(math.gcd(12, 18))         # 6  (গসাগু)
print(math.sin(math.pi / 2))    # 1.0
```

### `random` Module:

```python
import random

# ১ থেকে ১০০ এর মধ্যে র্যান্ডম সংখ্যা
print(random.randint(1, 100))

# ০ থেকে ১ এর মধ্যে float
print(random.random())

# list থেকে র্যান্ডম একটা উপাদান
fruits = ["আপেল", "কমলা", "কলা"]
print(random.choice(fruits))

# list কে shuffle করা
cards = [1, 2, 3, 4, 5]
random.shuffle(cards)
print(cards)   # যেকোনো ক্রমে

# র্যান্ডম float একটা রেঞ্জের মধ্যে
print(random.uniform(1.0, 10.0))
```

### `datetime` Module:

```python
from datetime import datetime, date, time

# বর্তমান তারিখ ও সময়
now = datetime.now()
print(now)
# 2026-10-12 14:30:00.123456

# শুধু তারিখ
today = date.today()
print(today)          # 2026-10-12
print(today.year)     # 2026
print(today.month)    # 10
print(today.day)      # 12

# তারিখ ফরম্যাট করা
formatted = now.strftime("%d/%m/%Y %H:%M:%S")
print(formatted)
# 12/10/2026 14:30:00

# নির্দিষ্ট তারিখ থেকে যেকোনো তারিখ
my_birthday = date(2000, 1, 1)
print(my_birthday)
```

### `os` Module:

```python
import os

# বর্তমান কাজের ডিরেক্টরি
print(os.getcwd())

# ডিরেক্টরির ফাইল লিস্ট
print(os.listdir())

# নতুন ডিরেক্টরি তৈরি
os.mkdir("নতুন_ফোল্ডার")

# ফাইল আছে কিনা চেক
print(os.path.exists("math_operations.py"))   # True/False

# ফাইল নাকি ডিরেক্টরি
print(os.path.isfile("math_operations.py"))   # True
print(os.path.isdir("নতুন_ফোল্ডার"))          # True
```

---

## ৫. Package কী?

**Package** হলো একাধিক module-এর একটা সংগ্রহ। একটা folder যেখানে `__init__.py` ফাইল আছে এবং অনেকগুলো `.py` ফাইল আছে, সেটা একটা package।

### Package স্ট্রাকচার:

```
my_package/
├── __init__.py
├── math_ops.py
├── string_ops.py
└── utils/
    ├── __init__.py
    └── helpers.py
```

### `__init__.py` এর কাজ:

এই ফাইলটা দিয়ে Python বুঝে যে এই folderটা একটা package। এটা খালি থাকতে পারে অথবা কিছু code থাকতে পারে।

### Package থেকে Import করা:

```python
# package থেকে module import
from my_package import math_ops
print(math_ops.add(10, 5))

# module থেকে function import
from my_package.math_ops import add
print(add(10, 5))

# nested package থেকে
from my_package.utils import helpers
```

---

## ৬. `pip` দিয়ে External Package ইনস্টল করা

Python-এর বাইরের package `pip` দিয়ে ইনস্টল করা যায়।

### সাধারণ Commands:

```bash
# Package ইনস্টল করা
pip install package_name

# নির্দিষ্ট version ইনস্টল
pip install package_name==2.0.0

# Package আপডেট
pip install --upgrade package_name

# Package আনইনস্টল
pip uninstall package_name

# ইনস্টলড package দেখা
pip list

# Package-এর তথ্য দেখা
pip show package_name

# requirements.txt থেকে সব ইনস্টল
pip install -r requirements.txt
```

### উদাহরণ: `requests` package

```bash
pip install requests
```

```python
import requests

response = requests.get("https://api.github.com")
print(response.status_code)   # 200
```

---

## ৭. `requirements.txt` ফাইল

আপনার প্রজেক্টের সব dependency একটা ফাইলে লিখে রাখা যায়, যাতে অন্যরা সহজে ইনস্টল করতে পারে।

### তৈরি করা:

```bash
pip freeze > requirements.txt
```

### ফাইলের কন্টেন্ট:

```
asgiref==3.12.1
Django==6.1.2
sqlparse==0.6.0
tzdata==2026.5
```

### ইনস্টল করা:

```bash
pip install -r requirements.txt
```

---

## ৮. `if __name__ == "__main__"`

এই কোডটা দিয়ে বুঝা যায় ফাইলটা সরাসরি রান করা হচ্ছে নাকি অন্য ফাইল থেকে import হচ্ছে।

### উদাহরণ:

```python
# math_operations.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

if __name__ == "__main__":
    # এই ফাইল সরাসরি রান করলে এই কোড চলবে
    print("Testing math_operations module")
    print(add(10, 5))
    print(subtract(10, 5))
```

```python
# main.py

import math_operations

# এখানে শুধু import হবে, __main__ এর ভেতরের কোড চলবে না
print(math_operations.add(100, 50))   # 150
```

---

## ৯. Practical Exercise

```python
# ============ math_operations.py ============
# এই ফাইলটা আলাদা করে সেভ করুন

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: শূন্য দিয়ে ভাগ করা যায় না"
    return a / b

if __name__ == "__main__":
    print("Module টেস্টিং:")
    print(f"10 + 5 = {add(10, 5)}")
    print(f"10 - 5 = {subtract(10, 5)}")
    print(f"10 * 5 = {multiply(10, 5)}")
    print(f"10 / 5 = {divide(10, 5)}")


# ============ main.py ============
# এই ফাইলটা আলাদা করে সেভ করুন এবং রান করুন

import math_operations as mo
import math
import random
from datetime import datetime

# Exercise 1: নিজের module ব্যবহার
print("=== নিজের Module ===")
print(f"যোগ: {mo.add(20, 30)}")
print(f"গুণ: {mo.multiply(4, 5)}")

# Exercise 2: math module
print("\n=== Math Module ===")
print(f"sqrt(81) = {math.sqrt(81)}")
print(f"factorial(5) = {math.factorial(5)}")
print(f"gcd(24, 36) = {math.gcd(24, 36)}")

# Exercise 3: random module
print("\n=== Random Module ===")
print(f"র্যান্ডম সংখ্যা: {random.randint(1, 100)}")
fruits = ["আপেল", "কমলা", "কলা", "আম"]
print(f"র্যান্ডম ফল: {random.choice(fruits)}")

# Exercise 4: datetime module
print("\n=== DateTime Module ===")
now = datetime.now()
print(f"আজ: {now.strftime('%d/%m/%Y')}")
print(f"সময়: {now.strftime('%H:%M:%S')}")

# Exercise 5: requirements.txt তৈরি
# টার্মিনালে রান করুন: pip freeze > requirements.txt
```

---

## 🎯 আজকের Key Takeaways

1. **Module** = একটা `.py` ফাইল যেখানে কোড আছে
2. **Package** = একাধিক module-এর সংগ্রহ (folder + `__init__.py`)
3. `import module` — পুরো module import
4. `from module import func` — নির্দিষ্ট function import
5. `import module as alias` — নতুন নাম দিয়ে import
6. Built-in modules: `math`, `random`, `datetime`, `os`, `json` ইত্যাদি
7. `pip install package` — external package ইনস্টল
8. `requirements.txt` — সব dependency এক ফাইলে
9. `if __name__ == "__main__"` — ফাইল সরাসরি রান হলেই এই কোড চলে

---

## ❓ অনুশীলনী প্রশ্ন

1. Module ও Package এর পার্থক্য কী?
2. `from module import *` ব্যবহার করা কেন ভালো না?
3. `math` module দিয়ে ১৪৪ এর বর্গমূল বের করুন
4. `random` module দিয়ে ১ থেকে ১০ এর মধ্যে একটা র্যান্ডম সংখ্যা বের করুন
5. `if __name__ == "__main__"` এর কাজ কী?
6. `pip` কী এবং কেন ব্যবহার করা হয়?
7. `requirements.txt` ফাইলের গুরুত্ব কী?
