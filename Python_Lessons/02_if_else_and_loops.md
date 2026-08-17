# Python: if/else & Loops 🔀

Python-এর সবচেয়ে গুরুত্বপূর্ণ অংশ — **if/else** (শর্ত অনুযায়ী কাজ করা) এবং **loops** (একই কাজ বারবার করা)। এগুলো ছাড়া কোনো প্রোগ্রাম কল্পনা করা যায় না।

---

## ১. if Statement (শর্ত চেক করা)

`if` দিয়ে আমরা একটা শর্ত চেক করি। শর্ত **সত্য (True)** হলে if-এর ভেতরের কোড চলে, না হলে চলে না।

### সিনট্যাক্স:

```python
if শর্ত:
    # শর্ত সত্য হলে এই কোড চলবে
    print("শর্ত সত্য")
```

### উদাহরণ:

```python
age = 18

if age >= 18:
    print("আপনি ভোট দিতে পারবেন")
```

---

## ২. if...else (দুই পথ)

যখন দুটো সম্ভাবনা থাকে — শর্ত সত্য হলে এক কাজ, মিথ্যা হলে অন্য কাজ:

```python
age = 15

if age >= 18:
    print("আপনি ভোট দিতে পারবেন")
else:
    print("আপনি এখনো ছোট, ভোট দিতে পারবেন না")
```

---

## ৩. if...elif...else (একাধিক শর্ত)

একাধিক শর্ত চেক করতে `elif` (else if) ব্যবহার করুন:

```python
marks = 75

if marks >= 80:
    print("A+")
elif marks >= 70:
    print("A")
elif marks >= 60:
    print("B")
else:
    print("F")

# আউটপুট: A  (কারণ 75 >= 70)
```

### 🔑 গুরুত্বপূর্ণ নিয়ম:
- `if` দিয়ে শুরু করতে হবে
- `elif` যত খুশি ব্যবহার করতে পারেন
- `else` শেষে একবার বসে (ঐচ্ছিক)
- Python **indentation** (indent) মেনে চলে — `if`-এর ভেতরের কোড 4 space দিয়ে indent করতে হয়

---

## ৪. Comparison Operators (তুলনা অপারেটর)

`if`-এর শর্তে এগুলো ব্যবহার হয়:

| অপারেটর | মানে | উদাহরণ |
|----------|------|--------|
| `==` | সমান | `x == 5` |
| `!=` | সমান নয় | `x != 5` |
| `>` | বড় | `x > 5` |
| `<` | ছোট | `x < 5` |
| `>=` | বড় বা সমান | `x >= 5` |
| `<=` | ছোট বা সমান | `x <= 5` |

### উদাহরণ:

```python
age = 20

print(age == 20)   # True
print(age != 20)   # False
print(age > 18)    # True
print(age <= 18)   # False
```

---

## ৫. Logical Operators (লজিক্যাল অপারেটর)

একাধিক শর্ত একসাথে চেক করতে:

| অপারেটর | মানে | উদাহরণ |
|----------|------|--------|
| `and` | দুটোই সত্য হতে হবে | `age >= 18 and has_id == True` |
| `or` | যেকোনো একটা সত্য হলেই | `age < 18 or age > 60` |
| `not` | উল্টো করে দেয় | `not is_logged_in` |

### উদাহরণ:

```python
age = 25
has_id = True

if age >= 18 and has_id:
    print("আপনি ভোট দিতে পারবেন")
else:
    print("ভোট দিতে পারবেন না")

# আউটপুট: আপনি ভোট দিতে পারবেন
```

---

## ৬. for Loop (পুনরাবৃত্তি)

`for` loop দিয়ে একটা সিকোয়েন্স (list, string, range) এর প্রতিটা উপাদান দিয়ে একই কাজ বারবার করা যায়।

### সিনট্যাক্স:

```python
for variable in sequence:
    # প্রতিটা উপাদানের জন্য এই কোড চলবে
    print(variable)
```

### উদাহরণ ১: List দিয়ে

```python
fruits = ["আপেল", "কমলা", "কলা"]

for fruit in fruits:
    print(fruit)

# আউটপুট:
# আপেল
# কমলা
# কলা
```

### উদাহরণ ২: range() দিয়ে

`range(n)` — 0 থেকে n-1 পর্যন্ত সংখ্যা দেয়:

```python
for i in range(5):
    print(i)

# আউটপুট:
# 0
# 1
# 2
# 3
# 4
```

`range(start, stop, step)` — নির্দিষ্ট রেঞ্জ:

