# Django REST Framework Serializers ও ModelSerializer 📦🔄

Django REST Framework (DRF)-এর সবচেয়ে কেন্দ্রীয় ও গুরুত্বপূর্ণ কম্পোনেন্ট হলো **Serializer**।

সাধারণ Django-তে যেভাবে **Django Forms** ব্যবহারকারীর ইনপুট ডেটা ভ্যালিডেট করে HTML থেকে পাইথনে নিয়ে আসত, DRF-এ **Serializers** ঠিক একইভাবে ক্লায়েন্টের পাঠানো **JSON ডেটা** এবং ডেটাবেজের **Model/QuerySet**-এর মধ্যে দ্বিমুখী রূপান্তরের কাজ করে।

---

## ১. Serialization এবং Deserialization কী?

```mermaid
graph LR
    subgraph ১. Serialization "ডেটা পাঠানো"
        A[Django Model / QuerySet] -->|Serializer| B[Python Dictionary]
        B -->|JSON Renderer| C[JSON ডেটা ক্লায়েন্টে যায়]
    end

    subgraph ২. Deserialization "ডেটা গ্রহণ ও সেভ"
        D[ক্লায়েন্টের পাঠানো JSON] -->|Parser| E[Serializer Validation]
        E -->|is_valid?| F[ডেটাবেজে Model অবজেক্ট হিসেবে Save]
    end
```

* **Serialization (ধারাবাহিকীকরণ):** ডেটাবেজের জটিল মডেল বা কুয়েরিসেট ডেটাকে পাইথন ডিকশনারি এবং পরবর্তীতে **JSON** ডেটায় রূপান্তর করা।
* **Deserialization (বিপরীত প্রক্রিয়া):** ক্লায়েন্ট থেকে আসা JSON ডেটা গ্রহণ করে তা সঠিক কিনা যাচাই (Validate) করা এবং ডেটাবেজে মডেল ইনস্ট্যান্স হিসেবে সংরক্ষণ করা।

---

## ২. বেসিক `serializers.Serializer`

যখন কোনো ডেটা সরাসরি ডেটাবেজ মডেলের সাথে সম্পর্কিত থাকে না (যেমন: ওটিপি যাচাই, কন্টাক্ট মেসেজ পাঠানো বা লগইন তথ্য প্রসেস করা):

```python
# accounts/serializers.py
from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=200, required=False)
    message = serializers.CharField()

    # Deserialization এর সময় সেভ করার মেথড:
    def create(self, validated_data):
        # ডেটা সেভ করা বা ইমেইল পাঠানো
        return validated_data
```

---

## ৩. `serializers.ModelSerializer` (DRF-এর সুপারপাওয়ার 🏆)

বাস্তব প্রজেক্টের ৯০% ক্ষেত্রে আমরা কোনো মডেলের ওপর ভিত্তি করে API তৈরি করি। `ModelSerializer` মডেলের ফিল্ডগুলো দেখে স্বয়ংক্রিয়ভাবে সিরিয়ালাইজার ফিল্ড, ভ্যালিডেটর এবং `create()` ও `update()` মেথড তৈরি করে ফেলে।

ধরা যাক আমাদের একটি `Post` মডেল আছে:

```python
# blog/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

### `ModelSerializer` তৈরি করা:

```python
# blog/serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # ১. কোন কোন ফিল্ড JSON এ থাকবে:
        fields = ['id', 'author', 'title', 'content', 'is_published', 'created_at']
        
        # অথবা সব ফিল্ড চাইলে:
        # fields = '__all__'

        # ২. কিছু ফিল্ড শুধু ক্লায়েন্টে যাবে, ক্লায়েন্ট থেকে ইনপুট নেওয়া হবে না:
        read_only_fields = ['id', 'created_at']

        # ৩. কোনো ফিল্ডে অতিরিক্ত শর্ত যোগ করতে (যেমন পাসওয়ার্ড write_only করা):
        extra_kwargs = {
            'title': {'min_length': 5, 'error_messages': {'min_length': 'টাইটেল কমপক্ষে ৫ অক্ষরের হতে হবে!'}}
        }
```

---

## ৪. Serializer Validation (৩ স্তরের ভ্যালিডেশন)

ক্লায়েন্ট যাতে ভুল বা ক্ষতিকর ডেটা পাঠাতে না পারে, সেজন্য DRF-এ ৩টি স্তরে ডেটা যাচাই করা যায়:

### ১. Field-level Built-in Validators:
ফিল্ড তৈরির সময়ই ভ্যালিডেটর দেওয়া:
```python
from django.core.validators import MinValueValidator

price = serializers.DecimalField(
    max_digits=10, 
    decimal_places=2, 
    validators=[MinValueValidator(0.0)]
)
```

---

### ২. নির্দিষ্ট ফিল্ডের জন্য কাস্টম ভ্যালিডেশন (`validate_<field_name>`):

মেথডের নাম হতে হয়: `validate_ফিল্ডেরনাম(self, value)`

```python
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def validate_title(self, value):
        # শর্ত ১: নিষিদ্ধ কোনো শব্দ থাকা যাবে না
        forbidden_words = ["spam", "clickbait", "hacked"]
        for word in forbidden_words:
            if word in value.lower():
                raise serializers.ValidationError(f"টাইটেলে '{word}' শব্দটি ব্যবহার করা নিষিদ্ধ!")
        
        return value  # সর্বদা ভ্যালিডেটেড ভ্যালু রিটার্ন করতে হবে
