# Python: Operators ➕➖

**Operator** হলো এমন কিছু চিহ্ন যা দুই বা ততোধিক operand (মান/ভেরিয়েবল) এর উপর কিছু অপারেশন সম্পন্ন করে। Python-এ বিভিন্ন ধরনের operator আছে।

---

## ১. Arithmetic Operators (গাণিতিক অপারেটর)

সাধারণ গাণিতিক অপারেশনের জন্য এই অপারেটরগুলো ব্যবহার হয়।

| অপারেটর | মানে | উদাহরণ | ফলাফল |
|----------|------|--------|--------|
| `+` | যোগ | `5 + 3` | `8` |
| `-` | বিয়োগ | `5 - 3` | `2` |
| `*` | গুণ | `5 * 3` | `15` |
| `/` | ভাগ (float ফলাফল) | `5 / 2` | `2.5` |
| `//` | ভাগ (integer ফলাফল) | `5 // 2` | `2` |
| `%` | মডুলো (ভাগশেষ) | `5 % 2` | `1` |
| `**` | পাওয়ার (ঘাত) | `2 ** 3` | `8` |

### উদাহরণ:

```python
a = 10
b = 3

print(a + b)    # 13
print(a - b)    # 7
print(a * b)    # 30
print(a / b)    # 3.333...
print(a // b)   # 3  (floor division)
print(a % b)    # 1  (ভাগশেষ)
print(a ** b)   # 1000  (10^3)
```

### `//` (Floor Division) বিস্তারিত:

`//` দিয়ে ভাগ করলে দশমিক অংশ বাদ যায় এবং সবচেয়ে ছোট integer দেয়:

```python
print(7 // 2)     # 3
print(-7 // 2)    # -4  (নেগেটিভে সাবধান!)
print(7 // -2)    # -4
```

### `%` (Modulus) বিস্তারিত:

ভাগশেষ বের করতে `%` ব্যবহার হয়। বিজোড়/জোড় চেক করতে খুব দরকারী:

```python
print(10 % 3)    # 1
print(10 % 2)    # 0  (জোড় সংখ্যা)
print(7 % 2)     # 1  (বিজোড় সংখ্যা)

# বিজোড় জোড় চেক
num = 7
if num % 2 == 0:
    print("জোড়")
else:
    print("বিজোড়")
# আউটপুট: বিজোড়
```

---

## ২. Assignment Operators (অ্যাসাইনমেন্ট অপারেটর)

ভেরিয়েবলে মান assign করতে এই অপারেটরগুলো ব্যবহার হয়।

| অপারেটর | সমতুল | উদাহরণ |
|----------|--------|--------|
| `=` | সরাসরি অ্যাসাইন | `x = 5` |
| `+=` | `x = x + y` | `x += 3` |
| `-=` | `x = x - y` | `x -= 3` |
| `*=` | `x = x * y` | `x *= 3` |
| `/=` | `x = x / y` | `x /= 3` |
| `//=` | `x = x // y` | `x //= 3` |
| `%=` | `x = x % y` | `x %= 3` |
| `**=` | `x = x ** y` | `x **= 3` |

### উদাহরণ:

```python
x = 10
print(x)    # 10

x += 5      # x = x + 5
print(x)    # 15

x -= 3      # x = x - 3
print(x)    # 12

x *= 2      # x = x * 2
print(x)    # 24

x /= 4      # x = x / 4
print(x)    # 6.0

x **= 2     # x = x ** 2
print(x)    # 36.0
```

---

## ৩. Comparison Operators (তুলনা অপারেটর)

দুই মান তুলনা করতে এই অপারেটরগুলো ব্যবহার হয়। ফলাফল সবসময় `True` বা `False` হয়।

| অপারেটর | মানে | উদাহরণ | ফলাফল |
|----------|------|--------|--------|
| `==` | সমান | `5 == 5` | `True` |
| `!=` | সমান নয় | `5 != 3` | `True` |
| `>` | বড় | `5 > 3` | `True` |
| `<` | ছোট | `5 < 3` | `False` |
| `>=` | বড় বা সমান | `5 >= 5` | `True` |
| `<=` | ছোট বা সমান | `5 <= 3` | `False` |

### উদাহরণ:

```python
a = 10
b = 20

print(a == b)   # False
print(a != b)   # True
print(a > b)    # False
print(a < b)    # True
print(a >= 10)  # True
print(a <= 10)  # True
```

### ⚠️ সাবধান! `=` বনাম `==`:
- `=` — মান assign করা
- `==` — তুলনা করা

```python
x = 5        # x-এ 5 assign করা হয়েছে
x == 5       # x, 5 এর সমান কিনা চেক হচ্ছে → True
```

