-- ایجاد دیتابیس فونیکس
CREATE DATABASE IF NOT EXISTS phonix_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- استفاده از دیتابیس
USE phonix_db;

-- نمایش اطلاعات دیتابیس
SHOW VARIABLES LIKE 'character_set%';
