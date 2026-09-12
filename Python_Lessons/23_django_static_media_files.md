# Django: Static Files ও Media Files 🎨📁

Django প্রজেক্টে CSS, JS, Images ইত্যাদি ফাইল **Static Files** এবং user-দ্বারা আপলোড করা ফাইল **Media Files** বলে। এই লেসনে দুটোই বিস্তারিত শিখবো।

---

## ১. Static Files কী?

**Static Files** হলো সেই ফাইলগুলো যা project-এ স্থির থাকে এবং সব user-এর জন্য একই থাকে। যেমন:
- CSS ফাইল
- JavaScript ফাইল
- Images (logo, banner ইত্যাদি)
- Fonts
- PDF ডকুমেন্ট

এই ফাইলগুলো developer নিজে যোগ করে, user আপলোড করে না।

---

## ২. Media Files কী?

**Media Files** হলো user দ্বারা আপলোড করা ফাইল। যেমন:
- Profile picture
- Blog post-এর image
- Document upload
- Video/Audio

এই ফাইলগুলো database-এ store হয় না, ফাইল সিস্টেমে store হয় এবং database-এ শুধু পাথ থাকে।

---

## ৩. Static Files সেটআপ

### ধাপ ১: `settings.py`-এ config

```python
# config/settings.py

# URL prefix for static files
STATIC_URL = "static/"

# Project-level static files (common CSS, JS, images)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Production-এর জন্য (collectstatic করলে এখানে যাবে)
STATIC_ROOT = BASE_DIR / "staticfiles"
```

### ধাপ ২: static ফোল্ডার তৈরি করা

```
my_project/
├── static/                    # project-level static
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       └── logo.png
├── blog/
│   └── static/                # app-level static
│       └── blog/
│           ├── css/
│           └── images/
└── config/
    └── settings.py
```

> 💡 App-level static-এর নাম `app_name/static/app_name/` রাখুন যাতে collision না হয়।

---

## ৪. Template-এ Static Files ব্যবহার করা

### `{% load static %}` লোড করা:

```html
{% load static %}

<!DOCTYPE html>
<html>
<head>
    <title>আমার সাইট</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <img src="{% static 'images/logo.png' %}" alt="Logo">
    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>
```

### CSS ফাইল:

```css
/* static/css/style.css */
body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
}

h1 {
    color: #333;
}
```

### JavaScript ফাইল:

```javascript
// static/js/script.js
console.log("Django static file loaded!");

function greet() {
    alert("হ্যালো!");
}
```

---

## ৫. App-level Static Files

প্রতিটা app-এর নিজস্ব static ফাইল থাকতে পারে।

```
blog/
└── static/
    └── blog/
        ├── css/
        │   └── blog_style.css
        └── images/
            └── default_avatar.png
```

Template-এ:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'blog/css/blog_style.css' %}">
<img src="{% static 'blog/images/default_avatar.png' %}">
```

---

## ৬. `collectstatic` কমান্ড

Production-এ সব static files একটা জায়গায় collect করতে:

```bash
python manage.py collectstatic
```

এটা `STATIC_ROOT`-এ নির্দিষ্ট ফোল্ডারে সব static files কপি করবে।

```
staticfiles/
├── admin/
├── css/
├── js/
└── images/
```

> ⚠️ Development-এ `collectstatic` করার দরকার নেই, `DEBUG = True` থাকলে Django স্বয়ংক্রিয়ভাবে serve করে।

---

## ৭. `{% static %}` বনাম hardcoded URL

### ভালো পদ্ধতি:

```html
<!-- ✅ সঠিক -->
<img src="{% static 'images/logo.png' %}">
```

### খারাপ পদ্ধতি:

```html
<!-- ❌ ভুল -->
<img src="/static/images/logo.png">
```

`{% static %}` ব্যবহার করলে `STATIC_URL` পরিবর্তন করলে সব জায়গায় স্বয়ংক্রিয়ভাবে পরিবর্তন হয়।

---

## ৮. Media Files সেটআপ

### ধাপ ১: `settings.py`-এ config

```python
# config/settings.py

# URL prefix for media files
MEDIA_URL = "media/"

# যেখানে media files store হবে
MEDIA_ROOT = BASE_DIR / "media"
```

### ধাপ ২: `urls.py`-এ media URL যুক্ত করা

```python
# config/urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # ...
]

# Development-এ media files serve করার জন্য
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

> ⚠️ Production-এ web server (Nginx/Apache) দিয়ে media serve করতে হয়।