---

## ৪. Logical Operators (লজিক্যাল অপারেটর)

একাধিক শর্ত একসাথে চেক করতে এই অপারেটরগুলো ব্যবহার হয়।

| অপারেটর | মানে | উদাহরণ |
|----------|------|--------|
| `and` | দুটোই সত্য হতে হবে | `a and b` |
| `or` | যেকোনো একটা সত্য হলেই | `a or b` |
| `not` | উল্টো করে দেয় | `not a` |

### `and` টেবিল:

| A | B | A `and` B |
|---|---|-----------|
| True | True | True |
| True | False | False |
| False | True | False |
| False | False | False |

### `or` টেবিল:

| A | B | A `or` B |
|---|---|----------|
| True | True | True |
| True | False | True |
| False | True | True |
| False | False | False |

### `not` টেবিল:

| A | `not` A |
|---|---------|
| True | False |
| False | True |

### উদাহরণ:

```python
age = 25
has_id = True

# and — দুটোই সত্য হতে হবে
if age >= 18 and has_id:
    print("ভোট দিতে পারবেন")
# আউটপুট: ভোট দিতে পারবেন

# or — যেকোনো একটা সত্য হলেই
is_student = True
is_teacher = False
if is_student or is_teacher:
    print("শিক্ষা প্রতিষ্ঠানের সদস্য")
# আউটপুট: শিক্ষা প্রতিষ্ঠানের সদস্য

# not — উল্টো
is_logged_in = False
if not is_logged_in:
    print("লগইন করুন")
# আউটপুট: লগইন করুন
```

### জটিল শর্ত:

```python
age = 25
has_ticket = True
is_member = False

if (age >= 18 and has_ticket) or is_member:
    print("ভেতরে যেতে পারবেন")
```

---

## ৫. Identity Operators (আইডেন্টিটি অপারেটর)

দুই object একই কিনা (মেমরিতে একই জায়গায় আছে কিনা) চেক করতে `is` ও `is not` ব্যবহার হয়।

| অপারেটর | মানে |
|----------|------|
| `is` | একই object |
| `is not` | একই object নয় |

### উদাহরণ:

```python
x = [1, 2, 3]
y = [1, 2, 3]
z = x

print(x is y)        # False — মান সমান হলেও আলাদা object
print(x is z)        # True — একই object

print(x == y)        # True — মান সমান
print(x is y)        # False — object আলাদা

# None চেক করার জন্য সবচেয়ে ভালো
value = None
if value is None:
    print("মান নেই")
```

⚠️ **গুরুত্বপূর্ণ:** `==` মান তুলনা করে, `is` মেমরি address তুলনা করে।

---

## ৬. Membership Operators (মেম্বারশিপ অপারেটর)

কোনো মান কোনো সিকোয়েন্স (list, string, tuple) এর মধ্যে আছে কিনা চেক করতে `in` ও `not in` ব্যবহার হয়।

| অপারেটর | মানে |
|----------|------|
| `in` | মধ্যে আছে |
| `not in` | মধ্যে নেই |

### উদাহরণ:

```python
fruits = ["আপেল", "কমলা", "কলা"]

print("আপেল" in fruits)       # True
print("আম" in fruits)         # False
print("আম" not in fruits)     # True

# String-এর মধ্যে
name = "Python"
print("P" in name)            # True
print("z" in name)            # False

# Dictionary-এর মধ্যে (key চেক হয়)
person = {"name": "রহিম", "age": 25}
print("name" in person)       # True
print("রহিম" in person)       # False (কারণ value চেক হয় না, key চেক হয়)
```

---

## ৭. Bitwise Operators (বিটওয়াইজ অপারেটর)

বাইনারি (binary) স্তরে অপারেশন করার জন্য এই অপারেটরগুলো ব্যবহার হয়। সাধারণত কম ব্যবহার হয়।

| অপারেটর | মানে | উদাহরণ |
|----------|------|--------|
| `&` | AND | `5 & 3` → `1` |
| `\|` | OR | `5 \| 3` → `7` |
| `^` | XOR | `5 ^ 3` → `6` |
| `~` | NOT | `~5` → `-6` |
| `<<` | Left Shift | `5 << 1` → `10` |
| `>>` | Right Shift | `5 >> 1` → `2` |

### উদাহরণ:

```python
a = 5    # binary: 0101
b = 3    # binary: 0011

print(a & b)     # 1  (0001)
print(a | b)     # 7  (0111)
print(a ^ b)     # 6  (0110)
print(~a)        # -6
print(a << 1)    # 10 (01010 — বামে ১ বিট সরানো)
print(a >> 1)    # 2  (0010 — ডানে ১ বিট সরানো)
```

