# Python: Lambda, Map ও Filter ⚡

Python-এর **Lambda**, **Map** এবং **Filter** হলো ফাংশনাল প্রোগ্রামিং এর সবচেয়ে শক্তিশালী টুল। এগুলো দিয়ে কোড সংক্ষিপ্ত করে লেখা যায় এবং list-এর উপর দ্রুত অপারেশন করা যায়।

---

## ১. Lambda Function (অ্যানোনিমাস ফাংশন)

**Lambda** হলো ছোট ছোট কাজের জন্য ব্যবহার করা এক লাইনের অ্যানোনিমাস (নামবিহীন) ফাংশন। সাধারণত যে কাজ একটা লাইনে করা যায়, সেই কাজের জন্য lambda ব্যবহার করা হয়।

### সিনট্যাক্স:
```python
lambda arguments: expression
```

### সাধারণ Function বনাম Lambda:

```python
# সাধারণ function
def double(x):
    return x * 2

print(double(5))   # 10

# Lambda — এক লাইনে
double = lambda x: x * 2
print(double(5))   # 10
```

### একাধিক Parameter:

```python
add = lambda a, b: a + b
print(add(3, 4))   # 7

multiply = lambda a, b, c: a * b * c
print(multiply(2, 3, 4))   # 24
```

### কোনো Parameter ছাড়া:

```python
greet = lambda: "সালাম!"
print(greet())   # সালাম!
```

### Lambda কেন ব্যবহার করবো?

Lambda মূলত **map**, **filter**, **sort** ইত্যাদি ফাংশনের সাথে ব্যবহার করার জন্য বানানো হয়েছে। ছোট ছোট অপারেশনের জন্য আলাদা function লেখার দরকার পড়ে না।

```python
# উদাহরণ: list-এর সব উপাদানকে ২ দিয়ে গুণ
numbers = [1, 2, 3, 4, 5]

# সাধারণভাবে:
def double(x):
    return x * 2

doubled = [double(n) for n in numbers]
print(doubled)   # [2, 4, 6, 8, 10]

# Lambda দিয়ে:
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)   # [2, 4, 6, 8, 10]
```

---

## ২. map() — প্রতিটা উপাদানে অপারেশন প্রয়োগ করা

`map()` ফাংশন একটা iterable (list, tuple ইত্যাদি) এর প্রতিটা উপাদানে একটা নির্দিষ্ট ফাংশন প্রয়োগ করে এবং নতুন একটা map object ফেরত দেয়।

### সিনট্যাক্স:
```python
map(function, iterable)
```

### উদাহরণ:

```python
numbers = [1, 2, 3, 4, 5]

# প্রতিটা সংখ্যাকে ২ দিয়ে গুণ
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)   # [2, 4, 6, 8, 10]

# প্রতিটা সংখ্যার বর্গ
squared = list(map(lambda x: x ** 2, numbers))
print(squared)   # [1, 4, 9, 16, 25]
```

### map() + সাধারণ Function:

```python
def add_ten(x):
    return x + 10

numbers = [1, 2, 3]
result = list(map(add_ten, numbers))
print(result)   # [11, 12, 13]
```

### একাধিক Iterable দিয়ে map():

`map()` একটার বেশি iterable নিতে পারে:

```python
nums1 = [1, 2, 3]
nums2 = [10, 20, 30]

# দুটো list এর উপাদানগুলো যোগ
result = list(map(lambda a, b: a + b, nums1, nums2))
print(result)   # [11, 22, 33]
```

### map() দিয়ে String প্রসেস করা:

```python
names = ["রহিম", "করিম", "সালাম"]

# প্রতিটা নামের সাথে "ভাই" যোগ
greetings = list(map(lambda name: f"{name} ভাই", names))
print(greetings)
# ['রহিম ভাই', 'করিম ভাই', 'সালাম ভাই']

# সব নামকে uppercase করা
words = ["hello", "world", "python"]
upper_words = list(map(str.upper, words))
print(upper_words)
# ['HELLO', 'WORLD', 'PYTHON']
```

---

## ৩. filter() — শর্ত অনুযায়ী উপাদান ছাঁকে নেওয়া

`filter()` ফাংশন একটা iterable থেকে এমন উপাদানগুলো বের করে যেগুলো একটা নির্দিষ্ট শর্ত পূরণ করে।

### সিনট্যাক্স:
```python
filter(function, iterable)
```

### উদাহরণ:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# শুধু বিজোড় সংখ্যা বের করা
odd = list(filter(lambda x: x % 2 != 0, numbers))
print(odd)   # [1, 3, 5, 7, 9]

