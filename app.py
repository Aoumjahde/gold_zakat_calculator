import streamlit as st

st.set_page_config(page_title="Gold Zakat & Growth Calculator", layout="centered")

st.title("🕌 Gold Zakat & Appreciation Calculator")
st.markdown("Easily calculate your annual zakat and estimate gold value growth over time.")

NISAB_GRAMS = 85
ZAKAT_PERCENTAGE = 0.025

def grams_to_pawan(grams):
    """Convert grams to pawan (1 pawan = 8 grams) """
    return grams / 8

# User inputs
unit = st.radio("Select Unit of Measurement", ["Grams", "Pawan (8g)"], horizontal=True)

if unit == "Grams":
    gold_grams_over_1_year = st.number_input("💰 Gold owned more than a lunar year (in grams)", min_value=0.0, value=40.0, step=0.1)
    gold_grams_below_1_year = st.number_input("💰 Gold owned for less than a lunar year (in grams)", min_value=0.0, value=40.0, step=0.1)
else:
    pawan_over = st.number_input("💰 Gold owned more than a lunar year (in pawan)", min_value=0.0, value=5.0, step=0.1)
    pawan_below = st.number_input("💰 Gold owned for less than a lunar year (in pawan)", min_value=0.0, value=5.0, step=0.1)
    gold_grams_over_1_year = pawan_over * 8
    gold_grams_below_1_year = pawan_below * 8

price_per_gram = st.number_input("📈 Current gold price per gram (₹)", min_value=0.0, value=8000.0, step=10.0)
growth_rate = st.number_input("📊 Expected yearly appreciation in INR (%)", min_value=0.0, value=8.0, step=0.1)
years = st.number_input("📅 Holding period (years)", min_value=1, value=5, step=1)

total_gold_grams = gold_grams_over_1_year + gold_grams_below_1_year

