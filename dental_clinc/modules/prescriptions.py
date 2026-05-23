import streamlit as st
import pandas as pd
import base64
from datetime import datetime
import streamlit.components.v1 as components
from modules.database import get_connection

# =========================================================================
# دیکشنری ترجمه برای بخش نسخه
# =========================================================================
translations_prescription = {
    "dr": {
        "page_title": "📝 سیستم نسخه نویسی",
        "back_to_list": "← بازگشت به لیست بیماران",
        "patient_info": "اطلاعات بیمار",
        "name": "نام",
        "age": "سن",
        "gender": "جنسیت",
        "patient_id": "شناسه بیمار",
        "service": "نوع خدمت",
        "last_visit": "آخرین ویزیت",
        "phone": "تلفن",
        "national_id": "کد ملی",
        "prescription_date": "تاریخ نسخه",
        "medicines": "💊 داروهای تجویزی",
        "select_medicines": "انتخاب داروها (چندین مورد را انتخاب کنید)",
        "custom_medicines": "➕ افزودن داروی جدید",
        "medicine_name": "نام دارو",
        "dosage": "مقدار مصرف",
        "frequency": "تناوب مصرف",
        "duration": "مدت مصرف",
        "note": "توضیحات ویژه",
        "save_medicine": "💾 ذخیره دارو",
        "delete_medicine": "🗑️ حذف دارو",
        "medicine_exists": "⚠️ این دارو قبلاً وجود دارد",
        "medicine_added": "✅ داروی جدید با موفقیت اضافه شد",
        "medicine_deleted": "✅ دارو با موفقیت حذف شد",
        "manage_medicines": "➕ مدیریت داروها",
        "medicine_list_title": "📋 لیست داروهای موجود",
        "enter_medicine_name": "لطفاً نام دارو را وارد کنید",
        "doctor_instructions": "📝 دستورالعمل پزشک",
        "instructions_placeholder": "مثال:\nداروها را بعد از غذا مصرف کنید\nاز غذاهای تند پرهیز کنید\nدوره درمان را کامل کنید",
        "generate_prescription": "📄 تولید نسخه حرفه‌ای",
        "clear_form": "🗑️ پاک کردن فرم",
        "select_at_least_one": "⚠️ لطفاً حداقل یک دارو انتخاب کنید یا داروی جدید اضافه کنید",
        "abbreviations": "💡 اختصارات: OD (روزی یکبار), BD (دو بار در روز), TDS (سه بار در روز), QID (چهار بار در روز), SOS (در صورت نیاز)",
        "doctor_name": "دکتر محمد عاصف عثمان",
        "doctor_title": "جراح دندانپزشک",
        "clinic_name": "کلینیک دندان عثمان مسلم",
        "clinic_subtitle": "مراقبت‌های تخصصی دهان و دندان"
    },
    "en": {
        "page_title": "📝 Prescription System",
        "back_to_list": "← Back to Patient List",
        "patient_info": "Patient Information",
        "name": "Name",
        "age": "Age",
        "gender": "Gender",
        "patient_id": "Patient ID",
        "service": "Service",
        "last_visit": "Last Visit",
        "phone": "Phone",
        "national_id": "National ID",
        "prescription_date": "Prescription Date",
        "medicines": "💊 Prescribed Medicines",
        "select_medicines": "Select Medicines (Select multiple)",
        "custom_medicines": "➕ Add Custom Medicine",
        "medicine_name": "Medicine Name",
        "dosage": "Dosage",
        "frequency": "Frequency",
        "duration": "Duration",
        "note": "Special Note",
        "save_medicine": "💾 Save Medicine",
        "delete_medicine": "🗑️ Delete Medicine",
        "medicine_exists": "⚠️ This medicine already exists",
        "medicine_added": "✅ New medicine added successfully",
        "medicine_deleted": "✅ Medicine deleted successfully",
        "manage_medicines": "➕ Manage Medicines",
        "medicine_list_title": "📋 Medicine List",
        "enter_medicine_name": "Please enter medicine name",
        "doctor_instructions": "📝 Doctor's Instructions",
        "instructions_placeholder": "Example:\nTake medicines after meals\nAvoid spicy food\nComplete the full course",
        "generate_prescription": "📄 Generate Professional Prescription",
        "clear_form": "🗑️ Clear Form",
        "select_at_least_one": "⚠️ Please select at least one medicine or add custom medicine",
        "abbreviations": "💡 Abbreviations: OD (Once daily), BD (Twice daily), TDS (Three times daily), QID (Four times daily), SOS (As needed)",
        "doctor_name": "Dr. Mohammad Asif Usman",
        "doctor_title": "Dental Surgeon",
        "clinic_name": "Osman Muslim Dental Clinic",
        "clinic_subtitle": "Specialized Oral & Dental Care"
    }
}

