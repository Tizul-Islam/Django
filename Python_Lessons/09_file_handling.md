# Python: File Handling 📂

প্রোগ্রাম থেকে কম্পিউটারের ফাইলে লেখা ও ফাইল থেকে পড়া কে **File Handling** বলে। এটা ডেটা সংরক্ষণ ও পুনরুদ্ধারের জন্য খুবই গুরুত্বপূর্ণ।

---

## ১. File Handling কেন দরকার?

প্রোগ্রাম চলা বন্ধ হলে তার সব ডেটা মুছে যায়। File-এ লিখলে ডেটা স্থায়ীভাবে সংরক্ষিত থাকে এবং পরে আবার পড়া যায়।

**ব্যবহার:**
- 💾 ডেটা সংরক্ষণ
- 📄 ফাইল থেকে ডেটা পড়া
- 📝 লগ ফাইল তৈরি
- 📊 CSV/JSON ফাইল হ্যান্ডেল

---

## ২. File খোলা — `open()` ফাংশন

Python-এ ফাইল খুলতে `open()` ফাংশন ব্যবহার করা হয়।

### সিনট্যাক্স:

```python
file = open("ফাইলের_নাম", "মোড")
```

### File Modes (মোড):

| মোড | কাজ |
|------|------|
| `"r"` | Read — ফাইল পড়া (ডিফল্ট) |
| `"w"` | Write — ফাইলে লেখা (পুরনো কন্টেন্ট মুছে দেয়) |
| `"a"` | Append — ফাইলের শেষে যোগ করা |
| `"x"` | Create — নতুন ফাইল তৈরি (ফাইল থাকলে error) |
| `"r+"` | Read + Write |
| `"rb"` | Binary mode-এ Read |
| `"wb"` | Binary mode-এ Write |

### ⚠️ গুরুত্বপূর্ণ:
ফাইল কাজ শেষে `close()` করতে হবে, না হলে সমস্যা হতে পারে।

---

## ৩. ফাইলে লেখা — Write

### Method 1: `write()` দিয়ে লেখা

```python
# "w" মোডে ফাইল খোলা
file = open("example.txt", "w")
file.write("হ্যালো, পাইথন!\n")
file.write("আমি ফাইল হ্যান্ডলিং শিখছি।\n")
file.close()

# ফাইলটা এখন দুই লাইন লেখা আছে
```

### Method 2: `writelines() দিয়ে লেখা

```python
lines = ["প্রথম লাইন\n", "দ্বিতীয় লাইন\n", "তৃতীয় লাইন\n"]

file = open("example.txt", "w")
file.writelines(lines)
file.close()
```

⚠️ `writelines() স্বয়ংক্রিয়ভাবে নতুন লাইন যোগ করে না — স্বয়ংক্রিয়ভাবে `\n` যোগ করতে হয়।

---

## ৪. ফাইল থেকে পড়া — Read

### Method 1: `read()` — পুরো ফাইল পড়া

```python
file = open("example.txt", "r")
content = file.read()
print(content)
file.close()
```

### Method 2: `read(n)` — নির্দিষ্ট অক্ষর পড়া

```python
file = open("example.txt", "r")
content = file.read(10)   # প্রথম ১০টা অক্ষর
print(content)
file.close()
```

### Method 3: `readline()` — এক লাইন পড়া

```python
file = open("example.txt", "r")
line1 = file.readline()   # প্রথম লাইন
line2 = file.readline()   # দ্বিতীয় লাইন
print(line1)
print(line2)
file.close()
```

### Method 4: `readlines()` — সব লাইন list আকারে

```python
file = open("example.txt", "r")
lines = file.readlines()
print(lines)
file.close()

# আউটপুট: ['প্রথম লাইন\n', 'দ্বিতীয় লাইন\n', 'তৃতীয় লাইন\n']
```

### Method 5: লুপ দিয়ে লাইন লাইন পড়া

```python
file = open("example.txt", "r")
for line in file:
    print(line, end="")
file.close()
```

---

## ৫. `with` স্টেটমেন্ট — সেরা পদ্ধতি

`with` স্টেটমেন্ট ব্যবহার করলে স্বয়ংক্রিয়ভাবে ফাইল বন্ধ হয়ে যায়। এটাই সবচেয়ে ভালো ও নিরাপদ পদ্ধতি।

### সিনট্যাক্স:

```python
with open("ফাইলের_নাম", "মোড") as file:
    # কাজ
    pass
# with ব্লক শেষে ফাইল স্বয়ংক্রিয়ভাবে বন্ধ হয়ে যায়
```

### লেখার উদাহরণ:

```python
with open("example.txt", "w") as file:
    file.write("হ্যালো, পাইথন!\n")
    file.write("with স্টেটমেন্ট দিয়ে লেখা হয়েছে।\n")
