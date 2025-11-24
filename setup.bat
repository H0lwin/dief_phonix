@echo off
REM راه‌اندازی پروژه فونیکس

echo ===============================================
echo راه‌اندازی پروژه سیستم مدیریت فونیکس
echo ===============================================

echo.
echo 1. نصب پکیج‌های مورد نیاز...
pip install -r requirements.txt

echo.
echo 2. اجرای Migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo 3. ایجاد سوپریوزر...
echo لطفا نام کاربری را وارد کنید (یا Enter برای H0lwin):
set /p username=
if "%username%"=="" set username=H0lwin

python manage.py create_superuser

echo.
echo 4. جمع‌آوری Static Files...
python manage.py collectstatic --no-input

echo.
echo ===============================================
echo راه‌اندازی تکمیل شد!
echo ===============================================
echo.
echo برای شروع سرور:
echo python manage.py runserver
echo.
echo آدرس‌های مهم:
echo - داشبورد: http://localhost:8000/dashboard/
echo - پنل سوپر ادمین: http://localhost:8000/superuser-admin/
echo - ورود: http://localhost:8000/accounts/login/
echo.
pause
