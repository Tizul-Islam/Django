# Django File Upload ও Media Files 📁🚀

ওয়েব অ্যাপ্লিকেশনে ব্যবহারকারীর কাছ থেকে প্রোফাইল ছবি, পিডিএফ ডকুমেন্ট, সিভি বা ভিডিও গ্রহণ ও সংরক্ষণ করার প্রক্রিয়াকে **File Upload** বলা হয়।

Django-তে ব্যবহারকারীর আপলোড করা ফাইলগুলোকে বলা হয় **Media Files** (যা ডেভেলপারদের Static Files যেমন CSS/JS থেকে সম্পূর্ণ আলাদা)। এই গাইডে আমরা ফাইল ও ছবি আপলোডের শুরু থেকে শেষ পর্যন্ত — কনফিগারেশন, নিরাপত্তা ভ্যালিডেশন, ইমেজ রিসাইজিং এবং সার্ভার থেকে পুরানো ফাইল স্বয়ংক্রিয়ভাবে ডিলিট করার কৌশল শিখব।

---

## ১. Static Files বনাম Media Files

| বৈশিষ্ট্য | Static Files | Media Files |
| :--- | :--- | :--- |
| **উৎস** | ডেভেলপার তৈরি করেন (CSS, JS, Logos, Icons) | সাধারণ ব্যবহারকারী আপলোড করেন (Avatar, PDF, CV) |
| **পরিবর্তনশীলতা** | সাইট চলার সময় সাধারণত অপরিবর্তিত থাকে | ব্যবহারকারীর যেকোনো সময় নতুন ফাইল যোগ/মুছে যায় |
| **Settings** | `STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT` | `MEDIA_URL`, `MEDIA_ROOT` |

---

## ২. পরিবেশ প্রস্তুতি ও Settings কনফিগারেশন

### ধাপ ১: Pillow লাইব্রেরি ইনস্টল করা
Django-র `ImageField` ব্যবহার করতে হলে পাইথনের ইমেজ প্রসেসিং লাইব্রেরি **Pillow** থাকা বাধ্যতামূলক:

```bash
pip install pillow
```

---

### ধাপ ২: `settings.py` কনফিগার করা

প্রজেক্টের মূল `settings.py`-এর নিচে মিডিয়া পাথ যুক্ত করুন:

```python
# config/settings.py
import os
from pathlib import Path

# ব্রাউজারে ফাইলের URL কেমন হবে (যেমন: http://127.0.0.1:8000/media/avatars/pic.jpg)
MEDIA_URL = '/media/'

# ফাইলগুলো হার্ডডিস্কের কোন ফোল্ডারে সেভ হবে (প্রজেক্ট রুটে media ফোল্ডার তৈরি হবে)
MEDIA_ROOT = BASE_DIR / 'media'
```

---

### ধাপ ৩: `urls.py`-এ Media রুট যুক্ত করা (Development Mode)

লোকাল সার্ভারে আপলোড করা ফাইলগুলো যেন ব্রাউজারে লিঙ্ক দিয়ে দেখা যায়, তার জন্য `config/urls.py`-এ নিচের অংশ যুক্ত করতে হয়:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
]

# শুধুমাত্র লোকাল ডেভেলপমেন্ট চলাকালীন মিডিয়া ফাইল সার্ভ করার জন্য:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

> ⚠️ **মনে রাখুন:** প্রোডাকশন সার্ভারে (যেমন: Nginx বা Apache) ওয়েব সার্ভার সরাসরি মিডিয়া ফাইল সার্ভ করে; তখন Django নিজে ফাইল সার্ভ করে না।

---

## ৩. Model তৈরি (`FileField` ও `ImageField`)

ফাইল সংরক্ষণের জন্য `models.FileField` এবং ছবি সংরক্ষণের জন্য `models.ImageField` ব্যবহার করা হয়।

### ডাইনামিক ও কাস্টম `upload_to` পাথ:

```python
# accounts/models.py
import os
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# ফাইলের নাম পরিবর্তন করে ইউনিক UUID নাম দেওয়ার ফাংশন:
def user_directory_path(instance, filename):
    # filename থেকে এক্সটেনশন আলাদা করা (যেমন: .png বা .pdf)
    ext = filename.split('.')[-1]
    # ইউনিক নাম তৈরি: e.g. 550e8400-e29b-41d4-a716-446655440000.png
    new_filename = f"{uuid.uuid4()}.{ext}"
    # ইউজারের আইডি অনুযায়ী আলাদা সাব-ফোল্ডারে সেভ: media/users/user_1/filename.png
    return os.path.join(f'users/user_{instance.user.id}/', new_filename)

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name="ডকুমেন্টের নাম")
    
    # সাধারণ ফাইল (PDF, Docx):
    file = models.FileField(upload_to='documents/%Y/%m/')  # বছর/মাস অনুযায়ী ফোল্ডার হবে
    
    # ছবি ফিল্ড (কাস্টম রিনেম ফাংশন সহ):
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

---

## ৪. ফাইল ভ্যালিডেশন (সাইজ ও এক্সটেনশন সীমাবদ্ধ করা) 🛡️

কোনো ইউজার যেন বিশাল সাইজের ফাইল (যেমন: 50MB) বা বিপজ্জনক এক্সিকিউটেবল ফাইল (`.exe`, `.sh`) আপলোড করতে না পারে, সেজন্য কাস্টম ভ্যালিডেটর লিখতে হয়:

```python
# accounts/validators.py
import os
from django.core.exceptions import ValidationError

