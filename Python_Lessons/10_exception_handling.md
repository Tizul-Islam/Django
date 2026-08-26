# Python: Exception Handling (try/except) ⚠️

**Exception** হলো এমন একটা error যা প্রোগ্রাম চলার সময় ঘটে এবং প্রোগ্রামকে crash করে দেয়। **Exception Handling** দিয়ে এই errors গুলো সুন্দরভাবে হ্যান্ডেল করা যায় এবং প্রোগ্রামকে চালু রাখা যায়।

---

## ১. Exception কী এবং কেন দরকার?

কিছু কমন error যা প্রোগ্রামকে crash করে:

```python
# ১. ZeroDivisionError - শূন্য দিয়ে ভাগ
print(10 / 0)   # ❌ Error!

# ২. ValueError - ভুল টাইপের মান
int("hello")    # ❌ Error!

# ৩. IndexError - list-এর বাইরে index
nums = [1, 2, 3]
print(nums[5])  # ❌ Error!

# ৪. KeyError - dict-এ নেই এমন key
d = {"name": "রহিম"}
print(d["age"]) # ❌ Error!

# ৫. TypeError - ভুল টাইপের অপারেশন
print("5" + 5)  # ❌ Error!
```

এই errors গুলো হ্যান্ডেল না করলে প্রোগ্রাম সম্পূর্ণ বন্ধ হয়ে যাবে। Exception Handling দিয়ে আমরা error হয়েছে বুঝিয়ে সুন্দর মেসেজ দিতে পারি।

---

## ২. try-except — বেসিক স্ট্রাকচার

### সিনট্যাক্স:

```python
try:
    # যে কোডে error হতে পারে
    risky_code()
except:
    # error হলে এই কোড চলবে
    print("কিছু সমস্যা হয়েছে")
```

### উদাহরণ:

```python
try:
    num = int(input("একটা সংখ্যা দিন: "))
    result = 10 / num
    print(f"ফলাফল: {result}")
except:
    print("দুঃখিত, একটি সঠিক সংখ্যা দিন (শূন্য ছাড়া)!")

# ইনপুট: ২ → ফলাফল: 5.0
# ইনপুট: ০ → দুঃখিত, একটি সঠিক সংখ্যা দিন (শূন্য ছাড়া)!
# ইনপুট: "abc" → দুঃখিত, একটি সঠিক সংখ্যা দিন (শূন্য ছাড়া)!
```

---

## ৩. নির্দিষ্ট Exception ধরা

সাধারণ `except` সব error ধরে। ভালো প্রাকটিস হলো নির্দিষ্ট error ধরা।

### কিছু কমন Exception:

| Exception | কখন হয় |
|-----------|---------|
| `ZeroDivisionError` | শূন্য দিয়ে ভাগ |
| `ValueError` | ভুল মান/টাইপ |
| `TypeError` | ভুল টাইপের অপারেশন |
| `IndexError` | list-এর বাইরে index |
| `KeyError` | dict-এ নেই এমন key |
| `FileNotFoundError` | ফাইল পাওয়া যায়নি |
| `ImportError` | module import সমস্যা |
| `AttributeError` | object-এ নেই এমন attribute |
| `NameError` | define না করা variable |
| `OverflowError` | খুব বড় সংখ্যা |

### উদাহরণ:

```python
try:
    num = int(input("একটা সংখ্যা দিন: "))
    result = 10 / num
    print(f"ফলাফল: {result}")
except ZeroDivisionError:
    print("শূন্য দিয়ে ভাগ করা যায় না!")
except ValueError:
    print("অনুগ্রহ করে একটি সংখ্যা লিখুন!")
```

---

## ৪. একাধিক except

একাধিক ধরনের error আলাদাভাবে হ্যান্ডেল করা যায়:

```python
try:
    num = int(input("একটা সংখ্যা দিন: "))
    result = 10 / num
    print(f"ফলাফল: {result}")

    my_list = [1, 2, 3]
    print(my_list[num])

except ZeroDivisionError:
    print("শূন্য দিয়ে ভাগ করা যায় না!")
except ValueError:
    print("অনুগ্রহ করে একটি সংখ্যা লিখুন!")
except IndexError:
    print("ভুল index! list-এর বাইরে যাচ্ছেন।")
except Exception as e:
    print(f"অন্য কোনো সমস্যা: {e}")
```

⚠️ `Exception` সব error-এর base class, তাই এটা সবসময় **শেষে** রাখতে হয়।

---

## ৫. Exception এর মেসেজ ধরা

`as` দিয়ে error-এর মেসেজ ধরা যায়:

```python
try:
    int("hello")
except ValueError as e:
    print(f"Error হয়েছে: {e}")
    print(f"Error টাইপ: {type(e).__name__}")

# আউটপুট:
# Error হয়েছে: invalid literal for int() with base 10: 'hello'
# Error টাইপ: ValueError
```

