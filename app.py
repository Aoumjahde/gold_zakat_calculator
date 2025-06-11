
import streamlit as st

st.set_page_config(page_title="Gold Zakat & Growth Calculator", layout="centered")

st.title("🕌 Gold Zakat & Appreciation Calculator")
st.markdown("Easily calculate your annual zakat and estimate gold value growth over time.")

NISAB_GRAMS = 85
ZAKAT_PERCENTAGE = 0.025


# User inputs
gold_grams_over_1_year = st.number_input("💰 Gold owned more than a lunar year (in grams)", min_value=0.0, value=40.0, step=0.1)
gold_grams_below_1_year = st.number_input("💰 Gold owned for less than a lunar year (in grams)", min_value=0.0, value=40.0, step=0.1)
price_per_gram = st.number_input("📈 Current gold price per gram (₹)", min_value=0.0, value=8000.0, step=10.0)
growth_rate = st.number_input("📊 Expected yearly appreciation in INR (%)", min_value=0.0, value=8.0, step=0.1)
years = st.number_input("📅 Holding period (years)", min_value=1, value=5, step=1)

total_gold_grams = gold_grams_over_1_year + gold_grams_below_1_year

if st.button("Calculate"):
    if total_gold_grams < NISAB_GRAMS:
        st.warning("⚠️ You do not need to pay zakat. The minimum threshold (nisab) is 85 grams of gold.")
    else:
        current_zakat =  gold_grams_over_1_year * ZAKAT_PERCENTAGE
        current_zakat_value =  current_zakat* price_per_gram
        current_gold_grams = total_gold_grams - current_zakat

        if gold_grams_over_1_year < NISAB_GRAMS:
            current_gold_grams = total_gold_grams
            current_zakat = 0
            current_zakat_value = 0
            
        initial_value = current_gold_grams* price_per_gram
        yearly_results = []
        total_zakat_paid = [current_zakat]
        total_zakat_paid_value = [current_zakat_value]
        
        value = initial_value

for year in range(1, years + 1):
    price_per_gram *= (1 + growth_rate / 100)
    zakat_grams = 0
    zakat_value = 0
    status = "❌ No zakat (below Nisab)"

    if current_gold_grams >= NISAB_GRAMS:
        zakat_grams = current_gold_grams * ZAKAT_PERCENTAGE
        current_gold_grams -= zakat_grams
        zakat_value = zakat_grams * price_per_gram + 1
        total_zakat_paid.append(zakat_grams)
        total_zakat_paid_value.append(zakat_value)
        status = "✅ Zakat Due"
    else:
        total_zakat_paid.append(0)
        total_zakat_paid_value.append(0)

    value = current_gold_grams * price_per_gram + 1
    yearly_results.append((
        year,
        round(zakat_grams, 2),
        round(current_gold_grams, 2),
        round(zakat_value),
        round(value),
        status
    ))

        total_appreciation = ((value - initial_value) / initial_value) * 100
        cagr = ((value / initial_value) ** (1 / years) - 1) * 100
        
        st.subheader("💰 Current Zakat Obligation")
        if gold_grams_over_1_year >= NISAB_GRAMS:
            st.write(f"You are currently obligated to Pay Zakat of:<big>**{current_zakat:,.2f}g**</big>, worth <big>**₹{current_zakat_value:,.0f}**</big>", unsafe_allow_html=True)
            st.write(f"The Remaining Gold will be: <big>**{total_gold_grams - current_zakat:,.2f}g**</big>, worth <big>**₹{initial_value:,.0f}**</big>" , unsafe_allow_html=True)

        else:
            st.info("The initial gold amount held for over a year is below Nisab, so no Zakat is due currently.")


        st.subheader("📋 Yearly Breakdown")
        for yr, zak_gram, current_gram,zak_value, value, status in yearly_results:
            st.write(status)
            st.write(f""" Your Zakat for year {yr}:  <big><b>{zak_gram:,.2f}g</b></big>, worth <big><b>₹{zak_value:,.0f}</b></big><br>
            Total Gold after Zakat:  <big><b>{current_gram:,.2f}g</b></big>, worth <big><b>₹{value:,.0f}</b></big> """, unsafe_allow_html=True)
        if current_gold_grams < 85:
                st.info("The gold amount thereafter is below Nisab, so no Zakat is due.")

        st.subheader("📌 Summary")

        year = yearly_results[-1][0]
        if gold_grams_over_1_year >= NISAB_GRAMS:
            year+=1
        
        st.markdown("<h5 style='margin-top: -10px;'>Zakat Paid</h5>", unsafe_allow_html=True)
        st.write(f"Total Zakat Paid over {year} years: **{sum(total_zakat_paid):,.2f}g**")
        st.write(f"Value of Total Zakat Paid in INR: **₹{sum(total_zakat_paid_value):,.2f}**")

        st.write(" ")

        st.markdown("<h5 style='margin-top: -10px;'>Gold after Zakat</h5>", unsafe_allow_html=True)
        st.write(f"Gold Currently Holding in Grams: **{current_gold_grams:,.2f}g**")
        st.write(f"Final Value of Gold Currently Holding: **₹{value:,.2f}**")

        st.write(" ")

        st.markdown("<h5 style='margin-top: -10px;'>Growth in Value</h5>", unsafe_allow_html=True)
        st.write(f"Total Appreciation (After Zakat): **{total_appreciation:.2f}%**")
        st.write(f"Effective Annual Growth (CAGR): **{cagr:.2f}%**")
