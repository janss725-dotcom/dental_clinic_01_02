import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.database import get_connection

# ============================================
# توابع کمکی برای دریافت داده از دیتابیس
# ============================================

def get_patient_plans(patient_id):
    """دریافت لیست طرح‌های درمان یک بیمار"""
    with get_connection() as conn:
        return pd.read_sql_query("""
            SELECT 
                tp.*, 
                COUNT(tpi.id) as items_count,
                SUM(CASE WHEN tpi.status = 'completed' THEN 1 ELSE 0 END) as completed_count
            FROM treatment_plans tp
            LEFT JOIN treatment_plan_items tpi ON tp.id = tpi.plan_id
            WHERE tp.patient_id = ?
            GROUP BY tp.id
            ORDER BY tp.plan_date DESC
        """, conn, params=(patient_id,))

def get_plan_items(plan_id):
    """دریافت آیتم‌های یک طرح درمان"""
    with get_connection() as conn:
        return pd.read_sql_query("""
            SELECT * FROM treatment_plan_items 
            WHERE plan_id = ? 
            ORDER BY id
        """, conn, params=(plan_id,))

def get_procedure_codes():
    """دریافت لیست کدهای درمانی"""
    with get_connection() as conn:
        return pd.read_sql_query("""
            SELECT * FROM procedure_codes 
            WHERE is_active = 1 
            ORDER BY category, name
        """, conn)

# ============================================
# توابع رندرینگ
# ============================================