---

## ৬. try-except-else

`else` ব্লকে সেই কোড থাকে যা শুধুমাত্র error না হলে চলে:

```python
try:
    num = int(input("একটা সংখ্যা দিন: "))
except ValueError:
    print("অনুগ্রহ করে একটি সংখ্যা লিখুন!")
else:
    # error না হলে এই ব্লক চলবে
    print(f"আপনি {num} লিখেছেন")
    print(f"বর্গ: {num ** 2}")
```

### try-except-else ফ্লো:

```
try → success → else
try → error → except (else চলবে না)
```

---

## ৭. try-except-finally

`finally` ব্লক সবসময় চলে — error হোক বা না হোক। মূলত ক্লিনআপের জন্য ব্যবহৃত হয়।

```python
try:
    file = open("example.txt", "r")
    content = file.read()
    print(content)
except FileNotFoundError:
    print("ফাইলটা পাওয়া যায়নি!")
finally:
    file.close()  # error হোক না হোক ফাইল বন্ধ হবে
    print("কাজ শেষ হয়েছে")
```

### try-except-else-finally সব একসাথে:

```python
try:
    num = int(input("একটা সংখ্যা দিন: "))
    result = 10 / num
except ValueError:
    print("ভুল সংখ্যা!")
except ZeroDivisionError:
    print("শূন্য দিয়ে ভাগ করা যায় না!")
else:
    print(f"ফলাফল: {result}")
finally:
    print("প্রোগ্রাম শেষ হলো")
```

### ফ্লো চার্ট:

```
try:
    risky code
except ErrorType:
    error হলে
else:
    error না হলে
finally:
    সবসময় চলে
```

---

## ৮. নিজের Exception তৈরি করা — `raise`

`raise` দিয়ে ইচ্ছেমতো exception তৈরি করা যায়:

```python
age = -5

if age < 0:
    raise ValueError("বয়স ঋণাত্মক হতে পারে না!")

# ❌ ValueError: বয়স ঋণাত্মক হতে পারে না!
```

### Function-এ raise:

```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("শূন্য দিয়ে ভাগ করা যায় না!")
    return a / b

try:
    result = divide(10, 0)
except ZeroDivisionError as e:
    print(f"সমস্যা: {e}")
```

### Custom Exception (নিজের Exception class):

```python
class InvalidAgeError(Exception):
    """বয়স সঠিক না হলে এই exception"""
    pass

def check_age(age):
    if age < 0:
        raise InvalidAgeError("বয়স ঋণাত্মক হতে পারে না!")
    if age > 150:
        raise InvalidAgeError("বয়স ১৫০ এর বেশি হতে পারে না!")
    return "বয়স সঠিক"

try:
    print(check_age(200))
except InvalidAgeError as e:
    print(f"সমস্যা: {e}")
# আউটপুট: সমস্যা: বয়স ১৫০ এর বেশি হতে পারে না!
```

---

## ৯. Nested try-except

একটা try-except আরেকটার ভেতরে থাকতে পারে:

```python
try:
    try:
        num = int(input("সংখ্যা দিন: "))
        print(10 / num)
    except ValueError:
        print("ভুল সংখ্যা!")
except Exception:
    print("বাইরের try-এ error")
```

---

## ১০. কিছু ব্যবহারিক উদাহরণ

### উদাহরণ ১: ইনপুট ভ্যালিডেশন

```python
while True:
    try:
        age = int(input("আপনার বয়স দিন: "))
        if age < 0:
            raise ValueError("বয়স ঋণাত্মক হতে পারে না")
        break
    except ValueError as e:
        print(f"ভুল ইনপুট! {e}")

print(f"আপনার বয়স: {age}")
```

### উদাহরণ ২: ফাইল হ্যান্ডেলিং

```python
filename = input("ফাইলের নাম দিন: ")

try:
    with open(filename, "r") as f:
        content = f.read()
        print(content)
except FileNotFoundError:
    print(f"'{filename}' ফাইলটা পাওয়া যায়নি!")
except PermissionError:
    print(f"'{filename}' ফাইল পড়ার অনুমতি নেই!")
except Exception as e:
    print(f"অন্য সমস্যা: {e}")
```

### উদাহরণ ৩: লিস্ট অপারেশন

```python
def get_element(lst, index):
    try:
        return lst[index]
    except IndexError:
        return None
    except TypeError:
        return None

my_list = [10, 20, 30]
print(get_element(my_list, 1))   # 20
print(get_element(my_list, 10))  # None
print(get_element(my_list, "a")) # None
```

### উদাহরণ ৪: ডিকশনারি হ্যান্ডেলিং

