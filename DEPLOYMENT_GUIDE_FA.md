# راهنمای کامل استقرار پروژه Phonix Dashboard

## فهرست مطالب
1. [معرفی پروژه](#معرفی-پروژه)
2. [پیش‌نیازها](#پیش‌نیازها)
3. [تهیه سرور](#تهیه-سرور)
4. [کلون کردن پروژه](#کلون-کردن-پروژه)
5. [نصب وابستگی‌ها](#نصب-وابستگی‌ها)
6. [پیکربندی دیتابیس](#پیکربندی-دیتابیس)
7. [پیکربندی محیط Django](#پیکربندی-محیط-django)
8. [پیکربندی Apache و SSL](#پیکربندی-apache-و-ssl)
9. [ساخت کاربر مدیریت](#ساخت-کاربر-مدیریت)
10. [راه‌اندازی و تست](#راه‌اندازی-و-تست)
11. [نظارت و نگهداری](#نظارت-و-نگهداری)

---

## معرفی پروژه

**Phonix Dashboard** یک اپلیکیشن مدیریتی تکاملی است که با Django و Python نوشته شده و امکانات زیر را فراهم می‌کند:

- **مدیریت شخصیت‌ها**: ثبت و مدیریت اطلاعات افراد
- **خدمات و سرویس‌ها**: مدیریت تمامی خدمات ارائه‌شده
- **مالی و حسابداری**: ردیابی درآمد، هزینه‌ها و تراکنش‌ها
- **گزارش‌گیری**: تولید گزارش‌های تفصیلی و آماری
- **داشبورد**: نمایش خلاصه‌ای از عملکرد و وضعیت سیستم

این پروژه برای محیط‌های تولید (Production) در نظر گرفته شده و دارای ویژگی‌های امنیتی مقدماتی است.

### معمارستی پروژه

```
phonix_dashboard/
├── config/              # تنظیمات Django و WSGI
├── accounts/            # سیستم احراز هویت و مدیریت کاربران
├── dashboard/           # داشبورد اصلی
├── persons/             # مدیریت شخصیت‌ها
├── services/            # مدیریت سرویس‌ها
├── finance/             # مدیریت مالی
├── reports/             # تولید گزارش‌ها
├── static/              # فایل‌های استاتیک (CSS, JS, تصاویر)
├── media/               # فایل‌های بارگذاری‌شده توسط کاربران
├── logs/                # فایل‌های لاگ
└── templates/           # الگوهای HTML
```

---

## پیش‌نیازها

### سخت‌افزار

- **CPU**: حداقل 2 هسته (4 هسته توصیه می‌شود)
- **RAM**: حداقل 2GB (4GB توصیه می‌شود)
- **Storage**: حداقل 10GB فضای خالی
- **Bandwidth**: اتصال پایدار به اینترنت

### دانش و مهارت‌های مورد نیاز

- آشنایی با خط فرمان Linux
- دسترسی root یا دسترسی sudo
- دانش اولیه از سرویس‌های Apache و MySQL
- درک اولیه از SSL/TLS

---

## تهیه سرور

### مرحله 1: روزرسانی سیستم

```bash
sudo apt update
sudo apt upgrade -y
```

### مرحله 2: نصب وابستگی‌های سیستم

```bash
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    wget \
    curl \
    nginx \
    apache2 \
    apache2-utils \
    libapache2-mod-wsgi-py3 \
    mysql-server \
    mysql-client \
    libmysqlclient-dev \
    postgresql \
    postgresql-contrib \
    redis-server \
    certbot \
    python3-certbot-apache \
    build-essential \
    libssl-dev \
    libffi-dev
```

### مرحله 3: ایجاد کاربر اختصاصی

```bash
# ایجاد کاربر بدون شل برای اجرای اپلیکیشن
sudo useradd -r -s /bin/bash phonix

# ایجاد دایرکتوری‌های مورد نیاز
sudo mkdir -p /var/www/phonix
sudo mkdir -p /var/log/phonix_dashboard
sudo mkdir -p /var/run/phonix

# تنظیم دسترسی‌ها
sudo chown -R phonix:phonix /var/www/phonix
sudo chown -R phonix:phonix /var/log/phonix_dashboard
sudo chown -R phonix:phonix /var/run/phonix
sudo chmod -R 755 /var/www/phonix
```

---

## کلون کردن پروژه

### مرحله 1: کلون مخزن

```bash
cd /var/www/phonix
sudo -u phonix git clone https://github.com/H0lwin/dief_phonix.git .
```

### مرحله 2: بررسی نسخه پروژه

```bash
cd /var/www/phonix
ls -la
git log --oneline -5
```

---

## نصب وابستگی‌ها

### مرحله 1: ایجاد محیط مجازی Python

```bash
cd /var/www/phonix
sudo -u phonix python3 -m venv venv
source venv/bin/activate
```

### مرحله 2: ارتقا pip و setuptools

```bash
pip install --upgrade pip setuptools wheel
```

### مرحله 3: نصب وابستگی‌های پروژه

```bash
# اگر فایل requirements.txt موجود است
pip install -r requirements.txt

# یا نصب دستی
pip install \
    Django==4.2.7 \
    mysqlclient==2.2.0 \
    python-decouple==3.8 \
    django-cors-headers==4.3.1 \
    django-csp==3.7 \
    gunicorn==21.2.0 \
    whitenoise==6.6.0 \
    cryptography==41.0.7
```

---

## پیکربندی دیتابیس

### مرحله 1: ورود به MySQL

```bash
sudo mysql -u root
```

### مرحله 2: ایجاد دیتابیس و کاربر

```sql
-- ایجاد دیتابیس
CREATE DATABASE phonix_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ایجاد کاربر محدود
CREATE USER 'phonix_user'@'localhost' IDENTIFIED BY 'SecurePassword123!@#';

-- اختصاص دسترسی‌ها
GRANT ALL PRIVILEGES ON phonix_db.* TO 'phonix_user'@'localhost';

-- بروزرسانی مجوزها
FLUSH PRIVILEGES;

-- خروج
EXIT;
```

### مرحله 3: ایجاد فایل .env

```bash
cd /var/www/phonix
sudo -u phonix cat > .env << 'EOF'
# Django Settings
SECRET_KEY=your-very-secure-secret-key-here-change-me-in-production
DEBUG=False
ALLOWED_HOSTS=dashboard.citysecret.ir,www.dashboard.citysecret.ir,127.0.0.1
CORS_ALLOWED_ORIGINS=https://dashboard.citysecret.ir

# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=phonix_db
DB_USER=phonix_user
DB_PASSWORD=SecurePassword123!@#
DB_HOST=localhost
DB_PORT=3306

# Database SSL (اختیاری)
DB_USE_SSL=False

# Security Headers
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_SECURITY_POLICY=True

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Logging
LOG_LEVEL=INFO
EOF

# تنظیم مجوزها
sudo chmod 600 .env
sudo chown phonix:phonix .env
```

### مرحله 4: ایجاد SECRET_KEY قوی

```bash
python3 << 'EOF'
import secrets
print(secrets.token_urlsafe(50))
EOF
```

سپس مقدار تولیدشده را در فایل `.env` قرار دهید.

---

## پیکربندی محیط Django

### مرحله 1: اعمال Migrations

```bash
cd /var/www/phonix
source venv/bin/activate
python manage.py migrate --noinput
```

### مرحله 2: جمع‌آوری فایل‌های استاتیک

```bash
python manage.py collectstatic --noinput
```

### مرحله 3: فعال‌سازی ماژول‌های Apache

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod rewrite
sudo a2enmod ssl
sudo a2enmod headers
sudo a2enmod mod_wsgi
```

---

## پیکربندی Apache و SSL

### مرحله 1: ایجاد فایل پیکربندی Apache

```bash
sudo cat > /etc/apache2/sites-available/phonix-dashboard.conf << 'EOF'
<VirtualHost *:80>
    ServerName dashboard.citysecret.ir
    ServerAlias www.dashboard.citysecret.ir
    
    # Redirect HTTP to HTTPS
    Redirect permanent / https://dashboard.citysecret.ir/
</VirtualHost>

<VirtualHost *:443>
    ServerName dashboard.citysecret.ir
    ServerAlias www.dashboard.citysecret.ir
    ServerAdmin admin@citysecret.ir
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/dashboard.citysecret.ir/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/dashboard.citysecret.ir/privkey.pem
    
    # SSL Security Headers
    SSLProtocol TLSv1.2 TLSv1.3
    SSLCipherSuite HIGH:!aNULL:!MD5
    SSLHonorCipherOrder on
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    
    # Logging
    ErrorLog ${APACHE_LOG_DIR}/phonix_dashboard_error.log
    CustomLog ${APACHE_LOG_DIR}/phonix_dashboard_access.log combined
    
    # Document Root
    DocumentRoot /var/www/phonix
    
    # Static Files
    <Location /static/>
        ProxyPass !
    </Location>
    Alias /static/ /var/www/phonix/staticfiles/
    <Directory /var/www/phonix/staticfiles>
        Options -Indexes
        AllowOverride None
        Allow from all
        Header set Cache-Control "public, max-age=3600"
    </Directory>
    
    # Media Files
    <Location /media/>
        ProxyPass !
    </Location>
    Alias /media/ /var/www/phonix/media/
    <Directory /var/www/phonix/media>
        Options -Indexes
        AllowOverride None
        Allow from all
    </Directory>
    
    # Proxy to Gunicorn
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    
    # Gzip Compression
    <IfModule mod_deflate.c>
        AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
    </IfModule>
    
    # Timeout Settings
    ProxyTimeout 300
    Timeout 300
</VirtualHost>
EOF
```

### مرحله 2: فعال‌سازی سایت

```bash
sudo a2ensite phonix-dashboard
sudo a2dissite 000-default
sudo apache2ctl configtest
```

اگر نتیجه `Syntax OK` باشد، تغییرات را اعمال کنید:

```bash
sudo systemctl restart apache2
```

### مرحله 3: دریافت SSL Certificate

```bash
# اولین بار
sudo certbot certonly --apache -d dashboard.citysecret.ir -d www.dashboard.citysecret.ir

# یا اگر می‌خواهید خودکار تنظیم کند
sudo certbot --apache -d dashboard.citysecret.ir -d www.dashboard.citysecret.ir
```

---

## راه‌اندازی Gunicorn

### مرحله 1: ایجاد فایل سرویس Systemd

```bash
sudo cat > /etc/systemd/system/phonix-dashboard.service << 'EOF'
[Unit]
Description=Phonix Dashboard Gunicorn Service
After=network.target mysql.service

[Service]
Type=notify
User=phonix
Group=phonix
WorkingDirectory=/var/www/phonix
Environment="PATH=/var/www/phonix/venv/bin"
ExecStart=/var/www/phonix/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:8000 \
    --timeout 300 \
    --access-logfile /var/log/phonix_dashboard/gunicorn_access.log \
    --error-logfile /var/log/phonix_dashboard/gunicorn_error.log \
    --log-level info \
    config.wsgi:application

Restart=on-failure
RestartSec=5s

# Security Settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=yes

[Install]
WantedBy=multi-user.target
EOF
```

### مرحله 2: فعال‌سازی و شروع سرویس

```bash
sudo systemctl daemon-reload
sudo systemctl enable phonix-dashboard.service
sudo systemctl start phonix-dashboard.service
```

### مرحله 3: بررسی وضعیت سرویس

```bash
sudo systemctl status phonix-dashboard.service
journalctl -u phonix-dashboard.service -n 50
```

---

## ساخت کاربر مدیریت

### مرحله 1: فعال‌سازی محیط مجازی

```bash
cd /var/www/phonix
source venv/bin/activate
```

### مرحله 2: ایجاد Superuser

**روش تعاملی:**

```bash
python manage.py createsuperuser
```

سپس بدینصورت جواب دهید:

```
Username: admin
Email address: admin@citysecret.ir
Password: (یک رمز عبور قوی وارد کنید - حداقل 12 کاراکتر)
Password (again): (تأیید رمز عبور)
Superuser created successfully.
```

**روش غیر‌تعاملی:**

```bash
python manage.py shell << 'EOF'
from accounts.models import CustomUser
CustomUser.objects.create_superuser(
    username='admin',
    email='admin@citysecret.ir',
    password='SecurePassword123!@#'
)
EOF
```

---

## راه‌اندازی و تست

### مرحله 1: بررسی تنظیمات Django

```bash
cd /var/www/phonix
source venv/bin/activate
python manage.py check
```

باید این پیام را ببینید:

```
System check identified no issues (0 silenced).
```

### مرحله 2: تست Gunicorn

```bash
cd /var/www/phonix
source venv/bin/activate
gunicorn --workers 2 --bind 127.0.0.1:8001 config.wsgi:application
```

سپس در ترمینال دیگری تست کنید:

```bash
curl http://127.0.0.1:8001/
```

### مرحله 3: تست Apache و HTTPS

```bash
# بررسی دسترسی HTTP (باید redirect کند)
curl -I http://dashboard.citysecret.ir/

# بررسی دسترسی HTTPS
curl -I https://dashboard.citysecret.ir/

# یا از مرورگر بروید به:
https://dashboard.citysecret.ir
```

### مرحله 4: ورود به پنل مدیریت

1. در مرورگر، `https://dashboard.citysecret.ir/admin` را باز کنید
2. با نام‌کاربری و رمز عبوری که ایجاد کردید وارد شوید
3. باید صفحه مدیریت Django را ببینید

---

## نظارت و نگهداری

### لاگ‌ها

**لاگ‌های Gunicorn:**

```bash
sudo tail -f /var/log/phonix_dashboard/gunicorn_access.log
sudo tail -f /var/log/phonix_dashboard/gunicorn_error.log
```

**لاگ‌های Apache:**

```bash
sudo tail -f /var/log/apache2/phonix_dashboard_access.log
sudo tail -f /var/log/apache2/phonix_dashboard_error.log
```

**لاگ‌های Django:**

```bash
tail -f /var/www/phonix/logs/django.log
```

### نگهداری دیتابیس

**پشتیبان‌گیری:**

```bash
mysqldump -u phonix_user -p phonix_db > /var/backups/phonix_db_$(date +%Y%m%d_%H%M%S).sql
```

**بازگردانی:**

```bash
mysql -u phonix_user -p phonix_db < /var/backups/phonix_db_backup.sql
```

### بروزرسانی SSL Certificate

```bash
# تجدید خودکار
sudo certbot renew

# یا بصورت دستی
sudo certbot renew --manual
```

### بروزرسانی کد

```bash
cd /var/www/phonix
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart phonix-dashboard.service
```

### نگارش دسترسی‌ها

```bash
# مجوزها را تنظیم کنید
sudo chown -R phonix:phonix /var/www/phonix
sudo chmod -R 755 /var/www/phonix
sudo chmod -R 700 /var/www/phonix/venv
chmod 600 /var/www/phonix/.env
```

---

## حل مشکلات

### سرویس Gunicorn شروع نمی‌شود

```bash
# بررسی وضعیت
sudo systemctl status phonix-dashboard.service

# مشاهده لاگ‌ها
journalctl -u phonix-dashboard.service -n 100 --no-pager

# بررسی فایل .env
cat /var/www/phonix/.env

# تست دستی
cd /var/www/phonix
source venv/bin/activate
gunicorn config.wsgi:application
```

### خطا در اتصال دیتابیس

```bash
# تست اتصال MySQL
mysql -u phonix_user -p -h localhost phonix_db -e "SELECT 1;"

# بررسی تنظیمات .env
cat /var/www/phonix/.env | grep DB_

# اجرای migrations
cd /var/www/phonix
source venv/bin/activate
python manage.py migrate --verbosity=2
```

### خطای SSL Certificate

```bash
# بررسی تاریخ انقضا
sudo certbot certificates

# تجدید دستی
sudo certbot renew --force-renewal -v

# بررسی فایل‌های SSL
ls -la /etc/letsencrypt/live/dashboard.citysecret.ir/
```

### صفحات استاتیک بارگذاری نمی‌شود

```bash
# جمع‌آوری مجدد فایل‌های استاتیک
cd /var/www/phonix
source venv/bin/activate
python manage.py collectstatic --noinput --clear

# بررسی مجوزها
sudo chown -R phonix:phonix /var/www/phonix/staticfiles
sudo chmod -R 755 /var/www/phonix/staticfiles

# بررسی پیکربندی Apache
sudo apache2ctl configtest
sudo systemctl restart apache2
```

---

## چک‌لیست نهایی

- [ ] سرور Ubuntu 22.04 نصب شده
- [ ] Python 3، pip، Git نصب شده
- [ ] MySQL نصب و پیکربندی‌شده
- [ ] مخزن کلون شده
- [ ] محیط مجازی ایجاد‌شده
- [ ] وابستگی‌ها نصب شده
- [ ] فایل `.env` ایجاد‌شده
- [ ] Migrations اعمال شده
- [ ] فایل‌های استاتیک جمع‌آوری‌شده
- [ ] Apache پیکربندی‌شده
- [ ] SSL Certificate دریافت‌شده
- [ ] Gunicorn سرویس شروع‌شده
- [ ] Superuser ایجاد‌شده
- [ ] مرورگر تست شده
- [ ] پنل مدیریت قابل‌دسترس است

---

## منابع مفید

- [Django Documentation](https://docs.djangoproject.com/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Apache Documentation](https://httpd.apache.org/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

---

**نوشته‌شده**: تاریخ اجرا
**نسخه**: 1.0
**وضعیت**: تولید (Production)