# শুধু জোড় সংখ্যা বের করা
even = list(filter(lambda x: x % 2 == 0, numbers))
print(even)   # [2, 4, 6, 8, 10]
```

### filter() দিয়ে খালি string বাদ দেওয়া:

```python
names = ["রহিম", "", "করিম", "", "সালাম"]

# খালি string বাদ
non_empty = list(filter(lambda name: name != "", names))
print(non_empty)
# ['রহিম', 'করিম', 'সালাম']

# সহজ উপায় — None দিলেই falsy মান বাদ যায়
non_empty = list(filter(None, names))
print(non_empty)
# ['রহিম', 'করিম', 'সালাম']
```

### filter() দিয়ে শর্ত চেক করা:

```python
ages = [15, 18, 20, 25, 30, 17]

# ১৮ বা তার বেশি বয়স বের করা
adults = list(filter(lambda age: age >= 18, ages))
print(adults)   # [18, 20, 25, 30]
```

---

## ৪. map() ও filter() একসাথে ব্যবহার করা

দুটো ফাংশন একসাথে ব্যবহার করা যায়:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# ধাপ ১: জোড় সংখ্যা বের করা (filter)
# ধাপ ২: প্রতিটা জোড় সংখ্যাকে ২ দিয়ে গুণ (map)
result = list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, numbers)))
print(result)
# [4, 8, 12, 16, 20]

# ধাপ ১: ৫০ এর বেশি সংখ্যা বের করা
# ধাপ ২: তাদের বর্গ করা
nums = [30, 60, 20, 80, 40, 90]
result = list(map(lambda x: x ** 2, filter(lambda x: x > 50, nums)))
print(result)
# [3600, 6400, 8100]
```

---

## ৫. Lambda + sort()

Lambda ব্যবহার করে list কোনো নির্দিষ্ট উপাদান দিয়ে sort করা যায়:

### Dictionary দিয়ে sort:

```python
students = [
    {"name": "রহিম", "marks": 85},
    {"name": "করিম", "marks": 92},
    {"name": "সালাম", "marks": 78},
]

# marks অনুযায়ী ছোট থেকে বড়
students.sort(key=lambda s: s["marks"])
print(students)
# [{'name': 'সালাম', 'marks': 78}, {'name': 'রহিম', 'marks': 85}, {'name': 'করিম', 'marks': 92}]

# marks অনুযায়ী বড় থেকে ছোট
students.sort(key=lambda s: s["marks"], reverse=True)
print(students)
# [{'name': 'করিম', 'marks': 92}, {'name': 'রহিম', 'marks': 85}, {'name': 'সালাম', 'marks': 78}]
```

### Tuple দিয়ে sort:

```python
people = [("রহিম", 25), ("করিম", 30), ("সালাম", 20)]

# বয়স অনুযায়ী sort
people.sort(key=lambda p: p[1])
print(people)
# [('সালাম', 20), ('রহিম', 25), ('করিম', 30)]
```

---

## ৬. reduce() — সব উপাদানকে এক মানে রূপান্তর করা

`reduce()` ফাংশন একটা iterable এর সব উপাদানকে একটা নির্দিষ্ট ফাংশন দিয়ে একত্রিত করে একটা মান ফেরত দেয়। এটা `functools` মডিউল থেকে import করতে হয়।

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# সব সংখ্যার যোগফল
total = reduce(lambda a, b: a + b, numbers)
print(total)   # 15

# সব সংখ্যার গুণফল
product = reduce(lambda a, b: a * b, numbers)
print(product)   # 120

# সবচেয়ে বড় সংখ্যা বের করা
max_num = reduce(lambda a, b: a if a > b else b, numbers)
print(max_num)   # 5
```

### reduce() কীভাবে কাজ করে:

`reduce(lambda a, b: a + b, [1, 2, 3, 4, 5])`:
- `a=1, b=2` → `1+2=3`
- `a=3, b=3` → `3+3=6`
- `a=6, b=4` → `6+4=10`
- `a=10, b=5` → `10+5=15`
- ফলাফল: `15`

---

## ৭. map/filter এর বিকল্প — List Comprehension

Python-এ `map` ও `filter` এর বিকল্প হিসেবে **list comprehension** ব্যবহার করা হয়, যা অনেকে বেশি readable মনে করে:

### map → List Comprehension:

```python
numbers = [1, 2, 3, 4, 5]

