# Django Authentication বনাম Authorization 🛡️🔑

ওয়েব অ্যাপ্লিকেশন নিরাপত্তার ক্ষেত্রে **Authentication (AuthN)** এবং **Authorization (AuthZ)** দুটি সবচেয়ে মৌলিক অথচ প্রায়ই বিভ্রান্তিকর ধারণা। এই দুটি একসাথে কাজ করে আপনার অ্যাপ্লিকেশনের ডেটা ও ইউজারদের সুরক্ষিত রাখে।

এই লেসনে আমরা জানব এই দুটির গভীর পার্থক্য, বাস্তব জীবনের উপমা, Django-র বিল্ট-ইন Permissions ও Groups সিস্টেম, ভিউ ও টেমপ্লেটে অ্যাক্সেস কন্ট্রোল এবং অবজেক্ট-লেভেল পারমিশন বাস্তবায়ন।

---

## ১. বাস্তব জীবনের উপমা (Real-World Analogy)

একটি আন্তর্জাতিক বিমানবন্দর বা করপোরেট অফিসের কথা চিন্তা করুন:

```mermaid
graph LR
    subgraph ১. Authentication "AuthN"
        A[পাসপোর্ট বা আইডি কার্ড প্রদর্শন] --> B{আপনি কি সত্যিই আপনি?}
        B -->|হ্যাঁ| C[বিমানবন্দরে বা অফিসে প্রবেশ অনুমোদিত]
    end

    subgraph ২. Authorization "AuthZ"
        C --> D{আপনার টিকিট বা কার্ডের অনুমতি কী?}
        D -->|ইকোনমি টিকিট| E[শুধুমাত্র সাধারণ লাউঞ্জে প্রবেশ]
        D -->|ভিআইপি বা ফার্স্ট ক্লাস| F[ভিআইপি লাউঞ্জ ও এক্সক্লুসিভ সেবা]
        D -->|পাইলট/স্টাফ| G[ককপিট ও কন্ট্রোল রুমে প্রবেশ]
    end
```

* **Authentication (AuthN):** "আপনি কে?" (Who are you?) — আপনার পরিচয় নিশ্চিত করা। (যেমন: ইউজারনেম ও পাসওয়ার্ড দিয়ে লগইন করা)।
* **Authorization (AuthZ):** "আপনার কী করার ক্ষমতা আছে?" (What are you allowed to do?) — আপনার অনুমোদিত কাজের পরিধি নির্ধারণ করা। (যেমন: একজন সাধারণ ইউজার কি অন্য কারো পোস্ট ডিলিট করতে পারবে? না, কেবল অ্যাডমিন পারবে)।

---

## ২. তুলনামূলক বিশ্লেষণ

| বৈশিষ্ট্য | Authentication (AuthN) | Authorization (AuthZ) |
| :--- | :--- | :--- |
| **মূল প্রশ্ন** | আপনি কে? (Who are you?) | আপনার কী কী করার অনুমতি আছে? (What permissions do you have?) |
| **কখন ঘটে?** | সিস্টেম ব্যবহারের শুরুতে (লগইন পর্যায়ে) | অথেনটিকেশন সফল হওয়ার পর প্রতিটি অ্যাকশনে |
| **যাচাইয়ের মাধ্যম** | পাসওয়ার্ড, বায়োমেট্রিক, OTP, 2FA, JWT টোকেন | রোল (Role), পারমিশন (Permissions), গ্রুপ (Groups), অ্যাক্সেস পলিসি |
| **ব্যর্থ হলে HTTP কোড** | **401 Unauthorized** (আসলে এর নাম হওয়া উচিত ছিল 401 Unauthenticated) | **403 Forbidden** (আপনি লগইন আছেন, কিন্তু এই কাজ করার অনুমতি নেই) |
| **Django-তে ফাংশন/টুল** | `authenticate()`, `login()`, `@login_required` | `user.has_perm()`, `@permission_required`, `Groups` |
| **ব্যবহারকারী পরিবর্তন** | ব্যবহারকারী নিজেই পাসওয়ার্ড পরিবর্তন করতে পারে | সাধারণত অ্যাডমিন বা সিস্টেম রোল দ্বারা নির্ধারিত হয় |

---

## ৩. Django-তে Authentication (AuthN)

Django-তে ব্যবহারকারীর পরিচয় যাচাই করার প্রক্রিয়া:

```python
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# ১. পরিচয় যাচাই করা
user = authenticate(request, username="rahim", password="secretpassword")

if user is not None:
    # ২. সিস্টেমে প্রবেশ করানো (Session তৈরি)
    login(request, user)

# ৩. ভিউতে শুধুমাত্র লগইন করা ইউজারদের প্রবেশের অনুমতি
@login_required
def profile_view(request):
    # request.user.is_authenticated এখানে নিশ্চিতভাবে True
    return render(request, "profile.html")
```

---

## ৪. Django-তে Authorization (AuthZ)