---

## ৯. Model-এ ImageField ও FileField

### ImageField:

```python
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.username
```

### FileField:

```python
class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

### `upload_to` অপশন:

```python
# সরাসরি ফোল্ডারে
avatar = models.ImageField(upload_to="avatars/")

# ফাংশন দিয়ে dynamic path
def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"

avatar = models.ImageField(upload_to=user_directory_path)
```

---

## ১০. Pillow ইনস্টল করা

`ImageField` ব্যবহার করতে `Pillow` লাগে।

```bash
pip install Pillow
```

requirements.txt-এ যোগ করুন:

```
Pillow==10.1.0
```

---

## ১১. Media Files-এর জন্য Form

### ModelForm:

```python
# blog/forms.py
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
```

### View:

```python
# blog/views.py
from django.shortcuts import render, redirect
from .forms import ProfileForm

def update_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "profile.html", {"form": form})
```

> ⚠️ File upload-এর জন্য form-এ `request.FILES` পাঠাতে হবে।

### Template:

```html
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">আপডেট</button>
</form>
```

> ⚠️ `enctype="multipart/form-data"` অবশ্যই দিতে হবে file upload-এর জন্য।

---

## ১২. Template-এ Media Files দেখানো

### Image দেখানো:

```html
{% if profile.avatar %}
    <img src="{{ profile.avatar.url }}" alt="Avatar">
{% else %}
    <img src="{% static 'images/default_avatar.png' %}" alt="Default">
{% endif %}
```

### File download link:

```html
<a href="{{ document.file.url }}" download>{{ document.title }}</a>
```

### Image-এর URL:

```python
# Python code-এ
profile.avatar.url    # /media/avatars/photo.jpg
profile.avatar.path   # /full/path/to/media/avatars/photo.jpg
profile.avatar.name   # avatars/photo.jpg
```

---

## ১৩. Image Resize করা (Pillow দিয়ে)

```python
from PIL import Image
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
```

---

## ১৪. File Validation

```python
from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError(f"ফাইলের সাইজ {max_size // (1024*1024)}MB এর বেশি হতে পারবে না")

class Document(models.Model):
    file = models.FileField(upload_to="documents/", validators=[validate_file_size])
```

### Image format validation:

```python
def validate_image_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("শুধু JPG, JPEG, PNG, GIF ফাইল আপলোড করা যাবে")
```

---

## ১৫. Default Image সেট করা

```python
avatar = models.ImageField(
    upload_to="avatars/",
    default="avatars/default.png",
    blank=True,
)
```

`default`-এ দেওয়া path `MEDIA_ROOT` থেকে relative হবে।

---

## ১৬. Development vs Production

### Development (`DEBUG = True`):

```python
# config/urls.py
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

Django নিজে static ও media serve করে।

### Production (`DEBUG = False`):

1. `collectstatic` চালান:
```bash
python manage.py collectstatic
```

2. Web server (Nginx/Apache) দিয়ে serve করুন।

Nginx config:
```nginx
location /static/ {
    alias /var/www/my_project/staticfiles/;
}

location /media/ {
    alias /var/www/my_project/media/;
}
```

---

## ১৭. একটা সম্পূর্ণ উদাহরণ

### settings.py:

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
```

### models.py:

```python
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png", blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
```

### forms.py:

```python
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]
```

### views.py:

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {"form": form})
```

### urls.py:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]
```

### Template:

```html
<!-- edit_profile.html -->
{% extends "base.html" %}
{% load static %}

{% block content %}
<h1>প্রোফাইল এডিট</h1>

<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">সেভ</button>
</form>
{% endblock %}
```

### base.html:

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>আমার সাইট</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    {% if user.profile.avatar %}
        <img src="{{ user.profile.avatar.url }}" alt="Avatar" width="50">
    {% else %}
        <img src="{% static 'images/default_avatar.png' %}" alt="Avatar" width="50">
    {% endif %}

    {% block content %}{% endblock %}

    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>
```

---

## ১৮. সাধারণ সমস্যা ও সমাধান

### সমস্যা ১: Static files লোড হচ্ছে না

**সমাধান:**
1. `settings.py`-এ `STATICFILES_DIRS` ও `STATIC_URL` চেক করুন
2. Template-এ `{% load static %}` লিখেছেন কিনা চেক করুন
3. `python manage.py collectstatic` চালান

### সমস্যা ২: Media files লোড হচ্ছে না

