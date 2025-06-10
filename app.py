import streamlit as st

st.set_page_config(page_title="Gold Zakat & Growth Calculator", layout="centered")

st.title("🕌 Gold Zakat & Appreciation Calculator")
st.markdown("Easily calculate your annual zakat and estimate gold value growth over time.")

# User inputs
gold_grams = st.number_input("💰 Gold owned (in grams)", min_value=0.0, value=40.0, step=0.1)
price_per_gram = st.number_input("📈 Current gold price per gram (₹)", min_value=0.0, value=6000.0, step=10.0)
growth_rate = st.number_input("📊 Expected yearly appreciation (%)", min_value=0.0, value=8.0, step=0.1)
years = st.number_input("📅 Holding period (years)", min_value=1, value=5, step=1)

if st.button("Calculate"):
    if gold_grams < 85:
        st.warning("⚠️ You do not need to pay zakat. The minimum threshold (nisab) is 85 grams of gold.")
    else:
        initial_value = gold_grams * price_per_gram
        yearly_results = []
        value = initial_value

        for year in range(1, years + 1):
            value *= (1 + growth_rate / 100)
            zakat = value * 0.025
            value -= zakat
            yearly_results.append((year, round(value, 2), round(zakat, 2)))

        total_appreciation = ((value - initial_value) / initial_value) * 100
        cagr = ((value / initial_value) ** (1 / years) - 1) * 100

        st.subheader("📋 Yearly Breakdown")
        for yr, val, zak in yearly_results:
            st.write(f"Your Zakat for year {yr}:  <big>**₹{zak:,.2f}**</big> , Total Gold Value after Zakat: ₹{val:,.2f} ", , unsafe_allow_html=True)

        st.subheader("📌 Summary")
        st.write(f"Final Value After Zakat: **₹{value:,.2f}**")
        st.write(f"Total Appreciation After Zakat: **{total_appreciation:.2f}%**")
        st.write(f"Effective Annual Growth (CAGR): **{cagr:.2f}%**")
