# Lesson 66: Deployment, Backup ও Rollback স্ট্র্যাটেজি 🚀💾🔄

একটি সফল ওয়েব অ্যাপ্লিকেশনের চূড়ান্ত সাফল্য নির্ভর করে তার **ডিপ্লয়মেন্ট প্রসেসের নির্ভরযোগ্যতা** এবং **দুর্যোগ ব্যবস্থাপনা (Disaster Recovery)**-র ওপর। 

লাইভ প্রোডাকশনে কোনো বাগযুক্ত কোড পুশ হলে কয়েক সেকেন্ডের মধ্যে কোটি টাকার ক্ষতি বা ডেটা লস হতে পারে। তাই পেশাদার ব্যাকএন্ড ইঞ্জিনিয়ারদের জন্য তিনটি বিষয় জানা অপরিহার্য:
1. **Zero-Downtime Deployment** (সাইট ডাউন না করে কোড আপডেট)
2. **Robust Automated Backup** (ডেটাবেজ ও মিডিয়া ফাইলের ৩-২-১ ব্যাকআপ নিয়ম)
3. **Instant Rollback Strategy** (বিপদ ঘটলে মুহূর্তের মধ্যে পূর্বাবস্থায় ফিরে যাওয়া)

---

## ১. আধুনিক ডিপ্লয়মেন্ট স্ট্র্যাটেজি 🎯

| পদ্ধতি | কাজের ধরণ | ডাউনটাইম | জটিলতা | উপযুক্ত ক্ষেত্র |
| :--- | :--- | :---: | :---: | :--- |
| **In-Place / Recreate** | পুরোনো প্রসেস বন্ধ করে নতুন কোড চালিয়ে রিস্টার্ট করা | 🔴 ৩০ সেকেন্ড - ২ মিনিট | খুব সহজ | ছোট ব্যক্তিগত প্রজেক্ট |
| **Rolling Deployment** | লোড ব্যালেন্সারের পেছনে একটি একটি করে সার্ভার আপডেট করা | 🟢 ০ সেকেন্ড | মাঝারি | সাধারণ প্রোডাকশন ক্লাস্টার |
| **Blue-Green Deployment** | দুটি আইডেন্টিক্যাল সার্ভার (Blue ও Green); এক ক্লিকে ট্রাফিক সুইচ করা | 🟢 ০ সেকেন্ড (ইনস্ট্যান্ট রোলব্যাক) | উন্নত | এন্টারপ্রাইজ / ফিনটেক সিস্টেম |
| **Canary Deployment** | ৫% ইউজারের কাছে নতুন কোড টেস্ট করে ধীরে ধীরে ১০০% করা | 🟢 ০ সেকেন্ড | সর্বোচ্চ | ফেসবুক, গুগল স্কেল |

---

## ২. স্ট্যান্ডার্ড প্রোডাকশন ডিপ্লয়মেন্ট লাইফসাইকেল ⚙️

```mermaid
flowchart TD
    A[১. CI/CD টেস্ট ও লিন্টিং পাস] --> B[২. প্রি-ডিপ্লয় চেক: check --deploy]
    B --> C[৩. ডেটাবেজ সেফটি ব্যাকআপ নেওয়া]
    C --> D[৪. মাইগ্রেশন রান: migrate --noinput]
    D --> E[৫. স্ট্যাটিক সংগ্রহ: collectstatic]
    E --> F[৬. গ্রেসফুল রিলোড: Gunicorn SIGHUP / Docker Swap]
    F --> G{৭. Health Check পাস করেছে?}
    G -->>|হ্যাঁ| H[ডিপ্লয়মেন্ট সফল! 🎉]
    G -->>|না| I[🚨 অটোমেটিক রোলব্যাক ট্রিগার!]
```

---

## ৩. স্বয়ংসম্পূর্ণ প্রোডাকশন ডিপ্লয়মেন্ট স্ক্রিপ্ট (`deploy.sh`)

একটি স্বয়ংক্রিয় স্ক্রিপ্ট যা ডিপ্লয় করার পূর্বে ব্যাকআপ নেবে এবং হেলথ চেক ফেইল করলে স্বয়ংক্রিয়ভাবে আগের কোডে রোলব্যাক করবে:

