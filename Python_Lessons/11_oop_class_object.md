# Python: OOP — Class ও Object 🧱

**OOP (Object-Oriented Programming)** হলো এমন একটা প্রোগ্রামিং প্যারাডাইম যেখানে কোডকে "object" দিয়ে সাজানো হয়। প্রতিটা object কিছু **attribute (বৈশিষ্ট্য)** এবং **method (কাজ/কার্যকলাপ)** ধারণ করে।

---

## ১. OOP কী এবং কেন দরকার?

বাস্তব জীবনের উদাহরণ: একটা **গাড়ি (Car)**।
- **বৈশিষ্ট্য (Attributes):** রং, মডেল, সাল, স্পিড
- **কাজ (Methods):** চালু করা, বন্ধ করা, গাড়ি চালানো, ব্রেক দেওয়া

OOP দিয়ে আমরা এই গাড়িটাকে কোডে উপস্থাপন করতে পারি।

**সুবিধা:**
- 🧩 কোড পুনরায় ব্যবহারযোগ্য
- 🏗️ বড় প্রজেক্টের কাজ সহজ হয়
- 🧠 বাস্তব জীবনের সমস্যা সহজে সমাধান করা যায়
- 🛡️ ডেটা সুরক্ষিত থাকে (Encapsulation)

---

## ২. Class কী?

**Class** হলো একটা ব্লুপ্রিন্ট বা নকশা যেখান থেকে object তৈরি হয়। Class-এ attribute (variable) এবং method (function) থাকে।

### সিনট্যাক্স:

```python
class ClassName:
    def __init__(self, parameter1, parameter2):
        self.attribute1 = parameter1
        self.attribute2 = parameter2

    def method_name(self):
        # কোড
        pass
```

### উদাহরণ — একটা গাড়ির Class:

```python
class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.speed = 0   # ডিফল্ট মান

    def start(self):
        print(f"{self.brand} {self.model} চালু হয়েছে!")

    def accelerate(self, increment):
        self.speed += increment
        print(f"গতি বাড়ছে... এখন {self.speed} km/h")

    def brake(self):
        self.speed = 0
        print("ব্রেক দেওয়া হয়েছে, গাড়ি থেমে গেছে")
```

---

## ৩. Object তৈরি করা

Class থেকে object তৈরি করাকে **instantiation** বলে।

```python
# Object তৈরি
my_car = Car("Toyota", "Corolla", 2023)

# Attribute access করা
print(my_car.brand)    # Toyota
print(my_car.model)    # Corolla
print(my_car.year)     # 2023
print(my_car.speed)    # 0

# Method call করা
my_car.start()         # Toyota Corolla চালু হয়েছে!
my_car.accelerate(50)  # গতি বাড়ছে... এখন 50 km/h
my_car.accelerate(30)  # গতি বাড়ছে... এখন 80 km/h
my_car.brake()         # ব্রেক দেওয়া হয়েছে, গাড়ি থেমে গেছে
```

### একাধিক Object:

একটা Class থেকে যত খুশি object তৈরি করা যায়:

```python
car1 = Car("Toyota", "Corolla", 2023)
car2 = Car("Honda", "Civic", 2022)
car3 = Car("BMW", "X5", 2024)

car1.start()    # Toyota Corolla চালু হয়েছে!
car2.start()    # Honda Civic চালু হয়েছে!
car3.start()    # BMW X5 চালু হয়েছে!
```

---

## ৪. `__init__` Method (Constructor)

`__init__` হলো কনস্ট্রাক্টর method। কোনো object তৈরি হওয়ার সময় এটা স্বয়ংক্রিয়ভাবে চলে এবং object-এর attribute গুলো সেট করে।

```python
class Person:
    def __init__(self, name, age):
        self.name = name   # instance attribute
        self.age = age     # instance attribute

p1 = Person("রহিম", 25)
print(p1.name)   # রহিম
print(p1.age)    # 25
```

### `self` কী?

`self` হলো object-এর নিজের একটা রেফারেন্স। যখন `p1.name` লিখি, তখন `self` হিসেবে `p1` ব্যবহার হয়।

---

## ৫. Class Attribute বনাম Instance Attribute

### Instance Attribute:
প্রতিটা object-এর আলাদা আলাদা মান থাকে। `__init__`-এ সেট করা হয়।

```python
class Car:
    def __init__(self, brand):
        self.brand = brand   # instance attribute

car1 = Car("Toyota")
car2 = Car("Honda")
print(car1.brand)   # Toyota
print(car2.brand)   # Honda
```

### Class Attribute:
সব object-এর জন্য একই মান থাকে। Class-এর সরাসরি ভেতরে সেট করা হয়।

```python
class Car:
    wheels = 4   # class attribute (সব গাড়িতেই ৪ চাকা)

    def __init__(self, brand):
        self.brand = brand

car1 = Car("Toyota")
car2 = Car("Honda")
print(car1.wheels)   # 4
print(car2.wheels)   # 4
```

---

