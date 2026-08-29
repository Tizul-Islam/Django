# Python: Constructor (__init__) 🏗️

**Constructor** হলো একটা বিশেষ method যা কোনো object তৈরি হওয়ার সময় স্বয়ংক্রিয়ভাবে চলে। Python-এ constructor হলো `__init__` method। এটা object-এর attribute গুলো সেট করার জন্য ব্যবহৃত হয়।

---

## ১. Constructor কী এবং কেন দরকার?

কোনো object তৈরি হওয়ার সময় যদি কিছু attribute সেট করতে হয়, তাহলে constructor ব্যবহার করা হয়। এটা object-এর জন্য প্রাথমিক সেটআপ করে।

**ছাড়া Constructor কেমন হতো:**

```python
class Person:
    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

p = Person()
p.set_name("রহিম")   # আলাদাভাবে কল করতে হচ্ছে
p.set_age(25)
```

**Constructor দিয়ে:**

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("রহিম", 25)   # এক লাইনে সব সেট
print(p.name, p.age)   # রহিম 25
```

---

## ২. `__init__` মেথড বিস্তারিত

### সিনট্যাক্স:

```python
class ClassName:
    def __init__(self, param1, param2):
        self.attribute1 = param1
        self.attribute2 = param2
```

### `self` কী?

`self` হলো object-এর নিজের রেফারেন্স। যখন `p = Person("রহিম", 25)` লিখি, তখন:
- `self` = `p`
- `self.name = "রহিম"` মানে `p.name = "রহিম"`

### উদাহরণ:

```python
class Student:
    def __init__(self, name, roll, department):
        self.name = name
        self.roll = roll
        self.department = department

    def display(self):
        print(f"নাম: {self.name}")
        print(f"রোল: {self.roll}")
        print(f"ডিপার্টমেন্ট: {self.department}")

s1 = Student("রহিম", 101, "CSE")
s1.display()
# আউটপুট:
# নাম: রহিম
# রোল: 101
# ডিপার্টমেন্ট: CSE
```

---

## ৩. Constructor-এ ডিফল্ট প্যারামিটার

Constructor-এ ডিফল্ট মান দেওয়া যায়, যাতে কোনো argument না দিলেও কাজ করে।

```python
class Person:
    def __init__(self, name, age=18, city="ঢাকা"):
        self.name = name
        self.age = age
        self.city = city

p1 = Person("রহিম")              # age=18, city="ঢাকা" (ডিফল্ট)
p2 = Person("করিম", 30)          # city="ঢাকা" (ডিফল্ট)
p3 = Person("সালাম", 25, "চট্টগ্রাম")

print(p1.name, p1.age, p1.city)   # রহিম 18 ঢাকা
print(p2.name, p2.age, p2.city)   # করিম 30 ঢাকা
print(p3.name, p3.age, p3.city)   # সালাম 25 চট্টগ্রাম
```

⚠️ নিয়ম: ডিফল্ট প্যারামিটার সবসময় **শেষে** থাকতে হবে।

---

## ৪. Constructor ছাড়া Object (ডিফল্ট Constructor)

যদি কোনো `__init__` না লিখেন, Python স্বয়ংক্রিয়ভাবে একটা ডিফল্ট constructor দেয়:

```python
class Empty:
    pass

e = Empty()   # কোনো argument ছাড়াই object তৈরি
```

কিন্তু attribute সেট করতে চাইলে `__init__` লিখতে হবে।

---

## ৫. Constructor-এ ভ্যালিডেশন

Constructor-এ ইনপুট ভ্যালিডেট করা যায়:

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        if balance < 0:
            raise ValueError("ব্যালেন্স ঋণাত্মক হতে পারে না!")
        self.balance = balance

acc1 = BankAccount("রহিম", 1000)
print(acc1.balance)   # 1000

try:
    acc2 = BankAccount("করিম", -500)
except ValueError as e:
    print(f"সমস্যা: {e}")   # সমস্যা: ব্যালেন্স ঋণাত্মক হতে পারে না!
```

---

## ৬. Constructor-এ অন্য Method কল করা

Constructor থেকে অন্য method কল করা যায়:

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius
        self.area = self.calculate_area()   # constructor থেকে method কল

    def calculate_area(self):
        return 3.14159 * self.radius ** 2

c = Circle(5)
print(f"ব্যাসার্ধ: {c.radius}")     # 5
print(f"ক্ষেত্রফল: {c.area:.2f}")   # 78.54
```

---

## ৭. `*args` ও `**kwargs` দিয়ে Constructor

```python
class Config:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

c1 = Config(1, 2, 3, name="রহিম", age=25)
print(c1.args)     # (1, 2, 3)
print(c1.kwargs)   # {'name': 'রহিম', 'age': 25}
```

---

## ৮. Constructor Overloading (Python-এ নেই)

Python-এ একাধিক `__init__` থাকতে পারে না। শেষেরটা সবসময় কাজ করে। তাই ডিফল্ট প্যারামিটার ব্যবহার করা হয়।

```python
# ❌ Python-এ কাজ করে না
class Demo:
    def __init__(self):
        pass
    def __init__(self, x):   # এইটাই কাজ করবে
        self.x = x
