import streamlit as st
import pandas as pd
import io
from datetime import datetime
from modules.database import get_connection
from modules.prescriptions import render_patient_prescription

# =========================================================================
# دیکشنری ترجمه برای بخش Add Patient
# =========================================================================
translations_patient = {
    "dr": {
        "page_title": "ثبت بیمار جدید",
        "page_subtitle": "فرم زیر را برای ثبت بیمار جدید در سیستم کلینیک دندان تکمیل کنید",
        "required_note": "تمام فیلدهای دارای <span style='color: #00C8FF;'>*</span> اجباری هستند",
        "personal_info": "اطلاعات شخصی",
        "first_name": "نام *",
        "last_name": "نام خانوادگی",
        "national_id": "کد ملی / شماره پاسپورت *",
        "phone": "شماره تماس",
        "age": "سن",
        "gender": "جنسیت",
        "male": "مرد",
        "female": "زن",
        "child": "کودک",
        "treatment_info": "اطلاعات درمانی",
        "service_type": "نوع خدمت دندانپزشکی",
        "tooth_number": "شماره دندان / موقعیت",
        "doctor_notes": "یادداشت‌ها و مشاهدات پزشک",
        "next_appointment": "نوبت بعدی",
        "next_visit_date": "تاریخ ویزیت بعدی",
        "next_visit_time": "ساعت ویزیت بعدی",
        "financial_info": "اطلاعات مالی",
        "total_fee": "هزینه کل درمان (AFN)",
        "paid_amount": "مبلغ پرداختی فعلی (AFN)",
        "discount": "تخفیف (AFN)",
        "payment_summary": "خلاصه پرداخت",
        "remaining_balance": "مانده باقیمانده",
        "fully_paid": "تسویه کامل ✓",
        "balance": "مانده حساب",
        "review_submit": "مرور و ثبت",
        "review_info": "لطفاً قبل از ثبت، تمام اطلاعات را مرور کنید",
        "personal_info_review": "اطلاعات شخصی",
        "treatment_info_review": "اطلاعات درمانی",
        "financial_summary": "خلاصه مالی",
        "save_patient": "✅ ثبت بیمار",
        "required_error": "❌ نام و کد ملی اجباری هستند",
        "success_msg": "✅ بیمار '{name}' با موفقیت ثبت شد!",
        "patient_id": "شناسه بیمار",
        "service": "خدمت",
        "total_fee_label": "هزینه کل",
        "balance_label": "مانده حساب",
        "what_next": "🔄 بعد از ثبت، چه کاری انجام دهید؟",
        "go_to_emr": "🦷 رفتن به پرونده الکترونیک",
        "go_to_list": "📋 رفتن به لیست بیماران",
        "register_another": "➕ ثبت بیمار دیگر",
        "redirect_msg": "⏳ در غیر این صورت، بعد از 3 ثانیه به لیست بیماران بازمی‌گردید...",
        "duplicate_error": "❌ این کد ملی قبلاً در سیستم ثبت شده است",
        "database_error": "❌ خطای دیتابیس",
        "add_new_service": "➕ افزودن سرویس جدید",
        "service_name": "نام سرویس",
        "service_price": "قیمت پیش‌فرض (AFN)",
        "save_service": "💾 ذخیره سرویس",
        "delete_service": "🗑️ حذف سرویس",
        "service_exists": "⚠️ این سرویس قبلاً وجود دارد",
        "service_added": "✅ سرویس جدید با موفقیت اضافه شد",
        "service_deleted": "✅ سرویس با موفقیت حذف شد",
        "manage_services": "➕ مدیریت خدمات دندانپزشکی",
        "service_list_title": "📋 لیست خدمات موجود"
    },
    "en": {
        "page_title": "Register New Patient",
        "page_subtitle": "Complete the form below to register a new patient in the dental clinic system",
        "required_note": "All fields marked with <span style='color: #00C8FF;'>*</span> are required",
        "personal_info": "Personal Information",
        "first_name": "First Name *",
        "last_name": "Last Name",
        "national_id": "National ID / Passport No. *",
        "phone": "Phone Number",
        "age": "Age",
        "gender": "Gender",
        "male": "Male",
        "female": "Female",
        "child": "Child",
        "treatment_info": "Treatment Information",
        "service_type": "Type of Dental Service",
        "tooth_number": "Tooth Number / Location",
        "doctor_notes": "Doctor's Notes & Observations",
        "next_appointment": "Next Appointment",
        "next_visit_date": "Next Visit Date",
        "next_visit_time": "Next Visit Time",
        "financial_info": "Financial Information",
        "total_fee": "Total Treatment Fee (AFN)",
        "paid_amount": "Current Paid Amount (AFN)",
        "discount": "Discount (AFN)",
        "payment_summary": "Payment Summary",
        "remaining_balance": "Remaining Balance",
        "fully_paid": "Fully Paid ✓",
        "balance": "Balance",
        "review_submit": "Review & Submit",
        "review_info": "Please review all information before submitting",
        "personal_info_review": "Personal Information",
        "treatment_info_review": "Treatment Information",
        "financial_summary": "Financial Summary",
        "save_patient": "✅ Save Patient Record",
        "required_error": "❌ First Name and National ID are mandatory",
        "success_msg": "✅ Patient '{name}' successfully registered!",
        "patient_id": "Patient ID",
        "service": "Service",
        "total_fee_label": "Total Fee",
        "balance_label": "Balance",
        "what_next": "🔄 What would you like to do next?",
        "go_to_emr": "🦷 Go to EMR",
        "go_to_list": "📋 Go to Patient List",
        "register_another": "➕ Register Another",
        "redirect_msg": "⏳ If no selection, redirecting to Patient List in 3 seconds...",
        "duplicate_error": "❌ This National ID is already registered in the system",
        "database_error": "❌ Database Error",
        "add_new_service": "➕ Add New Service",
        "service_name": "Service Name",
        "service_price": "Default Price (AFN)",
        "save_service": "💾 Save Service",
        "delete_service": "🗑️ Delete Service",
        "service_exists": "⚠️ This service already exists",
        "service_added": "✅ New service added successfully",
        "service_deleted": "✅ Service deleted successfully",
        "manage_services": "➕ Manage Dental Services",
        "service_list_title": "📋 Service List"
    }
}

