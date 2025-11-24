-- ایجاد دیتابیس فونیکس
CREATE DATABASE IF NOT EXISTS phonix_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci 
ENCRYPTION='Y';

-- ایجاد کاربر محدود برای دیتابیس (امن تر از root استفاده)
-- توجه: رمز عبور را تغییر دهید! این تنها یک مثال است
CREATE USER IF NOT EXISTS 'phonix_user'@'localhost' IDENTIFIED BY 'SecurePassword123!';

-- اختصاص دسترسی های صحیح
GRANT CREATE, ALTER, DROP, INDEX, SELECT, INSERT, UPDATE, DELETE, 
      LOCK TABLES, REFERENCES, CREATE ROUTINE, ALTER ROUTINE, 
      EXECUTE, CREATE VIEW, SHOW VIEW, CREATE TEMPORARY TABLES, 
      TRIGGER ON phonix_db.* TO 'phonix_user'@'localhost';

FLUSH PRIVILEGES;

-- استفاده از دیتابیس
USE phonix_db;

-- تنظیم متغیرهای امنیتی
SET GLOBAL sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- نمایش اطلاعات دیتابیس و تنظیمات کاراکتری
SHOW VARIABLES LIKE 'character_set%';
SHOW VARIABLES LIKE 'sql_mode';