def t_prescription(key):
    lang = st.session_state.get("dashboard_language", "dr")
    return translations_prescription[lang].get(key, key)


# =========================================================================
# توابع مدیریت داروها (مشابه بخش خدمات)
# =========================================================================

def get_medicines():
    """دریافت لیست داروها از دیتابیس"""
    try:
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS medicines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    medicine_name TEXT UNIQUE,
                    dosage TEXT,
                    frequency TEXT,
                    duration TEXT,
                    note TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor = conn.execute("SELECT COUNT(*) FROM medicines")
            if cursor.fetchone()[0] == 0:
                default_medicines = [
                    ("Amoxicillin 500mg", "1 cap", "TDS", "5 days", "After meals"),
                    ("Metronidazole 200mg", "1 tab", "TDS", "7 days", "With food"),
                    ("Paracetamol 500mg", "1-2 tabs", "SOS", "As needed", "For pain"),
                    ("Ibuprofen 400mg", "1 tab", "TDS", "3 days", "After food"),
                    ("Azithromycin 500mg", "2 tabs first day", "OD", "3 days", "Then 1 tab daily"),
                    ("Chlorhexidine Mouthwash", "15 ml", "BD", "7 days", "Gargle 30 sec"),
                ]
                conn.executemany("INSERT INTO medicines (medicine_name, dosage, frequency, duration, note) VALUES (?, ?, ?, ?, ?)", default_medicines)
                conn.commit()
            
            medicines = conn.execute("SELECT medicine_name, dosage, frequency, duration, note FROM medicines ORDER BY medicine_name").fetchall()
            return [{"name": m[0], "dosage": m[1], "frequency": m[2], "duration": m[3], "note": m[4]} for m in medicines]
    except Exception as e:
        return []

def add_medicine(medicine_name, dosage, frequency, duration, note):
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO medicines (medicine_name, dosage, frequency, duration, note) VALUES (?, ?, ?, ?, ?)", 
                        (medicine_name, dosage, frequency, duration, note))
            conn.commit()
            return True, None
    except Exception as e:
        if "UNIQUE" in str(e):
            return False, "duplicate"
        return False, str(e)

def delete_medicine(medicine_name):
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM medicines WHERE medicine_name = ?", (medicine_name,))
            conn.commit()
            return True
    except Exception as e:
        return False


