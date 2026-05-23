import sqlite3
import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# اتصال به دیتابیس
conn = sqlite3.connect('data/clinic.db')
cursor = conn.cursor()

# اطلاعات ادمین
username = "admin"
password = "admin123"
full_name = "مدیر سیستم"
first_name = "مدیر"
last_name = "سیستم"
national_id = "1111111111"
phone = "0777777777"
position = "مدیر"
hire_date = datetime.now().strftime('%Y-%m-%d')
role = "admin"

password_hash = hash_password(password)

# 1. ثبت در جدول users
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
if cursor.fetchone():
    # به‌روزرسانی
    cursor.execute("UPDATE users SET role = ?, password_hash = ? WHERE username = ?", (role, password_hash, username))
    print(f"✅ کاربر {username} در جدول users به‌روزرسانی شد!")
else:
    # ایجاد جدید
    cursor.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)", 
                   (username, password_hash, full_name, role))
    print(f"✅ کاربر {username} در جدول users ساخته شد!")

# 2. ثبت در جدول staff
cursor.execute("SELECT * FROM staff WHERE username = ?", (username,))
if cursor.fetchone():
    # به‌روزرسانی
    cursor.execute("""
        UPDATE staff 
        SET first_name = ?, last_name = ?, national_id = ?, phone = ?, position = ?, hire_date = ?, status = 'active'
        WHERE username = ?
    """, (first_name, last_name, national_id, phone, position, hire_date, username))
    print(f"✅ پرسنل {username} در جدول staff به‌روزرسانی شد!")
else:
    # ایجاد جدید
    cursor.execute("""
        INSERT INTO staff (first_name, last_name, national_id, phone, position, hire_date, username, password_hash, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (first_name, last_name, national_id, phone, position, hire_date, username, password_hash, 'active'))
    print(f"✅ پرسنل {username} در جدول staff ساخته شد!")

conn.commit()
conn.close()

print("\n" + "="*50)
print(f"✅ ادمین با موفقیت در هر دو جدول ثبت شد!")
print(f"👤 نام کاربری: {username}")
print(f"🔑 رمز عبور: {password}")
print(f"👥 نقش: {role}")
print("="*50)
print("\n🔄 حالا صفحه را رفرش کنید و با این اطلاعات وارد شوید.")