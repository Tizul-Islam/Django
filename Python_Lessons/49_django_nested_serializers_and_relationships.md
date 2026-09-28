# Lesson 49: Django REST Framework - Nested Serializers ও Relationships

Django REST Framework (DRF)-এ যখন একাধিক ডেটাবেজ টেবিল বা মডেল একে অপরের সাথে সম্পর্কিত (যেমন `OneToOne`, `ForeignKey` বা `ManyToManyField`) থাকে, তখন সেই রিলেশনশিপকে ক্লায়েন্টের কাছে সঠিকভাবে রিপ্রেজেন্ট এবং হ্যান্ডেল করার জন্য **Relationships** এবং **Nested Serializers** ব্যবহার করা হয়।

---

## ১. Relationships ও Nested Serializers কী এবং কেন প্রয়োজন?

বাস্তব জীবনের যে কোনো ডেটাবেজে টেবিলগুলো বিচ্ছিন্ন থাকে না। উদাহরণস্বরূপ:
- একজন **User** এর অনেকগুলো **Task** থাকতে পারে (`ForeignKey` - One to Many)।
- একটি **Order** এর ভেতরে অনেকগুলো **OrderItem** থাকে।
- একটি **Post** এর সাথে অনেকগুলো **Tag** বা **Comment** যুক্ত থাকে।

যখন আমরা `/api/v1/tasks/` অথবা `/api/v1/users/` এ API রিকোয়েস্ট পাঠাই, ক্লায়েন্ট (যেমন React, Next.js বা মোবাইল অ্যাপ) কেবল একটি ফরেন-কি আইডি (যেমন `"user": 3`) পেলে তাকে আবার ব্যবহারকারীর নাম ও ইমেইল পাওয়ার জন্য দ্বিতীয়বার রিকোয়েস্ট পাঠাতে হয়। 

**Nested Serializer** ব্যবহারের মাধ্যমে আমরা একটি সিঙ্গেল API রেসপন্সে রিলেটেড মডেলের বিস্তারিত অবজেক্ট সংযুক্ত করে পাঠাতে পারি।

```json
{
    "id": 1,
    "title": "Complete Django DRF Project",
    "is_completed": false,
    "user": {
        "id": 5,
        "username": "tizul",
        "email": "tizul@example.com"
    }
}
```

---

## ২. DRF-এ Relationship প্রদর্শনের বিভিন্ন উপায়

DRF রিলেটেড মডেলের ডেটা ফিল্ড আকারে প্রকাশ করার জন্য বেশ কিছু বিল্ট-ইন ফিল্ড ক্লাস সরবরাহ করে:

| ফিল্ডের নাম | কী আউটপুট দেয় | উদাহরণ |
| :--- | :--- | :--- |
| **`PrimaryKeyRelatedField`** | শুধুমাত্র প্রাইমারি কি (ID) | `"user": 5` |
| **`StringRelatedField`** | মডেলের `__str__()` মেথডের রিটার্ন মান | `"user": "tizul (tizul@example.com)"` |
| **`SlugRelatedField`** | মডেলের নির্দিষ্ট কোনো ইউনিক ফিল্ড (যেমন slug বা username) | `"user": "tizul"` |
| **`HyperlinkedRelatedField`** | রিলেটেড অবজেক্টের বিস্তারিত API URL | `"user": "http://127.0.0.1:8000/api/v1/users/5/"` |
| **`Nested Serializer`** | সম্পূর্ণ অবজেক্ট ডিকশনারি বা অবজেক্টের লিস্ট | `"user": {"id": 5, "username": "tizul", ...}` |

### উদাহরণ কোড:
```python
from rest_framework import serializers
from .models import Task

class TaskSimpleRelSerializer(serializers.ModelSerializer):
    # ১. স্ট্রিং রিপ্রেজেন্টেশন (Read-only)
    user_str = serializers.StringRelatedField(source='user', read_only=True)
    
    # ২. নির্দিষ্ট ফিল্ড বা স্লাগ
    user_name = serializers.SlugRelatedField(source='user', slug_field='username', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'user_str', 'user_name']
```

---

## ৩. Nested Serializer: Forward ও Reverse রিলেশনশিপ

### ক. Forward Relationship (Task -> User)
একটি Task-এর ভেতরে তার মালিক User-কে নেস্টেড আকারে পাঠানো:

```python
# accounts/serializers.py
class UserSummarySerializer(serializers.ModelSerializer):
    """হালকা ওজনের নেস্টেড সিরিয়ালাইজার"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    # ফরোয়ার্ড নেস্টেড রিলেশন
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'is_completed']
```

### খ. Reverse Relationship (User -> Tasks)
একজন User অবজেক্টের ভেতর তার তৈরি করা সব Task এর তালিকা নেস্টেড আকারে পাঠানো:

