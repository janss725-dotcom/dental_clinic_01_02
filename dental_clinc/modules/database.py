import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("data", "clinic.db")

def get_connection():
    """ایجاد اتصال به دیتابیس"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """ایجاد تمام جداول مورد نیاز و اضافه کردن ستون‌های缺失"""
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # ===== جدول users =====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                role TEXT DEFAULT 'staff'
            )
        ''')
        
        # ===== جدول patients =====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT,
                national_id TEXT UNIQUE,
                age INTEGER,
                gender TEXT,
                service_type TEXT,
                cost REAL DEFAULT 0,
                paid_amount REAL DEFAULT 0,
                discount REAL DEFAULT 0,
                appointment_date TEXT,
                next_visit_date TEXT,
                next_visit_time TEXT,
                phone TEXT,
                address TEXT,
                status TEXT DEFAULT 'ACTIVE'
            )
        ''')
        
        # ===== اضافه کردن ستون‌های missing به patients =====
        cursor.execute("PRAGMA table_info(patients)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'next_visit_time' not in columns:
            cursor.execute("ALTER TABLE patients ADD COLUMN next_visit_time TEXT")
            print("✅ ستون next_visit_time اضافه شد")
        
        if 'address' not in columns:
            cursor.execute("ALTER TABLE patients ADD COLUMN address TEXT")
            print("✅ ستون address اضافه شد")
        
        # ===== جدول dental_charting =====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dental_charting (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                tooth_number INTEGER NOT NULL,
                tooth_status TEXT,
                notes TEXT,
                is_treatment INTEGER DEFAULT 0,
                date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
            )
        ''')
        
        # ===== جدول emr_records =====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emr_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                medical_history TEXT,
                allergies TEXT,
                current_medications TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
            )
        ''')
        
        # ===== جدول patient_invoices =====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                service_name TEXT NOT NULL,
                unit_price REAL DEFAULT 0,
                FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
            )
        ''')
        
        # ===== جدول patient_payments =====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                amount REAL DEFAULT 0,
                payment_method TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
            )
        ''')
        
        # ===== جدول dental_services =====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dental_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_name TEXT UNIQUE,
                default_price REAL DEFAULT 0
            )
        ''')
        
        # ===== جدول staff =====
        cursor.execute('''
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
        ''')
        
        # ===== اضافه کردن ستون‌های missing به staff =====
        cursor.execute("PRAGMA table_info(staff)")
        staff_columns = [col[1] for col in cursor.fetchall()]
        
        if 'address' not in staff_columns:
            cursor.execute("ALTER TABLE staff ADD COLUMN address TEXT")
            print("✅ ستون address به جدول staff اضافه شد")
        
        if 'specialization' not in staff_columns:
            cursor.execute("ALTER TABLE staff ADD COLUMN specialization TEXT")
            print("✅ ستون specialization به جدول staff اضافه شد")
        
        if 'license_number' not in staff_columns:
            cursor.execute("ALTER TABLE staff ADD COLUMN license_number TEXT")
            print("✅ ستون license_number به جدول staff اضافه شد")
        
        if 'created_at' not in staff_columns:
            cursor.execute("ALTER TABLE staff ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✅ ستون created_at به جدول staff اضافه شد")
        
        # ===== جدول user_permissions =====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_permissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                permission_key TEXT NOT NULL,
                permission_value BOOLEAN DEFAULT 0,
                UNIQUE(user_id, permission_key)
            )
        ''')
        
        # ===== جداول طرح درمان =====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS treatment_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                plan_name TEXT NOT NULL,
                plan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                plan_status TEXT DEFAULT 'active',
                priority TEXT DEFAULT 'normal',
                estimated_start_date DATE,
                estimated_end_date DATE,
                total_estimated_cost REAL DEFAULT 0,
                total_actual_cost REAL DEFAULT 0,
                discount REAL DEFAULT 0,
                notes TEXT,
                is_completed BOOLEAN DEFAULT 0,
                completed_date TIMESTAMP,
                created_by TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS treatment_plan_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_id INTEGER NOT NULL,
                tooth_number INTEGER,
                procedure_name TEXT NOT NULL,
                procedure_code TEXT,
                category TEXT,
                estimated_cost REAL DEFAULT 0,
                actual_cost REAL DEFAULT 0,
                discount REAL DEFAULT 0,
                status TEXT DEFAULT 'planned',
                scheduled_date DATE,
                completed_date TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (plan_id) REFERENCES treatment_plans (id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS procedure_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                default_cost REAL DEFAULT 0,
                description TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # ===== بررسی و اضافه کردن ستون‌های missing به treatment_plans =====
        cursor.execute("PRAGMA table_info(treatment_plans)")
        plan_columns = [col[1] for col in cursor.fetchall()]
        
        if 'estimated_start_date' not in plan_columns:
            cursor.execute("ALTER TABLE treatment_plans ADD COLUMN estimated_start_date DATE")
            print("✅ ستون estimated_start_date به treatment_plans اضافه شد")
        
        if 'estimated_end_date' not in plan_columns:
            cursor.execute("ALTER TABLE treatment_plans ADD COLUMN estimated_end_date DATE")
            print("✅ ستون estimated_end_date به treatment_plans اضافه شد")
        
        if 'total_actual_cost' not in plan_columns:
            cursor.execute("ALTER TABLE treatment_plans ADD COLUMN total_actual_cost REAL DEFAULT 0")
            print("✅ ستون total_actual_cost به treatment_plans اضافه شد")
        
        if 'completed_date' not in plan_columns:
            cursor.execute("ALTER TABLE treatment_plans ADD COLUMN completed_date TIMESTAMP")
            print("✅ ستون completed_date به treatment_plans اضافه شد")
        
        # ===== بررسی و اضافه کردن ستون‌های missing به treatment_plan_items =====
        cursor.execute("PRAGMA table_info(treatment_plan_items)")
        item_columns = [col[1] for col in cursor.fetchall()]
        
        if 'procedure_code' not in item_columns:
            cursor.execute("ALTER TABLE treatment_plan_items ADD COLUMN procedure_code TEXT")
            print("✅ ستون procedure_code به treatment_plan_items اضافه شد")
        
        if 'category' not in item_columns:
            cursor.execute("ALTER TABLE treatment_plan_items ADD COLUMN category TEXT")
            print("✅ ستون category به treatment_plan_items اضافه شد")
        
        if 'actual_cost' not in item_columns:
            cursor.execute("ALTER TABLE treatment_plan_items ADD COLUMN actual_cost REAL DEFAULT 0")
            print("✅ ستون actual_cost به treatment_plan_items اضافه شد")
        
        if 'discount' not in item_columns:
            cursor.execute("ALTER TABLE treatment_plan_items ADD COLUMN discount REAL DEFAULT 0")
            print("✅ ستون discount به treatment_plan_items اضافه شد")
        
        if 'scheduled_date' not in item_columns:
            cursor.execute("ALTER TABLE treatment_plan_items ADD COLUMN scheduled_date DATE")
            print("✅ ستون scheduled_date به treatment_plan_items اضافه شد")
        
        # ===== درج کدهای استاندارد درمانی پیش‌فرض =====
        cursor.execute("SELECT COUNT(*) FROM procedure_codes")
        if cursor.fetchone()[0] == 0:
            default_codes = [
                ('D0120', 'Periodic Oral Evaluation', 'Diagnostic', 500, 'Routine checkup'),
                ('D0140', 'Limited Oral Evaluation', 'Diagnostic', 400, 'Problem focused'),
                ('D0150', 'Comprehensive Oral Evaluation', 'Diagnostic', 800, 'New patient'),
                ('D0210', 'Intraoral - Complete Series', 'Radiology', 1200, 'Full mouth X-rays'),
                ('D0220', 'Intraoral - Periapical', 'Radiology', 300, 'Single tooth X-ray'),
                ('D0230', 'Intraoral - Bitewing', 'Radiology', 250, 'Caries detection'),
                ('D0330', 'Panoramic Film', 'Radiology', 800, 'Full jaw X-ray'),
                ('D1110', 'Prophylaxis - Adult', 'Preventive', 800, 'Teeth cleaning'),
                ('D1120', 'Prophylaxis - Child', 'Preventive', 600, 'Child cleaning'),
                ('D1206', 'Topical Fluoride', 'Preventive', 300, 'Fluoride varnish'),
                ('D2140', 'Amalgam - 1 Surface', 'Restorative', 800, 'Silver filling'),
                ('D2150', 'Amalgam - 2 Surfaces', 'Restorative', 1200, 'Silver filling'),
                ('D2160', 'Amalgam - 3 Surfaces', 'Restorative', 1600, 'Silver filling'),
                ('D2330', 'Resin - 1 Surface', 'Restorative', 1000, 'Tooth colored filling'),
                ('D2331', 'Resin - 2 Surfaces', 'Restorative', 1500, 'Tooth colored filling'),
                ('D2332', 'Resin - 3 Surfaces', 'Restorative', 2000, 'Tooth colored filling'),
                ('D3110', 'Pulp Cap - Direct', 'Endodontic', 800, 'Direct pulp cap'),
                ('D3220', 'Pulpotomy', 'Endodontic', 1200, 'Partial root canal'),
                ('D3230', 'RCT - Anterior', 'Endodontic', 3500, 'Root canal - front tooth'),
                ('D3240', 'RCT - Premolar', 'Endodontic', 4500, 'Root canal - premolar'),
                ('D3250', 'RCT - Molar', 'Endodontic', 6000, 'Root canal - molar'),
                ('D7140', 'Extraction - Simple', 'Oral Surgery', 1200, 'Simple tooth removal'),
                ('D7210', 'Extraction - Surgical', 'Oral Surgery', 2000, 'Surgical removal'),
                ('D7220', 'Extraction - Soft Tissue Impacted', 'Oral Surgery', 2500, 'Impacted tooth'),
                ('D7240', 'Extraction - Bony Impacted', 'Oral Surgery', 4500, 'Bony impacted tooth'),
                ('D6010', 'Implant Placement', 'Implant', 25000, 'Single implant'),
                ('D6058', 'Implant Crown', 'Implant', 9000, 'Crown on implant'),
                ('D2740', 'Crown - Porcelain', 'Prosthodontic', 8000, 'Porcelain crown'),
                ('D2750', 'Crown - PFM', 'Prosthodontic', 6000, 'Porcelain fused to metal'),
                ('D2790', 'Crown - Full Cast', 'Prosthodontic', 5000, 'Full metal crown'),
                ('D6240', 'Bridge - PFM', 'Prosthodontic', 6000, 'Porcelain bridge per unit'),
                ('D8080', 'Ortho - Comprehensive', 'Orthodontic', 25000, 'Full orthodontic treatment'),
                ('D8670', 'Ortho - Periodic Visit', 'Orthodontic', 500, 'Adjustment visit'),
                ('D9110', 'Palliative Treatment', 'Emergency', 500, 'Emergency pain relief'),
                ('D9940', 'Occlusal Guard', 'Preventive', 2000, 'Night guard'),
            ]
            cursor.executemany("""
                INSERT INTO procedure_codes (code, name, category, default_cost, description)
                VALUES (?, ?, ?, ?, ?)
            """, default_codes)
            print("✅ 35 کد استاندارد درمانی به جدول procedure_codes اضافه شد")
        
        # ===== جدول staff_loans =====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff_loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER NOT NULL,
                loan_date DATE NOT NULL,
                amount REAL NOT NULL,
                remaining_amount REAL NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (staff_id) REFERENCES staff (id) ON DELETE CASCADE
            )
        ''')
        
        # ===== جدول staff_attendance =====
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff_attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER NOT NULL,
                staff_username TEXT,
                date DATE NOT NULL,
                check_in TEXT,
                check_out TEXT,
                check_in_status TEXT,
                check_out_status TEXT,
                late_minutes INTEGER DEFAULT 0,
                early_leave_minutes INTEGER DEFAULT 0,
                hours_worked REAL DEFAULT 0,
                status TEXT DEFAULT 'absent',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (staff_id) REFERENCES staff (id) ON DELETE CASCADE,
                UNIQUE(staff_id, date)
            )
        ''')
        
        # ===== اضافه کردن ستون‌های missing به staff_attendance =====
        cursor.execute("PRAGMA table_info(staff_attendance)")
        attendance_columns = [col[1] for col in cursor.fetchall()]
        
        if 'staff_username' not in attendance_columns:
            cursor.execute("ALTER TABLE staff_attendance ADD COLUMN staff_username TEXT")
            print("✅ ستون staff_username به staff_attendance اضافه شد")
        
        if 'check_in_status' not in attendance_columns:
            cursor.execute("ALTER TABLE staff_attendance ADD COLUMN check_in_status TEXT")
            print("✅ ستون check_in_status به staff_attendance اضافه شد")
        
        if 'check_out_status' not in attendance_columns:
            cursor.execute("ALTER TABLE staff_attendance ADD COLUMN check_out_status TEXT")
            print("✅ ستون check_out_status به staff_attendance اضافه شد")
        
        if 'late_minutes' not in attendance_columns:
            cursor.execute("ALTER TABLE staff_attendance ADD COLUMN late_minutes INTEGER DEFAULT 0")
            print("✅ ستون late_minutes به staff_attendance اضافه شد")
        
        if 'early_leave_minutes' not in attendance_columns:
            cursor.execute("ALTER TABLE staff_attendance ADD COLUMN early_leave_minutes INTEGER DEFAULT 0")
            print("✅ ستون early_leave_minutes به staff_attendance اضافه شد")
        
        if 'notes' not in attendance_columns:
            cursor.execute("ALTER TABLE staff_attendance ADD COLUMN notes TEXT")
            print("✅ ستون notes به staff_attendance اضافه شد")
        
        # ===== جدول patient_files =====
        cursor.execute('''
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
        ''')
        
        # ===== ایجاد ایندکس‌ها =====
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patients_national_id ON patients(national_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patients_status ON patients(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_dental_charting_patient ON dental_charting(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_invoices_patient ON patient_invoices(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_payments_patient ON patient_payments(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_treatment_plans_patient ON treatment_plans(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_treatment_items_plan ON treatment_plan_items(plan_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_procedure_codes_code ON procedure_codes(code)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_staff_attendance_date ON staff_attendance(date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_staff_attendance_username ON staff_attendance(staff_username)')
        
        # ===== اضافه کردن خدمات پیش‌فرض =====
        cursor.execute("SELECT COUNT(*) FROM dental_services")
        if cursor.fetchone()[0] == 0:
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
            cursor.executemany("INSERT INTO dental_services (service_name, default_price) VALUES (?, ?)", default_services)
        
        conn.commit()
        
        # ایجاد پوشه‌های مورد نیاز
        os.makedirs("patient_files", exist_ok=True)
        os.makedirs("xray_files", exist_ok=True)
        os.makedirs("backups", exist_ok=True)
        
        print("=" * 60)
        print("✅ Database initialized successfully")
        print("✅ تمام جداول اصلی با موفقیت ایجاد شدند")
        print("✅ 35 کد استاندارد درمانی اضافه شد")
        print("✅ ستون‌های جدید به جداول اضافه شدند")
        print("=" * 60)


def init_emr_tables():
    """ایجاد جداول EMR در پایگاه داده (برای سازگاری با فایل emr.py)"""
    init_database()
    print("✅ EMR tables initialized successfully")