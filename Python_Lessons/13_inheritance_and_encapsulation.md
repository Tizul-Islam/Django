# Python: Inheritance ও Encapsulation 🧬🔒

OOP-এর দুটি গুরুত্বপূর্ণ পিলার হলো **Inheritance (উত্তরাধিকার)** এবং **Encapsulation (এনক্যাপসুলেশন)**। Inheritance দিয়ে কোড reuse করা যায়, Encapsulation দিয়ে ডেটা সুরক্ষিত রাখা যায়।

---

## ১. Inheritance (উত্তরাধিকার) কী?

Inheritance হলো এমন একটা প্রক্রিয়া যেখানে একটা class অন্য একটা class-এর attribute ও method পেয়ে যায়।

- **Parent/Base class** — যার থেকে কিছু পাওয়া যায়
- **Child/Derived class** — যা Parent থেকে কিছু পায়

### সিনট্যাক্স:

```python
class Parent:
    # Parent-এর কোড
    pass

class Child(Parent):
    # Child-এর নিজের কোড
    pass
```

### উদাহরণ:

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} খাচ্ছে")

    def sleep(self):
        print(f"{self.name} ঘুমাচ্ছে")


class Dog(Animal):
    def bark(self):
        print(f"{self.name} ঘেউ ঘেউ করছে")


dog = Dog("পলাশ")
dog.eat()     # পলাশ খাচ্ছে  (Animal থেকে পাওয়া)
dog.sleep()   # পলাশ ঘুমাচ্ছে  (Animal থেকে পাওয়া)
dog.bark()    # পলাশ ঘেউ ঘেউ করছে  (নিজের method)
```

---

## ২. Inheritance-এর প্রকারভেদ

### ১. Single Inheritance (একক উত্তরাধিকার)

একটা Child class একটা Parent class থেকে inherit করে।

```python
class Parent:
    def parent_method(self):
        print("Parent method")

class Child(Parent):
    def child_method(self):
        print("Child method")

c = Child()
c.parent_method()   # Parent method
c.child_method()    # Child method
```

### ২. Multilevel Inheritance (বহুস্তরীয় উত্তরাধিকার)

একটা class অন্যটা থেকে, সেটা আরেকটা থেকে inherit করে।

```python
class Grandparent:
    def grandparent_method(self):
        print("Grandparent method")

class Parent(Grandparent):
    def parent_method(self):
        print("Parent method")

class Child(Parent):
    def child_method(self):
        print("Child method")

c = Child()
c.grandparent_method()   # Grandparent method
c.parent_method()        # Parent method
c.child_method()         # Child method
```

### ৩. Multiple Inheritance (বহু উত্তরাধিকার)

একটা Child class একাধিক Parent class থেকে inherit করে।

```python
class Father:
    def father_trait(self):
        print("বাবার বৈশিষ্ট্য")

class Mother:
    def mother_trait(self):
        print("মায়ের বৈশিষ্ট্য")

class Child(Father, Mother):
    def child_trait(self):
        print("শিশুর নিজের বৈশিষ্ট্য")

c = Child()
c.father_trait()    # বাবার বৈশিষ্ট্য
c.mother_trait()    # মায়ের বৈশিষ্ট্য
c.child_trait()     # শিশুর নিজের বৈশিষ্ট্য
```

### ৪. Hierarchical Inheritance (শ্রেণীবদ্ধ উত্তরাধিকার)

একটা Parent থেকে একাধিক Child inherit করে।

```python
class Animal:
    def eat(self):
        print("খাচ্ছে")

class Dog(Animal):
    def bark(self):
        print("ঘেউ ঘেউ")

class Cat(Animal):
    def meow(self):
        print("মিয়াও")

Dog().eat()    # খাচ্ছে
Dog().bark()   # ঘেউ ঘেউ
Cat().eat()    # খাচ্ছে
Cat().meow()   # মিয়াও
```

### ৫. Hybrid Inheritance (মিশ্র উত্তরাধিকার)

একাধিক ধরনের Inheritance একসাথে।

```python
class Animal:
    def eat(self):
        print("খাচ্ছে")

