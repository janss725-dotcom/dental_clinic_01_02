import os
import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
from modules.database import get_connection

def render_dashboard():
    # =========================================================================
    # دکمه تغییر زبان (نسخه مینیاتوری و تمیز)
    # =========================================================================
    
    # ۱. مدیریت وضعیت زبان
    if 'dashboard_language' not in st.session_state:
        st.session_state.dashboard_language = "dr"

    # ۲. استایل دکمه
    st.markdown("""
    <style>
    /* استایل دکمه تغییر زبان - نسخه مینیاتوری و تمیز */
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

    /* کارت‌های متریک */
    [data-testid="stMetric"] {
        background: #1A233A;
        border: 1px solid rgba(0, 200, 255, 0.2);
        padding: 15px 20px;
        border-radius: 15px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #7FBAFF !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ۳. دکمه واقعی
    current_lang = st.session_state.dashboard_language
    label = "Switch to English 🇬🇧" if current_lang == "dr" else "تغییر به دری 🇦🇫"
    
    if st.button(label):
        st.session_state.dashboard_language = "en" if current_lang == "dr" else "dr"
        st.rerun()
    
    # =========================================================================
    # دیکشنری ترجمه
    # =========================================================================
    translations = {
        "dr": {
            "dashboard_title": "داشبورد مدیریت کلینیک",
            "dashboard_subtitle": "نمایش لحظه‌ای آمار و مدیریت بیماران",
            "kpi_title": "📈 شاخص‌های کلیدی عملکرد",
            "total_patients": "تعداد بیماران",
            "total_revenue": "درآمد کل (AFN)",
            "total_paid": "پرداختی کل (AFN)",
            "balance": "مانده حساب (AFN)",
            "settled": "تسویه شده ✓",
            "outstanding": "مانده حساب",
            "analytics_title": "📊 آمار مالی و بیماران",
            "select_year": "📅 انتخاب سال",
            "chart_type": "📊 نوع نمودار",
            "line_chart": "نمودار خطی",
            "bar_chart": "نمودار ستونی",
            "area_chart": "نمودار منطقه‌ای",
            "period": "📆 بازه زمانی",
            "monthly": "ماهانه",
            "quarterly": "فصلی",
            "total_revenue_label": "💰 درآمد کل (AFN)",
            "revenue_note": "شامل: هزینه بیماران + فاکتورهای مالی",
            "patient_count_label": "👥 تعداد بیماران",
            "patient_note": "بر اساس نوبت‌های بیماران",
            "revenue_details": "💰 جزئیات درآمد",
            "year": "سال",
            "total_revenue_year": "کل درآمد",
            "total_patients_year": "تعداد بیماران",
            "avg_per_patient": "میانگین به ازای هر بیمار",
            "monthly_avg": "میانگین ماهانه (AFN)",
            "monthly_revenue": "📆 درآمد ماهانه",
            "select_month": "انتخاب ماه",
            "patients_count": "تعداد بیماران",
            "average": "میانگین",
            "daily_revenue": "📅 درآمد روزانه",
            "select_date": "انتخاب تاریخ",
            "patient_list": "لیست بیماران در تاریخ",
            "patient": "بیمار",
            "top_services": "🔝 خدمات پرطرفدار",
            "total_services": "مجموع خدمات ثبت شده",
            "no_service_data": "ℹ️ اطلاعات خدمات در دسترس نیست",
            "no_data": "ℹ️ اطلاعاتی برای نمایش وجود ندارد",
            "today_appointments": "🗓 نوبت‌های امروز",
            "no_appointment": "📭 امروز هیچ نوبتی ثبت نشده است",
            "waiting": "در انتظار",
            "attendance_title": "🕒 ثبت ورود و خروج پرسنل",
            "check_in": "✅ ثبت ورود",
            "check_out": "🔚 ثبت خروج",
            "already_checked_in": "⚠️ شما قبلاً امروز ورود خود را ثبت کرده‌اید",
            "already_checked_out": "⚠️ شما قبلاً امروز خروج خود را ثبت کرده‌اید",
            "first_check_in": "⚠️ ابتدا باید ورود خود را ثبت کنید",
            "checkout_time_limit": "⏰ ثبت خروج فقط از ساعت {time} به بعد امکان‌پذیر است",
            "checkout_time_reached": "زمان خروج فرا رسیده است",
            "time_remaining": "زمان باقی‌مانده",
            "status_today": "وضعیت امروز",
            "completed": "ورود و خروج کامل شد",
            "checkin_done": "ورود ثبت شده - می‌توانید خروج ثبت کنید",
            "checkin_done_wait": "ورود ثبت شده - خروج از ساعت {time} فعال می‌شود",
            "not_registered": "ثبت نشده",
            "admin_settings": "⚙️ تنظیمات پیشرفته (فقط مدیر)",
            "work_hours": "⏰ تنظیمات ساعت کاری",
            "check_in_time": "ساعت ورود",
            "check_out_time": "ساعت خروج",
            "save_settings": "💾 ذخیره تنظیمات",
            "reset_attendance": "🗑️ بازنشانی حضور و غیاب",
            "reset_all": "🗑️ بازنشانی همه کارمندان",
            "reset_staff": "🔄 بازنشانی {name}",
            "reset_warning": "⚠️ توجه: با کلیک روی دکمه زیر، تمام ورود و خروج‌های امروز همه کارمندان پاک می‌شود!",
            "staff_not_found": "⚠️ کاربر '{username}' در لیست پرسنل ثبت نشده است",
            "contact_admin": "💡 لطفاً با مدیر سیستم تماس بگیرید",
            "login_required": "⚠️ لطفاً ابتدا وارد سیستم شوید",
            "months": {1: "جنوری", 2: "فبروری", 3: "مارچ", 4: "اپریل", 5: "می", 6: "جون", 7: "جولای", 8: "آگست", 9: "سپتمبر", 10: "اکتوبر", 11: "نومبر", 12: "دسمبر"},
            "quarters": {1: "سه ماهه اول (جنوری-مارچ)", 2: "سه ماهه دوم (اپریل-جون)", 3: "سه ماهه سوم (جولای-سپتمبر)", 4: "سه ماهه چهارم (اکتوبر-دسمبر)"}
        },
        "en": {
            "dashboard_title": "Clinical Dashboard",
            "dashboard_subtitle": "Real-time analytics and patient management overview",
            "kpi_title": "📈 Key Performance Indicators",
            "total_patients": "Total Patients",
            "total_revenue": "Total Revenue (AFN)",
            "total_paid": "Total Paid (AFN)",
            "balance": "Balance (AFN)",
            "settled": "Settled ✓",
            "outstanding": "Outstanding",
            "analytics_title": "📊 Revenue & Patient Analytics",
            "select_year": "📅 Select Year",
            "chart_type": "📊 Chart Type",
            "line_chart": "Line Chart",
            "bar_chart": "Bar Chart",
            "area_chart": "Area Chart",
            "period": "📆 Period",
            "monthly": "Monthly",
            "quarterly": "Quarterly",
            "total_revenue_label": "💰 Total Revenue (AFN)",
            "revenue_note": "Includes: Patient costs + Invoice payments",
            "patient_count_label": "👥 Patient Count",
            "patient_note": "Based on patient appointments",
            "revenue_details": "💰 Revenue Details",
            "year": "Year",
            "total_revenue_year": "Total Revenue",
            "total_patients_year": "Total Patients",
            "avg_per_patient": "Average per Patient",
            "monthly_avg": "Monthly Average (AFN)",
            "monthly_revenue": "📆 Monthly Revenue",
            "select_month": "Select Month",
            "patients_count": "Patients",
            "average": "Average",
            "daily_revenue": "📅 Daily Revenue",
            "select_date": "Select Date",
            "patient_list": "Patient List on",
            "patient": "Patient",
            "top_services": "🔝 Top Services",
            "total_services": "Total Services",
            "no_service_data": "ℹ️ No service data available",
            "no_data": "ℹ️ No data to display",
            "today_appointments": "🗓 Today's Appointments",
            "no_appointment": "📭 No appointments for today",
            "waiting": "Waiting",
            "attendance_title": "🕒 Staff Attendance",
            "check_in": "✅ Check In",
            "check_out": "🔚 Check Out",
            "already_checked_in": "⚠️ You have already checked in today",
            "already_checked_out": "⚠️ You have already checked out today",
            "first_check_in": "⚠️ You must check in first",
            "checkout_time_limit": "⏰ Check out is only available after {time}",
            "checkout_time_reached": "Check out time has arrived",
            "time_remaining": "Time remaining",
            "status_today": "Today's Status",
            "completed": "Check in and check out completed",
            "checkin_done": "Check in recorded - You can check out",
            "checkin_done_wait": "Check in recorded - Check out available after {time}",
            "not_registered": "Not registered",
            "admin_settings": "⚙️ Advanced Settings (Admin Only)",
            "work_hours": "⏰ Work Hours Settings",
            "check_in_time": "Check In Time",
            "check_out_time": "Check Out Time",
            "save_settings": "💾 Save Settings",
            "reset_attendance": "🗑️ Reset Attendance",
            "reset_all": "🗑️ Reset All Staff",
            "reset_staff": "🔄 Reset {name}",
            "reset_warning": "⚠️ Warning: Clicking the button below will delete all today's attendance records!",
            "staff_not_found": "⚠️ User '{username}' is not registered as staff",
            "contact_admin": "💡 Please contact the system administrator",
            "login_required": "⚠️ Please login first",
            "months": {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"},
            "quarters": {1: "Q1 (Jan-Mar)", 2: "Q2 (Apr-Jun)", 3: "Q3 (Jul-Sep)", 4: "Q4 (Oct-Dec)"}
        }
    }
    
    def t(key):
        lang = st.session_state.get("dashboard_language", "dr")
        keys = key.split(".")
        value = translations[lang]
        for k in keys:
            value = value.get(k, {})
            if isinstance(value, dict) and not value:
                return key
        if isinstance(value, dict):
            return value
        return value if value else key
    
    # =========================================================================
    # استایل کلی Dashboard
    # =========================================================================
    st.markdown("""
        <style>
        :root {
            --bg-deep: #0A0F1F;
            --bg-dark: #0E1629;
            --bg-medium: #141E36;
            --bg-light: #1A2745;
            --neon-blue-1: #00C8FF;
            --neon-blue-2: #0066FF;
            --neon-blue-3: #4D9EFF;
            --neon-blue-4: #7FBAFF;
            --success: #00C8FF;
            --warning: #FF6B6B;
            --info: #4D9EFF;
            --text-bright: #FFFFFF;
            --text-soft: #E0F0FF;
            --text-muted: #7FBAFF;
            --glow-blue: 0 0 20px rgba(0, 200, 255, 0.3);
            --shadow-card: 0 5px 20px -5px rgba(0, 0, 0, 0.5);
        }
        
        .dashboard-header {
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
        
        .dashboard-header::before {
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
        
        .animated-icon {
            font-size: 48px;
            display: inline-block;
            animation: pulse 2s ease-in-out infinite, float 3s ease-in-out infinite;
            margin-bottom: 10px;
            filter: drop-shadow(0 0 15px #00C8FF);
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.9; }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .dashboard-header h1 {
            color: white;
            font-size: 36px;
            font-weight: 700;
            margin: 10px 0 0 0;
            text-shadow: 0 0 15px #00C8FF;
        }
        
        .dashboard-header p {
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
        
        .chart-title {
            color: #00C8FF;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #0066FF;
            text-shadow: 0 0 10px #00C8FF;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #141E36, #0E1629);
            padding: 25px;
            border-radius: 20px;
            border: 2px solid #00C8FF;
            box-shadow: 0 5px 15px -5px rgba(0, 200, 255, 0.2);
            text-align: center;
            transition: all 0.3s ease;
            height: 100%;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px -5px rgba(0, 200, 255, 0.3);
        }
        
        .metric-value {
            color: white;
            font-size: 32px;
            font-weight: 700;
            margin: 10px 0 5px 0;
            text-shadow: 0 0 15px #00C8FF;
        }
        
        .metric-label {
            color: #7FBAFF;
            font-size: 14px;
            font-weight: 500;
        }
        
        .appointment-card {
            background: linear-gradient(135deg, #141E36, #0E1629);
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 12px;
            border-right: 4px solid #00C8FF;
            transition: all 0.2s ease;
        }
        
        .appointment-card:hover {
            transform: translateX(-5px);
            box-shadow: 0 0 15px rgba(0, 200, 255, 0.2);
        }
        
        .appointment-name {
            color: white;
            font-size: 16px;
            font-weight: 600;
        }
        
        .appointment-time {
            color: #00C8FF;
            font-size: 13px;
            font-weight: 500;
        }
        
        .appointment-service {
            color: #7FBAFF;
            font-size: 12px;
        }
        
        .appointment-phone {
            color: #4D9EFF;
            font-size: 11px;
            direction: ltr;
        }
        
        .no-appointment {
            background: #0E1629;
            border: 1px dashed #00C8FF;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
        }
        
        .no-appointment span {
            color: #7FBAFF;
            font-size: 14px;
        }
        
        .stat-badge {
            background: #00C8FF;
            color: #0A0F1F;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            display: inline-block;
        }
        
        .attendance-info {
            background: #0A0F1F;
            border: 1px solid #00C8FF;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 15px;
        }
        
        .attendance-info span {
            color: #7FBAFF;
            font-size: 13px;
        }
        
        .attendance-info strong {
            color: #00C8FF;
        }
        
        .time-warning {
            background: #1a1a2e;
            border-right: 3px solid #F39C12;
            padding: 8px;
            border-radius: 6px;
            margin: 10px 0;
        }
        
        .time-success {
            background: #1a1a2e;
            border-right: 3px solid #2ECC71;
            padding: 8px;
            border-radius: 6px;
            margin: 10px 0;
        }
        
        .admin-title {
            color: #00C8FF;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 12px;
            border-bottom: 1px solid #00C8FF;
            padding-bottom: 5px;
        }
        
        .admin-warning {
            background: #1a1a2e;
            border-right: 3px solid #E74C3C;
            padding: 8px 12px;
            border-radius: 6px;
            margin: 10px 0;
            font-size: 12px;
            color: #E74C3C;
        }
        
        .stButton button {
            background: linear-gradient(135deg, #00C8FF, #0066FF) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 0 !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 12px #00C8FF;
        }
        
        .stButton button:disabled {
            background: #2C3E50 !important;
            opacity: 0.6;
        }
        
        .hdr-status-box {
            background: #0A0F1F;
            border: 1px solid #00C8FF;
            border-radius: 8px;
            padding: 10px;
            margin-top: 15px;
            text-align: center;
        }
        
        .hdr-status-text {
            color: #7FBAFF;
            font-size: 13px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # =========================================================================
    # دریافت اطلاعات از دیتابیس
    # =========================================================================
    try:
        with get_connection() as conn:
            df = pd.read_sql_query("SELECT * FROM patients", conn)
            invoices_df = pd.read_sql_query("SELECT * FROM patient_invoices", conn)
            payments_df = pd.read_sql_query("SELECT * FROM patient_payments", conn)
    except Exception as e:
        st.error(f"❌ Database Error: {e}")
        return
    
    if df.empty:
        st.warning("⚠️ No patient data found in the database.")
        return
    
    # =========================================================================
    # محاسبات مالی
    # =========================================================================
    total_revenue_from_patients = df['cost'].sum() if 'cost' in df.columns else 0
    total_revenue_from_invoices = invoices_df['unit_price'].sum() if not invoices_df.empty else 0
    total_revenue = total_revenue_from_patients + total_revenue_from_invoices
    
    total_paid_from_patients = df['paid_amount'].sum() if 'paid_amount' in df.columns else 0
    total_paid_from_payments = payments_df['amount'].sum() if not payments_df.empty else 0
    total_paid = total_paid_from_patients + total_paid_from_payments
    
    total_discount = df['discount'].sum() if 'discount' in df.columns else 0
    remaining_balance = total_revenue - total_paid - total_discount
    total_patients = len(df)
    
    # =========================================================================
    # هدر داشبورد
    # =========================================================================
    st.markdown(f"""
        <div class="dashboard-header">
            <div class="animated-icon">📊</div>
            <h1>{t('dashboard_title')}</h1>
            <p>{t('dashboard_subtitle')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # =========================================================================
    # KPI Cards
    # =========================================================================
    st.markdown(f'<div class="section-header">{t("kpi_title")}</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 32px; margin-bottom: 10px; color: #00C8FF;">👥</div>
                <div class="metric-value">{total_patients:,}</div>
                <div class="metric-label">{t('total_patients')}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 32px; margin-bottom: 10px; color: #00C8FF;">💰</div>
                <div class="metric-value">{total_revenue:,.0f}</div>
                <div class="metric-label">{t('total_revenue')}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 32px; margin-bottom: 10px; color: #4D9EFF;">💳</div>
                <div class="metric-value">{total_paid:,.0f}</div>
                <div class="metric-label">{t('total_paid')}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        balance_color = "#00C8FF" if remaining_balance <= 0 else "#FF6B6B"
        balance_text = t('settled') if remaining_balance <= 0 else t('outstanding')
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 32px; margin-bottom: 10px; color: #00C8FF;">⚖️</div>
                <div class="metric-value" style="color: {balance_color};">{remaining_balance:,.0f}</div>
                <div class="metric-label">{t('balance')}</div>
                <div style="margin-top: 10px; font-size: 11px; color: {balance_color};">{balance_text}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
    
    # =========================================================================
    # بخش نمودارها
    # =========================================================================
    
    # آماده‌سازی داده‌های تاریخ
    if 'appointment_date' in df.columns:
        df['appointment_date'] = pd.to_datetime(df['appointment_date'], errors='coerce')
        df = df.dropna(subset=['appointment_date'])
    
    if not invoices_df.empty and 'invoice_date' in invoices_df.columns:
        invoices_df['invoice_date'] = pd.to_datetime(invoices_df['invoice_date'], errors='coerce')
        invoices_df = invoices_df.dropna(subset=['invoice_date'])
    
    if not df.empty or not invoices_df.empty:
        years_from_patients = df['appointment_date'].dt.year.unique() if not df.empty else []
        years_from_invoices = invoices_df['invoice_date'].dt.year.unique() if not invoices_df.empty else []
        available_years = sorted(set(list(years_from_patients) + list(years_from_invoices)))
        
        if available_years:
            st.markdown(f'<div class="chart-title">{t("analytics_title")}</div>', unsafe_allow_html=True)
            
            col_year, col_chart_type, col_period = st.columns(3)
            
            with col_year:
                selected_year = st.selectbox(t("select_year"), available_years, index=len(available_years)-1, key="dashboard_year")
            
            with col_chart_type:
                chart_type_display = st.selectbox(t("chart_type"), [t("line_chart"), t("bar_chart"), t("area_chart")], index=0, key="dashboard_chart_type")
                if chart_type_display == t("line_chart"):
                    chart_type_en = "Line Chart"
                elif chart_type_display == t("bar_chart"):
                    chart_type_en = "Bar Chart"
                else:
                    chart_type_en = "Area Chart"
            
            with col_period:
                period_type = st.selectbox(t("period"), [t("monthly"), t("quarterly")], index=0, key="period_type")
            
            def get_revenue_by_period(data_type="monthly"):
                if data_type == "monthly":
                    revenue_dict = {m: 0 for m in range(1, 13)}
                    patient_count_dict = {m: 0 for m in range(1, 13)}
                else:
                    revenue_dict = {q: 0 for q in range(1, 5)}
                    patient_count_dict = {q: 0 for q in range(1, 5)}
                
                if not df.empty:
                    patients_year = df[df['appointment_date'].dt.year == selected_year]
                    if data_type == "monthly":
                        for month in range(1, 13):
                            month_data = patients_year[patients_year['appointment_date'].dt.month == month]
                            revenue_dict[month] += month_data['cost'].sum()
                            patient_count_dict[month] += len(month_data)
                    else:
                        patients_year['quarter'] = patients_year['appointment_date'].dt.quarter
                        for q in range(1, 5):
                            quarter_data = patients_year[patients_year['quarter'] == q]
                            revenue_dict[q] += quarter_data['cost'].sum()
                            patient_count_dict[q] += len(quarter_data)
                
                if not invoices_df.empty:
                    invoices_year = invoices_df[invoices_df['invoice_date'].dt.year == selected_year]
                    if data_type == "monthly":
                        for month in range(1, 13):
                            month_data = invoices_year[invoices_year['invoice_date'].dt.month == month]
                            revenue_dict[month] += month_data['unit_price'].sum()
                    else:
                        invoices_year['quarter'] = invoices_year['invoice_date'].dt.quarter
                        for q in range(1, 5):
                            quarter_data = invoices_year[invoices_year['quarter'] == q]
                            revenue_dict[q] += quarter_data['unit_price'].sum()
                
                return revenue_dict, patient_count_dict
            
            period_key = "monthly" if period_type == t("monthly") else "quarterly"
            revenue_data, patient_data = get_revenue_by_period(period_key)
            
            months_local = t("months")
            quarters_local = t("quarters")
            
            if period_type == t("monthly"):
                revenue_df = pd.DataFrame({'month': list(revenue_data.keys()), 'revenue': list(revenue_data.values())})
                revenue_df['month_name'] = revenue_df['month'].map(months_local)
                revenue_df = revenue_df.set_index('month_name')
                
                patients_df = pd.DataFrame({'month': list(patient_data.keys()), 'patient_count': list(patient_data.values())})
                patients_df['month_name'] = patients_df['month'].map(months_local)
                patients_df = patients_df.set_index('month_name')
                chart_height = 350
            else:
                revenue_df = pd.DataFrame({'quarter': list(revenue_data.keys()), 'revenue': list(revenue_data.values())})
                revenue_df['quarter_name'] = revenue_df['quarter'].map(quarters_local)
                revenue_df = revenue_df.set_index('quarter_name')
                
                patients_df = pd.DataFrame({'quarter': list(patient_data.keys()), 'patient_count': list(patient_data.values())})
                patients_df['quarter_name'] = patients_df['quarter'].map(quarters_local)
                patients_df = patients_df.set_index('quarter_name')
                chart_height = 300
            
            col_rev, col_pat = st.columns(2)
            
            with col_rev:
                st.markdown(f'<p style="color: #00C8FF; font-size: 14px; margin-bottom: 10px;">{t("total_revenue_label")}</p>', unsafe_allow_html=True)
                st.caption(t("revenue_note"))
                
                if chart_type_en == "Line Chart":
                    st.line_chart(revenue_df['revenue'], height=chart_height)
                elif chart_type_en == "Bar Chart":
                    st.bar_chart(revenue_df['revenue'], height=chart_height)
                else:
                    st.area_chart(revenue_df['revenue'], height=chart_height)
            
            with col_pat:
                st.markdown(f'<p style="color: #00C8FF; font-size: 14px; margin-bottom: 10px;">{t("patient_count_label")}</p>', unsafe_allow_html=True)
                st.caption(t("patient_note"))
                
                if chart_type_en == "Line Chart":
                    st.line_chart(patients_df['patient_count'], height=chart_height)
                elif chart_type_en == "Bar Chart":
                    st.bar_chart(patients_df['patient_count'], height=chart_height)
                else:
                    st.area_chart(patients_df['patient_count'], height=chart_height)
            
            st.markdown('<div style="margin: 30px 0;"></div>', unsafe_allow_html=True)
            
            # ========== جزئیات درآمد ==========
            st.markdown(f'<div class="chart-title">{t("revenue_details")}</div>', unsafe_allow_html=True)
            
            total_year_revenue = sum(revenue_data.values())
            total_year_patients = sum(patient_data.values())
            avg_per_patient = total_year_revenue / total_year_patients if total_year_patients > 0 else 0
            
            col_yr1, col_yr2, col_yr3 = st.columns(3)
            with col_yr1:
                st.markdown(f"""
                <div class="metric-card" style="padding: 15px;">
                    <div style="font-size: 24px;">📅</div>
                    <div class="metric-value" style="font-size: 22px;">{selected_year}</div>
                    <div class="metric-label">{t('year')}</div>
                    <div style="margin-top: 10px; font-size: 13px; color: #00C8FF;">{t('total_revenue_year')}</div>
                    <div style="font-size: 20px; font-weight: 700;">{total_year_revenue:,.0f} AFN</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_yr2:
                st.markdown(f"""
                <div class="metric-card" style="padding: 15px;">
                    <div style="font-size: 24px;">👥</div>
                    <div class="metric-value" style="font-size: 22px;">{total_year_patients}</div>
                    <div class="metric-label">{t('total_patients_year')}</div>
                    <div style="margin-top: 10px; font-size: 13px; color: #4D9EFF;">{t('avg_per_patient')}</div>
                    <div style="font-size: 18px; font-weight: 700;">{avg_per_patient:,.0f} AFN</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_yr3:
                monthly_avg = total_year_revenue / 12
                st.markdown(f"""
                <div class="metric-card" style="padding: 15px;">
                    <div style="font-size: 24px;">📈</div>
                    <div class="metric-value" style="font-size: 22px;">{monthly_avg:,.0f}</div>
                    <div class="metric-label">{t('monthly_avg')}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
            
            # ========== درآمد ماهانه ==========
            st.markdown(f'<h4 style="color: #00C8FF; margin-bottom: 15px;">{t("monthly_revenue")}</h4>', unsafe_allow_html=True)
            
            col_month_select, col_month_revenue = st.columns([1, 2])
            
            with col_month_select:
                selected_month_num = st.selectbox(
                    t("select_month"),
                    options=list(range(1, 13)),
                    format_func=lambda x: months_local[x],
                    index=datetime.now().month - 1 if selected_year == datetime.now().year else 0,
                    key="month_select"
                )
            
            month_revenue = revenue_data.get(selected_month_num, 0)
            month_patients = patient_data.get(selected_month_num, 0)
            month_avg = month_revenue / month_patients if month_patients > 0 else 0
            
            with col_month_revenue:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #141E36, #0E1629); border-radius: 15px; padding: 15px; border: 1px solid #00C8FF;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <span style="color: #7FBAFF; font-size: 13px;">{months_local[selected_month_num]} {selected_year}</span>
                            <div style="font-size: 28px; font-weight: 700; color: #00C8FF;">{month_revenue:,.0f} AFN</div>
                        </div>
                        <div style="text-align: right;">
                            <div><span style="color: #7FBAFF;">{t('patients_count')}:</span> <span style="color: white; font-weight: 600;">{month_patients}</span></div>
                            <div><span style="color: #7FBAFF;">{t('average')}:</span> <span style="color: #4D9EFF;">{month_avg:,.0f} AFN</span></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div style="margin: 30px 0;"></div>', unsafe_allow_html=True)
            
            # ========== درآمد روزانه ==========
            st.markdown(f'<h4 style="color: #00C8FF; margin-bottom: 15px;">{t("daily_revenue")}</h4>', unsafe_allow_html=True)
            
            all_dates = []
            if not df.empty:
                all_dates.extend(df['appointment_date'].dt.date.unique())
            if not invoices_df.empty:
                all_dates.extend(invoices_df['invoice_date'].dt.date.unique())
            
            available_dates = sorted(set(all_dates))
            
            if len(available_dates) > 0:
                col_date_select, col_date_revenue = st.columns([1, 2])
                
                with col_date_select:
                    selected_date = st.date_input(
                        t("select_date"),
                        value=available_dates[-1] if available_dates else datetime.now().date(),
                        min_value=min(available_dates) if available_dates else None,
                        max_value=max(available_dates) if available_dates else None,
                        key="date_select"
                    )
                
                daily_revenue = 0
                daily_patients = 0
                
                if not df.empty:
                    date_data_patients = df[df['appointment_date'].dt.date == selected_date]
                    daily_revenue += date_data_patients['cost'].sum()
                    daily_patients += len(date_data_patients)
                
                if not invoices_df.empty:
                    date_data_invoices = invoices_df[invoices_df['invoice_date'].dt.date == selected_date]
                    daily_revenue += date_data_invoices['unit_price'].sum()
                
                daily_avg = daily_revenue / daily_patients if daily_patients > 0 else 0
                
                with col_date_revenue:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #141E36, #0E1629); border-radius: 15px; padding: 15px; border: 1px solid #00C8FF;">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                            <div>
                                <span style="color: #7FBAFF; font-size: 13px;">{selected_date.strftime('%d %B %Y')}</span>
                                <div style="font-size: 28px; font-weight: 700; color: #00C8FF;">{daily_revenue:,.0f} AFN</div>
                            </div>
                            <div style="text-align: right;">
                                <div><span style="color: #7FBAFF;">{t('patients_count')}:</span> <span style="color: white; font-weight: 600;">{daily_patients}</span></div>
                                <div><span style="color: #7FBAFF;">{t('average')}:</span> <span style="color: #4D9EFF;">{daily_avg:,.0f} AFN</span></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if daily_patients > 0 and not df.empty:
                    with st.expander(f"{t('patient_list')} {selected_date.strftime('%d %B %Y')} ({daily_patients} {t('patient')})"):
                        date_patients_data = df[df['appointment_date'].dt.date == selected_date]
                        for idx, row in date_patients_data.iterrows():
                            st.markdown(f"""
                            <div style="background: #0E1629; border-radius: 8px; padding: 8px 12px; margin-bottom: 5px; border-right: 3px solid #00C8FF;">
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: white;">👤 {row['first_name']} {row['last_name']}</span>
                                    <span style="color: #00C8FF;">{row['cost']:,.0f} AFN</span>
                                </div>
                                <div style="font-size: 12px; color: #7FBAFF;">🦷 {row['service_type'][:40] if pd.notna(row['service_type']) else '---'}</div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.info(t("no_data"))
            
            st.markdown('<div style="margin: 30px 0;"></div>', unsafe_allow_html=True)
            
            # ========== خدمات پرطرفدار ==========
            st.markdown(f'<div class="chart-title">{t("top_services")}</div>', unsafe_allow_html=True)
            
            if 'service_type' in df.columns and not df.empty:
                df_year = df[df['appointment_date'].dt.year == selected_year]
                if not df_year.empty:
                    df_year['service_clean'] = df_year['service_type'].str.split('(').str[0].str.strip()
                    service_counts = df_year['service_clean'].value_counts().head(6)
                    
                    if len(service_counts) > 0:
                        max_count = service_counts.max()
                        total_count = service_counts.sum()
                        
                        service_cols = st.columns(2)
                        for idx, (service, count) in enumerate(service_counts.items()):
                            percent = (count / max_count) * 100
                            percent_of_total = (count / total_count) * 100
                            
                            with service_cols[idx % 2]:
                                st.markdown(f"""
                                <div style="margin-bottom: 15px;">
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                        <span style="color: white; font-weight: 500; font-size: 13px;">{service[:25]}</span>
                                        <span style="color: #00C8FF; font-weight: 600; font-size: 12px;">{count} ({percent_of_total:.0f}%)</span>
                                    </div>
                                    <div style="background: #1A2745; height: 8px; border-radius: 4px; overflow: hidden;">
                                        <div style="background: linear-gradient(90deg, #00C8FF, #0066FF); width: {percent}%; height: 100%; border-radius: 4px;"></div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div style="background: #0E1629; border-radius: 10px; padding: 10px; margin-top: 10px; text-align: center;">
                            <span style="color: #7FBAFF; font-size: 12px;">📊 {t('total_services')}: {total_count}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info(t("no_service_data"))
                else:
                    st.info(t("no_service_data"))
            else:
                st.info(t("no_service_data"))
        else:
            st.info(t("no_data"))
    else:
        st.info(t("no_data"))
    
    st.markdown('<div style="margin: 30px 0;"></div>', unsafe_allow_html=True)
    
    # =========================================================================
    # نوبت‌های امروز
    # =========================================================================
    st.markdown(f'<div class="chart-title">{t("today_appointments")}</div>', unsafe_allow_html=True)
    
    with get_connection() as conn:
        all_patients = pd.read_sql_query("""
            SELECT id, first_name, last_name, phone, service_type, next_visit_date, next_visit_time
            FROM patients 
            WHERE status = 'ACTIVE'
            ORDER BY next_visit_time
        """, conn)
    
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    if 'next_visit_date' in all_patients.columns:
        all_patients['next_visit_date_clean'] = pd.to_datetime(all_patients['next_visit_date'], errors='coerce')
        today_appointments = all_patients[all_patients['next_visit_date_clean'] == pd.to_datetime(today_str)].copy()
        
        if 'next_visit_time' in today_appointments.columns:
            today_appointments = today_appointments.sort_values('next_visit_time')
        
        if not today_appointments.empty:
            st.markdown(f"""
            <div style="background: #0E1629; border: 1px solid #00C8FF; border-radius: 10px; padding: 10px 15px; margin-bottom: 15px;">
                <span style="color: #00C8FF;">📋 {t('today_appointments')}: <strong>{len(today_appointments)}</strong></span>
            </div>
            """, unsafe_allow_html=True)
            
            for idx, row in today_appointments.iterrows():
                time_display = row['next_visit_time'] if pd.notna(row['next_visit_time']) else "---"
                phone_display = row['phone'] if pd.notna(row['phone']) else "---"
                service_display = row['service_type'][:30] + "..." if len(str(row['service_type'])) > 30 else str(row['service_type'])
                
                st.markdown(f"""
                <div class="appointment-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <div class="appointment-name">👤 {row['first_name']} {row['last_name']}</div>
                            <div class="appointment-service">🦷 {service_display}</div>
                            <div class="appointment-phone">📞 {phone_display}</div>
                        </div>
                        <div style="text-align: left;">
                            <div class="appointment-time">⏰ {time_display}</div>
                            <span class="stat-badge">{t('waiting')}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="no-appointment">
                <span>{t('no_appointment')}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(t("no_data"))
    
    st.markdown('<div style="margin: 30px 0;"></div>', unsafe_allow_html=True)
    
    # =========================================================================
    # حاضری کارمندان
    # =========================================================================
    
    st.markdown(f'<div class="chart-title" style="text-align: center;">{t("attendance_title")}</div>', unsafe_allow_html=True)
    
    current_username = None
    if 'user_info' in st.session_state and st.session_state.user_info:
        current_username = st.session_state.user_info.get('username')
    if not current_username:
        current_username = st.session_state.get('username')
    
    if not current_username:
        st.warning(t("login_required"))
        return
    
    today_date = datetime.now().strftime('%Y-%m-%d')
    now_time = datetime.now().strftime('%H:%M:%S')
    now_hour = datetime.now().hour
    now_minute = datetime.now().minute
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff_attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER,
                staff_username TEXT,
                date TEXT,
                check_in TEXT,
                check_out TEXT,
                status TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                default_check_in TEXT DEFAULT '08:00',
                default_check_out TEXT DEFAULT '16:00',
                updated_by TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM attendance_settings")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO attendance_settings (default_check_in, default_check_out, updated_by) VALUES ('08:00', '16:00', 'system')")
        conn.commit()
    
    with get_connection() as conn:
        settings = conn.execute("SELECT default_check_in, default_check_out FROM attendance_settings LIMIT 1").fetchone()
        default_check_in = settings[0] if settings else "08:00"
        default_check_out = settings[1] if settings else "16:00"
    
    check_out_hour = int(default_check_out.split(':')[0])
    check_out_minute = int(default_check_out.split(':')[1])
    
    with get_connection() as conn:
        staff_info = conn.execute("""
            SELECT id, first_name, last_name, position, username, 
                   (SELECT role FROM users WHERE username = ?) as role
            FROM staff 
            WHERE username = ?
        """, (current_username, current_username)).fetchone()
    
    if not staff_info:
        st.warning(t("staff_not_found").format(username=current_username))
        st.info(t("contact_admin"))
        return
    
    staff_id = staff_info[0]
    staff_first = staff_info[1]
    staff_last = staff_info[2]
    staff_position = staff_info[3]
    staff_username = staff_info[4]
    user_role = staff_info[5] if len(staff_info) > 5 else 'staff'
    staff_fullname = f"{staff_first} {staff_last}"
    
    st.markdown(f"""
    <div class="attendance-info">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
            <span>👤 <strong>{staff_fullname}</strong> - {staff_position}</span>
            <span>📅 <strong>{today_date}</strong></span>
            <span>⏰ {t('check_in_time')}: <strong>{default_check_in}</strong></span>
            <span>⏰ {t('check_out_time')}: <strong>{default_check_out}</strong></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    current_total_minutes = now_hour * 60 + now_minute
    check_out_total_minutes = check_out_hour * 60 + check_out_minute
    
    if current_total_minutes >= check_out_total_minutes:
        can_checkout = True
        time_remaining = t("checkout_time_reached")
        time_class = "time-success"
        time_icon = "✅"
    else:
        can_checkout = False
        remaining_hours = (check_out_total_minutes - current_total_minutes) // 60
        remaining_minutes = (check_out_total_minutes - current_total_minutes) % 60
        time_remaining = f"{remaining_hours} ساعت و {remaining_minutes} دقیقه"
        time_class = "time-warning"
        time_icon = "⏳"
    
    st.markdown(f"""
    <div class="{time_class}">
        <span style="color:#7FBAFF;">{time_icon} {t('checkout_time_limit').format(time=default_check_out)}</span>
        <span style="color:#00C8FF; margin-left:10px;">{t('time_remaining')}: {time_remaining}</span>
    </div>
    """, unsafe_allow_html=True)
    
    if user_role == 'admin':
        with st.expander(t("admin_settings"), expanded=False):
            st.markdown(f'<div class="admin-title">{t("work_hours")}</div>', unsafe_allow_html=True)
            
            col_set1, col_set2, col_set3 = st.columns(3)
            
            with col_set1:
                new_check_in = st.time_input(t("check_in_time"), value=datetime.strptime(default_check_in, '%H:%M').time())
            with col_set2:
                new_check_out = st.time_input(t("check_out_time"), value=datetime.strptime(default_check_out, '%H:%M').time())
            with col_set3:
                st.write("")
                st.write("")
                if st.button(t("save_settings"), use_container_width=True):
                    try:
                        with get_connection() as conn:
                            conn.execute("UPDATE attendance_settings SET default_check_in = ?, default_check_out = ?, updated_by = ?, updated_at = CURRENT_TIMESTAMP", (new_check_in.strftime('%H:%M'), new_check_out.strftime('%H:%M'), current_username))
                            conn.commit()
                        st.success("✅ " + t("save_settings"))
                        st.balloons()
                        import time
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            st.markdown("---")
            st.markdown(f'<div class="admin-title">{t("reset_attendance")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="admin-warning">{t("reset_warning")}</div>', unsafe_allow_html=True)
            
            col_reset1, col_reset2 = st.columns(2)
            
            with col_reset1:
                if st.button(t("reset_all"), use_container_width=True):
                    try:
                        with get_connection() as conn:
                            conn.execute("DELETE FROM staff_attendance WHERE date = ?", (today_date,))
                            conn.commit()
                        st.success("✅ " + t("reset_all"))
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            with col_reset2:
                with get_connection() as conn:
                    all_staff = conn.execute("SELECT id, first_name, last_name FROM staff WHERE status = 'active' ORDER BY first_name").fetchall()
                
                if all_staff:
                    staff_reset_names = [f"{s[1]} {s[2]}" for s in all_staff]
                    staff_reset_idx = st.selectbox("انتخاب کارمند", range(len(staff_reset_names)), format_func=lambda x: staff_reset_names[x], key="reset_staff_select")
                    staff_reset_id = all_staff[staff_reset_idx][0]
                    
                    if st.button(t("reset_staff").format(name=staff_reset_names[staff_reset_idx]), use_container_width=True):
                        try:
                            with get_connection() as conn:
                                conn.execute("DELETE FROM staff_attendance WHERE staff_id = ? AND date = ?", (staff_reset_id, today_date))
                                conn.commit()
                            st.success(f"✅ {t('reset_staff').format(name=staff_reset_names[staff_reset_idx])}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
    
    with get_connection() as conn:
        today_record = conn.execute("SELECT id, check_in, check_out FROM staff_attendance WHERE (staff_id = ? OR staff_username = ?) AND date = ?", (staff_id, staff_username, today_date)).fetchone()
    
    col_in, col_out = st.columns(2)
    
    with col_in:
        if st.button(t("check_in"), use_container_width=True):
            if today_record and today_record[1]:
                st.warning(t("already_checked_in"))
            else:
                try:
                    with get_connection() as conn:
                        if today_record:
                            conn.execute("UPDATE staff_attendance SET check_in = ? WHERE id = ?", (now_time, today_record[0]))
                        else:
                            conn.execute("INSERT INTO staff_attendance (staff_id, staff_username, date, check_in) VALUES (?, ?, ?, ?)", (staff_id, staff_username, today_date, now_time))
                        conn.commit()
                    st.success(f"⏱️ {t('check_in')} {now_time}")
                    st.balloons()
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    with col_out:
        checkout_disabled = False
        checkout_message = ""
        
        if not today_record or not today_record[1]:
            checkout_disabled = True
            checkout_message = t("first_check_in")
        elif today_record[2]:
            checkout_disabled = True
            checkout_message = t("already_checked_out")
        elif not can_checkout:
            checkout_disabled = True
            checkout_message = t("checkout_time_limit").format(time=default_check_out)
        
        if checkout_disabled:
            st.button(t("check_out"), disabled=True, use_container_width=True, help=checkout_message)
        else:
            if st.button(t("check_out"), use_container_width=True):
                try:
                    with get_connection() as conn:
                        conn.execute("UPDATE staff_attendance SET check_out = ? WHERE id = ?", (now_time, today_record[0]))
                        conn.commit()
                    st.success(f"🚪 {t('check_out')} {now_time}")
                    st.balloons()
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    with get_connection() as conn:
        record = conn.execute("SELECT check_in, check_out FROM staff_attendance WHERE (staff_id = ? OR staff_username = ?) AND date = ?", (staff_id, staff_username, today_date)).fetchone()
        
        if record:
            if record[0] and record[1]:
                st.markdown(f'<div class="hdr-status-box"><span class="hdr-status-text">🔵 {t("status_today")}: {t("completed")}</span></div>', unsafe_allow_html=True)
            elif record[0] and not record[1]:
                if can_checkout:
                    st.markdown(f'<div class="hdr-status-box"><span class="hdr-status-text">🟡 {t("status_today")}: {t("checkin_done")}</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="hdr-status-box"><span class="hdr-status-text">🟡 {t("status_today")}: {t("checkin_done_wait").format(time=default_check_out)}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="hdr-status-box"><span class="hdr-status-text">⚪ {t("status_today")}: {t("not_registered")}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="hdr-status-box"><span class="hdr-status-text">⚪ {t("status_today")}: {t("not_registered")}</span></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_dashboard()