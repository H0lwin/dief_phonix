# دستورات و یادداشت‌های توسعه

## دستورات مهم

### نصب پکیج‌ها
```bash
pip install -r requirements.txt
```

### ایجاد و اجرای Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### ایجاد سوپریوزر
```bash
python manage.py create_superuser
```

### اجرای سرور
```bash
python manage.py runserver
```

### Lint و Type Check
```bash
# (اگر محیط شامل linter باشد)
# pylint <app>
# mypy <app>
```

## تنظیمات دیتابیس

**نام دیتابیس:** phonix_db
**کاربر:** H0lwin
**رمز عبور:** Shayan.1400
**Host:** localhost
**Port:** 3306

دستور SQL برای ایجاد دیتابیس:
```sql
CREATE DATABASE phonix_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## اطلاعات سوپریوزر

- **نام کاربری:** H0lwin
- **ایمیل:** Shayanqasmy88@gmail.com
- **رمز عبور:** Shayan.1400
- **نام:** شایان
- **نام خانوادگی:** قاسمی

## URLs مهم

- داشبورد: http://localhost:8000/dashboard/
- پنل سوپر ادمین: http://localhost:8000/superuser-admin/
- پنل ادمین کاربران: http://localhost:8000/user-admin/
- پنل ادمین پیش‌فرض: http://localhost:8000/admin/

## توجه‌های مهم

1. دیتابیس MySQL باید قبل از migrate ایجاد شود
2. تمام فیلدهای متن از gettext_lazy استفاده می‌کنند
3. داشبورد RTL (راست به چپ) است
4. زبان پیش‌فرض فارسی است

## انتخاب‌گر خدمات مبتنی بر Modal (جدید)

### ویژگی‌های جدید
- **Modal-based selector**: جایگزین Select2 برای رابط کاربری بهتر
- **Live search**: جستجو بی درنگ برای فیلتر کردن خدمات
- **Auto-load**: هنگام انتخاب دسته‌بندی، modal خودکار باز می‌شود
- **No page refresh**: تمام عملیات بدون تازه‌سازی صفحه

### فایل‌های جدید
- `static/css/service_modal.css` - استایل‌های Modal
- `static/js/service_modal.js` - کد JavaScript اصلی

### فایل‌های تغییر‌یافته
- `static/js/sales_invoice_admin.js` - سرویس modal را فعال می‌کند
- `static/js/purchase_invoice_admin.js` - سرویس modal را فعال می‌کند
- `persons/admin.py` - تغییر Media برای اضافه کردن CSS و JS جدید

### چگونگی استفاده
1. کاربر دسته‌بندی خدمت را انتخاب می‌کند
2. Modal خودکار باز می‌شود و خدمات مرتبط را نمایش می‌دهد
3. کاربر می‌تواند با تایپ جستجو کند
4. پس از انتخاب خدمت، service ID و نام خودکار وارد فیلد می‌شوند
5. Modal بسته می‌شود

### تست کردن
```bash
python manage.py runserver
# برو به: http://localhost:8000/admin/
# نفر → فاکتور فروش → فاکتور جدید
# دسته‌بندی "خدمات بازرگانی" را انتخاب کن
# Modal باید باز شود
```

## گزارش مشتری (جدید)

### نام Model
- **CustomerReport** - گزارش مشتری

### فیلترهای موجود
1. **مشتری** (Person) - اختیاری
2. **دسته‌بندی خدمت** - خدمات بازرگانی، ثبت، حقوقی، لیزینگ، وام
3. **خدمت** (service_id) - بر اساس دسته انتخاب شده
4. **نوع فاکتور** - فروش / خرید / هر دو
5. **نوع تسویه** - نقدی / شرایطی / هر دو
6. **تاریخ** - تاریخ واحد یا بازه تاریخی
7. **کاربر ثبت‌کننده** - برای فیلتر عملکرد کارمندان

### ستون‌های جدول نتایج
| شماره پرونده | تاریخ | نام | نام خانوادگی | نوع | دسته خدمات | خدمت | نوع تسویه | مبلغ | کاربر ثبت‌کننده |

### دسترسی
- **فرم تولید گزارش**: `/reports/customer-report/`
- **نمایش نتایج**: `/reports/customer-report/<id>/`
- **پنل مدیریت**: Admin Panel → گزارش‌های مشتری

### فایل‌های ایجاد شده
- `reports/models.py` - Model CustomerReport
- `reports/forms.py` - Form برای جمع‌آوری فیلترها
- `reports/views.py` - Logic تولید و نمایش گزارش
- `reports/urls.py` - URL patterns
- `reports/admin.py` - ثبت در پنل مدیریت
- `templates/reports/customer_report_form.html` - فرم
- `templates/reports/customer_report_detail.html` - نتایج