Django-র অথোরাইজেশন সিস্টেম মূলত ৩টি স্তরে কাজ করে:
1. **User Flags:** (`is_active`, `is_staff`, `is_superuser`)
2. **Permissions:** সুনির্দিষ্ট মডেল অ্যাকশন (`add`, `change`, `delete`, `view`)
3. **Groups:** একাধিক পারমিশনের দলীয় বান্ডেল (যেমন: "Editor", "Moderator")

---

### ক. বিল্ট-ইন Model Permissions

আপনি যখনই Django-তে কোনো নতুন Model তৈরি করে `migrate` চালান, Django স্বয়ংক্রিয়ভাবে সেই মডেলের জন্য **৪টি পারমিশন** তৈরি করে:

ধরা যাক আমাদের `blog` অ্যাপে একটি `Post` মডেল আছে:
* `blog.add_post`: নতুন পোস্ট তৈরি করার অনুমতি
* `blog.change_post`: পোস্ট সম্পাদনা (Edit) করার অনুমতি
* `blog.delete_post`: পোস্ট মুছে ফেলার অনুমতি
* `blog.view_post`: পোস্ট দেখার অনুমতি

---

### খ. কোডে পারমিশন চেক করা (`has_perm`):

```python
user = request.user

# নির্দিষ্ট পারমিশন আছে কিনা
if user.has_perm('blog.delete_post'):
    print("ইউজার পোস্ট মুছতে পারবে")
else:
    print("অনুমতি নেই!")

# একাধিক পারমিশন একসাথে চেক:
if user.has_perms(['blog.change_post', 'blog.delete_post']):
    print("উভয় অনুমতি আছে")
```

> 💡 **নোট:** কোনো ইউজারের `is_superuser=True` হলে সে কোনো নির্দিষ্ট পারমিশন অ্যাসাইন করা ছাড়াই স্বয়ংক্রিয়ভাবে সিস্টেমের **সকল পারমিশন** পেয়ে যায়।

---

### গ. Django Groups (দলগত অনুমতি)

প্রতিটি ইউজারকে আলাদা আলাদা পারমিশন না দিয়ে, সমগোত্রীয় কাজের জন্য **Group** তৈরি করা প্রফেশনাল নিয়ম:

```python
from django.contrib.auth.models import Group, Permission

# ১. "Editors" নামের গ্রুপ তৈরি করা
editors_group, created = Group.objects.get_or_create(name='Editors')

# ২. গ্রুপে নির্দিষ্ট পারমিশন যুক্ত করা
can_change = Permission.objects.get(codename='change_post')
can_add = Permission.objects.get(codename='add_post')
editors_group.permissions.add(can_change, can_add)

# ৩. কোনো ইউজারকে সেই গ্রুপে যুক্ত করা
user.groups.add(editors_group)
```

এখন সেই ইউজারের কাছে স্বয়ংক্রিয়ভাবে `blog.add_post` ও `blog.change_post` পারমিশন চলে আসবে।

---

## ৫. Views-এ Authorization প্রয়োগ করা

### ১. `@permission_required` ডেকোরেটর (Function-Based Views)

```python
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post

# raise_exception=True দিলে অনুমতি না থাকলে 403 Forbidden এরর পেজ দেখাবে
@permission_required('blog.delete_post', raise_exception=True)
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
```

---

### ২. `@user_passes_test` ডেকোরেটর (কাস্টম লজিক বা রোল চেক)

নির্দিষ্ট কন্ডিশন দিয়ে ভিউ সুরক্ষিত করা:

```python
from django.contrib.auth.decorators import user_passes_test

# শুধু ম্যানেজাররা ঢুকতে পারবে
def is_manager(user):
    return user.is_authenticated and (user.groups.filter(name='Managers').exists() or user.is_superuser)

@user_passes_test(is_manager, login_url='/access-denied/')
def manager_dashboard(request):
    return render(request, "manager_dashboard.html")
```

---

### ৩. Class-Based Views-এ Authorization (`Mixins`)

```python
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Post

class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = 'blog.delete_post'
    success_url = reverse_lazy('post_list')
    template_name = 'post_confirm_delete.html'
```

---

## ৬. Templates-এ Authorization নিয়ন্ত্রণ

টেমপ্লেটে ইউজারের পারমিশন অনুযায়ী কোনো বাটন বা অপশন দেখানো বা লুকানোর জন্য `perms` অবজেক্ট ব্যবহৃত হয়:

```html
<!-- templates/post_detail.html -->
<div class="card p-4">
    <h2>{{ post.title }}</h2>
    <p>{{ post.content }}</p>

    <div class="mt-3">
        <!-- ১. যে কেউ দেখতে পাবে -->
        <a href="{% url 'post_list' %}" class="btn btn-secondary">ফিরে যান</a>

        <!-- ২. শুধুমাত্র edit পারমিশন থাকলে Edit বাটন দেখাবে -->
        {% if perms.blog.change_post %}
            <a href="{% url 'post_edit' post.pk %}" class="btn btn-warning">সম্পাদনা</a>
        {% endif %}

        <!-- ৩. শুধুমাত্র delete পারমিশন থাকলে Delete বাটন দেখাবে -->
        {% if perms.blog.delete_post %}
            <a href="{% url 'post_delete' post.pk %}" class="btn btn-danger">মুছে ফেলুন</a>
        {% endif %}
    </div>
</div>
```