class Mammal(Animal):
    def give_birth(self):
        print("সন্তান জন্ম দেয়")

class Bird(Animal):
    def fly(self):
        print("উড়তে পারে")

class Bat(Mammal, Bird):
    pass

bat = Bat()
bat.eat()         # খাচ্ছে
bat.give_birth()  # সন্তান জন্ম দেয়
bat.fly()         # উড়তে পারে
```

---

## ৩. `super()` ফাংশন

`super()` দিয়ে Child class থেকে Parent class-এর method কল করা যায়।

### Parent-এর `__init__` কল:

```python
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "কুকুর")   # Parent-এর __init__ কল
        self.breed = breed

dog = Dog("পলাশ", "German Shepherd")
print(dog.name)      # পলাশ
print(dog.species)   # কুকুর
print(dog.breed)     # German Shepherd
```

### Parent-এর অন্য Method কল:

```python
class Animal:
    def speak(self):
        return "শব্দ করছে"

class Dog(Animal):
    def speak(self):
        parent_speak = super().speak()
        return f"{parent_speak} - ঘেউ ঘেউ"

print(Dog().speak())   # শব্দ করছে - ঘেউ ঘেউ
```

---

## ৪. Method Overriding

Child class-এ Parent class-এর method পুনরায় লেখা যায়।

```python
class Animal:
    def speak(self):
        print("জানুয়ারি শব্দ করছে")

class Dog(Animal):
    def speak(self):   # overriding
        print("ঘেউ ঘেউ")

class Cat(Animal):
    def speak(self):   # overriding
        print("মিয়াও")

Animal().speak()   # জানুয়ারি শব্দ করছে
Dog().speak()      # ঘেউ ঘেউ
Cat().speak()      # মিয়াও
```

### Method Resolution Order (MRO)

Multiple Inheritance-এ কোন method আগে কল হবে তা MRO নির্ধারণ করে।

```python
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")

class C(A):
    def show(self):
        print("C")

class D(B, C):
    pass

D().show()   # B (B আগে)
print(D.mro())  # MRO দেখা যায়
# [<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
```

---

## ৫. `isinstance()` ও `issubclass()`

```python
class Animal:
    pass

class Dog(Animal):
    pass

dog = Dog()

print(isinstance(dog, Dog))      # True — Dog class-এর object
print(isinstance(dog, Animal))   # True — Animal-এরও (inherit করায়)
print(issubclass(Dog, Animal))   # True — Dog, Animal-এর subclass
print(issubclass(Animal, Dog))   # False
```

---

## ৬. Encapsulation (এনক্যাপসুলেশন) কী?

Encapsulation মানে data-কে বাইরের থেকে সরাসরি অ্যাক্সেস বন্ধ করে দেওয়া এবং method দিয়ে অ্যাক্সেস করার সুযোগ দেওয়া। এটা ডেটা সুরক্ষা ও নিয়ন্ত্রণের জন্য গুরুত্বপূর্ণ।

### Access Modifiers:

Python-এ তিন ধরনের access modifier আছে:

| প্রকার | চিহ্ন | বিবরণ |
|--------|------|------|
| Public | সাধারণ | সবাই অ্যাক্সেস করতে পারে |
| Protected | `_` | Class ও subclass দিয়ে অ্যাক্সেস |
| Private | `__` | শুধু নিজের class দিয়ে অ্যাক্সেস |

### Public Attribute:

```python
class Person:
    def __init__(self, name):
        self.name = name   # public

p = Person("রহিম")
print(p.name)   # রহিম — সরাসরি অ্যাক্সেস
p.name = "করিম"
print(p.name)   # করিম — সরাসরি পরিবর্তন
```

### Protected Attribute (`_`):

```python
class Person:
    def __init__(self, name):
        self._name = name   # protected

