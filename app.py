import streamlit as st

st.title("מחשבון השקעות פשוט")

investment = st.number_input("כמה כסף יש לך עכשיו?", value=10000)
monthly = st.number_input("כמה אתה מוסיף כל חודש?", value=1000)
months = st.number_input("לכמה חודשים?", value=12)

future_value = investment + (monthly * months)

st.write("שווי עתידי:")
st.success(f"{future_value} ש״ח")
