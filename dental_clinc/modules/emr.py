
import streamlit as st
import pandas as pd
import json
import time
import streamlit.components.v1 as components
import os
import base64
import ast
from datetime import datetime
from modules.database import get_connection, init_emr_tables
import json

def render_emr_section():
    """Comprehensive Dental Electronic Health Record System - Modern Interface"""
    
    # Read logo
    try:
        with open("logofaisal.jpg", "rb") as image_file:
            logo_bytes = image_file.read()
            logo_base64 = base64.b64encode(logo_bytes).decode()
    except:
        logo_base64 = None
    
    # Blue Neon Theme for Healthcare System - Refined
    st.markdown("""
        <style>
        /* ===== VARIABLES ===== */
        :root {
            --bg-deep: #0A0F1F;
            --bg-dark: #0E1629;
            --bg-medium: #141E36;
            --bg-light: #1A2745;
            --neon-blue-1: #00C8FF;
            --neon-blue-2: #0066FF;
            --neon-blue-3: #4D9EFF;
            --neon-blue-4: #7FBAFF;
            --electric-blue: #2B7FFF;
            --cyber-blue: #0A4D9E;
            --deep-blue: #003399;
            --text-bright: #FFFFFF;
            --text-soft: #E0F0FF;
            --text-muted: #A0B8D9;
            --text-table: #E8F0FF;
            --glow-blue-1: 0 0 15px rgba(0, 200, 255, 0.3);
            --glow-blue-2: 0 0 15px rgba(0, 102, 255, 0.3);
            --glow-blue-3: 0 0 15px rgba(77, 158, 255, 0.2);
            --shadow-deep: 0 10px 25px -10px rgba(0, 0, 0, 0.5);
            --shadow-soft: 0 5px 15px -5px rgba(0, 0, 0, 0.3);
            --border-blue-1: 1px solid #00C8FF;
            --border-blue-2: 1px solid #0066FF;
        }
        
        .stApp {
            background: var(--bg-deep);
            background-image: radial-gradient(circle at 50% 50%, rgba(0, 200, 255, 0.03) 0%, transparent 50%);
        }
        
        .main > div {
            background: transparent;
        }
        
        .main-header {
            background: linear-gradient(135deg, var(--bg-dark) 0%, var(--bg-deep) 100%);
            padding: 40px 35px;
            border-radius: 30px;
            margin-bottom: 30px;
            text-align: center;
            border: 2px solid var(--neon-blue-1);
            box-shadow: var(--shadow-deep), var(--glow-blue-1);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            right: -50%;
            bottom: -50%;
            background: radial-gradient(circle, rgba(0, 200, 255, 0.05) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .main-header h1 {
            color: var(--text-bright) !important;
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 0 15px var(--neon-blue-1);
            letter-spacing: 1px;
        }
        
        .main-header p {
            color: var(--text-soft) !important;
            font-size: 18px;
            opacity: 0.9;
        }
        
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--bg-dark) 0%, var(--bg-deep) 100%);
            border-right: 2px solid var(--neon-blue-2);
        }
        
        section[data-testid="stSidebar"]::before {
            content: '';
            position: absolute;
            top: 0;
            bottom: 0;
            left: 0;
            width: 2px;
            background: linear-gradient(180deg, var(--neon-blue-1), var(--neon-blue-2), var(--neon-blue-3));
        }
        
        .patient-header-card {
            background: linear-gradient(135deg, var(--bg-medium) 0%, var(--bg-dark) 100%);
            color: var(--text-bright);
            border-radius: 25px;
            padding: 35px;
            margin-bottom: 25px;
            border: 2px solid var(--neon-blue-3);
            box-shadow: var(--shadow-soft);
        }
        
        .patient-header-card h2 {
            color: var(--text-bright) !important;
            font-size: 30px;
            font-weight: 600;
            margin-bottom: 15px;
        }
        
        .stSelectbox > div > div {
            background-color: var(--bg-medium) !important;
            border: 2px solid var(--neon-blue-3) !important;
            border-radius: 40px !important;
        }
        
        .stSelectbox > div > div > div {
            color: var(--text-bright) !important;
        }
        
        /* ===== دکمه‌های کوچک و مرتب ===== */
        .stButton > button {
            background: transparent;
            border-radius: 25px;
            font-weight: 500;
            padding: 6px 12px !important;
            transition: all 0.2s;
            font-size: 12px;
            height: 34px;
            white-space: nowrap;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
        }
        
        /* دکمه پرایمر (New Patient) */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--neon-blue-1) 0%, var(--neon-blue-2) 100%);
            color: white !important;
            border: none;
            box-shadow: 0 0 10px var(--neon-blue-1);
        }
        
        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 0 15px var(--neon-blue-1);
            transform: translateY(-1px);
        }
        
        /* دکمه ثانویه (Refresh) */
        .stButton > button[kind="secondary"] {
            background: rgba(255,255,255,0.08);
            color: var(--text-soft) !important;
            border: 1px solid var(--neon-blue-3);
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: rgba(255,255,255,0.15);
            border-color: var(--neon-blue-1);
            color: var(--neon-blue-1) !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 15px;
            background: var(--bg-dark);
            padding: 15px 20px;
            border-radius: 40px;
            border: 2px solid var(--neon-blue-2);
            margin-bottom: 30px;
            box-shadow: var(--shadow-soft);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 30px;
            padding: 12px 32px;
            border: 1px solid transparent;
            font-weight: 600;
            font-size: 14px;
            color: var(--text-muted) !important;
            transition: all 0.2s;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            border-color: var(--neon-blue-1);
            color: var(--neon-blue-1) !important;
            transform: translateY(-1px);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--neon-blue-1) 0%, var(--neon-blue-2) 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: var(--glow-blue-1) !important;
            transform: translateY(-1px);
        }
        
        .stTabs [data-baseweb="tab-panel"] {
            background: var(--bg-dark);
            border-radius: 30px;
            padding: 35px;
            border: 2px solid var(--neon-blue-2);
            box-shadow: var(--shadow-deep);
        }
        
        .section-header {
            color: var(--neon-blue-1) !important;
            border-bottom: 3px solid var(--neon-blue-2);
            padding-bottom: 15px;
            margin-bottom: 30px;
            font-weight: 600;
            font-size: 24px;
            text-shadow: 0 0 10px var(--neon-blue-1);
        }
        
        hr {
            background: linear-gradient(90deg, transparent, var(--neon-blue-1), var(--neon-blue-2), var(--neon-blue-3), transparent);
            height: 2px;
            border: none;
            margin: 50px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Main header with logo
    if logo_base64:
        header_html = f"""
        <div class="main-header">
            <div style="display: flex; align-items: center; justify-content: center; gap: 20px;">
                <div>
                    <h1 style="margin: 0; font-size: 32px;">🦷 Comprehensive Electronic Health Record System</h1>
                    <p style="margin: 5px 0; opacity: 0.9; font-size: 18px;">Osman Muslim Dental Clinic</p>
                    <p style="margin: 0; font-size: 14px; opacity: 0.8;">Professional Patient Record Management</p>
                </div>
            </div>
        </div>
        """
    else:
        header_html = """
        <div class="main-header">
            <h1 style="margin: 0; font-size: 32px;">🦷 Comprehensive Electronic Health Record (EHR) System</h1>
            <p style="margin: 5px 0; opacity: 0.9; font-size: 18px;">Osman Muslim Dental Clinic</p>
        </div>
        """
    
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Table setup button
    col_setup, col_stats, col_help = st.columns(3)
    with col_setup:
        if st.button("🔄 Initialize EHR Tables", use_container_width=True):
            init_emr_tables()
            st.success("✅ EHR tables created successfully")
            st.rerun()
    
    with col_stats:
        with get_connection() as conn:
            patient_count = pd.read_sql_query("SELECT COUNT(*) as count FROM patients", conn).iloc[0]['count']
            st.metric("Total Patients", patient_count)
    
    with col_help:
        with st.expander("ℹ️ Help Guide", expanded=False):
            st.write("""
            **EHR System User Guide:**
            1. Select a patient from the list
            2. Use tabs to access different sections
            3. Enter information carefully
            4. Review reports before printing
            """)
    
    st.divider()
    
    # ===== Patient Selection Section =====
    st.markdown('<h3 style="color: #00C8FF; font-family: sans-serif;">🔍 Select Patient</h3>', unsafe_allow_html=True)
    
    # Connect to database for patient list
    with get_connection() as conn:
        patients_df = pd.read_sql_query("SELECT id, first_name, last_name, age, gender, phone, national_id FROM patients ORDER BY last_name", conn)
    
    if patients_df.empty:
        st.warning("⚠️ No patients registered in the system. Please add a new patient first.")
        return
    
    # Create search options
    search_options = {}
    for _, row in patients_df.iterrows():
        display_text = f" {row['first_name']} {row['last_name']} |  {row['age']} years |  {row['phone']} |  #{row['id']}"
        search_options[display_text] = row['id']
    
    # ردیف دکمه‌ها در کنار selectbox
    col_search, col_new, col_refresh = st.columns([3, 1, 1])
    
    with col_search:
        selected_patient_display = st.selectbox(
            "",
            options=[""] + list(search_options.keys()),
            placeholder="👈 Type patient name or select from list...",
            label_visibility="collapsed"
        )
    
    # ========== دکمه New Patient - آبی (primary) ==========
    #with col_new:
       # st.markdown('<div style="height: 5px;"></div>', unsafe_allow_html=True)  # فاصله برای همردیفی با selectbox
       # if st.button("➕ New Patient", use_container_width=True, type="primary"):
          #  st.session_state.goto_add_patient = True
          #  st.rerun()
    
    # ========== دکمه Refresh - خاکستری (secondary) ==========
    with col_refresh:
        st.markdown('<div style="height: 5px;"></div>', unsafe_allow_html=True)  # فاصله برای همردیفی با selectbox
        if st.button("🔄 Refresh", use_container_width=True, type="secondary"):
            st.rerun()
    
    if not selected_patient_display:
        st.info("👈 Please select a patient from the list")
        
        with st.expander("📋 Complete Patient List", expanded=True):
            display_df = patients_df[['id', 'first_name', 'last_name', 'age', 'gender', 'phone']].copy()
            display_df.columns = ['ID', 'First Name', 'Last Name', 'Age', 'Gender', 'Phone']
            st.dataframe(
                display_df,
                use_container_width=True,
                height=350,
                column_config={
                    "ID": st.column_config.NumberColumn(width="small"),
                    "Age": st.column_config.NumberColumn(width="small"),
                    "Gender": st.column_config.TextColumn(width="small")
                }
            )
        return
    
    # ===== Display Selected Patient Record =====
    p_id = search_options[selected_patient_display]
    
    # Get complete patient information
    with get_connection() as conn:
        patient_data = pd.read_sql_query(f"SELECT * FROM patients WHERE id = {p_id}", conn).iloc[0]
    
    # Patient header
    st.markdown(f"""
    <div class="patient-header-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div style="flex: 2;">
                <h2 style="margin: 0; font-size: 28px;">👤 {patient_data['first_name']} {patient_data['last_name']}</h2>
                <div style="display: flex; gap: 20px; margin-top: 10px; flex-wrap: wrap;">
                    <div>
                        <span style="font-size: 14px; opacity: 0.9;">Patient ID:</span>
                        <span style="font-size: 18px; font-weight: bold;">#{patient_data['id']}</span>
                    </div>
                    <div>
                        <span style="font-size: 14px; opacity: 0.9;">Age:</span>
                        <span style="font-size: 18px; font-weight: bold;">{patient_data['age']} years</span>
                    </div>
                    <div>
                        <span style="font-size: 14px; opacity: 0.9;">Gender:</span>
                        <span style="font-size: 18px; font-weight: bold;">{' Male' if patient_data['gender'] in ['Male', 'male'] else ' Female'}</span>
                    </div>
                    <div>
                        <span style="font-size: 14px; opacity: 0.9;">Phone:</span>
                        <span style="font-size: 18px; font-weight: bold;">{patient_data['phone']}</span>
                    </div>
                </div>
            </div>
            <div style="flex: 1; text-align: right;">
                <span class="badge-success" style="font-size: 16px; padding: 8px 20px;">● Active</span>
                <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">
                    Last Visit: {patient_data.get('appointment_date', 'No history')}
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== Main Tabs =====
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 General Information", 
        "🏥 Health Questionnaire", 
        "🦷 Dental Chart", 
        "📁 Images & Documents", 
        "💰 Financial Section", 
        "📜 Reports & Print"
    ])


    # ===== Tab 1: General Information =====
    with tab1:
        # ========== Tab Header ==========
        st.markdown("""
            <div style="background: linear-gradient(135deg, #0A0F1F, #0E1629);
                        padding: 30px 25px;
                        border-radius: 25px;
                        margin-bottom: 30px;
                        border: 2px solid #00C8FF;
                        box-shadow: 0 10px 25px -10px rgba(0, 200, 255, 0.3);">
                <h1 style="color: white; text-align: center; margin: 0; font-size: 32px; font-weight: 700; text-shadow: 0 0 15px #00C8FF;">
                    📋 Patient General Information
                </h1>
                <p style="color: #7FBAFF; text-align: center; margin: 10px 0 0 0; font-size: 16px; letter-spacing: 0.5px;">
                    View and edit personal and contact information
                </p>
            </div>
        """, unsafe_allow_html=True)

        # ========== Get Patient Information ==========
        try:
            with get_connection() as conn:
                # اطلاعات پایه بیمار
                patient_data = pd.read_sql_query(f"SELECT * FROM patients WHERE id = {p_id}", conn)
                
                if patient_data.empty:
                    st.error("❌ Patient not found!")
                    st.stop()
                
                patient = patient_data.iloc[0]
                
                # ===== دریافت اطلاعات مالی =====
                # بخش 1: از جدول patients (مقادیر وارد شده در تب General)
                patient_financial = pd.read_sql_query(f"""
                    SELECT 
                        COALESCE(cost, 0) as cost_from_patients,
                        COALESCE(paid_amount, 0) as paid_from_patients,
                        COALESCE(discount, 0) as discount_from_patients
                    FROM patients 
                    WHERE id = {p_id}
                """, conn).iloc[0]
                
                # بخش 2: از جداول مالی (تب 5)
                invoices_sum = pd.read_sql_query(f"""
                    SELECT COALESCE(SUM(unit_price), 0) as total 
                    FROM patient_invoices 
                    WHERE patient_id = {p_id}
                """, conn).iloc[0, 0]
                
                payments_sum = pd.read_sql_query(f"""
                    SELECT COALESCE(SUM(amount), 0) as total 
                    FROM patient_payments 
                    WHERE patient_id = {p_id}
                """, conn).iloc[0, 0]
                
                # ===== محاسبه مجموع نهایی (دقیقاً مثل تب 5) =====
                total_invoices = float(patient_financial['cost_from_patients']) + float(invoices_sum)
                total_payments = float(patient_financial['paid_from_patients']) + float(payments_sum)
                total_discount = float(patient_financial['discount_from_patients'])
                
                # محاسبه باقی‌مانده
                remaining = total_invoices - total_payments - total_discount
                
        except Exception as e:
            st.error(f"❌ Database connection error: {e}")
            st.stop()

        # ========== Patient ID Card ==========
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #141E36, #0E1629);
                padding: 20px 25px;
                border-radius: 20px;
                margin-bottom: 25px;
                border: 2px solid #0066FF;
                box-shadow: 0 5px 15px -5px rgba(0, 102, 255, 0.3);
                position: relative;
                overflow: hidden;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <div style="background: rgba(0, 200, 255, 0.1); padding: 12px; border-radius: 50%; border: 2px solid #00C8FF;">
                            <span style="font-size: 28px; color: #00C8FF;">🆔</span>
                        </div>
                        <div>
                            <div style="color: #7FBAFF; font-size: 14px; font-weight: 600; margin-bottom: 5px; letter-spacing: 1px;">Patient ID</div>
                            <div style="color: white; font-size: 28px; font-weight: 700; font-family: 'monospace'; text-shadow: 0 0 10px #00C8FF;">#{patient['id']}</div>
                        </div>
                    </div>
                    <div>
                        <div style="
                            color: white; 
                            font-size: 14px; 
                            font-weight: 600; 
                            background: rgba(0, 200, 255, 0.1); 
                            padding: 10px 25px; 
                            border-radius: 40px; 
                            border: 2px solid #00C8FF;
                            box-shadow: 0 0 15px rgba(0, 200, 255, 0.3);
                            display: flex;
                            align-items: center;
                            gap: 10px;
                        ">
                            <span style="width: 10px; height: 10px; background: #00C8FF; border-radius: 50%; box-shadow: 0 0 10px #00C8FF;"></span>
                            Status: Active
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # ========== Two Main Columns ==========
        col1, col2 = st.columns(2)

        # ========== First Column ==========
        with col1:
            # ---- Identity Information Card ----
            st.markdown("""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 25px;
                            border-radius: 20px;
                            margin-bottom: 20px;
                            border: 2px solid #00C8FF;
                            box-shadow: 0 5px 15px -5px rgba(0, 200, 255, 0.2);
                            transition: all 0.3s ease;">
                    <div style="display: flex; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #0066FF; padding-bottom: 15px;">
                        <span style="font-size: 28px; margin-right: 10px; color: #00C8FF;">👤</span>
                        <span style="color: white; font-size: 20px; font-weight: 700; text-shadow: 0 0 10px #00C8FF;">Identity Information</span>
                    </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                    <div style="margin-bottom: 15px; display: flex; align-items: center; padding: 5px 0;">
                        <span style="color: #7FBAFF; width: 100px; font-weight: 500;">Name:</span>
                        <span style="color: white; font-weight: 600; font-size: 16px;">{patient['first_name']} {patient['last_name']}</span>
                    </div>
                    <div style="margin-bottom: 15px; display: flex; align-items: center; padding: 5px 0;">
                        <span style="color: #7FBAFF; width: 100px; font-weight: 500;">National ID:</span>
                        <span style="color: white; font-weight: 600;">{patient['national_id']}</span>
                    </div>
                    <div style="margin-bottom: 15px; display: flex; align-items: center; padding: 5px 0;">
                        <span style="color: #7FBAFF; width: 100px; font-weight: 500;">Age:</span>
                        <span style="color: white; font-weight: 600;">{patient['age']} years</span>
                    </div>
                    <div style="margin-bottom: 5px; display: flex; align-items: center; padding: 5px 0;">
                        <span style="color: #7FBAFF; width: 100px; font-weight: 500;">Gender:</span>
                        <span style="color: white; font-weight: 600;">{'Male' if patient['gender'] in ['Male', 'male', 'مرد'] else 'Female'}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # ---- Contact Information Card ----
            st.markdown("""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 25px;
                            border-radius: 20px;
                            margin-bottom: 20px;
                            border: 2px solid #0066FF;
                            box-shadow: 0 5px 15px -5px rgba(0, 102, 255, 0.2);
                            transition: all 0.3s ease;">
                    <div style="display: flex; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #00C8FF; padding-bottom: 15px;">
                        <span style="font-size: 28px; margin-right: 10px; color: #0066FF;">📞</span>
                        <span style="color: white; font-size: 20px; font-weight: 700; text-shadow: 0 0 10px #0066FF;">Contact Information</span>
                    </div>
            """, unsafe_allow_html=True)
            
            # Check column existence
            phone = patient['phone'] if pd.notna(patient['phone']) else '---'
            service = patient['service_type'] if 'service_type' in patient and pd.notna(patient['service_type']) else '---'
            appointment = patient['appointment_date'] if 'appointment_date' in patient and pd.notna(patient['appointment_date']) else '---'
            
            st.markdown(f"""
                    <div style="margin-bottom: 15px; display: flex; align-items: center; padding: 5px 0;">
                        <span style="color: #7FBAFF; width: 100px; font-weight: 500;">Phone:</span>
                        <span style="color: white; font-weight: 600; direction: ltr;">{phone}</span>
                    </div>
                    <div style="margin-bottom: 15px; display: flex; align-items: center; padding: 5px 0;">
                        <span style="color: #7FBAFF; width: 100px; font-weight: 500;">Service Type:</span>
                        <span style="color: white; font-weight: 600;">{service}</span>
                    </div>
                    <div style="margin-bottom: 5px; display: flex; align-items: center; padding: 5px 0;">
                        <span style="color: #7FBAFF; width: 100px; font-weight: 500;">Appointment Date:</span>
                        <span style="color: white; font-weight: 600;">{appointment}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # ========== Second Column ==========
        with col2:
            # ---- Next Visit Card ----
            st.markdown("""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 25px;
                            border-radius: 20px;
                            margin-bottom: 20px;
                            border: 2px solid #4D9EFF;
                            box-shadow: 0 5px 15px -5px rgba(77, 158, 255, 0.2);
                            transition: all 0.3s ease;">
                    <div style="display: flex; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #0066FF; padding-bottom: 15px;">
                        <span style="font-size: 28px; margin-right: 10px; color: #4D9EFF;">📅</span>
                        <span style="color: white; font-size: 20px; font-weight: 700; text-shadow: 0 0 10px #4D9EFF;">Next Visit</span>
                    </div>
            """, unsafe_allow_html=True)
            
            next_date = patient['next_visit_date'] if pd.notna(patient['next_visit_date']) else '---'
            next_time = patient['next_visit_time'] if pd.notna(patient['next_visit_time']) else '---'
            
            st.markdown(f"""
                    <div style="margin-bottom: 15px; display: flex; align-items: center; padding: 5px 0;">
                        <span style="color: #7FBAFF; width: 100px; font-weight: 500;">Date:</span>
                        <span style="color: white; font-weight: 600;">{next_date}</span>
                    </div>
                    <div style="margin-bottom: 5px; display: flex; align-items: center; padding: 5px 0;">
                        <span style="color: #7FBAFF; width: 100px; font-weight: 500;">Time:</span>
                        <span style="color: white; font-weight: 600;">{next_time}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # ---- Financial Summary Card (دقیقاً مثل تب 5) ----
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 25px;
                            border-radius: 20px;
                            margin-bottom: 20px;
                            border: 2px solid #7FBAFF;
                            box-shadow: 0 5px 15px -5px rgba(127, 186, 255, 0.2);
                            transition: all 0.3s ease;">
                    <div style="display: flex; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #00C8FF; padding-bottom: 15px;">
                        <span style="font-size: 28px; margin-right: 10px; color: #7FBAFF;">💰</span>
                        <span style="color: white; font-size: 20px; font-weight: 700; text-shadow: 0 0 10px #7FBAFF;">Financial Summary</span>
                    </div>
                    <div style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; padding: 5px 0;">
                        <span style="color: #7FBAFF; font-weight: 500;">Total Invoices:</span>
                        <span style="color: white; font-weight: 700; font-size: 16px;">{total_invoices:,.0f} AFN</span>
                    </div>
                    <div style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; padding: 5px 0;">
                        <span style="color: #7FBAFF; font-weight: 500;">Total Paid:</span>
                        <span style="color: #00C8FF; font-weight: 700; font-size: 16px; text-shadow: 0 0 10px #00C8FF;">{total_payments:,.0f} AFN</span>
                    </div>
                    <div style="margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; padding: 5px 0;">
                        <span style="color: #7FBAFF; font-weight: 500;">Discount:</span>
                        <span style="color: #4D9EFF; font-weight: 700; font-size: 16px;">{total_discount:,.0f} AFN</span>
                    </div>
                    <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid #0066FF;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <span style="color: #7FBAFF; font-size: 18px; font-weight: 600;">Balance:</span>
                            <span style="color: {'#00C8FF' if remaining <= 0 else '#FF6B6B'}; font-size: 22px; font-weight: 700; text-shadow: 0 0 15px {'#00C8FF' if remaining <= 0 else '#FF6B6B'};">
                                {remaining:,.0f} AFN
                            </span>
                        </div>
                        <div style="text-align: center;">
                            <span style="
                                color: white; 
                                background: {'#00C8FF' if remaining <= 0 else '#FF6B6B'}; 
                                padding: 8px 25px; 
                                border-radius: 40px; 
                                font-size: 14px;
                                font-weight: 600;
                                display: inline-block;
                                box-shadow: 0 0 15px {'#00C8FF' if remaining <= 0 else '#FF6B6B'};
                            ">
                                {'✓ Fully Paid' if remaining <= 0 else '⚠️ Outstanding Balance'}
                            </span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # نمایش تفکیک منابع (برای شفافیت کامل)
            with st.expander("📊 View Financial Breakdown", expanded=False):
                st.markdown(f"""
                    <div style="padding: 10px; background: rgba(0,0,0,0.2); border-radius: 10px;">
                        <p style="color: #7FBAFF; margin: 5px 0;"><strong>💰 From General Section (patients table):</strong></p>
                        <p style="color: white; margin: 5px 0 5px 15px;">📋 Cost/Invoices: {float(patient_financial['cost_from_patients']):,.0f} AFN</p>
                        <p style="color: white; margin: 5px 0 5px 15px;">💵 Paid Amount: {float(patient_financial['paid_from_patients']):,.0f} AFN</p>
                        <p style="color: white; margin: 5px 0 5px 15px;">🎯 Discount: {float(patient_financial['discount_from_patients']):,.0f} AFN</p>
                        
                        <p style="color: #7FBAFF; margin: 15px 0 5px 0;"><strong>➕ From Financial Section (Tab 5):</strong></p>
                        <p style="color: white; margin: 5px 0 5px 15px;">📋 Additional Invoices: {float(invoices_sum):,.0f} AFN</p>
                        <p style="color: white; margin: 5px 0 5px 15px;">💳 Additional Payments: {float(payments_sum):,.0f} AFN</p>
                        
                        <hr style="border-color: #00C8FF; opacity: 0.3; margin: 15px 0;">
                        
                        <p style="color: #00C8FF; margin: 5px 0;"><strong>📊 TOTAL SUMMARY:</strong></p>
                        <p style="color: white; margin: 5px 0 5px 15px;">📋 Total Invoices: {total_invoices:,.0f} AFN</p>
                        <p style="color: white; margin: 5px 0 5px 15px;">💵 Total Paid: {total_payments:,.0f} AFN</p>
                        <p style="color: white; margin: 5px 0 5px 15px;">💰 Final Balance: {remaining:,.0f} AFN</p>
                    </div>
                """, unsafe_allow_html=True)

        # ========== Divider ==========
        st.markdown("""
            <hr style="height: 3px; 
                    background: linear-gradient(90deg, #00C8FF, #0066FF, #4D9EFF, #7FBAFF, #00C8FF); 
                    border: none; 
                    margin: 40px 0;
                    border-radius: 3px;
                    box-shadow: 0 0 20px rgba(0, 200, 255, 0.3);">
        """, unsafe_allow_html=True)

        # ========== Edit Section ==========
        st.markdown("""
            <div style="background: linear-gradient(135deg, #0E1629, #0A0F1F);
                        padding: 20px 25px;
                        border-radius: 20px;
                        margin-bottom: 25px;
                        border: 2px solid #00C8FF;
                        box-shadow: 0 5px 15px -5px rgba(0, 200, 255, 0.2);">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 28px; margin-right: 15px; color: #00C8FF;">✏️</span>
                    <span style="color: white; font-size: 22px; font-weight: 700; text-shadow: 0 0 10px #00C8FF;">Edit Patient Information</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Edit form
        with st.form("edit_patient_form"):
            col_edit1, col_edit2 = st.columns(2)
            
            with col_edit1:
                st.markdown("""
                    <div style="color: #7FBAFF; font-size: 16px; font-weight: 600; margin-bottom: 15px; border-left: 4px solid #00C8FF; padding-left: 10px;">
                        📱 Contact Information
                    </div>
                """, unsafe_allow_html=True)
                
                edit_phone = st.text_input(
                    "Phone Number",
                    value=patient['phone'] if pd.notna(patient['phone']) else '',
                    placeholder="e.g., +93 700 000 000"
                )
                
                edit_address = st.text_area(
                    "Address",
                    value=patient['address'] if 'address' in patient and pd.notna(patient['address']) else '',
                    placeholder="Complete postal address",
                    height=100
                )
            
            with col_edit2:
                st.markdown("""
                    <div style="color: #7FBAFF; font-size: 16px; font-weight: 600; margin-bottom: 15px; border-left: 4px solid #0066FF; padding-left: 10px;">
                        📅 Visit Schedule & Discount
                    </div>
                """, unsafe_allow_html=True)
                
                edit_next_date = st.date_input(
                    "Next Visit Date",
                    value=datetime.strptime(patient['next_visit_date'], '%Y-%m-%d') if pd.notna(patient['next_visit_date']) else datetime.now(),
                    format="YYYY-MM-DD"
                )
                
                edit_next_time = st.time_input(
                    "Next Visit Time",
                    value=datetime.strptime(patient['next_visit_time'], '%H:%M').time() if pd.notna(patient['next_visit_time']) else datetime.strptime("09:00", "%H:%M").time()
                )
                
                # فیلد تخفیف
                edit_discount = st.number_input(
                    "Discount Amount (AFN)",
                    min_value=0,
                    step=100,
                    value=int(patient_financial['discount_from_patients']) if patient_financial['discount_from_patients'] else 0
                )
            
            col_submit, col_cancel = st.columns(2)
            
            with col_submit:
                submitted = st.form_submit_button(
                    "💾 Save Changes",
                    use_container_width=True,
                    type="primary"
                )
            
            with col_cancel:
                cancelled = st.form_submit_button(
                    "❌ Cancel",
                    use_container_width=True,
                    type="secondary"
                )
            
            if submitted:
                try:
                    with get_connection() as conn:
                        # به‌روزرسانی اطلاعات
                        update_fields = []
                        values = []
                        
                        update_fields.append("phone = ?")
                        values.append(edit_phone)
                        
                        update_fields.append("next_visit_date = ?")
                        values.append(edit_next_date.strftime('%Y-%m-%d'))
                        
                        update_fields.append("next_visit_time = ?")
                        values.append(edit_next_time.strftime('%H:%M'))
                        
                        # به‌روزرسانی تخفیف
                        update_fields.append("discount = ?")
                        values.append(edit_discount)
                        
                        if 'address' in patient.index:
                            update_fields.append("address = ?")
                            values.append(edit_address)
                        
                        values.append(p_id)
                        
                        query = f"""
                            UPDATE patients 
                            SET {', '.join(update_fields)}
                            WHERE id = ?
                        """
                        
                        conn.execute(query, values)
                        conn.commit()
                    
                    st.success("✅ Patient information updated successfully!")
                    st.balloons()
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error saving information: {e}")
            
            if cancelled:
                st.rerun()

        # ========== Action Buttons ==========
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_op1, col_op2, col_op3 = st.columns(3)
        
        with col_op1:
            if st.button("🔄 Refresh Page", use_container_width=True):
                st.rerun()
        
        with col_op2:
            if st.button("📊 Full Report", use_container_width=True):
                st.success("Please go to 'Reports & Print' tab for complete report")
        
        with col_op3:
            if st.button("🏥 New Visit", use_container_width=True):
                st.info("Please go to 'Health Questionnaire' tab for new visit")

        # ========== Success Message ==========
        st.markdown(f"""
            <div style="background: rgba(0, 200, 255, 0.05); 
                        border-left: 4px solid #00C8FF; 
                        padding: 15px 20px; 
                        border-radius: 12px; 
                        margin-top: 25px;
                        border: 1px solid rgba(0, 200, 255, 0.2);">
                <p style="color: #00C8FF; margin: 0; font-size: 14px; font-weight: 500; display: flex; align-items: center; gap: 10px;">
                    <span style="width: 8px; height: 8px; background: #00C8FF; border-radius: 50%; box-shadow: 0 0 10px #00C8FF;"></span>
                    ✅ Patient information is up to date - Last updated: {datetime.now().strftime('%Y/%m/%d %H:%M')}
                </p>
            </div>
        """, unsafe_allow_html=True)

  
  # ===== Tab 2: Health Questionnaire =====
    with tab2:
        # ========== Tab Header ==========
        st.markdown("""
            <div style="background: linear-gradient(135deg, #0A0F1F, #0E1629);
                        padding: 30px 25px;
                        border-radius: 25px;
                        margin-bottom: 30px;
                        border: 2px solid #00C8FF;
                        box-shadow: 0 10px 25px -10px rgba(0, 200, 255, 0.3);">
                <h1 style="color: white; text-align: center; margin: 0; font-size: 32px; font-weight: 700; text-shadow: 0 0 15px #00C8FF;">
                    🏥 Health Questionnaire
                </h1>
                <p style="color: #7FBAFF; text-align: center; margin: 10px 0 0 0; font-size: 16px; letter-spacing: 0.5px;">
                    Record medical history, diseases and patient allergies
                </p>
            </div>
        """, unsafe_allow_html=True)

        # ========== Check and Create Table ==========
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS emr_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER NOT NULL,
                        medical_history TEXT,
                        allergies TEXT,
                        current_medications TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
                    )
                """)
                conn.commit()
        except Exception as e:
            st.error(f"Error creating table: {e}")

        # ========== Load Existing Information ==========
        def load_health_data(patient_id):
            try:
                with get_connection() as conn:
                    health_record = pd.read_sql_query(f"""
                        SELECT * FROM emr_records 
                        WHERE patient_id = {patient_id} 
                        ORDER BY created_at DESC LIMIT 1
                    """, conn)
                    
                    if not health_record.empty:
                        record = health_record.iloc[0]
                        has_record = True
                        
                        import ast
                        try:
                            medical_history = ast.literal_eval(record['medical_history']) if pd.notna(record['medical_history']) else {}
                        except:
                            medical_history = {}
                        
                        allergies = record['allergies'] if pd.notna(record['allergies']) else ''
                        medications = record['current_medications'] if pd.notna(record['current_medications']) else ''
                        last_update = record['created_at'] if pd.notna(record['created_at']) else ''
                    else:
                        has_record = False
                        medical_history = {}
                        allergies = ''
                        medications = ''
                        last_update = ''
                        
                    return has_record, medical_history, allergies, medications, last_update
            except Exception as e:
                return False, {}, '', '', ''

        # Initial load
        has_record, medical_history, allergies, medications, last_update = load_health_data(p_id)

        # ========== Patient Information Card ==========
        status_text = '✓ Registered' if has_record else '⚠️ Not Registered'
        status_color = '#00C8FF' if has_record else '#FF6B6B'
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                        padding: 20px 25px;
                        border-radius: 20px;
                        margin-bottom: 25px;
                        border: 2px solid {status_color};
                        box-shadow: 0 5px 15px -5px {status_color}40;
                        position: relative;
                        overflow: hidden;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <div style="background: {status_color}10; padding: 10px; border-radius: 50%; border: 2px solid {status_color};">
                            <span style="font-size: 24px; color: {status_color};">🆔</span>
                        </div>
                        <div>
                            <span style="color: {status_color}; font-size: 16px; font-weight: 600; letter-spacing: 1px;">Patient ID</span>
                            <div style="color: white; font-size: 28px; font-weight: 700; text-shadow: 0 0 10px {status_color};">#{p_id}</div>
                        </div>
                    </div>
                    <div>
                        <span style="
                            color: white; 
                            font-size: 16px; 
                            font-weight: 600; 
                            background: {status_color}; 
                            padding: 10px 25px; 
                            border-radius: 40px; 
                            box-shadow: 0 0 15px {status_color};
                            display: inline-block;
                        ">
                            {status_text}
                        </span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # ========== Allergy Warning Display ==========
        if allergies:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FF6B6B20, #FF444420);
                            padding: 20px 25px;
                            border-radius: 20px;
                            margin-bottom: 25px;
                            border: 2px solid #FF6B6B;
                            box-shadow: 0 5px 15px -5px #FF6B6B;">
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <div style="background: #FF6B6B20; padding: 12px; border-radius: 50%; border: 2px solid #FF6B6B;">
                            <span style="font-size: 28px; color: #FF6B6B;">⚠️</span>
                        </div>
                        <div>
                            <span style="color: #FF6B6B; font-size: 20px; font-weight: 700; text-shadow: 0 0 10px #FF6B6B;">Allergy Warning!</span>
                            <p style="color: white; margin: 8px 0 0 0; font-size: 15px;">{allergies}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # ========== Form for Recording Information ==========
        with st.form("health_form"):
            # ----- Heart Diseases -----
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 15px 20px;
                            border-radius: 15px;
                            margin-bottom: 25px;
                            border-right: 6px solid #FF6B6B;
                            border: 2px solid #FF6B6B;
                            box-shadow: 0 5px 15px -5px #FF6B6B;">
                    <span style="color: #FF6B6B; font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 10px;">
                        <span>🫀</span> Heart Diseases
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                heart_disease = st.checkbox("Heart Disease", value=medical_history.get('heart_disease', False))
                hypertension = st.checkbox("Hypertension", value=medical_history.get('hypertension', False))
            with col2:
                heart_surgery = st.checkbox("Heart Surgery History", value=medical_history.get('heart_surgery', False))
                arrhythmia = st.checkbox("Arrhythmia", value=medical_history.get('arrhythmia', False))
            with col3:
                stroke = st.checkbox("Stroke", value=medical_history.get('stroke', False))
                cholesterol = st.checkbox("High Cholesterol", value=medical_history.get('cholesterol', False))

            # ----- Metabolic Diseases -----
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 15px 20px;
                            border-radius: 15px;
                            margin: 30px 0 25px 0;
                            border-right: 6px solid #00C8FF;
                            border: 2px solid #00C8FF;
                            box-shadow: 0 5px 15px -5px #00C8FF;">
                    <span style="color: #00C8FF; font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 10px;">
                        <span>🩸</span> Metabolic Diseases
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                diabetes = st.checkbox("Diabetes", value=medical_history.get('diabetes', False))
                thyroid = st.checkbox("Thyroid Problems", value=medical_history.get('thyroid', False))
            with col2:
                kidney = st.checkbox("Kidney Disease", value=medical_history.get('kidney', False))
                liver = st.checkbox("Liver Disease", value=medical_history.get('liver', False))

            # ----- Respiratory Diseases -----
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 15px 20px;
                            border-radius: 15px;
                            margin: 30px 0 25px 0;
                            border-right: 6px solid #4D9EFF;
                            border: 2px solid #4D9EFF;
                            box-shadow: 0 5px 15px -5px #4D9EFF;">
                    <span style="color: #4D9EFF; font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 10px;">
                        <span>🌬️</span> Respiratory Diseases
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                asthma = st.checkbox("Asthma", value=medical_history.get('asthma', False))
                copd = st.checkbox("COPD", value=medical_history.get('copd', False))
            with col2:
                tb = st.checkbox("Tuberculosis History", value=medical_history.get('tb', False))
                sleep_apnea = st.checkbox("Sleep Apnea", value=medical_history.get('sleep_apnea', False))

            # ----- Other Diseases -----
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 15px 20px;
                            border-radius: 15px;
                            margin: 30px 0 25px 0;
                            border-right: 6px solid #7FBAFF;
                            border: 2px solid #7FBAFF;
                            box-shadow: 0 5px 15px -5px #7FBAFF;">
                    <span style="color: #7FBAFF; font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 10px;">
                        <span>🦴</span> Other Diseases
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                hepatitis = st.checkbox("Hepatitis", value=medical_history.get('hepatitis', False))
                cancer = st.checkbox("Cancer History", value=medical_history.get('cancer', False))
            with col2:
                autoimmune = st.checkbox("Autoimmune Disease", value=medical_history.get('autoimmune', False))
                epilepsy = st.checkbox("Epilepsy", value=medical_history.get('epilepsy', False))

            # ----- Personal Habits -----
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 15px 20px;
                            border-radius: 15px;
                            margin: 30px 0 25px 0;
                            border-right: 6px solid #0066FF;
                            border: 2px solid #0066FF;
                            box-shadow: 0 5px 15px -5px #0066FF;">
                    <span style="color: #0066FF; font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 10px;">
                        <span>🚭</span> Personal Habits
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                smoking_options = ["None", "Occasional", "Less than 10/day", "More than 10/day"]
                smoking_index = smoking_options.index(medical_history.get('smoking', "None")) if medical_history.get('smoking') in smoking_options else 0
                smoking = st.selectbox("Smoking", smoking_options, index=smoking_index)
                
                alcohol_options = ["None", "Occasional", "Regular"]
                alcohol_index = alcohol_options.index(medical_history.get('alcohol', "None")) if medical_history.get('alcohol') in alcohol_options else 0
                alcohol = st.selectbox("Alcohol", alcohol_options, index=alcohol_index)
            
            with col2:
                drug_use = st.checkbox("Drug Use", value=medical_history.get('drug_use', False))
                pregnancy = st.checkbox("Pregnancy (for women)", value=medical_history.get('pregnancy', False))

            # ----- Allergies and Medications -----
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 15px 20px;
                            border-radius: 15px;
                            margin: 30px 0 25px 0;
                            border-right: 6px solid #FF6B6B;
                            border: 2px solid #FF6B6B;
                            box-shadow: 0 5px 15px -5px #FF6B6B;">
                    <span style="color: #FF6B6B; font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 10px;">
                        <span>⚠️</span> Allergies & Medications
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            allergies_input = st.text_area(
                "Drug and Food Allergies",
                value=allergies,
                placeholder="e.g., Penicillin, Amoxicillin, Peanuts, Latex",
                height=80
            )
            
            medications_input = st.text_area(
                "Current Medications",
                value=medications,
                placeholder="e.g., Metoprolol 50mg once daily, Aspirin 80mg once daily",
                height=80
            )

            st.markdown("<br>", unsafe_allow_html=True)
            
            # ----- Buttons -----
            col_submit, col_clear = st.columns(2)
            
            with col_submit:
                submitted = st.form_submit_button("✅ Save Health Questionnaire", use_container_width=True, type="primary")
            
            with col_clear:
                clear = st.form_submit_button("🗑️ Clear Form", use_container_width=True, type="secondary")
            
            if submitted:
                # Collect data
                health_dict = {
                    'heart_disease': heart_disease,
                    'hypertension': hypertension,
                    'heart_surgery': heart_surgery,
                    'arrhythmia': arrhythmia,
                    'stroke': stroke,
                    'cholesterol': cholesterol,
                    'diabetes': diabetes,
                    'thyroid': thyroid,
                    'kidney': kidney,
                    'liver': liver,
                    'asthma': asthma,
                    'copd': copd,
                    'tb': tb,
                    'sleep_apnea': sleep_apnea,
                    'hepatitis': hepatitis,
                    'cancer': cancer,
                    'autoimmune': autoimmune,
                    'epilepsy': epilepsy,
                    'smoking': smoking,
                    'alcohol': alcohol,
                    'drug_use': drug_use,
                    'pregnancy': pregnancy
                }
                
                try:
                    with get_connection() as conn:
                        # Check if record exists
                        existing = pd.read_sql_query(f"SELECT id FROM emr_records WHERE patient_id = {p_id}", conn)
                        
                        if not existing.empty:
                            conn.execute("""
                                UPDATE emr_records 
                                SET medical_history = ?,
                                    allergies = ?,
                                    current_medications = ?,
                                    created_at = CURRENT_TIMESTAMP
                                WHERE patient_id = ?
                            """, (str(health_dict), allergies_input, medications_input, p_id))
                        else:
                            conn.execute("""
                                INSERT INTO emr_records 
                                (patient_id, medical_history, allergies, current_medications)
                                VALUES (?, ?, ?, ?)
                            """, (p_id, str(health_dict), allergies_input, medications_input))
                        
                        conn.commit()
                    
                    st.success("✅ Health questionnaire saved successfully!")
                    st.balloons()
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error saving information: {e}")
            
            if clear:
                st.rerun()

        # ========== Display Last Update ==========
        if has_record:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #00C8FF10, #0066FF10);
                            padding: 15px 25px;
                            border-radius: 15px;
                            margin-top: 30px;
                            border: 2px solid #00C8FF;
                            box-shadow: 0 5px 15px -5px #00C8FF;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #00C8FF; font-size: 16px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                            <span>📋</span> Last Updated
                        </span>
                        <span style="color: white; font-weight: 500;">{last_update[:16] if last_update else '---'}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)


    
     















     


    # =====================================================
# TAB 3: DENTAL CHART + DARI MANAGEMENT + DELETE + A5 BILL PRINT
# Required imports at top of emr.py:
# import streamlit as st
# import pandas as pd
# import streamlit.components.v1 as components
# =====================================================

    with tab3:
        # =====================================================
        # CONFIG
        # =====================================================
        UPPER_TEETH = list(range(1, 17))
        LOWER_TEETH = list(range(32, 16, -1))

        PRIMARY_UPPER_TEETH = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        PRIMARY_LOWER_TEETH = ["T", "S", "R", "Q", "P", "O", "N", "M", "L", "K"]

        ALL_PERMANENT_TEETH = [str(i) for i in range(1, 33)]
        ALL_PRIMARY_TEETH = [
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
            "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"
        ]

        TOOTH_STATUS_OPTIONS = [
            "سالم",
            "خرابی دندان",
            "دندان گم‌شده",
            "عصب‌کشی",
            "روکش",
            "پرکاری",
            "ایمپلنت",
            "ضرورت کشیدن",
            "در جریان تداوی",
        ]

        STATUS_COLOR_MAP = {
            "سالم": "#52B45A",
            "خرابی دندان": "#E74C3C",
            "دندان گم‌شده": "#95A5A6",
            "عصب‌کشی": "#F1C40F",
            "روکش": "#8E44AD",
            "پرکاری": "#3498DB",
            "ایمپلنت": "#16A085",
            "ضرورت کشیدن": "#C0392B",
            "در جریان تداوی": "#E67E22",
        }

        STANDARD_DENTAL_PROBLEMS = [
            "سالم",
            "کرم‌خوردگی / خرابی",
            "سوراخ دندان",
            "درد دندان",
            "حساسیت",
            "شکستگی / ترک",
            "دندان گم‌شده",
            "دندان نهفته",
            "عقب‌نشینی بیره",
            "مشکل بیره",
            "آبسه / عفونت",
            "التهاب عصب دندان",
            "ضرورت عصب‌کشی",
            "مشکل پرکاری قبلی",
            "مشکل روکش",
            "ضرورت ایمپلنت",
            "ضرورت کشیدن دندان",
            "لقی دندان",
            "ساییدگی دندان",
            "تغییر رنگ دندان",
        ]

        STANDARD_TREATMENT_PLANS = [
            "فقط معاینه و پیگیری",
            "فلوراید تراپی",
            "پرکاری دندان",
            "ترمیم کامپوزیت",
            "جرم‌گیری و پاک‌کاری",
            "پاک‌کاری عمیق بیره",
            "عصب‌کشی",
            "پست و کور",
            "گذاشتن روکش",
            "بریج دندان",
            "ایمپلنت",
            "کشیدن دندان",
            "کشیدن جراحی",
            "تخلیه آبسه",
            "تداوی با آنتی‌بیوتیک",
            "کنترول درد",
            "ترمیم موقت",
            "ارجاع به متخصص",
            "قرار ملاقات بعدی",
        ]

        PROBLEM_SEVERITY_OPTIONS = ["خفیف", "متوسط", "شدید", "عاجل"]
        TREATMENT_PRIORITY_OPTIONS = ["عادی", "به‌زودی", "فوری", "عاجل"]
        TREATMENT_STATUS_OPTIONS = ["پلان‌شده", "در جریان", "تکمیل‌شده", "متوقف", "لغو‌شده"]
        PAYMENT_METHOD_OPTIONS = ["نقدی", "کارت", "حواله بانکی", "بیمه", "پرداخت آنلاین", "ترکیبی"]
        PAYMENT_STATUS_OPTIONS = ["خودکار", "پرداخت‌نشده", "قسمتی پرداخت‌شده", "پرداخت‌شده", "برگشت داده‌شده", "لغو‌شده"]

        # =====================================================
        # HELPERS
        # =====================================================
        def get_tooth_type_from_code(tooth_code):
            tooth_code = str(tooth_code).strip().upper()
            return "دایمی" if tooth_code.isdigit() else "شیری"


        def safe_status(value):
            if value in TOOTH_STATUS_OPTIONS:
                return value
            return "سالم"


        def safe_option(value, options, default_value):
            if value in options:
                return value
            return default_value


        def get_existing_multiselect_values(text_value, options):
            if not text_value:
                return []

            items = [item.strip() for item in str(text_value).split(",") if item.strip()]
            return [item for item in items if item in options]


        def safe_html_text(value):
            value = "" if value is None else str(value)
            return (
                value.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#039;")
            )

        # =====================================================
        # DATABASE
        # =====================================================
        def ensure_tooth_management_tables():
            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS patient_dental_chart_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER NOT NULL,
                        tooth_code TEXT NOT NULL,
                        tooth_type TEXT NOT NULL DEFAULT 'دایمی',
                        status TEXT NOT NULL DEFAULT 'سالم',
                        notes TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(patient_id, tooth_code)
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS patient_tooth_details (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER NOT NULL,
                        tooth_code TEXT NOT NULL,
                        tooth_type TEXT NOT NULL,
                        dental_problems TEXT,
                        problem_severity TEXT DEFAULT 'خفیف',
                        diagnosis_notes TEXT,
                        proposed_treatment TEXT,
                        treatment_priority TEXT DEFAULT 'عادی',
                        treatment_status TEXT DEFAULT 'پلان‌شده',
                        appointment_date TEXT,
                        clinical_notes TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(patient_id, tooth_code)
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS patient_tooth_invoices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER NOT NULL,
                        tooth_code TEXT NOT NULL,
                        tooth_type TEXT NOT NULL,
                        invoice_title TEXT DEFAULT 'بل تداوی دندان',
                        treatment_cost REAL DEFAULT 0,
                        material_cost REAL DEFAULT 0,
                        lab_cost REAL DEFAULT 0,
                        discount REAL DEFAULT 0,
                        tax REAL DEFAULT 0,
                        total_amount REAL DEFAULT 0,
                        paid_amount REAL DEFAULT 0,
                        balance REAL DEFAULT 0,
                        payment_method TEXT DEFAULT 'نقدی',
                        payment_status TEXT DEFAULT 'پرداخت‌نشده',
                        payment_notes TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(patient_id, tooth_code)
                    )
                """)

                conn.commit()


        def load_all_chart_records(patient_id):
            with get_connection() as conn:
                df = pd.read_sql_query("""
                    SELECT tooth_code, tooth_type, status, COALESCE(notes, '') AS notes, updated_at
                    FROM patient_dental_chart_items
                    WHERE patient_id = ?
                """, conn, params=(int(patient_id),))

            records = {}

            if not df.empty:
                for _, row in df.iterrows():
                    code = str(row["tooth_code"])
                    records[code] = {
                        "tooth_code": code,
                        "tooth_type": row["tooth_type"],
                        "status": safe_status(row["status"]),
                        "notes": row["notes"],
                        "updated_at": row["updated_at"],
                    }

            return records


        def load_chart_record(patient_id, tooth_code):
            with get_connection() as conn:
                df = pd.read_sql_query("""
                    SELECT *
                    FROM patient_dental_chart_items
                    WHERE patient_id = ? AND tooth_code = ?
                    LIMIT 1
                """, conn, params=(int(patient_id), str(tooth_code)))

            if df.empty:
                return {}

            return df.iloc[0].to_dict()


        def load_tooth_detail_record(patient_id, tooth_code):
            with get_connection() as conn:
                df = pd.read_sql_query("""
                    SELECT *
                    FROM patient_tooth_details
                    WHERE patient_id = ? AND tooth_code = ?
                    LIMIT 1
                """, conn, params=(int(patient_id), str(tooth_code)))

            if df.empty:
                return {}

            return df.iloc[0].to_dict()


        def load_tooth_invoice_record(patient_id, tooth_code):
            with get_connection() as conn:
                df = pd.read_sql_query("""
                    SELECT *
                    FROM patient_tooth_invoices
                    WHERE patient_id = ? AND tooth_code = ?
                    LIMIT 1
                """, conn, params=(int(patient_id), str(tooth_code)))

            if df.empty:
                return {}

            return df.iloc[0].to_dict()


        def save_chart_record(patient_id, tooth_code, tooth_status, notes):
            tooth_type = get_tooth_type_from_code(tooth_code)

            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO patient_dental_chart_items (
                        patient_id, tooth_code, tooth_type, status, notes, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(patient_id, tooth_code)
                    DO UPDATE SET
                        tooth_type = excluded.tooth_type,
                        status = excluded.status,
                        notes = excluded.notes,
                        updated_at = CURRENT_TIMESTAMP
                """, (
                    int(patient_id),
                    str(tooth_code),
                    tooth_type,
                    str(tooth_status),
                    str(notes),
                ))

                conn.commit()


        def save_tooth_detail_record(
            patient_id,
            tooth_code,
            dental_problems,
            problem_severity,
            diagnosis_notes,
            proposed_treatment,
            treatment_priority,
            treatment_status,
            appointment_date,
            clinical_notes,
        ):
            tooth_type = get_tooth_type_from_code(tooth_code)

            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO patient_tooth_details (
                        patient_id,
                        tooth_code,
                        tooth_type,
                        dental_problems,
                        problem_severity,
                        diagnosis_notes,
                        proposed_treatment,
                        treatment_priority,
                        treatment_status,
                        appointment_date,
                        clinical_notes,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(patient_id, tooth_code)
                    DO UPDATE SET
                        tooth_type = excluded.tooth_type,
                        dental_problems = excluded.dental_problems,
                        problem_severity = excluded.problem_severity,
                        diagnosis_notes = excluded.diagnosis_notes,
                        proposed_treatment = excluded.proposed_treatment,
                        treatment_priority = excluded.treatment_priority,
                        treatment_status = excluded.treatment_status,
                        appointment_date = excluded.appointment_date,
                        clinical_notes = excluded.clinical_notes,
                        updated_at = CURRENT_TIMESTAMP
                """, (
                    int(patient_id),
                    str(tooth_code),
                    tooth_type,
                    str(dental_problems),
                    str(problem_severity),
                    str(diagnosis_notes),
                    str(proposed_treatment),
                    str(treatment_priority),
                    str(treatment_status),
                    str(appointment_date) if appointment_date else "",
                    str(clinical_notes),
                ))

                conn.commit()


        def save_tooth_invoice_record(
            patient_id,
            tooth_code,
            invoice_title,
            treatment_cost,
            material_cost,
            lab_cost,
            discount,
            tax,
            paid_amount,
            payment_method,
            payment_status,
            payment_notes,
        ):
            tooth_type = get_tooth_type_from_code(tooth_code)

            treatment_cost = float(treatment_cost or 0)
            material_cost = float(material_cost or 0)
            lab_cost = float(lab_cost or 0)
            discount = float(discount or 0)
            tax = float(tax or 0)
            paid_amount = float(paid_amount or 0)

            subtotal = treatment_cost + material_cost + lab_cost
            total_amount = max(subtotal - discount + tax, 0)
            balance = max(total_amount - paid_amount, 0)

            if payment_status == "خودکار":
                if paid_amount <= 0:
                    final_payment_status = "پرداخت‌نشده"
                elif paid_amount < total_amount:
                    final_payment_status = "قسمتی پرداخت‌شده"
                else:
                    final_payment_status = "پرداخت‌شده"
            else:
                final_payment_status = payment_status

            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO patient_tooth_invoices (
                        patient_id,
                        tooth_code,
                        tooth_type,
                        invoice_title,
                        treatment_cost,
                        material_cost,
                        lab_cost,
                        discount,
                        tax,
                        total_amount,
                        paid_amount,
                        balance,
                        payment_method,
                        payment_status,
                        payment_notes,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(patient_id, tooth_code)
                    DO UPDATE SET
                        tooth_type = excluded.tooth_type,
                        invoice_title = excluded.invoice_title,
                        treatment_cost = excluded.treatment_cost,
                        material_cost = excluded.material_cost,
                        lab_cost = excluded.lab_cost,
                        discount = excluded.discount,
                        tax = excluded.tax,
                        total_amount = excluded.total_amount,
                        paid_amount = excluded.paid_amount,
                        balance = excluded.balance,
                        payment_method = excluded.payment_method,
                        payment_status = excluded.payment_status,
                        payment_notes = excluded.payment_notes,
                        updated_at = CURRENT_TIMESTAMP
                """, (
                    int(patient_id),
                    str(tooth_code),
                    tooth_type,
                    str(invoice_title),
                    treatment_cost,
                    material_cost,
                    lab_cost,
                    discount,
                    tax,
                    total_amount,
                    paid_amount,
                    balance,
                    str(payment_method),
                    str(final_payment_status),
                    str(payment_notes),
                ))

                conn.commit()

            return total_amount, balance, final_payment_status


        def delete_single_tooth_record(patient_id, tooth_code):
            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    DELETE FROM patient_tooth_invoices
                    WHERE patient_id = ? AND tooth_code = ?
                """, (int(patient_id), str(tooth_code)))

                cursor.execute("""
                    DELETE FROM patient_tooth_details
                    WHERE patient_id = ? AND tooth_code = ?
                """, (int(patient_id), str(tooth_code)))

                cursor.execute("""
                    DELETE FROM patient_dental_chart_items
                    WHERE patient_id = ? AND tooth_code = ?
                """, (int(patient_id), str(tooth_code)))

                conn.commit()


        def delete_all_tooth_records(patient_id):
            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    DELETE FROM patient_tooth_invoices
                    WHERE patient_id = ?
                """, (int(patient_id),))

                cursor.execute("""
                    DELETE FROM patient_tooth_details
                    WHERE patient_id = ?
                """, (int(patient_id),))

                cursor.execute("""
                    DELETE FROM patient_dental_chart_items
                    WHERE patient_id = ?
                """, (int(patient_id),))

                conn.commit()


        def load_patient_basic_info(patient_id):
            try:
                with get_connection() as conn:
                    columns_df = pd.read_sql_query("PRAGMA table_info(patients)", conn)
                    available_columns = columns_df["name"].tolist()

                    df = pd.read_sql_query(
                        "SELECT * FROM patients WHERE id = ? LIMIT 1",
                        conn,
                        params=(int(patient_id),)
                    )

                if df.empty:
                    return {
                        "name": "",
                        "phone": "",
                        "age": "",
                        "gender": "",
                    }

                row = df.iloc[0].to_dict()

                def pick_value(keys):
                    for key in keys:
                        if key in available_columns and row.get(key) not in [None, ""]:
                            return row.get(key)
                    return ""

                return {
                    "name": pick_value(["name", "full_name", "patient_name", "first_name"]),
                    "phone": pick_value(["phone", "phone_number", "mobile", "contact"]),
                    "age": pick_value(["age"]),
                    "gender": pick_value(["gender", "sex"]),
                }

            except Exception:
                return {
                    "name": "",
                    "phone": "",
                    "age": "",
                    "gender": "",
                }


        def build_a5_invoice_html(
            patient_id,
            patient_info,
            tooth_code,
            tooth_type,
            detail_data,
            invoice_data,
        ):
            invoice_title = invoice_data.get("invoice_title", "بل تداوی دندان")
            treatment_name = detail_data.get("proposed_treatment", "")
            dental_problems = detail_data.get("dental_problems", "")
            payment_status = invoice_data.get("payment_status", "")
            payment_method = invoice_data.get("payment_method", "")
            payment_notes = invoice_data.get("payment_notes", "")

            treatment_cost = float(invoice_data.get("treatment_cost", 0) or 0)
            material_cost = float(invoice_data.get("material_cost", 0) or 0)
            lab_cost = float(invoice_data.get("lab_cost", 0) or 0)
            discount = float(invoice_data.get("discount", 0) or 0)
            tax = float(invoice_data.get("tax", 0) or 0)
            total_amount = float(invoice_data.get("total_amount", 0) or 0)
            paid_amount = float(invoice_data.get("paid_amount", 0) or 0)
            balance = float(invoice_data.get("balance", 0) or 0)

            patient_name = safe_html_text(patient_info.get("name", ""))
            patient_phone = safe_html_text(patient_info.get("phone", ""))
            patient_age = safe_html_text(patient_info.get("age", ""))
            patient_gender = safe_html_text(patient_info.get("gender", ""))

            invoice_title = safe_html_text(invoice_title)
            treatment_name = safe_html_text(treatment_name)
            dental_problems = safe_html_text(dental_problems)
            payment_status = safe_html_text(payment_status)
            payment_method = safe_html_text(payment_method)
            payment_notes = safe_html_text(payment_notes)

            tooth_code = safe_html_text(tooth_code)
            tooth_type = safe_html_text(tooth_type)

            html = f"""
            <!DOCTYPE html>
            <html lang="fa" dir="rtl">
            <head>
                <meta charset="UTF-8">

                <style>
                    * {{
                        box-sizing: border-box;
                    }}

                    body {{
                        margin: 0;
                        padding: 0;
                        background: #e5e7eb;
                        font-family: Tahoma, Arial, sans-serif;
                        direction: rtl;
                        color: #111827;
                    }}

                    .page {{
                        width: 138mm;
                        min-height: 198mm;
                        margin: 0 auto;
                        background: #ffffff;
                        padding: 8mm;
                        border: 1px solid #d1d5db;
                    }}

                    .print-btn {{
                        width: 100%;
                        margin-bottom: 10px;
                        padding: 8px;
                        background: #0ea5e9;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 13px;
                        font-weight: 900;
                        cursor: pointer;
                    }}

                    .header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        border-bottom: 2px solid #111827;
                        padding-bottom: 8px;
                        margin-bottom: 10px;
                    }}

                    .clinic-name {{
                        font-size: 19px;
                        font-weight: 900;
                        margin-bottom: 3px;
                    }}

                    .clinic-sub {{
                        font-size: 11px;
                        color: #4b5563;
                    }}

                    .invoice-box {{
                        text-align: left;
                    }}

                    .invoice-title {{
                        font-size: 17px;
                        font-weight: 900;
                        color: #0f172a;
                    }}

                    .invoice-meta {{
                        font-size: 10px;
                        color: #4b5563;
                        margin-top: 4px;
                    }}

                    .section {{
                        margin-top: 9px;
                        border: 1px solid #e5e7eb;
                        border-radius: 8px;
                        overflow: hidden;
                    }}

                    .section-title {{
                        background: #0f172a;
                        color: #ffffff;
                        padding: 6px 8px;
                        font-size: 12px;
                        font-weight: 900;
                    }}

                    .grid {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                    }}

                    .row {{
                        display: flex;
                        justify-content: space-between;
                        gap: 8px;
                        padding: 6px 8px;
                        border-bottom: 1px solid #f1f5f9;
                        font-size: 11px;
                    }}

                    .row span {{
                        color: #4b5563;
                    }}

                    .row strong {{
                        color: #111827;
                        font-weight: 900;
                        text-align: left;
                    }}

                    .full {{
                        grid-column: span 2;
                    }}

                    .amount-table {{
                        width: 100%;
                        border-collapse: collapse;
                        font-size: 11px;
                    }}

                    .amount-table th {{
                        background: #f3f4f6;
                        padding: 6px;
                        text-align: right;
                        border-bottom: 1px solid #e5e7eb;
                    }}

                    .amount-table td {{
                        padding: 6px;
                        border-bottom: 1px solid #f1f5f9;
                    }}

                    .amount-table td:last-child {{
                        text-align: left;
                        font-weight: 900;
                    }}

                    .total-row td {{
                        background: #ecfeff;
                        font-size: 13px;
                        font-weight: 900;
                        border-top: 2px solid #0891b2;
                    }}

                    .paid-row td:last-child {{
                        color: #047857;
                    }}

                    .balance-row td:last-child {{
                        color: #dc2626;
                        font-size: 13px;
                    }}

                    .note-box {{
                        min-height: 35px;
                        padding: 8px;
                        font-size: 11px;
                        color: #374151;
                        line-height: 1.6;
                    }}

                    .signature-area {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 18px;
                        margin-top: 20px;
                        font-size: 11px;
                    }}

                    .signature-box {{
                        border-top: 1px dashed #6b7280;
                        padding-top: 6px;
                        text-align: center;
                        color: #374151;
                    }}

                    .footer {{
                        margin-top: 14px;
                        padding-top: 8px;
                        border-top: 1px dashed #9ca3af;
                        text-align: center;
                        font-size: 10px;
                        color: #4b5563;
                        line-height: 1.6;
                    }}

                    @media print {{
                        body {{
                            background: #ffffff;
                            margin: 0;
                            padding: 0;
                        }}

                        .print-btn {{
                            display: none;
                        }}

                        .page {{
                            width: 138mm;
                            min-height: 198mm;
                            margin: 0 auto;
                            border: none;
                            box-shadow: none;
                            padding: 8mm;
                        }}

                        @page {{
                            size: A5 portrait;
                            margin: 5mm;
                        }}
                    }}
                </style>
            </head>

            <body>
                <div class="page">
                    <button class="print-btn" onclick="window.print()">🖨️ پرینت بل در کاغذ A5</button>

                    <div class="header">
                        <div>
                            <div class="clinic-name">کلینیک دندان</div>
                            <div class="clinic-sub">رسید / بل تداوی دندان</div>
                        </div>

                        <div class="invoice-box">
                            <div class="invoice-title">{invoice_title}</div>
                            <div class="invoice-meta">آی‌دی مریض: {patient_id}</div>
                        </div>
                    </div>

                    <div class="section">
                        <div class="section-title">معلومات مریض</div>

                        <div class="grid">
                            <div class="row">
                                <span>نام مریض:</span>
                                <strong>{patient_name}</strong>
                            </div>

                            <div class="row">
                                <span>شماره تماس:</span>
                                <strong>{patient_phone}</strong>
                            </div>

                            <div class="row">
                                <span>سن:</span>
                                <strong>{patient_age}</strong>
                            </div>

                            <div class="row">
                                <span>جنسیت:</span>
                                <strong>{patient_gender}</strong>
                            </div>
                        </div>
                    </div>

                    <div class="section">
                        <div class="section-title">معلومات دندان و تداوی</div>

                        <div class="grid">
                            <div class="row">
                                <span>شماره دندان:</span>
                                <strong>{tooth_code}</strong>
                            </div>

                            <div class="row">
                                <span>نوع دندان:</span>
                                <strong>{tooth_type}</strong>
                            </div>

                            <div class="row full">
                                <span>مشکل دندان:</span>
                                <strong>{dental_problems}</strong>
                            </div>

                            <div class="row full">
                                <span>نوع تداوی:</span>
                                <strong>{treatment_name}</strong>
                            </div>
                        </div>
                    </div>

                    <div class="section">
                        <div class="section-title">جزئیات مالی</div>

                        <table class="amount-table">
                            <tr>
                                <th>شرح</th>
                                <th>مبلغ</th>
                            </tr>

                            <tr>
                                <td>هزینه تداوی</td>
                                <td>${treatment_cost:,.2f}</td>
                            </tr>

                            <tr>
                                <td>هزینه مواد</td>
                                <td>${material_cost:,.2f}</td>
                            </tr>

                            <tr>
                                <td>هزینه لابراتوار</td>
                                <td>${lab_cost:,.2f}</td>
                            </tr>

                            <tr>
                                <td>تخفیف</td>
                                <td>${discount:,.2f}</td>
                            </tr>

                            <tr>
                                <td>مالیه</td>
                                <td>${tax:,.2f}</td>
                            </tr>

                            <tr class="total-row">
                                <td>مجموع</td>
                                <td>${total_amount:,.2f}</td>
                            </tr>

                            <tr class="paid-row">
                                <td>پرداخت‌شده</td>
                                <td>${paid_amount:,.2f}</td>
                            </tr>

                            <tr class="balance-row">
                                <td>باقی‌مانده</td>
                                <td>${balance:,.2f}</td>
                            </tr>
                        </table>
                    </div>

                    <div class="section">
                        <div class="section-title">پرداخت</div>

                        <div class="grid">
                            <div class="row">
                                <span>روش پرداخت:</span>
                                <strong>{payment_method}</strong>
                            </div>

                            <div class="row">
                                <span>وضعیت پرداخت:</span>
                                <strong>{payment_status}</strong>
                            </div>

                            <div class="full note-box">
                                <strong>یادداشت:</strong><br>
                                {payment_notes}
                            </div>
                        </div>
                    </div>

                    <div class="signature-area">
                        <div class="signature-box">امضای مسئول کلینیک</div>
                        <div class="signature-box">امضای مریض</div>
                    </div>

                    <div class="footer">
                        تشکر از مراجعه شما<br>
                        لطفاً این بل را با خود نگهدارید.
                    </div>
                </div>
            </body>
            </html>
            """

            return html

        # =====================================================
        # INIT
        # =====================================================
        ensure_tooth_management_tables()
        tooth_records = load_all_chart_records(p_id)

        manual_selected_key = f"manual_selected_tooth_{p_id}"

        if manual_selected_key not in st.session_state:
            st.session_state[manual_selected_key] = "1"

        selected_tooth_for_chart = st.session_state[manual_selected_key]

        # =====================================================
        # GRAPHIC CHART - NATURAL TEETH
        # =====================================================
        def get_tooth_position(tooth_number):
            upper_positions = {
                1:  (266, 390, -42),
                2:  (287, 330, -34),
                3:  (318, 276, -27),
                4:  (354, 230, -20),
                5:  (395, 193, -13),
                6:  (438, 165, -7),
                7:  (482, 149, -3),
                8:  (522, 146, 0),
                9:  (562, 146, 0),
                10: (602, 149, 3),
                11: (646, 165, 7),
                12: (689, 193, 13),
                13: (730, 230, 20),
                14: (766, 276, 27),
                15: (797, 330, 34),
                16: (818, 390, 42),
            }

            lower_positions = {
                32: (266, 604, 42),
                31: (287, 664, 34),
                30: (318, 718, 27),
                29: (354, 764, 20),
                28: (395, 801, 13),
                27: (438, 829, 7),
                26: (482, 845, 3),
                25: (522, 848, 0),
                24: (562, 848, 0),
                23: (602, 845, -3),
                22: (646, 829, -7),
                21: (689, 801, -13),
                20: (730, 764, -20),
                19: (766, 718, -27),
                18: (797, 664, -34),
                17: (818, 604, -42),
            }

            if tooth_number in upper_positions:
                return upper_positions[tooth_number]

            return lower_positions[tooth_number]


        def get_primary_tooth_position(tooth_label):
            primary_positions = {
                "A": (335, 430, -30),
                "B": (374, 390, -22),
                "C": (417, 362, -14),
                "D": (464, 344, -6),
                "E": (512, 338, 0),
                "F": (572, 338, 0),
                "G": (620, 344, 6),
                "H": (667, 362, 14),
                "I": (710, 390, 22),
                "J": (749, 430, 30),

                "T": (335, 564, 30),
                "S": (374, 604, 22),
                "R": (417, 632, 14),
                "Q": (464, 650, 6),
                "P": (512, 656, 0),
                "O": (572, 656, 0),
                "N": (620, 650, -6),
                "M": (667, 632, -14),
                "L": (710, 604, -22),
                "K": (749, 564, -30),
            }

            return primary_positions[tooth_label]


        def tooth_category(tooth_number):
            if tooth_number in [1, 2, 3, 14, 15, 16, 17, 18, 19, 30, 31, 32]:
                return "molar"

            if tooth_number in [4, 5, 12, 13, 20, 21, 28, 29]:
                return "premolar"

            if tooth_number in [6, 11, 22, 27]:
                return "canine"

            return "incisor"


        def tooth_dimensions(tooth_number):
            kind = tooth_category(tooth_number)

            if kind == "molar":
                return 66, 72

            if kind == "premolar":
                return 54, 62

            if kind == "canine":
                return 48, 68

            return 44, 60


        def anatomical_tooth_path(tooth_number, upper=True):
            kind = tooth_category(tooth_number)
            width, height = tooth_dimensions(tooth_number)

            x = width / 2
            y = height / 2

            if kind == "molar":
                return (
                    f"M {-x*0.92} {-y*0.52} "
                    f"C {-x*1.12} {-y*0.12}, {-x*1.03} {y*0.45}, {-x*0.60} {y*0.82} "
                    f"C {-x*0.28} {y*1.08}, {x*0.28} {y*1.08}, {x*0.60} {y*0.82} "
                    f"C {x*1.03} {y*0.45}, {x*1.12} {-y*0.12}, {x*0.92} {-y*0.52} "
                    f"C {x*0.62} {-y*1.02}, {-x*0.62} {-y*1.02}, {-x*0.92} {-y*0.52} Z"
                )

            if kind == "premolar":
                return (
                    f"M 0 {-y*1.05} "
                    f"C {x*0.88} {-y*0.90}, {x*1.02} {-y*0.08}, {x*0.72} {y*0.63} "
                    f"C {x*0.36} {y*1.05}, {-x*0.36} {y*1.05}, {-x*0.72} {y*0.63} "
                    f"C {-x*1.02} {-y*0.08}, {-x*0.88} {-y*0.90}, 0 {-y*1.05} Z"
                )

            if kind == "canine":
                if upper:
                    return (
                        f"M {-x*0.66} {-y*0.62} "
                        f"C {-x*0.98} {-y*0.04}, {-x*0.50} {y*0.48}, 0 {y*1.16} "
                        f"C {x*0.50} {y*0.48}, {x*0.98} {-y*0.04}, {x*0.66} {-y*0.62} "
                        f"C {x*0.32} {-y*1.04}, {-x*0.32} {-y*1.04}, {-x*0.66} {-y*0.62} Z"
                    )

                return (
                    f"M {-x*0.66} {y*0.62} "
                    f"C {-x*0.98} {y*0.04}, {-x*0.50} {-y*0.48}, 0 {-y*1.16} "
                    f"C {x*0.50} {-y*0.48}, {x*0.98} {y*0.04}, {x*0.66} {y*0.62} "
                    f"C {x*0.32} {y*1.04}, {-x*0.32} {y*1.04}, {-x*0.66} {y*0.62} Z"
                )

            return (
                f"M {-x*0.78} {-y*0.70} "
                f"C {-x*0.58} {-y*1.05}, {x*0.58} {-y*1.05}, {x*0.78} {-y*0.70} "
                f"L {x*0.65} {y*0.76} "
                f"C {x*0.34} {y*1.08}, {-x*0.34} {y*1.08}, {-x*0.65} {y*0.76} Z"
            )


        def anatomical_details(tooth_number):
            kind = tooth_category(tooth_number)
            width, height = tooth_dimensions(tooth_number)

            x = width / 2
            y = height / 2

            if kind == "molar":
                return f"""
                    <path class="enamel-groove" d="M {-x*0.55} {-y*0.10} C {-x*0.20} {y*0.06}, {x*0.20} {y*0.06}, {x*0.55} {-y*0.10}" />
                    <path class="enamel-groove" d="M 0 {-y*0.62} C {-x*0.10} {-y*0.20}, {-x*0.10} {y*0.34}, 0 {y*0.65}" />
                    <path class="enamel-groove" d="M {-x*0.42} {y*0.36} C {-x*0.12} {y*0.22}, {x*0.12} {y*0.22}, {x*0.42} {y*0.36}" />
                    <circle class="cusp-dot" cx="{-x*0.35}" cy="{-y*0.34}" r="2.8" />
                    <circle class="cusp-dot" cx="{x*0.35}" cy="{-y*0.34}" r="2.8" />
                    <circle class="cusp-dot" cx="{-x*0.30}" cy="{y*0.32}" r="2.5" />
                    <circle class="cusp-dot" cx="{x*0.30}" cy="{y*0.32}" r="2.5" />
                """

            if kind == "premolar":
                return f"""
                    <path class="enamel-groove" d="M {-x*0.45} 0 C {-x*0.10} {y*0.17}, {x*0.10} {y*0.17}, {x*0.45} 0" />
                    <path class="enamel-groove" d="M 0 {-y*0.50} C {-x*0.05} {-y*0.08}, {-x*0.05} {y*0.32}, 0 {y*0.58}" />
                    <circle class="cusp-dot" cx="{-x*0.22}" cy="{-y*0.18}" r="2.3" />
                    <circle class="cusp-dot" cx="{x*0.22}" cy="{-y*0.18}" r="2.3" />
                """

            if kind == "canine":
                return f"""
                    <path class="enamel-groove" d="M 0 {-y*0.62} C {-x*0.08} {-y*0.10}, {-x*0.06} {y*0.34}, 0 {y*0.74}" />
                """

            return f"""
                <path class="enamel-groove" d="M {-x*0.42} {-y*0.08} C {-x*0.12} {y*0.10}, {x*0.12} {y*0.10}, {x*0.42} {-y*0.08}" />
            """


        def primary_tooth_path():
            return (
                "M -15 -19 "
                "C -23 -11, -21 12, -10 20 "
                "C -4 25, 4 25, 10 20 "
                "C 21 12, 23 -11, 15 -19 "
                "C 8 -26, -8 -26, -15 -19 Z"
            )


        def get_status_for_tooth(code):
            record = tooth_records.get(str(code), {})
            return safe_status(record.get("status", "سالم"))


        def get_gradient_for_status(status):
            gradient_map = {
                "سالم": "toothGradHealthy",
                "خرابی دندان": "toothGradDecay",
                "دندان گم‌شده": "toothGradMissing",
                "عصب‌کشی": "toothGradEndo",
                "روکش": "toothGradCrown",
                "پرکاری": "toothGradFilling",
                "ایمپلنت": "toothGradImplant",
                "ضرورت کشیدن": "toothGradExtraction",
                "در جریان تداوی": "toothGradTreatment",
            }

            return gradient_map.get(status, "toothGradHealthy")


        def build_tooth_svg(tooth_number):
            x, y, rotation = get_tooth_position(tooth_number)
            d = anatomical_tooth_path(tooth_number, upper=tooth_number <= 16)
            details = anatomical_details(tooth_number)

            code = str(tooth_number)
            status = get_status_for_tooth(code)
            grad = get_gradient_for_status(status)

            selected_class = " selected-tooth-svg" if selected_tooth_for_chart == code else ""

            return f"""
                <g id="tooth-{code}"
                class="tooth-node{selected_class}"
                transform="translate({x:.2f} {y:.2f}) rotate({rotation:.2f})">
                    <path class="tooth-root-shadow" d="{d}" transform="translate(5, 9)" />
                    <path class="tooth-side" d="{d}" transform="translate(3.5, 6)" />
                    <path class="tooth-body" style="fill:url(#{grad});" d="{d}" />
                    <path class="tooth-highlight" d="{d}" transform="translate(-6,-8) scale(0.56)" />
                    {details}
                    <text class="tooth-label" x="0" y="5" text-anchor="middle">{code}</text>
                </g>
            """


        def build_primary_tooth_svg(tooth_label):
            x, y, rotation = get_primary_tooth_position(tooth_label)
            d = primary_tooth_path()

            code = str(tooth_label)
            status = get_status_for_tooth(code)
            grad = get_gradient_for_status(status)

            selected_class = " selected-tooth-svg" if selected_tooth_for_chart == code else ""

            return f"""
                <g id="primary-tooth-{code}"
                class="primary-tooth-node{selected_class}"
                transform="translate({x:.2f} {y:.2f}) rotate({rotation:.2f})">
                    <path class="primary-tooth-side" d="{d}" transform="translate(3, 5)" />
                    <path class="primary-tooth-body" style="fill:url(#{grad});" d="{d}" />
                    <path class="primary-tooth-highlight" d="{d}" transform="translate(-3,-5) scale(0.62)" />
                    <text class="primary-tooth-label" x="0" y="5" text-anchor="middle">{code}</text>
                </g>
            """


        upper_svg = "".join(build_tooth_svg(tooth) for tooth in UPPER_TEETH)
        lower_svg = "".join(build_tooth_svg(tooth) for tooth in LOWER_TEETH)

        primary_svg = ""

        for tooth in PRIMARY_UPPER_TEETH:
            primary_svg += build_primary_tooth_svg(tooth)

        for tooth in PRIMARY_LOWER_TEETH:
            primary_svg += build_primary_tooth_svg(tooth)

        legend_html = ""

        for status, color in STATUS_COLOR_MAP.items():
            legend_html += f"""
                <div class="legend-item">
                    <span class="legend-dot" style="background:{color};"></span>
                    <span>{status}</span>
                </div>
            """

        chart_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">

            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: #08111f;
                    font-family: Arial, sans-serif;
                    overflow: hidden;
                }}

                .dental-chart-wrapper {{
                    width: 100%;
                    height: 1080px;
                    background: #08111f;
                    border-radius: 20px;
                    overflow: hidden;
                    border: 1px solid rgba(255,255,255,0.12);
                    box-shadow: 0 18px 44px rgba(0,0,0,0.48);
                }}

                .dental-browser-top {{
                    height: 48px;
                    background: #111820;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    padding: 0 18px;
                    color: #dfe6ee;
                    font-weight: 700;
                    border-bottom: 1px solid rgba(255,255,255,0.08);
                }}

                .dental-browser-dot {{
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    background: #2ECC71;
                    box-shadow: 20px 0 #F1C40F, 40px 0 #E74C3C;
                    margin-right: 48px;
                }}

                .dental-svg-shell {{
                    position: relative;
                    width: 100%;
                    height: 1032px;
                    overflow: hidden;
                    background:
                        radial-gradient(circle at 50% 45%, rgba(255,255,255,0.16), transparent 22%),
                        radial-gradient(circle at center, #1E73BE 0%, #0f3d68 56%, #071a2f 100%);
                }}

                .dental-legend {{
                    position: absolute;
                    top: 14px;
                    left: 50%;
                    transform: translateX(-50%);
                    z-index: 10;
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    justify-content: center;
                    padding: 10px 14px;
                    border-radius: 16px;
                    background: rgba(0,0,0,0.38);
                    border: 1px solid rgba(255,255,255,0.25);
                    max-width: 790px;
                }}

                .legend-item {{
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    color: #fff;
                    font-size: 11px;
                    font-weight: 800;
                    padding: 5px 8px;
                    border-radius: 12px;
                    background: rgba(255,255,255,0.09);
                }}

                .legend-dot {{
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    border: 2px solid rgba(255,255,255,0.78);
                    display: inline-block;
                }}

                .selected-status-strip {{
                    position: absolute;
                    left: 50%;
                    top: 496px;
                    transform: translate(-50%, -50%);
                    z-index: 9;
                    color: #fff;
                    background: rgba(0,0,0,0.34);
                    border: 1px solid rgba(255,255,255,0.25);
                    border-radius: 999px;
                    padding: 8px 18px;
                    font-size: 14px;
                    font-weight: 900;
                    pointer-events: none;
                }}

                .quadrant-label {{
                    position: absolute;
                    z-index: 8;
                    color: #d9ebff;
                    background: rgba(5,25,50,0.46);
                    border: 1px solid rgba(130,190,255,0.36);
                    border-radius: 12px;
                    padding: 9px 13px;
                    text-align: center;
                    font-size: 13px;
                    font-weight: 900;
                    line-height: 1.32;
                }}

                .q-ur {{ left: 100px; top: 220px; }}
                .q-ul {{ right: 100px; top: 220px; }}
                .q-lr {{ left: 100px; bottom: 255px; }}
                .q-ll {{ right: 100px; bottom: 255px; }}

                svg {{
                    width: 100%;
                    height: 1032px;
                    display: block;
                }}

                .tooth-node,
                .primary-tooth-node {{
                    cursor: pointer;
                    transition: filter 0.16s ease, transform 0.16s ease;
                }}

                .tooth-node:hover,
                .primary-tooth-node:hover {{
                    filter: drop-shadow(0 0 15px rgba(255,255,255,0.95));
                }}

                .tooth-root-shadow {{
                    fill: rgba(0,0,0,0.20);
                    stroke: none;
                    filter: blur(0.4px);
                }}

                .tooth-side {{
                    fill: rgba(19,110,45,0.70);
                    stroke: rgba(0,0,0,0.18);
                    stroke-width: 1.2;
                    filter: url(#toothSideShadow);
                }}

                .tooth-body {{
                    stroke: rgba(255,255,255,0.94);
                    stroke-width: 2.4;
                    filter: url(#tooth3dShadow);
                }}

                .tooth-highlight {{
                    fill: rgba(255,255,255,0.36);
                    pointer-events: none;
                    opacity: 0.88;
                }}

                .selected-tooth-svg .tooth-body,
                .selected-tooth-svg .primary-tooth-body {{
                    stroke: #ffffff !important;
                    stroke-width: 7 !important;
                    filter: url(#selectedGlow) !important;
                }}

                .tooth-label,
                .primary-tooth-label {{
                    font-size: 12px;
                    font-weight: 950;
                    fill: #111;
                    paint-order: stroke;
                    stroke: rgba(255,255,255,0.88);
                    stroke-width: 2.7;
                    pointer-events: none;
                    user-select: none;
                }}

                .primary-tooth-label {{
                    font-size: 11px;
                }}

                .primary-tooth-side {{
                    fill: rgba(150,100,40,0.30);
                    stroke: rgba(0,0,0,0.15);
                    stroke-width: 0.9;
                    filter: url(#toothSideShadow);
                }}

                .primary-tooth-body {{
                    stroke: rgba(255,255,255,0.90);
                    stroke-width: 1.7;
                    filter: url(#primaryToothShadow);
                }}

                .primary-tooth-highlight {{
                    fill: rgba(255,255,255,0.40);
                    pointer-events: none;
                    opacity: 0.92;
                }}

                .enamel-groove {{
                    fill: none;
                    stroke: rgba(12,55,25,0.44);
                    stroke-width: 1.45;
                    stroke-linecap: round;
                    stroke-linejoin: round;
                    pointer-events: none;
                }}

                .cusp-dot {{
                    fill: rgba(255,255,255,0.68);
                    stroke: rgba(20,20,20,0.12);
                    stroke-width: 0.5;
                    pointer-events: none;
                }}

                .quadrant-line {{
                    stroke: rgba(255,255,255,0.48);
                    stroke-width: 2;
                    stroke-dasharray: 8 10;
                }}

                .arch-guide {{
                    fill: none;
                    stroke: rgba(255,255,255,0.30);
                    stroke-width: 2;
                    stroke-linecap: round;
                    stroke-dasharray: 7 9;
                }}

                .primary-title {{
                    font-size: 13px;
                    font-weight: 900;
                    fill: rgba(255,255,255,0.92);
                    paint-order: stroke;
                    stroke: rgba(0,0,0,0.36);
                    stroke-width: 3;
                }}

                .gum-detail {{
                    fill: none;
                    stroke: rgba(255,255,255,0.22);
                    stroke-width: 3;
                    stroke-linecap: round;
                }}

                .gum-shadow-line {{
                    fill: none;
                    stroke: rgba(120,20,45,0.18);
                    stroke-width: 8;
                    stroke-linecap: round;
                }}

                .click-hint {{
                    position: absolute;
                    left: 50%;
                    bottom: 18px;
                    transform: translateX(-50%);
                    z-index: 10;
                    color: #fff;
                    background: rgba(0,0,0,0.38);
                    border: 1px solid rgba(255,255,255,0.18);
                    border-radius: 18px;
                    padding: 8px 14px;
                    font-size: 13px;
                    font-weight: 800;
                }}
            </style>
        </head>

        <body>
            <div class="dental-chart-wrapper">
                <div class="dental-browser-top">
                    <div class="dental-browser-dot"></div>
                    <span>Odontogram</span>
                </div>

                <div class="dental-svg-shell">
                    <div class="dental-legend">
                        {legend_html}
                    </div>

                    <div class="quadrant-label q-ur">Upper Right<br>Quadrant<br>1-8</div>
                    <div class="quadrant-label q-ul">Upper Left<br>Quadrant<br>9-16</div>
                    <div class="quadrant-label q-lr">Lower Right<br>Quadrant<br>25-32</div>
                    <div class="quadrant-label q-ll">Lower Left<br>Quadrant<br>17-24</div>

                    <div class="selected-status-strip">
                        دندان انتخاب‌شده {selected_tooth_for_chart}
                    </div>

                    <svg viewBox="0 0 1080 1032" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="gumGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" stop-color="#ffdce5"/>
                                <stop offset="45%" stop-color="#ff9fb8"/>
                                <stop offset="100%" stop-color="#d96d8a"/>
                            </linearGradient>

                            <radialGradient id="mouthCavity" cx="50%" cy="50%" r="65%">
                                <stop offset="0%" stop-color="#ffd9e3" stop-opacity="0.72"/>
                                <stop offset="55%" stop-color="#f7a8bd" stop-opacity="0.38"/>
                                <stop offset="100%" stop-color="#d76e8a" stop-opacity="0.16"/>
                            </radialGradient>

                            <filter id="gumShadow" x="-50%" y="-50%" width="200%" height="200%">
                                <feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="#000000" flood-opacity="0.35"/>
                                <feDropShadow dx="0" dy="-4" stdDeviation="5" flood-color="#ffffff" flood-opacity="0.18"/>
                            </filter>

                            <filter id="tooth3dShadow" x="-60%" y="-60%" width="220%" height="220%">
                                <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000000" flood-opacity="0.38"/>
                                <feDropShadow dx="-2" dy="-2" stdDeviation="2" flood-color="#ffffff" flood-opacity="0.25"/>
                            </filter>

                            <filter id="toothSideShadow" x="-50%" y="-50%" width="200%" height="200%">
                                <feDropShadow dx="0" dy="5" stdDeviation="3" flood-color="#000000" flood-opacity="0.32"/>
                            </filter>

                            <filter id="selectedGlow" x="-90%" y="-90%" width="280%" height="280%">
                                <feDropShadow dx="0" dy="0" stdDeviation="7" flood-color="#ffffff" flood-opacity="1"/>
                                <feDropShadow dx="0" dy="0" stdDeviation="15" flood-color="#ffffff" flood-opacity="0.78"/>
                                <feDropShadow dx="0" dy="5" stdDeviation="5" flood-color="#000000" flood-opacity="0.38"/>
                            </filter>

                            <filter id="primaryToothShadow" x="-60%" y="-60%" width="220%" height="220%">
                                <feDropShadow dx="0" dy="4" stdDeviation="3" flood-color="#000000" flood-opacity="0.30"/>
                                <feDropShadow dx="-1" dy="-1" stdDeviation="1.5" flood-color="#ffffff" flood-opacity="0.35"/>
                            </filter>

                            <radialGradient id="toothGradHealthy" cx="35%" cy="24%" r="78%">
                                <stop offset="0%" stop-color="#c8ffc4"/>
                                <stop offset="35%" stop-color="#76de73"/>
                                <stop offset="72%" stop-color="#38aa4b"/>
                                <stop offset="100%" stop-color="#1e7c34"/>
                            </radialGradient>

                            <radialGradient id="toothGradDecay" cx="35%" cy="24%" r="78%">
                                <stop offset="0%" stop-color="#ffc1b8"/>
                                <stop offset="35%" stop-color="#f36e61"/>
                                <stop offset="72%" stop-color="#d64235"/>
                                <stop offset="100%" stop-color="#9f241c"/>
                            </radialGradient>

                            <radialGradient id="toothGradMissing" cx="35%" cy="24%" r="78%">
                                <stop offset="0%" stop-color="#e5e8e8"/>
                                <stop offset="40%" stop-color="#bfc9ca"/>
                                <stop offset="80%" stop-color="#839192"/>
                                <stop offset="100%" stop-color="#566573"/>
                            </radialGradient>

                            <radialGradient id="toothGradEndo" cx="35%" cy="24%" r="78%">
                                <stop offset="0%" stop-color="#fff8b8"/>
                                <stop offset="40%" stop-color="#f7dc6f"/>
                                <stop offset="80%" stop-color="#d4ac0d"/>
                                <stop offset="100%" stop-color="#9a7d0a"/>
                            </radialGradient>

                            <radialGradient id="toothGradCrown" cx="35%" cy="24%" r="78%">
                                <stop offset="0%" stop-color="#e8d3ef"/>
                                <stop offset="40%" stop-color="#b378c6"/>
                                <stop offset="80%" stop-color="#8546a0"/>
                                <stop offset="100%" stop-color="#512e5f"/>
                            </radialGradient>

                            <radialGradient id="toothGradFilling" cx="35%" cy="24%" r="78%">
                                <stop offset="0%" stop-color="#d6eaff"/>
                                <stop offset="40%" stop-color="#5dade2"/>
                                <stop offset="80%" stop-color="#2e86c1"/>
                                <stop offset="100%" stop-color="#1b4f72"/>
                            </radialGradient>

                            <radialGradient id="toothGradImplant" cx="35%" cy="24%" r="78%">
                                <stop offset="0%" stop-color="#c1fff4"/>
                                <stop offset="40%" stop-color="#48c9b0"/>
                                <stop offset="80%" stop-color="#16a085"/>
                                <stop offset="100%" stop-color="#0e6251"/>
                            </radialGradient>

                            <radialGradient id="toothGradExtraction" cx="35%" cy="24%" r="78%">
                                <stop offset="0%" stop-color="#ffb3b3"/>
                                <stop offset="40%" stop-color="#e74c3c"/>
                                <stop offset="80%" stop-color="#c0392b"/>
                                <stop offset="100%" stop-color="#7b241c"/>
                            </radialGradient>

                            <radialGradient id="toothGradTreatment" cx="35%" cy="24%" r="78%">
                                <stop offset="0%" stop-color="#ffd8a8"/>
                                <stop offset="40%" stop-color="#f5b041"/>
                                <stop offset="80%" stop-color="#e67e22"/>
                                <stop offset="100%" stop-color="#935116"/>
                            </radialGradient>
                        </defs>

                        <path style="filter:url(#gumShadow)"
                            d="M 228 435
                            C 218 230, 340 92, 542 74
                            C 744 92, 864 230, 854 435
                            C 735 386, 632 368, 542 374
                            C 452 368, 347 386, 228 435 Z"
                            fill="url(#gumGradient)" />

                        <path style="filter:url(#gumShadow)"
                            d="M 228 557
                            C 218 762, 340 900, 542 918
                            C 744 900, 864 762, 854 557
                            C 735 606, 632 624, 542 618
                            C 452 624, 347 606, 228 557 Z"
                            fill="url(#gumGradient)" />

                        <path d="M 365 395
                            C 402 346, 468 320, 542 318
                            C 616 320, 682 346, 719 395
                            C 704 592, 616 648, 542 650
                            C 468 648, 380 592, 365 395 Z"
                            fill="url(#mouthCavity)" />

                        <path class="gum-detail" d="M 300 410 C 370 338, 440 305, 542 302 C 644 305, 714 338, 784 410" />
                        <path class="gum-detail" d="M 300 582 C 370 654, 440 687, 542 690 C 644 687, 714 654, 784 582" />

                        <path class="gum-shadow-line" d="M 315 430 C 400 385, 480 375, 542 378 C 604 375, 684 385, 769 430" />
                        <path class="gum-shadow-line" d="M 315 562 C 400 607, 480 617, 542 614 C 604 617, 684 607, 769 562" />

                        <line class="quadrant-line" x1="542" y1="76" x2="542" y2="920" />
                        <line class="quadrant-line" x1="215" y1="496" x2="870" y2="496" />

                        <path class="arch-guide" d="M 270 410 C 335 255, 430 155, 542 132 C 654 155, 749 255, 814 410" />
                        <path class="arch-guide" d="M 270 582 C 335 737, 430 837, 542 860 C 654 837, 749 737, 814 582" />

                        <text class="primary-title" x="542" y="304" text-anchor="middle">Primary Teeth</text>

                        {primary_svg}
                        {upper_svg}
                        {lower_svg}
                    </svg>

                    <div class="click-hint">برای مدیریت دقیق، از بخش پایین شماره دندان را انتخاب کنید</div>
                </div>
            </div>
        </body>
        </html>
        """

        components.html(chart_html, height=1100, scrolling=False)

        # =====================================================
        # MANAGEMENT PANEL
        # =====================================================
        st.markdown("---")

        st.markdown("""
        <div style="
            direction: rtl;
            text-align: right;
            background: linear-gradient(135deg, #0E1629, #14213D);
            border: 2px solid #00C8FF;
            border-radius: 20px;
            padding: 18px 20px;
            margin-top: 20px;
            margin-bottom: 18px;
            box-shadow: 0 8px 24px rgba(0,200,255,0.18);
        ">
            <h3 style="color:white; text-align:center; margin:0;">
                🦷 بخش مدیریت دندان
            </h3>
            <p style="color:#D4E6F1; text-align:center; margin:8px 0 0 0;">
                شماره دندان را انتخاب کنید و معلومات کلینیکی، پلان تداوی، بل، هزینه و پرداخت را ثبت نمایید.
            </p>
        </div>
        """, unsafe_allow_html=True)

        selector_col1, selector_col2, selector_col3 = st.columns([1, 1, 1])

        with selector_col1:
            tooth_group = st.radio(
                "گروه دندان",
                ["دندان‌های دایمی", "دندان‌های شیری"],
                horizontal=True,
                key=f"tooth_group_{p_id}"
            )

        with selector_col2:
            if tooth_group == "دندان‌های دایمی":
                selectable_teeth = ALL_PERMANENT_TEETH
            else:
                selectable_teeth = ALL_PRIMARY_TEETH

            selected_tooth_code = st.selectbox(
                "انتخاب شماره دندان",
                selectable_teeth,
                index=selectable_teeth.index(st.session_state[manual_selected_key])
                if st.session_state[manual_selected_key] in selectable_teeth else 0,
                key=f"manual_tooth_select_{p_id}"
            )

        with selector_col3:
            st.markdown("<div style='height: 29px;'></div>", unsafe_allow_html=True)

            open_tooth_btn = st.button(
                "🔍 باز کردن مدیریت دندان",
                use_container_width=True,
                type="primary",
                key=f"open_tooth_management_{p_id}"
            )

        if open_tooth_btn:
            st.session_state[manual_selected_key] = selected_tooth_code

            save_chart_record(
                patient_id=p_id,
                tooth_code=selected_tooth_code,
                tooth_status="سالم",
                notes="از بخش مدیریت دستی باز شد"
            )

            st.rerun()

        selected_tooth = st.session_state[manual_selected_key]
        selected_tooth_type = get_tooth_type_from_code(selected_tooth)

        chart_record = load_chart_record(p_id, selected_tooth)
        detail_record = load_tooth_detail_record(p_id, selected_tooth)
        invoice_record = load_tooth_invoice_record(p_id, selected_tooth)

        current_status = safe_status(chart_record.get("status", "سالم"))

        existing_problems = get_existing_multiselect_values(
            detail_record.get("dental_problems", ""),
            STANDARD_DENTAL_PROBLEMS
        )

        existing_treatment = safe_option(
            detail_record.get("proposed_treatment", "فقط معاینه و پیگیری"),
            STANDARD_TREATMENT_PLANS,
            "فقط معاینه و پیگیری"
        )

        existing_problem_severity = safe_option(
            detail_record.get("problem_severity", "خفیف"),
            PROBLEM_SEVERITY_OPTIONS,
            "خفیف"
        )

        existing_treatment_priority = safe_option(
            detail_record.get("treatment_priority", "عادی"),
            TREATMENT_PRIORITY_OPTIONS,
            "عادی"
        )

        existing_treatment_status = safe_option(
            detail_record.get("treatment_status", "پلان‌شده"),
            TREATMENT_STATUS_OPTIONS,
            "پلان‌شده"
        )

        st.success(f"✅ دندان انتخاب‌شده: {selected_tooth} | نوع دندان: {selected_tooth_type}")

        summary_df = pd.DataFrame([{
            "آی‌دی مریض": p_id,
            "دندان انتخاب‌شده": selected_tooth,
            "نوع دندان": selected_tooth_type,
            "حالت فعلی": current_status,
        }])

        st.dataframe(summary_df, use_container_width=True, hide_index=True)

        # =====================================================
        # MAIN FORM
        # =====================================================
        left_col, right_col = st.columns([1.2, 0.8])

        with left_col:
            st.markdown("### 🩺 معلومات کلینیکی و پلان تداوی")

            with st.form(key=f"clinical_management_form_{p_id}_{selected_tooth}"):
                c1, c2 = st.columns(2)

                with c1:
                    tooth_status = st.selectbox(
                        "حالت دندان",
                        TOOTH_STATUS_OPTIONS,
                        index=TOOTH_STATUS_OPTIONS.index(current_status),
                        key=f"tooth_status_{p_id}_{selected_tooth}"
                    )

                    dental_problems = st.multiselect(
                        "مشکلات معمول دندان",
                        STANDARD_DENTAL_PROBLEMS,
                        default=existing_problems,
                        key=f"dental_problems_{p_id}_{selected_tooth}"
                    )

                    problem_severity = st.selectbox(
                        "شدت مشکل",
                        PROBLEM_SEVERITY_OPTIONS,
                        index=PROBLEM_SEVERITY_OPTIONS.index(existing_problem_severity),
                        key=f"problem_severity_{p_id}_{selected_tooth}"
                    )

                with c2:
                    proposed_treatment = st.selectbox(
                        "پلان پیشنهادی تداوی",
                        STANDARD_TREATMENT_PLANS,
                        index=STANDARD_TREATMENT_PLANS.index(existing_treatment),
                        key=f"proposed_treatment_{p_id}_{selected_tooth}"
                    )

                    treatment_priority = st.selectbox(
                        "اولویت تداوی",
                        TREATMENT_PRIORITY_OPTIONS,
                        index=TREATMENT_PRIORITY_OPTIONS.index(existing_treatment_priority),
                        key=f"treatment_priority_{p_id}_{selected_tooth}"
                    )

                    treatment_status = st.selectbox(
                        "وضعیت تداوی",
                        TREATMENT_STATUS_OPTIONS,
                        index=TREATMENT_STATUS_OPTIONS.index(existing_treatment_status),
                        key=f"treatment_status_{p_id}_{selected_tooth}"
                    )

                appointment_date = st.date_input(
                    "تاریخ قرار ملاقات / پیگیری",
                    value=None,
                    key=f"appointment_date_{p_id}_{selected_tooth}"
                )

                diagnosis_notes = st.text_area(
                    "یادداشت تشخیص",
                    value=detail_record.get("diagnosis_notes", ""),
                    height=90,
                    placeholder="علایم، تشخیص، نتیجه ایکسری، یافته‌های کلینیکی...",
                    key=f"diagnosis_notes_{p_id}_{selected_tooth}"
                )

                clinical_notes = st.text_area(
                    "یادداشت داکتر",
                    value=detail_record.get("clinical_notes", ""),
                    height=90,
                    placeholder="یادداشت تداوی، توصیه، خطرات، پیگیری...",
                    key=f"clinical_notes_{p_id}_{selected_tooth}"
                )

                save_clinical_btn = st.form_submit_button(
                    "💾 ثبت معلومات کلینیکی و تداوی",
                    use_container_width=True,
                    type="primary"
                )

                if save_clinical_btn:
                    save_chart_record(
                        patient_id=p_id,
                        tooth_code=selected_tooth,
                        tooth_status=tooth_status,
                        notes=clinical_notes
                    )

                    save_tooth_detail_record(
                        patient_id=p_id,
                        tooth_code=selected_tooth,
                        dental_problems=", ".join(dental_problems),
                        problem_severity=problem_severity,
                        diagnosis_notes=diagnosis_notes,
                        proposed_treatment=proposed_treatment,
                        treatment_priority=treatment_priority,
                        treatment_status=treatment_status,
                        appointment_date=appointment_date,
                        clinical_notes=clinical_notes
                    )

                    st.success(f"✅ معلومات کلینیکی و تداوی برای دندان {selected_tooth} ثبت شد.")
                    st.rerun()

        with right_col:
            st.markdown("### 💳 بل، هزینه و پرداخت")

            existing_treatment_cost = float(invoice_record.get("treatment_cost", 0) or 0)
            existing_material_cost = float(invoice_record.get("material_cost", 0) or 0)
            existing_lab_cost = float(invoice_record.get("lab_cost", 0) or 0)
            existing_discount = float(invoice_record.get("discount", 0) or 0)
            existing_tax = float(invoice_record.get("tax", 0) or 0)
            existing_paid_amount = float(invoice_record.get("paid_amount", 0) or 0)

            subtotal_preview = existing_treatment_cost + existing_material_cost + existing_lab_cost
            total_preview = max(subtotal_preview - existing_discount + existing_tax, 0)
            balance_preview = max(total_preview - existing_paid_amount, 0)

            st.markdown(f"""
            <div style="
                direction: rtl;
                text-align: right;
                background:#0F172A;
                border:1px solid rgba(255,255,255,0.14);
                border-radius:16px;
                padding:14px;
                margin-bottom:12px;
            ">
                <div style="display:flex; justify-content:space-between; color:white;">
                    <span>مجموع</span>
                    <strong>${total_preview:,.2f}</strong>
                </div>
                <div style="display:flex; justify-content:space-between; color:#D4E6F1; margin-top:6px;">
                    <span>پرداخت‌شده</span>
                    <strong>${existing_paid_amount:,.2f}</strong>
                </div>
                <div style="display:flex; justify-content:space-between; color:#F8D7DA; margin-top:6px;">
                    <span>باقی‌مانده</span>
                    <strong>${balance_preview:,.2f}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.form(key=f"invoice_management_form_{p_id}_{selected_tooth}"):
                invoice_title = st.text_input(
                    "عنوان بل",
                    value=invoice_record.get("invoice_title", "بل تداوی دندان"),
                    key=f"invoice_title_{p_id}_{selected_tooth}"
                )

                treatment_cost = st.number_input(
                    "هزینه تداوی",
                    min_value=0.0,
                    value=existing_treatment_cost,
                    step=10.0,
                    key=f"treatment_cost_{p_id}_{selected_tooth}"
                )

                material_cost = st.number_input(
                    "هزینه مواد",
                    min_value=0.0,
                    value=existing_material_cost,
                    step=10.0,
                    key=f"material_cost_{p_id}_{selected_tooth}"
                )

                lab_cost = st.number_input(
                    "هزینه لابراتوار",
                    min_value=0.0,
                    value=existing_lab_cost,
                    step=10.0,
                    key=f"lab_cost_{p_id}_{selected_tooth}"
                )

                discount = st.number_input(
                    "تخفیف",
                    min_value=0.0,
                    value=existing_discount,
                    step=5.0,
                    key=f"discount_{p_id}_{selected_tooth}"
                )

                tax = st.number_input(
                    "مالیه",
                    min_value=0.0,
                    value=existing_tax,
                    step=5.0,
                    key=f"tax_{p_id}_{selected_tooth}"
                )

                paid_amount = st.number_input(
                    "مقدار پرداخت‌شده",
                    min_value=0.0,
                    value=existing_paid_amount,
                    step=10.0,
                    key=f"paid_amount_{p_id}_{selected_tooth}"
                )

                existing_payment_method = safe_option(
                    invoice_record.get("payment_method", "نقدی"),
                    PAYMENT_METHOD_OPTIONS,
                    "نقدی"
                )

                payment_method = st.selectbox(
                    "روش پرداخت",
                    PAYMENT_METHOD_OPTIONS,
                    index=PAYMENT_METHOD_OPTIONS.index(existing_payment_method),
                    key=f"payment_method_{p_id}_{selected_tooth}"
                )

                existing_payment_status = safe_option(
                    invoice_record.get("payment_status", "خودکار"),
                    PAYMENT_STATUS_OPTIONS,
                    "خودکار"
                )

                payment_status = st.selectbox(
                    "وضعیت پرداخت",
                    PAYMENT_STATUS_OPTIONS,
                    index=PAYMENT_STATUS_OPTIONS.index(existing_payment_status),
                    key=f"payment_status_{p_id}_{selected_tooth}"
                )

                payment_notes = st.text_area(
                    "یادداشت پرداخت",
                    value=invoice_record.get("payment_notes", ""),
                    height=90,
                    placeholder="بیمه، قسط، باقی‌مانده، توضیحات پرداخت...",
                    key=f"payment_notes_{p_id}_{selected_tooth}"
                )

                save_invoice_btn = st.form_submit_button(
                    "💾 ثبت بل و پرداخت",
                    use_container_width=True,
                    type="primary"
                )

                if save_invoice_btn:
                    total_amount, balance, final_payment_status = save_tooth_invoice_record(
                        patient_id=p_id,
                        tooth_code=selected_tooth,
                        invoice_title=invoice_title,
                        treatment_cost=treatment_cost,
                        material_cost=material_cost,
                        lab_cost=lab_cost,
                        discount=discount,
                        tax=tax,
                        paid_amount=paid_amount,
                        payment_method=payment_method,
                        payment_status=payment_status,
                        payment_notes=payment_notes
                    )

                    st.success(
                        f"✅ بل ثبت شد | مجموع: ${total_amount:,.2f} | باقی‌مانده: ${balance:,.2f} | وضعیت: {final_payment_status}"
                    )
                    st.rerun()

        # =====================================================
        # A5 PRINT BILL
        # =====================================================
        st.markdown("---")
        st.markdown("### 🧾 پرینت بل A5 برای مریض")

        print_col1, print_col2 = st.columns([1, 1])

        with print_col1:
            show_print_preview = st.button(
                "🧾 نمایش بل A5 برای پرینت",
                use_container_width=True,
                key=f"show_a5_invoice_print_{p_id}_{selected_tooth}"
            )

        with print_col2:
            refresh_invoice_btn = st.button(
                "🔄 تازه‌سازی معلومات بل",
                use_container_width=True,
                key=f"refresh_a5_invoice_{p_id}_{selected_tooth}"
            )

        if refresh_invoice_btn:
            st.rerun()

        if show_print_preview:
            patient_info_for_print = load_patient_basic_info(p_id)
            invoice_data_for_print = load_tooth_invoice_record(p_id, selected_tooth)
            detail_data_for_print = load_tooth_detail_record(p_id, selected_tooth)

            if not invoice_data_for_print:
                st.warning("⚠️ برای این دندان هنوز بل ثبت نشده است. اول بل و پرداخت را ثبت کنید.")
            else:
                a5_invoice_html = build_a5_invoice_html(
                    patient_id=p_id,
                    patient_info=patient_info_for_print,
                    tooth_code=selected_tooth,
                    tooth_type=selected_tooth_type,
                    detail_data=detail_data_for_print,
                    invoice_data=invoice_data_for_print,
                )

                components.html(
                    a5_invoice_html,
                    height=900,
                    scrolling=True
                )

                st.download_button(
                    label="⬇️ دانلود بل A5 به شکل HTML",
                    data=a5_invoice_html,
                    file_name=f"a5_bill_patient_{p_id}_tooth_{selected_tooth}.html",
                    mime="text/html",
                    use_container_width=True,
                    key=f"download_a5_invoice_{p_id}_{selected_tooth}"
                )

        # =====================================================
        # RECORDS TABLE + DELETE
        # =====================================================
        st.markdown("---")
        st.markdown("### 📋 تمام سوابق مدیریت دندان‌ها")

        with get_connection() as conn:
            records_df = pd.read_sql_query("""
                SELECT
                    c.tooth_code AS 'دندان',
                    c.tooth_type AS 'نوع',
                    c.status AS 'حالت',
                    COALESCE(d.dental_problems, '') AS 'مشکلات',
                    COALESCE(d.problem_severity, '') AS 'شدت',
                    COALESCE(d.proposed_treatment, '') AS 'تداوی',
                    COALESCE(d.treatment_priority, '') AS 'اولویت',
                    COALESCE(d.treatment_status, '') AS 'وضعیت تداوی',
                    COALESCE(i.total_amount, 0) AS 'مجموع',
                    COALESCE(i.paid_amount, 0) AS 'پرداخت‌شده',
                    COALESCE(i.balance, 0) AS 'باقی‌مانده',
                    COALESCE(i.payment_status, '') AS 'وضعیت پرداخت',
                    c.updated_at AS 'آخرین تغییر'
                FROM patient_dental_chart_items c
                LEFT JOIN patient_tooth_details d
                    ON c.patient_id = d.patient_id
                    AND c.tooth_code = d.tooth_code
                LEFT JOIN patient_tooth_invoices i
                    ON c.patient_id = i.patient_id
                    AND c.tooth_code = i.tooth_code
                WHERE c.patient_id = ?
                ORDER BY
                    CASE
                        WHEN c.tooth_code GLOB '[0-9]*' THEN CAST(c.tooth_code AS INTEGER)
                        ELSE 100
                    END,
                    c.tooth_code
            """, conn, params=(int(p_id),))

        if records_df.empty:
            st.info("تا هنوز هیچ سابقه‌ای برای دندان‌ها ثبت نشده است.")
        else:
            st.dataframe(records_df, use_container_width=True, hide_index=True)

            st.markdown("### 🗑️ حذف سوابق دندان")

            delete_col1, delete_col2, delete_col3 = st.columns([1, 1, 1])

            with delete_col1:
                tooth_delete_options = records_df["دندان"].astype(str).tolist()

                tooth_to_delete = st.selectbox(
                    "انتخاب دندان برای حذف",
                    tooth_delete_options,
                    key=f"delete_tooth_select_{p_id}"
                )

            with delete_col2:
                st.markdown("<div style='height: 29px;'></div>", unsafe_allow_html=True)

                delete_single_btn = st.button(
                    "🗑️ حذف همین دندان",
                    use_container_width=True,
                    key=f"delete_single_tooth_btn_{p_id}"
                )

            with delete_col3:
                st.markdown("<div style='height: 29px;'></div>", unsafe_allow_html=True)

                delete_all_btn = st.button(
                    "🔥 حذف تمام سوابق",
                    use_container_width=True,
                    key=f"delete_all_teeth_btn_{p_id}"
                )

            if delete_single_btn:
                st.session_state[f"confirm_delete_single_{p_id}"] = True
                st.session_state[f"tooth_to_delete_{p_id}"] = tooth_to_delete

            if st.session_state.get(f"confirm_delete_single_{p_id}", False):
                selected_delete_tooth = st.session_state.get(f"tooth_to_delete_{p_id}", tooth_to_delete)

                st.warning(f"⚠️ آیا مطمئن هستید که سابقه دندان {selected_delete_tooth} حذف شود؟")

                confirm_col1, confirm_col2 = st.columns(2)

                with confirm_col1:
                    if st.button(
                        "✅ بلی، حذف شود",
                        use_container_width=True,
                        key=f"confirm_single_delete_yes_{p_id}"
                    ):
                        delete_single_tooth_record(
                            patient_id=p_id,
                            tooth_code=selected_delete_tooth
                        )

                        st.session_state[f"confirm_delete_single_{p_id}"] = False

                        if manual_selected_key in st.session_state:
                            if st.session_state[manual_selected_key] == selected_delete_tooth:
                                st.session_state[manual_selected_key] = "1"

                        st.success(f"✅ سابقه دندان {selected_delete_tooth} حذف شد.")
                        st.rerun()

                with confirm_col2:
                    if st.button(
                        "❌ لغو",
                        use_container_width=True,
                        key=f"confirm_single_delete_no_{p_id}"
                    ):
                        st.session_state[f"confirm_delete_single_{p_id}"] = False
                        st.rerun()

            if delete_all_btn:
                st.session_state[f"confirm_delete_all_{p_id}"] = True

            if st.session_state.get(f"confirm_delete_all_{p_id}", False):
                st.error("⚠️ هشدار: با تایید این گزینه، تمام سوابق دندان‌های این مریض حذف می‌شود.")

                confirm_all_col1, confirm_all_col2 = st.columns(2)

                with confirm_all_col1:
                    if st.button(
                        "✅ بلی، همه حذف شود",
                        use_container_width=True,
                        key=f"confirm_all_delete_yes_{p_id}"
                    ):
                        delete_all_tooth_records(patient_id=p_id)

                        st.session_state[f"confirm_delete_all_{p_id}"] = False

                        if manual_selected_key in st.session_state:
                            st.session_state[manual_selected_key] = "1"

                        st.success("✅ تمام سوابق دندان‌های این مریض حذف شد.")
                        st.rerun()

                with confirm_all_col2:
                    if st.button(
                        "❌ لغو",
                        use_container_width=True,
                        key=f"confirm_all_delete_no_{p_id}"
                    ):
                        st.session_state[f"confirm_delete_all_{p_id}"] = False
                        st.rerun()



   

# ===== Tab 4: Images and Documents (Organized Version) =====
    with tab4:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #8E44AD, #6C3483); padding: 25px 20px; border-radius: 15px; margin-bottom: 30px;">
                <h1 style="color: white; text-align: center; margin: 0; font-size: 28px;">📁 Images & Documents</h1>
                <p style="color: #E8DAEF; text-align: center; margin: 10px 0 0 0;">Upload and manage radiographs, intraoral photos and medical documents</p>
            </div>
        """, unsafe_allow_html=True)

        # --- Create patient-specific folder ---
        patient_folder = f"patient_files/{p_id}"
        os.makedirs(patient_folder, exist_ok=True)

        # --- Check and create table ---
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS patient_files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER NOT NULL,
                        file_name TEXT NOT NULL,
                        file_type TEXT,
                        file_path TEXT NOT NULL,
                        description TEXT,
                        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
                    )
                """)
                conn.commit()
        except Exception as e:
            st.error(f"❌ Error creating table: {e}")

        col_upload, col_stats = st.columns([2, 1])

        # ========== Upload Column ==========
        with col_upload:
            with st.container(border=True):
                st.markdown("#### 📤 Upload New File")
                
                file_type = st.selectbox(
                    "File Type",
                    ["Radiography (X-Ray)", "Intraoral Photo", "Extraoral Photo", "CT Scan", "Medical Documents", "Other"]
                )
                
                description = st.text_input(
                    "File Description",
                    placeholder="e.g., Panoramic radiograph, Photo of tooth #6..."
                )
                
                uploaded_file = st.file_uploader(
                    "Select File",
                    type=['jpg', 'jpeg', 'png', 'pdf', 'dcm', 'tiff'],
                    help="Allowed formats: Images, PDF, DICOM"
                )
                
                if uploaded_file:
                    file_size = len(uploaded_file.getvalue()) / 1024  # KB
                    file_size_mb = file_size / 1024  # MB
                    
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.caption(f"📄 Name: {uploaded_file.name[:30]}{'...' if len(uploaded_file.name) > 30 else ''}")
                    with col_info2:
                        if file_size_mb > 1:
                            st.caption(f"💾 Size: {file_size_mb:.2f} MB")
                        else:
                            st.caption(f"💾 Size: {file_size:.1f} KB")
                    
                    if st.button("⬆️ Upload File", use_container_width=True, type="primary"):
                        try:
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            safe_filename = f"{timestamp}_{uploaded_file.name}"
                            file_path = os.path.join(patient_folder, safe_filename)
                            
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            with get_connection() as conn:
                                conn.execute("""
                                    INSERT INTO patient_files 
                                    (patient_id, file_name, file_type, file_path, description)
                                    VALUES (?, ?, ?, ?, ?)
                                """, (p_id, uploaded_file.name, file_type, file_path, description))
                                conn.commit()
                            
                            st.success("✅ File uploaded successfully")
                            st.balloons()
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Upload error: {e}")

        # ========== Statistics Column ==========
        with col_stats:
            try:
                with get_connection() as conn:
                    files_count = pd.read_sql_query(
                        "SELECT COUNT(*) as count FROM patient_files WHERE patient_id = ?", 
                        conn, params=(p_id,)
                    ).iloc[0]['count']
                    
                    files_by_type = pd.read_sql_query(
                        "SELECT file_type, COUNT(*) as count FROM patient_files WHERE patient_id = ? GROUP BY file_type",
                        conn, params=(p_id,)
                    )
                    
                    total_size = 0
                    files_list = pd.read_sql_query(
                        "SELECT file_path FROM patient_files WHERE patient_id = ?",
                        conn, params=(p_id,)
                    )
                    for _, row in files_list.iterrows():
                        if os.path.exists(row['file_path']):
                            total_size += os.path.getsize(row['file_path'])
                    
                    total_size_mb = total_size / (1024 * 1024)
                
                st.markdown(f"""
                    <div style="background: linear-gradient(145deg, #6C3483, #5B2C6F); padding: 20px; border-radius: 12px; margin-bottom: 20px;">
                        <div style="text-align: center;">
                            <span style="font-size: 36px;">📊</span>
                            <h3 style="color: white; margin: 10px 0 5px; font-size: 32px;">{files_count}</h3>
                            <p style="color: #E8DAEF; margin: 0; font-size: 14px;">Total Files</p>
                            <p style="color: #F9E79F; margin: 10px 0 0; font-size: 13px;">Total Size: {total_size_mb:.2f} MB</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if not files_by_type.empty:
                    with st.container(border=True):
                        st.markdown("#### 📊 Distribution by Type")
                        for _, row in files_by_type.iterrows():
                            percentage = (row['count'] / files_count) * 100
                            st.markdown(f"""
                                <div style="margin-bottom: 12px;">
                                    <div style="display: flex; justify-content: space-between;">
                                        <span style="font-weight: bold;">{row['file_type']}</span>
                                        <span>{row['count']} ({percentage:.0f}%)</span>
                                    </div>
                                    <div style="width: 100%; background: #ECF0F1; border-radius: 10px; height: 8px;">
                                        <div style="width: {percentage}%; background: #8E44AD; height: 8px; border-radius: 10px;"></div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                
            except Exception as e:
                st.info("ℹ️ No files uploaded yet.")

        # ========== File List (Organized Version) ==========
        st.markdown("<hr style='margin: 30px 0 20px;'>", unsafe_allow_html=True)
        
        st.markdown("""
            <div style="background: linear-gradient(145deg, #2C3E50, #1E2B38); padding: 15px 20px; border-radius: 12px; margin-bottom: 25px;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 24px; margin-right: 10px;">📋</span>
                        <span style="color: white; font-size: 20px; font-weight: bold;">Uploaded Files</span>
                    </div>
                    <span style="color: #AED6F1; font-size: 14px;">👈 Click on file to view</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        try:
            with get_connection() as conn:
                files_df = pd.read_sql_query(
                    """
                    SELECT id, file_name, file_type, file_path, description, uploaded_at 
                    FROM patient_files 
                    WHERE patient_id = ? 
                    ORDER BY uploaded_at DESC
                    """,
                    conn, params=(p_id,)
                )
            
            if not files_df.empty:
                for idx, row in files_df.iterrows():
                    file_exists = os.path.exists(row['file_path'])
                    
                    # Determine icon based on file type
                    file_ext = row['file_path'].lower()
                    if any(ext in file_ext for ext in ['.jpg', '.jpeg', '.png', '.tiff']):
                        file_icon = "🖼️"
                    elif '.pdf' in file_ext:
                        file_icon = "📄"
                    elif '.dcm' in file_ext:
                        file_icon = "🩻"
                    else:
                        file_icon = "📁"
                    
                    # Determine color based on status
                    if not file_exists:
                        status_color = "#E74C3C"
                        status_text = "❌ File Missing"
                    else:
                        status_color = "#2ECC71"
                        status_text = "✅ Available"
                    
                    # File card - clean and uniform design
                    with st.container(border=True):
                        col_icon, col_info, col_actions = st.columns([0.5, 3, 1.5])
                        
                        with col_icon:
                            st.markdown(f"<div style='font-size: 32px; text-align: center;'>{file_icon}</div>", unsafe_allow_html=True)
                        
                        with col_info:
                            st.markdown(f"**{row['file_name'][:40]}{'...' if len(row['file_name']) > 40 else ''}**")
                            
                            col_type, col_date, col_status = st.columns(3)
                            with col_type:
                                st.caption(f"🗂 {row['file_type']}")
                            with col_date:
                                st.caption(f"📅 {row['uploaded_at'][:10]}")
                            with col_status:
                                st.markdown(f"<span style='color: {status_color}; font-size: 12px;'>{status_text}</span>", unsafe_allow_html=True)
                            
                            if row['description']:
                                st.caption(f"📝 {row['description']}")
                        
                        with col_actions:
                            if file_exists:
                                # View button
                                if st.button("👁️ View", key=f"view_{row['id']}", use_container_width=True):
                                    try:
                                        if file_ext.endswith(('.png', '.jpg', '.jpeg', '.tiff')):
                                            st.image(row['file_path'], caption=row['description'], use_container_width=True)
                                        elif file_ext.endswith('.pdf'):
                                            with open(row['file_path'], "rb") as f:
                                                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                                                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500px"></iframe>'
                                                st.markdown(pdf_display, unsafe_allow_html=True)
                                        elif file_ext.endswith('.dcm'):
                                            st.info("ℹ️ DICOM file requires specialized viewer")
                                        else:
                                            st.warning("⚠️ File format not viewable")
                                    except Exception as e:
                                        st.error(f"❌ Error displaying file")
                            
                            # Delete button with popover
                            with st.popover("🗑️ Delete", use_container_width=True):
                                st.caption(f"Are you sure you want to delete this file?")
                                st.markdown(f"**{row['file_name'][:30]}**")
                                col_confirm1, col_confirm2 = st.columns(2)
                                with col_confirm1:
                                    if st.button("✅ Yes", key=f"confirm_del_{row['id']}", use_container_width=True):
                                        try:
                                            if os.path.exists(row['file_path']):
                                                os.remove(row['file_path'])
                                            
                                            with get_connection() as conn:
                                                conn.execute("DELETE FROM patient_files WHERE id = ?", (row['id'],))
                                                conn.commit()
                                            
                                            st.success("✅ Deleted")
                                            st.rerun()
                                        except Exception as e:
                                            st.error("❌ Error")
                                with col_confirm2:
                                    if st.button("❌ No", key=f"cancel_del_{row['id']}", use_container_width=True):
                                        st.rerun()
            else:
                st.info("ℹ️ No files uploaded for this patient yet.")
                st.markdown("""
                    <div style="text-align: center; padding: 40px; background: #F8F9FA; border-radius: 12px;">
                        <span style="font-size: 64px;">📁</span>
                        <p style="color: #7F8C8D; margin-top: 15px; font-size: 16px;">Upload your first file to get started</p>
                    </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.warning("⚠️ Error retrieving file list")
   
   
   
        # ===== Tab 5: Financial Section (نسخه نهایی و بدون خطا) =====
    with tab5:
        # ========== Tab Header ==========
        st.markdown("""
            <div style="background: linear-gradient(135deg, #0A0F1F, #0E1629);
                        padding: 30px 25px;
                        border-radius: 25px;
                        margin-bottom: 30px;
                        border: 2px solid #00C8FF;
                        box-shadow: 0 10px 25px -10px rgba(0, 200, 255, 0.3);">
                <h1 style="color: white; text-align: center; margin: 0; font-size: 32px; font-weight: 700; text-shadow: 0 0 15px #00C8FF;">
                    💰 مدیریت مالی یکپارچه بیمار
                </h1>
                <p style="color: #7FBAFF; text-align: center; margin: 10px 0 0 0; font-size: 16px; letter-spacing: 0.5px;">
                    جمع کل = مبلغ از بخش عمومی + مبلغ از بخش مالی
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # تابع فرمت کردن اعداد
        def afg(x): 
            try:
                return f"{float(x):,.0f}".replace(",", ",")
            except:
                return "0"
        
        # ========== بررسی و ایجاد جداول با ساختار صحیح ==========
        with get_connection() as conn:
            # بررسی و ایجاد جدول dental_services
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dental_services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_name TEXT UNIQUE,
                    default_price REAL DEFAULT 0
                )
            """)
            
            # بررسی و ایجاد جدول patient_invoices
            conn.execute("""
                CREATE TABLE IF NOT EXISTS patient_invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    service_name TEXT NOT NULL,
                    unit_price REAL DEFAULT 0,
                    FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
                )
            """)
            
            # بررسی و ایجاد جدول patient_payments (بدون ستون notes)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS patient_payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    amount REAL DEFAULT 0,
                    payment_method TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
                )
            """)
            
            # سرویس‌های پیش‌فرض
            if conn.execute("SELECT COUNT(*) FROM dental_services").fetchone()[0] == 0:
                default_services = [
                    ('ویزیت و معاینه', 500),
                    ('رادیوگرافی پانورامیک', 1200),
                    ('عصب‌کشی تک کانال', 3500),
                    ('پر کردن دندان', 1500),
                    ('کشیدن ساده', 1200),
                    ('جرم‌گیری', 1000),
                    ('ایمپلنت', 25000),
                    ('لمینت', 18000),
                    ('روکش تمام سرامیک', 10000),
                    ('بلیچینگ', 7000)
                ]
                conn.executemany("INSERT INTO dental_services (service_name, default_price) VALUES (?, ?)", default_services)
                conn.commit()
            
            # ========== دریافت اطلاعات بیمار ==========
            patient_data = pd.read_sql_query(f"SELECT * FROM patients WHERE id = {p_id}", conn)
            if patient_data.empty:
                st.error("بیمار یافت نشد!")
                st.stop()
            patient = patient_data.iloc[0]
            
            # ========== دریافت مقادیر از جدول patients (بخش General) ==========
            patient_financial_query = pd.read_sql_query(f"""
                SELECT 
                    COALESCE(cost, 0) as cost_from_general,
                    COALESCE(paid_amount, 0) as paid_from_general,
                    COALESCE(discount, 0) as discount_from_general
                FROM patients 
                WHERE id = {p_id}
            """, conn)
            
            # بررسی خالی نبودن نتیجه
            if not patient_financial_query.empty:
                patient_financial = patient_financial_query.iloc[0]
            else:
                patient_financial = {'cost_from_general': 0, 'paid_from_general': 0, 'discount_from_general': 0}
            
            # ========== دریافت مقادیر از جداول مالی (بخش Financial) ==========
            invoices_sum_query = pd.read_sql_query(f"""
                SELECT COALESCE(SUM(unit_price), 0) as total 
                FROM patient_invoices 
                WHERE patient_id = {p_id}
            """, conn)
            
            if not invoices_sum_query.empty:
                invoices_from_financial = invoices_sum_query.iloc[0, 0]
            else:
                invoices_from_financial = 0
            
            payments_sum_query = pd.read_sql_query(f"""
                SELECT COALESCE(SUM(amount), 0) as total 
                FROM patient_payments 
                WHERE patient_id = {p_id}
            """, conn)
            
            if not payments_sum_query.empty:
                payments_from_financial = payments_sum_query.iloc[0, 0]
            else:
                payments_from_financial = 0
            
            # ========== دریافت لیست فاکتورها و پرداخت‌ها برای نمایش ==========
            all_invoices = pd.read_sql_query(f"""
                SELECT id, invoice_date, service_name, unit_price
                FROM patient_invoices 
                WHERE patient_id = {p_id}
                ORDER BY invoice_date DESC
            """, conn)
            
            all_payments = pd.read_sql_query(f"""
                SELECT id, payment_date, amount, payment_method
                FROM patient_payments 
                WHERE patient_id = {p_id}
                ORDER BY payment_date DESC
            """, conn)
        
        # ========== محاسبه مقادیر نهایی (جمع دو منبع) ==========
        total_invoices = float(patient_financial['cost_from_general']) + float(invoices_from_financial)
        total_payments = float(patient_financial['paid_from_general']) + float(payments_from_financial)
        total_discount = float(patient_financial['discount_from_general'])
        
        # محاسبه باقی‌مانده
        remaining = total_invoices - total_payments - total_discount
        
        # ========== کارت‌های آماری ==========
        st.markdown("### 📊 خلاصه مالی یکپارچه")
        st.caption("مقادیر زیر مجموع مبالغ از بخش عمومی و بخش مالی می‌باشند")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 20px;
                            border-radius: 15px;
                            border: 2px solid #00C8FF;
                            text-align: center;
                            box-shadow: 0 5px 15px -5px rgba(0, 200, 255, 0.3);">
                    <span style="font-size: 13px; color: #7FBAFF;">جمع فاکتورها</span><br>
                    <span style="font-size: 28px; font-weight: 700; color: white; text-shadow: 0 0 15px #00C8FF;">{afg(total_invoices)}</span><br>
                    <span style="font-size: 11px; color: #7FBAFF;">AFN</span>
                    <div style="font-size: 10px; margin-top: 5px; color: #4D9EFF;">
                        عمومی: {afg(patient_financial['cost_from_general'])} | مالی: {afg(invoices_from_financial)}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 20px;
                            border-radius: 15px;
                            border: 2px solid #00C8FF;
                            text-align: center;
                            box-shadow: 0 5px 15px -5px rgba(0, 200, 255, 0.3);">
                    <span style="font-size: 13px; color: #7FBAFF;">جمع پرداختی</span><br>
                    <span style="font-size: 28px; font-weight: 700; color: #00C8FF; text-shadow: 0 0 15px #00C8FF;">{afg(total_payments)}</span><br>
                    <span style="font-size: 11px; color: #7FBAFF;">AFN</span>
                    <div style="font-size: 10px; margin-top: 5px; color: #4D9EFF;">
                        عمومی: {afg(patient_financial['paid_from_general'])} | مالی: {afg(payments_from_financial)}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            discount_color = "#00C8FF" if total_discount > 0 else "#7FBAFF"
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 20px;
                            border-radius: 15px;
                            border: 2px solid {discount_color};
                            text-align: center;
                            box-shadow: 0 5px 15px -5px rgba(0, 200, 255, 0.3);">
                    <span style="font-size: 13px; color: #7FBAFF;">تخفیف</span><br>
                    <span style="font-size: 28px; font-weight: 700; color: {discount_color}; text-shadow: 0 0 15px {discount_color};">{afg(total_discount)}</span><br>
                    <span style="font-size: 11px; color: #7FBAFF;">AFN</span>
                    <div style="font-size: 10px; margin-top: 5px; color: #4D9EFF;">
                        از بخش عمومی
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            remaining_color = "#00C8FF" if remaining <= 0 else "#FF6B6B"
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629);
                            padding: 20px;
                            border-radius: 15px;
                            border: 2px solid {remaining_color};
                            text-align: center;
                            box-shadow: 0 5px 15px -5px rgba(0, 200, 255, 0.3);">
                    <span style="font-size: 13px; color: #7FBAFF;">باقی‌مانده</span><br>
                    <span style="font-size: 28px; font-weight: 700; color: {remaining_color}; text-shadow: 0 0 15px {remaining_color};">{afg(remaining)}</span><br>
                    <span style="font-size: 11px; color: #7FBAFF;">AFN</span>
                    <div style="font-size: 10px; margin-top: 5px; color: #4D9EFF;">
                        {'✅ تسویه شده' if remaining <= 0 else '⚠️ مانده حساب'}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # ========== سبد خرید موقت ==========
        if 'cart' not in st.session_state:
            st.session_state.cart = []
        
        # ========== تب‌های مالی ==========
        tab_inv, tab_pay, tab_hist, tab_srv = st.tabs([
            "➕ افزودن فاکتور جدید", 
            "💰 ثبت پرداخت جدید", 
            "📋 تاریخچه تراکنش‌ها", 
            "⚙️ مدیریت خدمات"
        ])
        
        # ===== تب 1: افزودن فاکتور =====
        with tab_inv:
            st.markdown("### 🛒 ثبت فاکتور جدید (فقط برای بخش مالی)")
            st.caption("این مبالغ به جمع کل اضافه خواهند شد")
            
            col_services, col_cart = st.columns([1, 1])
            
            with col_services:
                st.markdown("#### 📋 لیست خدمات")
                with get_connection() as conn:
                    services = pd.read_sql_query("SELECT service_name, default_price FROM dental_services ORDER BY service_name", conn)
                
                # نمایش خدمات در 2 ستون
                for i in range(0, len(services), 2):
                    col1, col2 = st.columns(2)
                    with col1:
                        if i < len(services):
                            s = services.iloc[i]
                            if st.button(f"**{s['service_name']}**\n\n{afg(s['default_price'])} AFN", key=f"srv_{i}", use_container_width=True):
                                st.session_state.cart.append({'name': s['service_name'], 'price': float(s['default_price'])})
                                st.rerun()
                    with col2:
                        if i + 1 < len(services):
                            s = services.iloc[i + 1]
                            if st.button(f"**{s['service_name']}**\n\n{afg(s['default_price'])} AFN", key=f"srv_{i+1}", use_container_width=True):
                                st.session_state.cart.append({'name': s['service_name'], 'price': float(s['default_price'])})
                                st.rerun()
            
            with col_cart:
                st.markdown("#### 🛒 سبد خرید جاری")
                if st.session_state.cart:
                    cart_total = 0
                    for i, item in enumerate(st.session_state.cart):
                        col_a, col_b, col_c = st.columns([3, 2, 1])
                        with col_a:
                            st.markdown(f"<span style='color: white;'>{item['name'][:20]}</span>", unsafe_allow_html=True)
                        with col_b:
                            st.markdown(f"<span style='color: #00C8FF;'>{afg(item['price'])} AFN</span>", unsafe_allow_html=True)
                        with col_c:
                            if st.button("✕", key=f"del_{i}"):
                                st.session_state.cart.pop(i)
                                st.rerun()
                        cart_total += item['price']
                    
                    st.markdown("<hr style='border-color: #00C8FF; opacity: 0.3;'>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div style='display: flex; justify-content: space-between;'>
                            <span style='color: #7FBAFF;'>جمع:</span>
                            <span style='color: #00C8FF; font-size: 18px; font-weight: 700;'>{afg(cart_total)} AFN</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("💾 ذخیره فاکتور", use_container_width=True, type="primary"):
                        with get_connection() as conn:
                            for item in st.session_state.cart:
                                conn.execute("""
                                    INSERT INTO patient_invoices (patient_id, service_name, unit_price)
                                    VALUES (?, ?, ?)
                                """, (p_id, item['name'], item['price']))
                            conn.commit()
                        
                        st.success(f"✅ {len(st.session_state.cart)} خدمت با موفقیت به فاکتورهای مالی اضافه شد")
                        st.session_state.cart = []
                        st.rerun()
                else:
                    st.info("🛒 سبد خرید خالی است")
                    st.caption("خدمات مورد نظر را از لیست سمت راست انتخاب کنید")
        
        # ===== تب 2: ثبت پرداخت =====
        with tab_pay:
            st.markdown("### 💰 ثبت پرداخت جدید (فقط برای بخش مالی)")
            st.caption("این مبالغ به جمع کل پرداختی‌ها اضافه خواهند شد")
            
            with st.form("payment_form"):
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    amount = st.number_input("مبلغ پرداخت (AFN)", min_value=0, step=100, value=0)
                with col_p2:
                    method = st.selectbox("روش پرداخت", ["نقدی", "کارت بانکی", "چک", "آنلاین", "سایر"])
                
                submitted = st.form_submit_button("✅ ثبت پرداخت", use_container_width=True, type="primary")
                
                if submitted and amount > 0:
                    with get_connection() as conn:
                        conn.execute("""
                            INSERT INTO patient_payments (patient_id, amount, payment_method)
                            VALUES (?, ?, ?)
                        """, (p_id, amount, method))
                        conn.commit()
                    
                    st.success(f"✅ پرداخت {afg(amount)} AFN با موفقیت ثبت شد")
                    st.rerun()
        
        # ===== تب 3: تاریخچه تراکنش‌ها =====
        with tab_hist:
            st.markdown("### 📋 تاریخچه کامل تراکنش‌های مالی")
            
            col_h1, col_h2 = st.columns(2)
            
            with col_h1:
                st.markdown("#### 📝 فاکتورهای ثبت شده")
                st.caption("شامل مبالغ از بخش عمومی و بخش مالی")
                
                # نمایش فاکتورهای عمومی (از جدول patients)
                if float(patient_financial['cost_from_general']) > 0:
                    appointment_date = patient['appointment_date'] if pd.notna(patient.get('appointment_date')) else '---'
                    st.markdown(f"""
                        <div style="background: rgba(0, 200, 255, 0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #00C8FF;">
                            <div style="display: flex; justify-content: space-between;">
                                <span style="color: white;">💰 مبلغ از بخش عمومی</span>
                                <span style="color: #00C8FF; font-weight: 600;">{afg(patient_financial['cost_from_general'])} AFN</span>
                            </div>
                            <div style="color: #7FBAFF; font-size: 12px; margin-top: 5px;">
                                📅 تاریخ ثبت: {appointment_date}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # نمایش فاکتورهای مالی
                if not all_invoices.empty:
                    for _, inv in all_invoices.iterrows():
                        inv_date = inv['invoice_date'][:16] if pd.notna(inv['invoice_date']) else '---'
                        st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #3498db;">
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: white;">{inv['service_name'][:30]}</span>
                                    <span style="color: #3498db; font-weight: 600;">{afg(inv['unit_price'])} AFN</span>
                                </div>
                                <div style="color: #7FBAFF; font-size: 11px; margin-top: 5px;">
                                    📅 {inv_date}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    if float(patient_financial['cost_from_general']) == 0:
                        st.info("هیچ فاکتوری ثبت نشده است")
            
            with col_h2:
                st.markdown("#### 💰 پرداخت‌های ثبت شده")
                st.caption("شامل مبالغ از بخش عمومی و بخش مالی")
                
                # نمایش پرداخت‌های عمومی (از جدول patients)
                if float(patient_financial['paid_from_general']) > 0:
                    st.markdown(f"""
                        <div style="background: rgba(46, 204, 113, 0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #2ecc71;">
                            <div style="display: flex; justify-content: space-between;">
                                <span style="color: white;">💰 پرداخت از بخش عمومی</span>
                                <span style="color: #2ecc71; font-weight: 600;">{afg(patient_financial['paid_from_general'])} AFN</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # نمایش پرداخت‌های مالی
                if not all_payments.empty:
                    for _, pay in all_payments.iterrows():
                        pay_date = pay['payment_date'][:16] if pd.notna(pay['payment_date']) else '---'
                        st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #2ecc71;">
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: white;">{pay['payment_method']}</span>
                                    <span style="color: #2ecc71; font-weight: 600;">{afg(pay['amount'])} AFN</span>
                                </div>
                                <div style="color: #7FBAFF; font-size: 11px; margin-top: 5px;">
                                    📅 {pay_date}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    if float(patient_financial['paid_from_general']) == 0:
                        st.info("هیچ پرداختی ثبت نشده است")
        
        # ===== تب 4: مدیریت خدمات =====
        with tab_srv:
            st.markdown("### ⚙️ مدیریت لیست خدمات دندانپزشکی")
            
            tab_add, tab_edit, tab_del = st.tabs(["➕ سرویس جدید", "✏️ ویرایش قیمت", "🗑️ حذف سرویس"])
            
            with tab_add:
                with st.form("add_service_form"):
                    col_a1, col_a2, col_a3 = st.columns([3, 2, 1])
                    with col_a1:
                        new_name = st.text_input("نام سرویس", placeholder="مثلاً: لمینت دندان", label_visibility="collapsed")
                    with col_a2:
                        new_price = st.number_input("قیمت", min_value=0, step=100, value=0, label_visibility="collapsed", placeholder="قیمت (AFN)")
                    with col_a3:
                        if st.form_submit_button("➕ افزودن", use_container_width=True) and new_name and new_price > 0:
                            with get_connection() as conn:
                                try:
                                    conn.execute("INSERT INTO dental_services (service_name, default_price) VALUES (?, ?)", (new_name, new_price))
                                    conn.commit()
                                    st.success(f"✅ سرویس {new_name} اضافه شد")
                                    st.rerun()
                                except:
                                    st.warning("⚠️ این سرویس قبلاً ثبت شده است")
            
            with tab_edit:
                with get_connection() as conn:
                    services_edit = pd.read_sql_query("SELECT service_name, default_price FROM dental_services ORDER BY service_name", conn)
                
                if not services_edit.empty:
                    with st.form("edit_service_form"):
                        col_e1, col_e2, col_e3 = st.columns([3, 2, 1])
                        with col_e1:
                            selected = st.selectbox("انتخاب سرویس", services_edit['service_name'].tolist(), label_visibility="collapsed")
                        with col_e2:
                            current_price = services_edit[services_edit['service_name'] == selected]['default_price'].iloc[0]
                            new_price = st.number_input("قیمت جدید", min_value=0, value=int(current_price), step=100, label_visibility="collapsed")
                        with col_e3:
                            if st.form_submit_button("✏️ ویرایش", use_container_width=True):
                                with get_connection() as conn:
                                    conn.execute("UPDATE dental_services SET default_price = ? WHERE service_name = ?", (new_price, selected))
                                    conn.commit()
                                st.success(f"✅ قیمت {selected} به {afg(new_price)} AFN تغییر کرد")
                                st.rerun()
            
            with tab_del:
                with get_connection() as conn:
                    services_del = pd.read_sql_query("SELECT service_name FROM dental_services ORDER BY service_name", conn)
                
                if not services_del.empty:
                    with st.form("delete_service_form"):
                        col_d1, col_d2 = st.columns([4, 1])
                        with col_d1:
                            selected_del = st.selectbox("انتخاب سرویس برای حذف", services_del['service_name'].tolist(), label_visibility="collapsed")
                        with col_d2:
                            if st.form_submit_button("🗑️ حذف", use_container_width=True):
                                with get_connection() as conn:
                                    conn.execute("DELETE FROM dental_services WHERE service_name = ?", (selected_del,))
                                    conn.commit()
                                st.success(f"✅ سرویس {selected_del} حذف شد")
                                st.rerun()
        
        # ========== خلاصه نهایی ==========
        st.divider()
        st.markdown("### 📊 خلاصه یکپارچه مالی")
        
        col_sum1, col_sum2 = st.columns(2)
        
        with col_sum1:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0A0F1F, #0E1629);
                            padding: 20px;
                            border-radius: 15px;
                            border: 2px solid #00C8FF;">
                    <h4 style="color: white; margin: 0 0 15px 0;">منابع مالی:</h4>
                    <table style="width: 100%; color: white;">
                        <tr>
                            <td>💰 از بخش عمومی (هزینه):</td>
                            <td style="text-align: left; color: #00C8FF;">{afg(patient_financial['cost_from_general'])} AFN</td>
                        </tr>
                        <tr>
                            <td>➕ از بخش مالی (فاکتورها):</td>
                            <td style="text-align: left; color: #00C8FF;">{afg(invoices_from_financial)} AFN</td>
                        </tr>
                        <tr style="border-top: 1px solid #00C8FF;">
                            <td><strong>جمع کل فاکتورها:</strong></td>
                            <td style="text-align: left; color: #00C8FF; font-weight: 700;">{afg(total_invoices)} AFN</td>
                        </tr>
                    </table>
                </div>
            """, unsafe_allow_html=True)
        
        with col_sum2:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0A0F1F, #0E1629);
                            padding: 20px;
                            border-radius: 15px;
                            border: 2px solid #2ecc71;">
                    <h4 style="color: white; margin: 0 0 15px 0;">منابع پرداخت:</h4>
                    <table style="width: 100%; color: white;">
                        <tr>
                            <td>💰 از بخش عمومی (پرداخت):</td>
                            <td style="text-align: left; color: #2ecc71;">{afg(patient_financial['paid_from_general'])} AFN</td>
                        </tr>
                        <tr>
                            <td>➕ از بخش مالی (پرداخت‌ها):</td>
                            <td style="text-align: left; color: #2ecc71;">{afg(payments_from_financial)} AFN</td>
                        </tr>
                        <tr>
                            <td>🎯 تخفیف:</td>
                            <td style="text-align: left; color: #f39c12;">{afg(total_discount)} AFN</td>
                        </tr>
                        <tr style="border-top: 1px solid #2ecc71;">
                            <td><strong>باقی‌مانده نهایی:</strong></td>
                            <td style="text-align: left; color: {'#2ecc71' if remaining <= 0 else '#e74c3c'}; font-weight: 700;">{afg(remaining)} AFN</td>
                        </tr>
                    </table>
                </div>
            """, unsafe_allow_html=True)









    # ===== Tab 6: Comprehensive Integrated Reporting with HTML Download =====
    with tab6:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #2C3E50, #1A5276);
                        padding: 30px 25px;
                        border-radius: 20px;
                        margin-bottom: 30px;
                        box-shadow: 0 10px 20px rgba(0,0,0,0.2);">
                <h1 style="color: white; text-align: center; margin: 0; font-size: 36px; font-weight: 700;">
                    📋 Smart Integrated Reporting
                </h1>
                <p style="color: #AED6F1; text-align: center; margin: 15px 0 0 0; font-size: 18px;">
                    Collect and display all patient information in a complete HTML report
                </p>
            </div>
        """, unsafe_allow_html=True)

        # ===== Get complete information from all databases =====
        with get_connection() as conn:
            # Basic patient information
            patient_full = pd.read_sql_query(f"SELECT * FROM patients WHERE id = {p_id}", conn).iloc[0]
            
            # Health questionnaire history
            medical_history_all = pd.read_sql_query(f"""
                SELECT * FROM emr_records 
                WHERE patient_id = {p_id} 
                ORDER BY created_at DESC LIMIT 1
            """, conn)
            
            # All teeth with latest status
            dental_full = pd.read_sql_query(f"""
                SELECT tooth_number, tooth_status, notes, is_treatment, date_updated
                FROM dental_charting 
                WHERE patient_id = {p_id} 
                GROUP BY tooth_number
                HAVING MAX(date_updated)
                ORDER BY tooth_number
            """, conn)
            
            # All invoices and payments
            invoices_full = pd.read_sql_query(f"""
                SELECT * FROM patient_invoices 
                WHERE patient_id = {p_id} 
                ORDER BY invoice_date DESC
            """, conn)
            
            payments_full = pd.read_sql_query(f"""
                SELECT * FROM patient_payments 
                WHERE patient_id = {p_id} 
                ORDER BY payment_date DESC
            """, conn)
            
            # All files and documents
            files_full = pd.read_sql_query(f"""
                SELECT * FROM patient_files 
                WHERE patient_id = {p_id} 
                ORDER BY uploaded_at DESC
            """, conn)

        # ===== Process medical information =====
        if not medical_history_all.empty:
            latest_medical = medical_history_all.iloc[0]
            import ast
            try:
                medical_dict = ast.literal_eval(latest_medical['medical_history']) if pd.notna(latest_medical['medical_history']) else {}
            except:
                medical_dict = {}
            allergies_text = latest_medical['allergies'] if pd.notna(latest_medical['allergies']) and latest_medical['allergies'] else 'Not recorded'
            medications_text = latest_medical['current_medications'] if pd.notna(latest_medical['current_medications']) and latest_medical['current_medications'] else 'No medications recorded'
            last_medical_date = latest_medical['created_at'][:16] if pd.notna(latest_medical['created_at']) else '---'
        else:
            medical_dict = {}
            allergies_text = 'Not recorded'
            medications_text = 'No medications recorded'
            last_medical_date = '---'

        # ===== Financial calculations =====
        total_invoices = float(patient_full['cost']) + (invoices_full['unit_price'].sum() if not invoices_full.empty else 0)
        total_payments = float(patient_full['paid_amount']) + (payments_full['amount'].sum() if not payments_full.empty else 0)
        total_discount = float(patient_full['discount'])
        remaining = total_invoices - total_payments - total_discount

        # ===== Dental statistics =====
        tooth_status_counts = dental_full['tooth_status'].value_counts().to_dict() if not dental_full.empty else {}
        treatment_count = len(dental_full[dental_full['is_treatment'] == 1]) if not dental_full.empty else 0
        missing_count = tooth_status_counts.get('Missing', 0)
        filled_count = sum(tooth_status_counts.get(s, 0) for s in ['Filled', 'RCT', 'Crown', 'Bridge'])
        
        # ===== File statistics =====
        total_files = len(files_full)
        file_types = files_full['file_type'].value_counts().to_dict() if not files_full.empty else {}

        # ===== Disease translation dictionary (English version) =====
        diseases_en = {
            'heart_disease': 'Heart Disease', 
            'hypertension': 'Hypertension', 
            'diabetes': 'Diabetes',
            'asthma': 'Asthma', 
            'kidney': 'Kidney Disease', 
            'liver': 'Liver Disease',
            'cancer': 'Cancer History', 
            'epilepsy': 'Epilepsy', 
            'pregnancy': 'Pregnancy',
            'heart_surgery': 'Heart Surgery',
            'arrhythmia': 'Arrhythmia',
            'stroke': 'Stroke',
            'cholesterol': 'High Cholesterol',
            'thyroid': 'Thyroid Problems',
            'copd': 'COPD',
            'tb': 'Tuberculosis',
            'sleep_apnea': 'Sleep Apnea',
            'hepatitis': 'Hepatitis',
            'autoimmune': 'Autoimmune Disease',
            'drug_use': 'Drug Use',
            'smoking': 'Smoking',
            'alcohol': 'Alcohol'
        }

        # ===== Main report buttons =====
        col_report1, col_report2, col_report3 = st.columns(3)
        
        with col_report1:
            report_type = st.selectbox(
                "📋 Report Type",
                ["Complete Integrated Report", "Medical Summary", "Financial Report", "Dental Status", "Documents List"],
                index=0
            )
        
        with col_report2:
            include_sections = st.multiselect(
                "✅ Sections to Include",
                ["Basic Info", "Medical", "Dental", "Financial", "Documents"],
                default=["Basic Info", "Medical", "Dental", "Financial", "Documents"]
            )
        
        with col_report3:
            report_style = st.radio(
                "🎨 Report Style",
                ["Professional (Blue)", "Classic (Gold)", "Minimal (Gray)"],
                horizontal=True
            )

        # ===== Generate HTML Report =====
        def generate_html_report():
            # Determine colors based on selected style
            if report_style == "Professional (Blue)":
                primary_color = "#1A5276"
                secondary_color = "#3498DB"
                accent_color = "#F39C12"
                bg_light = "#F8F9FA"
                text_dark = "#2C3E50"
            elif report_style == "Classic (Gold)":
                primary_color = "#B8860B"
                secondary_color = "#DAA520"
                accent_color = "#8B4513"
                bg_light = "#FFF9E6"
                text_dark = "#4A4A4A"
            else:  # Minimal
                primary_color = "#2C3E50"
                secondary_color = "#7F8C8D"
                accent_color = "#E67E22"
                bg_light = "#ECF0F1"
                text_dark = "#2C3E50"

            # Start HTML
            html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Patient Comprehensive Report - Osman Muslim Dental Clinic</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Inter', sans-serif;
            }}
            
            body {{
                background: {bg_light};
                padding: 40px 20px;
            }}
            
            .report-container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            
            .report-header {{
                background: linear-gradient(135deg, {primary_color}, {secondary_color});
                padding: 40px 50px;
                color: white;
                position: relative;
            }}
            
            .report-header::after {{
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 5px;
                background: {accent_color};
            }}
            
            .clinic-name {{
                font-size: 28px;
                font-weight: 800;
                margin-bottom: 5px;
            }}
            
            .report-title {{
                font-size: 22px;
                font-weight: 500;
                opacity: 0.9;
                margin-bottom: 20px;
            }}
            
            .patient-badge {{
                background: rgba(255,255,255,0.15);
                padding: 20px 25px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                margin-top: 20px;
            }}
            
            .badge-item {{
                display: inline-block;
                margin-right: 30px;
            }}
            
            .badge-label {{
                font-size: 14px;
                opacity: 0.8;
                margin-bottom: 5px;
            }}
            
            .badge-value {{
                font-size: 18px;
                font-weight: 700;
            }}
            
            .report-content {{
                padding: 40px 50px;
            }}
            
            .section {{
                margin-bottom: 40px;
                border-bottom: 2px solid {bg_light};
                padding-bottom: 30px;
            }}
            
            .section:last-child {{
                border-bottom: none;
            }}
            
            .section-title {{
                font-size: 24px;
                font-weight: 700;
                color: {primary_color};
                margin-bottom: 25px;
                position: relative;
                padding-left: 20px;
            }}
            
            .section-title::before {{
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 6px;
                background: {accent_color};
                border-radius: 3px;
            }}
            
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }}
            
            .info-card {{
                background: {bg_light};
                padding: 20px;
                border-radius: 15px;
                border-left: 4px solid {secondary_color};
            }}
            
            .info-label {{
                font-size: 14px;
                color: {text_dark};
                opacity: 0.7;
                margin-bottom: 8px;
            }}
            
            .info-value {{
                font-size: 18px;
                font-weight: 700;
                color: {primary_color};
            }}
            
            .warning-box {{
                background: #FEF9E7;
                border-left: 6px solid #F39C12;
                padding: 20px 25px;
                border-radius: 15px;
                margin-bottom: 25px;
            }}
            
            .warning-title {{
                color: #B03A2E;
                font-weight: 700;
                font-size: 18px;
                margin-bottom: 8px;
            }}
            
            .tooth-grid {{
                display: grid;
                grid-template-columns: repeat(8, 1fr);
                gap: 8px;
                margin: 20px 0;
            }}
            
            .tooth-item {{
                background: white;
                border: 2px solid {secondary_color};
                border-radius: 10px;
                padding: 8px;
                text-align: center;
                font-weight: 700;
                font-size: 14px;
                transition: all 0.3s;
            }}
            
            .tooth-item.normal {{ border-color: #27AE60; background: #E8F6F3; }}
            .tooth-item.problem {{ border-color: #E74C3C; background: #FDEDEC; }}
            .tooth-item.treated {{ border-color: #3498DB; background: #EBF5FB; }}
            .tooth-item.missing {{ border-color: #7F8C8D; background: #F2F3F4; }}
            .tooth-item.treatment {{ border-color: #E74C3C; background: #FDEDEC; border-width: 3px; }}
            
            .financial-stats {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
                margin-bottom: 30px;
            }}
            
            .stat-card {{
                background: {primary_color};
                color: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
            }}
            
            .stat-label {{
                font-size: 14px;
                opacity: 0.8;
                margin-bottom: 8px;
            }}
            
            .stat-value {{
                font-size: 24px;
                font-weight: 700;
            }}
            
            .stat-unit {{
                font-size: 12px;
                opacity: 0.7;
                margin-top: 5px;
            }}
            
            .table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            
            .table th {{
                background: {primary_color};
                color: white;
                padding: 12px;
                font-weight: 500;
                text-align: center;
            }}
            
            .table td {{
                padding: 12px;
                border-bottom: 1px solid {bg_light};
                text-align: center;
            }}
            
            .table tr:nth-child(even) {{
                background: {bg_light};
            }}
            
            .footer {{
                background: {primary_color};
                color: white;
                padding: 30px 50px;
                text-align: center;
                margin-top: 30px;
            }}
            
            .footer-text {{
                opacity: 0.8;
                font-size: 14px;
                margin-top: 10px;
            }}
            
            .signature {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 2px dashed {accent_color};
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            @media print {{
                body {{
                    background: white;
                    padding: 0;
                }}
                .report-container {{
                    box-shadow: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="report-container">
            <div class="report-header">
                <div class="clinic-name">🦷 Osman Muslim Dental Clinic</div>
                <div class="report-title">{report_type} | Date: {datetime.now().strftime('%Y/%m/%d - %H:%M')}</div>
                
                <div class="patient-badge">
                    <div class="badge-item">
                        <div class="badge-label">Patient Name</div>
                        <div class="badge-value">{patient_full['first_name']} {patient_full['last_name']}</div>
                    </div>
                    <div class="badge-item">
                        <div class="badge-label">Patient ID</div>
                        <div class="badge-value">#{patient_full['id']}</div>
                    </div>
                    <div class="badge-item">
                        <div class="badge-label">Age / Gender</div>
                        <div class="badge-value">{patient_full['age']} years / {'Male' if str(patient_full['gender']).lower() in ['male', 'مرد'] else 'Female'}</div>
                    </div>
                    <div class="badge-item">
                        <div class="badge-label">Phone</div>
                        <div class="badge-value">{patient_full['phone'] if pd.notna(patient_full['phone']) else '---'}</div>
                    </div>
                </div>
            </div>
            
            <div class="report-content">
    """

            # ===== Section 1: Basic Information =====
            if "Basic Info" in include_sections:
                html += f"""
                <div class="section">
                    <div class="section-title">📋 Basic Information & Contact</div>
                    <div class="info-grid">
                        <div class="info-card">
                            <div class="info-label">Full Name</div>
                            <div class="info-value">{patient_full['first_name']} {patient_full['last_name']}</div>
                        </div>
                        <div class="info-card">
                            <div class="info-label">National ID</div>
                            <div class="info-value">{patient_full['national_id']}</div>
                        </div>
                        <div class="info-card">
                            <div class="info-label">Age</div>
                            <div class="info-value">{patient_full['age']} years</div>
                        </div>
                        <div class="info-card">
                            <div class="info-label">Phone Number</div>
                            <div class="info-value">{patient_full['phone'] if pd.notna(patient_full['phone']) else '---'}</div>
                        </div>
                        <div class="info-card">
                            <div class="info-label">Next Visit</div>
                            <div class="info-value">{patient_full['next_visit_date'] if pd.notna(patient_full['next_visit_date']) else '---'} at {patient_full['next_visit_time'] if pd.notna(patient_full['next_visit_time']) else '---'}</div>
                        </div>
                    </div>
                </div>
    """

            # ===== Section 2: Medical Information =====
            if "Medical" in include_sections:
                html += f"""
                <div class="section">
                    <div class="section-title">🏥 Health Questionnaire</div>
    """

                if allergies_text not in ['Not recorded', ''] and allergies_text != 'No medications recorded':
                    html += f"""
                    <div class="warning-box">
                        <div class="warning-title">⚠️ Allergy Warning</div>
                        <p>{allergies_text}</p>
                    </div>
    """

                html += f"""
                    <div class="info-grid">
                        <div class="info-card">
                            <div class="info-label">Allergies</div>
                            <div class="info-value">{allergies_text}</div>
                        </div>
                        <div class="info-card">
                            <div class="info-label">Current Medications</div>
                            <div class="info-value">{medications_text}</div>
                        </div>
                        <div class="info-card">
                            <div class="info-label">Last Updated</div>
                            <div class="info-value">{last_medical_date}</div>
                        </div>
                    </div>
    """

                if medical_dict:
                    active_diseases = []
                    
                    for key, value in medical_dict.items():
                        if value and key in diseases_en and value not in [False, 'None', '']:
                            if key in ['smoking', 'alcohol']:
                                active_diseases.append(f"{diseases_en[key]}: {value}")
                            else:
                                active_diseases.append(diseases_en[key])
                    
                    if active_diseases:
                        html += """
                        <div style="margin-top: 20px;">
                            <div style="font-weight: 700; margin-bottom: 10px;">Active Conditions:</div>
                            <div style="display: flex; flex-wrap: wrap; gap: 10px;">"""
                        
                        for disease in active_diseases[:8]:  # Limit to 8
                            html += f'<span style="background: {bg_light}; padding: 8px 15px; border-radius: 20px;">{disease}</span>'
                        
                        html += "</div></div>"
                
                html += "</div>"

            # ===== Section 3: Dental Status =====
            if "Dental" in include_sections:
                html += f"""
                <div class="section">
                    <div class="section-title">🦷 Dental Chart & Status</div>
                    
                    <div class="info-grid" style="grid-template-columns: repeat(4, 1fr);">
                        <div class="stat-card" style="background: {primary_color};">
                            <div class="stat-label">Total Recorded</div>
                            <div class="stat-value">{len(dental_full)}</div>
                        </div>
                        <div class="stat-card" style="background: #E74C3C;">
                            <div class="stat-label">In Treatment</div>
                            <div class="stat-value">{treatment_count}</div>
                        </div>
                        <div class="stat-card" style="background: #27AE60;">
                            <div class="stat-label">Treated</div>
                            <div class="stat-value">{filled_count}</div>
                        </div>
                        <div class="stat-card" style="background: #7F8C8D;">
                            <div class="stat-label">Missing</div>
                            <div class="stat-value">{missing_count}</div>
                        </div>
                    </div>

                    <div style="margin: 30px 0;">
                        <h4 style="margin-bottom: 15px;">🔹 Upper Jaw</h4>
                        <div class="tooth-grid">
    """

                # Upper jaw (teeth 1-16)
                for i in range(16):
                    tooth_num = i + 1
                    tooth_row = dental_full[dental_full['tooth_number'] == tooth_num]
                    if not tooth_row.empty:
                        status = tooth_row.iloc[0]['tooth_status']
                        is_treatment = tooth_row.iloc[0]['is_treatment']
                        if is_treatment:
                            tooth_class = "treatment"
                        elif status == "Missing":
                            tooth_class = "missing"
                        elif status in ["Caries", "RCT Needed", "Fractured", "Discolored"]:
                            tooth_class = "problem"
                        elif status in ["Filled", "RCT", "Crown", "Bridge"]:
                            tooth_class = "treated"
                        else:
                            tooth_class = "normal"
                    else:
                        tooth_class = ""
                    
                    html += f'<div class="tooth-item {tooth_class}">{tooth_num}</div>'

                html += """
                        </div>
                        
                        <h4 style="margin: 20px 0 15px;">🔸 Lower Jaw</h4>
                        <div class="tooth-grid">
    """

                # Lower jaw (teeth 17-32)
                for i in range(16):
                    tooth_num = i + 17
                    tooth_row = dental_full[dental_full['tooth_number'] == tooth_num]
                    if not tooth_row.empty:
                        status = tooth_row.iloc[0]['tooth_status']
                        is_treatment = tooth_row.iloc[0]['is_treatment']
                        if is_treatment:
                            tooth_class = "treatment"
                        elif status == "Missing":
                            tooth_class = "missing"
                        elif status in ["Caries", "RCT Needed", "Fractured", "Discolored"]:
                            tooth_class = "problem"
                        elif status in ["Filled", "RCT", "Crown", "Bridge"]:
                            tooth_class = "treated"
                        else:
                            tooth_class = "normal"
                    else:
                        tooth_class = ""
                    
                    html += f'<div class="tooth-item {tooth_class}">{tooth_num}</div>'

                html += """
                        </div>
                        
                        <div style="display: flex; gap: 20px; margin-top: 20px; flex-wrap: wrap;">
                            <span><span style="display: inline-block; width: 15px; height: 15px; background: #27AE60; border-radius: 3px;"></span> Normal</span>
                            <span><span style="display: inline-block; width: 15px; height: 15px; background: #E74C3C; border-radius: 3px;"></span> Problem</span>
                            <span><span style="display: inline-block; width: 15px; height: 15px; background: #3498DB; border-radius: 3px;"></span> Treated</span>
                            <span><span style="display: inline-block; width: 15px; height: 15px; background: #7F8C8D; border-radius: 3px;"></span> Missing</span>
                            <span><span style="display: inline-block; width: 15px; height: 15px; background: #E74C3C; border-radius: 3px; border: 2px solid #C0392B;"></span> Current Treatment</span>
                        </div>
                    </div>
    """

                if not dental_full.empty:
                    html += """
                    <h4 style="margin: 20px 0;">📋 Tooth Details</h4>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Number</th>
                                <th>Status</th>
                                <th>Notes</th>
                                <th>Current Treatment</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
    """
                    for _, tooth in dental_full.iterrows():
                        status_english = tooth['tooth_status']
                        treatment_status = "🔴 Yes" if tooth['is_treatment'] == 1 else "✅ No"
                        note = tooth['notes'] if pd.notna(tooth['notes']) else '-'
                        date = tooth['date_updated'][:10] if pd.notna(tooth['date_updated']) else '-'
                        
                        html += f"""
                            <tr>
                                <td><strong>{int(tooth['tooth_number'])}</strong></td>
                                <td>{status_english}</td>
                                <td>{note}</td>
                                <td>{treatment_status}</td>
                                <td>{date}</td>
                            </tr>
    """
                    html += """
                        </tbody>
                    </table>
    """
                html += "</div>"

            # ===== Section 4: Financial Information =====
            if "Financial" in include_sections:
                html += f"""
                <div class="section">
                    <div class="section-title">💰 Financial Statement</div>
                    
                    <div class="financial-stats">
                        <div class="stat-card" style="background: {primary_color};">
                            <div class="stat-label">Total Invoices</div>
                            <div class="stat-value">{total_invoices:,.0f}</div>
                            <div class="stat-unit">AFN</div>
                        </div>
                        <div class="stat-card" style="background: #27AE60;">
                            <div class="stat-label">Paid Amount</div>
                            <div class="stat-value">{total_payments:,.0f}</div>
                            <div class="stat-unit">AFN</div>
                        </div>
                        <div class="stat-card" style="background: #F39C12;">
                            <div class="stat-label">Discount</div>
                            <div class="stat-value">{total_discount:,.0f}</div>
                            <div class="stat-unit">AFN</div>
                        </div>
                        <div class="stat-card" style="background: {'#27AE60' if remaining <= 0 else '#E74C3C'};">
                            <div class="stat-label">Balance</div>
                            <div class="stat-value">{remaining:,.0f}</div>
                            <div class="stat-unit">AFN</div>
                        </div>
                    </div>

                    <div class="info-grid" style="grid-template-columns: 1fr 1fr;">
                        <div>
                            <h4 style="margin-bottom: 15px;">📋 Recent Invoices</h4>
    """

                if not invoices_full.empty:
                    html += '<table class="table"><thead><tr><th>Service</th><th>Amount</th><th>Date</th></tr></thead><tbody>'
                    for _, inv in invoices_full.head(5).iterrows():
                        html += f'<tr><td>{inv["service_name"][:20]}</td><td>{inv["unit_price"]:,.0f}</td><td>{str(inv["invoice_date"])[:10]}</td></tr>'
                    html += '</tbody></table>'
                else:
                    html += '<p>No invoices recorded</p>'

                html += """
                        </div>
                        <div>
                            <h4 style="margin-bottom: 15px;">💰 Recent Payments</h4>
    """

                if not payments_full.empty:
                    html += '<table class="table"><thead><tr><th>Method</th><th>Amount</th><th>Date</th></tr></thead><tbody>'
                    for _, pay in payments_full.head(5).iterrows():
                        html += f'<tr><td>{pay["payment_method"] if pd.notna(pay["payment_method"]) else "---"}</td><td>{pay["amount"]:,.0f}</td><td>{str(pay["payment_date"])[:10]}</td></tr>'
                    html += '</tbody></table>'
                else:
                    html += '<p>No payments recorded</p>'

                html += """
                        </div>
                    </div>
                </div>
    """

            # ===== Section 5: Documents and Files =====
            if "Documents" in include_sections:
                html += f"""
                <div class="section">
                    <div class="section-title">📁 Documents & Images</div>
                    
                    <div class="info-grid" style="grid-template-columns: repeat(3, 1fr);">
                        <div class="stat-card" style="background: {secondary_color};">
                            <div class="stat-label">Total Files</div>
                            <div class="stat-value">{total_files}</div>
                        </div>
                        <div class="stat-card" style="background: {accent_color};">
                            <div class="stat-label">File Types</div>
                            <div class="stat-value">{len(file_types)}</div>
                        </div>
                        <div class="stat-card" style="background: {primary_color};">
                            <div class="stat-label">Last Upload</div>
                            <div class="stat-value">{files_full.iloc[0]['uploaded_at'][:10] if not files_full.empty else '---'}</div>
                        </div>
                    </div>
    """

                if not files_full.empty:
                    html += """
                    <table class="table">
                        <thead>
                            <tr>
                                <th>File Name</th>
                                <th>Type</th>
                                <th>Description</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
    """
                    for _, file_row in files_full.head(5).iterrows():
                        html += f"""
                            <tr>
                                <td>{file_row['file_name'][:30]}{'...' if len(file_row['file_name']) > 30 else ''}</td>
                                <td>{file_row['file_type']}</td>
                                <td>{file_row['description'] if pd.notna(file_row['description']) else '-'}</td>
                                <td>{file_row['uploaded_at'][:10]}</td>
                            </tr>
    """
                    html += """
                        </tbody>
                    </table>
    """
                else:
                    html += '<p>No files uploaded.</p>'

                html += "</div>"

            # ===== Signature Section =====
            html += f"""
                <div class="signature">
                    <div style="text-align: center; width: 100%;">
                        <div style="font-weight: 700; margin-bottom: 5px; color: {primary_color};">Seal & Signature</div>
                        <div style="font-size: 20px; font-weight: 700; color: {accent_color};">Osman Muslim Clinic</div>
                        <div style="margin-top: 10px; width: 200px; height: 2px; background: linear-gradient(90deg, transparent, {accent_color}, transparent); margin: 10px auto;"></div>
                        <div style="display: flex; justify-content: center; gap: 30px; margin-top: 10px;">
                            <div>
                                <div style="font-size: 12px; color: {text_dark};">Print Date</div>
                                <div style="font-weight: 500;">{datetime.now().strftime('%Y/%m/%d')}</div>
                            </div>
                            <div>
                                <div style="font-size: 12px; color: {text_dark};">Report Code</div>
                                <div style="font-weight: 500;">GR-{datetime.now().strftime('%Y%m%d')}-{patient_full['id']}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <div>🦷 Osman Muslim Dental Clinic - Electronic Health Record System</div>
                <div class="footer-text">This report is automatically generated by the EHR system</div>
            </div>
        </div>
    </body>
    </html>"""
            
            return html

        # ===== Display Report Preview =====
        st.markdown("""
            <div style="background: linear-gradient(145deg, #2C3E50, #1E2B38); 
                        padding: 15px 20px; 
                        border-radius: 12px; 
                        margin: 30px 0 20px;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 24px; margin-right: 10px;">👁️</span>
                        <span style="color: white; font-size: 20px; font-weight: bold;">Report Preview</span>
                    </div>
                    <span style="color: #AED6F1; font-size: 14px;">Report Type: {report_type}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Generate HTML
        html_content = generate_html_report()

        # Action buttons
        col_download, col_print, col_refresh = st.columns(3)

        with col_download:
            # Filename based on report type
            filename = f"report_{patient_full['first_name']}_{patient_full['last_name']}_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
            
            st.download_button(
                label="📥 Download HTML Report",
                data=html_content,
                file_name=filename,
                mime="text/html",
                use_container_width=True,
                type="primary"
            )

        with col_print:
            if st.button("🖨️ Print Report", use_container_width=True):
                # Save temporary file for printing
                temp_file = f"temp_report_{patient_full['id']}.html"
                with open(temp_file, "w", encoding="utf-8") as f:
                    f.write(html_content)
                
                # Create temporary download link
                with open(temp_file, "rb") as f:
                    temp_content = f.read()
                
                st.download_button(
                    label="📄 Download and Open for Printing",
                    data=temp_content,
                    file_name=f"print_{filename}",
                    mime="text/html",
                    use_container_width=True,
                    key="print_btn"
                )
                
                st.info("""
                    **Printing Instructions:**
                    1. Download the HTML file
                    2. Open the file in your browser
                    3. Press Ctrl+P (Windows) or Cmd+P (Mac)
                    4. Adjust print settings and print
                """)

        with col_refresh:
            if st.button("🔄 Refresh Report", use_container_width=True):
                st.rerun()

        # Display HTML preview in an iframe
       
   