p = Person("রহিম")
print(p._name)   # রহিম — অ্যাক্সেস করা যায় কিন্তু convention অনুযায়ী shouldn't
```

⚠️ `_` শুধু convention, আসলে কোনো restriction নেই।

### Private Attribute (`__`):

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance   # private

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount

    def get_balance(self):
        return self.__balance

acc = BankAccount("রহিম", 1000)
# print(acc.__balance)   # ❌ Error! সরাসরি অ্যাক্সেস করা যায় না
print(acc.get_balance())   # 1000 — method দিয়ে অ্যাক্সেস
acc.deposit(500)
print(acc.get_balance())   # 1500
```

---

## ৭. Getter ও Setter Method

Private attribute পড়া ও পরিবর্তন করার জন্য getter ও setter method ব্যবহার করা হয়।

```python
class Person:
    def __init__(self, name, age):
        self.__name = name
        self.set_age(age)   # setter দিয়ে সেট করা

    def get_name(self):
        return self.__name

    def set_name(self, name):
        if len(name) > 0:
            self.__name = name
        else:
            print("নাম খালি হতে পারে না")

    def get_age(self):
        return self.__age

    def set_age(self, age):
        if 0 < age < 150:
            self.__age = age
        else:
            print("ভুল বয়স")

p = Person("রহিম", 25)
print(p.get_name())   # রহিম
print(p.get_age())    # 25

p.set_age(30)
print(p.get_age())    # 30

p.set_age(200)        # ভুল বয়স
print(p.get_age())    # 30 (পরিবর্তন হয়নি)
```

---

## ৮. Property Decorator — `@property`

`@property` দিয়ে method কে attribute-এর মতো ব্যবহার করা যায়।

### সিনট্যাক্স:

```python
class ClassName:
    @property
    def attribute(self):
        return self._value

    @attribute.setter
    def attribute(self, value):
        # ভ্যালিডেশন
        self._value = value
```

### উদাহরণ:

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("ব্যাসার্ধ ঋণাত্মক হতে পারে না")
        self._radius = value

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(c.radius)   # 5 — property-এর মতো অ্যাক্সেস
print(c.area)     # 78.53975

c.radius = 10     # setter কাজ করছে
print(c.area)     # 314.159

try:
    c.radius = -5
except ValueError as e:
    print(f"সমস্যা: {e}")
```

### Read-only Property:

শুধু getter থাকলে read-only হয়:

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32

t = Temperature(25)
print(t.fahrenheit)   # 77.0
# t.fahrenheit = 100  # ❌ Error! শুধু read-only
```

---

## ৯. ব্যবহারিক উদাহরণ — ই-কমার্স

```python
class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self._price = price
        self._stock = stock

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("দাম ঋণাত্মক হতে পারে না")
        self._price = value

    @property
    def stock(self):
        return self._stock

    def buy(self, quantity):
        if quantity <= self._stock:
            self._stock -= quantity
            return f"{quantity}টি কেনা হয়েছে, বাকি: {self._stock}"
        return f"পর্যাপ্ত স্টক নেই! আছে: {self._stock}"


class Electronics(Product):
    def __init__(self, name, price, stock, warranty_years):
        super().__init__(name, price, stock)
        self.warranty_years = warranty_years

    def details(self):
        print(f"{self.name} - {self.price} টাকা")
        print(f"স্টক: {self.stock}, ওয়ারেন্টি: {self.warranty_years} বছর")


phone = Electronics("iPhone", 100000, 10, 2)
phone.details()
print(phone.buy(3))   # 3টি কেনা হয়েছে, বাকি: 7
phone.details()
```

---

## ১০. Practical Exercise

