import os

PROJECT_PATH = r"C:\Users\faisal\Desktop\New folder (2)"

def create_directories():
    dirs = [
        PROJECT_PATH,
        os.path.join(PROJECT_PATH, "modules"),
        os.path.join(PROJECT_PATH, "data"),
        os.path.join(PROJECT_PATH, "patient_files"),
        os.path.join(PROJECT_PATH, "xray_files"),
        os.path.join(PROJECT_PATH, "prescription_files"),
        os.path.join(PROJECT_PATH, "backups"),
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created: {dir_path}")

# ============ app.py ============
app_content = '''import streamlit as st
from modules.database import init_database, get_connection
from modules.auth import login_user, create_default_admin
from modules.dashboard import render_dashboard
from modules.patients import render_add_patient, render_patient_list
from modules.emr import render_emr_section
from modules.settings import render_settings
from modules.treatment_plan import render_treatment_plan_selector
from modules.staff import render_staff_management

st.set_page_config(page_title="سیستم مدیریت کلینیک دندان", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_info = {}

init_database()
create_default_admin()

if not st.session_state.logged_in:
    st.title("🔐 ورود به سیستم")
    with st.form("login_form"):
        username = st.text_input("نام کاربری")
        password = st.text_input("رمز عبور", type="password")
        submit = st.form_submit_button("ورود")
        if submit:
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_info = {'id': user[0], 'username': user[1], 'full_name': user[3], 'role': user[4]}
                st.rerun()
            else:
                st.error("نام کاربری یا رمز عبور اشتباه است")
    st.stop()

with st.sidebar:
    st.markdown("## 🦷 کلینیک دندان")
    st.markdown(f"خوش آمدید {st.session_state.user_info.get('full_name', 'کاربر')}")
    st.markdown("---")
    menu = st.radio("منو", ["📊 Dashboard", "👨‍⚕️ Add Patient", "📋 Patient List", "🦷 EMR", "⚙️ Settings", "📋 Treatment Plan", "👥 Staff"])
    if st.button("🚪 خروج"):
        st.session_state.logged_in = False
        st.rerun()

if menu == "📊 Dashboard":
    render_dashboard()
elif menu == "👨‍⚕️ Add Patient":
    render_add_patient()
elif menu == "📋 Patient List":
    render_patient_list()
elif menu == "🦷 EMR":
    render_emr_section()
elif menu == "⚙️ Settings":
    render_settings()
elif menu == "📋 Treatment Plan":
    render_treatment_plan_selector()
elif menu == "👥 Staff":
    render_staff_management()
'''

# ============ requirements.txt ============
requirements_content = '''streamlit
pandas
openpyxl
xlsxwriter
'''

# ============ modules/__init__.py ============
init_content = '''

'''

# ============ modules/database.py ============
database_content = '''import sqlite3
import os

DB_PATH = os.path.join("data", "clinic.db")

def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_database():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, full_name TEXT, role TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, national_id TEXT UNIQUE, age INTEGER, gender TEXT, service_type TEXT, cost REAL, paid_amount REAL, discount REAL, appointment_date TEXT, next_visit_date TEXT, phone TEXT, status TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS dental_charting (id INTEGER PRIMARY KEY, patient_id INTEGER, tooth_number INTEGER, tooth_status TEXT, notes TEXT, date_updated TIMESTAMP)')
        c.execute('CREATE TABLE IF NOT EXISTS emr_records (id INTEGER PRIMARY KEY, patient_id INTEGER, allergies TEXT, current_medications TEXT, created_at TIMESTAMP)')
        c.execute('CREATE TABLE IF NOT EXISTS patient_invoices (id INTEGER PRIMARY KEY, patient_id INTEGER, service_name TEXT, unit_price REAL, invoice_date TIMESTAMP)')
        c.execute('CREATE TABLE IF NOT EXISTS patient_payments (id INTEGER PRIMARY KEY, patient_id INTEGER, amount REAL, payment_method TEXT, payment_date TIMESTAMP)')
        c.execute('CREATE TABLE IF NOT EXISTS staff (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, national_id TEXT UNIQUE, phone TEXT, position TEXT, salary REAL, hire_date TEXT, username TEXT UNIQUE, password_hash TEXT, status TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS treatment_plans (id INTEGER PRIMARY KEY, patient_id INTEGER, plan_name TEXT, plan_date TIMESTAMP, total_estimated_cost REAL)')
        c.execute('CREATE TABLE IF NOT EXISTS treatment_plan_items (id INTEGER PRIMARY KEY, plan_id INTEGER, procedure_name TEXT, estimated_cost REAL)')
        c.execute('CREATE TABLE IF NOT EXISTS patient_files (id INTEGER PRIMARY KEY, patient_id INTEGER, file_name TEXT, file_type TEXT, file_path TEXT, uploaded_at TIMESTAMP)')
        conn.commit()
        os.makedirs("patient_files", exist_ok=True)
        os.makedirs("backups", exist_ok=True)
        print("Database initialized")
'''

# ============ modules/auth.py ============
auth_content = '''import hashlib
from modules.database import get_connection

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def login_user(username, password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, hash_password(password)))
        return c.fetchone()

def create_default_admin():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                     ("admin", hash_password("admin123"), "مدیر سیستم", "admin"))
            conn.commit()
            print("Admin created: admin/admin123")
'''

# ============ modules/dashboard.py ============
dashboard_content = '''import streamlit as st
import pandas as pd
from datetime import datetime
from modules.database import get_connection

def render_dashboard():
    st.title("داشبورد")
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM patients", conn)
    if df.empty:
        st.warning("No patients")
        return
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Patients", len(df))
    c2.metric("Total Revenue", f"{df['cost'].sum():,.0f} AFN")
    c3.metric("Avg Cost", f"{df['cost'].mean():,.0f} AFN")
    st.dataframe(df[['first_name', 'last_name', 'service_type', 'cost']].head(10))
'''

# ============ modules/patients.py ============
patients_content = '''import streamlit as st
import pandas as pd
from datetime import datetime
from modules.database import get_connection

def render_add_patient():
    st.title("Add Patient")
    with st.form("add"):
        c1, c2 = st.columns(2)
        with c1:
            first = st.text_input("First Name")
            national = st.text_input("National ID")
            age = st.number_input("Age", 1, 120, 30)
        with c2:
            last = st.text_input("Last Name")
            phone = st.text_input("Phone")
            gender = st.selectbox("Gender", ["Male", "Female"])
        service = st.selectbox("Service", ["Checkup", "Filling", "Extraction", "Root Canal"])
        cost = st.number_input("Cost", 0, 100000, 0)
        paid = st.number_input("Paid", 0, 100000, 0)
        date = st.date_input("Date", datetime.now())
        if st.form_submit_button("Save"):
            if first and national:
                with get_connection() as conn:
                    conn.execute('INSERT INTO patients (first_name, last_name, national_id, age, gender, phone, service_type, cost, paid_amount, appointment_date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                               (first, last, national, age, gender, phone, service, cost, paid, date.strftime('%Y-%m-%d'), 'ACTIVE'))
                    conn.commit()
                st.success("Saved!")
                st.balloons()
            else:
                st.error("Required fields")

def render_patient_list():
    st.title("Patient List")
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM patients ORDER BY id DESC", conn)
    if df.empty:
        st.info("No patients")
        return
    st.dataframe(df[['id', 'first_name', 'last_name', 'phone', 'service_type', 'cost']])
    with st.expander("Delete"):
        pid = st.number_input("Patient ID", 1, 9999, 1)
        if st.button("Delete"):
            with get_connection() as conn:
                conn.execute("DELETE FROM patients WHERE id=?", (pid,))
                conn.commit()
            st.rerun()
'''

# ============ modules/prescriptions.py ============
prescriptions_content = '''import streamlit as st
import pandas as pd
from datetime import datetime
from modules.database import get_connection

def render_patient_prescription(patient_id):
    with get_connection() as conn:
        p = pd.read_sql_query("SELECT * FROM patients WHERE id=?", conn, params=(patient_id,)).iloc[0]
    st.header(f"Prescription for {p['first_name']} {p['last_name']}")
    with st.form("rx"):
        meds = st.text_area("Medicines")
        inst = st.text_area("Instructions")
        doc = st.text_input("Doctor", "Dr. Asif")
        if st.form_submit_button("Save"):
            st.success("Saved")
            st.markdown(f"<div style='border:1px solid #ccc;padding:20px'><h3>Prescription</h3><p><strong>Patient:</strong> {p['first_name']} {p['last_name']}</p><p><strong>Medicines:</strong><br>{meds}</p><p><strong>Instructions:</strong><br>{inst}</p><p><strong>Doctor:</strong> {doc}</p><p><strong>Date:</strong> {datetime.now()}</p></div>", unsafe_allow_html=True)
'''

# ============ modules/emr.py ============
emr_content = '''import streamlit as st
import pandas as pd
from modules.database import get_connection

def render_emr_section():
    st.title("Electronic Medical Record")
    with get_connection() as conn:
        patients = pd.read_sql_query("SELECT id, first_name, last_name FROM patients", conn)
    if patients.empty:
        st.warning("No patients")
        return
    selected = st.selectbox("Select Patient", patients.apply(lambda x: f"{x['first_name']} {x['last_name']}", axis=1))
    pid = patients.iloc[list(patients.apply(lambda x: f"{x['first_name']} {x['last_name']}", axis=1)).index(selected)]['id']
    with get_connection() as conn:
        p = pd.read_sql_query("SELECT * FROM patients WHERE id=?", conn, params=(pid,)).iloc[0]
    st.info(f"Patient: {p['first_name']} {p['last_name']} | Age: {p['age']}")
    t1, t2 = st.tabs(["Medical History", "Dental Chart"])
    with t1:
        with get_connection() as conn:
            existing = pd.read_sql_query("SELECT * FROM emr_records WHERE patient_id=?", conn, params=(pid,))
        allergies = existing['allergies'].iloc[0] if not existing.empty else ""
        meds = existing['current_medications'].iloc[0] if not existing.empty else ""
        with st.form("med"):
            a = st.text_area("Allergies", allergies)
            m = st.text_area("Medications", meds)
            if st.form_submit_button("Save"):
                if not existing.empty:
                    conn.execute("UPDATE emr_records SET allergies=?, current_medications=? WHERE patient_id=?", (a, m, pid))
                else:
                    conn.execute("INSERT INTO emr_records (patient_id, allergies, current_medications) VALUES (?,?,?)", (pid, a, m))
                conn.commit()
                st.success("Saved")
    with t2:
        st.write("Dental chart (teeth 1-32)")
        cols = st.columns(8)
        for i in range(1, 33):
            with cols[(i-1)%8]:
                st.button(str(i))
'''

# ============ modules/settings.py ============
settings_content = '''import streamlit as st
import pandas as pd
import hashlib
from modules.database import get_connection

def render_settings():
    st.title("Settings")
    t1, t2 = st.tabs(["Users", "Backup"])
    with t1:
        with get_connection() as conn:
            users = pd.read_sql_query("SELECT id, username, full_name, role FROM users", conn)
        st.dataframe(users)
        with st.form("new_user"):
            uname = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            name = st.text_input("Full Name")
            role = st.selectbox("Role", ["admin", "staff"])
            if st.form_submit_button("Add"):
                if uname and pwd:
                    hashed = hashlib.sha256(pwd.encode()).hexdigest()
                    conn.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?,?,?,?)", (uname, hashed, name, role))
                    conn.commit()
                    st.rerun()
    with t2:
        if st.button("Create Backup"):
            import shutil, datetime
            name = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2("data/clinic.db", f"backups/{name}")
            with open(f"backups/{name}", "rb") as f:
                st.download_button("Download", f, file_name=name)
'''

# ============ modules/treatment_plan.py ============
treatment_plan_content = '''import streamlit as st
import pandas as pd
from modules.database import get_connection

def render_treatment_plan_selector():
    st.title("Treatment Plan")
    with get_connection() as conn:
        patients = pd.read_sql_query("SELECT id, first_name, last_name FROM patients", conn)
    if patients.empty:
        st.warning("No patients")
        return
    selected = st.selectbox("Select Patient", patients.apply(lambda x: f"{x['first_name']} {x['last_name']}", axis=1))
    pid = patients.iloc[list(patients.apply(lambda x: f"{x['first_name']} {x['last_name']}", axis=1)).index(selected)]['id']
    with st.form("plan"):
        name = st.text_input("Plan Name")
        if st.form_submit_button("Create"):
            with get_connection() as conn:
                conn.execute("INSERT INTO treatment_plans (patient_id, plan_name) VALUES (?,?)", (pid, name))
                conn.commit()
            st.rerun()
    with get_connection() as conn:
        plans = pd.read_sql_query("SELECT * FROM treatment_plans WHERE patient_id=?", conn, params=(pid,))
    for _, plan in plans.iterrows():
        with st.expander(plan['plan_name']):
            st.write(f"Cost: {plan['total_estimated_cost']:,.0f} AFN")
            with st.form(f"item_{plan['id']}"):
                proc = st.text_input("Procedure")
                cost = st.number_input("Cost", 0, 100000, 0)
                if st.form_submit_button("Add Item"):
                    conn.execute("INSERT INTO treatment_plan_items (plan_id, procedure_name, estimated_cost) VALUES (?,?,?)", (plan['id'], proc, cost))
                    conn.execute("UPDATE treatment_plans SET total_estimated_cost = (SELECT SUM(estimated_cost) FROM treatment_plan_items WHERE plan_id=?) WHERE id=?", (plan['id'], plan['id']))
                    conn.commit()
                    st.rerun()
'''

# ============ modules/staff.py ============
staff_content = '''import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime
from modules.database import get_connection

def render_staff_management():
    st.title("Staff Management")
    t1, t2 = st.tabs(["Staff List", "Add Staff"])
    with t1:
        with get_connection() as conn:
            staff = pd.read_sql_query("SELECT id, first_name, last_name, position, phone, salary FROM staff", conn)
        if not staff.empty:
            st.dataframe(staff)
    with t2:
        with st.form("add_staff"):
            c1, c2 = st.columns(2)
            with c1:
                first = st.text_input("First Name")
                last = st.text_input("Last Name")
                national = st.text_input("National ID")
                phone = st.text_input("Phone")
            with c2:
                pos = st.selectbox("Position", ["Dentist", "Assistant", "Receptionist", "Admin"])
                salary = st.number_input("Salary", 0, 100000, 0)
                hire = st.date_input("Hire Date", datetime.now())
                uname = st.text_input("Username")
                pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Save"):
                if first and last and national and uname and pwd:
                    hashed = hashlib.sha256(pwd.encode()).hexdigest()
                    with get_connection() as conn:
                        conn.execute("INSERT INTO staff (first_name, last_name, national_id, phone, position, salary, hire_date, username, password_hash, status) VALUES (?,?,?,?,?,?,?,?,?,?)",
                                   (first, last, national, phone, pos, salary, hire.strftime('%Y-%m-%d'), uname, hashed, 'active'))
                        conn.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?,?,?,?)",
                                   (uname, hashed, f"{first} {last}", 'staff'))
                        conn.commit()
                    st.success("Staff added")
                    st.rerun()
'''

# ============ WRITE ALL FILES ============
def main():
    print("=" * 50)
    print("Building Dental Clinic System...")
    print("=" * 50)
    
    create_directories()
    
    files = [
        (os.path.join(PROJECT_PATH, "app.py"), app_content),
        (os.path.join(PROJECT_PATH, "requirements.txt"), requirements_content),
        (os.path.join(PROJECT_PATH, "modules", "__init__.py"), init_content),
        (os.path.join(PROJECT_PATH, "modules", "database.py"), database_content),
        (os.path.join(PROJECT_PATH, "modules", "auth.py"), auth_content),
        (os.path.join(PROJECT_PATH, "modules", "dashboard.py"), dashboard_content),
        (os.path.join(PROJECT_PATH, "modules", "patients.py"), patients_content),
        (os.path.join(PROJECT_PATH, "modules", "prescriptions.py"), prescriptions_content),
        (os.path.join(PROJECT_PATH, "modules", "emr.py"), emr_content),
        (os.path.join(PROJECT_PATH, "modules", "settings.py"), settings_content),
        (os.path.join(PROJECT_PATH, "modules", "treatment_plan.py"), treatment_plan_content),
        (os.path.join(PROJECT_PATH, "modules", "staff.py"), staff_content),
    ]
    
    for path, content in files:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created: {path}")
    
    print("=" * 50)
    print("✅ DONE!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. pip install streamlit pandas openpyxl xlsxwriter")
    print("2. streamlit run app.py")
    print("3. Login: admin / admin123")

if __name__ == "__main__":
    main()