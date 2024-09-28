import streamlit as st

st.title("Sterling Apartments IRR Calculator")

# Display a local image
st.header("Sterling Property")

st.image("images/sterling-property.png", caption="Sterling Property", use_column_width=True)

st.write("""
We're excited to offer investors the opportunity to invest in Sterling Realty Apartments, a 72-unit multifamily property located in Barrington, NH, a Class-B submarket in the seacoast region of New Hampshire. This deal was sourced off-market, direct-to-seller, from a direct mail letter. We only competed with two other buyers, enabling us to secure this deal at below-market pricing.
""")

# Description of cases
st.write("""
**Scenario Descriptions:**

- **Bear:** Prolonged decrease in property values, high initial and ongoing vacancy, negative rent growth compared to expense growth.
- **Base:** Our conservative assumptions on slight decrease in market values, high initial vacancy and moderate vacancy thereafter, and slight positive rent growth compared to expense growth.
- **Bull:** Neutral or increasing property value, low initial vacancy, and near zero vacancy thereafter, and moderate rent growth compared to expenses.
""")

# Hardcoded values for each scenario
scenarios = {
    "Bear": {
        "cap_rate_refinance": 7.0,
        "cap_rate_sale": 7.15,
        "y1_vacancy": 20.0,
        "ongoing_vacancy": 10.0,
        "expense_growth": 3.0,
        "rent_growth": 2.0,
        "irr": 5.83
    },
    "Base": {
        "cap_rate_refinance": 6.7,
        "cap_rate_sale": 6.85,
        "y1_vacancy": 15.0,
        "ongoing_vacancy": 5.0,
        "expense_growth": 2.5,
        "rent_growth": 3.0,
        "irr": 15.54
    },
    "Bull": {
        "cap_rate_refinance": 6.4,
        "cap_rate_sale": 6.45,
        "y1_vacancy": 8.0,
        "ongoing_vacancy": 2.0,
        "expense_growth": 2.0,
        "rent_growth": 4.0,
        "irr": 20.80
    }
}

# User selects the case
case = st.selectbox("Select Case", ["Bear", "Base", "Bull"])

# Get the selected scenario's values
selected_values = scenarios[case]

# Display the values for the selected case
st.subheader(f"{case} Case")
st.write(f"Cap Rate at Refinance: {selected_values['cap_rate_refinance']}%")
st.write(f"Cap Rate at Sale: {selected_values['cap_rate_sale']}%")
st.write(f"Year 1 Vacancy Rate: {selected_values['y1_vacancy']}%")
st.write(f"Ongoing Annual Vacancy Rate: {selected_values['ongoing_vacancy']}%")
st.write(f"Expense Growth Rate: {selected_values['expense_growth']}%")
st.write(f"Rent Growth Rate: {selected_values['rent_growth']}%")
st.write(f"**IRR: {selected_values['irr']:.2f}%**")
