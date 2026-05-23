import streamlit as st
import pandas as pd
import hashlib
import sqlite3
import io
import time
import json
import os
from datetime import datetime
from modules.database import get_connection

# ========== تنظیمات فایل دسترسی‌ها ==========
PERMISSIONS_FILE = "user_permissions.json"

def hash_password(password):
    """تبدیل رمز عبور به هش"""
    return hashlib.sha256(password.encode()).hexdigest()

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

def render_staff_management():
    """مدیریت جامع پرسنل کلینیک دندان‌پزشکی"""
    
    # بررسی دسترسی کاربر برای مشاهده این بخش (فقط ادمین)
    user_role = st.session_state.user_info.get('role', 'staff')
    if user_role != 'admin':
        st.error("⛔ شما دسترسی لازم برای مشاهده این بخش را ندارید.")
        st.info("این بخش فقط برای مدیران سیستم قابل دسترسی است.")
        return
    
    # ===== استایل مدرن =====
    st.markdown("""
        <style>
        .staff-header {
            background: linear-gradient(135deg, #0A0F1F, #0E1629);
            padding: 30px 25px;
            border-radius: 25px;
            margin-bottom: 30px;
            border: 2px solid #00C8FF;
            text-align: center;
            box-shadow: 0 10px 25px -10px rgba(0, 200, 255, 0.3);
        }
        .staff-header h1 {
            color: white;
            font-size: 36px;
            margin: 0;
            text-shadow: 0 0 15px #00C8FF;
        }
        .staff-header p {
            color: #7FBAFF;
            margin: 10px 0 0 0;
        }
        .staff-card {
            background: linear-gradient(135deg, #141E36, #0E1629);
            border-radius: 20px;
            padding: 25px;
            border: 2px solid #00C8FF;
            margin-bottom: 20px;
            transition: all 0.3s;
        }
        .staff-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 25px rgba(0, 200, 255, 0.2);
        }
        .stat-card-staff {
            background: rgba(20, 30, 54, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid #00C8FF;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s;
        }
        .stat-card-staff:hover {
            transform: translateY(-3px);
            border-color: #7FBAFF;
            box-shadow: 0 0 20px rgba(0, 200, 255, 0.2);
        }
        .stat-value-staff {
            font-size: 32px;
            font-weight: 700;
            color: white;
            text-shadow: 0 0 15px #00C8FF;
        }
        .stat-label-staff {
            color: #7FBAFF;
            font-size: 13px;
            margin-top: 5px;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: #0E1629;
            padding: 12px 18px;
            border-radius: 50px;
            border: 1px solid rgba(0, 200, 255, 0.2);
            margin-bottom: 30px;
        }
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 40px;
            padding: 10px 28px;
            color: #7FBAFF !important;
            font-weight: 500;
            transition: all 0.3s;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(0, 200, 255, 0.1);
            color: #00C8FF !important;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #00C8FF, #0066FF) !important;
            color: white !important;
            box-shadow: 0 0 20px #00C8FF !important;
        }
        .stButton > button {
            background: linear-gradient(135deg, #00C8FF, #0066FF);
            color: white;
            border: none;
            border-radius: 40px;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.3s;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 25px #00C8FF;
        }
        </style>
    """, unsafe_allow_html=True)

    # ===== هدر اصلی =====
    st.markdown("""
        <div class="staff-header">
            <h1>👥 مدیریت پیشرفته پرسنل</h1>
            <p>سیستم جامع مدیریت کاربران، دسترسی‌ها، وام و کسورات</p>
        </div>
    """, unsafe_allow_html=True)

    # ===== ایجاد جداول (در صورت عدم وجود) =====
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # جدول staff
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                national_id TEXT UNIQUE NOT NULL,
                phone TEXT,
                address TEXT,
                position TEXT NOT NULL,
                specialization TEXT,
                license_number TEXT,
                hire_date DATE NOT NULL,
                salary REAL DEFAULT 0,
                status TEXT DEFAULT 'active',
                username TEXT UNIQUE,
                password_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # جدول وام‌های پرسنل
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff_loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER NOT NULL,
                loan_date DATE NOT NULL,
                amount REAL NOT NULL,
                remaining_amount REAL NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (staff_id) REFERENCES staff (id) ON DELETE CASCADE
            )
        """)
        
        # جدول اقساط و بازپرداخت وام
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loan_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                loan_id INTEGER NOT NULL,
                payment_date DATE NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (loan_id) REFERENCES staff_loans (id) ON DELETE CASCADE
            )
        """)
        
        # جدول حضور و غیاب
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff_attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER NOT NULL,
                date DATE NOT NULL,
                check_in TIME,
                check_out TIME,
                hours_worked REAL,
                patients_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'present',
                absence_type TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (staff_id) REFERENCES staff (id) ON DELETE CASCADE,
                UNIQUE(staff_id, date)
            )
        """)
        
        # جدول حقوق و دستمزد
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff_payroll (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER NOT NULL,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                base_salary REAL DEFAULT 0,
                overtime_hours REAL DEFAULT 0,
                overtime_pay REAL DEFAULT 0,
                bonus REAL DEFAULT 0,
                absence_deduction REAL DEFAULT 0,
                loan_deduction REAL DEFAULT 0,
                other_deductions REAL DEFAULT 0,
                total_deductions REAL DEFAULT 0,
                total_salary REAL DEFAULT 0,
                net_salary REAL DEFAULT 0,
                payment_date DATE,
                payment_status TEXT DEFAULT 'pending',
                notes TEXT,
                FOREIGN KEY (staff_id) REFERENCES staff (id) ON DELETE CASCADE,
                UNIQUE(staff_id, year, month)
            )
        """)
        
        # ایجاد ایندکس‌ها
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_staff_status ON staff(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_attendance_date ON staff_attendance(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_loans_staff ON staff_loans(staff_id)")
        
        conn.commit()

    # ===== دریافت آمار کلی =====
    try:
        with get_connection() as conn:
            total_staff = conn.execute("SELECT COUNT(*) FROM staff").fetchone()[0]
            active_staff_count = conn.execute("SELECT COUNT(*) FROM staff WHERE status = 'active'").fetchone()[0]
            total_loans = conn.execute("SELECT COALESCE(SUM(remaining_amount), 0) FROM staff_loans WHERE status = 'active'").fetchone()[0]
            
            today = datetime.now().strftime('%Y-%m-%d')
            absent_today = conn.execute("""
                SELECT COUNT(*) FROM staff_attendance 
                WHERE date = ? AND status = 'absent'
            """, (today,)).fetchone()[0]
    except:
        total_staff = active_staff_count = total_loans = absent_today = 0

    # ===== نمایش آمار =====
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card-staff">
                <div style="font-size: 32px; margin-bottom: 10px;">👥</div>
                <div class="stat-value-staff">{total_staff}</div>
                <div class="stat-label-staff">کل پرسنل</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-card-staff">
                <div style="font-size: 32px; margin-bottom: 10px;">✅</div>
                <div class="stat-value-staff">{active_staff_count}</div>
                <div class="stat-label-staff">فعال</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-card-staff">
                <div style="font-size: 32px; margin-bottom: 10px;">💰</div>
                <div class="stat-value-staff">{total_loans:,.0f}</div>
                <div class="stat-label-staff">وام‌های فعال</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stat-card-staff">
                <div style="font-size: 32px; margin-bottom: 10px;">❌</div>
                <div class="stat-value-staff">{absent_today}</div>
                <div class="stat-label-staff">غیبت امروز</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ===== تب‌های اصلی =====
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 لیست پرسنل",
        "➕ ثبت پرسنل جدید",
        "🔐 مدیریت دسترسی‌ها",
        "💰 وام و کسورات",
        "⏰ حضور و غیاب"
    ])

    # ===== Tab 1: لیست پرسنل =====
    with tab1:
        st.subheader("📋 لیست پرسنل")
        
        try:
            with get_connection() as conn:
                staff_df = pd.read_sql_query("""
                    SELECT s.*, 
                           COALESCE((SELECT SUM(remaining_amount) FROM staff_loans WHERE staff_id = s.id AND status = 'active'), 0) as total_debt
                    FROM staff s
                    ORDER BY s.id DESC
                """, conn)
        except:
            staff_df = pd.DataFrame()

        if not staff_df.empty:
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                status_filter = st.selectbox("فیلتر وضعیت", ["همه", "active", "inactive", "leave"])
            with col_f2:
                position_filter = st.selectbox("فیلتر پوزیشن", ["همه"] + list(staff_df['position'].unique()))

            filtered_df = staff_df.copy()
            if status_filter != "همه":
                filtered_df = filtered_df[filtered_df['status'] == status_filter]
            if position_filter != "همه":
                filtered_df = filtered_df[filtered_df['position'] == position_filter]

            display_cols = ['first_name', 'last_name', 'position', 'specialization', 'phone', 'status', 'total_debt']
            display_df = filtered_df[display_cols].copy()
            display_df.columns = ['نام', 'نام خانوادگی', 'پوزیشن', 'تخصص', 'تلفن', 'وضعیت', 'بدهی']

            st.dataframe(display_df, width="stretch", hide_index=True)

            # جزئیات پرسنل
            st.subheader("🔍 جزئیات پرسنل")
            if not filtered_df.empty:
                selected_staff = st.selectbox(
                    "انتخاب پرسنل",
                    options=filtered_df.apply(lambda x: f"{x['first_name']} {x['last_name']} - {x['position']}", axis=1)
                )

                if selected_staff:
                    staff_id = filtered_df.iloc[filtered_df.apply(lambda x: f"{x['first_name']} {x['last_name']} - {x['position']}", axis=1).tolist().index(selected_staff)]['id']
                    staff_info = filtered_df[filtered_df['id'] == staff_id].iloc[0]

                    col_d1, col_d2 = st.columns(2)
                    
                    with col_d1:
                        st.markdown(f"""
                            <div class="staff-card">
                                <h4 style="color: #00C8FF;">📋 اطلاعات پایه</h4>
                                <p><span style="color: #7FBAFF;">نام:</span> {staff_info['first_name']} {staff_info['last_name']}</p>
                                <p><span style="color: #7FBAFF;">کد ملی:</span> {staff_info['national_id']}</p>
                                <p><span style="color: #7FBAFF;">تلفن:</span> {staff_info['phone'] or '---'}</p>
                                <p><span style="color: #7FBAFF;">تاریخ استخدام:</span> {staff_info['hire_date']}</p>
                            </div>
                        """, unsafe_allow_html=True)

                    with col_d2:
                        st.markdown(f"""
                            <div class="staff-card">
                                <h4 style="color: #00C8FF;">💼 اطلاعات شغلی</h4>
                                <p><span style="color: #7FBAFF;">پوزیشن:</span> {staff_info['position']}</p>
                                <p><span style="color: #7FBAFF;">تخصص:</span> {staff_info['specialization'] or '---'}</p>
                                <p><span style="color: #7FBAFF;">حقوق پایه:</span> {staff_info['salary']:,.0f} AFN</p>
                                <p><span style="color: #7FBAFF;">وضعیت:</span> {staff_info['status']}</p>
                            </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ هیچ پرسنلی ثبت نشده است.")

    # ===== Tab 2: ثبت پرسنل جدید =====
    with tab2:
        st.subheader("➕ ثبت پرسنل جدید")

        with st.form("new_staff_form"):
            col1, col2 = st.columns(2)

            with col1:
                new_first_name = st.text_input("نام *")
                new_last_name = st.text_input("نام خانوادگی *")
                new_national_id = st.text_input("کد ملی *")
                new_phone = st.text_input("تلفن")

            with col2:
                new_position = st.selectbox(
                    "پوزیشن *",
                    ["دندانپزشک", "دستیار", "منشی", "تکنسین", "مدیر", "نظافتچی", "تکنسین لابراتوار"]
                )
                new_specialization = st.text_input("تخصص")
                new_hire_date = st.date_input("تاریخ استخدام *", value=datetime.now())
                new_salary = st.number_input("حقوق پایه (AFN)", min_value=0, step=1000, value=0)

            new_address = st.text_area("آدرس")

            st.markdown("### 🔐 اطلاعات کاربری")
            col_u1, col_u2 = st.columns(2)
            with col_u1:
                new_username = st.text_input("نام کاربری *")
            with col_u2:
                new_password = st.text_input("رمز عبور *", type="password")

            submitted = st.form_submit_button("✅ ثبت پرسنل", width="stretch", type="primary")

            if submitted:
                if not all([new_first_name, new_last_name, new_national_id, new_position, new_username, new_password]):
                    st.error("❌ فیلدهای الزامی را پر کنید")
                else:
                    try:
                        with get_connection() as conn:
                            password_hash = hash_password(new_password)
                            
                            cursor = conn.execute("""
                                INSERT INTO staff (
                                    first_name, last_name, national_id, phone, address,
                                    position, specialization, hire_date, salary,
                                    username, password_hash, status
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                new_first_name, new_last_name, new_national_id,
                                new_phone, new_address, new_position, new_specialization,
                                new_hire_date.strftime('%Y-%m-%d'), new_salary,
                                new_username, password_hash, 'active'
                            ))
                            
                            staff_id = cursor.lastrowid

                            full_name = f"{new_first_name} {new_last_name}"
                            conn.execute("""
                                INSERT INTO users (username, password_hash, full_name, role)
                                VALUES (?, ?, ?, ?)
                            """, (new_username, password_hash, full_name, 'staff'))

                            conn.commit()

                        st.success("✅ پرسنل با موفقیت ثبت شد!")
                        st.balloons()
                        time.sleep(2)
                        st.rerun()

                    except sqlite3.IntegrityError as e:
                        if "national_id" in str(e):
                            st.error("❌ این کد ملی قبلاً ثبت شده است")
                        elif "username" in str(e):
                            st.error("❌ این نام کاربری قبلاً ثبت شده است")
                        else:
                            st.error(f"❌ خطا: {e}")

    # ===== Tab 3: مدیریت دسترسی‌ها (نسخه JSON) =====
    with tab3:
        st.subheader("🔐 مدیریت دسترسی‌های کاربران")

        # دریافت لیست کاربران از دیتابیس
        with get_connection() as conn:
            users_df = pd.read_sql_query("SELECT id, username, full_name, role FROM users ORDER BY id", conn)
        
        if users_df.empty:
            st.info("ℹ️ هیچ کاربری در سیستم یافت نشد.")
        else:
            # فیلتر کردن ادمین‌ها
            non_admin_users = users_df[users_df['role'] != 'admin']
            
            if non_admin_users.empty:
                st.info("ℹ️ هیچ کاربر غیر ادمینی یافت نشد. ابتدا یک کاربر ایجاد کنید.")
            else:
                # بارگذاری دسترسی‌های فعلی
                all_permissions = load_all_permissions()
                
                for _, user in non_admin_users.iterrows():
                    username = user['username']
                    full_name = user['full_name']
                    user_id = user['id']
                    
                    # دریافت دسترسی‌های فعلی این کاربر
                    user_perms = all_permissions.get(username, {
                        'patients_add': False,
                        'patients_view': False,
                        'emr_view': False,
                        'settings_access': False,
                        'treatment_plan_view': False
                    })
                    
                    with st.expander(f"👤 {full_name} ({username})"):
                        st.markdown("🔒 **تنظیم دسترسی‌ها:**")
                        
                        col_p1, col_p2 = st.columns(2)
                        
                        with col_p1:
                            st.markdown("**🏥 مدیریت بیماران**")
                            p_add = st.checkbox("➕ ثبت بیمار جدید", value=user_perms.get('patients_add', False), key=f"add_{username}")
                            p_view = st.checkbox("📋 مشاهده لیست بیماران", value=user_perms.get('patients_view', False), key=f"view_{username}")
                            emr_v = st.checkbox("🦷 مشاهده پرونده الکترونیک", value=user_perms.get('emr_view', False), key=f"emr_{username}")
                        
                        with col_p2:
                            st.markdown("**⚙️ تنظیمات و ابزارها**")
                            sett_a = st.checkbox("⚙️ دسترسی به تنظیمات", value=user_perms.get('settings_access', False), key=f"sett_{username}")
                            treat_v = st.checkbox("📋 مشاهده طرح درمان", value=user_perms.get('treatment_plan_view', False), key=f"treat_{username}")
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button(f"💾 ذخیره دسترسی‌ها", key=f"save_{username}"):
                                all_permissions[username] = {
                                    'patients_add': p_add,
                                    'patients_view': p_view,
                                    'emr_view': emr_v,
                                    'settings_access': sett_a,
                                    'treatment_plan_view': treat_v
                                }
                                save_all_permissions(all_permissions)
                                
                                # اگر همین کاربر بود، session را به روز کن
                                if st.session_state.user_info.get('username') == username:
                                    st.session_state.user_info['permissions'] = all_permissions[username]
                                
                                st.success(f"✅ دسترسی‌های کاربر '{username}' با موفقیت به روزرسانی شد.")
                                st.info("⚠️ کاربر باید از سیستم خارج و دوباره وارد شود تا دسترسی‌ها اعمال شوند.")
                                st.balloons()
                        
                        with col_btn2:
                            if st.button(f"🗑️ حذف کاربر", key=f"del_{username}"):
                                confirm = st.checkbox(f"آیا از حذف کاربر {username} مطمئن هستید؟", key=f"confirm_{username}")
                                if confirm:
                                    try:
                                        with get_connection() as conn:
                                            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
                                            conn.execute("DELETE FROM staff WHERE username = ?", (username,))
                                            conn.commit()
                                        
                                        # حذف از فایل دسترسی‌ها
                                        if username in all_permissions:
                                            del all_permissions[username]
                                            save_all_permissions(all_permissions)
                                        
                                        st.success(f"✅ کاربر {username} با موفقیت حذف شد.")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ خطا در حذف کاربر: {e}")
                
                st.info("💡 نکته: دسترسی‌های ادمین‌ها به صورت پیش‌فرض کامل است و در این لیست نمایش داده نمی‌شوند.")

    # ===== Tab 4: وام و کسورات =====
    with tab4:
        st.subheader("💰 مدیریت وام و کسورات")

        tab_l1, tab_l2 = st.tabs(["📝 ثبت وام جدید", "📋 لیست وام‌ها و بازپرداخت"])

        with tab_l1:
            try:
                with get_connection() as conn:
                    staff_for_loan = pd.read_sql_query(
                        "SELECT id, first_name, last_name FROM staff WHERE status = 'active'",
                        conn
                    )
            except:
                staff_for_loan = pd.DataFrame()

            if not staff_for_loan.empty:
                with st.form("loan_form"):
                    col_l1, col_l2 = st.columns(2)

                    with col_l1:
                        selected_staff_loan = st.selectbox(
                            "انتخاب پرسنل",
                            options=staff_for_loan.apply(lambda x: f"{x['first_name']} {x['last_name']}", axis=1)
                        )
                        loan_amount = st.number_input("مبلغ وام (AFN)", min_value=0, step=1000, value=0)

                    with col_l2:
                        loan_date = st.date_input("تاریخ وام", value=datetime.now())
                        loan_description = st.text_input("توضیحات", placeholder="دلیل وام...")

                    if st.form_submit_button("✅ ثبت وام", width="stretch", type="primary"):
                        staff_id = staff_for_loan.iloc[staff_for_loan.apply(lambda x: f"{x['first_name']} {x['last_name']}", axis=1).tolist().index(selected_staff_loan)]['id']

                        try:
                            with get_connection() as conn:
                                conn.execute("""
                                    INSERT INTO staff_loans (staff_id, loan_date, amount, remaining_amount, description, status)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                """, (staff_id, loan_date.strftime('%Y-%m-%d'), loan_amount, loan_amount, loan_description, 'active'))
                                conn.commit()
                            st.success("✅ وام با موفقیت ثبت شد!")
                            st.balloons()
                            time.sleep(2)
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطا: {e}")

        with tab_l2:
            try:
                with get_connection() as conn:
                    loans_df = pd.read_sql_query("""
                        SELECT l.*, s.first_name, s.last_name, s.position
                        FROM staff_loans l
                        JOIN staff s ON l.staff_id = s.id
                        WHERE l.status = 'active'
                        ORDER BY l.loan_date DESC
                    """, conn)
            except:
                loans_df = pd.DataFrame()

            if not loans_df.empty:
                for _, loan in loans_df.iterrows():
                    with st.expander(f"وام {loan['first_name']} {loan['last_name']} - {loan['amount']:,.0f} AFN"):
                        st.markdown(f"""
                            <div style="background: rgba(20,30,54,0.8); padding: 15px; border-radius: 10px;">
                                <p><span style="color: #7FBAFF;">مبلغ وام:</span> {loan['amount']:,.0f} AFN</p>
                                <p><span style="color: #7FBAFF;">باقی‌مانده:</span> <span style="color: #E74C3C; font-weight: 700;">{loan['remaining_amount']:,.0f} AFN</span></p>
                                <p><span style="color: #7FBAFF;">تاریخ:</span> {loan['loan_date']}</p>
                                <p><span style="color: #7FBAFF;">توضیحات:</span> {loan['description'] or '---'}</p>
                            </div>
                        """, unsafe_allow_html=True)

                        with st.form(f"payment_form_{loan['id']}"):
                            col_p1, col_p2 = st.columns(2)
                            with col_p1:
                                payment_amount = st.number_input(
                                    "مبلغ بازپرداخت",
                                    min_value=0,
                                    max_value=int(loan['remaining_amount']),
                                    step=100,
                                    key=f"pay_{loan['id']}"
                                )
                            with col_p2:
                                payment_method = st.selectbox(
                                    "روش پرداخت",
                                    ["نقدی", "کارت بانکی", "چک", "کسری از حقوق"],
                                    key=f"method_{loan['id']}"
                                )

                            if st.form_submit_button("💳 ثبت بازپرداخت", width="stretch"):
                                try:
                                    with get_connection() as conn:
                                        conn.execute("""
                                            INSERT INTO loan_payments (loan_id, payment_date, amount, payment_method)
                                            VALUES (?, ?, ?, ?)
                                        """, (loan['id'], datetime.now().strftime('%Y-%m-%d'), payment_amount, payment_method))

                                        new_remaining = loan['remaining_amount'] - payment_amount
                                        new_status = 'active' if new_remaining > 0 else 'paid'
                                        
                                        conn.execute("""
                                            UPDATE staff_loans
                                            SET remaining_amount = ?, status = ?
                                            WHERE id = ?
                                        """, (new_remaining, new_status, loan['id']))
                                        
                                        conn.commit()
                                    st.success("✅ بازپرداخت با موفقیت ثبت شد!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ خطا: {e}")
            else:
                st.info("ℹ️ هیچ وام فعالی یافت نشد")

                # ===== Tab 5: حضور و غیاب =====
    with tab5:
        st.markdown("""
        <style>
        /* استایل کلی */
        .att-title {
            text-align: center;
            margin-bottom: 8px;
        }
        .att-title h3 {
            color: #00C8FF;
            font-size: 18px;
            margin: 0;
            text-shadow: 0 0 8px #00C8FF;
        }
        .att-title p {
            color: #7FBAFF;
            font-size: 10px;
            margin: 2px 0 0 0;
        }
        .att-box {
            background: #0E1629;
            border: 1px solid #00C8FF;
            border-radius: 6px;
            padding: 4px 6px;
            margin-bottom: 8px;
        }
        .att-day-header {
            background: linear-gradient(135deg, #00C8FF, #0066FF);
            color: white;
            text-align: center;
            padding: 3px 0;
            border-radius: 4px;
            font-size: 9px;
            font-weight: 600;
            width: 100%;
            margin-bottom: 2px;
        }
        .att-empty {
            background: #0A0F1F;
            border: 1px solid #2C3E50;
            border-radius: 4px;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 36px;
            width: 100%;
            color: #4a627a;
            font-size: 9px;
        }
        .att-legend {
            display: flex;
            justify-content: center;
            gap: 6px;
            margin: 6px 0;
            flex-wrap: wrap;
        }
        .att-legend span {
            padding: 1px 6px;
            border-radius: 10px;
            font-size: 8px;
            font-weight: 600;
        }
        .att-stat-card {
            background: #0E1629;
            border: 1px solid #00C8FF;
            border-radius: 5px;
            padding: 4px 2px;
            text-align: center;
        }
        .att-stat-number {
            font-size: 12px;
            font-weight: 700;
            color: #00C8FF;
        }
        .att-stat-label {
            font-size: 7px;
            color: #7FBAFF;
            margin-top: 1px;
        }
        
        /* دکمه‌ها - استایل مشابه بخش ادمین */
        .stButton {
            width: 100%;
        }
        
        .stButton button {
            width: 100% !important;
            height: 36px !important;
            min-height: 36px !important;
            max-height: 36px !important;
            padding: 0 !important;
            margin: 0 !important;
            border-radius: 4px !important;
            font-size: 9px !important;
            font-weight: 600 !important;
            white-space: pre-line !important;
            line-height: 1.1 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            flex-direction: column !important;
            transition: all 0.2s ease !important;
            border: none !important;
            cursor: pointer !important;
            color: white !important;
        }
        
        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 0 8px currentColor;
            filter: brightness(1.05);
        }
        
        /* ستون‌ها - فاصله افقی کم */
        .stColumn {
            padding: 0 1px !important;
        }
        
        /* فاصله عمودی بین ردیف‌ها - چسبیده */
        .stHorizontalBlock {
            gap: 1px !important;
            margin-bottom: 0px !important;
        }
        
        /* حذف تمام فاصله‌های اضافی */
        .element-container {
            margin-bottom: 0 !important;
        }
        
        .stMarkdown {
            margin-bottom: 0 !important;
        }
        
        /* selectbox */
        .stSelectbox label {
            display: none;
        }
        .stSelectbox > div {
            background: #0E1629;
            border: 1px solid #00C8FF;
            border-radius: 5px;
        }
        
        /* دکمه بروزرسانی */
        .stButton button[key="refresh_btn"] {
            background: linear-gradient(135deg, #00C8FF, #0066FF) !important;
            height: 30px !important;
            min-height: 30px !important;
            max-height: 30px !important;
            font-size: 9px !important;
            margin-top: 5px !important;
        }
        .stButton button[key="refresh_btn"]:hover {
            transform: translateY(-1px);
            box-shadow: 0 0 12px #00C8FF;
        }
        </style>
        """, unsafe_allow_html=True)

        # عنوان
        st.markdown("""
        <div class="att-title">
            <h3>⚡ حضور و غیاب کارکنان ⚡</h3>
            <p>کلیک روی هر روز برای تغییر وضعیت</p>
        </div>
        """, unsafe_allow_html=True)

        # انتخاب‌ها
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="att-box">', unsafe_allow_html=True)
            months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
            selected_month_name = st.selectbox("ماه", months, index=datetime.now().month - 1, label_visibility="collapsed")
            selected_month = months.index(selected_month_name) + 1
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="att-box">', unsafe_allow_html=True)
            current_year = datetime.now().year
            selected_year = st.selectbox("سال", [current_year-1, current_year, current_year+1], index=1, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="att-box">', unsafe_allow_html=True)
            with get_connection() as conn:
                staffs = conn.execute("SELECT id, first_name, last_name, username FROM staff WHERE status = 'active' ORDER BY first_name").fetchall()
            
            if not staffs:
                st.warning("⚠️ هیچ کارمندی یافت نشد")
                return
            
            staff_list = [f"{s[1]} {s[2]}" for s in staffs]
            staff_idx = st.selectbox("کارمند", range(len(staff_list)), format_func=lambda x: staff_list[x], label_visibility="collapsed")
            staff_id = staffs[staff_idx][0]
            staff_username = staffs[staff_idx][3]
            staff_name = staff_list[staff_idx]
            st.markdown('</div>', unsafe_allow_html=True)

        # راهنما
        st.markdown("""
        <div class="att-legend">
            <span style="background: linear-gradient(135deg, #00C8FF, #0066FF); color:white;">🔵 حاضر کامل</span>
            <span style="background: linear-gradient(135deg, #42A5F5, #1E88E5); color:white;">💙 نیمه حضور</span>
            <span style="background: linear-gradient(135deg, #1565C0, #0D47A1); color:white;">🌀 غایب</span>
            <span style="background: linear-gradient(135deg, #00C8FF, #0066FF); color:white;">✨ کلیک</span>
        </div>
        """, unsafe_allow_html=True)

        # اطلاعات کارمند
        st.markdown(f"""
        <div class="att-box" style="text-align:center;">
            <span style="color:#00C8FF; font-weight:600;">👤 {staff_name}</span>
            <span style="color:#7FBAFF; margin-left:6px;">📅 {selected_month_name} {selected_year}</span>
        </div>
        """, unsafe_allow_html=True)

        # دریافت اطلاعات حضور
        import calendar
        days_in_month = calendar.monthrange(selected_year, selected_month)[1]
        
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT date, check_in, check_out FROM staff_attendance 
                WHERE (staff_id = ? OR staff_username = ?)
                AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
            """, (staff_id, staff_username, str(selected_year), f"{selected_month:02d}")).fetchall()
        
        att_dict = {}
        for r in rows:
            if r[0]:
                try:
                    day = int(r[0].split('-')[2])
                    att_dict[day] = {'in': r[1], 'out': r[2]}
                except:
                    pass

        # هدر روزها
        weekdays = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']
        header_cols = st.columns(7, gap="small")
        for i, day in enumerate(weekdays):
            header_cols[i].markdown(f'<div class="att-day-header">{day}</div>', unsafe_allow_html=True)

        # گرید
        first_day = datetime(selected_year, selected_month, 1)
        start_weekday = (first_day.weekday() + 1) % 7
        
        cells = []
        for _ in range(start_weekday):
            cells.append(None)
        for d in range(1, days_in_month + 1):
            cells.append(d)
        
        rows_grid = [cells[i:i+7] for i in range(0, len(cells), 7)]

        # نمایش دکمه‌ها با استایل گرادیان
        for row in rows_grid:
            cols = st.columns(7, gap="small")
            for i, cell in enumerate(row):
                if cell is None:
                    with cols[i]:
                        st.markdown('<div class="att-empty">—</div>', unsafe_allow_html=True)
                else:
                    day_num = cell
                    info = att_dict.get(day_num, {})
                    has_in = info.get('in')
                    has_out = info.get('out')
                    
                    if has_in and has_out:
                        btn_gradient = "linear-gradient(135deg, #00C8FF, #0066FF)"
                        btn_text = "🟢"
                    elif has_in and not has_out:
                        btn_gradient = "linear-gradient(135deg, #42A5F5, #1E88E5)"
                        btn_text = "🟡"
                    else:
                        btn_gradient = "linear-gradient(135deg, #1565C0, #0D47A1)"
                        btn_text = "🔴"
                    
                    with cols[i]:
                        btn_key = f"att_{staff_id}_{selected_year}_{selected_month}_{day_num}"
                        
                        if st.button(f"{btn_text}\n{day_num}", key=btn_key, use_container_width=True):
                            if not has_in and not has_out:
                                new_in = "08:00"
                                new_out = None
                            elif has_in and not has_out:
                                new_in = has_in
                                new_out = "16:00"
                            else:
                                new_in = None
                                new_out = None
                            
                            date_str = f"{selected_year}-{selected_month:02d}-{day_num:02d}"
                            
                            try:
                                with get_connection() as conn:
                                    exist = conn.execute("""
                                        SELECT id FROM staff_attendance 
                                        WHERE (staff_id = ? OR staff_username = ?) AND date = ?
                                    """, (staff_id, staff_username, date_str)).fetchone()
                                    
                                    if new_in is None and new_out is None:
                                        if exist:
                                            conn.execute("DELETE FROM staff_attendance WHERE id = ?", (exist[0],))
                                    else:
                                        if exist:
                                            conn.execute("UPDATE staff_attendance SET check_in = ?, check_out = ? WHERE id = ?", (new_in, new_out, exist[0]))
                                        else:
                                            conn.execute("INSERT INTO staff_attendance (staff_id, staff_username, date, check_in, check_out) VALUES (?, ?, ?, ?, ?)", (staff_id, staff_username, date_str, new_in, new_out))
                                    conn.commit()
                                st.rerun()
                            except Exception as e:
                                st.error(f"خطا: {e}")
                        
                        # استایل دکمه با گرادیان
                        st.markdown(f"""
                        <style>
                        div[data-testid="column"] button[key="{btn_key}"] {{
                            background: {btn_gradient} !important;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
                        }}
                        div[data-testid="column"] button[key="{btn_key}"]:hover {{
                            transform: translateY(-1px);
                            box-shadow: 0 0 8px #00C8FF;
                            filter: brightness(1.05);
                        }}
                        </style>
                        """, unsafe_allow_html=True)

        st.markdown("---")

        # آمار
        st.markdown('<div style="text-align:center; margin-bottom:2px;"><span style="color:#00C8FF; font-size:9px; font-weight:600;">📊 خلاصه آمار</span></div>', unsafe_allow_html=True)
        
        full = 0
        half = 0
        absent = 0
        
        for d in range(1, days_in_month + 1):
            info = att_dict.get(d, {})
            if info.get('in') and info.get('out'):
                full += 1
            elif info.get('in') and not info.get('out'):
                half += 1
            else:
                absent += 1
        
        percent = round(((full + half) / days_in_month) * 100) if days_in_month > 0 else 0
        
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f"""
            <div class="att-stat-card">
                <div class="att-stat-number">🔵 {full}</div>
                <div class="att-stat-label">حاضر کامل</div>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"""
            <div class="att-stat-card">
                <div class="att-stat-number">💙 {half}</div>
                <div class="att-stat-label">نیمه حضور</div>
            </div>
            """, unsafe_allow_html=True)
        
        with c3:
            st.markdown(f"""
            <div class="att-stat-card">
                <div class="att-stat-number">🌀 {absent}</div>
                <div class="att-stat-label">غایب</div>
            </div>
            """, unsafe_allow_html=True)
        
        with c4:
            st.markdown(f"""
            <div class="att-stat-card">
                <div class="att-stat-number">📊 {percent}%</div>
                <div class="att-stat-label">درصد حضور</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🔄 بروزرسانی", key="refresh_btn", use_container_width=True):
            st.rerun()