def t_patient(key):
    lang = st.session_state.get("dashboard_language", "dr")
    return translations_patient[lang].get(key, key)


# =========================================================================
# توابع مدیریت خدمات دندانپزشکی
# =========================================================================

def get_dental_services():
    """دریافت لیست خدمات از دیتابیس"""
    try:
        with get_connection() as conn:
            # ایجاد جدول اگر وجود ندارد
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dental_services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_name TEXT UNIQUE,
                    default_price REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # سرویس‌های پیش‌فرض اگر جدول خالی است
            cursor = conn.execute("SELECT COUNT(*) FROM dental_services")
            if cursor.fetchone()[0] == 0:
                default_services = [
                    ("General Checkup", 500.0),
                    ("Filling", 1500.0),
                    ("RCT (Root Canal)", 3500.0),
                    ("Extraction", 1200.0),
                    ("Implant", 25000.0),
                    ("Orthodontics", 30000.0),
                    ("Teeth Cleaning", 1000.0),
                    ("Whitening", 7000.0),
                    ("Crown", 10000.0),
                    ("Bridge", 15000.0)
                ]
                conn.executemany("INSERT INTO dental_services (service_name, default_price) VALUES (?, ?)", default_services)
                conn.commit()
            
            # دریافت لیست خدمات
            services = conn.execute("SELECT service_name, default_price FROM dental_services ORDER BY service_name").fetchall()
            return [{"name": s[0], "price": float(s[1])} for s in services]
    except Exception as e:
        return [{"name": "General Checkup", "price": 500.0}]

def add_dental_service(service_name, service_price):
    """افزودن سرویس جدید به دیتابیس"""
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO dental_services (service_name, default_price) VALUES (?, ?)", (service_name, service_price))
            conn.commit()
            return True, None
    except Exception as e:
        if "UNIQUE" in str(e):
            return False, "duplicate"
        return False, str(e)

def delete_dental_service(service_name):
    """حذف سرویس از دیتابیس"""
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM dental_services WHERE service_name = ?", (service_name,))
            conn.commit()
            return True
    except Exception as e:
        return False