```python
# ============ Exercise 1: Single Inheritance ============
print("=== Exercise 1: Single Inheritance ===")
class Vehicle:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def start(self):
        print(f"{self.brand} গাড়ি চালু হয়েছে")

class Car(Vehicle):
    def __init__(self, brand, year, model):
        super().__init__(brand, year)
        self.model = model

    def info(self):
        print(f"{self.brand} {self.model} ({self.year})")

car = Car("Toyota", 2023, "Corolla")
car.start()
car.info()

# ============ Exercise 2: Multiple Inheritance ============
print("\n=== Exercise 2: Multiple Inheritance ===")
class Father:
    def father_property(self):
        return "বাবার সম্পত্তি"

class Mother:
    def mother_property(self):
        return "মায়ের সম্পত্তি"

class Child(Father, Mother):
    def own_property(self):
        return "নিজের সম্পত্তি"

child = Child()
print(child.father_property())
print(child.mother_property())
print(child.own_property())

# ============ Exercise 3: Method Overriding ============
print("\n=== Exercise 3: Method Overriding ===")
class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):   # overriding
        return self.side ** 2

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):   # overriding
        return 3.14159 * self.radius ** 2

print(f"বর্গের ক্ষেত্রফল: {Square(5).area()}")
print(f"বৃত্তের ক্ষেত্রফল: {Circle(5).area():.2f}")

# ============ Exercise 4: Encapsulation ============
print("\n=== Exercise 4: Encapsulation ===")
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.__marks = marks   # private

    def get_marks(self):
        return self.__marks

    def set_marks(self, marks):
        if 0 <= marks <= 100:
            self.__marks = marks
        else:
            print("নম্বর ০-১০০ এর মধ্যে হতে হবে")

s = Student("রহিম", 85)
print(f"নাম: {s.name}, নম্বর: {s.get_marks()}")
s.set_marks(95)
print(f"নতুন নম্বর: {s.get_marks()}")
s.set_marks(150)   # ভুল
print(f"নম্বর: {s.get_marks()}")   # 95 (পরিবর্তন হয়নি)

# ============ Exercise 5: Property ============
print("\n=== Exercise 5: Property ===")
class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("ব্যালেন্স ঋণাত্মক হতে পারে না")
        self._balance = amount

    def deposit(self, amount):
        self.balance += amount
        print(f"{amount} জমা হয়েছে। ব্যালেন্স: {self.balance}")

acc = BankAccount(1000)
print(f"শুরুর ব্যালেন্স: {acc.balance}")
acc.deposit(500)
try:
    acc.balance = -100
except ValueError as e:
    print(f"সমস্যা: {e}")
```

---

## 🎯 আজকের Key Takeaways

### Inheritance:
1. **Inheritance** — Child class Parent class-এর attribute/method পায়
2. **Single** — এক Parent থেকে এক Child
3. **Multilevel** — Parent → Child → Grandchild
4. **Multiple** — একাধিক Parent থেকে এক Child
5. **Hierarchical** — এক Parent থেকে একাধিক Child
6. **Hybrid** — একাধিক ধরনের মিশ্রণ
7. `super()` — Parent class-এর method কল করা
8. **Method Overriding** — Child-এ Parent method পুনরায় লেখা
9. `isinstance()`, `issubclass()` — চেক করার জন্য

### Encapsulation:
1. **Encapsulation** — data-কে বাইরের থেকে সরাসরি অ্যাক্সেস বন্ধ
2. **Public** — সাধারণ attribute
3. **Protected** — `_` দিয়ে শুরু (convention)
4. **Private** — `__` দিয়ে শুরু (আসলে restriction)
5. **Getter/Setter** — private attribute পড়া/লেখার জন্য method
6. **`@property`** — method কে attribute-এর মতো ব্যবহার
7. `@property.setter` — ভ্যালিডেশন সহ attribute সেট করা

---

## ❓ অনুশীলনী প্রশ্ন

1. Inheritance কী? কত প্রকার?
2. `super()` ফাংশনের কাজ কী?
3. Method Overriding কী?
4. Encapsulation কী? কেন দরকার?
5. `_` এবং `__` এর পার্থক্য কী?
6. Getter/Setter method কী?
7. `@property` ডেকোরেটর কীভাবে কাজ করে?
8. একটা `Employee` class তৈরি করুন যেখানে private `salary` attribute থাকবে এবং property দিয়ে অ্যাক্সেস করা যাবে