```python
class UserSerializer(serializers.ModelSerializer):
    # রিভার্স রিলেশনশিপ: একজন ইউজারের একাধিক টাস্ক থাকতে পারে (many=True)
    tasks = TaskSerializer(many=True, read_only=True)
    task_count = serializers.IntegerField(source='tasks.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'tasks', 'task_count']
```

> **টিপ:** মডেলে `ForeignKey`-তে যে `related_name` দেওয়া থাকে (যেমন `related_name='tasks'`), সিরিয়ালাইজারে ঠিক সেই নামের ভেরিয়েবল ডিফাইন করতে হয়।

---

## ৪. `depth` অপশন ব্যবহার (স্বয়ংক্রিয় নেস্টিং)

যদি প্রতিটি রিলেশনের জন্য আলাদা আলাদা সিরিয়ালাইজার ক্লাস তৈরি করতে না চান, তবে `Meta` ক্লাসে `depth` ব্যবহার করা যায়:

```python
class TaskDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        depth = 1  # রিলেটেড মডেলগুলোকে ১ লেভেল পর্যন্ত অবজেক্ট আকারে রূপান্তর করবে
```

### `depth` এর সীমাবদ্ধতা:
- এটি রিলেটেড মডেলের **সব ফিল্ড** এক্সপোজ করে দেয় (যেমন ইউজারের পাসওয়ার্ড হ্যাশ বা সংবেদনশীল তথ্য চলে আসার ঝুঁকি থাকে)।
- ফিল্ড ফিল্টারিং বা কাস্টমাইজেশন করা যায় না।
- তাই প্রফেশনাল প্রজেক্টে সবসময় **Explicit Nested Serializer** ব্যবহার করাই বেস্ট প্র্যাকটিস।

---

## ৫. Writable Nested Serializers (ডেটা তৈরি ও আপডেট করা)

ডিফল্টভাবে DRF নেস্টেড ফিল্ডে রাইট (POST / PUT) অপারেশন সরাসরি হ্যান্ডেল করতে পারে না। কারণ DRF নিশ্চিত হতে পারে না যে নেস্টেড অবজেক্টটি কি নতুন তৈরি হবে, নাকি বিদ্যমান অবজেক্ট আপডেট হবে, নাকি ডিলিট হবে।

নেস্টেড অবজেক্ট সহ প্যারেন্ট অবজেক্ট সেভ করতে চাইলে সিরিয়ালাইজারের `create()` এবং `update()` মেথড ওভাররাইড করতে হয়:

```python
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'phone_number']

class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def create(self, validated_data):
        # ১. নেস্টেড ডেটা আলাদা করে বের করে নেওয়া (pop)
        profile_data = validated_data.pop('profile')
        
        # ২. প্যারেন্ট মডেল তৈরি করা
        user = User.objects.create_user(**validated_data)
        
        # ৩. চাইল্ড মডেল তৈরি করা
        Profile.objects.create(user=user, **profile_data)
        
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # ১. প্যারেন্ট মডেল আপডেট
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        
        # ২. চাইল্ড মডেল আপডেট
        if profile_data:
            profile = instance.profile
            profile.bio = profile_data.get('bio', profile.bio)
            profile.phone_number = profile_data.get('phone_number', profile.phone_number)
            profile.save()
            
        return instance
```

---

## ৬. The N+1 Database Query Problem এবং অপটিমাইজেশন

নেস্টেড সিরিয়ালাইজার ব্যবহারের সময় সবচেয়ে মারাত্মক যে সমস্যাটি দেখা দেয় তা হলো **N+1 Query Problem**।

### সমস্যাটি কী?
ধরা যাক আমাদের ২০ জন ইউজার আছে। প্রতিটি ইউজারের সাথে তাদের টাস্কগুলো লোড করা হচ্ছে।
- ১ টি কোয়েরি দিয়ে ২০ জন ইউজার লোড হলো: `SELECT * FROM auth_user;`
- এরপর সিরিয়ালাইজার যখন প্রতিটি ইউজারের জন্য লুপ চালায়, তখন প্রতিটি ইউজারের জন্য আলাদা করে ১টি করে কোয়েরি ডেটাবেজে পাঠায়: ২০ জনের জন্য ২০ টি কোয়েরি!
- মোট কোয়েরি সংখ্যা দাঁড়ায়: `1 + 20 = 21 টি কোয়েরি`। ব্যবহারকারী ১,০০০ জন হলে ১,০০১ টি কোয়েরি রান হবে, যা সার্ভারকে চরম ধীরগতির করে ফেলে।

### সমাধান: Django ORM এর অপটিমাইজেশন টেকনিক

