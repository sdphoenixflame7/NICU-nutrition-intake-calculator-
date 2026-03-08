import streamlit as st
import pandas as pd

# --- Configuration & Styling ---
st.set_page_config(page_title="NICU Input Output Calculator", layout="wide")

st.title("👶 NICU Nutrition Calculator")
st.markdown("Calculate daily intake (Kcal, Protein, and Micronutrients) per kg/day based on feeds, additives, and infusions.")

# --- Database extracted directly from 'Data.csv' ---
NUTRITION_DB = {
    "EBM term (ml)": {"base": 100, "Energy (kcal)": 67, "Protein (g)": 1.1, "Lipid (g)": 4.5, "Sodium (mEq)": 0.8, "Potassium (mEq)": 1.5, "Calcium (mg)": 33, "Phosphorus (mg)": 15, "Vit D (IU)": 4, "Iron (mg)": 0.03},
    "EBM preterm (ml)": {"base": 100, "Energy (kcal)": 69, "Protein (g)": 1.9, "Lipid (g)": 3.6, "Sodium (mEq)": 1.2, "Potassium (mEq)": 1.7, "Calcium (mg)": 28, "Phosphorus (mg)": 14, "Vit D (IU)": 4},
    "TERM formula (ml)": {"base": 100, "Energy (kcal)": 68, "Protein (g)": 1.5, "Lipid (g)": 3.4, "Sodium (mEq)": 1.2, "Potassium (mEq)": 1.5, "Calcium (mg)": 64, "Phosphorus (mg)": 40, "Vit D (IU)": 38, "Iron (mg)": 1.1},
    "PRETERM formula (ml)": {"base": 100, "Energy (kcal)": 79, "Protein (g)": 2.0, "Lipid (g)": 3.9, "Sodium (mEq)": 1.4, "Potassium (mEq)": 1.5, "Calcium (mg)": 101, "Phosphorus (mg)": 50, "Vit D (IU)": 80, "Iron (mg)": 1.2},
    "LD (ml)": {"base": 100, "Energy (kcal)": 68, "Protein (g)": 2.2, "Sodium (mEq)": 2.3, "Potassium (mEq)": 1.5, "Calcium (mg)": 140, "Phosphorus (mg)": 7, "Vit D (IU)": 30, "Iron (mg)": 0.9},
    "HMF 1g (sachets)": {"base": 1, "Energy (kcal)": 3.37, "Protein (g)": 0.27, "Lipid (g)": 0.04, "Sodium (mEq)": 0.08, "Potassium (mEq)": 0.23, "Calcium (mg)": 15.8, "Phosphorus (mg)": 7.9, "Vit D (IU)": 3.32, "Iron (mg)": 0.3},
    "Tonoferon (ml)": {"base": 1, "Iron (mg)": 25, "Vit B12": 5},
    "Arbivit (ml)": {"base": 1, "Vit D (IU)": 800},
    "Osteocal (ml)": {"base": 1, "Calcium (mg)": 16.4, "Phosphorus (mg)": 8.2, "Vit D (IU)": 80},
    "Calcimax P (ml)": {"base": 1, "Calcium (mg)": 30, "Magnesium (mg)": 15, "Vit D (IU)": 20, "Zinc (mg)": 3},
    "Zincovit (ml)": {"base": 1, "Energy (kcal)": 2.3, "Vit D (IU)": 10, "Vit A (IU)": 30, "Zinc (mg)": 0.4},
    "Isolyte P (ml)": {"base": 100, "Energy (kcal)": 17, "Sodium (mEq)": 2.3, "Potassium (mEq)": 2, "Mg (mEq)": 0.3},
    "GIR (gm dextrose)": {"base": 1, "Energy (kcal)": 3.4},
    "3% Nacl (ml)": {"base": 1, "Sodium (mEq)": 2},
    "KCl (ml)": {"base": 1, "Potassium (mEq)": 0.5},
    "Ca Gluconate (ml)": {"base": 1, "Calcium (mg)": 100},
    "Adphos (sachets)": {"base": 1, "Phosphorus (mg)": 500}
}

NUTRIENTS = [
    "Energy (kcal)", "Protein (g)", "Lipid (g)", "Sodium (mEq)", "Potassium (mEq)", 
    "Calcium (mg)", "Magnesium (mg)", "Phosphorus (mg)", "Vit D (IU)", "Vit A (IU)", 
    "Iron (mg)", "Vit B12", "Zinc (mg)", "Mg (mEq)"
]