def render_patient_list():
    st.header("🏥 Comprehensive Patient Records & Financial Reports")
    
    # Check if we're in prescription mode
    if 'show_prescription' not in st.session_state:
        st.session_state.show_prescription = False
    if 'selected_patient_id' not in st.session_state:
        st.session_state.selected_patient_id = None
    
    # If prescription mode is active, show prescription form
    if st.session_state.show_prescription and st.session_state.selected_patient_id:
        # Prescription back button
        if st.button("← Back to Patient List"):
            st.session_state.show_prescription = False
            st.session_state.selected_patient_id = None
            st.rerun()
        
        # Render prescription for selected patient
        render_patient_prescription(st.session_state.selected_patient_id)
        return
    
    # ===== ORIGINAL PATIENT LIST CODE =====
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM patients ORDER BY id DESC", conn)

    if df.empty:
        st.info("📝 No patient records found in the system.")
        return

    st.subheader("🔍 Search & Filter")
    search_query = st.text_input(
        "Search all fields (Name, ID, Service, Tooth No, Notes, etc.):",
        placeholder="e.g., Faisal, 26, Root Canal, Debt..."
    )
    
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False, na=False).any(), axis=1)]

    st.write(f"📊 Total results found: **{len(df)}** records")

    display_df = df.copy()
    display_df['cost'] = display_df['cost'].apply(lambda x: f"{x:,.0f} AFN")
    
    rename_columns = {
        'id': 'ID',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'national_id': 'National ID',
        'age': 'Age',
        'gender': 'Gender',
        'service_type': 'Service & Treatment Details',
        'cost': 'Total Fee (AFN)',
        'appointment_date': 'Visit Date',
        'phone': 'Phone Number',
        'status': 'Status'
    }

    st.dataframe(
        display_df.rename(columns=rename_columns),
        width="stretch", 
        hide_index=True
    )

    st.divider()
    
    # ===== PRESCRIPTION SECTION =====
    st.subheader("💊 Prescription Management")
    
    if not df.empty:
        # Create patient selection for prescription
        patient_options = []
        for idx, row in df.iterrows():
            display_text = f"ID {row['id']}: {row['first_name']} {row['last_name']} - {row['age']}yrs, {row['gender']}"
            patient_options.append((row['id'], display_text))
        
        selected_option = st.selectbox(
            "Select a patient for prescription:",
            options=patient_options,
            format_func=lambda x: x[1],
            index=0
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Create Prescription", type="primary", use_container_width=True):
                st.session_state.selected_patient_id = selected_option[0]
                st.session_state.show_prescription = True
                st.rerun()
        
        with col2:
            patient_data = df[df['id'] == selected_option[0]].iloc[0]
            if st.button("👁️ View Details", use_container_width=True):
                st.info(f"""
                **Patient Details:**
                - **Name:** {patient_data['first_name']} {patient_data['last_name']}
                - **Age:** {patient_data['age']} | **Gender:** {patient_data['gender']}
                - **Phone:** {patient_data['phone']}
                - **Last Service:** {patient_data['service_type']}
                - **Last Visit:** {patient_data['appointment_date']}
                """)
    
    st.divider()
    
    # ===== DELETE SECTION =====
    with st.expander("🗑️ Manage & Permanently Delete Records"):
        col_del1, col_del2 = st.columns([1, 2])
        with col_del1:
            id_to_delete = st.number_input("Enter Record ID to delete:", min_value=1, step=1)
        with col_del2:
            st.write(" ")
            st.write(" ")
            if st.button("Confirm and Delete from System"):
                with get_connection() as conn:
                    check = conn.execute("SELECT first_name, last_name FROM patients WHERE id=?", (id_to_delete,)).fetchone()
                    if check:
                        conn.execute("DELETE FROM patients WHERE id=?", (id_to_delete,))
                        conn.commit()
                        st.error(f"❗ Record for '{check[0]} {check[1]}' has been permanently deleted.")
                        st.rerun()
                    else:
                        st.warning("The specified ID was not found in the database.")

    # ===== EXPORT SECTION =====
    st.sidebar.divider()
    st.sidebar.subheader("📥 Export Reports")
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Clinic_Report')
        
    excel_data = output.getvalue()
    st.sidebar.download_button(
        label="📥 Download List as Excel",
        data=excel_data,
        file_name=f"Clinic_Report_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def render_add_patient():
    # ========== مدیریت وضعیت زبان ==========
    if 'dashboard_language' not in st.session_state:
        st.session_state.dashboard_language = "dr"
    
    # ========== استایل کامل ==========
    st.markdown("""
    <style>
    /* استایل دکمه تغییر زبان */
    div.stButton > button:first-child {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #00C8FF !important;
        border: 1px solid #00C8FF !important;
        border-radius: 8px !important;
        padding: 4px 15px !important;
        font-weight: 500 !important;
        font-size: 12px !important;
        transition: all 0.3s ease !important;
        float: right !important;
    }

    div.stButton > button:first-child:hover {
        background: #00C8FF !important;
        color: #0A0F1F !important;
        box-shadow: 0 0 15px rgba(0, 200, 255, 0.4) !important;
        border-color: transparent !important;
    }
    
    /* رفع مشکل selectbox */
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #141E36 !important;
        border: 2px solid #00C8FF !important;
        border-radius: 40px !important;
        min-height: 42px !important;
    }
    
    .stSelectbox [data-baseweb="select"] div[role="button"] {
        color: white !important;
        font-size: 14px !important;
    }
    
    .stSelectbox [data-baseweb="select"] div[aria-selected="true"] {
        color: white !important;
        background: #1A2745 !important;
    }
    
    div[role="listbox"] {
        background: #0E1629 !important;
        border: 1px solid #00C8FF !important;
        border-radius: 15px !important;
    }
    
    div[role="listbox"] div[role="option"] {
        color: white !important;
        background: #0E1629 !important;
        padding: 10px 15px !important;
    }
    
    div[role="listbox"] div[role="option"]:hover {
        background: #00C8FF !important;
        color: #0A0F1F !important;
    }
    
    .stSelectbox [data-baseweb="select"] span {
        color: white !important;
    }
    
    .stSelectbox label {
        color: #7FBAFF !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
    }
    
    /* استایل فرم Add Patient */
    .add-patient-header {
        background: linear-gradient(135deg, #0A0F1F, #0E1629);
        padding: 30px 25px;
        border-radius: 25px;
        margin-bottom: 30px;
        border: 2px solid #00C8FF;
        box-shadow: 0 10px 25px -10px rgba(0, 200, 255, 0.3);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .add-patient-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        right: -50%;
        bottom: -50%;
        background: radial-gradient(circle, rgba(0, 200, 255, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .add-patient-header h1 {
        color: white;
        font-size: 36px;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 15px #00C8FF;
    }
    .add-patient-header p {
        color: #7FBAFF;
        font-size: 16px;
        margin: 10px 0 0 0;
    }
    .section-header {
        color: #00C8FF !important;
        border-bottom: 3px solid #0066FF;
        padding-bottom: 15px;
        margin: 30px 0 20px 0;
        font-weight: 700;
        font-size: 24px;
        text-shadow: 0 0 10px #00C8FF;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: #141E36 !important;
        border: 2px solid #00C8FF !important;
        border-radius: 40px !important;
        color: white !important;
        padding: 10px 20px !important;
    }
    .info-card {
        background: linear-gradient(135deg, #141E36, #0E1629);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #4D9EFF;
        margin: 20px 0;
    }
    .payment-summary {
        background: linear-gradient(135deg, #141E36, #0E1629);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #00C8FF;
        margin-top: 20px;
    }
    .review-card {
        background: linear-gradient(135deg, #141E36, #0E1629);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #00C8FF;
        margin-bottom: 20px;
    }
    .metric-card {
        background: linear-gradient(135deg, #141E36, #0E1629);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #00C8FF;
        text-align: center;
    }
    .metric-value {
        color: white;
        font-size: 24px;
        font-weight: 700;
    }
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00C8FF, #0066FF, #4D9EFF, #7FBAFF, transparent);
        margin: 30px 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: #0E1629;
        padding: 15px 20px;
        border-radius: 40px;
        border: 2px solid #00C8FF;
        margin-bottom: 30px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 30px;
        padding: 12px 32px;
        color: #7FBAFF !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00C8FF 0%, #0066FF 100%) !important;
        color: #0A0F1F !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ========== دکمه تغییر زبان ==========
    current_lang = st.session_state.dashboard_language
    label = "Switch to English 🇬🇧" if current_lang == "dr" else "تغییر به دری 🇦🇫"
    
    if st.button(label):
        st.session_state.dashboard_language = "en" if current_lang == "dr" else "dr"
        st.rerun()
    
    # ========== Header فرم ==========
    st.markdown(f"""
        <div class="add-patient-header">
            <h1>👨‍⚕️ {t_patient('page_title')}</h1>
            <p>{t_patient('page_subtitle')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="color: #7FBAFF; margin-bottom: 30px; font-size: 16px; text-align: center;">
            {t_patient('required_note')}
        </div>
    """, unsafe_allow_html=True)
    
    # ========== Tab 1: Personal Info ==========
    tab1, tab2, tab3, tab4 = st.tabs([
        f"👤 {t_patient('personal_info')}", 
        f"🦷 {t_patient('treatment_info')}", 
        f"💰 {t_patient('financial_info')}", 
        f"📋 {t_patient('review_submit')}"
    ])
    
    with tab1:
        st.markdown(f'<div class="section-header">{t_patient("personal_info")}</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            f_name = st.text_input(f"**{t_patient('first_name')}**", placeholder="Enter first name")
            l_name = st.text_input(f"**{t_patient('last_name')}**", placeholder="Enter last name")
        
        with col2:
            n_id = st.text_input(f"**{t_patient('national_id')}**", placeholder="e.g., 123456789")
            phone = st.text_input(f"**{t_patient('phone')}**", placeholder="+93 70 123 4567")
        
        with col3:
            age = st.number_input(f"**{t_patient('age')}**", min_value=1, max_value=120, value=25)
            gender = st.selectbox(
                f"**{t_patient('gender')}**", 
                [t_patient('male'), t_patient('female'), t_patient('child')],
                index=0
            )
        
        st.markdown(f"""
            <div class="info-card">
                <p><span style="color: #00C8FF;">ⓘ</span> <strong>Note:</strong> {t_patient('first_name')} and {t_patient('national_id')} are mandatory fields.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown(f'<div class="section-header">{t_patient("treatment_info")}</div>', unsafe_allow_html=True)
        
        # ========== دریافت لیست خدمات از دیتابیس ==========
        services = get_dental_services()
        service_names = [s["name"] for s in services]
        
        # ========== بخش مدیریت خدمات (با ترجمه کامل) ==========
        with st.expander(t_patient('manage_services'), expanded=False):
            st.markdown(f"### {t_patient('add_new_service')}")
            
            col_add1, col_add2, col_add3 = st.columns([2, 1, 1])
            
            with col_add1:
                new_service_name = st.text_input(t_patient('service_name'), placeholder="مثلاً: لمینت دندان", key="new_service_name")
            
            with col_add2:
                new_service_price = st.number_input(t_patient('service_price'), min_value=0.0, step=100.0, value=0.0, key="new_service_price")
            
            with col_add3:
                st.write("")
                st.write("")
                if st.button(t_patient('save_service'), key="save_service_btn", use_container_width=True):
                    if new_service_name.strip():
                        success, error = add_dental_service(new_service_name.strip(), float(new_service_price))
                        if success:
                            st.success(t_patient('service_added'))
                            st.rerun()
                        elif error == "duplicate":
                            st.error(t_patient('service_exists'))
                        else:
                            st.error(f"{t_patient('database_error')}: {error}")
                    else:
                        st.warning("لطفاً نام سرویس را وارد کنید")
            
            st.markdown("---")
            
            # لیست خدمات موجود با قابلیت حذف
            st.markdown(f"### {t_patient('service_list_title')}")
            
            default_services = ["General Checkup", "Filling", "RCT (Root Canal)", "Extraction", "Implant", "Orthodontics", "Teeth Cleaning", "Whitening", "Crown", "Bridge"]
            custom_services = [s for s in services if s["name"] not in default_services]
            
            if custom_services:
                for s in custom_services:
                    col_del1, col_del2 = st.columns([3, 1])
                    with col_del1:
                        st.write(f"**{s['name']}** - {s['price']:,.0f} AFN")
                    with col_del2:
                        if st.button(t_patient('delete_service'), key=f"del_{s['name']}", use_container_width=True):
                            if delete_dental_service(s['name']):
                                st.success(t_patient('service_deleted'))
                                st.rerun()
            else:
                st.info("برای افزودن سرویس جدید از فرم بالا استفاده کنید")
        
        # ========== انتخاب سرویس ==========
        selected_service = st.selectbox(
            f"**{t_patient('service_type')}**",
            options=service_names,
            index=0
        )
        
        # دریافت قیمت سرویس انتخاب شده
        selected_service_price = next((float(s["price"]) for s in services if s["name"] == selected_service), 0.0)
        
        # نمایش قیمت سرویس
        st.caption(f"💰 قیمت پیش‌فرض: {selected_service_price:,.0f} AFN")
        
        # بقیه فیلدهای درمانی
        tooth_number = st.text_input(f"**{t_patient('tooth_number')}**", placeholder="e.g., 14, 26 or Upper Jaw")
        doctor_notes = st.text_area(f"**{t_patient('doctor_notes')}**", 
                                   placeholder="Enter detailed notes, diagnosis, and prescription details",
                                   height=150)
        
        st.markdown(f"""
            <div class="next-appointment-section">
                <h4>🗓 {t_patient('next_appointment')}</h4>
            </div>
        """, unsafe_allow_html=True)
        
        col_next1, col_next2 = st.columns(2)
        with col_next1:
            next_date = st.date_input(f"**{t_patient('next_visit_date')}**", value=None)
        with col_next2:
            next_time = st.time_input(f"**{t_patient('next_visit_time')}**", value=None)
    
    with tab3:
        st.markdown(f'<div class="section-header">{t_patient("financial_info")}</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="info-card">
                <p><span style="color: #00C8FF;">ⓘ</span> <strong>Note:</strong> All amounts are in Afghanis (AFN)</p>
            </div>
        """, unsafe_allow_html=True)
        
        col6, col7, col8 = st.columns(3)
        with col6:
            total_cost = st.number_input(f"**{t_patient('total_fee')}**", min_value=0.0, step=100.0, value=float(selected_service_price))
        with col7:
            paid_amount = st.number_input(f"**{t_patient('paid_amount')}**", min_value=0.0, step=100.0, value=0.0)
        with col8:
            discount = st.number_input(f"**{t_patient('discount')}**", min_value=0.0, step=50.0, value=0.0)
        
        balance = total_cost - (paid_amount + discount)
        
        st.markdown(f"""
            <div class="payment-summary">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4>{t_patient('payment_summary')}</h4>
                        <p>Real-time balance calculation</p>
                    </div>
                    <div style="text-align: right;">
        """, unsafe_allow_html=True)
        
        if balance > 0:
            st.markdown(f"""
                        <span class="balance-positive">{balance:,.0f} AFN</span>
                        <div style="color: #FF6B6B; font-size: 14px;">{t_patient('remaining_balance')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif balance == 0 and total_cost > 0:
            st.markdown(f"""
                        <span class="balance-zero">{balance:,.0f} AFN</span>
                        <div style="color: #00C8FF; font-size: 14px;">{t_patient('fully_paid')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                        <span class="balance-pending">{balance:,.0f} AFN</span>
                        <div style="color: #7FBAFF; font-size: 14px;">{t_patient('balance')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown(f'<div class="section-header">{t_patient("review_submit")}</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="info-card">
                <h4>📋 {t_patient('review_info')}</h4>
            </div>
        """, unsafe_allow_html=True)
        
        col_sum1, col_sum2 = st.columns(2)
        
        with col_sum1:
            st.markdown(f"""
                <div class="review-card">
                    <strong>{t_patient('personal_info_review')}</strong><br><br>
            """, unsafe_allow_html=True)
            st.markdown(f"<strong>{t_patient('first_name')}:</strong> <span>{f_name if f_name else 'Not provided'} {l_name if l_name else ''}</span><br>", unsafe_allow_html=True)
            st.markdown(f"<strong>{t_patient('national_id')}:</strong> <span>{n_id if n_id else 'Not provided'}</span><br>", unsafe_allow_html=True)
            st.markdown(f"<strong>{t_patient('age')}:</strong> <span>{age}</span> | <strong>{t_patient('gender')}:</strong> <span>{gender}</span><br>", unsafe_allow_html=True)
            st.markdown(f"<strong>{t_patient('phone')}:</strong> <span>{phone if phone else 'Not provided'}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_sum2:
            st.markdown(f"""
                <div class="review-card">
                    <strong>{t_patient('treatment_info_review')}</strong><br><br>
            """, unsafe_allow_html=True)
            st.markdown(f"<strong>{t_patient('service_type')}:</strong> <span>{selected_service if selected_service else 'Not selected'}</span><br>", unsafe_allow_html=True)
            st.markdown(f"<strong>{t_patient('tooth_number')}:</strong> <span>{tooth_number if tooth_number else 'Not specified'}</span><br>", unsafe_allow_html=True)
            st.markdown(f"<strong>{t_patient('next_visit_date')}:</strong> <span>{next_date if next_date else 'Not scheduled'}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="review-card">
                <strong>{t_patient('financial_summary')}</strong><br><br>
        """, unsafe_allow_html=True)
        
        col_fin1, col_fin2, col_fin3 = st.columns(3)
        with col_fin1:
            st.markdown(f"""
                <div class="metric-card">
                    <label>{t_patient('total_fee')}</label>
                    <div class="metric-value">{total_cost:,.0f} AFN</div>
                </div>
            """, unsafe_allow_html=True)
        with col_fin2:
            st.markdown(f"""
                <div class="metric-card">
                    <label>{t_patient('paid_amount')}</label>
                    <div class="metric-value">{paid_amount:,.0f} AFN</div>
                </div>
            """, unsafe_allow_html=True)
        with col_fin3:
            st.markdown(f"""
                <div class="metric-card">
                    <label>{t_patient('balance')}</label>
                    <div class="metric-value" style="color: {'#FF6B6B' if balance > 0 else '#00C8FF'}">{balance:,.0f} AFN</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col_submit1, col_submit2, col_submit3 = st.columns([1, 2, 1])
    with col_submit2:
        submit_btn = st.button(f"✅ {t_patient('save_patient')}", use_container_width=True, type="primary")
    
    if submit_btn:
        if not f_name.strip() or not n_id.strip():
            st.error(f"❌ {t_patient('required_error')}")
        else:
            try:
                import time
                with get_connection() as conn:
                    cursor = conn.cursor()
                    service_details = f"{selected_service} (Tooth: {tooth_number})" if tooth_number else selected_service
                    
                    # تبدیل جنسیت به انگلیسی برای دیتابیس
                    gender_db = "Male" if gender == t_patient('male') else ("Female" if gender == t_patient('female') else "Child")
                    
                    sql = """
                        INSERT INTO patients 
                        (first_name, last_name, national_id, age, gender, service_type, 
                        cost, paid_amount, discount, appointment_date, 
                        next_visit_date, next_visit_time, phone, status) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    cursor.execute(sql, (
                        f_name, l_name, n_id, age, gender_db, service_details, 
                        float(total_cost), float(paid_amount), float(discount), 
                        datetime.now().strftime('%Y-%m-%d'), 
                        str(next_date) if next_date else None,
                        next_time.strftime('%H:%M') if next_time else None,
                        phone, "ACTIVE"
                    ))
                    conn.commit()
                    new_patient_id = cursor.lastrowid
                
                st.success(f"""
                ✅ **{t_patient('success_msg').format(name=f_name + ' ' + l_name)}**
                
                **Details:**
                - {t_patient('patient_id')}: {new_patient_id}
                - {t_patient('service')}: {service_details}
                - {t_patient('total_fee_label')}: {total_cost:,.0f} AFN
                - {t_patient('balance_label')}: {balance:,.0f} AFN
                """)
                
                st.balloons()
                
                st.markdown("---")
                st.markdown(f"### 🔄 {t_patient('what_next')}")
                
                col_after1, col_after2, col_after3 = st.columns(3)
                
                with col_after2:
                    if st.button(f"📋 {t_patient('go_to_list')}", use_container_width=True):
                        st.rerun()
                
                with col_after3:
                    if st.button(f"➕ {t_patient('register_another')}", use_container_width=True):
                        st.rerun()
                
                st.info(f"⏳ {t_patient('redirect_msg')}")
                time.sleep(3)
                st.rerun()
                
            except Exception as e:
                if "UNIQUE" in str(e):
                    st.error(f"❌ {t_patient('duplicate_error')}")
                else:
                    st.error(f"❌ {t_patient('database_error')}: {str(e)}")