```
+---------------------------------------------------------------+
|                      Query Optimization                       |
+-------------------------------+-------------------------------+
|         select_related        |        prefetch_related       |
+-------------------------------+-------------------------------+
| • Forward ForeignKey          | • Reverse ForeignKey (1-to-N) |
| • One-to-One Relationships    | • Many-to-Many Relationships  |
| • কাজ করে SQL JOIN দিয়ে      | • কাজ করে আলাদা ২য় কোয়েরি ও   |
| • একটাই SQL স্টেটমেন্টে ডেটা   |   পাইথনে মেমোরিতে জয়েন করে    |
|   আসে                         |                               |
+-------------------------------+-------------------------------+
```

#### আমাদের প্রজেক্টের ভিউতে বাস্তবায়ন:
```python
# accounts/views.py

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # ⚡ Performance: prefetch_related avoids N+1 queries for reverse relation (tasks)
    queryset = User.objects.all().prefetch_related('tasks').order_by('-date_joined')
    serializer_class = UserSerializer

class TaskViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # ⚡ Performance: select_related performs SQL JOIN for forward relation (user)
        return Task.objects.select_related('user').order_by('-created_at')
```

---

## ৭. আমাদের প্রজেক্টে রিয়েল-লাইফ কোড স্ট্রাকচার

### `accounts/serializers.py`
```python
class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'is_completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    tasks = TaskSerializer(many=True, read_only=True)
    task_count = serializers.IntegerField(source='tasks.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'tasks', 'task_count', 'date_joined']
        read_only_fields = ['id', 'date_joined']
```

---

## ৮. টেস্ট এবং ফলাফল যাচাই

টার্মিনাল থেকে টেস্ট রান করার কমান্ড:
```powershell
.\venv\Scripts\python.exe manage.py test accounts
```

লাইভ API যাচাই করার এন্ডপয়েন্ট:
1. `GET /api/v1/users/` – ব্যবহারকারীদের তালিকা এবং প্রতি ইউজারের অ্যাসাইনকৃত টাস্কের লিস্ট (`tasks: [...]`) ও টাস্কের সংখ্যা (`task_count: X`)।
2. `GET /api/v1/tasks/` – প্রতিটি টাস্কের ভেতরে তার ওনার ব্যবহারকারীর সংক্ষিপ্ত তথ্য (`user: {"id": 1, "username": "...", "email": "..."}`)।

---

## ৯. Key Takeaways (মূল শিক্ষণীয় বিষয়)

1. **Explicit Serializers are Best**: নিরাপত্তা ও নিয়ন্ত্রণের জন্য `depth` এর বদলে আলাদা নেস্টেড সিরিয়ালাইজার ব্যবহার করা শ্রেয়।
2. **Reverse Relation naming**: রিভার্স রিলেশনে মডেলে নির্ধারিত `related_name` ব্যবহার করতে হয় এবং একাধিক অবজেক্ট হলে `many=True` দিতে হয়।
3. **N+1 Avoidance**: 
   - ফরোয়ার্ড ফরেন কি বা ওয়ান-টু-ওয়ান হলে `select_related()`।
   - রিভার্স রিলেশন বা মেনি-টু-মেনি হলে `prefetch_related()`।
4. **Read-only vs Writable**: নেস্টেড সিরিয়ালাইজার ডিফল্টভাবে রাইট অপারেশনে এরর দেয় যদি না `create()` বা `update()` কাস্টমাইজ করা হয়।

---

## ১০. প্র্যাকটিস ও ইন্টারভিউ প্রশ্নাবলী (Questions & Answers)

### প্রশ্ন ১: Nested Serializer এবং Regular Serializer এর মধ্যে মূল পার্থক্য কী?
**উত্তর:** রেগুলার সিরিয়ালাইজার শুধুমাত্র একটি নির্দিষ্ট মডেলের সরাসরি কলাম বা ফিল্ডগুলোকে কনভার্ট করে। কিন্তু Nested Serializer ওই মডেলের সাথে সম্পর্কযুক্ত অন্যান্য মডেলের ডাটাকে অবজেক্ট বা লিস্ট আকারে সিরিয়ালাইজেশনের ভেতরে অন্তর্ভুক্ত করে।

### প্রশ্ন ২: `depth = 1` ব্যবহার করার অসুবিধাগুলো কী কী?
**উত্তর:** `depth = 1` রিলেটেড মডেলের সব ফিল্ড এক্সপোজ করে দেয় (যেমন পাসওয়ার্ড হ্যাশ), এতে সেনসিটিভ ডাটা লিক হওয়ার ঝুঁকি থাকে এবং ক্লায়েন্টের অপ্রয়োজনীয় ফিল্ড বাদ দেওয়ার বা ফরম্যাটিং করার সুযোগ থাকে না।