## ৬. Method এর প্রকারভেদ

### Instance Method:
প্রতিটা object-এর জন্য আলাদা। প্রথম প্যারামিটার হয় `self`।

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"আমি {self.name}, আমি {self.age} বছরের")

p = Person("রহিম", 25)
p.greet()   # আমি রহিম, আমি 25 বছরের
```

### Class Method:
সম্পূর্ণ class-এর জন্য। `@classmethod` ডেকোরেটর দিয়ে চিহ্নিত করা হয়। প্রথম প্যারামিটার `cls`।

```python
class Car:
    total_cars = 0

    def __init__(self, brand):
        self.brand = brand
        Car.total_cars += 1

    @classmethod
    def get_total_cars(cls):
        return cls.total_cars

car1 = Car("Toyota")
car2 = Car("Honda")
print(Car.get_total_cars())   # 2
```

### Static Method:
কোনো class বা instance-এর সাথে সরাসরি সম্পর্কিত না। `@staticmethod` দিয়ে চিহ্নিত করা হয়।

```python
class Math:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def multiply(a, b):
        return a * b

print(Math.add(5, 3))        # 8
print(Math.multiply(5, 3))   # 15
```

---

## ৭. Encapsulation (এনক্যাপসুলেশন)

Encapsulation মানে data-কে বাইরের থেকে সরাসরি অ্যাক্সেস বন্ধ করে দেওয়া এবং method দিয়ে অ্যাক্সেস করার সুযোগ দেওয়া।

### Public Attribute:
সাধারণভাবে সব attribute public — বাইরে থেকে সরাসরি অ্যাক্সেস করা যায়।

```python
class Person:
    def __init__(self, name):
        self.name = name   # public

p = Person("রহিম")
print(p.name)        # রহিম
p.name = "করিম"      # সরাসরি পরিবর্তন করা যায়
print(p.name)        # করিম
```

### Private Attribute:
`__` দিয়ে শুরু করলে attribute private হয় — বাইরে থেকে সরাসরি অ্যাক্সেস করা যায় না।

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance   # private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"{amount} টাকা জমা হয়েছে")
        else:
            print("অবৈধ পরিমাণ")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"{amount} টাকা তোলা হয়েছে")
        else:
            print("পর্যাপ্ত ব্যালেন্স নেই")

    def get_balance(self):
        return self.__balance

account = BankAccount("রহিম", 1000)
# print(account.__balance)   # ❌ Error! সরাসরি অ্যাক্সেস করা যায় না
print(account.get_balance())   # 1000
account.deposit(500)           # 500 টাকা জমা হয়েছে
print(account.get_balance())   # 1500
account.withdraw(200)          # 200 টাকা তোলা হয়েছে
print(account.get_balance())   # 1300
```

### Property Decorator:
`@property` দিয়ে attribute-এর মতো method ব্যবহার করা যায়।

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
print(c.radius)   # 5
print(c.area)     # 78.53975
c.radius = 10     # setter ব্যবহার করে
print(c.area)     # 314.159
```

---

## ৮. Inheritance (ইনহেরিট্যান্স/উত্তরাধিকার)

একটা class অন্য একটা class-এর attribute ও method পেয়ে যাকে Inheritance বলে। Parent class থেকে Child class তৈরি করা হয়।

### সিনট্যাক্স:

```python
class ChildClass(ParentClass):
    # কোড
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


class Cat(Animal):
    def meow(self):
        print(f"{self.name} মিয়াও করছে")


dog = Dog("পলাশ")
dog.eat()     # পলাশ খাচ্ছে (Animal থেকে পাওয়া)
dog.sleep()   # পলাশ ঘুমাচ্ছে (Animal থেকে পাওয়া)
dog.bark()    # পলাশ ঘেউ ঘেউ করছে (নিজের method)

cat = Cat("মিনি")
cat.eat()     # মিনি খাচ্ছে
cat.meow()    # মিনি মিয়াও করছে
```

### Method Overriding:
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


Dog().speak()   # ঘেউ ঘেউ
Cat().speak()   # মিয়াও
Animal().speak()  # জানুয়ারি শব্দ করছে
```

### `super()` দিয়ে Parent class-এর method কল:

```python
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def info(self):
        print(f"নাম: {self.name}, প্রজাতি: {self.species}")


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "কুকুর")   # Parent এর __init__ কল
        self.breed = breed

    def info(self):
        super().info()   # Parent এর info কল
        print(f"জাত: {self.breed}")


dog = Dog("পলাশ", "German Shepherd")
dog.info()
# আউটপুট:
# নাম: পলাশ, প্রজাতি: কুকুর
# জাত: German Shepherd
```

---

## ৯. Polymorphism (পলিমরফিজম)

Polymorphism মানে "একই নাম, আলাদা আচরণ"। একই method ভিন্ন ভিন্ন ক্লাসে আলাদাভাবে কাজ করতে পারে।