```

### পড়ার উদাহরণ:

```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```

---

## ৬. Append (যোগ করা

ফাইলের শেষে নতুন কন্টেন্ট যোগ করতে `"a"` মোড ব্যবহার করা হয়।

```python
with open("example.txt", "a") as file:
    file.write("এই লাইনটা যোগ করা হয়েছে।\n")
    file.write("আরেকটা লাইন।\n")
```

### `"w"` বনাম `"a"`:

| `"w"` | `"a"` |
|--------|--------|
| পুরনো কন্টেন্ট মুছে দেয় | পুরনো কন্টেন্ট রেখে শেষে যোগ করে |
| ফাইল না থাকলে তৈরি করে | ফাইল না থাকলে তৈরি করে |

---

## ৭. ফাইল ম্যানিপুলেশন

### ফাইল আছে কিনা চেক করা

```python
import os

if os.path.exists("example.txt"):
    print("ফাইলটা আছে")
else:
    print("ফাইলটা নেই")
```

### ফাইল ডিলিট করা

```python
import os

if os.path.exists("example.txt"):
    os.remove("example.txt")
    print("ফাইল ডিলিট হয়েছে")
else:
    print("ফাইলটা নেই")
```

### ফাইলের নাম পরিবর্তন করা

```python
import os

os.rename("পুরনো_নাম.txt", "নতুন_নাম.txt")
```

### ফোল্ডার তৈরি ও ডিলিট

```python
import os

# নতুন ফোল্ডার তৈরি
os.mkdir("নতুন_ফোল্ডার")

# ফোল্ডার ডিলিট
os.rmdir("নতুন_ফোল্ডার")
```

---

## ৮. CSV ফাইল হ্যান্ডেল

CSV (Comma Separated Values) ফাইল হ্যান্ডেল করতে `csv` module ব্যবহার করা হয়।

### CSV ফাইলে লেখা

```python
import csv