### প্রশ্ন ৩: `many=True` কখন এবং কেন ব্যবহার করতে হয়?
**উত্তর:** যখন কোনো রিলেশনশিপে একটি অবজেক্টের বিপরীতে একাধিক চাইল্ড অবজেক্ট থাকে (যেমন One-to-Many রিভার্স রিলেশন বা Many-to-Many রিলেশন), তখন DRF কে বোঝাতে `many=True` ব্যবহার করতে হয় যাতে সে অবজেক্টগুলোকে লিস্ট বা কুয়েরিসেট হিসেবে হ্যান্ডেল করে।

### প্রশ্ন ৪: `PrimaryKeyRelatedField` এবং `SlugRelatedField` এর পার্থক্য কী?
**উত্তর:** `PrimaryKeyRelatedField` শুধুমাত্র অবজেক্টের আইডি (যেমন `5`) প্রদর্শন বা ইনপুট হিসেবে গ্রহণ করে। আর `SlugRelatedField` অবজেক্টের একটি ইউনিক স্ট্রিং ফিল্ড (যেমন `username` বা `slug`) ব্যবহার করে।

### প্রশ্ন ৫: N+1 কোয়েরি সমস্যা কী?
**উত্তর:** কোনো প্রধান টেবিলের N সংখ্যক রো কোয়েরি করার পর প্রতিটি রো-এর রিলেটেড চাইল্ড রেকর্ড ফেচ করার জন্য যদি আলাদাভাবে আরও N সংখ্যক কোয়েরি চালানো হয়, তবে তাকে N+1 প্রবলেম বলে। এটি ডাটাবেজ পারফরম্যান্স মারাত্মকভাবে কমিয়ে দেয়।

### প্রশ্ন ৬: `select_related()` এবং `prefetch_related()` এর মধ্যে মেকানিজমগত পার্থক্য কী?
**উত্তর:** `select_related()` ডেটাবেজ লেভেলে SQL `JOIN` চালায় এবং একটাই কোয়েরিতে সব ডেটা এনে দেয় (Forward ForeignKey ও OneToOne-এ প্রযোজ্য)। অন্যদিকে `prefetch_related()` প্রথমে মূল কোয়েরি এবং পরবর্তীতে রিলেটেড টেবিলের জন্য আলাদা একটি SQL `IN (...)` কোয়েরি চালায় এবং পাইথন লেভেলে তাদের মধ্যে মেমোরিতে ম্যাপিং করে দেয় (ManyToMany ও Reverse ForeignKey-তে প্রযোজ্য)।

### প্রশ্ন ৭: Writable Nested Serializer তৈরি করার নিয়ম কী?
**উত্তর:** প্যারেন্ট সিরিয়ালাইজারে `create()` এবং/অথবা `update()` মেথড ওভাররাইড করতে হয়। ইনপুট ডাটা থেকে `validated_data.pop('nested_field')` করে নেস্টেড ডেটা আলাদা করে প্রথমে প্যারেন্ট ইনস্ট্যান্স তৈরি করতে হয় এবং পরে চাইল্ড ইনস্ট্যান্স ক্রিয়েট বা আপডেট করতে হয়।

### প্রশ্ন ৮: Nested Serializer কি ডিফল্টভাবে `read_only` থাকে?
**উত্তর:** না, তবে DRF এর বিল্ট-ইন `create()` বা `update()` নেস্টেড অবজেক্টের ক্ষেত্রে `NotImplementedError` বা ভ্যালিডেশন এরর প্রদান করে, তাই এক্সপ্লিসিটলি হ্যান্ডেল না করলে তা মূলত Read-Only হিসেবেই আচরণ করে।

### প্রশ্ন ৯: রিভার্স রিলেশনে সিরিয়ালাইজার ফিল্ডের নাম কী দিতে হয়?
**উত্তর:** চাইল্ড মডেলের ফরেন-কিতে ডিফাইন করা `related_name` এর নামানুসারে সিরিয়ালাইজার ফিল্ডের নাম রাখতে হয়। যদি মডেলে কোনো `related_name` না দেওয়া থাকে, তবে ডিফল্ট নাম হয় `modelname_set` (যেমন `task_set`)।

### প্রশ্ন ১০: `SerializerMethodField` দিয়ে কি রিলেটেড অবজেক্টের তথ্য আনা সম্ভব?
**উত্তর:** হ্যাঁ, যেকোনো কাস্টম মেথড লিখে (যেমন `get_tasks(self, obj)`) সেখান থেকে ফিল্টার বা ক্যালকুলেশন করে ডাটা রিটার্ন করা সম্ভব, তবে পারফরম্যান্স ও কাঠামোগত সৌন্দর্যের জন্য ডেডিকেটেড নেস্টেড সিরিয়ালাইজার ব্যবহার করাই সর্বোত্তম।
