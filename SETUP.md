# راهنمای راه‌اندازی پروژه فونیکس

## ابتدا

### نیازمندی‌ها
- Python 3.8+
- MySQL Server

### مراحل نصب

1. **نصب پکیج‌ها:**
```bash
pip install -r requirements.txt
```

2. **ایجاد دیتابیس MySQL:**

قبل از اجرای migrations، دیتابیس MySQL را بسازید:

```sql
CREATE DATABASE phonix_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

اطلاعات اتصال در `config/settings.py`:
- نام دیتابیس: `phonix_db`
- نام کاربری: `H0lwin`
- رمز عبور: `Shayan.1400`
- Host: `localhost`
- Port: `3306`

3. **اجرای Migrations:**
```bash
python manage.py migrate
```

4. **ایجاد سوپریوزر:**
```bash
python manage.py create_superuser
```

یا دستور عادی Django:
```bash
python manage.py createsuperuser
```

اطلاعات پیش‌فرض:
- نام کاربری: `H0lwin`
- ایمیل: `Shayanqasmy88@gmail.com`
- رمز عبور: `Shayan.1400`

5. **جمع‌آوری Static Files (اختیاری):**
```bash
python manage.py collectstatic
```

6. **اجرای سرور توسعه:**
```bash
python manage.py runserver
```

سرور در آدرس `http://localhost:8000` اجرا می‌شود.

## دسترسی‌های مختلف

### پنل سوپر ادمین
آدرس: `http://localhost:8000/superuser-admin/`
- فقط برای سوپریوزر
- دسترسی کامل به همه مدل‌ها

### پنل ادمین کاربران
آدرس: `http://localhost:8000/user-admin/`
- برای کاربران staff
- دسترسی محدود

### پنل ادمین پیش‌فرض Django
آدرس: `http://localhost:8000/admin/`

### داشبورد
آدرس: `http://localhost:8000/dashboard/`
- برای کاربران لاگین‌شده

## ساختار پروژه

```
phonix_dashboard/
├── config/              # تنظیمات پروژه
│   ├── settings.py     # تنظیمات Django
│   ├── urls.py         # URLs اصلی
│   └── wsgi.py
├── accounts/           # برنامه کاربران
│   ├── models.py       # CustomUser و UserGroup
│   ├── admin.py        # Admin panels
│   ├── urls.py
│   ├── views.py
│   └── management/commands/
│       └── create_superuser.py
├── dashboard/          # برنامه داشبورد
│   ├── models.py       # DashboardWidget
│   ├── admin.py
│   ├── urls.py
│   └── views.py
├── templates/          # Template‌های HTML
├── static/             # فایل‌های static (CSS, JS)
├── media/              # فایل‌های آپلود‌شده
└── manage.py
```

## مدل‌ها

### CustomUser
- نسخه‌ی سفارشی‌شده‌ی AbstractUser
- فیلد‌های اضافی: phone_number, role, bio, profile_picture

### UserGroup
- گروه‌بندی کاربران
- دسترسی‌های سطح گروه

### DashboardWidget
- ویجت‌های نمایش‌داده‌شده در داشبورد

## تنظیمات فارسی

- LANGUAGE_CODE: `fa-ir`
- TIME_ZONE: `Asia/Tehran`
- RTL_DIRECTION: `True`
- جهت صفحات: RTL (راست به چپ)