def render_treatment_plan_selector():
    """صفحه اصلی مدیریت طرح درمان"""
    
    # ========== استایل اختصاصی ==========
    st.markdown("""
        <style>
        .plan-header {
            background: linear-gradient(135deg, #0A0F1F, #0E1629);
            padding: 35px 25px;
            border-radius: 25px;
            margin-bottom: 30px;
            border: 2px solid #00C8FF;
            text-align: center;
            box-shadow: 0 10px 25px -10px rgba(0, 200, 255, 0.3);
        }
        .plan-header h1 {
            color: white;
            font-size: 36px;
            margin: 0;
            text-shadow: 0 0 15px #00C8FF;
        }
        .plan-header p {
            color: #7FBAFF;
            margin: 10px 0 0 0;
        }
        .plan-card {
            background: linear-gradient(135deg, #141E36, #0E1629);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid #00C8FF;
            transition: all 0.3s;
        }
        .plan-card:hover {
            transform: translateX(5px);
            box-shadow: 0 0 20px rgba(0, 200, 255, 0.2);
        }
        .plan-status-active {
            background: #2ECC71;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .plan-status-completed {
            background: #3498DB;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .plan-status-cancelled {
            background: #E74C3C;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .priority-high {
            color: #E74C3C;
            font-weight: 600;
        }
        .priority-normal {
            color: #F39C12;
            font-weight: 600;
        }
        .priority-low {
            color: #2ECC71;
            font-weight: 600;
        }
        .stat-box {
            background: linear-gradient(135deg, #141E36, #0E1629);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            border: 1px solid #00C8FF;
        }
        .stat-number {
            font-size: 28px;
            font-weight: 700;
            color: #00C8FF;
        }
        .stat-label {
            color: #7FBAFF;
            font-size: 12px;
        }
        .item-row {
            background: rgba(20, 30, 54, 0.5);
            border-radius: 15px;
            padding: 12px;
            margin-bottom: 8px;
            transition: all 0.2s;
        }
        .item-row:hover {
            background: rgba(20, 30, 54, 0.8);
            border-left: 3px solid #00C8FF;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="plan-header">
            <h1>📋 Treatment Plan Management</h1>
            <p>Create, manage and track patient treatment plans</p>
        </div>
    """, unsafe_allow_html=True)
    
    # دریافت لیست بیماران
    with get_connection() as conn:
        patients = pd.read_sql_query("SELECT id, first_name, last_name, age, phone FROM patients ORDER BY last_name", conn)
    
    if patients.empty:
        st.warning("⚠️ No patients found. Please add a patient first.")
        if st.button("➕ Add New Patient", width="stretch"):
            st.session_state.menu = "👨‍⚕️ Add New Patient"
            st.rerun()
        return
    
    # انتخاب بیمار
    st.subheader("👤 Select Patient")
    col_p1, col_p2 = st.columns([3, 1])
    
    with col_p1:
        patient_options = {f"{row['first_name']} {row['last_name']} (ID: {row['id']})": row['id'] 
                          for _, row in patients.iterrows()}
        selected_patient = st.selectbox("", list(patient_options.keys()), key="plan_patient")
    
    with col_p2:
        if st.button("🔄 Refresh", width="stretch"):
            st.rerun()
    
    patient_id = patient_options[selected_patient]
    patient = patients[patients['id'] == patient_id].iloc[0]
    
    st.markdown(f"""
        <div style="background: rgba(0, 200, 255, 0.1); padding: 15px; border-radius: 15px; margin: 15px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: #00C8FF;">👤 Patient:</span>
                    <strong style="color: white;"> {patient['first_name']} {patient['last_name']}</strong>
                    <span style="color: #7FBAFF; margin-left: 20px;">Age: {patient['age']}</span>
                    <span style="color: #7FBAFF; margin-left: 20px;">Phone: {patient['phone']}</span>
                </div>
                <div>
                    <span style="background: #00C8FF20; color: #00C8FF; padding: 5px 15px; border-radius: 20px;">ID: #{patient_id}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # تب‌های اصلی
    tab_list, tab_create, tab_stats = st.tabs([
        "📋 Existing Plans",
        "➕ Create New Plan",
        "📊 Statistics & Reports"
    ])
    
    # ===== TAB 1: لیست طرح‌های موجود =====
    with tab_list:
        plans = get_patient_plans(patient_id)
        
        if plans.empty:
            st.info("📭 No treatment plans found for this patient. Create a new plan using the 'Create New Plan' tab.")
        else:
            st.markdown(f"### 📋 Treatment Plans ({len(plans)} total)")
            
            for idx, plan in plans.iterrows():
                # تعیین کلاس وضعیت
                status_class = "plan-status-active"
                if plan['plan_status'] == 'completed':
                    status_class = "plan-status-completed"
                elif plan['plan_status'] == 'cancelled':
                    status_class = "plan-status-cancelled"
                
                # تعیین کلاس اولویت
                priority_value = plan['priority'] if 'priority' in plan and pd.notna(plan['priority']) else 'normal'
                priority_class = "priority-normal"
                if priority_value == 'high':
                    priority_class = "priority-high"
                elif priority_value == 'low':
                    priority_class = "priority-low"
                
                priority_text = {"high": "🔴 High", "normal": "🟡 Normal", "low": "🟢 Low"}.get(priority_value, "Normal")
                
                with st.container():
                    col_p1, col_p2, col_p3, col_p4 = st.columns([3, 1.5, 1.5, 1])
                    
                    with col_p1:
                        st.markdown(f"""
                            <div class="plan-card">
                                <div style="display: flex; justify-content: space-between; align-items: start;">
                                    <div>
                                        <strong style="color: white; font-size: 16px;">{plan['plan_name']}</strong><br>
                                        <span style="color: #7FBAFF; font-size: 12px;">📅 {plan['plan_date'][:10] if plan['plan_date'] else 'N/A'}</span>
                                    </div>
                                    <div>
                                        <span class="{status_class}">{plan['plan_status'].upper()}</span>
                                    </div>
                                </div>
                                <div style="margin-top: 10px;">
                                    <span class="{priority_class}">{priority_text}</span>
                                    <span style="color: #7FBAFF; margin-left: 15px;">💰 {float(plan['total_estimated_cost'] or 0):,.0f} AFN</span>
                                    <span style="color: #7FBAFF; margin-left: 15px;">✅ {int(plan['completed_count'] or 0)}/{int(plan['items_count'] or 0)} completed</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col_p2:
                        if st.button("👁️ View", key=f"view_{plan['id']}", width="stretch"):
                            st.session_state.selected_plan_id = plan['id']
                            st.session_state.view_plan = True
                    
                    with col_p3:
                        if plan['plan_status'] != 'completed':
                            if st.button("✓ Complete", key=f"complete_{plan['id']}", width="stretch"):
                                with get_connection() as conn:
                                    conn.execute("""
                                        UPDATE treatment_plans 
                                        SET plan_status = 'completed', is_completed = 1, completed_date = CURRENT_TIMESTAMP
                                        WHERE id = ?
                                    """, (plan['id'],))
                                    conn.commit()
                                st.success("Plan marked as completed!")
                                st.rerun()
                    
                    with col_p4:
                        if plan['plan_status'] == 'active':
                            if st.button("🗑️", key=f"del_plan_{plan['id']}", width="stretch"):
                                confirm = st.checkbox(f"Confirm", key=f"confirm_del_plan_{plan['id']}")
                                if confirm:
                                    with get_connection() as conn:
                                        conn.execute("DELETE FROM treatment_plan_items WHERE plan_id = ?", (plan['id'],))
                                        conn.execute("DELETE FROM treatment_plans WHERE id = ?", (plan['id'],))
                                        conn.commit()
                                    st.success("Plan deleted!")
                                    st.rerun()
                    
                    st.markdown("<hr style='margin: 10px 0; opacity: 0.1;'>", unsafe_allow_html=True)
            
            # نمایش جزئیات طرح انتخاب شده
            if st.session_state.get('view_plan') and st.session_state.get('selected_plan_id'):
                st.markdown("---")
                st.markdown("### 🔍 Plan Details")
                render_plan_details(st.session_state.selected_plan_id)
    
    # ===== TAB 2: ایجاد طرح جدید =====
    with tab_create:
        st.markdown("### ➕ Create New Treatment Plan")
        
        with st.form("create_plan_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                plan_name = st.text_input("Plan Name *", placeholder="e.g., Comprehensive Treatment Plan")
                priority = st.selectbox("Priority", ["normal", "high", "low"], 
                                       format_func=lambda x: {"normal": "🟡 Normal", "high": "🔴 High", "low": "🟢 Low"}[x])
                estimated_start = st.date_input("Estimated Start Date", value=datetime.now())
            
            with col2:
                notes = st.text_area("Notes", placeholder="Additional notes about this treatment plan...", height=100)
                estimated_end = st.date_input("Estimated End Date", value=datetime.now() + timedelta(days=90))
            
            submitted = st.form_submit_button("✅ Create Plan", width="stretch", type="primary")
            
            if submitted:
                if not plan_name:
                    st.error("Please enter a plan name")
                else:
                    try:
                        with get_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO treatment_plans 
                                (patient_id, plan_name, priority, estimated_start_date, estimated_end_date, notes, plan_status)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (patient_id, plan_name, priority, estimated_start.strftime('%Y-%m-%d'),
                                  estimated_end.strftime('%Y-%m-%d'), notes, 'active'))
                            plan_id = cursor.lastrowid
                            conn.commit()
                        
                        st.success(f"✅ Plan '{plan_name}' created successfully!")
                        st.session_state.new_plan_id = plan_id
                        st.session_state.add_items_to_plan = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        # فرم افزودن آیتم به طرح جدید
        if st.session_state.get('add_items_to_plan') and st.session_state.get('new_plan_id'):
            st.markdown("---")
            st.markdown("### ➕ Add Treatment Items")
            render_add_items_to_plan(st.session_state.new_plan_id, patient_id)
    
    # ===== TAB 3: آمار و گزارشات =====
    with tab_stats:
        st.markdown("### 📊 Treatment Plan Statistics")
        
        plans = get_patient_plans(patient_id)
        
        if plans.empty:
            st.info("No data available for this patient")
        else:
            # آمار کلی
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            
            with col_s1:
                st.markdown(f"""
                    <div class="stat-box">
                        <div class="stat-number">{len(plans)}</div>
                        <div class="stat-label">Total Plans</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_s2:
                active_plans = len(plans[plans['plan_status'] == 'active'])
                st.markdown(f"""
                    <div class="stat-box">
                        <div class="stat-number">{active_plans}</div>
                        <div class="stat-label">Active Plans</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_s3:
                completed_plans = len(plans[plans['plan_status'] == 'completed'])
                st.markdown(f"""
                    <div class="stat-box">
                        <div class="stat-number">{completed_plans}</div>
                        <div class="stat-label">Completed Plans</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_s4:
                total_cost = plans['total_estimated_cost'].sum()
                st.markdown(f"""
                    <div class="stat-box">
                        <div class="stat-number">{total_cost:,.0f}</div>
                        <div class="stat-label">Total Cost (AFN)</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("#### 📊 Plan Details")
            
            # نمایش جدول طرح‌ها
            display_cols = ['plan_name', 'plan_status', 'plan_date', 'total_estimated_cost', 'items_count', 'completed_count']
            if 'priority' in plans.columns:
                display_cols.insert(2, 'priority')
            
            display_df = plans[display_cols].copy()
            column_names = {
                'plan_name': 'Plan Name',
                'plan_status': 'Status',
                'priority': 'Priority',
                'plan_date': 'Created Date',
                'total_estimated_cost': 'Estimated Cost',
                'items_count': 'Items',
                'completed_count': 'Completed'
            }
            display_df = display_df.rename(columns=column_names)
            st.dataframe(display_df, width="stretch", hide_index=True)
            
            # دانلود گزارش
            st.markdown("---")
            st.markdown("#### 📥 Export Report")
            
            if st.button("📄 Generate Full Report", width="stretch"):
                report_data = []
                for _, plan in plans.iterrows():
                    report_data.append({
                        "Plan Name": plan['plan_name'],
                        "Status": plan['plan_status'],
                        "Priority": plan['priority'] if 'priority' in plan else 'normal',
                        "Created Date": plan['plan_date'][:10] if plan['plan_date'] else '',
                        "Estimated Cost": float(plan['total_estimated_cost'] or 0),
                        "Items Count": int(plan['items_count'] or 0),
                        "Completed Items": int(plan['completed_count'] or 0)
                    })
                
                df_report = pd.DataFrame(report_data)
                csv = df_report.to_csv(index=False)
                st.download_button("📥 Download CSV Report", csv, file_name=f"treatment_plan_report_{patient_id}.csv", 
                                 mime="text/csv", width="stretch")

def render_plan_details(plan_id):
    """نمایش جزئیات یک طرح درمان"""
    
    with get_connection() as conn:
        plan = pd.read_sql_query("SELECT * FROM treatment_plans WHERE id = ?", conn, params=(plan_id,)).iloc[0]
        items = pd.read_sql_query("SELECT * FROM treatment_plan_items WHERE plan_id = ? ORDER BY id", conn, params=(plan_id,))
    
    # اطلاعات طرح
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Plan Name", plan['plan_name'])
    with col2:
        priority_value = plan['priority'] if 'priority' in plan and pd.notna(plan['priority']) else 'normal'
        priority_text = {"high": "High", "normal": "Normal", "low": "Low"}.get(priority_value, "Normal")
        st.metric("Priority", priority_text)
    with col3:
        st.metric("Status", plan['plan_status'].capitalize())
    with col4:
        st.metric("Total Cost", f"{float(plan['total_estimated_cost'] or 0):,.0f} AFN")
    
    st.markdown("---")
    
    # لیست آیتم‌ها
    st.markdown("#### 🦷 Treatment Items")
    
    if items.empty:
        st.info("No items added to this plan yet.")
        
        if st.button("➕ Add Items to This Plan", width="stretch"):
            st.session_state.add_items_to_existing = plan_id
            st.rerun()
    else:
        for idx, item in items.iterrows():
            with st.container():
                col_i1, col_i2, col_i3, col_i4, col_i5 = st.columns([2.5, 1.5, 1.5, 1.5, 1])
                
                with col_i1:
                    tooth_text = f"🦷 Tooth {int(item['tooth_number'])}" if pd.notna(item['tooth_number']) and item['tooth_number'] else "📋 General"
                    st.markdown(f"""
                        <div class="item-row">
                            <strong>{item['procedure_name']}</strong><br>
                            <span style="color: #7FBAFF; font-size: 12px;">{tooth_text}</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_i2:
                    item_status = item['status'] if 'status' in item and pd.notna(item['status']) else 'planned'
                    status_color = {
                        'planned': '#F39C12',
                        'in_progress': '#3498DB',
                        'completed': '#2ECC71',
                        'cancelled': '#E74C3C'
                    }.get(item_status, '#7FBAFF')
                    st.markdown(f"<span style='color: {status_color};'>{item_status.replace('_', ' ').title()}</span>", unsafe_allow_html=True)
                
                with col_i3:
                    st.markdown(f"💰 {float(item['estimated_cost'] or 0):,.0f} AFN")
                
                with col_i4:
                    if item_status != 'completed':
                        if st.button(f"✓ Complete", key=f"complete_item_{item['id']}", width="stretch"):
                            with get_connection() as conn:
                                conn.execute("""
                                    UPDATE treatment_plan_items 
                                    SET status = 'completed', completed_date = CURRENT_TIMESTAMP
                                    WHERE id = ?
                                """, (item['id'],))
                                conn.commit()
                            st.success("Item completed!")
                            st.rerun()
                
                with col_i5:
                    if st.button(f"🗑️", key=f"del_item_{item['id']}", width="stretch"):
                        with get_connection() as conn:
                            conn.execute("DELETE FROM treatment_plan_items WHERE id = ?", (item['id'],))
                            conn.commit()
                        st.rerun()
                
                st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)
        
        if st.button("➕ Add More Items", width="stretch"):
            st.session_state.add_items_to_existing = plan_id
            st.rerun()
    
    # فرم افزودن آیتم به طرح موجود
    if st.session_state.get('add_items_to_existing') == plan_id:
        st.markdown("---")
        st.markdown("### ➕ Add New Treatment Item")
        
        with st.form(f"add_item_form_{plan_id}"):
            col_a1, col_a2 = st.columns(2)
            
            with col_a1:
                procedure_codes = get_procedure_codes()
                procedure_options = {f"{row['code']} - {row['name']} ({row['category']})": {
                    'name': row['name'],
                    'code': row['code'],
                    'category': row['category'],
                    'cost': row['default_cost']
                } for _, row in procedure_codes.iterrows()}
                
                selected_proc = st.selectbox("Select Procedure", [""] + list(procedure_options.keys()))
                
                if selected_proc:
                    proc_data = procedure_options[selected_proc]
                    procedure_name = proc_data['name']
                    estimated_cost = proc_data['cost']
                else:
                    procedure_name = st.text_input("Procedure Name")
                    estimated_cost = st.number_input("Estimated Cost (AFN)", min_value=0, step=100, value=0)
            
            with col_a2:
                tooth_number = st.number_input("Tooth Number (Optional)", min_value=1, max_value=32, step=1, value=1)
                notes = st.text_area("Notes", placeholder="Additional notes about this procedure...", height=80)
            
            if st.form_submit_button("➕ Add to Plan", width="stretch", type="primary"):
                if procedure_name:
                    with get_connection() as conn:
                        conn.execute("""
                            INSERT INTO treatment_plan_items (plan_id, tooth_number, procedure_name, estimated_cost, notes, status)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (plan_id, tooth_number, procedure_name, estimated_cost, notes, 'planned'))
                        
                        conn.execute("""
                            UPDATE treatment_plans 
                            SET total_estimated_cost = COALESCE((SELECT SUM(estimated_cost) FROM treatment_plan_items WHERE plan_id = ?), 0)
                            WHERE id = ?
                        """, (plan_id, plan_id))
                        conn.commit()
                    
                    st.success(f"✅ '{procedure_name}' added to plan!")
                    st.rerun()
                else:
                    st.error("Please enter a procedure name")
        
        if st.button("❌ Close", width="stretch"):
            del st.session_state.add_items_to_existing
            st.rerun()

def render_add_items_to_plan(plan_id, patient_id):
    """فرم افزودن آیتم به طرح جدید"""
    
    with st.form(f"add_items_form_{plan_id}"):
        st.markdown("#### Select Treatment Items")
        
        procedure_codes = get_procedure_codes()
        
        categories = procedure_codes['category'].unique()
        
        selected_items = []
        total_cost = 0
        
        for category in categories:
            st.markdown(f"**{category}**")
            cat_items = procedure_codes[procedure_codes['category'] == category]
            
            cols = st.columns(2)
            for idx, (_, item) in enumerate(cat_items.iterrows()):
                with cols[idx % 2]:
                    col_check, col_info = st.columns([1, 4])
                    with col_check:
                        add = st.checkbox("", key=f"add_{item['code']}")
                    with col_info:
                        st.markdown(f"**{item['code']} - {item['name']}**")
                        st.caption(f"💰 {item['default_cost']:,.0f} AFN | {item['description']}")
                    
                    if add:
                        selected_items.append({
                            'name': item['name'],
                            'code': item['code'],
                            'category': item['category'],
                            'cost': item['default_cost']
                        })
                        total_cost += item['default_cost']
            
            st.markdown("<hr style='margin: 15px 0; opacity: 0.1;'>", unsafe_allow_html=True)
        
        if selected_items:
            st.markdown("---")
            st.markdown("#### 📋 Selected Items Summary")
            
            for item in selected_items:
                st.markdown(f"- {item['name']}: {item['cost']:,.0f} AFN")
            
            st.markdown(f"**Total Estimated Cost: {total_cost:,.0f} AFN**")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.form_submit_button("💾 Save All Items", width="stretch", type="primary"):
                if selected_items:
                    with get_connection() as conn:
                        for item in selected_items:
                            conn.execute("""
                                INSERT INTO treatment_plan_items (plan_id, procedure_name, procedure_code, category, estimated_cost, status)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (plan_id, item['name'], item['code'], item['category'], item['cost'], 'planned'))
                        
                        conn.execute("""
                            UPDATE treatment_plans 
                            SET total_estimated_cost = ?
                            WHERE id = ?
                        """, (total_cost, plan_id))
                        conn.commit()
                    
                    st.success(f"✅ {len(selected_items)} items added to plan!")
                    if 'add_items_to_plan' in st.session_state:
                        del st.session_state.add_items_to_plan
                    if 'new_plan_id' in st.session_state:
                        del st.session_state.new_plan_id
                    st.rerun()
                else:
                    st.warning("No items selected")
        
        with col_s2:
            if st.form_submit_button("❌ Skip for Now", width="stretch"):
                if 'add_items_to_plan' in st.session_state:
                    del st.session_state.add_items_to_plan
                if 'new_plan_id' in st.session_state:
                    del st.session_state.new_plan_id
                st.rerun()