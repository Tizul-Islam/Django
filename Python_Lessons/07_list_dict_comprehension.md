# Python: List & Dictionary Comprehension 🎯

**Comprehension** হলো Python-এর একটি শক্তিশালী ফিচার যা দিয়ে এক লাইনে list, dictionary, set তৈরি করা যায়। এটা কোডকে সংক্ষিপ্ত ও readable করে তোলে।

---

## ১. List Comprehension কী?

সাধারণভাবে list তৈরি করতে `for` loop লিখতে হয়। List comprehension দিয়ে সেই কাজ এক লাইনে করা যায়।

### সাধারণ পদ্ধতি (Loop):

```python
numbers = [1, 2, 3, 4, 5]
doubled = []

for n in numbers:
    doubled.append(n * 2)

print(doubled)   # [2, 4, 6, 8, 10]
```

### List Comprehension দিয়ে:

```python
numbers = [1, 2, 3, 4, 5]
doubled = [n * 2 for n in numbers]

print(doubled)   # [2, 4, 6, 8, 10]
```

---

## ২. List Comprehension এর সিনট্যাক্স

```python
[expression for item in iterable]
```

| অংশ | বিবরণ |
|-----|--------|
| `expression` | প্রতিটা item থেকে কী বানাবেন |
| `item` | প্রতিটা উপাদানের নাম |
| `iterable` | যেখান থেকে item নেবেন (list, range, string) |

### উদাহরণসমূহ:

```python
# ১ থেকে ১০ পর্যন্ত সংখ্যার list
nums = [i for i in range(1, 11)]
print(nums)   # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# সব সংখ্যার বর্গ
squares = [i ** 2 for i in range(1, 6)]
print(squares)   # [1, 4, 9, 16, 25]

# String-এর প্রতিটা ক্যারেক্টার
chars = [c for c in "Python"]
print(chars)   # ['P', 'y', 't', 'h', 'o', 'n']

# সব উপাদানকে string করা
nums = [1, 2, 3]
str_nums = [str(n) for n in nums]
print(str_nums)   # ['1', '2', '3']
```

---

## ৩. List Comprehension এ Condition (if)

শর্ত অনুযায়ী উপাদান বেছে নেওয়া যায়।

### সিনট্যাক্স:

```python
[expression for item in iterable if condition]
```

### উদাহরণ:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# শুধু জোড় সংখ্যা
even = [n for n in numbers if n % 2 == 0]
print(even)   # [2, 4, 6, 8, 10]

# শুধু বিজোড় সংখ্যা
odd = [n for n in numbers if n % 2 != 0]
print(odd)   # [1, 3, 5, 7, 9]

# ৫ এর বেশি সংখ্যা
big = [n for n in numbers if n > 5]
print(big)   # [6, 7, 8, 9, 10]
```

---

## ৪. List Comprehension এ if-else (তিন অংশ)

শর্ত অনুযায়ী আলাদা আলাদা মান দিতে চাইলে `if-else` expression ব্যবহার করা যায়।

### সিনট্যাক্স:

```python
[expression1 if condition else expression2 for item in iterable]
```

### উদাহরণ:

```python
numbers = [1, 2, 3, 4, 5]

# জোড় হলে "even", বিজোড় হলে "odd"
labels = ["even" if n % 2 == 0 else "odd" for n in numbers]
print(labels)   # ['odd', 'even', 'odd', 'even', 'odd']

# ৩ এর বেশি হলে সংখ্যাটা, না হলে ০
result = [n if n > 3 else 0 for n in numbers]
print(result)   # [0, 0, 0, 4, 5]

# পজিটিভ/নেগেটিভ চেক
nums = [-3, -1, 0, 2, 5]
signs = ["positive" if n > 0 else ("negative" if n < 0 else "zero") for n in nums]
print(signs)
# ['negative', 'negative', 'zero', 'positive', 'positive']
```

---

## ৫. Nested List Comprehension

একাধিক `for` loop একসাথে ব্যবহার করা যায়।

### 2D List তৈরি:

```python
# ৩x৩ ম্যাট্রিক্স
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(matrix)
# [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```

### Nested List ফ্ল্যাট করা:

