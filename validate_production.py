#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Production readiness validation script for Phonix Dashboard
Run this before deploying to production
"""

import os
import sys
import subprocess
from pathlib import Path
from decouple import config, UndefinedValueError

if sys.stdout.encoding and 'utf' not in sys.stdout.encoding.lower():
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).resolve().parent


class ValidationError(Exception):
    pass


class ProductionValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_failed = 0

    def add_error(self, message):
        self.errors.append(f"❌ {message}")
        self.checks_failed += 1

    def add_warning(self, message):
        self.warnings.append(f"⚠️  {message}")

    def add_success(self, message):
        print(f"✅ {message}")
        self.checks_passed += 1

    def check_env_file_exists(self):
        """Verify .env file exists"""
        env_file = BASE_DIR / ".env"
        if not env_file.exists():
            self.add_error(".env file not found. Copy .env.example and configure it.")
        else:
            self.add_success(".env file found")

    def check_secret_key(self):
        """Verify SECRET_KEY is configured securely"""
        try:
            secret_key = config("SECRET_KEY")
            if secret_key.startswith("django-insecure-"):
                self.add_error(
                    "SECRET_KEY uses insecure default. Generate a new one: "
                    "python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
                )
            elif len(secret_key) < 50:
                self.add_error(f"SECRET_KEY is too short ({len(secret_key)} chars). Use at least 50 characters.")
            else:
                self.add_success(f"SECRET_KEY is properly configured ({len(secret_key)} chars)")
        except UndefinedValueError:
            self.add_error("SECRET_KEY is not configured in .env")

    def check_debug_mode(self):
        """Verify DEBUG is False"""
        try:
            debug = config("DEBUG", default=False, cast=bool)
            if debug:
                self.add_error("DEBUG=True in production! Set DEBUG=False in .env")
            else:
                self.add_success("DEBUG is set to False")
        except UndefinedValueError:
            self.add_error("DEBUG is not configured in .env")

    def check_allowed_hosts(self):
        """Verify ALLOWED_HOSTS is configured"""
        try:
            allowed_hosts = config("ALLOWED_HOSTS", default="")
            if not allowed_hosts or allowed_hosts == "*":
                self.add_error("ALLOWED_HOSTS is not properly configured. Set specific domain names.")
            elif "localhost" in allowed_hosts and "yourdomain.com" in allowed_hosts:
                self.add_warning("ALLOWED_HOSTS might contain example values. Verify they are correct.")
            else:
                self.add_success(f"ALLOWED_HOSTS configured: {allowed_hosts}")
        except UndefinedValueError:
            self.add_error("ALLOWED_HOSTS is not configured in .env")

    def check_database_config(self):
        """Verify database configuration"""
        try:
            db_user = config("DB_USER", default="")
            db_password = config("DB_PASSWORD", default="")
            db_host = config("DB_HOST", default="localhost")
            db_name = config("DB_NAME", default="phonix_db")
            
            if not db_user:
                self.add_error("DB_USER is not configured in .env")
            elif db_user == "H0lwin":
                self.add_error("DB_USER still uses old hardcoded value. Change immediately!")
            elif db_user == "root":
                self.add_warning("Using root user for database. Consider using a limited user.")
            else:
                self.add_success(f"Database user configured: {db_user}")
            
            if not db_password or db_password == "Shayan.1400":
                self.add_error("DB_PASSWORD is not securely configured. Set a strong password!")
            else:
                self.add_success("Database password is configured")
            
            if db_host == "localhost":
                self.add_warning("Database is on localhost. For production, consider remote database.")
            else:
                self.add_success(f"Database host configured: {db_host}")
                
        except UndefinedValueError as e:
            self.add_error(f"Database configuration missing: {e}")

    def check_ssl_configuration(self):
        """Verify SSL/TLS configuration"""
        try:
            ssl_redirect = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
            session_secure = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
            csrf_secure = config("CSRF_COOKIE_SECURE", default=False, cast=bool)
            
            if not ssl_redirect:
                self.add_warning("SECURE_SSL_REDIRECT is not enabled. Enable for HTTPS enforcement.")
            else:
                self.add_success("SECURE_SSL_REDIRECT is enabled")
            
            if not session_secure:
                self.add_warning("SESSION_COOKIE_SECURE is not enabled. Enable for production.")
            else:
                self.add_success("SESSION_COOKIE_SECURE is enabled")
            
            if not csrf_secure:
                self.add_warning("CSRF_COOKIE_SECURE is not enabled. Enable for production.")
            else:
                self.add_success("CSRF_COOKIE_SECURE is enabled")
                
        except UndefinedValueError as e:
            self.add_warning(f"SSL configuration incomplete: {e}")

    def check_email_configuration(self):
        """Verify email configuration"""
        try:
            email_backend = config("EMAIL_BACKEND", default="")
            email_host = config("EMAIL_HOST", default="")
            
            if not email_host or email_host == "smtp.gmail.com":
                self.add_warning("Email not properly configured for error notifications.")
            else:
                self.add_success(f"Email configured: {email_host}")
                
        except UndefinedValueError:
            self.add_warning("Email configuration not set. Error emails won't be sent.")

    def check_django_security_check(self):
        """Run Django's security checks"""
        try:
            result = subprocess.run(
                [sys.executable, "manage.py", "check", "--deploy"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.add_success("Django security checks passed")
            else:
                output = result.stdout + result.stderr
                if "identified no issues" in output:
                    self.add_success("Django security checks passed")
                else:
                    self.add_warning("Django security checks found issues (see output above)")
                    print(output)
                    
        except Exception as e:
            self.add_warning(f"Could not run Django security checks: {e}")

    def check_requirements_installed(self):
        """Verify all required packages are installed"""
        try:
            import django
            import decouple
            import mysqlclient
            import corsheaders
            import csp
            import gunicorn
            import whitenoise
            
            self.add_success("All required packages are installed")
        except ImportError as e:
            self.add_error(f"Missing required package: {e}")

    def check_static_files(self):
        """Verify static files directory exists"""
        static_root = BASE_DIR / "staticfiles"
        if static_root.exists():
            self.add_success("Static files directory exists")
        else:
            self.add_warning("Static files not collected yet. Run: python manage.py collectstatic")

    def check_logs_directory(self):
        """Verify logs directory is writable"""
        logs_dir = BASE_DIR / "logs"
        try:
            logs_dir.mkdir(exist_ok=True)
            test_file = logs_dir / ".test"
            test_file.write_text("test")
            test_file.unlink()
            self.add_success("Logs directory is writable")
        except Exception as e:
            self.add_error(f"Cannot write to logs directory: {e}")

    def check_database_connection(self):
        """Test database connection"""
        try:
            import django
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
            django.setup()
            
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            self.add_success("Database connection successful")
        except Exception as e:
            self.add_error(f"Database connection failed: {e}")

    def check_migrations(self):
        """Check for pending migrations"""
        try:
            result = subprocess.run(
                [sys.executable, "manage.py", "migrate", "--plan"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if "No migrations to apply" in result.stdout or result.returncode == 0:
                self.add_success("All migrations are applied")
            else:
                self.add_warning("Pending migrations found. Run: python manage.py migrate")
                
        except Exception as e:
            self.add_warning(f"Could not check migrations: {e}")

    def check_file_permissions(self):
        """Check critical file permissions"""
        env_file = BASE_DIR / ".env"
        if env_file.exists():
            mode = oct(env_file.stat().st_mode)[-3:]
            if mode != "600":
                self.add_warning(f".env file permissions are {mode}. Should be 600 for security.")
            else:
                self.add_success(".env file permissions are correct (600)")

    def run_all_checks(self):
        """Run all validation checks"""
        print("=" * 60)
        print("🔍 Production Readiness Validation")
        print("=" * 60)
        print()
        
        self.check_env_file_exists()
        self.check_secret_key()
        self.check_debug_mode()
        self.check_allowed_hosts()
        self.check_database_config()
        self.check_ssl_configuration()
        self.check_email_configuration()
        self.check_requirements_installed()
        self.check_static_files()
        self.check_logs_directory()
        self.check_file_permissions()
        self.check_django_security_check()
        self.check_database_connection()
        self.check_migrations()
        
        print()
        print("=" * 60)
        print("📊 Validation Summary")
        print("=" * 60)
        print(f"✅ Passed: {self.checks_passed}")
        print(f"❌ Failed: {self.checks_failed}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print()
        
        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(error)
            print()
        
        if self.warnings:
            print("WARNINGS:")
            for warning in self.warnings:
                print(warning)
            print()
        
        if self.errors:
            print("❌ Validation FAILED - Fix errors before deploying to production!")
            return False
        elif self.warnings:
            print("⚠️  Validation PASSED with warnings - Review warnings above")
            return True
        else:
            print("✅ Validation PASSED - Ready for production deployment!")
            return True


if __name__ == "__main__":
    validator = ProductionValidator()
    success = validator.run_all_checks()
    sys.exit(0 if success else 1)