```bash
#!/bin/bash
# deploy.sh - Production Safe Deployment Script

set -e # কোনো কমান্ডে এরর হলে স্ক্রিপ্ট থামিয়ে দেবে

APP_DIR="/var/www/myproject"
VENV_DIR="$APP_DIR/venv"
BACKUP_DIR="/var/backups/django"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
PREV_COMMIT=$(git rev-parse HEAD)

echo "=========================================="
echo "🚀 Starting Deployment: $TIMESTAMP"
echo "=========================================="

cd $APP_DIR

# ধাপ ১: জরুরি ডেটাবেজ ব্যাকআপ (ডিপ্লয় শুরুর ঠিক পূর্বে)
echo "💾 Step 1: Taking pre-deployment database snapshot..."
mkdir -p $BACKUP_DIR
pg_dump -U django_user -h 127.0.0.1 -d my_production_db | gzip > "$BACKUP_DIR/pre_deploy_$TIMESTAMP.sql.gz"

# ধাপ ২: গিট থেকে নতুন কোড পুল করা
echo "📥 Step 2: Pulling latest code from main branch..."
git pull origin main

# ধাপ ৩: ডিপেন্ডেন্সি ইনস্টল
echo "📦 Step 3: Installing dependencies..."
$VENV_DIR/bin/pip install --no-cache-dir -r requirements.txt

# ধাপ ৪: ডেটাবেজ মাইগ্রেশন
echo "🗄️ Step 4: Running database migrations..."
$VENV_DIR/bin/python manage.py migrate --noinput

# ধাপ ৫: স্ট্যাটিক ফাইল সংগ্রহ
echo "🎨 Step 5: Collecting static files..."
$VENV_DIR/bin/python manage.py collectstatic --noinput

# ধাপ ৬: ওয়েব সার্ভার গ্রেসফুল রিস্টার্ট (জিরো ডাউনটাইম)
echo "🔄 Step 6: Reloading Gunicorn workers gracefully..."
sudo systemctl reload gunicorn

# ধাপ ৭: স্বয়ংক্রিয় হেলথ চেক
echo "🩺 Step 7: Verifying application health..."
sleep 3
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health/ || true)

if [ "$HEALTH_STATUS" -eq 200 ]; then
    echo "✅ Deployment Successful! Site is healthy (HTTP 200)."
else
    echo "❌ Health check failed with HTTP $HEALTH_STATUS! Triggering EMERGENCY ROLLBACK..."
    
    # ইমার্জেন্সি রোলব্যাক এক্সিকিউশন
    git checkout $PREV_COMMIT
    sudo systemctl restart gunicorn
    echo "⚠️ Rolled back to commit $PREV_COMMIT. Database backup available at $BACKUP_DIR/pre_deploy_$TIMESTAMP.sql.gz"
    exit 1
fi
```

---

## ৪. ব্যাকআপ স্ট্র্যাটেজি: The 3-2-1 Rule 💾

বিশ্বখ্যাত ব্যাকআপ নিয়ম হলো **3-2-1**:
- **৩টি কপি:** আপনার মূল প্রোডাকশন ডেটা সহ মোট ৩টি ডেটা কপি থাকতে হবে।
- **২টি আলাদা মিডিয়া:** লোকাল সার্ভারের ড্রাইভ ছাড়াও ক্লাউড অবজেক্ট স্টোরেজে ডেটা থাকবে।
- **১টি অফ-সাইট কপি:** সম্পূর্ণ আলাদা ভৌগোলিক অঞ্চলের ক্লাউড ডাটা সেন্টারে (যেমন AWS S3 বা Cloudflare R2) এনক্রিপ্ট করে সেভ রাখা।

---

## ৫. স্বয়ংক্রিয় ডেটাবেজ ও মিডিয়া ব্যাকআপ স্ক্রিপ্ট (`backup.sh`)

প্রতি রাতে ডেটাবেজের ব্যাকআপ নেওয়া, ফাইল কম্প্রেশন করা, পুরোনো ৭ দিনের ব্যাকআপ মুছে ফেলা এবং ক্লাউডে সিঙ্ক করার স্ক্রিপ্ট:

```bash
#!/bin/bash
# backup.sh - Daily Automated Backup & S3 Sync Script

BACKUP_DIR="/backups/django"
DATE=$(date +"%Y-%m-%d")
DB_NAME="my_production_db"
S3_BUCKET="s3://my-company-backups/django"

mkdir -p $BACKUP_DIR

# ১. PostgreSQL ডেটাবেজ ডাম্প ও কম্প্রেশন
echo "Dumping database: $DB_NAME..."
pg_dump -U postgres -h 127.0.0.1 $DB_NAME | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# ২. ক্লাউড স্টোরেজে (AWS S3) ব্যাকআপ ফাইল আপলোড
echo "Syncing backup to AWS S3..."
aws s3 cp "$BACKUP_DIR/db_$DATE.sql.gz" "$S3_BUCKET/db_$DATE.sql.gz"

# ৩. মিডিয়া ফাইল ব্যাকআপ (ব্যবহারকারীর আপলোড করা ফাইল)
echo "Syncing media files to S3..."
aws s3 sync /var/www/myproject/media/ "$S3_BUCKET/media_backup/" --delete

# ৪. লোকাল ডিস্ক খালি রাখতে ৭ দিনের পুরোনো ব্যাকআপ ফাইল অটোমেটিক ডিলিট
find $BACKUP_DIR -type f -name "db_*.sql.gz" -mtime +7 -exec rm {} \;

echo "Backup completed successfully for $DATE!"
```