def render_patient_prescription(patient_id):
    """Prescription form integrated within patient list"""
    st.header(f"📝 Prescription System / سیستم نسخه نویسی")
    st.subheader("Patient Information Auto-filled")
    
    # اضافه کردن لوگو
    try:
        with open("logofaisal.jpg", "rb") as image_file:
            logo_bytes = image_file.read()
            logo_base64 = base64.b64encode(logo_bytes).decode()
    except FileNotFoundError:
        st.warning("⚠️ لوگو یافت نشد. از لوگوی متنی استفاده می‌شود.")
        logo_base64 = None
    
    # Fetch patient data
    with get_connection() as conn:
        patient_data = pd.read_sql_query(
            "SELECT * FROM patients WHERE id = ?", 
            conn, 
            params=(patient_id,)
        )
    
    if patient_data.empty:
        st.error("Patient not found!")
        return
    
    patient_data = patient_data.iloc[0]
    
    # اختصارات پزشکی
    st.caption("💡 **Abbreviations:** OD (Once daily), BD (Twice daily), TDS (Three times daily), QID (Four times daily), SOS (As needed)")

    # نمایش اطلاعات بیمار
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""
        **👤 Patient Information:**
        - **Name:** {patient_data['first_name']} {patient_data['last_name']}
        - **Age:** {patient_data['age']}
        - **Gender:** {patient_data['gender']}
        - **Patient ID:** {patient_data['id']}
        """)
    
    with col2:
        st.info(f"""
        **📋 Medical Info:**
        - **Service:** {patient_data['service_type']}
        - **Last Visit:** {patient_data['appointment_date']}
        - **Phone:** {patient_data['phone']}
        - **National ID:** {patient_data['national_id']}
        """)
    
    st.divider()
    
    # ===== PRESCRIPTION DETAILS =====
    st.subheader("💊 Prescription Details")
    
    # تاریخ نسخه
    col_date, col_gender = st.columns(2)
    with col_date:
        p_date = st.date_input("Prescription Date / تاریخ نسخه", value=datetime.now())
    
    with col_gender:
        gender_map = {'Male': 'Male / مرد', 'Female': 'Female / زن', 'male': 'Male / مرد', 'female': 'Female / زن'}
        rx_gender = gender_map.get(patient_data['gender'], 'Male / مرد')
    
    # Auto-filled patient info
    patient_name = f"{patient_data['first_name']} {patient_data['last_name']}"
    age = str(patient_data['age'])
    
    st.divider()
    
    # ========== بخش مدیریت داروها (مشابه بخش خدمات) ==========
    st.subheader("💊 داروهای تجویزی")
    
    # دریافت لیست داروها از دیتابیس
    medicines = get_medicines()
    medicine_names = [m["name"] for m in medicines]
    
    # ========== بخش مدیریت داروها (در یک expander) ==========
    with st.expander("➕ مدیریت داروها", expanded=False):
        st.markdown("### ➕ افزودن داروی جدید")
        
        col_add1, col_add2, col_add3, col_add4, col_add5 = st.columns([2, 1.2, 1.2, 1, 1])
        
        with col_add1:
            new_medicine_name = st.text_input("نام دارو", placeholder="مثلاً: Amoxicillin 500mg", key="new_medicine_name")
        
        with col_add2:
            new_dosage = st.text_input("مقدار مصرف", placeholder="1 cap", key="new_dosage")
        
        with col_add3:
            new_frequency = st.text_input("تناوب مصرف", placeholder="TDS", key="new_frequency")
        
        with col_add4:
            new_duration = st.text_input("مدت مصرف", placeholder="5 days", key="new_duration")
        
        with col_add5:
            new_note = st.text_input("توضیحات", placeholder="After meals", key="new_note")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            if st.button("💾 ذخیره دارو", key="save_medicine_btn", use_container_width=True, type="primary"):
                if new_medicine_name.strip():
                    success, error = add_medicine(new_medicine_name.strip(), new_dosage.strip(), new_frequency.strip(), new_duration.strip(), new_note.strip())
                    if success:
                        st.success("✅ داروی جدید با موفقیت اضافه شد")
                        st.rerun()
                    elif error == "duplicate":
                        st.error("⚠️ این دارو قبلاً وجود دارد")
                    else:
                        st.error(f"خطا: {error}")
                else:
                    st.warning("لطفاً نام دارو را وارد کنید")
        
        st.markdown("---")
        
        # لیست داروهای موجود با قابلیت حذف
        st.markdown("### 📋 لیست داروهای موجود")
        
        default_medicines = ["Amoxicillin 500mg", "Metronidazole 200mg", "Paracetamol 500mg", "Ibuprofen 400mg", "Azithromycin 500mg", "Chlorhexidine Mouthwash"]
        custom_medicines = [m for m in medicines if m["name"] not in default_medicines]
        
        if custom_medicines:
            for m in custom_medicines:
                col_d1, col_d2, col_d3, col_d4, col_d5, col_d6 = st.columns([2, 1.2, 1.2, 1, 1.5, 0.8])
                with col_d1:
                    st.write(m['name'])
                with col_d2:
                    st.write(m['dosage'])
                with col_d3:
                    st.write(m['frequency'])
                with col_d4:
                    st.write(m['duration'])
                with col_d5:
                    st.write(m['note'])
                with col_d6:
                    if st.button("🗑️", key=f"del_med_{m['name']}"):
                        if delete_medicine(m['name']):
                            st.success("✅ دارو با موفقیت حذف شد")
                            st.rerun()
        else:
            st.info("برای افزودن داروی جدید از فرم بالا استفاده کنید")
    
    # ========== انتخاب داروها (Multiselect) ==========
    selected_med_names = st.multiselect(
        "انتخاب داروها (چندین مورد را انتخاب کنید):",
        medicine_names,
        placeholder="Choose medicines from list..."
    )
    
    # دریافت جزئیات داروهای انتخاب شده
    selected_med_details = [m for m in medicines if m["name"] in selected_med_names]
    
    # نمایش داروهای انتخاب شده با جزئیات
    if selected_med_details:
        st.write("**داروهای انتخاب شده با جزئیات:**")
        for med in selected_med_details:
            with st.container():
                cols = st.columns([3, 2, 2, 2, 3])
                with cols[0]:
                    st.write(f"**{med['name']}**")
                with cols[1]:
                    st.write(f"Dose: {med['dosage']}")
                with cols[2]:
                    st.write(f"Freq: {med['frequency']}")
                with cols[3]:
                    st.write(f"Dur: {med['duration']}")
                with cols[4]:
                    st.write(f"Note: {med['note']}")
    
    # ========== داروهای سفارشی (اختیاری) ==========
    st.subheader("➕ افزودن داروی سفارشی")
    with st.expander("افزودن داروی سفارشی با جزئیات کامل"):
        st.write("**فرمت:** نام دارو | مقدار مصرف | تناوب مصرف | مدت مصرف | توضیحات")
        custom_med_input = st.text_area(
            "داروهای سفارشی را وارد کنید:",
            placeholder="مثال:\nPenicillin VK 500mg | 1 tab | TDS | 10 days | After meals\nDiazepam 5mg | 1 tab | HS | 7 days | At bedtime",
            height=100
        )
    
    # Doctor's instructions
    st.subheader("📝 Doctor's Instructions")
    instructions = st.text_area(
        "Instructions for the patient (in English & Dari):",
        placeholder="Example:\nTake medicines after meals / داروها را بعد از غذا مصرف کنید\nAvoid spicy food / از غذاهای تند پرهیز کنید\nComplete the full course / دوره درمان را کامل کنید",
        height=120
    )
    
    # Generate prescription button
    if st.button("📄 Generate Professional Prescription", type="primary", use_container_width=True):
        # جمع‌آوری همه داروها (استاندارد + سفارشی)
        all_medicines = []
        
        # اضافه کردن داروهای استاندارد انتخاب شده
        for med in selected_med_details:
            all_medicines.append(med)
        
        # اضافه کردن داروهای سفارشی
        if custom_med_input.strip():
            for line in custom_med_input.strip().split('\n'):
                if line.strip():
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 5:
                        all_medicines.append({
                            "name": parts[0],
                            "dosage": parts[1],
                            "frequency": parts[2],
                            "duration": parts[3],
                            "note": parts[4]
                        })
        
        if not all_medicines:
            st.error("⚠️ لطفاً حداقل یک دارو انتخاب کنید یا داروی سفارشی اضافه کنید.")
        else:
            # Prepare medicines HTML with professional format
            meds_html = ""
            for med in all_medicines:
                meds_html += f"""
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #eee; direction: ltr; text-align: left;">{med['name']}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center; font-size: 10px;">{med['dosage']}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center; font-size: 10px;">{med['frequency']}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: center; font-size: 10px;">{med['duration']}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: right; font-size: 10px;">{med['note']}</td>
                </tr>
                """
            
            # Doctor's contact information
            doctor_info = """
            <div style="margin-top: 40px; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #1a5276;">
                <h4 style="margin: 0 0 10px 0; color: #1a5276;">Doctor's Information:</h4>
                <p style="margin: 5px 0;"><strong>Dr. Mohammad Asif Usman</strong></p>
                <p style="margin: 5px 0;">📞 Phone: +93 78 123 4567 / +93 70 987 6543</p>
                <p style="margin: 5px 0;">🏥 Address: Street 3, karte-e-Naw, Kabul, Afghanistan</p>
                <p style="margin: 5px 0;">🕒 Clinic Hours: 9:00 AM - 5:00 PM (Sat-Thu)</p>
                <p style="margin: 5px 0;">📧 Email: dr.asif.dental@clinic.af</p>
            </div>
            """
            
            # لوگو HTML
            if logo_base64:
                logo_html = f"""
                <table width="100%" style="border-bottom: 3px double #1a5276; padding-bottom: 15px; margin-bottom: 25px;">
                    <tr>
                        <td width="25%" style="vertical-align: middle; padding-right: 20px;">
                            <img src="data:image/jpeg;base64,{logo_base64}" style="max-height: 80px; max-width: 120px;" alt="Clinic Logo">
                        </td>
                        <td width="75%" style="text-align: right; vertical-align: middle; direction: rtl;">
                """
            else:
                logo_html = """
                <table width="100%" style="border-bottom: 3px double #1a5276; padding-bottom: 15px; margin-bottom: 25px;">
                    <tr>
                        <td width="100%" style="text-align: right; vertical-align: middle; direction: rtl;">
                """
            
            # Generate prescription HTML (بدون تغییر - همان کد اصلی)
            prescription_html = f"""
            <html>
            <head>
                <style>
                    @page {{ 
                        size: A4; 
                        margin: 15mm 10mm 15mm 10mm;
                    }}
                    
                    body {{ 
                        margin: 0; 
                        padding: 0; 
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        font-size: 12px;
                        line-height: 1.4;
                        color: #333;
                    }}
                    
                    .prescription-container {{
                        max-width: 210mm;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    
                    .header {{
                        padding-bottom: 15px;
                        margin-bottom: 25px;
                    }}
                    
                    .clinic-name {{
                        font-size: 20px;
                        font-weight: bold;
                        color: #1a5276;
                        margin: 0 0 5px 0;
                        text-align: right;
                        direction: ltr;
                    }}
                    
                    .clinic-name-farsi {{
                        font-size: 18px;
                        font-weight: bold;
                        color: #2c3e50;
                        margin: 0 0 10px 0;
                        text-align: right;
                        direction: rtl;
                    }}
                    
                    .clinic-subtitle {{
                        font-size: 13px;
                        color: #666;
                        margin: 5px 0 10px 0;
                        text-align: right;
                        direction: rtl;
                        line-height: 1.6;
                    }}
                    
                    .clinic-info {{
                        font-size: 11px;
                        margin: 5px 0 0 0;
                        text-align: right;
                        direction: rtl;
                    }}
                    
                    .patient-info {{
                        background: #f5f5f5;
                        padding: 12px;
                        border-radius: 6px;
                        margin-bottom: 15px;
                        font-size: 11px;
                    }}
                    
                    .medication-table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin: 15px 0;
                        font-size: 11px;
                    }}
                    
                    .medication-table th {{
                        background: #1a5276;
                        color: white;
                        padding: 8px;
                        text-align: left;
                        font-size: 10px;
                    }}
                    
                    .medication-table td {{
                        padding: 6px;
                        border-bottom: 1px solid #ddd;
                        font-size: 10px;
                    }}
                    
                    .instructions {{
                        background: #fff8e1;
                        padding: 12px;
                        border-radius: 6px;
                        margin: 15px 0;
                        border-right: 3px solid #ffc107;
                        font-size: 11px;
                    }}
                    
                    .footer {{
                        margin-top: 30px;
                        padding-top: 15px;
                        border-top: 1px solid #ddd;
                        font-size: 11px;
                    }}
                    
                    .signature {{
                        float: right;
                        text-align: center;
                        margin-top: 20px;
                        font-size: 11px;
                    }}
                    
                    .watermark {{
                        position: fixed;
                        bottom: 50px;
                        left: 0;
                        right: 0;
                        text-align: center;
                        font-size: 40px;
                        color: rgba(0, 150, 255, 0.05);
                        transform: rotate(-45deg);
                        z-index: -1;
                    }}
                    
                    @media print {{
                        .no-print {{ display: none !important; }}
                        .prescription-container {{ padding: 0; }}
                        body {{ font-size: 11px; }}
                    }}
                </style>
            </head>
            <body>
                <div class="watermark">PRESCRIPTION</div>
                
                <div class="prescription-container">
                    <div class="header">
                        {logo_html}
                            <h1 class="clinic-name">OSMAN MUSLIM DENTAL CLINIC</h1>
                            <p class="clinic-name-farsi">کلینیک دندان عثمان مسلم</p>
                            <p class="clinic-subtitle">Specialized Oral & Dental Care | مراقبت‌های تخصصی دهان و دندان</p>
                            <p class="clinic-info">License No: MED-2024-789 | Chamber No: 405, Dental Complex</p>
                        </td>
                    </tr>
                </table>
            </div>
            
            <div class="patient-info">
                <table width="100%">
                    <tr>
                        <td width="50%"><strong>Patient Name:</strong> {patient_name}</td>
                        <td width="50%"><strong>Prescription Date:</strong> {p_date}</td>
                    </tr>
                    <tr>
                        <td><strong>Age/Sex:</strong> {age} / {rx_gender}</td>
                        <td><strong>Patient ID:</strong> {patient_id}</td>
                    </tr>
                    <tr>
                        <td><strong>National ID:</strong> {patient_data['national_id']}</td>
                        <td><strong>Phone:</strong> {patient_data['phone']}</td>
                    </tr>
                </table>
            </div>
            
            <h3 style="color: #1a5276; border-bottom: 2px solid #1a5276; padding-bottom: 5px; font-size: 14px;">PRESCRIBED MEDICATIONS</h3>
            
            <table class="medication-table">
                <thead>
                    <tr>
                        <th width="30%" style="text-align: left;">Medicine</th>
                        <th width="15%" style="text-align: center;">Dosage</th>
                        <th width="15%" style="text-align: center;">Frequency</th>
                        <th width="15%" style="text-align: center;">Duration</th>
                        <th width="25%" style="text-align: right;">Special Instructions</th>
                    </tr>
                </thead>
                <tbody>
                    {meds_html}
                </tbody>
            </table>
            
            <div class="instructions">
                <h4 style="color: #d35400; margin-top: 0; font-size: 12px;">DOCTOR'S INSTRUCTIONS:</h4>
                <p style="margin: 8px 0; font-weight: bold; font-size: 11px; direction: ltr; text-align: left;">
                    {instructions.split('/')[0].strip() if '/' in instructions else instructions}
                </p>
                <p style="margin: 8px 0; font-weight: bold; font-size: 11px; direction: rtl; text-align: right;">
                    {instructions.split('/')[1].strip() if '/' in instructions else 'داروها را طبق دستور مصرف کنید'}
                </p>
            </div>
            
            {doctor_info}
            
            <div class="footer">
                <div style="float: left; width: 60%; font-size: 10px; color: #666;">
                    <p><strong>Important Notes:</strong></p>
                    <ul style="margin: 5px 0; padding-left: 15px;">
                        <li>This prescription is valid for 30 days only</li>
                        <li>Keep medicines out of reach of children</li>
                        <li>Do not share your medicines with others</li>
                        <li>Store in cool, dry place away from sunlight</li>
                        <li>Follow up appointment recommended</li>
                    </ul>
                </div>
                
                <div class="signature">
                    <div style="height: 50px; border-bottom: 1px solid #000; width: 180px; margin-bottom: 8px;"></div>
                    <p style="margin: 5px 0;"><strong>Dr. Mohammad Asif Usman</strong></p>
                    <p style="margin: 0; font-size: 9px;">Dental Surgeon | License No: DS-7894-KBL</p>
                    <p style="margin: 0; font-size: 9px;">Date: {datetime.now().strftime('%d/%m/%Y')}</p>
                </div>
                
                <div style="clear: both;"></div>
            </div>
        </div>
        
        <div class="no-print" style="text-align: center; padding: 20px; background: #f8f9fa; margin-top: 15px; border-radius: 8px;">
            <button onclick="window.print()" style="padding: 12px 30px; background: #1a5276; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; margin: 8px;">
                🖨️ Print & Save as PDF
            </button>
            <button onclick="window.location.reload()" style="padding: 12px 30px; background: #27ae60; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; margin: 8px;">
                📝 Create New Prescription
            </button>
        </div>
        </body>
        </html>
        """
        
        components.html(prescription_html, height=1000, scrolling=True)
    
    # Clear button
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("🗑️ Clear Prescription Form", use_container_width=True):
            st.rerun()