# ১. ফাইল সাইজ ভ্যালিডেটর (সর্বোচ্চ 2 MB)
def validate_file_size(value):
    filesize = value.size
    max_size_mb = 2
    if filesize > max_size_mb * 1024 * 1024:
        raise ValidationError(f"ফাইলের আকার সর্বোচ্চ {max_size_mb} MB হতে পারে! আপনার ফাইলটি অনেক বড়।")

# ২. এক্সটেনশন ভ্যালিডেটর
def validate_pdf_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError("শুধুমাত্র PDF অথবা DOCX ফাইল আপলোড গ্রহণযোগ্য!")
```

### মডেলে ভ্যালিডেটর যুক্ত করা:
```python
file = models.FileField(
    upload_to='documents/', 
    validators=[validate_file_size, validate_pdf_extension]
)
```

---

## ৫. ফাইল আপলোড Form ও View হ্যান্ডলিং

### ধাপ ১: Form তৈরি (`forms.py`)

```python
# accounts/forms.py
from django import forms
from .models import Document

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
```

---

### ধাপ ২: View তৈরি (`views.py`)

> ⚠️ **সবচেয়ে গুরুত্বপূর্ণ নিয়ম:**
> ফাইল আপলোডের সময় ভিউতে অবশ্যই `request.POST`-এর পাশাপাশি **`request.FILES`** পাস করতে হবে! অন্যথায় ফাইল ফিল্ড খালি থাকবে।

```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DocumentUploadForm
from .models import Document

@login_required
def upload_document_view(request):
    if request.method == "POST":
        # 🔥 request.POST এবং request.FILES দুটিই দিতে হবে
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            messages.success(request, "ফাইল সফলভাবে আপলোড হয়েছে!")
            return redirect('document_list')
        else:
            messages.error(request, "আপলোডে ত্রুটি হয়েছে! নিচে দেখুন।")
    else:
        form = DocumentUploadForm()

    return render(request, "accounts/upload.html", {"form": form})
```

---

### ধাপ ৩: Template তৈরি (`upload.html`)

> ⚠️ **সবচেয়ে গুরুত্বপূর্ণ HTML অ্যাট্রিবিউট:**
> `<form>` ট্যাগে অবশ্যই **`enctype="multipart/form-data"`** থাকতে হবে। এটি না থাকলে ব্রাউজার শুধু ফাইলের নাম পাঠাবে, আসল ফাইল পাঠাবে না!

```html
<!-- templates/accounts/upload.html -->
<form method="POST" enctype="multipart/form-data" novalidate>
    {% csrf_token %}

    {% for field in form %}
        <div class="mb-3">
            <label class="form-label fw-bold">{{ field.label }}</label>
            {{ field }}
            {% for error in field.errors %}
                <span class="text-danger small">{{ error }}</span>
            {% endfor %}
        </div>
    {% endfor %}

    <button type="submit" class="btn btn-primary">আপলোড করুন</button>
</form>
```

---

### ধাপ ৪: টেমপ্লেটে আপলোড করা ফাইল প্রদর্শন বা ডাউনলোড

```html
<!-- templates/accounts/document_list.html -->
<table class="table">
    <thead>
        <tr>
            <th>ছবি</th>
            <th>শিরোনাম</th>
            <th>ফাইল লিঙ্ক</th>
            <th>আকার</th>
        </tr>
    </thead>
    <tbody>
        {% for doc in documents %}
            <tr>
                <td>
                    {% if doc.image %}
                        <!-- doc.image.url দিয়ে ফাইলের ব্রাউজার লিঙ্ক পাওয়া যায় -->
                        <img src="{{ doc.image.url }}" width="50" height="50" class="rounded">
                    {% else %}
                        <span class="text-muted">ছবি নেই</span>
                    {% endif %}
                </td>
                <td>{{ doc.title }}</td>
                <td>
                    {% if doc.file %}
                        <a href="{{ doc.file.url }}" target="_blank" class="btn btn-sm btn-outline-info">
                            <i class="bi bi-download"></i> ডাউনলোড
                        </a>
                    {% endif %}
                </td>
                <td>{{ doc.file.size|filesizeformat }}</td>
            </tr>
        {% endfor %}
    </tbody>
</table>
```

---

## ৬. Pillow দিয়ে আপলোডের সময় ছবি স্বয়ংক্রিয়ভাবে রিসাইজ করা 🖼️

ইউজার মোবাইল বা ক্যামেরা থেকে ৫-১০ মেগাবাইট এবং 4000x3000 পিক্সেলের বিশাল ছবি আপলোড করতে পারে। মডেলের `save()` মেথড ওভাররাইড করে ছবিকে স্বয়ংক্রিয়ভাবে কমিয়ে (Optimize) নেওয়া যায়:

```python
# accounts/models.py
from PIL import Image

