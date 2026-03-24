import streamlit as st
import pandas as pd

st.set_page_config(page_title="מנהל השקעות חכם", layout="wide")

st.title("💼 מנהל השקעות ויעדים חכם")

# -----------------------
# קלטים
# -----------------------

st.sidebar.header("📥 הזן נתונים")

initial = st.sidebar.number_input("💰 סכום התחלתי", value=10000)
monthly = st.sidebar.number_input("📆 הפקדה חודשית", value=1000)
years = st.sidebar.slider("⏳ טווח השקעה (שנים)", 1, 30, 5)
rate = st.sidebar.number_input("📈 תשואה שנתית (%)", value=7.0)

goal = st.sidebar.number_input("🎯 סכום יעד", value=100000)

# -----------------------
# חישוב
# -----------------------

months = years * 12
monthly_rate = rate / 100 / 12

values = []
total = initial

for m in range(months):
    total = total * (1 + monthly_rate) + monthly
    values.append(total)

df = pd.DataFrame({
    "חודש": list(range(1, months + 1)),
    "שווי תיק": values
})

final_value = values[-1]
invested = initial + monthly * months
profit = final_value - invested

# -----------------------
# תצוגה ראשית
# -----------------------

col1, col2, col3 = st.columns(3)

col1.metric("💰 שווי סופי", f"{int(final_value):,} ₪")
col2.metric("📥 סה״כ הפקדות", f"{int(invested):,} ₪")
col3.metric("📈 רווח", f"{int(profit):,} ₪")

st.divider()

# -----------------------
# גרף
# -----------------------

st.subheader("📊 התפתחות התיק לאורך זמן")
st.line_chart(df.set_index("חודש"))

# -----------------------
# בדיקת יעד
# -----------------------

st.subheader("🎯 בדיקת יעד")

if final_value >= goal:
    st.success("✅ אתה צפוי להגיע ליעד!")
else:
    needed = (goal - final_value) / months
    st.error("❌ לא מגיע ליעד")
    st.write(f"צריך להוסיף בערך {int(needed):,} ₪ לחודש כדי להגיע ליעד")

# -----------------------
# AI פשוט (ללא API)
# -----------------------

st.subheader("🧠 ניתוח חכם")

analysis = ""

if rate < 4:
    analysis += "התשואה נמוכה יחסית, ייתכן שאתה במסלול סולידי מאוד.\n"

if monthly < 500:
    analysis += "קצב ההפקדה נמוך — הגדלה קטנה יכולה לשנות משמעותית את התוצאה.\n"

if years < 3:
    analysis += "טווח השקעה קצר — קשה לייצר ריבית דריבית משמעותית.\n"

if final_value > goal:
    analysis += "המצב שלך טוב — אפשר לשקול יעד גבוה יותר או הפחתת סיכון.\n"

if analysis == "":
    analysis = "התיק שלך נראה מאוזן יחסית לפי הנתונים."

st.info(analysis)

# -----------------------
# סימולציה נוספת
# -----------------------

st.subheader("🔄 מה קורה אם משנים דברים?")

new_rate = st.slider("שנה תשואה ל...", 1, 15, int(rate))
new_monthly = st.slider("שנה הפקדה ל...", 0, 5000, int(monthly))

new_total = initial

for m in range(months):
    new_total = new_total * (1 + (new_rate/100/12)) + new_monthly

st.write(f"📈 שווי חדש משוער: {int(new_total):,} ₪")
