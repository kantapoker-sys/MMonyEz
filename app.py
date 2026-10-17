import json  # นำเข้าโมดูล json สำหรับ อ่าน-เขียน ไฟล์ข้อมูล
import os    # นำเข้าโมดูล os สำหรับตรวจสอบไฟล์ในระบบ
import base64 # สำหรับแปลงรูปแสดงใน HTML
from datetime import datetime, date # สำหรับจัดการวันที่และเวลา
import streamlit as st  # นำเข้าไลบรารี streamlit สำหรับสร้างหน้าเว็บ UI

# ==========================================
# 🎨 ส่วนที่ 0: ระบบจัดการธีม ไอคอน และชื่อแอป
# ==========================================
def load_theme():
    try:
        with open("theme.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "theme_color": "#e60012",
            "app_icon": "🎭",
            "app_title": "MMonyEz",
            "show_countdown": True,
            "menu_order": [
                "🏠 หน้าหลัก",
                "📊 สถิติ & สรุปการเงิน",
                "📝 To-Do List & กำหนดการ",
                "📅 ตารางเรียน ม.6",
                "💰 เพิ่ม/แก้ไข ประวัติการเงิน",
                "👤 จัดการโปรไฟล์"
            ]
        }

def save_theme(theme_data):
    with open("theme.json", "w", encoding="utf-8") as f:
        json.dump(theme_data, f, ensure_ascii=False, indent=4)