**সমাধান:**
1. `urls.py`-এ `static(settings.MEDIA_URL, ...)` যোগ করা আছে কিনা চেক করুন
2. `DEBUG = True` আছে কিনা চেক করুন
3. Model-এ `upload_to` ঠিক আছে কিনা চেক করুন

### সমস্যা ৩: File upload হচ্ছে না

**সমাধান:**
1. Form-এ `enctype="multipart/form-data"` আছে কিনা চেক করুন
2. View-এ `request.FILES` পাঠাচ্ছেন কিনা চেক করুন
3. `MEDIA_ROOT` ফোল্ডারটা আছে কিনা চেক করুন

### সমস্যা ৪: `Pillow` error

**সমাধান:**
```bash
pip install Pillow
```

---

## ১৯. সেরা প্র্যাকটিস (Best Practices)

1. ✅ সব static files-এর জন্য `{% static %}` ব্যবহার করুন
2. ✅ App-level static-এর নাম `app_name/static/app_name/` রাখুন
3. ✅ Media files-এর জন্য `upload_to` সঠিকভাবে সেট করুন
4. ✅ File upload form-এ `enctype="multipart/form-data"` দিন
5. ✅ View-এ `request.FILES` পাঠান
6. ✅ File size ও format validation যোগ করুন
7. ✅ Production-এ `collectstatic` চালান
8. ✅ `media/` ও `staticfiles/` ফোল্ডার `.gitignore`-এ রাখুন
9. ❌ Static ও media files database-এ store করবেন না

---

## ২০. `.gitignore`

```gitignore
# Media files
media/

# Static files (collectstatic)
staticfiles/

# Python
__pycache__/
*.pyc

# Database
db.sqlite3
```

---

## ২১. Practical Exercise

```bash
# ১. Pillow ইনস্টল করুন
pip install Pillow

# ২. static ফোল্ডার তৈরি করুন
mkdir static\css
mkdir static\js
mkdir static\images

# ৩. media ফোল্ডার তৈরি করুন
mkdir media

# ৪. collectstatic চালান
python manage.py collectstatic
```

### CSS ফাইল তৈরি করুন:

```css
/* static/css/style.css */
body {
    margin: 0;
    padding: 20px;
    font-family: Arial, sans-serif;
    background: #f0f0f0;
}

h1 {
    color: #2c3e50;
}

.btn {
    background: #3498db;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
```

### Model:

```python
# blog/models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

### Template:

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <h1>{{ post.title }}</h1>
    {% if post.image %}
        <img src="{{ post.image.url }}" alt="{{ post.title }}" style="max-width: 100%;">
    {% endif %}
    <p>{{ post.content }}</p>
    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>
```

---

## 🎯 আজকের Key Takeaways

### Static Files:
1. **Static Files** = CSS, JS, Images (developer যোগ করে)
2. `STATIC_URL = "static/"` — URL prefix
3. `STATICFILES_DIRS` — project-level static ফোল্ডার
4. `STATIC_ROOT` — production-এর জন্য collectstatic path
5. `{% load static %}` + `{% static 'path' %}` — template-এ ব্যবহার
6. `python manage.py collectstatic` — production-এর জন্য

### Media Files:
1. **Media Files** = user আপলোড করা ফাইল
2. `MEDIA_URL = "media/"` — URL prefix
3. `MEDIA_ROOT = BASE_DIR / "media"` — store হওয়ার জায়গা
4. `ImageField` ও `FileField` — model-এ ব্যবহার
5. `upload_to` — কোন ফোল্ডারে store হবে
6. `request.FILES` + `enctype="multipart/form-data"` — upload
7. `{{ object.field.url }}` — template-এ দেখানো
8. `Pillow` install করতে হবে ImageField-এর জন্য

---

## ❓ অনুশীলনী প্রশ্ন

1. Static ও Media Files এর পার্থক্য কী?
2. `STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT` এর কাজ কী?
3. Template-এ static file কীভাবে লোড করা যায়?
4. `{% static %}` ব্যবহারের সুবিধা কী?
5. Media Files-এর জন্য `MEDIA_URL` ও `MEDIA_ROOT` কী?
6. `ImageField` ও `FileField` এর পার্থক্য কী?
7. File upload form-এ `enctype="multipart/form-data"` কেন দরকার?
8. View-এ `request.FILES` কেন পাঠাতে হয়?
9. Template-এ media file কীভাবে দেখানো যায়?
10. `collectstatic` কমান্ডের কাজ কী?