---

## ৭. কাস্টম পারমিশন (Custom Permissions) তৈরি করা

বিল্ট-ইন ৪টি পারমিশনের বাইরে যদি বিশেষ কোনো বিজনেস লজিকের পারমিশন লাগে (যেমন: "Can publish post", "Can approve review"), তা মডেলের `Meta` ক্লাসে ডিফাইন করতে হয়:

```python
# blog/models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("can_publish_post", "পোস্ট পাবলিশ করার অনুমতি"),
            ("can_mark_featured", "ফিচার্ড পোস্ট হিসেবে চিহ্নিত করার অনুমতি"),
        ]
```

মাইগ্রেশন চালালে (`makemigrations` এবং `migrate`) এই পারমিশনগুলো ডেটাবেজে যুক্ত হয়ে যাবে। এরপর কোডে ব্যবহার করা যাবে:
```python
if request.user.has_perm('blog.can_publish_post'):
    post.is_published = True
```

---

## ৮. Object-Level Authorization (মডেলের মালিকানা যাচাই)

Django-র বিল্ট-ইন পারমিশন হলো **Model-Level** (যেমন: ইউজারের পোস্ট ডিলিট করার ক্ষমতা আছে কি নেই)। কিন্তু **Object-Level** অথোরাইজেশন হলো:
> *"ইউজারের পোস্ট এডিট করার ক্ষমতা আছে, কিন্তু সে কি **শুধুমাত্র নিজের পোস্ট** এডিট করতে পারবে, নাকি অন্যের পোস্টও এডিট করতে পারবে?"*

### ভিউতে সহজ সমাধান:

```python
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 🔥 Object-Level Check: ইউজার কি এই পোস্টের লেখক? অথবা সুপারইউজার?
    if post.author != request.user and not request.user.is_superuser:
        raise PermissionDenied("আপনার এই পোস্টটি সম্পাদনা করার অধিকার নেই!")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "post_form.html", {"form": form})
```

---

## 🎯 আজকের Key Takeaways

1. **Authentication** যাচাই করে "ইউজার কে" (Identity); আর **Authorization** নির্ধারণ করে "ইউজারের কী কী করার অনুমতি আছে" (Permissions)।
2. Authentication ব্যর্থ হলে **401 Unauthorized** (বা রিডাইরেক্ট) এবং Authorization ব্যর্থ হলে **403 Forbidden** এরর দেওয়া হয়।
3. Django প্রতিটি মডেলের জন্য স্বয়ংক্রিয়ভাবে ৪টি পারমিশন তৈরি করে: `add`, `change`, `delete`, `view`।
4. একাধিক পারমিশনকে সহজে পরিচালনা করতে **Groups** তৈরি করে গ্রুপে পারমিশন এবং গ্রুপে ইউজার যুক্ত করা সেরা অভ্যাস।
5. Function-Based ভিউতে `@permission_required` এবং Class-Based ভিউতে `PermissionRequiredMixin` ব্যবহার করুন।
6. টেমপ্লেটে শর্তাধীন UI দেখাতে `perms.<app_label>.<permission_codename>` সিনট্যাক্স ব্যবহার করুন।
7. ব্যবহারকারী যেন শুধুমাত্র তার নিজস্ব ডেটা এডিট করতে পারে, তা নিশ্চিত করতে **Object-Level মালিকানা** (`obj.author == request.user`) যাচাই করুন।

---

## ❓ অনুশীলনী প্রশ্ন

1. Authentication এবং Authorization-এর মধ্যে মূল ৩টি পার্থক্য লিখুন।
2. 401 Unauthorized এবং 403 Forbidden স্ট্যাটাস কোডের মধ্যে পার্থক্য কী?
3. Django-তে একটি নতুন মডেল তৈরি করলে স্বয়ংক্রিয়ভাবে কোন ৪টি পারমিশন তৈরি হয়?
4. `user.has_perm()` মেথডে পারমিশন স্ট্রিং লেখার সঠিক ফরম্যাট কী?
5. Django Groups ব্যবহারের মূল সুবিধা কী? একটি উদাহরণ দিন।
6. `@permission_required` ডেকোরেটরে `raise_exception=True` না দিলে কী ঘটে এবং দিলে কী ঘটে?
7. টেমপ্লেটে শুধুমাত্র মডারেটরদের জন্য Delete বাটন দেখানোর DTL কোড কেমন হবে?
8. Model-Level Permission এবং Object-Level Permission-এর মধ্যে পার্থক্য কী?
9. একটি মডেলে কাস্টম পারমিশন কীভাবে সংজ্ঞায়িত করতে হয়?
10. একজন সাধারণ ইউজার যাতে অন্য ইউজারের প্রোফাইল এডিট করতে না পারে, তা ভিউতে কীভাবে হ্যান্ডেল করবেন?