class Document(models.Model):
    # ... আগের ফিল্ডসমূহ ...

    def save(self, *args, **kwargs):
        # প্রথমে সাধারণ সেভ করা
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            # ছবির সাইজ 800x800 এর চেয়ে বড় হলে রেশিও ঠিক রেখে রিসাইজ করা
            max_size = (800, 800)
            if img.height > 800 or img.width > 800:
                img.thumbnail(max_size)
                # রিসাইজ করা ছবিটি আগের ফাইলে রিপ্লেস করে সেভ করা (Quality 85% দিয়ে হালকা করা)
                img.save(self.image.path, quality=85, optimize=True)
```

---

## ৭. ডেটাবেজ থেকে অবজেক্ট ডিলিট হলে সার্ভারের ফাইল ক্লিনআপ করা 🧹

ডিফল্টভাবে Django কোনো মডেল ডিলিট করলেও মিডিয়া ফোল্ডারে ফাইলটি রেখে দেয়। এটি ক্লিন করতে সিগন্যাল ব্যবহার করা যায়:

```python
# accounts/signals.py
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Document

@receiver(post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    # ১. ডকুমেন্ট ফাইল ডিলিট
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)

    # ২. ইমেজ ফাইল ডিলিট
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
```

> 💡 **জনপ্রিয় থার্ড-পার্টি প্যাকেজ:** আপনি চাইলে কোনো কোড না লিখে সরাসরি `django-cleanup` লাইব্রেরি ব্যবহার করতে পারেন (`pip install django-cleanup`), যা স্বয়ংক্রিয়ভাবে ফাইল ক্লিনআপ করে দেয়।

---

## 🎯 আজকের Key Takeaways

1. **Media Files** হলো ব্যবহারকারীর আপলোড করা ফাইল; এদের পাথ নির্ধারণে `MEDIA_URL` ও `MEDIA_ROOT` ব্যবহার হয়।
2. `ImageField` ব্যবহার করার পূর্বে অবশ্যই `Pillow` লাইব্রেরি ইনস্টল করতে হয় (`pip install pillow`)।
3. HTML ফর্ম ট্যাগে **`enctype="multipart/form-data"`** না থাকলে কোনো ফাইল আপলোড হবে না।
4. ভিউতে ফর্ম ইনস্ট্যান্স করার সময় অবশ্যই `form = Form(request.POST, request.FILES)` পাস করতে হবে।
5. টেমপ্লেটে ফাইলের URL পেতে `{{ object.file.url }}` এবং সুন্দর সাইজ দেখতে `{{ object.file.size|filesizeformat }}` ফিল্টার ব্যবহার করুন।
6. সুরক্ষার জন্য ফাইল সাইজ সীমাবদ্ধ করুন এবং এলোমেলো নাম (UUID) দিয়ে ফাইল রিনেম করুন।
7. ছবির সাইজ কমাতে Pillow দিয়ে `img.thumbnail()` ব্যবহার করে ব্যাকএন্ডেই অপ্টিমাইজ করুন।

---

## ❓ অনুশীলনী প্রশ্ন

1. Django-তে Static Files এবং Media Files-এর মধ্যে মূল পার্থক্য কী?
2. `settings.py`-এ `MEDIA_URL` এবং `MEDIA_ROOT` সেটিংস দুটির কাজ কী?
3. `ImageField` ব্যবহারের পূর্বে কোন পাইথন লাইব্রেরি ইনস্টল করা আবশ্যক?
4. HTML ফর্ম ট্যাগে `enctype="multipart/form-data"` না দিলে কী সমস্যা হবে?
5. ভিউতে `request.POST` থাকা সত্ত্বেও কেন `request.FILES` আলাদাভাবে পাস করতে হয়?
6. ফাইল আপলোডের ক্ষেত্রে মূল ফাইলের নাম সরাসরি ব্যবহার না করে কেন UUID দিয়ে রিনেম করা নিরাপদ?
7. টেমপ্লেটে আপলোড করা ছবির আসল ফাইল সাইজ মানুষের সহজে পড়ার উপযোগী ফরম্যাটে (যেমন: 1.5 MB) দেখানোর জন্য কোন DTL ফিল্টার ব্যবহার করা হয়?
8. ডেভেলপমেন্ট মোডে ব্রাউজারে মিডিয়া ফাইল প্রদর্শনের জন্য `urls.py`-এ কোন কোড যোগ করতে হয়?
9. ব্যবহারকারী কোনো মডেলের রেকর্ড ডেটাবেজ থেকে মুছে ফেললে সার্ভারের হার্ডডিস্ক থেকে ফাইল ডিলিট করার কৌশল কী?
10. ব্যবহারকারী যেন 5 MB-র বেশি সাইজের ফাইল আপলোড করতে না পারে, তার জন্য ভ্যালিডেশন কীভাবে লিখতে হয়?