```python
nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# nested list থেকে এক একটা উপাদান বের করা
flat = [item for sublist in nested for item in sublist]
print(flat)
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### উদাহরণ ব্যাখ্যা:
```python
flat = [item for sublist in nested for item in sublist]

# এটা সমতুল:
flat = []
for sublist in nested:
    for item in sublist:
        flat.append(item)
```

---

## ৬. List Comprehension বনাম map/filter

আগের লেসনে শিখেছি `map` ও `filter`। List comprehension এগুলোর বিকল্প হিসেবে কাজ করে এবং অনেকে বেশি readable মনে করে।

### map() → List Comprehension:

```python
numbers = [1, 2, 3, 4, 5]

# map দিয়ে
doubled_map = list(map(lambda x: x * 2, numbers))

# list comprehension দিয়ে
doubled_comp = [x * 2 for x in numbers]

print(doubled_map)    # [2, 4, 6, 8, 10]
print(doubled_comp)   # [2, 4, 6, 8, 10]
```

### filter() → List Comprehension:

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

---

## ৭. Dictionary Comprehension

List-এর মতো এক লাইনে dictionary তৈরি করা যায়।

### সিনট্যাক্স:

```python
{key_expression: value_expression for item in iterable}
```

### উদাহরণসমূহ:

```python
# সংখ্যা ও তার বর্গ
squares = {i: i ** 2 for i in range(1, 6)}
print(squares)
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# দুই list থেকে dict তৈরি
names = ["রহিম", "করিম", "সালাম"]
ages = [25, 30, 20]
people = {name: age for name, age in zip(names, ages)}
print(people)
# {'রহিম': 25, 'করিম': 30, 'সালাম': 20}

# list থেকে dict
words = ["hello", "world", "python"]
word_length = {word: len(word) for word in words}
print(word_length)
# {'hello': 5, 'world': 5, 'python': 6}
```

---

## ৮. Dictionary Comprehension এ Condition

### if সহ:

```python
numbers = {"a": 1, "b": 2, "c": 3, "d": 4}

# value ২ এর বেশি এমন items
big = {k: v for k, v in numbers.items() if v > 2}
print(big)
# {'c': 3, 'd': 4}

# জোড় value বাদ
odd = {k: v for k, v in numbers.items() if v % 2 != 0}
print(odd)
# {'a': 1, 'c': 3}
```

### if-else সহ:

```python
numbers = {"a": 1, "b": 2, "c": 3, "d": 4}

# value জোড় হলে "even", না হলে "odd"
labels = {k: ("even" if v % 2 == 0 else "odd") for k, v in numbers.items()}
print(labels)
# {'a': 'odd', 'b': 'even', 'c': 'odd', 'd': 'even'}
```

---

## ৯. Set Comprehension (বোনাস)

Dictionary-এর মতো set comprehension-ও আছে (কোনো key নেই, শুধু value)।

### সিনট্যাক্স:

```python
{expression for item in iterable}
```

### উদাহরণ:

```python
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 5]

# unique values (duplicate বাদ)
unique = {n for n in numbers}
print(unique)   # {1, 2, 3, 4, 5}

# unique even numbers
even_unique = {n for n in numbers if n % 2 == 0}
print(even_unique)   # {2, 4}
```

---

## ১০. ব্যবহারিক উদাহরণসমূহ

### উদাহরণ ১: বাক্সের ক্যাপিটাল লেটার

```python
names = ["রহিম", "করিম", "সালাম"]
upper_names = [name.upper() for name in names]
print(upper_names)
# ['রহিম', 'করিম', 'সালাম']  (বাংলায় কোনো প্রভাব নেই, ইংরেজিতে দেখুন)

words = ["hello", "world"]
upper = [w.upper() for w in words]
print(upper)
# ['HELLO', 'WORLD']
```

### উদাহরণ ২: ফ্ল্যাটেন করা

```python
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]
print(flat)   # [1, 2, 3, 4, 5, 6]
```

### উদাহরণ ৩: ফিল্টারিং ও ট্রান্সফর্ম একসাথে

```python
numbers = [1, -2, 3, -4, 5, -6, 7, -8]

# শুধু পজিটিভ সংখ্যা গুলোর বর্গ
result = [n ** 2 for n in numbers if n > 0]
print(result)   # [1, 9, 25, 49]
```

### উদাহরণ ৪: Dictionary এর key-value অদল-বদল

```python
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(swapped)
# {1: 'a', 2: 'b', 3: 'c'}
```

### উদাহরণ ৫: Common elements (উভয়ে আছে)

```python
list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]