```python
person = {"নাম": "রহিম", "বয়স": 25}

keys = ["নাম", "বয়স", "শহর", "পেশা"]

for key in keys:
    try:
        print(f"{key}: {person[key]}")
    except KeyError:
        print(f"{key}: তথ্য নেই")
```

### উদাহরণ ৫: ডিভিশন ক্যালকুলেটর

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "শূন্য দিয়ে ভাগ করা যায় না"
    except TypeError:
        return "সংখ্যা দিন"

print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # শূন্য দিয়ে ভাগ করা যায় না
print(safe_divide(10, "2"))  # সংখ্যা দিন
```

---

## ১১. Practical Exercise

```python
# ============ Exercise 1: বেসিক try-except ============
print("=== Exercise 1 ===")
try:
    num = int(input("একটা সংখ্যা দিন: "))
    print(f"বর্গ: {num ** 2}")
except ValueError:
    print("অনুগ্রহ করে একটি সংখ্যা লিখুন!")

# ============ Exercise 2: একাধিক except ============
print("\n=== Exercise 2 ===")
try:
    num1 = int(input("প্রথম সংখ্যা: "))
    num2 = int(input("দ্বিতীয় সংখ্যা: "))
    result = num1 / num2
    print(f"ফলাফল: {result}")
except ValueError:
    print("সংখ্যা লিখুন!")
except ZeroDivisionError:
    print("শূন্য দিয়ে ভাগ করা যায় না!")

# ============ Exercise 3: try-except-else-finally ============
print("\n=== Exercise 3 ===")
try:
    age = int(input("বয়স দিন: "))
except ValueError:
    print("ভুল বয়স!")
else:
    print(f"আপনি {age} বছরের")
    if age >= 18:
        print("ভোট দিতে পারবেন")
finally:
    print("প্রোগ্রাম শেষ হলো")

# ============ Exercise 4: raise ============
print("\n=== Exercise 4 ===")
def check_positive(num):
    if num <= 0:
        raise ValueError("সংখ্যা পজিটিভ হতে হবে!")
    return num

try:
    print(check_positive(5))
    print(check_positive(-3))
except ValueError as e:
    print(f"সমস্যা: {e}")

# ============ Exercise 5: Custom Exception ============
print("\n=== Exercise 5 ===")
class InsufficientBalanceError(Exception):
    pass

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientBalanceError(
                f"পর্যাপ্ত টাকা নেই! ব্যালেন্স: {self.balance}, চেয়েছেন: {amount}"
            )
        self.balance -= amount
        return self.balance

account = BankAccount(1000)
try:
    print(f"নতুন ব্যালেন্স: {account.withdraw(500)}")
    print(f"নতুন ব্যালেন্স: {account.withdraw(700)}")
except InsufficientBalanceError as e:
    print(f"সমস্যা: {e}")

# ============ Exercise 6: ফাইল হ্যান্ডেলিং ============
print("\n=== Exercise 6 ===")
filename = input("ফাইলের নাম দিন: ")
try:
    with open(filename, "r") as f:
        lines = f.readlines()
        print(f"মোট লাইন: {len(lines)}")
except FileNotFoundError:
    print(f"'{filename}' ফাইল পাওয়া যায়নি!")
except Exception as e:
    print(f"সমস্যা: {e}")
```

---

## 🎯 আজকের Key Takeaways

1. **Exception** = runtime error যা প্রোগ্রাম crash করে
2. `try-except` — error হ্যান্ডেল করার মূল উপায়
3. নির্দিষ্ট Exception ধরা ভালো প্রাকটিস (সাধারণ `except` নয়)
4. `else` — error না হলে চলে
5. `finally` — সবসময় চলে (ক্লিনআপের জন্য)
6. `raise` — নিজের মতো exception তৈরি করা
7. Custom Exception — `class MyError(Exception)` দিয়ে তৈরি
8. `Exception as e` — error মেসেজ ধরা
9. `Exception` base class সবসময় শেষে রাখতে হয়
10. File, input, network — সব জায়গায় exception handling দরকার

---

## ❓ অনুশীলনী প্রশ্ন

1. `try`, `except`, `else`, `finally` এর কাজ কী?
2. `ZeroDivisionError` কখন হয়? একটা উদাহরণ দিন
3. `ValueError` এবং `TypeError` এর পার্থক্য কী?
4. নিজের একটা custom exception class তৈরি করুন
5. একটা function লিখুন যা দুই সংখ্যা ভাগ করবে, কিন্তু শূন্য দিয়ে ভাগ করলে error দেবে না
6. একটা ফাইল খোলার কোড লিখুন যা `FileNotFoundError` হ্যান্ডেল করবে
7. `raise` কীভাবে কাজ করে? উদাহরণ সহ বলুন