# --- UI Layout: Inputs ---
st.header("1. Patient Details")
weight = st.number_input("Baby Weight (kg)", min_value=0.4, max_value=10.0, value=3.88, step=0.01)

st.header("2. Daily Intake (24h)")
col1, col2, col3 = st.columns(3)

inputs = {}

with col1:
    st.subheader("🍼 Feeds (ml)")
    inputs["EBM term (ml)"] = st.number_input("EBM term", 0.0, value=840.0)
    inputs["EBM preterm (ml)"] = st.number_input("EBM preterm", 0.0)
    inputs["TERM formula (ml)"] = st.number_input("TERM formula", 0.0)
    inputs["PRETERM formula (ml)"] = st.number_input("PRETERM formula", 0.0)
    inputs["LD (ml)"] = st.number_input("LD", 0.0)

with col2:
    st.subheader("💊 Supplements")
    inputs["HMF 1g (sachets)"] = st.number_input("HMF (sachets)", 0.0)
    inputs["Adphos (sachets)"] = st.number_input("Adphos (sachets)", 0.0)
    inputs["Tonoferon (ml)"] = st.number_input("Tonoferon", 0.0)
    inputs["Arbivit (ml)"] = st.number_input("Arbivit", 0.0)
    inputs["Osteocal (ml)"] = st.number_input("Osteocal", 0.0)
    inputs["Calcimax P (ml)"] = st.number_input("Calcimax P", 0.0)
    inputs["Zincovit (ml)"] = st.number_input("Zincovit", 0.0)

with col3:
    st.subheader("💧 Infusions")
    inputs["Isolyte P (ml)"] = st.number_input("Isolyte P (ml)", 0.0)
    inputs["GIR (gm dextrose)"] = st.number_input("GIR (gm dextrose)", 0.0)
    inputs["3% Nacl (ml)"] = st.number_input("3% NaCl", 0.0)
    inputs["KCl (ml)"] = st.number_input("KCl", 0.0)
    inputs["Ca Gluconate (ml)"] = st.number_input("Ca Gluconate", 0.0)

# --- Calculation Engine ---
totals = {nut: 0.0 for nut in NUTRIENTS}
active_inputs = {}

for item, amount in inputs.items():
    if amount > 0:
        active_inputs[item] = amount
        db_entry = NUTRITION_DB[item]
        multiplier = amount / db_entry["base"]
        
        for nutrient in NUTRIENTS:
            if nutrient in db_entry:
                totals[nutrient] += db_entry[nutrient] * multiplier

# --- Results Presentation ---
st.divider()
st.header("3. Nutritional Status")

if weight > 0:
    results_data = []
    for nut in NUTRIENTS:
        total_val = totals[nut]
        if total_val > 0:
            results_data.append({
                "Nutrient": nut,
                "Total (24h absolute)": round(total_val, 2),
                "Per Kg / Day": round(total_val / weight, 2)
            })

    if results_data:
        df_results = pd.DataFrame(results_data)
        
        st.subheader("Key Macros (Per kg/day)")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Energy", f"{totals['Energy (kcal)'] / weight:.1f} kcal")
        m2.metric("Protein", f"{totals['Protein (g)'] / weight:.2f} g")
        m3.metric("Calcium", f"{totals['Calcium (mg)'] / weight:.1f} mg")
        m4.metric("Phosphorus", f"{totals['Phosphorus (mg)'] / weight:.1f} mg")
        
        st.subheader("Detailed Breakdown")
        st.dataframe(df_results, use_container_width=True, hide_index=True)

        # --- EXPORT SECTION ---
        st.divider()
        st.subheader("📥 Export Patient Record")
        
        # 1. CSV Export Configuration
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')
            
        csv = convert_df(df_results)
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            st.download_button(
                label="📊 Download CSV Data",
                data=csv,
                file_name=f"nicu_nutrition_{weight}kg.csv",
                mime="text/csv",
                help="Download the calculated table to open in Excel."
            )
            
        with col_exp2:
            st.info("📄 **Print to PDF:** To save this entire dashboard to a patient's file, simply press **Ctrl + P** (or **Cmd + P** on Mac) and select **'Save as PDF'**.")

    else:
        st.info("Enter input values above to see the calculation.")
else:
    st.error("Baby weight must be greater than 0.")
