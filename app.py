import math
import pandas as pd
import streamlit as st
import joblib

def main():
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
        with st.form("pet_form",border=False):
            st.markdown("### 🐾 Pet Details")
            form_col_left, form_col_right = st.columns(2)

            with form_col_left:
                isBite = st.selectbox("🩸 Bite Before", ["Please Select..","Yes", "No"])
                breed = st.selectbox("🐕 Breed", ["Please Select..","German Shepherd","Pit Bull","Rottweiler","Bulldog","Siberian Husky","Mixed Breed","Others"])
                age = st.selectbox("🎀 Age", list(range(1, 20)), format_func=lambda x: f"{x} years")

            with form_col_right:
                gender = st.selectbox("⚧️ Gender", ["Please Select..","Male", "Female"])
                spay_neuter = st.selectbox("✂️ Spay/Neuter", ["Please Select..","Yes", "No"])
                borough = st.selectbox("📍 Borough", ["Please Select..","Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island", "Others"])

            submitted = st.form_submit_button("🔍 Estimate My Premium")

    # ----- Load Model -----
    model = joblib.load("dog_bite_score_predictor.pkl")

    # ----- Output -----
    with right_col:
        st.markdown("### 📋 Insurance Summary")
        hint_markdown = st.markdown(f"""
                <div style='background:#fff2cc; padding: 1rem; border-radius: 8px; margin-top:1rem;'>
                    <p style='color: black;'>To estimate your insurance premium, we'll need your dog's breed, age, gender, spay/neuter status, bite history, and your current borough of residence.</p>
                </div>
                    """, unsafe_allow_html=True)
        
        if submitted:
            if "Please Select.." in [isBite, breed, gender, spay_neuter, borough]:
                st.warning("🚫 Please make sure all dropdown fields are selected before estimating the premium.")
            else:
                hint_markdown.empty()
                # Simulate risk and premium (you can replace this with real logic later)
                isBite_map = {"Yes": 1, "No": 0}
                breed_map = {"German Shepherd":1,"Pit Bull":2,"Rottweiler":3,"Bulldog":4,"Siberian Husky":5,"Mixed Breed":6,"Others":7}
                gender_map = {"Male": 1, "Female": 2}
                spay_map = {"Yes": 1, "No": 0}
                borough_map = {"Manhattan": 1, "Brooklyn": 6, "Queens": 4, "Bronx": 3, "Staten Island": 5, "Others": 2}

                # Fallback for unknown breeds
                encoded_breed = breed_map.get(breed, 7)
                encoded_gender = gender_map.get(gender, 1)
                encoded_spay = spay_map.get(spay_neuter, 0)
                encoded_borough = borough_map.get(borough, 1)
                encoded_isBite = isBite_map.get(isBite, 1)

                new_data = pd.DataFrame({
                    'Breed': [encoded_breed],
                    'Age': [age],
                    'Gender': [encoded_gender],
                    'SpayNeuter': [encoded_spay],
                    'Borough': [encoded_borough],
                    'IsBite': [encoded_isBite]  # Always 1 to trigger bite risk estimation
                })
                biting_risk = int(model.predict(new_data)[0])
                base_price = 46
                premium_fee = math.ceil(base_price * (1 + (biting_risk / 100)))
                
                # Risk color logic
                risk_color = "#27ae60" if biting_risk <= 30 else "#f39c12" if biting_risk <= 70 else "#e74c3c"
                risk_text = f"<span style='font-weight:bold; color:{risk_color}; font-size:1.2rem;'>{biting_risk} / 100</span>"
                premium_text = f"<span style='font-weight:bold; font-size:1.2rem;'>{premium_fee}</span>"
                rsult_markdown = st.markdown(f"""
                    <div style='background:#fff2cc; padding: 1rem; border-radius: 8px; margin-top:1rem;'>
                        <p style='color: black;'>Your dog is a <strong>{age}-year-old {gender.lower()}</strong> <strong>{breed}</strong> living in <strong>{borough}</strong> borough.</p>
                        <p style='color: black;'>Spayed/Neutered: <strong>{spay_neuter}</strong></p>
                        <p style='color: black;'>Bite before: <strong>{isBite}</strong></p>
                        <p style='color: black;'>⚠️ <strong>Estimated Biting Risk:</strong> {risk_text}</p>
                        <p style='color: black;'>💰 <strong>Estimated Monthly Premium:</strong> ${premium_text}</p> 
                    </div>
                        """, unsafe_allow_html=True)
            
if __name__ == "__main__":
    main()