def get_contrast_text_color(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return "#000000" if brightness > 128 else "#ffffff"

current_theme = load_theme()
theme_color = current_theme.get("theme_color", "#e60012")
app_icon = current_theme.get("app_icon", "🎭")
app_title = current_theme.get("app_title", "MMonyEz")
default_menu_list = [
    "🏠 หน้าหลัก",
    "📊 สถิติ & สรุปการเงิน",
    "📝 To-Do List & กำหนดการ",
    "📅 ตารางเรียน ม.6",
    "💰 เพิ่ม/แก้ไข ประวัติการเงิน",
    "👤 จัดการโปรไฟล์"
]
saved_menu_order = current_theme.get("menu_order", default_menu_list)

if set(saved_menu_order) != set(default_menu_list):
    saved_menu_order = default_menu_list

text_color_on_theme = get_contrast_text_color(theme_color)

st.set_page_config(
    page_title=app_title,
    page_icon=app_icon,
    layout="centered"
)

st.markdown(f"""
<style>
    /* 📱 บังคับสีพื้นหลังของแอปและ Sidebar ให้เป็น Dark Mode เสมอ */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #0b0b0b !important;
        color: #ffffff !important;
    }}

    /* 🔒 บังคับ Sidebar ให้เป็นโทนเข้มถาวร */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] {{
        background-color: #121212 !important;
        color: #ffffff !important;
    }}

    /* ปรับสีตัวอักษร หัวข้อ และป้ายชื่อใน Sidebar ให้เป็นสีขาวชัดเจน */
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
        color: #ffffff !important;
    }}

    /* ✏️ ปรับกล่องป้อนข้อความ (Text Input) และ Dropdown ใน Sidebar ให้เป็นโทนเข้มเข้ากัน */
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] div[data-baseweb="select"] > div {{
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
    }}

    /* ปรับขนาดส่วนหัวแอป */
    .p5-header {{
        font-size: 1.4rem;
        font-weight: 800;
        color: {text_color_on_theme};
        background-color: {theme_color};
        padding: 8px 16px;
        transform: skew(-3deg);
        box-shadow: 4px 4px 0px #000000;
        margin-bottom: 1rem;
        text-align: center;
        letter-spacing: 1px;
    }}

    /* 👤 ตกแต่งกล่องการ์ดโปรไฟล์ส่วนตัว */
    .profile-box {{
        display: flex;
        align-items: center;
        gap: 14px;
        background-color: #121212;
        border: 2px solid {theme_color};
        padding: 12px 16px;
        margin-bottom: 15px;
        transform: skew(-1deg);
        box-shadow: 4px 4px 0px #000000;
    }}
    
    .profile-avatar {{
        width: 75px;
        height: 75px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid {theme_color};
        flex-shrink: 0;
    }}
    
    .profile-avatar-placeholder {{
        width: 75px;
        height: 75px;
        border-radius: 50%;
        background-color: #1a1a1a;
        border: 2px solid {theme_color};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        flex-shrink: 0;
    }}

    .profile-info {{
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .p5-profile-name {{
        font-size: 1.15rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 4px;
    }}
    .p5-profile-sub {{
        font-size: 0.88rem;
        color: #cccccc;
        margin-bottom: 2px;
        line-height: 1.3;
    }}

    /* 💳 ตกแต่งกล่องการ์ดสรุปยอดเงิน */
    .p5-balance-card {{
        background-color: #000000;
        border: 3px solid {theme_color};
        padding: 18px 14px;
        transform: skew(-2deg);
        box-shadow: 5px 5px 0px {theme_color};
        margin-bottom: 18px;
        text-align: center;
    }}
    .p5-balance-title {{
        font-size: 0.9rem;
        color: #ffffff;
        font-weight: bold;
        letter-spacing: 1px;
    }}
    .p5-balance-amount {{
        font-size: 2.4rem;
        font-weight: 900;
        color: {theme_color};
        margin: 4px 0 12px 0;
    }}
    
    /* กล่องย่อยแบ่งเงินสดกับเงินในบัญชี */
    .sub-balance-container {{
        display: flex;
        justify-content: space-around;
        gap: 10px;
        background-color: #121212;
        border: 1px solid #333333;
        padding: 10px;
        border-radius: 6px;
    }}
    .sub-balance-box {{
        flex: 1;
        text-align: center;
    }}
    .sub-balance-label {{
        font-size: 0.82rem;
        color: #aaaaaa;
        margin-bottom: 2px;
    }}
    .sub-balance-val {{
        font-size: 1.15rem;
        font-weight: bold;
        color: #ffffff;
    }}

    /* 🎨 บังคับปุ่มกดสไตล์ Persona 5 */
    .stButton>button {{
        background-color: {theme_color} !important;
        color: {text_color_on_theme} !important;
        font-weight: bold !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        transform: skew(-3deg);
        box-shadow: 3px 3px 0px #ffffff;
        transition: all 0.1s ease;
        margin-bottom: 6px;
    }}
    .stButton>button p, .stButton>button span {{
        color: {text_color_on_theme} !important;
        font-weight: bold !important;
    }}
    .stButton>button:hover {{
        background-color: #ffffff !important;
        color: {theme_color} !important;
        box-shadow: 3px 3px 0px {theme_color};
    }}
    .stButton>button:hover p, .stButton>button:hover span {{
        color: {theme_color} !important;
    }}

    .p5-income {{ color: #22c55e; font-weight: bold; }}
    .p5-expense {{ color: #ef4444; font-weight: bold; }}
    .p5-date {{ font-size: 0.75rem; color: #888888; }}

    /* 📋 สไตล์รายการ To-Do List สองบรรทัดสวยงาม */
    .todo-box {{
        background-color: #121212;
        border-left: 4px solid {theme_color};
        padding: 8px 12px;
        margin-bottom: 8px;
        border-radius: 4px;
    }}
    .todo-line1 {{
        font-size: 0.95rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 4px;
    }}
    .todo-line2 {{
        font-size: 0.82rem;
        color: #aaaaaa;
    }}
</style>
""", unsafe_allow_html=True)

# แสดงหัวข้อหลัก
st.markdown(f'<div class="p5-header">{app_icon} {app_title}</div>', unsafe_allow_html=True)


# ==========================================
# 📂 ส่วนที่ 1: ฟังก์ชันจัดการไฟล์ข้อมูล (JSON)
# ==========================================
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def load_initial_balance():
    try:
        with open("initial_balance.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_initial_balance(data):
    with open("initial_balance.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_รายรับ():
    try:
        with open("รายรับ.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_รายรับ(data):
    with open("รายรับ.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_รายจ่าย():
    try:
        with open("รายจ่าย.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_รายจ่าย(data):
    with open("รายจ่าย.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_todolist():
    try:
        with open("todolist.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return [
            {"รายการ": "สมัคร TGAT/TPAT2-5", "สถานะ": False, "วันที่": "2026-11-04", "เวลา": "00:01", "ประเภท": "⏰ วันสอบ"},
            {"รายการ": "สอบ A-Level", "สถานะ": False, "วันที่": "2027-03-15", "เวลา": "09:00", "ประเภท": "⏰ วันสอบ"}
        ]

def save_todolist(data):
    with open("todolist.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_profile():
    try:
        with open("profile.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data[-1] if data else {}
            return data
    except FileNotFoundError:
        return {}

def save_profile(data):
    with open("profile.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# โหลดข้อมูลทั้งหมด
initial_data = load_initial_balance()
รายรับ_list = load_รายรับ()
รายจ่าย_list = load_รายจ่าย()
todolist = load_todolist()
user_profile = load_profile()

init_cash = initial_data.get("cash", 0.0) if initial_data else 0.0
init_bank = initial_data.get("bank", 0.0) if initial_data else 0.0

cash_income = sum(item["จำนวน"] for item in รายรับ_list if item.get("ช่องทาง") == "เงินสด")
cash_expense = sum(item["จำนวน"] for item in รายจ่าย_list if item.get("ช่องทาง") == "เงินสด")
cash_balance = init_cash + cash_income - cash_expense

bank_income = sum(item["จำนวน"] for item in รายรับ_list if item.get("ช่องทาง") != "เงินสด")
bank_expense = sum(item["จำนวน"] for item in รายจ่าย_list if item.get("ช่องทาง") != "เงินสด")
bank_balance = init_bank + bank_income - bank_expense

total_income = cash_income + bank_income
total_expense = cash_expense + bank_expense
total_balance = cash_balance + bank_balance


# ==========================================
# 🚨 ส่วนที่ 1.5: ระบบตั้งค่ายอดเงินเริ่มต้น
# ==========================================
if initial_data is None:
    st.warning(f"👋 **ต้อนรับสู่ {app_title}!** กรุณากำหนด **ยอดเงินเริ่มต้นที่มีอยู่จริง** ในปัจจุบันก่อนเริ่มใช้งานครับ")
    with st.container(border=True):
        st.write("### 💵 ตั้งค่ายอดเงินเริ่มต้น")
        c_init_cash = st.number_input("เงินสดติดตัวเริ่มต้น (บาท):", min_value=0.0, step=100.0, value=0.0)
        c_init_bank = st.number_input("เงินในบัญชีธนาคารเริ่มต้น (บาท):", min_value=0.0, step=100.0, value=0.0)
        
        if st.button("🚀 ยืนยันยอดเงินเริ่มต้นและเริ่มใช้งาน", use_container_width=True):
            save_initial_balance({"cash": c_init_cash, "bank": c_init_bank})
            st.success("✅ บันทึกยอดเงินเริ่มต้นสำเร็จ!")
            st.rerun()
    st.stop()


# ==========================================
# 📂 ส่วนที่ 2: ระบบจำสถานะหน้าปัจจุบัน
# ==========================================
if "current_page" not in st.session_state:
    st.session_state.current_page = saved_menu_order[0]


# ==========================================
# 🗂️ ส่วนที่ 3: เมนูด้านข้าง (Sidebar Menu)
# ==========================================
st.sidebar.markdown("### 📂 เมนูคำสั่ง")

for page_name in saved_menu_order:
    btn_text = f"▶ {page_name}" if st.session_state.current_page == page_name else page_name
    if st.sidebar.button(btn_text, key=f"menu_btn_{page_name}", use_container_width=True):
        st.session_state.current_page = page_name
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("⚙️ **ตั้งค่ายอดเงินเริ่มต้นใหม่**")
if st.sidebar.button("🔄 แก้ไขเงินเริ่มต้น (Initial)", use_container_width=True):
    st.session_state.show_edit_init = True

if st.session_state.get("show_edit_init", False):
    with st.sidebar.expander("📝 แก้ไขยอดเริ่มต้น", expanded=True):
        new_init_cash = st.number_input("เงินสดเริ่มต้น:", value=init_cash, step=100.0)
        new_init_bank = st.number_input("เงินในบัญชีเริ่มต้น:", value=init_bank, step=100.0)
        if st.button("💾 บันทึกยอดเริ่มต้นใหม่", use_container_width=True):
            save_initial_balance({"cash": new_init_cash, "bank": new_init_bank})
            st.session_state.show_edit_init = False
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("🎨 **ตั้งค่าแอป & จัดลำดับเมนู**")

show_countdown_card = st.sidebar.checkbox("👁️ แสดงการ์ดนับถอยหลังบนหน้าหลัก", value=current_theme.get("show_countdown", True))

new_app_title = st.sidebar.text_input("ชื่อแอปของคุณ:", value=app_title)

icon_options = ["🎭", "💰", "💳", "💸", "💎", "👑", "⚡", "🚀", "🎮", "🎓"]
if app_icon not in icon_options:
    icon_options.append(app_icon)
new_app_icon = st.sidebar.selectbox("เลือกไอคอนแอป:", icon_options, index=icon_options.index(app_icon))

selected_color = st.sidebar.color_picker("เลือกสีธีมที่คุณชอบ:", value=theme_color)

with st.sidebar.expander("🔀 ปรับจัดเรียงลำดับเมนู", expanded=False):
    st.caption("เลือกจัดเรียงลำดับเมนูตามความสะดวก:")
    new_ordered_menu = st.multiselect(
        "ลำดับเมนู (เลือกให้ครบ 6 รายการ):",
        options=default_menu_list,
        default=saved_menu_order
    )

if (selected_color != theme_color) or (new_app_icon != app_icon) or (new_app_title != app_title) or (show_countdown_card != current_theme.get("show_countdown", True)) or (len(new_ordered_menu) == 6 and new_ordered_menu != saved_menu_order):
    updated_order = new_ordered_menu if len(new_ordered_menu) == 6 else saved_menu_order
    save_theme({
        "theme_color": selected_color,
        "app_icon": new_app_icon,
        "app_title": new_app_title,
        "show_countdown": show_countdown_card,
        "menu_order": updated_order
    })
    st.rerun()


# ==========================================
# 📌 1. หน้าหลัก (Dashboard)
# ==========================================
if st.session_state.current_page == "🏠 หน้าหลัก":

    if user_profile:
        user_alias = user_profile.get("profilename") or user_profile.get("name") or "ผู้ใช้งาน"
        user_motto = user_profile.get("คติประจำใจ") or "ยังไม่ได้ตั้งคติประจำใจ"
        user_goal = user_profile.get("goal") or "ยังไม่ได้ตั้งเป้าหมาย"
        user_img = user_profile.get("image_path")

        if user_img and os.path.exists(user_img):
            img_b64 = get_image_base64(user_img)
            avatar_html = f'<img src="data:image/png;base64,{img_b64}" class="profile-avatar" />'
        else:
            avatar_html = '<div class="profile-avatar-placeholder">👤</div>'

        st.markdown(
            f"""
        <div class="profile-box">
            {avatar_html}
            <div class="profile-info">
                <div class="p5-profile-name">👤 {user_alias}</div>
                <div class="p5-profile-sub">💬 <b>คติประจำใจ:</b> {user_motto}</div>
                <div class="p5-profile-sub">🎯 <b>เป้าหมาย:</b> {user_goal}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ⏰ การ์ดนับถอยหลังวันสอบ
    if current_theme.get("show_countdown", True):
        exams_in_todo = [task for task in todolist if task.get("ประเภท") == "⏰ วันสอบ" and not task.get("สถานะ")]
        if exams_in_todo:
            with st.container(border=True):
                st.write("##### ⏰ นับถอยหลังวันสอบสำคัญ (COUNTDOWN)")
                today = date.today()
                for exam in exams_in_todo:
                    try:
                        e_date = datetime.strptime(exam["วันที่"], "%Y-%m-%d").date()
                        days_left = (e_date - today).days
                        
                        c_ex1, c_ex2 = st.columns([3, 1.2])
                        with c_ex1:
                            st.write(f"📌 **{exam['รายการ']}**")
                            st.caption(f"📅 {exam['วันที่']} ({exam.get('เวลา', '09:00')})")
                        with c_ex2:
                            if days_left > 0:
                                st.write(f"⏳ **เหลือ {days_left} วัน**")
                            elif days_left == 0:
                                st.error("🔥 วันนี้!")
                            else:
                                st.caption("เลยกำหนดแล้ว")
                    except Exception:
                        continue

    st.markdown(
        f"""
    <div class="p5-balance-card">
        <div class="p5-balance-title">⚡ ยอดเงินคงเหลือรวมทั้งหมด (TOTAL BALANCE) ⚡</div>
        <div class="p5-balance-amount">{total_balance:,.2f} ฿</div>
        <div class="sub-balance-container">
            <div class="sub-balance-box">
                <div class="sub-balance-label">💵 เงินสด (ในตัว)</div>
                <div class="sub-balance-val">{cash_balance:,.2f} ฿</div>
            </div>
            <div style="width: 1px; background-color: #333333;"></div>
            <div class="sub-balance-box">
                <div class="sub-balance-label">💳 เงินในบัญชี</div>
                <div class="sub-balance-val">{bank_balance:,.2f} ฿</div>
            </div>
        </div>
        <div style="font-size: 0.85rem; color: #aaa; margin-top: 10px;">
            📥 รวมรับเพิ่ม: <span class="p5-income">+{total_income:,.2f}</span> | 
            📤 รวมจ่ายออก: <span class="p5-expense">-{total_expense:,.2f}</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("📊 ดูประวัติเงิน", use_container_width=True):
            st.session_state.show_history = not st.session_state.get("show_history", False)

    with col_btn2:
        if st.button("📝 ดู To-Do List", use_container_width=True):
            st.session_state.show_todo = not st.session_state.get("show_todo", False)

    with col_btn3:
        if st.button("📅 ดูตารางเรียน", use_container_width=True):
            st.session_state.show_schedule = not st.session_state.get("show_schedule", False)

    st.markdown("---")

    if st.session_state.get("show_schedule", False):
        st.subheader("📅 ตารางเรียน ม.6/2")
        schedule_img_path = "schedule_pic.png"
        if os.path.exists(schedule_img_path):
            st.image(schedule_img_path, use_container_width=True)
        else:
            st.info("📭 ยังไม่มีรูปตารางเรียนในระบบ ไปอัปโหลดรูปตารางเรียนได้ที่เมนู '📅 ตารางเรียน ม.6' ครับ")
        st.markdown("---")

    if st.session_state.get("show_history", False):
        st.subheader("📊 ประวัติการเงินทั้งหมด")
        col_inc, col_exp = st.columns(2)
        with col_inc:
            st.write("#### 📥 รายรับ")
            if len(รายรับ_list) > 0:
                for idx, item in enumerate(รายรับ_list, start=1):
                    ch_icon = "💵" if item.get("ช่องทาง") == "เงินสด" else "💳"
                    date_str = f" <span class='p5-date'>({item.get('วันที่', '-')})</span>" if item.get("วันที่") else ""
                    st.markdown(
                        f"**{idx}.** {ch_icon} {item['รายการ']} :"
                        f' <span class="p5-income">+{item["จำนวน"]:,.2f} ฿</span>{date_str}',
                        unsafe_allow_html=True,
                    )
            else:
                st.info("ยังไม่มีข้อมูลรายรับ")

        with col_exp:
            st.write("#### 📤 รายจ่าย")
            if len(รายจ่าย_list) > 0:
                for idx, item in enumerate(รายจ่าย_list, start=1):
                    ch_icon = "💵" if item.get("ช่องทาง") == "เงินสด" else "💳"
                    date_str = f" <span class='p5-date'>({item.get('วันที่', '-')})</span>" if item.get("วันที่") else ""
                    st.markdown(
                        f"**{idx}.** {ch_icon} {item['รายการ']} :"
                        f' <span class="p5-expense">-{item["จำนวน"]:,.2f} ฿</span>{date_str}',
                        unsafe_allow_html=True,
                    )
            else:
                st.info("ยังไม่มีข้อมูลรายจ่าย")
        st.markdown("---")

    # 📋 รายการ To-Do List ปรับใหม่ 2 บรรทัดชัดเจน ไม่ซ้อนกัน
    if st.session_state.get("show_todo", False):
        st.subheader("📋 รายการสิ่งที่ต้องทำ")
        if len(todolist) == 0:
            st.info("📭 ยังไม่มีรายการงาน")
        else:
            for idx, task in enumerate(todolist, start=1):
                status_str = "✅ ทำแล้ว" if task.get("สถานะ") else "❌ ยังไม่ทำ"
                time_str = f"📅 {task.get('วันที่', '')} {task.get('เวลา', '')}" if task.get('วันที่') else ""
                
                st.markdown(f"""
                <div class="todo-box">
                    <div class="todo-line1">{idx}. [{task.get('ประเภท', '📌 งานทั่วไป')}] {task['รายการ']}</div>
                    <div class="todo-line2">{status_str} | {time_str}</div>
                </div>
                """, unsafe_allow_html=True)


# ==========================================
# 📌 2. หน้าสถิติ & สรุปการเงิน
# ==========================================
elif st.session_state.current_page == "📊 สถิติ & สรุปการเงิน":
    st.subheader("📊 สรุปสถิติการเงินสไตล์การ์ด")

    m1, m2, m3 = st.columns(3)
    m1.metric("🚩 เงินเริ่มต้นรวม", f"{init_cash + init_bank:,.2f} ฿")
    m2.metric("📥 รายรับรวมเพิ่ม", f"{total_income:,.2f} ฿")
    m3.metric("📤 รายจ่ายรวมออก", f"{total_expense:,.2f} ฿")

    st.markdown("---")

    st.write("#### 💵 สัดส่วนกระเป๋าเงินที่มี")
    safe_total = max(1.0, total_balance)
    cash_ratio = min(1.0, max(0.0, cash_balance / safe_total))
    bank_ratio = min(1.0, max(0.0, bank_balance / safe_total))

    with st.container(border=True):
        st.write(f"💵 **เงินสดติดตัว:** `{cash_balance:,.2f} ฿` ({cash_ratio*100:.1f}%)")
        st.progress(cash_ratio)

        st.write(f"💳 **เงินในบัญชี:** `{bank_balance:,.2f} ฿` ({bank_ratio*100:.1f}%)")
        st.progress(bank_ratio)

    st.markdown("---")

    st.write("#### ⚖️ อัตราส่วนรายจ่ายเทียบกับรายรับ")
    safe_income = max(1.0, total_income)
    expense_ratio = min(1.0, max(0.0, total_expense / safe_income))

    with st.container(border=True):
        st.write(f"📤 **ใช้จ่ายไปแล้ว:** `{total_expense:,.2f} ฿` จากรายรับทั้งหมด `{total_income:,.2f} ฿`")
        st.progress(expense_ratio)
        st.caption(f"💡 คุณใช้เงินไปแล้ว **{expense_ratio*100:.1f}%** ของรายรับทั้งหมดที่หาได้")

    st.markdown("---")
    st.write("#### 📌 รายละเอียดเงินเริ่มต้น")
    st.write(f"- 💵 **เงินสดเริ่มต้น:** `{init_cash:,.2f}` บาท")
    st.write(f"- 💳 **เงินในบัญชีเริ่มต้น:** `{init_bank:,.2f}` บาท")


# ==========================================
# 📌 3. หน้า To-Do List & กำหนดการ
# ==========================================
elif st.session_state.current_page == "📝 To-Do List & กำหนดการ":
    st.subheader("📝 จัดการรายการสิ่งที่ต้องทำ & กำหนดการสอบ")

    with st.container(border=True):
        st.write("#### ➕ เพิ่มรายการงาน / กำหนดการใหม่")
        task_type = st.radio("ประเภทรายการ:", ["📌 งานทั่วไป", "⏰ วันสอบ", "📝 การบ้าน/รายงาน", "🎯 เป้าหมาย"], horizontal=True)
        task_title = st.text_input("ชื่องาน / ชื่อวิชาสอบ:")
        
        c_d1, c_d2 = st.columns(2)
        with c_d1:
            task_date = st.date_input("กำหนดวันที่ (Due Date):", value=date.today())
        with c_d2:
            task_time = st.time_input("กำหนดเวลา:", value=datetime.now().time())

        if st.button("💾 บันทึกรายการ", use_container_width=True):
            if task_title.strip() != "":
                new_task_item = {
                    "รายการ": task_title.strip(),
                    "สถานะ": False,
                    "วันที่": str(task_date),
                    "เวลา": task_time.strftime("%H:%M"),
                    "ประเภท": task_type
                }
                todolist.append(new_task_item)
                save_todolist(todolist)
                st.success("✅ เพิ่มรายการสำเร็จ!")
                st.rerun()
            else:
                st.warning("กรุณากรอกชื่อรายการ!")

    st.markdown("---")
    st.write("#### 📋 รายการภารกิจทั้งหมด")

    if len(todolist) == 0:
        st.info("ไม่มีรายการงาน")
    else:
        for idx, task in enumerate(todolist):
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    is_done = st.checkbox(
                        f"**[{task.get('ประเภท', '📌 งานทั่วไป')}]** {task['รายการ']}",
                        value=task.get("สถานะ", False),
                        key=f"manage_todo_{idx}"
                    )
                    st.caption(f"📅 กำหนดส่ง/วันสอบ: `{task.get('วันที่', '-')}` เวลา `{task.get('เวลา', '-')}`")

                    if is_done != task.get("สถานะ", False):
                        todolist[idx]["สถานะ"] = is_done
                        save_todolist(todolist)
                        st.rerun()
                with c2:
                    if st.button("🗑️ ลบ", key=f"del_todo_page_{idx}"):
                        del todolist[idx]
                        save_todolist(todolist)
                        st.success("ลบรายการสำเร็จ!")
                        st.rerun()


# ==========================================
# 📌 4. หน้าตารางเรียน ม.6
# ==========================================
elif st.session_state.current_page == "📅 ตารางเรียน ม.6":
    st.subheader("📅 ระบบตารางเรียน ม.6")

    schedule_img_path = "schedule_pic.png"

    with st.container(border=True):
        if os.path.exists(schedule_img_path):
            st.write("### 🏫 ตารางเรียนปัจจุบันของคุณ")
            st.image(schedule_img_path, use_container_width=True)
        else:
            st.info("📭 ยังไม่มีรูปตารางเรียนในระบบ อัปโหลดรูปตารางเรียนของคุณได้ด้านล่างเลยครับ!")

    st.markdown("---")

    with st.container(border=True):
        st.write("#### 📸 อัปโหลด / เปลี่ยนรูปตารางเรียนใหม่")
        uploaded_schedule = st.file_uploader("เลือกรูปตารางเรียนของคุณ:", type=["png", "jpg", "jpeg"])

        if st.button("💾 บันทึกรูปตารางเรียน", use_container_width=True):
            if uploaded_schedule is not None:
                with open(schedule_img_path, "wb") as f:
                    f.write(uploaded_schedule.getbuffer())
                st.success("✅ อัปโหลดและบันทึกรูปตารางเรียนสำเร็จ!")
                st.rerun()
            else:
                st.warning("⚠️ กรุณาเลือกไฟล์รูปภาพก่อนกดบันทึกครับ!")


# ==========================================
# 📌 5. หน้าเพิ่มหรือแก้ไข ประวัติการเงิน
# ==========================================
elif st.session_state.current_page == "💰 เพิ่ม/แก้ไข ประวัติการเงิน":
    st.subheader("💰 จัดการบันทึกประวัติการเงิน")

    tab1, tab2 = st.tabs(["➕ เพิ่มรายการใหม่", "🗑️ ลบรายการเงิน"])

    with tab1:
        with st.container(border=True):
            trans_type = st.radio("ประเภท:", ["รายรับ", "รายจ่าย"], horizontal=True)
            channel_type = st.radio("ช่องทางเงิน:", ["💳 เงินในบัญชี", "💵 เงินสด (ในตัว)"], horizontal=True)
            
            item_name = st.text_input("ชื่อรายการ:")
            item_amount = st.number_input("จำนวนเงิน (บาท):", min_value=0.0, step=1.0, format="%.2f")
            
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            record_datetime = st.text_input("วันที่และเวลาบันทึก:", value=now_str)

            if st.button("💾 บันทึกข้อมูล", use_container_width=True):
                if item_name.strip() == "":
                    st.warning("กรุณากรอกชื่อรายการ!")
                elif item_amount <= 0:
                    st.warning("จำนวนเงินต้องมากกว่า 0!")
                else:
                    selected_channel = "เงินสด" if "เงินสด" in channel_type else "เงินในบัญชี"
                    new_record = {
                        "รายการ": item_name,
                        "จำนวน": item_amount,
                        "ช่องทาง": selected_channel,
                        "วันที่": record_datetime
                    }
                    if trans_type == "รายรับ":
                        รายรับ_list.append(new_record)
                        save_รายรับ(รายรับ_list)
                    else:
                        รายจ่าย_list.append(new_record)
                        save_รายจ่าย(รายจ่าย_list)
                    st.success(f"✅ บันทึก {trans_type} ({selected_channel}) เรียบร้อยเมื่อ {record_datetime}!")
                    st.rerun()

    with tab2:
        with st.container(border=True):
            del_type = st.radio("ลบประเภท:", ["รายรับ", "รายจ่าย"], horizontal=True)
            target_list = รายรับ_list if del_type == "รายรับ" else รายจ่าย_list

            if len(target_list) > 0:
                options = [
                    f"{idx+1}. [{item.get('ช่องทาง', 'เงินในบัญชี')}] {item['รายการ']} ({item['จำนวน']:,.2f} บาท) - {item.get('วันที่', '-')}"
                    for idx, item in enumerate(target_list)
                ]
                selected = st.selectbox("เลือกรายการที่ต้องการลบ:", options)
                if st.button("🗑️ ยืนยันการลบ", use_container_width=True):
                    idx_del = options.index(selected)
                    removed = target_list.pop(idx_del)
                    if del_type == "รายรับ":
                        save_รายรับ(target_list)
                    else:
                        save_รายจ่าย(target_list)
                    st.success("🗑️ ลบสำเร็จ!")
                    st.rerun()
            else:
                st.info("ไม่มีรายการให้ลบ")


# ==========================================
# 👤 6. หน้าจัดการโปรไฟล์ผู้ใช้
# ==========================================
elif st.session_state.current_page == "👤 จัดการโปรไฟล์":
    st.subheader("👤 ระบบข้อมูลโปรไฟล์ผู้ใช้")

    with st.container(border=True):
        if not user_profile:
            st.info("📭 ยังไม่มีข้อมูลโปรไฟล์ในระบบ กรอกข้อมูลด้านล่างเพื่อสร้างโปรไฟล์ใหม่ได้เลยครับ!")
        else:
            p_img = user_profile.get("image_path")
            if p_img and os.path.exists(p_img):
                img_b64 = get_image_base64(p_img)
                avatar_html = f'<img src="data:image/png;base64,{img_b64}" class="profile-avatar" />'
            else:
                avatar_html = '<div class="profile-avatar-placeholder">👤</div>'

            st.markdown(
                f"""
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
                {avatar_html}
                <div>
                    <h3 style="margin: 0;">👤 โปรไฟล์ผู้ใช้ปัจจุบัน</h3>
                    <p style="margin: 0; color: #aaa;">{user_profile.get('profilename', '-')}</p>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.write(f"**ชื่อจริง:** {user_profile.get('name', '-')}")
            st.write(f"**อายุ:** {user_profile.get('age', '-')} ปี | **วันเกิด:** {user_profile.get('birth', '-')}")
            st.write(f"**น้ำหนัก:** {user_profile.get('weight', '-')} กก. | **ส่วนสูง:** {user_profile.get('height', '-')}")
            st.write(f"**สถานะ:** {user_profile.get('status', '-')}")
            st.write(f"**คติประจำใจ:** {user_profile.get('คติประจำใจ', '-')}")
            st.write(f"**เป้าหมาย:** {user_profile.get('goal', '-')}")

    st.markdown("---")

    with st.container(border=True):
        st.write("#### ✏️ แก้ไขข้อมูลโปรไฟล์")

        old_img = user_profile.get("image_path", "")
        uploaded_file = st.file_uploader("📸 เลือก/เปลี่ยน รูปโปรไฟล์ใหม่:", type=["png", "jpg", "jpeg"])

        name_input = st.text_input("ชื่อจริง:", value=user_profile.get("name", ""))
        profilename_input = st.text_input("ชื่อโปรไฟล์ (Nickname/Alias):", value=user_profile.get("profilename", ""))
        age_input = st.text_input("อายุ:", value=user_profile.get("age", ""))
        birth_input = st.text_input("วัน-เดือน-ปีเกิด:", value=user_profile.get("birth", ""))
        weight_input = st.text_input("น้ำหนัก (กก.):", value=user_profile.get("weight", ""))
        height_input = st.text_input("ส่วนสูง (ซม.):", value=user_profile.get("height", ""))
        status_input = st.text_input("สถานะ (เช่น โสด):", value=user_profile.get("status", ""))
        motto_input = st.text_input("คติประจำใจ:", value=user_profile.get("คติประจำใจ", ""))
        goal_input = st.text_input("เป้าหมาย (เช่น วิศวะคอมฯ):", value=user_profile.get("goal", ""))

        if st.button("💾 บันทึกโปรไฟล์", use_container_width=True):
            if name_input.strip() == "":
                st.warning("⚠️ กรุณากรอกชื่อจริงอย่างน้อยหนึ่งช่องครับ!")
            else:
                saved_image_path = old_img
                if uploaded_file is not None:
                    saved_image_path = "profile_pic.png"
                    with open(saved_image_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                updated_profile = {
                    "name": name_input,
                    "profilename": profilename_input,
                    "age": age_input,
                    "birth": birth_input,
                    "weight": weight_input,
                    "height": height_input,
                    "status": status_input,
                    "คติประจำใจ": motto_input,
                    "goal": goal_input,
                    "image_path": saved_image_path
                }

                save_profile(updated_profile)
                st.success("✅ อัปเดตข้อมูลโปรไฟล์เรียบร้อย!")
                st.rerun()