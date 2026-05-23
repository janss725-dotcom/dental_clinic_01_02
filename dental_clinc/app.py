import sys
import os
import json
# این کد مسیر پوشه موقت را به پایتون می‌شناساند تا ماژول‌ها را پیدا کند
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
import streamlit as st
import json
import os
from modules.database import get_connection, init_database
from modules.auth import login_user, create_default_admin
from modules.dashboard import render_dashboard
from modules.patients import render_add_patient, render_patient_list
from modules.emr import render_emr_section
from modules.settings import render_settings
from modules.treatment_plan import render_treatment_plan_selector
from modules.staff import render_staff_management

# ========== تنظیمات صفحه ==========
st.set_page_config(page_title="سیستم مدیریت کلینیک دندان", layout="wide")

# ========== مسیر فایل دسترسی‌ها ==========
PERMISSIONS_FILE = "user_permissions.json"

# ========== توابع مدیریت دسترسی با JSON ==========

def load_all_permissions():
    """بارگذاری تمام دسترسی‌ها از فایل JSON"""
    if os.path.exists(PERMISSIONS_FILE):
        try:
            with open(PERMISSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_all_permissions(permissions):
    """ذخیره تمام دسترسی‌ها در فایل JSON"""
    with open(PERMISSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(permissions, f, indent=2, ensure_ascii=False)

def get_user_permissions(username):
    """دریافت دسترسی‌های یک کاربر"""
    all_perms = load_all_permissions()
    # دسترسی‌های پیش‌فرض در صورت نبود رکورد
    default_perms = {
        'patients_add': False,
        'patients_view': False,
        'emr_view': False,
        'settings_access': False,
        'treatment_plan_view': False
    }
    return all_perms.get(username, default_perms)

# ========== راه‌اندازی دیتابیس ==========
init_database()
create_default_admin()

# ایجاد فایل دسترسی‌ها اگر وجود ندارد
if not os.path.exists(PERMISSIONS_FILE):
    save_all_permissions({})

# ========== مقداردهی اولیه Session State ==========
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = {}

# ========== صفحه لاگین ==========
if not st.session_state.logged_in:
    st.title("🔐 ورود به سیستم کلینیک")
    
    with st.form("login_form"):
        username = st.text_input("نام کاربری")
        password = st.text_input("رمز عبور", type="password")
        submit = st.form_submit_button("ورود")
        
        if submit:
            user = login_user(username, password)
            if user:
                user_id = user[0]
                user_role = user[4] if len(user) > 4 else 'staff'
                user_fullname = user[3] if len(user) > 3 else username
                
                # دریافت دسترسی‌ها از فایل JSON
                user_permissions = get_user_permissions(username)
                
                # ادمین‌ها همیشه به همه چیز دسترسی دارند
                if user_role == 'admin':
                    user_permissions = {k: True for k in user_permissions}
                
                st.session_state.logged_in = True
                st.session_state.user_info = {
                    'id': user_id,
                    'username': username,
                    'full_name': user_fullname,
                    'role': user_role,
                    'permissions': user_permissions
                }
                st.success(f"خوش آمدید {user_fullname}")
                st.rerun()
            else:
                st.error("نام کاربری یا رمز عبور اشتباه است")
    st.stop()

# ========== استایل سایدبار ==========
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A0F1F 0%, #0E1629 100%);
    border-right: 2px solid #00C8FF;
}
.sidebar-header {
    background: linear-gradient(135deg, #0E1629, #0A0F1F);
    padding: 30px 20px 20px 20px;
    text-align: center;
    border-bottom: 2px solid #00C8FF;
    margin-bottom: 20px;
}
.clinic-name {
    font-size: 24px;
    font-weight: 700;
    color: white;
    margin: 0;
    text-shadow: 0 0 15px #00C8FF;
}
.clinic-tagline {
    font-size: 12px;
    color: #7FBAFF;
    margin: 8px 0 0 0;
}
.sidebar-user {
    background: linear-gradient(135deg, #141E36, #0E1629);
    padding: 20px;
    border-radius: 20px;
    margin: 0 15px 25px 15px;
    border: 2px solid #00C8FF;
}
.user-avatar {
    display: flex;
    align-items: center;
    gap: 15px;
}
.avatar-circle {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #00C8FF, #0066FF);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    color: white;
    font-weight: bold;
}
.user-info h4 {
    margin: 0;
    color: white;
}
.user-info p {
    margin: 5px 0 0 0;
    color: #7FBAFF;
    font-size: 11px;
}
.status-indicator {
    display: inline-block;
    width: 10px;
    height: 10px;
    background: #00C8FF;
    border-radius: 50%;
    margin-right: 8px;
    box-shadow: 0 0 15px #00C8FF;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.1); }
}
.section-title {
    color: #00C8FF !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 0 15px !important;
    margin-bottom: 15px !important;
    text-shadow: 0 0 10px #00C8FF;
}
div[data-baseweb="radio"] label {
    background: #141E36 !important;
    color: #E0F0FF !important;
    padding: 14px 18px !important;
    border-radius: 15px !important;
    margin: 8px 0 !important;
    border: 2px solid #4D9EFF !important;
    width: 100% !important;
}
div[data-baseweb="radio"] input:checked + label {
    background: linear-gradient(135deg, #00C8FF, #0066FF) !important;
    color: white !important;
    box-shadow: 0 0 25px #00C8FF !important;
}
.sidebar-footer {
    padding: 20px 15px;
    margin-top: 20px;
    border-top: 2px solid #0066FF;
    text-align: center;
}
.footer-info {
    font-size: 11px;
    color: #7FBAFF;
}
.version-badge {
    display: inline-block;
    background: rgba(0, 200, 255, 0.1);
    color: #00C8FF;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    margin-top: 10px;
    border: 1px solid #00C8FF;
}
.stButton > button {
    background: linear-gradient(135deg, #FF6B6B, #FF4757) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 14px !important;
    font-weight: 600 !important;
    margin: 10px 15px !important;
    width: calc(100% - 30px) !important;
}
</style>
""", unsafe_allow_html=True)

# ========== سایدبار ==========
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <h1 class="clinic-name">🦷 ASIF DENTAL CLINIC</h1>
            <p class="clinic-tagline">مرکز تخصصی مراقبت‌های دهان و دندان</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        user_info = st.session_state.user_info
        st.markdown(f"""
            <div class="sidebar-user">
                <div class="user-avatar">
                    <div class="avatar-circle">👤</div>
                    <div class="user-info">
                        <h4>{user_info.get('full_name', 'کاربر')}</h4>
                        <p>نقش: {user_info.get('role', 'staff')}</p>
                        <p>نام کاربری: {user_info.get('username', '?')}</p>
                    </div>
                </div>
                <div style="display: flex; align-items: center; margin-top: 10px;">
                    <span class="status-indicator"></span>
                    <span style="color: #00C8FF; font-size: 12px;">آنلاین</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # نمایش دسترسی‌های کاربر
        with st.expander("🔐 دسترسی‌های من", expanded=False):
            permissions = user_info.get('permissions', {})
            st.write("**وضعیت دسترسی‌ها:**")
            st.markdown(f"➕ ثبت بیمار جدید: {'✅ فعال' if permissions.get('patients_add') else '❌ غیرفعال'}")
            st.markdown(f"📋 مشاهده بیماران: {'✅ فعال' if permissions.get('patients_view') else '❌ غیرفعال'}")
            st.markdown(f"🦷 پرونده الکترونیک: {'✅ فعال' if permissions.get('emr_view') else '❌ غیرفعال'}")
            st.markdown(f"⚙️ تنظیمات: {'✅ فعال' if permissions.get('settings_access') else '❌ غیرفعال'}")
            st.markdown(f"📋 طرح درمان: {'✅ فعال' if permissions.get('treatment_plan_view') else '❌ غیرفعال'}")
    
    st.markdown('<div class="section-title">📋 منوی اصلی</div>', unsafe_allow_html=True)
    
    # ===== ساخت منو بر اساس دسترسی کاربر =====
    user_role = st.session_state.user_info.get('role', 'staff')
    user_permissions = st.session_state.user_info.get('permissions', {})
    
    menu_list = []
    
    # 1. داشبورد - همیشه در دسترس
    menu_list.append("📊 Dashboard Analytics")
    
    # 2. افزودن بیمار
    if user_role == 'admin' or user_permissions.get('patients_add', False):
        menu_list.append("👨‍⚕️ Add New Patient")
    
    # 3. لیست بیماران
    if user_role == 'admin' or user_permissions.get('patients_view', False):
        menu_list.append("📋 Patient Records")
    
    # 4. پرونده الکترونیک
    if user_role == 'admin' or user_permissions.get('emr_view', False):
        menu_list.append("🦷 Electronic Medical Record")
    
    # 5. تنظیمات
    if user_role == 'admin' or user_permissions.get('settings_access', False):
        menu_list.append("⚙️ Settings")
    
    # 6. طرح درمان
    if user_role == 'admin' or user_permissions.get('treatment_plan_view', False):
        menu_list.append("📋 Treatment Plan")
    
    # 7. مدیریت پرسنل - فقط ادمین
    if user_role == 'admin':
        menu_list.append("👥 مدیریت پرسنل")
    
    # نمایش تعداد منوها
    st.caption(f"🔍 {len(menu_list)} منو قابل دسترسی است")
    
    if menu_list:
        menu_choice = st.radio(
            "انتخاب بخش:",
            options=menu_list,
            index=0,
            label_visibility="collapsed"
        )
    else:
        menu_choice = "📊 Dashboard Analytics"
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # دکمه خروج
    if st.button("🚪 خروج از سیستم", width="stretch"):
        st.session_state.logged_in = False
        st.session_state.user_info = {}
        st.rerun()
    
    st.markdown("""
        <div class="sidebar-footer">
            <div class="footer-info">
                <p>© 2026 Asif Dental Clinic</p>
                <p>نسخه 3.0</p>
            </div>
            <div class="version-badge">نسخه نئون آبی</div>
        </div>
    """, unsafe_allow_html=True)

# ========== کنترلر اصلی (ساده و بدون قفل) ==========

# ذخیره انتخاب فعلی در session_state
st.session_state.menu_choice = menu_choice

# نمایش بخش مناسب بر اساس menu_choice (از سایدبار)
if menu_choice == "📊 Dashboard Analytics":
    render_dashboard()
elif menu_choice == "👨‍⚕️ Add New Patient":
    render_add_patient()
elif menu_choice == "📋 Patient Records":
    render_patient_list()
elif menu_choice == "🦷 Electronic Medical Record":
    render_emr_section()
elif menu_choice == "⚙️ Settings":
    render_settings()
elif menu_choice == "📋 Treatment Plan":
    render_treatment_plan_selector()
elif menu_choice == "👥 مدیریت پرسنل":
    render_staff_management()