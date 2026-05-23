import hashlib
from modules.database import get_connection

def hash_password(password):
    """تبدیل رمز عبور به هش برای امنیت"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    """بررسی اعتبار کاربر برای ورود به سیستم"""
    hashed = hash_password(password)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password_hash, full_name, role FROM users WHERE username = ? AND password_hash = ?",
            (username, hashed)
        )
        user = cursor.fetchone()
        return user

def register_user(username, password, full_name, role='staff'):
    """ثبت نام کاربر جدید"""
    hashed = hash_password(password)
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                (username, hashed, full_name, role)
            )
            conn.commit()
            return True, "کاربر با موفقیت ثبت شد"
    except Exception as e:
        return False, str(e)

def change_password(user_id, old_password, new_password):
    """تغییر رمز عبور کاربر"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return False, "کاربر یافت نشد"
        
        if user[0] != hash_password(old_password):
            return False, "رمز عبور فعلی اشتباه است"
        
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (hash_password(new_password), user_id)
        )
        conn.commit()
        return True, "رمز عبور با موفقیت تغییر کرد"

def get_user_by_id(user_id):
    """دریافت اطلاعات کاربر با شناسه"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, full_name, role FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

def get_all_users():
    """دریافت لیست همه کاربران"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, full_name, role FROM users ORDER BY id")
        return cursor.fetchall()

def delete_user(user_id):
    """حذف کاربر (فقط برای ادمین)"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return True, "کاربر حذف شد"
    except Exception as e:
        return False, str(e)

def create_default_admin():
    """ایجاد کاربر ادمین پیش‌فرض در صورت نبودن هیچ کاربری"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        if count == 0:
            admin_pass = hash_password("admin123")
            cursor.execute(
                "INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                ("admin", admin_pass, "مدیر سیستم", "admin")
            )
            conn.commit()
            print("=" * 50)
            print("✅ کاربر ادمین پیش‌فرض ایجاد شد!")
            print("   Username: admin")
            print("   Password: admin123")
            print("=" * 50)
            return True
    return False

def check_user_exists(username):
    """بررسی وجود کاربر با نام کاربری مشخص"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        return cursor.fetchone() is not None

def get_user_role(username):
    """دریافت نقش کاربر"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        return user[0] if user else None

def is_admin(user_id):
    """بررسی ادمین بودن کاربر"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return user and user[0] == 'admin'