```

---

## ৯. `__del__` — Destructor

`__del__` হলো destructor, object মুছে যাওয়ার সময় চলে। খুব কম ব্যবহৃত হয়।

```python
class Demo:
    def __init__(self, name):
        self.name = name
        print(f"{self.name} তৈরি হয়েছে")

    def __del__(self):
        print(f"{self.name} মুছে যাচ্ছে")

d = Demo("অবজেক্ট")
del d   # মুছে ফেলা হচ্ছে
# আউটপুট:
# অবজেক্ট তৈরি হয়েছে
# অবজেক্ট মুছে যাচ্ছে
```

---

## ১০. Practical Exercise

```python
# ============ Exercise 1: বেসিক Constructor ============
print("=== Exercise 1 ===")
class Book:
    def __init__(self, title, author, year, pages):
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages

    def info(self):
        print(f"'{self.title}' - {self.author} ({self.year})")
        print(f"পৃষ্ঠা: {self.pages}")

b1 = Book("পাইথন শিখি", "রহিম আহমেদ", 2023, 300)
b1.info()

# ============ Exercise 2: ডিফল্ট প্যারামিটার ============
print("\n=== Exercise 2 ===")
class User:
    def __init__(self, username, role="user", active=True):
        self.username = username
        self.role = role
        self.active = active

    def display(self):
        status = "সক্রিয়" if self.active else "নিষ্ক্রিয়"
        print(f"{self.username} - {self.role} ({status})")

u1 = User("rahim")
u2 = User("karim", "admin")
u3 = User("salam", "editor", False)
u1.display()
u2.display()
u3.display()

# ============ Exercise 3: ভ্যালিডেশন ============
print("\n=== Exercise 3 ===")
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        if price < 0:
            raise ValueError("দাম ঋণাত্মক হতে পারে না")
        if quantity < 0:
            raise ValueError("পরিমাণ ঋণাত্মক হতে পারে না")
        self.price = price
        self.quantity = quantity

    def total_value(self):
        return self.price * self.quantity

try:
    p = Product("লেপটপ", 50000, 5)
    print(f"মোট মূল্য: {p.total_value()} টাকা")
    p2 = Product("খারাপ", -100, 2)
except ValueError as e:
    print(f"সমস্যা: {e}")

# ============ Exercise 4: Constructor থেকে Method কল ============
print("\n=== Exercise 4 ===")
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.area = self.calc_area()
        self.perimeter = self.calc_perimeter()

    def calc_area(self):
        return self.length * self.width

    def calc_perimeter(self):
        return 2 * (self.length + self.width)

r = Rectangle(5, 3)
print(f"ক্ষেত্রফল: {r.area}")
print(f"পরিসীমা: {r.perimeter}")

# ============ Exercise 5: বাস্তব উদাহরণ ============
print("\n=== Exercise 5 ===")
class ShoppingCart:
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.items = []

    def add_item(self, item, price):
        self.items.append({"item": item, "price": price})

    def total(self):
        return sum(i["price"] for i in self.items)

    def show_cart(self):
        print(f"{self.customer_name}-এর কার্ট:")
        for i in self.items:
            print(f"  - {i['item']}: {i['price']} টাকা")
        print(f"মোট: {self.total()} টাকা")

cart = ShoppingCart("রহিম")
cart.add_item("পেন", 10)
cart.add_item("কিতাব", 50)
cart.add_item("ব্যাগ", 200)
cart.show_cart()
```

---

## 🎯 আজকের Key Takeaways

1. **Constructor** = object তৈরির সময় স্বয়ংক্রিয়ভাবে চলা method
2. Python-এ constructor হলো `__init__`
3. `self` — object-এর নিজের রেফারেন্স
4. Constructor-এ ডিফল্ট প্যারামিটার দেওয়া যায়
5. Constructor-এ ইনপুট ভ্যালিডেশন করা যায়
6. Constructor থেকে অন্য method কল করা যায়
7. Python-এ constructor overloading নেই — ডিফল্ট প্যারামিটার ব্যবহার করতে হয়
8. `__del__` — destructor (খুব কম ব্যবহৃত)

---

## ❓ অনুশীলনী প্রশ্ন

1. Constructor কী? কেন ব্যবহার করা হয়?
2. `self` কী এবং কেন দরকার?
3. Constructor-এ ডিফল্ট প্যারামিটার কীভাবে ব্যবহার করা হয়?
4. একটা `Car` class তৈরি করুন যেখানে constructor-এ `brand`, `model`, `year`, `price` থাকবে
5. Constructor-এ ভ্যালিডেশন কীভাবে করা যায়?
6. `__del__` method এর কাজ কী?
