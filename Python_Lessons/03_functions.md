# Python: Functions 📦

**Function** হলো কোডের একটা ব্লক যা একটা নির্দিষ্ট কাজ সম্পন্ন করে এবং যখন চাই তখন ব্যবহার করা যায়। Function আপনাকে একই কোড বারবার লিখতে বাঁচায়।

---

## ১. Function কেন দরকার?

ধরুন আপনার প্রোগ্রামে ১০ জায়গায় দুই সংখ্যার যোগফল বের করতে হবে। Function ছাড়া ১০ বার একই কোড লিখতে হতো। Function দিয়ে একবার লিখে ১০ বার ব্যবহার করা যায়।

**সুবিধা:**
- 🔁 কোড reuse (পুনরায় ব্যবহার)
- 🧹 কোড clean ও readable
- 🐛 ডিবাগিং সহজ
- 🧩 মডুলার কোডিং

---

## ২. Function তৈরি করা — `def`

`def` কীওয়ার্ড দিয়ে function তৈরি করা হয়:

### সিনট্যাক্স:

```python
def function_name(parameters):
    """ডকুমেন্টেশন (optional)"""
    # কোড
    return value
```

### উদাহরণ:

```python
def greet():
    print("সালাম! কেমন আছেন?")

greet()   # function call
# আউটপুট: সালাম! কেমন আছেন?
```

---

## ৩. Parameters ও Arguments

Function-এ ডেটা পাঠানোর জন্য parameters ব্যবহার করা হয়।

```python
def greet(name):        # name = parameter
    print(f"সালাম, {name}!")

greet("রহিম")           # "রহিম" = argument
greet("করিম")           # "করিম" = argument
# আউটপুট:
# সালাম, রহিম!
# সালাম, করিম!
```

### একাধিক Parameter:

```python
def add(a, b):
    result = a + b
    print(f"{a} + {b} = {result}")

add(5, 3)        # 5 + 3 = 8
add(10, 20)      # 10 + 20 = 30
```

---

## ৪. `return` — মান ফেরত দেওয়া

`return` দিয়ে function থেকে কোনো মান ফেরত দেওয়া যায়। সেই মান variable-এ সংরক্ষণ করা যায়।

```python
def add(a, b):
    return a + b

total = add(5, 3)
print(total)         # 8

print(add(10, 20))   # 30
```

### ⚠️ `return` বনাম `print`:
- `print` — শুধু console-এ দেখায়, মান সংরক্ষণ করে না
- `return` — মান ফেরত দেয়, যা সংরক্ষণ ও ব্যবহার করা যায়

```python
# print — মান reuse করা যায় না
def print_add(a, b):
    print(a + b)

result = print_add(5, 3)   # 8 print হয়
print(result)              # None (কিছু ফেরত আসে না!)

# return — মান reuse করা যায়
def return_add(a, b):
    return a + b

result = return_add(5, 3)  # কিছু print হয় না
print(result)              # 8 (মান সংরক্ষিত)
```

---

## ৫. Default Parameters

কোনো argument না দিলে একটা ডিফল্ট মান ব্যবহার করতে পারেন:

```python
def greet(name, greeting="সালাম"):
    print(f"{greeting}, {name}!")

greet("রহিম")              # সালাম, রহিম!
greet("করিম", "নমস্কার")   # নমস্কার, করিম!
```

### ⚠️ নিয়ম:
Default parameter সবসময় **শেষে** থাকতে হবে:
```python
# ✅ সঠিক
def greet(name, greeting="সালাম"): ...

# ❌ ভুল
def greet(greeting="সালাম", name): ...
```

---

## ৬. Keyword Arguments

Argument-এর নাম বলে বলে মান পাঠানো যায়। এতে ক্রম মেলানোর দরকার পড়ে না:

```python
def full_name(first, last):
    print(f"{first} {last}")

full_name(first="রহিম", last="আহমেদ")   # রহিম আহমেদ
full_name(last="আহমেদ", first="রহিম")   # রহিম আহমেদ (ক্রম ঠিকই)
```

---

## ৭. `*args` — অনেকগুলো Positional Argument

যখন কতগুলো argument আসবে জানা না থাকে, তখন `*args` ব্যবহার করুন। এটা একটা tuple হিসেবে গ্রহণ করে।

```python
def add_all(*args):
    total = 0
    for num in args:
        total += num
    return total

print(add_all(1, 2, 3))          # 6
print(add_all(1, 2, 3, 4, 5))    # 15
```

---

## ৮. `**kwargs` — অনেকগুলো Keyword Argument

`**kwargs` একটা dictionary হিসেবে গ্রহণ করে:

```python
def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

show_info(name="রহিম", age=25, city="ঢাকা")
# আউটপুট:
# name: রহিম
# age: 25
# city: ঢাকা
```

### `*args` ও `**kwargs` একসাথে:

```python
def display(*args, **kwargs):
    print("Positional:", args)
    print("Keyword:", kwargs)

display(1, 2, 3, name="রহিম", age=25)
# আউটপুট:
# Positional: (1, 2, 3)
# Keyword: {'name': 'রহিম', 'age': 25}
```

---

## ৯. Variable Scope (ভেরিয়েবলের ক্ষমতা)

Function-এর ভেতরের variable বাইরে accessible না:

```python
# Local scope
def my_func():
    x = 10        # local variable
    print(x)

my_func()         # 10
# print(x)        # ❌ Error! x এখানে নেই

# Global scope
y = 20            # global variable

def my_func2():
    print(y)      # global variable access করা যায়

my_func2()        # 20
```

### `global` কীওয়ার্ড:

Function-এর ভেতর থেকে global variable পরিবর্তন করতে চাইলে `global` ব্যবহার করুন:

```python
count = 0

def increment():
    global count
    count += 1

increment()
increment()
print(count)      # 2
```

---

## ১০. Nested Function (ভেতরের Function)

Function-এর ভেতরে আরেকটা function তৈরি করা যায়:

```python
def outer():
    print("Outer function")

    def inner():
        print("Inner function")

    inner()   # ভেতরের function call করা হচ্ছে

outer()
# আউটপুট:
# Outer function
# Inner function
```

---

## ১১. Lambda Function (এক লাইন Function)

ছোট ছোট কাজের জন্য ল্যাম্বডা function ব্যবহার করা হয়:

### সিনট্যাক্স:
```python
lambda arguments: expression
```

### উদাহরণ:

```python
# সাধারণ function
def double(x):
    return x * 2

# Lambda
double = lambda x: x * 2

print(double(5))    # 10
```

### একাধিক parameter:

```python
add = lambda a, b: a + b
print(add(3, 4))    # 7
```

### Lambda + filter:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8]

even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)   # [2, 4, 6, 8]
```

### Lambda + map:

```python
numbers = [1, 2, 3, 4, 5]

squared = list(map(lambda x: x ** 2, numbers))
print(squared)   # [1, 4, 9, 16, 25]
```

---

## ১২. Practical Exercise

নিচের কোড রান করে দেখুন:

```python
# --- Exercise 1: যোগফল বের করা ---
def add(a, b):
    return a + b

print("যোগফল:", add(10, 20))   # 30

# --- Exercise 2: বড় সংখ্যা বের করা ---
def max_of_two(a, b):
    if a > b:
        return a
    return b

print("বড়:", max_of_two(10, 20))   # 20

# --- Exercise 3: list-এর সব সংখ্যার যোগফল ---
def sum_list(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print("যোগফল:", sum_list([1, 2, 3, 4, 5]))   # 15

# --- Exercise 4: ফ্যাক্টরিয়াল ---
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print("5! =", factorial(5))   # 120

# --- Exercise 5: ডিফল্ট parameter ---
def power(base, exp=2):
    return base ** exp

print(power(5))      # 25
print(power(5, 3))   # 125

# --- Exercise 6: *args ---
def multiply(*args):
    result = 1
    for num in args:
        result *= num
    return result

print(multiply(1, 2, 3, 4))   # 24
```

---

## 🎯 আজকের Key Takeaways

1. **Function** = একবার লিখে, বারবার ব্যবহার করা যায় এমন কোড ব্লক
2. `def` দিয়ে function তৈরি করা হয়
3. **Parameter** — function ডিক্লারেশনে থাকে, **Argument** — function call-এ পাঠানো হয়
4. `return` — function থেকে মান ফেরত দেয়
5. **Default parameter** — argument না দিলে ডিফল্ট মান ব্যবহার হয়
6. **Keyword arguments** — নাম বলে মান পাঠানো
7. `*args` — অনেক positional argument (tuple)
8. `**kwargs` — অনেক keyword argument (dict)
9. **Scope** — local variable বাইরে accessible না
10. **Lambda** — এক লাইনে ছোট function তৈরি

---

## ❓ অনুশীলনী প্রশ্ন

1. `return` আর `print`-এর পার্থক্য কী?
2. একটা function লিখুন যা একটা list-এর সব সংখ্যার গড় বের করবে
3. একটা function লিখুন যা একটা সংখ্যা কি prime কিনা চেক করবে
4. `*args` কেন ব্যবহার করা হয়?
5. Lambda function কী? একটা উদাহরণ দিন