---

## ৮. Operator Precedence (অপারেটরের অগ্রাধিকার)

একাধিক operator একসাথে থাকলে কোনটা আগে কাজ করবে তা নির্ধারণ করে precedence।

**উচ্চ থেকে নিম্ন ক্রম:**

| অগ্রাধিকার | অপারেটর | বিবরণ |
|------------|----------|--------|
| 1 | `()` | বন্ধনী |
| 2 | `**` | পাওয়ার |
| 3 | `+x`, `-x`, `~x` | ইউনারি |
| 4 | `*`, `/`, `//`, `%` | গুণ, ভাগ |
| 5 | `+`, `-` | যোগ, বিয়োগ |
| 6 | `<<`, `>>` | শিফট |
| 7 | `&` | Bitwise AND |
| 8 | `^` | Bitwise XOR |
| 9 | `\|` | Bitwise OR |
| 10 | `==`, `!=`, `<`, `>`, `<=`, `>=`, `is`, `in` | তুলনা |
| 11 | `not` | Logical NOT |
| 12 | `and` | Logical AND |
| 13 | `or` | Logical OR |

### উদাহরণ:

```python
# গুণ আগে, তারপর যোগ
print(2 + 3 * 4)       # 14 (2 + 12), না 20

# বন্ধনী আগে
print((2 + 3) * 4)     # 20

# পাওয়ার আগে
print(2 ** 3 * 2)      # 16 (8 * 2)
print(2 ** (3 * 2))    # 64 (2^6)
```

---

## ৯. Practical Exercise

নিচের কোড রান করে দেখুন:

```python
# --- Exercise 1: Arithmetic ---
a = 15
b = 4

print(f"যোগ: {a + b}")        # 19
print(f"বিয়োগ: {a - b}")     # 11
print(f"গুণ: {a * b}")        # 60
print(f"ভাগ: {a / b}")        # 3.75
print(f"Floor ভাগ: {a // b}") # 3
print(f"ভাগশেষ: {a % b}")     # 3
print(f"পাওয়ার: {a ** 2}")   # 225

# --- Exercise 2: Assignment ---
x = 10
x += 5    # 15
x *= 2    # 30
x -= 10   # 20
print(f"x = {x}")   # 20

# --- Exercise 3: Comparison ---
age = 20
print(f"বয়স ১৮+? {age >= 18}")     # True
print(f"বয়স ২১? {age == 21}")      # False
print(f"বয়স ৩০ নয়? {age != 30}")  # True

# --- Exercise 4: Logical ---
has_license = True
age = 20

if age >= 18 and has_license:
    print("গাড়ি চালাতে পারবেন")

is_student = True
age = 15
if is_student or age >= 18:
    print("ডিসকাউন্ট পাবেন")

# --- Exercise 5: Membership ---
name = "PythonProgramming"
if "Python" in name:
    print("Python আছে")

fruits = ["আপেল", "কমলা", "কলা"]
if "আম" not in fruits:
    print("আম নেই")

# --- Exercise 6: Precedence ---
print(2 + 3 * 4)           # 14
print((2 + 3) * 4)         # 20
print(10 - 2 * 3 + 1)      # 5
print(2 ** 3 ** 2)         # 512 (2^9, right to left)
```

---

## 🎯 আজকের Key Takeaways

1. **Arithmetic**: `+`, `-`, `*`, `/`, `//`, `%`, `**`
2. **Assignment**: `=`, `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`
3. **Comparison**: `==`, `!=`, `>`, `<`, `>=`, `<=`
4. **Logical**: `and`, `or`, `not`
5. **Identity**: `is`, `is not` — মেমরি address তুলনা
6. **Membership**: `in`, `not in` — সিকোয়েন্সে আছে কিনা
7. **Bitwise**: `&`, `|`, `^`, `~`, `<<`, `>>`
8. **Precedence**: বন্ধনী `()` সবচেয়ে আগে কাজ করে
9. `==` মান তুলনা করে, `is` মেমরি address তুলনা করে

---

## ❓ অনুশীলনী প্রশ্ন

1. `10 // 3` এবং `10 / 3` এর মধ্যে পার্থক্য কী?
2. `7 % 2` এর মান কী এবং কেন?
3. `=` এবং `==` এর পার্থক্য কী?
4. `3 ** 2 ** 2` এর মান কী হবে?
5. একটা সংখ্যা বিজোড় নাকি জোড় সেটা কীভাবে চেক করবেন?
6. `x = [1, 2]`, `y = [1, 2]` — `x == y` এবং `x is y` এর মান কী কী হবে এবং কেন?
7. `5 > 3 and 2 < 1` — ফলাফল কী হবে?
