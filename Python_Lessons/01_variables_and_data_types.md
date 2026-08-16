# Python Basics: Variables & Data Types 🐍

Python-এর সবচেয়ে ভিত্তিগত বিষয় — **Variables** (ভেরিয়েবল) আর **Data Types** (ডেটা টাইপ)।

---

## ১. Variables (ভেরিয়েবল) কী?

ভেরিয়েবল = **ডেটা রাখার বক্স**। যেমন একটা বাক্সে আপনি মার্কার রাখলেন এবং বাক্সের উপর লিখে দিলেন "মার্কার"। পরে "মার্কার" বললেই আপনি বুঝবেন সেই বাক্সটা।

Python-এ ভেরিয়েবল তৈরি করা খুব সহজ — `=` চিহ্ন দিয়ে মান বসিয়ে দিলেই হয়:

```python
name = "Rahim"
age = 25
height = 5.8
is_student = True
```

### Variable নামের নিয়ম:
| নিয়ম | ✅ ভ্যালিড | ❌ অবৈধ |
|-------|-----------|---------|
| Letter বা `_` দিয়ে শুরু | `name`, `_age` | `2name` |
| শুধু letter, number, `_` | `my_var2` | `my-var`, `my var` |
| Space থাকবে না | `first_name` | `first name` |
| Case-sensitive | `name` ≠ `Name` | — |

```python
name = "Rahim"
Name = "Karim"
print(name)   # Rahim
print(Name)   # Karim  (আলাদা ভেরিয়েবল!)
```

---

## ২. Data Types (ডেটা টাইপ)

Python-এ কয়েকটি built-in data type আছে। একই ভেরিয়েবলে একসময় `int`, পরে `str` রাখা যায় — এটাকে **Dynamic Typing** বলে।

### 🎯 মূল ৪টি Data Type:

| Type | নাম | উদাহরণ | ব্যবহার |
|------|-----|--------|---------|
| `int` | Integer | `10`, `-5`, `1000` | পূর্ণ সংখ্যা |
| `float` | Float | `3.14`, `-0.5`, `2.0` | দশমিক সংখ্যা |
| `str` | String | `"Hello"`, `'Python'` | লেখা / টেক্সট |
| `bool` | Boolean | `True`, `False` | হ্যাঁ / না |

### রান করে দেখুন:

```python
age = 25              # int
price = 99.99         # float
name = "Karim"        # str
is_logged_in = True   # bool

print(age)            # 25
print(price)          # 99.99
print(name)           # Karim
print(is_logged_in)   # True
```

---

## ৩. Type চেক করা — `type()` ফাংশন

কোনো ভেরিয়েবলের type জানতে `type()` ব্যবহার করুন:

```python
x = 42
print(type(x))          # <class 'int'>

y = 3.14
print(type(y))          # <class 'float'>

name = "Python"
print(type(name))       # <class 'str'>

is_ok = True
print(type(is_ok))      # <class 'bool'>
```

---

## ৪. Type Conversion (টাইপ রূপান্তর)

কখনও কখনও একটা type থেকে অন্য type-এ পরিবর্তন করতে হয়। Python-এ এটা খুব সহজ:

| ফাংশন | কাজ | উদাহরণ |
|-------|-----|--------|
| `int()` | Integer বানায় | `int("10")` → `10` |
| `float()` | Float বানায় | `float(5)` → `5.0` |
| `str()` | String বানায় | `str(25)` → `"25"` |
| `bool()` | Boolean বানায় | `bool(1)` → `True` |

### কোড উদাহরণ:

```python
# String → Integer
num_str = "100"
num_int = int(num_str)
print(num_int * 2)          # 200

# Integer → String
age = 25
print("Ami " + str(age) + " bochorer")  # Ami 25 bochorer

# Integer → Float
x = 5
y = float(x)
print(y)                    # 5.0

# Float → Integer (decimal বাদ যাবে!)
z = 9.99
print(int(z))               # 9
```

### ⚠️ সাবধান!
`int("hello")` — এটা Error দেবে, কারণ "hello" কে সংখ্যায় রূপান্তর করা যায় না।

---

## ৫. Practical Exercise — নিজে চেষ্টা করুন

নিচের কোডটা একটা ফাইলে লিখে রান করে দেখুন:

```python
# --- নিজের তথ্য প্রিন্ট করুন ---
student_name = "আপনার_নাম"
roll = 10
gpa = 4.85
passed = True

print("Name:", student_name, "| Type:", type(student_name))
print("Roll:", roll, "| Type:", type(roll))
print("GPA:", gpa, "| Type:", type(gpa))
print("Passed:", passed, "| Type:", type(passed))

# --- String concatenation (জোড়া লাগানো) ---
city = "Dhaka"
print("I live in " + city)

# --- Type conversion চেষ্টা করুন ---
math = "80"
physics = "75"
total = int(math) + int(physics)
print("Total marks:", total)   # 155
```

---

## 🎯 আজকের Key Takeaways

1. **Variable** = ডেটা রাখার বক্স, নাম দিয়ে access করা যায়
2. Python-এ type declare করতে হয় না — `=` দিয়ে assign করলেই হয়
3. **৪টি fundamental type**: `int`, `float`, `str`, `bool`
4. `type()` দিয়ে type check করা যায়
5. `int()`, `float()`, `str()`, `bool()` দিয়ে type conversion করা যায়
6. Variable নাম case-sensitive — `name` আর `Name` আলাদা

---

## ❓ অনুশীলনী প্রশ্ন

1. `"10"` আর `10` এর মধ্যে পার্থক্য কী?
2. `int(3.7)` এর আউটপুট কী হবে এবং কেন?
3. কীভাবে আপনি আপনার নাম ও বয়স একই লাইনে প্রিন্ট করবেন?
