import streamlit as st

st.set_page_config(page_title="Gold Zakat & Growth Calculator", layout="centered")

st.title("🕌 Gold Zakat & Appreciation Calculator")
st.markdown("Easily calculate your annual zakat and estimate gold value growth over time.")
NISAB_GRAMS = 85
ZAKAT_VALUE = 0.025


# User inputs
gold_grams_over_1_year = st.number_input("💰 Gold owned more than a lunar year (in grams)", min_value=0.0, value=40.0, step=0.1)
gold_grams_below_1_year = st.number_input("💰 Gold owned for less than a lunar year (in grams)", min_value=0.0, value=40.0, step=0.1)
price_per_gram = st.number_input("📈 Current gold price per gram (₹)", min_value=0.0, value=8000.0, step=10.0)
growth_rate = st.number_input("📊 Expected yearly appreciation (%)", min_value=0.0, value=8.0, step=0.1)
years = st.number_input("📅 Holding period (years)", min_value=1, value=5, step=1)
total_gold_grams = gold_grams_over_1_year + gold_grams_below_1_year
if st.button("Calculate"):
    if total_gold_grams < NISAB_GRAMS:
        st.warning("⚠️ You do not need to pay zakat. The minimum threshold (nisab) is 85 grams of gold.")
    else:
        current_zakat =  gold_grams_over_1_year * ZAKAT_VALUE* price_per_gram
        current_gold_grams = total_gold_grams - current_zakat

        if gold_grams_over_1_year < NISAB_GRAMS:
            current_gold_grams = total_gold_grams
            currentzakat = 0
            
        initial_value = current_gold_grams* price_per_gram
        yearly_results = []
        
        value = initial_value

        for year in range(1, years + 1):
            value *= (1 + growth_rate / 100)
            current_gold_grams -=ZAKAT_VALUE
            zakat = value * ZAKAT_VALUE
            value -= zakat
            yearly_results.append((year, round(value, 2), round(zakat, 2),round(current_gold_grams, 3)))

        total_appreciation = ((value - initial_value) / initial_value) * 100
        cagr = ((value / initial_value) ** (1 / years) - 1) * 100
        
        st.subheader("💰 Current Zakat Obligation")
        if gold_grams_over_1_year >= NISAB_GRAMS:
            st.write(f"You are currently obligated to Pay Zakat of: <big>**₹{current_zakat:,.2f}**</big>", unsafe_allow_html=True)
        else:
            st.info("The initial gold amount held for over a year is below Nisab, so no Zakat is due currently.")


        st.subheader("📋 Yearly Breakdown")
        for yr, val, zak,gram in yearly_results:
            if gram >= NISAB_GRAMS:
                st.write(f"Your Zakat for year {yr}:  <big>**₹{zak:,.2f}**</big> ,Total Gold Value after Zakat: ₹{val:,.2f} , \nTotal Gold Remaining : ₹{gram:,.2f}", unsafe_allow_html=True)
        if current_gold_grams < 85:
                st.write("The gold amount thereafter is below Nisab, so no Zakat is due.")

            

        st.subheader("📌 Summary")
        st.write(f"Final Value After Zakat: **₹{value:,.2f}**")
        st.write(f"Total Appreciation After Zakat: **{total_appreciation:.2f}%**")
        st.write(f"Effective Annual Growth (CAGR): **{cagr:.2f}%**")
