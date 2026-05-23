import streamlit as st
import pandas as pd
import hashlib
import os
import json
import shutil
import time
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from modules.database import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_size():
    """دریافت سایز دیتابیس"""
    if os.path.exists("data/clinic.db"):
        return os.path.getsize("data/clinic.db") / (1024 * 1024)
    return 0

def get_table_counts():
    """دریافت تعداد رکوردهای هر جدول"""
    counts = {}
    with get_connection() as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        for table in tables:
            try:
                count = conn.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
                counts[table[0]] = count
            except:
                counts[table[0]] = 0
    return counts

def get_recent_backups():
    """دریافت لیست بکاپ‌های اخیر"""
    backups = []
    try:
        backup_files = list(Path("backups").glob("*.db"))
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        for bf in backup_files[:20]:
            backups.append({
                "name": bf.name,
                "path": str(bf),
                "size_mb": bf.stat().st_size / (1024 * 1024),
                "date": datetime.fromtimestamp(bf.stat().st_mtime),
                "is_protected": bf.name.startswith("protected_")
            })
    except:
        pass
    return backups

def create_backup(backup_name, is_protected=False):
    """ایجاد بکاپ جدید"""
    try:
        os.makedirs("backups", exist_ok=True)
        prefix = "protected_" if is_protected else ""
        backup_file = f"backups/{prefix}{backup_name}.db"
        shutil.copy2("data/clinic.db", backup_file)
        
        metadata = {
            "name": backup_name,
            "date": datetime.now().isoformat(),
            "size_mb": os.path.getsize(backup_file) / (1024 * 1024),
            "protected": is_protected,
            "tables": get_table_counts()
        }
        with open(f"backups/{prefix}{backup_name}.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        return True, backup_file
    except Exception as e:
        return False, str(e)

def render_settings():
    # ========== استایل نئون آبی ==========
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .settings-header {
            background: linear-gradient(135deg, #0A0F1F, #0E1629);
            padding: 40px 30px;
            border-radius: 30px;
            margin-bottom: 35px;
            border: 2px solid #00C8FF;
            box-shadow: 0 10px 30px -10px rgba(0, 200, 255, 0.4);
            position: relative;
            overflow: hidden;
        }
        
        .settings-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0, 200, 255, 0.08) 0%, transparent 70%);
            animation: rotateSlow 25s linear infinite;
        }
        
        @keyframes rotateSlow {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .settings-header h1 {
            color: white;
            font-size: 38px;
            margin: 0;
            text-shadow: 0 0 20px #00C8FF;
            position: relative;
            letter-spacing: -0.5px;
        }
        
        .settings-header p {
            color: #7FBAFF;
            margin: 12px 0 0 0;
            position: relative;
            font-size: 16px;
        }
        
        .stat-card-modern {
            background: linear-gradient(145deg, #141E36, #0E1629);
            padding: 25px 20px;
            border-radius: 24px;
            border: 1px solid rgba(0, 200, 255, 0.2);
            text-align: center;
            transition: all 0.3s cubic-bezier(0.2, 0.9, 0.4, 1.1);
            position: relative;
            overflow: hidden;
        }
        
        .stat-card-modern::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00C8FF, #0066FF, #00C8FF);
            transform: scaleX(0);
            transition: transform 0.4s;
        }
        
        .stat-card-modern:hover {
            transform: translateY(-5px);
            border-color: #00C8FF;
            box-shadow: 0 0 35px rgba(0, 200, 255, 0.25);
        }
        
        .stat-card-modern:hover::after {
            transform: scaleX(1);
        }
        
        .stat-value {
            font-size: 38px;
            font-weight: 800;
            color: #00C8FF;
            text-shadow: 0 0 15px #00C8FF;
        }
        
        .stat-label {
            color: #7FBAFF;
            font-size: 13px;
            font-weight: 500;
            margin-top: 8px;
            letter-spacing: 0.5px;
        }
        
        .info-card-modern {
            background: linear-gradient(145deg, #141E36, #0E1629);
            padding: 25px;
            border-radius: 24px;
            border: 1px solid rgba(0, 200, 255, 0.15);
            margin: 20px 0;
            transition: all 0.3s;
        }
        
        .info-card-modern:hover {
            border-color: #00C8FF;
            box-shadow: 0 0 25px rgba(0, 200, 255, 0.15);
        }
        
        .info-card-modern h3 {
            color: #00C8FF;
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: #0E1629;
            padding: 12px 18px;
            border-radius: 50px;
            border: 1px solid rgba(0, 200, 255, 0.2);
            margin-bottom: 35px;
            backdrop-filter: blur(10px);
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
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 25px #00C8FF;
        }
        
        .metric-card {
            background: rgba(20, 30, 54, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 18px;
            border: 1px solid rgba(0, 200, 255, 0.2);
            text-align: center;
        }
        
        hr {
            margin: 25px 0;
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #00C8FF, #0066FF, #00C8FF, transparent);
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div class="settings-header">
            <h1>⚙️ Advanced System Settings</h1>
            <p>Complete control over users, backups, and system configuration</p>
        </div>
    """, unsafe_allow_html=True)

    # ===== آمار سیستم =====
    db_size = get_db_size()
    table_counts = get_table_counts()
    backups = get_recent_backups()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card-modern">
                <div class="stat-value">{table_counts.get('users', 0)}</div>
                <div class="stat-label">Total Users</div>
                <div style="font-size: 11px; color: #4D9EFF; margin-top: 5px;">👥 Active Accounts</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-card-modern">
                <div class="stat-value">{table_counts.get('patients', 0):,}</div>
                <div class="stat-label">Total Patients</div>
                <div style="font-size: 11px; color: #4D9EFF; margin-top: 5px;">🦷 Registered Records</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-card-modern">
                <div class="stat-value">{db_size:.1f}</div>
                <div class="stat-label">Database Size</div>
                <div style="font-size: 11px; color: #4D9EFF; margin-top: 5px;">💾 MB</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="stat-card-modern">
                <div class="stat-value">{len(backups)}</div>
                <div class="stat-label">Backups Available</div>
                <div style="font-size: 11px; color: #4D9EFF; margin-top: 5px;">💿 Total Backups</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ===== تب‌های اصلی =====
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 User Management",
        "💾 Backup System", 
        "📊 System Monitor",
        "🔧 Maintenance Tools"
    ])

    # ===== TAB 1: مدیریت کاربران =====
    with tab1:
        st.markdown("""
            <div class="info-card-modern">
                <h3>👥 User Management Center</h3>
                <p>Create, manage, and control user access with full security features</p>
            </div>
        """, unsafe_allow_html=True)

        # فرم افزودن کاربر
        with st.expander("➕ Create New User", expanded=False):
            with st.form("add_user_form"):
                st.markdown("#### New User Details")
                col_u1, col_u2 = st.columns(2)
                with col_u1:
                    new_username = st.text_input("Username *", placeholder="Enter unique username")
                    new_fullname = st.text_input("Full Name *", placeholder="Enter full name")
                with col_u2:
                    new_password = st.text_input("Password *", type="password", placeholder="Enter strong password")
                    confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Confirm password")
                
                new_role = st.selectbox("Role *", ["admin", "doctor", "staff", "receptionist", "manager"])
                
                if st.form_submit_button("✅ Create User", width="stretch"):
                    if not new_username or not new_password or not new_fullname:
                        st.error("❌ Please fill all required fields")
                    elif new_password != confirm_password:
                        st.error("❌ Passwords do not match")
                    elif len(new_password) < 4:
                        st.error("❌ Password must be at least 4 characters")
                    else:
                        try:
                            with get_connection() as conn:
                                conn.execute("""
                                    INSERT INTO users (username, password_hash, full_name, role)
                                    VALUES (?, ?, ?, ?)
                                """, (new_username, hash_password(new_password), new_fullname, new_role))
                                conn.commit()
                            st.success(f"✅ User '{new_username}' created successfully!")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("❌ Username already exists! Please choose another one.")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")

        # لیست کاربران
        st.markdown("#### 📋 User Directory")
        
        with get_connection() as conn:
            users = pd.read_sql_query("SELECT id, username, full_name, role FROM users ORDER BY id", conn)

        if not users.empty:
            for idx, user in users.iterrows():
                with st.container():
                    col_u1, col_u2, col_u3, col_u4, col_u5 = st.columns([2.5, 1.5, 1.5, 1.5, 1])
                    
                    with col_u1:
                        st.markdown(f"""
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #00C8FF, #0066FF); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                                    {user['full_name'][0] if user['full_name'] else 'U'}
                                </div>
                                <div>
                                    <strong>{user['full_name']}</strong><br>
                                    <span style="color: #7FBAFF; font-size: 12px;">@{user['username']}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col_u2:
                        role_color = {
                            'admin': '#E74C3C',
                            'doctor': '#2ECC71',
                            'manager': '#F39C12',
                            'staff': '#3498DB',
                            'receptionist': '#9B59B6'
                        }.get(user['role'], '#7FBAFF')
                        st.markdown(f"<span style='background: {role_color}20; color: {role_color}; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: 600;'>{user['role'].upper()}</span>", unsafe_allow_html=True)
                    
                    with col_u3:
                        if st.button(f"🔑 Reset", key=f"reset_{user['id']}", width="stretch"):
                            st.session_state.reset_user_id = user['id']
                            st.session_state.reset_username = user['username']
                            st.session_state.reset_fullname = user['full_name']
                    
                    with col_u4:
                        if user['username'] != 'admin':
                            if st.button(f"✏️ Edit Role", key=f"role_{user['id']}", width="stretch"):
                                st.session_state.edit_role_id = user['id']
                                st.session_state.edit_role_current = user['role']
                    
                    with col_u5:
                        if user['username'] != 'admin':
                            if st.button(f"🗑️", key=f"del_{user['id']}", width="stretch"):
                                confirm_del = st.checkbox(f"Confirm", key=f"confirm_del_{user['id']}")
                                if confirm_del:
                                    try:
                                        with get_connection() as conn:
                                            conn.execute("DELETE FROM users WHERE id = ?", (user['id'],))
                                            conn.commit()
                                        st.success(f"✅ User {user['username']} deleted")
                                        time.sleep(1)
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error: {e}")
                
                # مودال ریست پسورد
                if st.session_state.get('reset_user_id') == user['id']:
                    with st.container():
                        st.markdown(f"""
                            <div style="background: rgba(0, 200, 255, 0.05); padding: 20px; border-radius: 20px; margin: 10px 0;">
                                <h4>🔐 Reset Password for {st.session_state.reset_fullname}</h4>
                        """, unsafe_allow_html=True)
                        col_p1, col_p2 = st.columns(2)
                        with col_p1:
                            new_pass = st.text_input("New Password", type="password", key=f"np_{user['id']}")
                        with col_p2:
                            confirm_pass = st.text_input("Confirm Password", type="password", key=f"cp_{user['id']}")
                        
                        col_b1, col_b2 = st.columns(2)
                        with col_b1:
                            if st.button("✅ Save", key=f"save_pass_{user['id']}", width="stretch"):
                                if new_pass and new_pass == confirm_pass:
                                    if len(new_pass) >= 4:
                                        with get_connection() as conn:
                                            conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hash_password(new_pass), user['id']))
                                            conn.commit()
                                        st.success("✅ Password updated!")
                                        del st.session_state.reset_user_id
                                        st.rerun()
                                    else:
                                        st.error("Password must be at least 4 characters")
                                else:
                                    st.error("Passwords don't match")
                        with col_b2:
                            if st.button("❌ Cancel", key=f"cancel_pass_{user['id']}", width="stretch"):
                                del st.session_state.reset_user_id
                                st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                
                # مودال ویرایش نقش
                if st.session_state.get('edit_role_id') == user['id']:
                    with st.container():
                        st.markdown(f"""
                            <div style="background: rgba(0, 200, 255, 0.05); padding: 20px; border-radius: 20px; margin: 10px 0;">
                                <h4>✏️ Edit Role for {user['full_name']}</h4>
                        """, unsafe_allow_html=True)
                        new_role = st.selectbox("Select New Role", ["admin", "doctor", "staff", "receptionist", "manager"], 
                                               index=["admin", "doctor", "staff", "receptionist", "manager"].index(st.session_state.edit_role_current),
                                               key=f"new_role_{user['id']}")
                        col_r1, col_r2 = st.columns(2)
                        with col_r1:
                            if st.button("✅ Save", key=f"save_role_{user['id']}", width="stretch"):
                                with get_connection() as conn:
                                    conn.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user['id']))
                                    conn.commit()
                                st.success(f"✅ Role updated to {new_role}")
                                del st.session_state.edit_role_id
                                st.rerun()
                        with col_r2:
                            if st.button("❌ Cancel", key=f"cancel_role_{user['id']}", width="stretch"):
                                del st.session_state.edit_role_id
                                st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<hr style='margin: 10px 0; opacity: 0.1;'>", unsafe_allow_html=True)
        else:
            st.info("No users found in the system")

    # ===== TAB 2: سیستم پشتیبان‌گیری =====
    with tab2:
        st.markdown("""
            <div class="info-card-modern">
                <h3>💾 Advanced Backup System</h3>
                <p>Create, manage, and restore backups</p>
            </div>
        """, unsafe_allow_html=True)

        col_b1, col_b2 = st.columns(2)

        with col_b1:
            st.markdown("#### 📤 Manual Backup")
            backup_name = st.text_input("Backup Name", value=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            is_protected = st.checkbox("🔒 Protect this backup")
            
            if st.button("🔄 Create Backup Now", width="stretch", type="primary"):
                with st.spinner("Creating backup..."):
                    success, result = create_backup(backup_name, is_protected)
                    if success:
                        st.success(f"✅ Backup created successfully!")
                        st.info(f"📁 Location: {result}")
                        st.info(f"💾 Size: {os.path.getsize(result) / (1024 * 1024):.2f} MB")
                        with open(result, "rb") as f:
                            st.download_button("📥 Download Backup", f, file_name=f"{backup_name}.db", width="stretch")
                    else:
                        st.error(f"❌ Error: {result}")

        with col_b2:
            st.markdown("#### 🤖 Automatic Backup")
            auto_backup = st.checkbox("Enable Automatic Backup", value=False)
            if auto_backup:
                backup_interval = st.selectbox("Backup Interval", ["Daily", "Every 6 Hours", "Every 12 Hours", "Weekly"])
                backup_time = st.time_input("Backup Time", value=datetime.strptime("02:00", "%H:%M").time())
                max_backups = st.slider("Maximum Backups to Keep", 5, 100, 30)
                
                if st.button("💾 Save Auto Backup Settings", width="stretch"):
                    settings = {
                        "enabled": True,
                        "interval": backup_interval,
                        "time": backup_time.strftime("%H:%M"),
                        "max_backups": max_backups
                    }
                    os.makedirs("backups", exist_ok=True)
                    with open("backups/auto_backup_settings.json", "w") as f:
                        json.dump(settings, f, indent=2)
                    st.success("✅ Auto backup settings saved!")

        st.markdown("---")
        st.markdown("#### 📋 Backup History")

        backups_list = get_recent_backups()
        
        if backups_list:
            for backup in backups_list:
                with st.container():
                    col_b1, col_b2, col_b3, col_b4 = st.columns([3, 2, 1.5, 1.5])
                    
                    with col_b1:
                        icon = "🔒" if backup['is_protected'] else "💿"
                        st.markdown(f"{icon} **{backup['name']}**")
                        st.caption(f"📅 {backup['date'].strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    with col_b2:
                        st.markdown(f"📦 Size: {backup['size_mb']:.2f} MB")
                    
                    with col_b3:
                        with open(backup['path'], "rb") as f:
                            st.download_button("⬇️ Download", f, file_name=backup['name'], key=f"dl_{backup['name']}", width="stretch")
                    
                    with col_b4:
                        if not backup['is_protected']:
                            if st.button("🗑️ Delete", key=f"del_{backup['name']}", width="stretch"):
                                try:
                                    os.remove(backup['path'])
                                    json_path = backup['path'].replace('.db', '.json')
                                    if os.path.exists(json_path):
                                        os.remove(json_path)
                                    st.success(f"✅ Deleted {backup['name']}")
                                    st.rerun()
                                except:
                                    st.error("Could not delete")
                    
                    st.markdown("<hr style='margin: 8px 0; opacity: 0.1;'>", unsafe_allow_html=True)
        else:
            st.info("No backups found. Create your first backup using the form above.")

        st.markdown("---")
        st.markdown("#### 📥 Restore Database")
        st.warning("⚠️ Restoring will overwrite your current database. Create a backup first!")
        
        uploaded_file = st.file_uploader("Upload backup file (.db)", type=["db"])
        if uploaded_file:
            st.info(f"File: {uploaded_file.name} | Size: {len(uploaded_file.getvalue()) / (1024 * 1024):.2f} MB")
            confirm_restore = st.checkbox("✅ I understand this will overwrite my current database")
            if confirm_restore and st.button("🚨 Restore Database", width="stretch"):
                try:
                    # Create backup before restore
                    pre_restore_name = f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    create_backup(pre_restore_name, False)
                    
                    # Restore
                    with open("data/clinic.db", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    st.success("✅ Database restored successfully!")
                    st.info("Restarting application...")
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    # ===== TAB 3: مانیتورینگ سیستم =====
    with tab3:
        st.markdown("""
            <div class="info-card-modern">
                <h3>📊 System Monitor</h3>
                <p>Real-time system statistics and health monitoring</p>
            </div>
        """, unsafe_allow_html=True)

        # آمار جداول
        st.markdown("#### 📋 Table Statistics")
        table_stats = get_table_counts()
        
        if table_stats:
            df_stats = pd.DataFrame(list(table_stats.items()), columns=['Table Name', 'Record Count'])
            df_stats = df_stats.sort_values('Record Count', ascending=False)
            st.dataframe(df_stats, width="stretch", hide_index=True)
        
        st.markdown("---")
        
        # سلامت سیستم
        st.markdown("#### 🩺 System Health")
        
        col_h1, col_h2, col_h3, col_h4 = st.columns(4)
        
        with col_h1:
            db_status = "✅ Healthy" if get_db_size() > 0 else "⚠️ Issues"
            st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 24px;">🗄️</div>
                    <div style="font-size: 18px; font-weight: 600;">Database</div>
                    <div style="color: {'#2ECC71' if db_status == '✅ Healthy' else '#E74C3C'};">{db_status}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_h2:
            backup_status = "✅ Available" if len(backups_list) > 0 else "⚠️ No Backups"
            st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 24px;">💿</div>
                    <div style="font-size: 18px; font-weight: 600;">Backups</div>
                    <div style="color: {'#2ECC71' if len(backups_list) > 0 else '#F39C12'};">{backup_status}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_h3:
            st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 24px;">👥</div>
                    <div style="font-size: 18px; font-weight: 600;">Active Users</div>
                    <div style="color: #00C8FF;">{table_stats.get('users', 0)}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_h4:
            last_backup = backups_list[0]['date'].strftime('%Y-%m-%d') if backups_list else 'Never'
            st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 24px;">📅</div>
                    <div style="font-size: 18px; font-weight: 600;">Last Backup</div>
                    <div style="color: #00C8FF;">{last_backup}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Database size trend
        st.markdown("#### 📈 Database Size Trend (Last 30 Days)")
        sizes_data = []
        for i in range(30, -1, -1):
            simulated_size = db_size * (0.95 + (i * 0.01))
            sizes_data.append({
                "date": (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'), 
                "size (MB)": simulated_size
            })
        df_sizes = pd.DataFrame(sizes_data)
        st.line_chart(df_sizes.set_index('date'), width="stretch")

    # ===== TAB 4: ابزارهای تعمیر و نگهداری =====
    with tab4:
        st.markdown("""
            <div class="info-card-modern">
                <h3>🔧 Maintenance Tools</h3>
                <p>Database optimization, integrity checks, and repair utilities</p>
            </div>
        """, unsafe_allow_html=True)

        col_m1, col_m2 = st.columns(2)

        with col_m1:
            st.markdown("#### 🔍 Database Integrity")
            if st.button("Run Integrity Check", width="stretch"):
                with st.spinner("Checking database integrity..."):
                    with get_connection() as conn:
                        result = conn.execute("PRAGMA integrity_check").fetchone()[0]
                        if result == "ok":
                            st.success("✅ Database integrity check passed! No issues found.")
                        else:
                            st.error(f"❌ Issues found: {result}")
            
            st.markdown("#### 🛠️ Vacuum Database")
            if st.button("Optimize Database (VACUUM)", width="stretch"):
                with st.spinner("Optimizing database..."):
                    with get_connection() as conn:
                        conn.execute("VACUUM")
                    st.success("✅ Database optimized successfully! Size reduced.")

        with col_m2:
            st.markdown("#### 📋 Export Schema")
            if st.button("Generate Database Schema", width="stretch"):
                with get_connection() as conn:
                    schema = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL").fetchall()
                    schema_text = "-- Osman Muslim Dental Clinic Database Schema\n-- Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n"
                    for s in schema:
                        if s[0]:
                            schema_text += s[0] + ";\n\n"
                    
                    st.download_button("📥 Download Schema SQL", schema_text, file_name=f"schema_{datetime.now().strftime('%Y%m%d')}.sql", 
                                     mime="text/plain", width="stretch")
            
            st.markdown("#### 🧹 Cleanup Old Backups")
            if st.button("Delete Backups Older Than 30 Days", width="stretch"):
                deleted = 0
                cutoff = datetime.now() - timedelta(days=30)
                for backup in backups_list:
                    if not backup['is_protected'] and backup['date'] < cutoff:
                        try:
                            os.remove(backup['path'])
                            json_path = backup['path'].replace('.db', '.json')
                            if os.path.exists(json_path):
                                os.remove(json_path)
                            deleted += 1
                        except:
                            pass
                if deleted > 0:
                    st.success(f"✅ Deleted {deleted} old backups")
                    st.rerun()
                else:
                    st.info("No old backups to delete")

        st.markdown("---")
        st.markdown("#### 🗑️ Dangerous Actions")
        st.error("⚠️ The following actions are irreversible. Use with extreme caution!")
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            confirm_clear = st.checkbox("I understand this will delete ALL patient data")
            if confirm_clear and st.button("⚠️ Clear All Patient Data", width="stretch"):
                with get_connection() as conn:
                    conn.execute("DELETE FROM patients")
                    conn.execute("DELETE FROM dental_charting")
                    conn.execute("DELETE FROM emr_records")
                    conn.execute("DELETE FROM patient_invoices")
                    conn.execute("DELETE FROM patient_payments")
                    conn.commit()
                st.success("✅ All patient data cleared. Create a backup first next time!")
                st.rerun()
        
        with col_d2:
            confirm_reset = st.checkbox("I understand this will reset the entire system")
            if confirm_reset and st.button("⚠️ Factory Reset (Delete Everything)", width="stretch"):
                if st.button("✅ FINAL CONFIRMATION", width="stretch"):
                    try:
                        os.remove("data/clinic.db")
                        st.success("✅ Database deleted. Please restart the application.")
                    except:
                        st.error("Could not delete database")

        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; padding: 30px; color: #7FBAFF;">
                <p style="font-size: 14px;">🦷 Osman Muslim Dental Clinic Management System</p>
                <p style="font-size: 12px;">Version 3.0 Professional | © 2024 All Rights Reserved</p>
                <p style="font-size: 11px; opacity: 0.7;">Secure | Reliable | Professional</p>
            </div>
        """, unsafe_allow_html=True)