common = [x for x in list1 if x in list2]
print(common)   # [4, 5]
```

---

## ১১. Practical Exercise

নিচের কোড রান করে দেখুন:

```python
# --- Exercise 1: List Comprehension মৌলিক ---
# ১ থেকে ১০ পর্যন্ত সংখ্যা
nums = [i for i in range(1, 11)]
print("১-১০:", nums)

# সব সংখ্যার ঘনফল
cubes = [i ** 3 for i in range(1, 6)]
print("ঘনফল:", cubes)   # [1, 8, 27, 64, 125]

# --- Exercise 2: Condition সহ ---
# শুধু ৩ দিয়ে বিভাজ্য সংখ্যা
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
div_by_3 = [n for n in nums if n % 3 == 0]
print("৩ দিয়ে বিভাজ্য:", div_by_3)   # [3, 6, 9, 12]

# --- Exercise 3: if-else সহ ---
# জোড় হলে সংখ্যাটা রাখুন, বিজোড় হলে -1
labels = [n if n % 2 == 0 else -1 for n in range(1, 11)]
print("লেবেল:", labels)
# [-1, 2, -1, 4, -1, 6, -1, 8, -1, 10]

# --- Exercise 4: Nested List Comprehension ---
# ৪x৪ identity matrix
identity = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
for row in identity:
    print(row)
# [1, 0, 0, 0]
# [0, 1, 0, 0]
# [0, 0, 1, 0]
# [0, 0, 0, 1]

# --- Exercise 5: Dictionary Comprehension ---
students = {"রহিম": 85, "করিম": 92, "সালাম": 78, "আব্দুল্লাহ": 95}

# ৯০+ পাওয়া ছাত্র
top = {name: marks for name, marks in students.items() if marks >= 90}
print("শীর্ষ:", top)
# {'করিম': 92, 'আব্দুল্লাহ': 95}

# গ্রেড দেওয়া
grades = {name: ("A+" if marks >= 90 else "A" if marks >= 80 else "B") 
          for name, marks in students.items()}
print("গ্রেড:", grades)
# {'রহিম': 'A', 'করিম': 'A+', 'সালাম': 'B', 'আব্দুল্লাহ': 'A+'}

# --- Exercise 6: Set Comprehension ---
names = ["রহিম", "করিম", "রহিম", "সালাম", "করিম"]
unique = {name for name in names}
print("Unique:", unique)
# {'রহিম', 'করিম', 'সালাম'}
```

---

## 🎯 আজকের Key Takeaways

1. **List Comprehension** — এক লাইনে list তৈরি করা: `[expr for item in iterable]`
2. **Condition সহ**: `[expr for item in iterable if condition]`
3. **if-else সহ**: `[expr1 if cond else expr2 for item in iterable]`
4. **Nested Comprehension** — একাধিক `for` loop
5. **Dictionary Comprehension**: `{k: v for item in iterable}`
6. **Set Comprehension**: `{expr for item in iterable}`
7. List comprehension `map`/`filter` এর বিকল্প, বেশি readable
8. জটিল লজিকের জন্য সাধারণ `for` loop ব্যবহার করা ভালো (readability জন্য)

---

## ❓ অনুশীলনী প্রশ্ন

1. List comprehension দিয়ে ১ থেকে ২০ পর্যন্ত সব জোড় সংখ্যার list বানান
2. `[1, 2, 3, 4, 5]` থেকে list comprehension দিয়ে সব সংখ্যার ঘনফল বের করুন
3. Dictionary comprehension দিয়ে `{"a": 1, "b": 2, "c": 3}` এর key-value অদল-বদল করুন
4. `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` থেকে শুধু ৩ দিয়ে বিভাজ্য সংখ্যাগুলোর বর্গ বের করুন
5. List comprehension দিয়ে `[[1,2],[3,4],[5,6]]` nested list-কে flat করুন
6. Dictionary comprehension দিয়ে `["apple", "banana", "cherry"]` list থেকে `{"apple": 5, ...}` এমন একটা dict বানান যেখানে value হবে word-এর দৈর্ঘ্য