# map দিয়ে
doubled_map = list(map(lambda x: x * 2, numbers))

# list comprehension দিয়ে
doubled_comp = [x * 2 for x in numbers]

print(doubled_map)    # [2, 4, 6, 8, 10]
print(doubled_comp)   # [2, 4, 6, 8, 10]
```

### filter → List Comprehension:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# filter দিয়ে
even_filter = list(filter(lambda x: x % 2 == 0, numbers))

# list comprehension দিয়ে
even_comp = [x for x in numbers if x % 2 == 0]

print(even_filter)   # [2, 4, 6, 8, 10]
print(even_comp)     # [2, 4, 6, 8, 10]
```

### map + filter → List Comprehension:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map + filter দিয়ে
result_map = list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, numbers)))

# list comprehension দিয়ে
result_comp = [x * 2 for x in numbers if x % 2 == 0]

print(result_map)    # [4, 8, 12, 16, 20]
print(result_comp)   # [4, 8, 12, 16, 20]
```

**কোনটা ব্যবহার করবেন?**
- ছোট অপারেশনের জন্য **list comprehension** বেশি readable
- কোনো বড় function প্রয়োগ করতে হলে **map** ভালো
- একাধিক iterable দিয়ে কাজ করতে হলে **map** ভালো

---

## ৮. Practical Exercise

নিচের কোড রান করে দেখুন:

```python
from functools import reduce

# --- Exercise 1: Lambda ---
# একটা সংখ্যা বিজোড় কিনা চেক
is_odd = lambda x: x % 2 != 0
print(is_odd(7))    # True
print(is_odd(8))    # False

# --- Exercise 2: map() ---
# list-এর সব সংখ্যার বর্গ
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, numbers))
print("বর্গ:", squares)   # [1, 4, 9, 16, 25]

# --- Exercise 3: filter() ---
# ১০০ এর বেশি সংখ্যা বের করা
prices = [50, 120, 30, 200, 80, 150]
expensive = list(filter(lambda p: p > 100, prices))
print("১০০+:", expensive)   # [120, 200, 150]

# --- Exercise 4: map + filter ---
# জোড় সংখ্যাগুলোকে ৩ দিয়ে গুণ
nums = [1, 2, 3, 4, 5, 6, 7, 8]
result = list(map(lambda x: x * 3, filter(lambda x: x % 2 == 0, nums)))
print("ফলাফল:", result)   # [6, 12, 18, 24]

# --- Exercise 5: sort with lambda ---
products = [
    {"name": "পেন", "price": 10},
    {"name": "কিতাব", "price": 50},
    {"name": "পেন্সিল", "price": 5},
]
products.sort(key=lambda p: p["price"])
print("সাজানো:", products)
# [{'name': 'পেন্সিল', 'price': 5}, {'name': 'পেন', 'price': 10}, {'name': 'কিতাব', 'price': 50}]

# --- Exercise 6: reduce() ---
# সব সংখ্যার যোগফল
total = reduce(lambda a, b: a + b, [10, 20, 30, 40])
print("যোগফল:", total)   # 100
```

---

## 🎯 আজকের Key Takeaways

1. **Lambda** — এক লাইনের নামবিহীন ফাংশন, ছোট ছোট কাজের জন্য
2. **map()** — iterable এর প্রতিটা উপাদানে ফাংশন প্রয়োগ করে
3. **filter()** — iterable থেকে শর্ত অনুযায়ী উপাদান ছাঁকে নেয়
4. **reduce()** — iterable এর সব উপাদানকে এক মানে রূপান্তর করে
5. **Lambda + sort()** — list কোনো নির্দিষ্ট কী দিয়ে sort করা যায়
6. **List comprehension** — map/filter এর readable বিকল্প

---

## ❓ অনুশীলনী প্রশ্ন

1. `lambda x: x * 3` — ল্যাম্বডা ফাংশনটি `6` কল করলে আউটপুট কী হবে?
2. `map()` ও `filter()`-এর পার্থক্য কী?
3. `reduce()` কীভাবে কাজ করে? একটা উদাহরণ দিন
4. `[10, 20, 30, 40, 50]` list থেকে `map` ব্যবহার করে সব সংখ্যাকে ৫ দিয়ে ভাগ করুন
5. `[5, 12, 17, 18, 25, 30]` থেকে `filter` ব্যবহার করে শুধু ৩ দিয়ে বিভাজ্য সংখ্যা বের করুন
6. List comprehension দিয়ে উপরের দুইটা সমস্যা সমাধান করুন