```python
for i in range(1, 11, 2):   # 1 থেকে 10 পর্যন্ত, 2 করে বাড়ে
    print(i)

# আউটপুট:
# 1
# 3
# 5
# 7
# 9
```

### উদাহরণ ৩: String দিয়ে

```python
name = "Python"

for char in name:
    print(char)

# আউটপুট:
# P
# y
# t
# h
# o
# n
```

---

## ৭. while Loop

`while` loop যতক্ষণ শর্ত সত্য থাকে, ততক্ষণ চলতে থাকে:

```python
count = 1

while count <= 5:
    print(count)
    count += 1    # count = count + 1

# আউটপুট:
# 1
# 2
# 3
# 4
# 5
```

### ⚠️ সাবধান! Infinite Loop
শর্ত কখনো False না হলে loop চিরকাল চলতে থাকবে!

```python
# ❌ ভুল — infinite loop
count = 1
while count <= 5:
    print(count)
    # count বাড়ানো হয়নি! তাই কখনো থামবে না
```

---

## ৮. break ও continue

### `break` — loop থেকে বের হয়ে যাওয়া

```python
for i in range(10):
    if i == 5:
        break       # 5 এ গেলে loop থেকে বের হয়ে যাবে
    print(i)

# আউটপুট: 0 1 2 3 4
```

### `continue` — এই ধাপ বাদ দিয়ে পরের ধাপে যাওয়া

```python
for i in range(5):
    if i == 2:
        continue    # 2 বাদ যাবে, পরের ধাপে চলে যাবে
    print(i)

# আউটপুট: 0 1 3 4
```

---

## ৯. Nested (ভেতরের) if/else ও loop

`if`-এর ভেতরে `if` অথবা loop-এর ভেতরে loop রাখা যায়:

```python
# Nested if
age = 20
has_ticket = True

if age >= 18:
    if has_ticket:
        print("ভেতরে যেতে পারবেন")
    else:
        print("টিকেট কিনুন")
else:
    print("বয়স কম")

# Nested loop — প্যাটার্ন প্রিন্ট
for i in range(3):
    for j in range(3):
        print("*", end=" ")
    print()   # নতুন লাইন

# আউটপুট:
# * * *
# * * *
# * * *
```

---

## ১০. Practical Exercise

নিচের কোড রান করে দেখুন:

```python
# --- Exercise 1: if/elif/else ---
score = int(input("আপনার স্কোর দিন: "))

if score >= 90:
    print("গ্রেড: A+")
elif score >= 80:
    print("গ্রেড: A")
elif score >= 70:
    print("গ্রেড: B")
elif score >= 60:
    print("গ্রেড: C")
else:
    print("গ্রেড: F")

# --- Exercise 2: for loop দিয়ে ১ থেকে ১০ পর্যন্ত যোগফল ---
total = 0
for i in range(1, 11):
    total += i
print("১ থেকে ১০ যোগফল:", total)   # 55

# --- Exercise 3: while loop দিয়ে countdown ---
num = 5
while num > 0:
    print(num)
    num -= 1
print("বাকসাদ! 🎉")

# --- Exercise 4: break ও continue ---
for i in range(1, 11):
    if i % 2 == 0:
        continue    # জোড় সংখ্যা বাদ
    print(i)         # শুধু বিজোড় সংখ্যা প্রিন্ট হবে
```

---

## 🎯 আজকের Key Takeaways

1. **if/elif/else** — শর্ত অনুযায়ী আলাদা আলাদা কাজ করানো
2. **Comparison operators**: `==`, `!=`, `>`, `<`, `>=`, `<=`
3. **Logical operators**: `and`, `or`, `not`
4. **for loop** — list/string/range দিয়ে পুনরাবৃত্তি
5. **while loop** — শর্ত সত্য থাকা পর্যন্ত চলে
6. **break** — loop থেকে বের হয়ে যাওয়া
7. **continue** — এই ধাপ বাদ দেওয়া
8. **Indentation** খুবই গুরুত্বপূর্ণ — ভুল করলে error হবে

---

## ❓ অনুশীলনী প্রশ্ন

1. `for i in range(2, 8, 2)` — কী কী প্রিন্ট হবে?
2. `while` এবং `for` loop-এর পার্থক্য কী?
3. `break` আর `continue`-এর পার্থক্য কী?
4. ১ থেকে ১০০ পর্যন্ত সব বিজোড় সংখ্যা প্রিন্ট করুন (for loop দিয়ে)
5. ১ থেকে ১০০ পর্যন্ত সব সংখ্যার যোগফল বের করুন