with open("students.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["নাম", "বয়স", "শহর"])
    writer.writerow(["রহিম", 25, "ঢাকা"])
    writer.writerow(["করিম", 30, "চট্টগ্রাম"])
    writer.writerow(["সালাম", 20, "সিলেট"])
```

### CSV ফাইল থেকে পড়া

```python
import csv

with open("students.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# আউটপুট:
# ['নাম', 'বয়স', 'শহর']
# ['রহিম', '25', 'ঢাকা']
# ['করিম', '30', 'চট্টগ্রাম']
# ['সালাম', '20', 'সিলেট']
```

### DictReader দিয়ে পড়া

```python
import csv

with open("students.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(f"{row['নাম']} - {row['বয়স']} বছর - {row['শহর']}")

# আউটপুট:
# রহিম - 25 বছর - ঢাকা
# করিম - 30 বছর - চট্টগ্রাম
# সালাম - 20 বছর - সিলেট
```

---

## ৯. JSON ফাইল হ্যান্ডেল

JSON (JavaScript Object Notation) হলো ডেটা স্টোরেজ ও API-র জন্য জনপ্রিয় ফরম্যাট।

### JSON ফাইলে লেখা

```python
import json

data = {
    "নাম": "রহিম",
    "বয়স": 25,
    "শহর": "ঢাকা",
    "পছন্দের_খাবার": ["ভাত", "মাছ", "ডাল"]
}

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
```

### JSON ফাইল থেকে পড়া

```python
import json

with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    print(data)
    print(data["নাম"])
    print(data["পছন্দের_খাবার"])
```

### JSON ↔ Python রূপান্তর

| JSON | Python |
|-------|--------|
| object | dict |
| array | list |
| string | str |
| number (int) | int |
| number (float) | float |
| true | True |
| false | False |
| null | None |

---

## ১০. File Pointer ও স্ট্রাকচার

### `tell()` ও `seek()` দিয়ে ফাইলের পজিশন কন্ট্রোল করা যায়।

```python
with open("example.txt", "r") as file:
    print(file.tell())   # ০ — শুরুতে
    content = file.read(5)  # ৫ অক্ষর পড়া
    print(file.tell())   # ৫ — এখন ৫ নম্বর পজিশনে
    file.seek(0)          # আবার শুরুতে ফিরে গেল
    print(file.read())   # পুরো ফাইল আবার পড়া
```

---

## ১১. ব্যবহারিক উদাহরণ

### উদাহরণ ১: ছাত্রদের তথ্য সংরক্ষণ

```python
def save_students(students):
    with open("students.txt", "w") as file:
        for student in students:
            file.write(f"{student['নাম']},{student['বয়স']},{student['শহর']}\n")

students = [
    {"নাম": "রহিম", "বয়স": 25, "শহর": "ঢাকা"},
    {"নাম": "করিম", "বয়স": 30, "শহর": "চট্টগ্রাম"},
]

save_students(students)
print("সংরক্ষিত হয়েছে")
```

### উদাহরণ ২: Word Counter

```python
def count_words(filename):
    with open(filename, "r") as file:
        content = file.read()
        words = content.split()
        return len(words)

print(f"মোট শব্দ: {count_words('example.txt')}")
```

### উদাহরণ ৩: লগ ফাইল

```python
import datetime

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("app.log", "a") as file:
        file.write(f"[{timestamp}] {message}\n")

log("অ্যাপ্লিকেশন শুরু হয়েছে")
log("ব্যবহারকারী লগইন করেছে")
log("ডেটা সংরক্ষিত হয়েছে")
```

---

## ১২. Practical Exercise

```python
import json
import csv
import os

# --- Exercise 1: ফাইলে লেখা ও পড়া ---
with open("notes.txt", "w") as f:
    f.write("পাইথন শিখছি\n")
    f.write("ফাইল হ্যান্ডলিং সহজ\n")
    f.write("প্রাকটিস করুন\n")

with open("notes.txt", "r") as f:
    print("=== ফাইলের কন্টেন্ট ===")
    print(f.read())

# --- Exercise 2: Append ---
with open("notes.txt", "a") as f:
    f.write("নতুন লাইন যোগ হয়েছে\্র\n")

# --- Exercise 3: লাইন লাইন পড়া ---
with open("notes.txt", "r") as f:
    print("=== লাইন লাইন:")
    for i, line in enumerate(f, 1):
        print(f"{i}. {line.strip()}")

# --- Exercise 4: CSV ---
data = [
    ["পণ্য", "দাম", "পরিমাণ"],
    ["আপেল", 50, 10],
    ["কমলা", 40, 15],
    ["কলা", 30, 20],
]

with open("shop.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

print("\n=== CSV ফাইল ===")
with open("shop.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# --- Exercise 5: JSON ---
person = {
    "নাম": "আব্দুল্লাহ",
    "বয়স": 28,
    "পেশা": "প্রোগ্রামার",
    "দক্ষতা": ["Python", "Django", "JavaScript"]
}

with open("person.json", "w", encoding="utf-8") as f:
    json.dump(person, f, ensure_ascii=False, indent=2)

print("\n=== JSON ফাইল ===")
with open("person.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print(f"{data['নাম']} - {data['বয়স']} বছর")
    print(f"দক্ষতা: {', '.join(data['দক্ষতা'])}")

# --- Exercise 6: ফাইল চেক ও ডিলিট ---
print("\n=== ফাইল ম্যানেজমেন্ট ===")
print(f"notes.txt আছে? {os.path.exists('notes.txt')}")
print(f"shop.csv আছে? {os.path.exists('shop.csv')}")
```

---

## 🎯 আজকের Key Takeaways

1. `open("ফাইল", "মোড") — ফাইল খোলা
2. File modes: `"r"` (read), `"w"` (write), `"a"` (append), `"x"` (create)
3. `write()` — ফাইলে লেখা
4. `read()`, `readline()`, `readlines()` — ফাইল থেকে পড়া
5. `with` স্টেটমেন্ট — স্বয়ংক্রিয়ভাবে ফাইল বন্ধ করে (সেরা পদ্ধতি)
6. `os.path.exists()` — ফাইল আছে কিনা চেক
7. `os.remove()` — ফাইল ডিলিট
8. `csv` module — CSV ফাইল হ্যান্ডেল
9. `json` module — JSON ফাইল হ্যান্ডেল
10. কাজ শেষে ফাইল `close()` করতে হবে (with ব্যবহার করলে দরকার নেই)

---

## ❓ অনুশীলনী প্রশ্ন

1. `"r"`, `"w"`, `"a"` মোডের পার্থক্য কী?
2. `with` স্টেটমেন্ট কেন ব্যবহার করা ভালো?
3. একটা টেক্সট ফাইল থেকে সব লাইন পড়ে কীভাবে প্রিন্ট করবেন?
4. CSV ফাইলে কীভাবে ডেটা লিখবেন?
5. JSON ফাইল থেকে কীভাবে ডেটা পড়বেন?
6. ফাইল আছে কিনা কীভাবে চেক করবেন?
7. একটা ফাইলের শেষে নতুন কন্টেন্ট যোগ করুন
