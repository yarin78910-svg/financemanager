import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="מנהל פיננסי חכם", layout="wide")

# ========================
# STATE
# ========================
if "assets" not in st.session_state:
    st.session_state.assets = []
if "goals" not in st.session_state:
    st.session_state.goals = []
if "income" not in st.session_state:
    st.session_state.income = 12000
if "expenses" not in st.session_state:
    st.session_state.expenses = 8000

# ========================
# FUNCTIONS
# ========================
def total_assets():
    return sum(a["amount"] for a in st.session_state.assets)

def free_cash():
    return st.session_state.income - st.session_state.expenses

def avg_return():
    if not st.session_state.assets:
        return 0
    total = total_assets()
    return sum(a["amount"] * a["return"] for a in st.session_state.assets) / total

def projection(months=60):
    total = total_assets()
    r = avg_return() / 100 / 12
    values = []
    for _ in range(months):
        total = total * (1 + r)
        values.append(total)
    return values

# ========================
# NAV
# ========================
page = st.sidebar.radio("ניווט", [
    "🏠 דשבורד",
    "💼 נכסים",
    "🎯 יעדים",
    "🤖 סוכן AI"
])

# ========================
# DASHBOARD
# ========================
if page == "🏠 דשבורד":
    st.title("📊 דשבורד פיננסי")

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 שווי כולל", f"{int(total_assets()):,} ₪")
    col2.metric("📥 הכנסה", f"{st.session_state.income:,} ₪")
    col3.metric("📤 הוצאות", f"{st.session_state.expenses:,} ₪")

    st.metric("💸 תזרים פנוי", f"{free_cash():,} ₪")

    st.divider()

    st.subheader("📈 תחזית תיק")
    st.line_chart(projection())

# ========================
# ASSETS
# ========================
elif page == "💼 נכסים":
    st.title("💼 ניהול נכסים")

    with st.form("add_asset"):
        name = st.text_input("שם נכס")
        amount = st.number_input("שווי", value=0)
        ret = st.number_input("תשואה שנתית (%)", value=5.0)
        submit = st.form_submit_button("➕ הוסף")

        if submit:
            st.session_state.assets.append({
                "name": name,
                "amount": amount,
                "return": ret
            })

    if st.session_state.assets:
        df = pd.DataFrame(st.session_state.assets)
        st.dataframe(df)

        for i, a in enumerate(st.session_state.assets):
            if st.button(f"❌ מחק {a['name']}", key=i):
                st.session_state.assets.pop(i)
                st.rerun()

# ========================
# GOALS
# ========================
elif page == "🎯 יעדים":
    st.title("🎯 יעדים")

    with st.form("add_goal"):
        name = st.text_input("שם יעד")
        amount = st.number_input("סכום יעד", value=50000)
        months = st.number_input("חודשים", value=24)
        submit = st.form_submit_button("➕ הוסף יעד")

        if submit:
            st.session_state.goals.append({
                "name": name,
                "amount": amount,
                "months": months
            })

    for g in st.session_state.goals:
        needed = (g["amount"] - total_assets()) / g["months"]

        st.subheader(g["name"])
        st.write(f"יעד: {g['amount']:,} ₪")
        st.write(f"חיסכון חודשי דרוש: {int(needed):,} ₪")

        if needed > free_cash():
            st.error("❌ לא ריאלי")
        else:
            st.success("✅ אפשרי")

# ========================
# AI AGENT
# ========================
elif page == "🤖 סוכן AI":
    st.title("🤖 סוכן פיננסי חכם")

    question = st.text_area("שאל שאלה")

    if st.button("נתח"):
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            prompt = f"""
            אתה יועץ פיננסי.

            שווי כולל: {total_assets()}
            הכנסה: {st.session_state.income}
            הוצאות: {st.session_state.expenses}
            תזרים פנוי: {free_cash()}

            נכסים:
            {st.session_state.assets}

            יעדים:
            {st.session_state.goals}

            שאלה:
            {question}

            תן תשובה חכמה, ברורה וישירה.
            """

            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            st.success(res.choices[0].message.content)

        except Exception as e:
            st.error("בעיה ב-AI")
            st.write(e)