```python
class Animal:
    def speak(self):
        return "শব্দ করছে"


class Dog(Animal):
    def speak(self):
        return "ঘেউ ঘেউ"


class Cat(Animal):
    def speak(self):
        return "মিয়াও"


def make_sound(animal):
    print(animal.speak())


make_sound(Dog())   # ঘেউ ঘেউ
make_sound(Cat())   # মিয়াও
```

---

## ১০. ব্যবহারিক উদাহরণ — Student ম্যানেজমেন্ট

```python
class Student:
    def __init__(self, name, roll, marks):
        self.name = name
        self.roll = roll
        self.marks = marks

    def get_grade(self):
        if self.marks >= 80:
            return "A+"
        elif self.marks >= 70:
            return "A"
        elif self.marks >= 60:
            return "B"
        else:
            return "F"

    def display(self):
        print(f"নাম: {self.name}")
        print(f"রোল: {self.roll}")
        print(f"নম্বর: {self.marks}")
        print(f"গ্রেড: {self.get_grade()}")
        print("-" * 30)


s1 = Student("রহিম", 101, 85)
s2 = Student("করিম", 102, 72)
s3 = Student("সালাম", 103, 55)

s1.display()
s2.display()
s3.display()
```

---

## ১১. Practical Exercise

```python
# ============ Exercise 1: বেসিক Class ============
print("=== Exercise 1 ===")
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def description(self):
        return f"'{self.title}' - {self.author} ({self.pages} পৃষ্ঠা)"


book1 = Book("পাইথন শিখি", "রহিম আহমেদ", 300)
book2 = Book("ডিজিটাল বাজার", "করিম হোসেন", 250)
print(book1.description())
print(book2.description())

# ============ Exercise 2: Class Attribute ============
print("\n=== Exercise 2 ===")
class Counter:
    count = 0

    def __init__(self):
        Counter.count += 1


c1 = Counter()
c2 = Counter()
c3 = Counter()
print(f"মোট অবজেক্ট: {Counter.count}")   # 3

# ============ Exercise 3: Encapsulation ============
print("\n=== Exercise 3 ===")
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"{amount} টাকা জমা হয়েছে। ব্যালেন্স: {self.__balance}")

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            print(f"{amount} টাকা উত্তোলন হয়েছে। ব্যালেন্স: {self.__balance}")
        else:
            print("পর্যাপ্ত ব্যালেন্স নেই")

    def check_balance(self):
        return self.__balance


acc = BankAccount("রহিম", 500)
acc.deposit(1000)
acc.withdraw(300)
print(f"চূড়ান্ত ব্যালেন্স: {acc.check_balance()}")

# ============ Exercise 4: Inheritance ============
print("\n=== Exercise 4 ===")
class Shape:
    def area(self):
        pass

    def perimeter(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)


circle = Circle(5)
rect = Rectangle(4, 6)
print(f"বৃত্তের ক্ষেত্রফল: {circle.area():.2f}")
print(f"আয়তক্ষেত্রের ক্ষেত্রফল: {rect.area()}")
print(f"আয়তক্ষেত্রের পরিসীমা: {rect.perimeter()}")

# ============ Exercise 5: Property ============
print("\n=== Exercise 5 ===")
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("ন্যূনতম তাপমাতা -273.15°C")
        self._celsius = value

    @property
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32


temp = Temperature(25)
print(f"{temp.celsius}°C = {temp.fahrenheit}°F")
temp.celsius = 100
print(f"{temp.celsius}°C = {temp.fahrenheit}°F")
```

---

## 🎯 আজকের Key Takeaways

1. **Class** = ব্লুপ্রিন্ট/নকশা, **Object** = class থেকে তৈরি বাস্তব বস্তু
2. `__init__` — constructor, object তৈরির সময় স্বয়ংক্রিয়ভাবে চলে
3. `self` — object-এর নিজের রেফারেন্স
4. **Instance Attribute** — প্রতিটা object-এর আলাদা
5. **Class Attribute** — সব object-এর জন্য একই
6. **Instance/Class/Static Method** — তিন ধরনের method
7. **Encapsulation** — `__` দিয়ে private attribute, method দিয়ে অ্যাক্সেস
8. **Inheritance** — Child class Parent class থেকে কিছু পায়
9. **Method Overriding** — Child class-এ Parent method পুনরায় লেখা
10. **Polymorphism** — একই নাম, আলাদা আচরণ
11. `super()` — Parent class-এর method কল করা

---

## ❓ অনুশীলনী প্রশ্ন

1. Class ও Object এর পার্থক্য কী?
2. `__init__` method এর কাজ কী?
3. `self` কী এবং কেন দরকার?
4. Instance Attribute ও Class Attribute এর পার্থক্য কী?
5. Encapsulation কী? উদাহরণ দিন
6. Inheritance কী? একটা উদাহরণ দিন
7. Method Overriding কী?
8. একটা `Employee` class তৈরি করুন যেখানে name, salary থাকবে এবং একটা method দিয়ে বোনাস (10% of salary) বের করবে
