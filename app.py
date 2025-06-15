import streamlit as st
import random

# ----- Page Setup -----
st.set_page_config(page_title="Pawtection - Pet Insurance", layout="centered")

# ----- Styling -----
st.markdown("""
    <style>
    .big-title {
        text-align: center;
        font-size: 2.5rem;
        color: #2c3e50;
        margin-bottom: 0.2em;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #7f8c8d;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ----- Header -----
st.markdown("<div class='big-title'>🐶 Pawtection</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your trusted third-party dog insurance – built to protect your furry friend 🐾</div>", unsafe_allow_html=True)


# ----- Layout Columns -----
left_col, right_col = st.columns([1, 1])

# ----- Form -----
with left_col:
    with st.form("pet_form"):
        st.markdown("### 🐾 Pet Details")
        col1, col2 = st.columns(2)

        with col1:
            pet_name = st.text_input("🐶 Pet Name", value="Saudi Rich")
            breed = st.selectbox("🐕 Breed", ["Labrador", "Bulldog", "Poodle", "Mixed", "Other"])
            age = st.selectbox("🎀 Age", list(range(0, 21)), format_func=lambda x: f"{x} years")

        with col2:
            gender = st.selectbox("⚧️ Gender", ["Male", "Female"])
            spay_neuter = st.selectbox("✂️ Spay/Neuter", ["Yes", "No"])
            borough = st.selectbox("📍 Borough", ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"])



        st.markdown("</div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔍 Estimate My Premium")

# ----- Output -----
with right_col:

    st.markdown("### 📋 Insurance Summary")
    hint_markdown = st.markdown(f"""
            <div style='background:#fff2cc; padding: 1rem; border-radius: 8px; margin-top:1rem;'>
                <p>To estimate your insurance premium, we'll need to assess your dog's breed, age, and gender, along with their spay/neuter status and your current borough of residence.</p>
            </div>
                """, unsafe_allow_html=True)
    

    
    if submitted:
        hint_markdown.empty()
        # Simulate risk and premium (you can replace this with real logic later)
        biting_risk = random.randint(1, 10)
        base_price = 30
        premium_fee = base_price + (age * 1.5) + (biting_risk * 2)
        
        # Risk color logic
        risk_color = "#27ae60" if biting_risk <= 3 else "#f39c12" if biting_risk <= 7 else "#e74c3c"
        risk_text = f"<span style='font-weight:bold; color:{risk_color}; font-size:1.2rem;'>{biting_risk} / 10</span>"
        premium_text = f"<span style='font-weight:bold; font-size:1.2rem;'>{premium_fee}</span>"
        rsult_markdown = st.markdown(f"""
            <div style='background:#fff2cc; padding: 1rem; border-radius: 8px; margin-top:1rem;'>
                <p><strong>{pet_name}</strong> is a <strong>{age}-year-old {gender.lower()}</strong> <strong>{breed}</strong> living in <strong>{borough}</strong>.</p>
                <p>Spayed/Neutered: <strong>{spay_neuter}</strong></p>
                <p>⚠️ <strong>Estimated Biting Risk:</strong> {risk_text}</p>
                <p>💰 <strong>Estimated Monthly Premium:</strong> ${premium_text}</p> 
            </div>
                """, unsafe_allow_html=True)