### লিনাক্স ক্রন জবে শিডিউল করা (`crontab -e`):
```bash
# প্রতিদিন রাত ৩:০০ টায় ব্যাকআপ স্ক্রিপ্ট স্বয়ংক্রিয়ভাবে রান করবে
0 3 * * * /bin/bash /var/scripts/backup.sh >> /var/log/backup.log 2>&1
```

---

## ৬. ইমার্জেন্সি রোলব্যাক প্ল্যান (When Things Go Wrong) 🚨

যখন লাইভ প্রোডাকশনে গুরুতর কোনো এরর ধরা পড়ে, প্যানিক না করে নিচের তিনটি স্তরে রোলব্যাক পরিচালনা করতে হয়:

```mermaid
flowchart LR
    Bug[ক্র্যাশ বা বাগ ধরা পড়ল] --> Choice{সমস্যাটি কীসের?}
    
    Choice -->|শুধুমাত্র কোড বাগ| CodeRollback[১. কোড রোলব্যাক\ngit checkout HEAD~1\nঅথবা docker rollback]
    Choice -->|মাইগ্রেশন সহ বাগ| DBRollback[২. মাইগ্রেশন রিভার্ট\nmanage.py migrate app 0003]
    Choice -->|মারাত্মক ডেটা করাপশন| FullRestore[৩. পূর্ণাঙ্গ ডেটাবেজ রিস্টোর\ngunzip < backup.sql.gz | psql]
```

### ক. কোড রোলব্যাক (Git বা Docker):
```bash
# গিট দিয়ে আগের কমিটে ফিরে যাওয়া
git checkout <previous_commit_hash>
sudo systemctl restart gunicorn

# ডকার দিয়ে আগের ট্যাগ করা ইমেজ রান করা
docker run -d -p 8000:8000 myapp:v1.2.3  # বাগযুক্ত v1.2.4 বাদ দিয়ে
```

### খ. মাইগ্রেশন রোলব্যাক:
যদি ডেটাবেজ মাইগ্রেশন কোনো ভুল টেবিল পরিবর্তন করে থাকে এবং মাইগ্রেশনটি রিভার্সিবল হয়:
```bash
python manage.py migrate accounts 0002_previous_good_migration
```

### গ. ডেটাবেজ রিস্টোর (পূর্ণাঙ্গ ব্যাকআপ পুনঃস্থাপন):
যদি ডেটা নষ্ট বা মুছে যায়, তাহলে ডিপ্লয়মেন্টের পূর্বের স্ন্যাপশট থেকে ডেটাবেজ পুনরুদ্ধার করুন:
```bash
# ডেটাবেজের রানিং কানেকশন ড্রপ করে ফ্রেশ রিস্টোর করা
dropdb -U postgres -h 127.0.0.1 my_production_db
createdb -U postgres -h 127.0.0.1 my_production_db
gunzip < /var/backups/django/pre_deploy_20260610.sql.gz | psql -U postgres -h 127.0.0.1 my_production_db
```

---

## প্রোডাকশন চেকলিস্ট 📋

1. ✅ প্রতিটি ডিপ্লয়মেন্টের পূর্বে **অটোমেটিক প্রি-ডিপ্লয় ডেটাবেজ ব্যাকআপ** নিশ্চিত করা হয়েছে।
2. ✅ ডিপ্লয়মেন্ট শেষে স্বয়ংক্রিয়ভাবে **`/health/` এন্ডপয়েন্টে পিং** করে স্ট্যাটাস ২০০ যাচাই করা হয়।
3. ✅ নাইটলি অটোমেটিক ডেটাবেজ ব্যাকআপের জন্য **Cron Job এবং AWS S3 অফ-সাইট সিঙ্ক** সক্রিয় আছে।
4. ✅ আপলোড করা মিডিয়া ফাইলের জন্য **S3 Bucket Versioning** চালু আছে (ভুলবশত ফাইল মুছে গেলে পুনরুদ্ধারের জন্য)।
5. ✅ টিমের সবার কাছে আপদকালীন **রোলব্যাক প্লেবুক** ডকুমেন্টেড রয়েছে।