```

---

### ৩. অবজেক্ট-লেভেল বা মাল্টি-ফিল্ড ভ্যালিডেশন (`validate`):

যখন একাধিক ফিল্ড একসাথে মিলিয়ে দেখতে হয় (যেমন: পাসওয়ার্ড এবং কনফার্ম পাসওয়ার্ড মিলেছে কিনা):

```python
class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "পাসওয়ার্ড দুটি মিলছে না!"})
        return data
```

---

## ৫. অ্যাডভান্সড সিরিয়ালাইজার টেকনিকসমূহ

### ১. `SerializerMethodField` (ডাইনামিক বা কাস্টম ফিল্ড):
মডেলে সরাসরি কোনো ফিল্ড না থাকলেও হিসাব করে নতুন ফিল্ড JSON-এ যোগ করা যায়:

```python
class PostSerializer(serializers.ModelSerializer):
    # নতুন ফিল্ড ঘোষণা:
    word_count = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'word_count', 'author_name']

    # get_<field_name> ফরম্যাটে ফাংশন লিখতে হয়:
    def get_word_count(self, obj):
        return len(obj.content.split())

    def get_author_name(self, obj):
        return obj.author.get_full_name() or obj.author.username
```

---

### ২. Nested Serializer (সম্পর্কিত মডেলের পূর্ণ তথ্য দেখানো):

ডিফল্টভাবে ForeignKey ফিল্ডে শুধু ID নম্বর (যেমন: `author: 1`) দেখায়। কিন্তু আমরা যদি লেখকের সম্পূর্ণ প্রোফাইল JSON-এ দেখাতে চাই:

```python
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PostDetailSerializer(serializers.ModelSerializer):
    # লেখক অবজেক্টকে নেস্ট করা হলো:
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at']
```

**JSON আউটপুট:**
```json
{
    "id": 1,
    "title": "Django REST Framework টিউটোরিয়াল",
    "content": "বিস্তারিত টিউটোরিয়াল...",
    "author": {
        "id": 5,
        "username": "tizul",
        "email": "tizul@example.com"
    },
    "created_at": "2026-09-23T10:00:00Z"
}
```

---

## ৬. ভিউতে Serializer ব্যবহারের সঠিক নিয়ম

```python
# ১. ডেটা ক্লায়েন্টে পাঠানো (Serialization):
posts = Post.objects.all()
serializer = PostSerializer(posts, many=True)  # QuerySet হলে many=True আবশ্যক
return Response(serializer.data)

# ২. ডেটা রিসিভ করে সেভ করা (Deserialization):
serializer = PostSerializer(data=request.data)
if serializer.is_valid():
    # অতিরিক্ত কোনো তথ্য কোড থেকে দিতে চাইলে:
    post = serializer.save(author=request.user)
    return Response(serializer.data, status=201)
else:
    return Response(serializer.errors, status=400)
```

---

## 🎯 আজকের Key Takeaways

1. **Serializer** মডেল অবজেক্টকে JSON-এ এবং আগত JSON ডেটাকে ভ্যালিডেট করে মডেল অবজেক্টে রূপান্তর করে।
2. দ্রুত মডেল ভিত্তিক API তৈরি করতে সর্বদা `ModelSerializer` ব্যবহার করুন।
3. একাধিক রেকর্ডের তালিকা পাঠাতে `many=True` আর্গুমেন্ট ব্যবহার করতে হয়।
4. একক ফিল্ড ভ্যালিডেশনের জন্য `validate_<fieldname>()` এবং বহু-ফিল্ডের জন্য `validate()` মেথড ব্যবহার করুন।
5. হিসাবকৃত বা ডাইনামিক ফিল্ড পাঠাতে `SerializerMethodField` এবং সংশ্লিষ্ট `get_<field>()` মেথড ব্যবহার করুন।
6. পাসওয়ার্ডের মতো গোপন তথ্য ক্লায়েন্টে না পাঠিয়ে শুধু গ্রহণের জন্য `extra_kwargs = {'password': {'write_only': True}}` ব্যবহার করুন।

---

## ❓ অনুশীলনী প্রশ্ন

1. Serialization এবং Deserialization-এর মধ্যে মূল পার্থক্য কী?
2. `serializers.Serializer` এবং `serializers.ModelSerializer`-এর মধ্যে ৩টি প্রধান পার্থক্য লিখুন।
3. একটি QuerySet-কে সিরিয়ালাইজ করার সময় `many=True` না দিলে কী ধরনের এরর দেখা দেবে?
4. `SerializerMethodField`-এর কাজ কী এবং এর সাথে সম্পর্কিত মেথডের নামকরণের নিয়ম কী?
5. `read_only_fields` এবং `write_only` অ্যাট্রিবিউট দুটির কাজ কী কী?
6. পাসওয়ার্ড এবং কনফার্ম পাসওয়ার্ড মেলানোর জন্য কোন ভ্যালিডেশন মেথডটি ওভাররাইড করতে হবে?
7. ForeignKey ফিল্ডে লেখকের শুধু ID নম্বরের বদলে লেখকের পুরো অবজেক্ট পাঠাতে কোন টেকনিক ব্যবহার করবেন?
8. `serializer.is_valid()` কল না করে `serializer.validated_data` রিড করলে কী সমস্যা হবে?
9. `serializer.save(author=request.user)` কোডটি ব্যাকএন্ডে কীভাবে কাজ করে?
10. `extra_kwargs` ডিকশনারি কোন কাজে ব্যবহৃত হয়?