if st.button("Calculate"):
    if total_gold_grams < NISAB_GRAMS:
        st.warning("⚠️ You do not need to pay Zakat. The minimum threshold (nisab) is 85 grams of gold.")
    else:
        current_zakat =  gold_grams_over_1_year * ZAKAT_PERCENTAGE
        current_zakat_value =  current_zakat * price_per_gram
        current_gold_grams = total_gold_grams - current_zakat

        if gold_grams_over_1_year < NISAB_GRAMS:
            current_gold_grams = total_gold_grams
            current_zakat = 0
            current_zakat_value = 0
            
        initial_value = current_gold_grams * price_per_gram
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
                zakat_value = zakat_grams * price_per_gram
                total_zakat_paid.append(zakat_grams)
                total_zakat_paid_value.append(zakat_value)
                status = "✅ Zakat Due"

            else:
                total_zakat_paid.append(0)
                total_zakat_paid_value.append(0)

            value = current_gold_grams * price_per_gram
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
            if unit == "Pawan":
                st.write(f"You are currently obligated to pay Zakat of: <big>**{current_zakat:,.2f}g ({grams_to_pawan(current_zakat):,.2f} pawan)**</big>, worth <big>**₹{current_zakat_value:,.0f}**</big>", unsafe_allow_html=True)
                st.write(f"The Remaining Gold will be: <big>**{total_gold_grams - current_zakat:,.2f}g ({grams_to_pawan(total_gold_grams - current_zakat):,.2f} pawan)**</big>, worth <big>**₹{initial_value:,.0f}**</big>" , unsafe_allow_html=True)
            else:
                st.write(f"You are currently obligated to pay Zakat of: <big>**{current_zakat:,.2f}g**</big>, worth <big>**₹{current_zakat_value:,.0f}**</big>", unsafe_allow_html=True)
                st.write(f"The Remaining Gold will be: <big>**{total_gold_grams - current_zakat:,.2f}g**</big>, worth <big>**₹{initial_value:,.0f}**</big>" , unsafe_allow_html=True)

        else:
            st.info("The initial gold amount held for over a year is below Nisab, so no Zakat is due currently.")
    

        st.subheader("📋 Yearly Breakdown")
        for yr, zak_gram, current_gram, zak_value, value, status in yearly_results:
            if unit == "Pawan":
                pawan_gram = grams_to_pawan(zak_gram)
                pawan_curr = grams_to_pawan(current_gram)
                
                if status == "✅ Zakat Due":
                    st.write(f"""For year {yr}, Zakat: <big>{zak_gram:,.2f}g ({pawan_gram:,.2f} pawan)</big>, worth <big>₹{zak_value:,.0f}</big>.
                    Gold after Zakat: <big>{current_gram:,.2f}g ({pawan_curr:,.2f} pawan)</big>, worth <big>₹{value:,.0f}</big>""", unsafe_allow_html=True)
                else:
                    st.write(f"""For Year {yrs}, total Gold: <big>{current_gram:,.2f}g ({pawan_curr:,.2f} pawan)</big>, worth <big>₹{value:,.0f}</big>""", unsafe_allow_html=True)

            else:
                if status == "✅ Zakat Due":
                    st.write(f"""For year {yrs}, Zakat: <big>{zak_gram:,.2f}g</big>, worth <big>₹{zak_value:,.0f}</big>.
                    Gold after Zakat: <big>{current_gram:,.2f}g</big>, worth <big>₹{value:,.0f}</big>""", unsafe_allow_html=True)
                else:
                    st.write(f"""For Year {yrs}, total Gold: <big>{current_gram:,.2f}g</big>, worth <big>₹{value:,.0f}</big>""", unsafe_allow_html=True)

        st.subheader("📌 Summary")
        total_zakat_grams = sum(total_zakat_paid)
        pawan_total = grams_to_pawan(total_zakat_grams)

        if unit == "Pawan":
            if total_zakat_grams > 8:
                st.write(f"Total Zakat Paid over {years} years: **{total_zakat_grams:,.2f}g ({pawan_total:,.2f} pawan)**")
            else:
                st.write(f"Total Zakat Paid over {years} years: **{total_zakat_grams:,.2f}g**")
        else:
            st.write(f"Total Zakat Paid over {years} years: **{total_zakat_grams:,.2f}g**")

        st.write(f"Value of Zakat Paid in INR: **₹{sum(total_zakat_paid_value):,.2f}**")
        st.write(f"Final Gold Currently Holding: **{current_gold_grams:,.2f}g**")
        st.write(f"Final Value of Gold Currently Holding: **₹{value:,.2f}**")
        st.write(f"Total Appreciation (After Zakat): **{total_appreciation:.2f}%**")
        st.write(f"Effective Annual Growth (CAGR): **{cagr:.2f}%**")

st.markdown("""
<style>
.disclaimer-box {
    background-color: #f1f3f6;
    padding: 15px 20px;
    border-left: 5px solid #ffcc00;
    border-radius: 8px;
    font-size: 0.9rem;
    color: #333;
    margin-top: 40px;
    line-height: 1.6;
}
.disclaimer-box h4 {
    margin-top: 0;
    color: #cc0000;
}
</style>

<div class="disclaimer-box">
    <h4>⚠️ Disclaimer</h4>
    <ul>
        <li>This calculator follows the <strong>Shafi’i school of jurisprudence</strong> and is for <strong>educational purposes only</strong>. Please consult a <strong>qualified Islamic scholar</strong> for final rulings.</li>
        <li>The calculator assumes assets are held for <strong>less than two years</strong>. If held longer, <strong>zakat for previous years</strong> may apply, which is not calculated here.</li>
        <li>Gold and silver kept <strong>solely for personal jewelry use</strong> (e.g., by women or children) are generally <strong>not zakatable</strong>.</li>
        <li>Asset growth shown is an <strong>estimate only</strong> based on past market trends. Returns are <strong>not guaranteed</strong>.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
