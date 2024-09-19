import streamlit as st
import numpy as np
import numpy_financial as npf

st.title("Real Estate ROI Calculator")

# Description of cases
st.write("""
**Scenario Descriptions:**

- **Bear:** Prolonged decrease in property values, high initial and ongoing vacancy, negative rent growth compared to expense growth.
- **Base:** Our conservative assumptions on slight decrease in market values, high initial vacancy and moderate vacancy thereafter, and slight positive rent growth compared to expense growth.
- **Bull:** Neutral or increasing property value, low initial vacancy, and near zero vacancy thereafter, and moderate rent growth compared to expenses.
""")

# User selects the case
case = st.selectbox("Select Case", ["Bear", "Base", "Bull"])

# Set default values based on case
if case == "Bear":
    cap_rate_refinance = 8.0
    cap_rate_sale = 8.0
    y1_vacancy = 15.0
    ongoing_vacancy = 10.0
    expense_growth = 5.0
    rent_growth = 1.0
elif case == "Base":
    cap_rate_refinance = 7.0
    cap_rate_sale = 7.0
    y1_vacancy = 10.0
    ongoing_vacancy = 7.0
    expense_growth = 3.0
    rent_growth = 3.0
else:  # Bull
    cap_rate_refinance = 6.0
    cap_rate_sale = 6.0
    y1_vacancy = 5.0
    ongoing_vacancy = 5.0
    expense_growth = 2.0
    rent_growth = 5.0

# Allow user to adjust the inputs
st.subheader("Adjust the inputs (all percentages):")

cap_rate_refinance = st.number_input("Cap Rate at Refinance (%)", value=cap_rate_refinance, min_value=0.0, max_value=100.0)
cap_rate_sale = st.number_input("Cap Rate at Sale (%)", value=cap_rate_sale, min_value=0.0, max_value=100.0)
y1_vacancy = st.number_input("Year 1 Vacancy Rate (%)", value=y1_vacancy, min_value=0.0, max_value=100.0)
ongoing_vacancy = st.number_input("Ongoing Annual Vacancy Rate (%)", value=ongoing_vacancy, min_value=0.0, max_value=100.0)
expense_growth = st.number_input("Expense Growth Rate (%)", value=expense_growth, min_value=0.0, max_value=100.0)
rent_growth = st.number_input("Rent Growth Rate (%)", value=rent_growth, min_value=0.0, max_value=100.0)

# Perform calculations

# Convert percentages to decimals
cap_rate_refinance /= 100.0
cap_rate_sale /= 100.0
y1_vacancy /= 100.0
ongoing_vacancy /= 100.0
expense_growth /= 100.0
rent_growth /= 100.0

# Initial assumptions
purchase_price = 1000000  # $1,000,000
initial_gpr = 150000  # $150,000 per year
initial_expenses = 60000  # $60,000 per year

holding_period = 5  # 5 years
ltv = 0.7  # 70% loan to value
loan_interest_rate = 0.05  # 5% interest rate
loan_amortization = 30  # 30 years amortization
selling_costs = 0.05  # 5% selling costs

# Initial loan amount
initial_loan_amount = purchase_price * ltv
initial_equity = purchase_price - initial_loan_amount

# Loan payment calculation
monthly_rate = loan_interest_rate / 12
n_total_payments = loan_amortization * 12
monthly_payment = -npf.pmt(monthly_rate, n_total_payments, initial_loan_amount)
annual_debt_service = monthly_payment * 12

# Calculate annual cash flows
cash_flows = [-initial_equity]  # Year 0 cash flow is initial equity investment (negative)

gpr = initial_gpr
expenses = initial_expenses

for year in range(1, holding_period + 1):
    # Adjust GPR and expenses
    if year == 1:
        vacancy_rate = y1_vacancy
    else:
        vacancy_rate = ongoing_vacancy

    gpr *= (1 + rent_growth)
    expenses *= (1 + expense_growth)

    egi = gpr * (1 - vacancy_rate)
    noi = egi - expenses

    if year == 2:
        # Refinance occurs
        property_value = noi / cap_rate_refinance
        new_loan_amount = property_value * ltv

        # Calculate existing loan balance
        n_payments_made = (year - 1) * 12
        n_remaining_payments = n_total_payments - n_payments_made
        existing_loan_balance = -npf.pv(monthly_rate, n_remaining_payments, monthly_payment, fv=0)

        # Cash out from refinance
        cash_out = new_loan_amount - existing_loan_balance

        # Update loan amount and payment
        loan_balance = new_loan_amount
        monthly_payment = -npf.pmt(monthly_rate, n_total_payments, loan_balance)
        annual_debt_service = monthly_payment * 12

        cash_flow_from_operations = noi - annual_debt_service
        # Add cash out from refinance
        cash_flow = cash_flow_from_operations + cash_out
    else:
        cash_flow_from_operations = noi - annual_debt_service
        cash_flow = cash_flow_from_operations

    if year == holding_period:
        # Sale occurs
        property_value = noi / cap_rate_sale
        sale_proceeds = property_value * (1 - selling_costs)

        # Calculate outstanding loan balance
        n_payments_made = (year - 1) * 12
        n_remaining_payments = n_total_payments - n_payments_made
        loan_balance = -npf.pv(monthly_rate, n_remaining_payments, monthly_payment, fv=0)

        net_sale_proceeds = sale_proceeds - loan_balance

        cash_flow += net_sale_proceeds

    cash_flows.append(cash_flow)

# Compute IRR
irr = npf.irr(cash_flows) * 100  # Convert to percentage

# Display the IRR
st.subheader(f"Calculated IRR: {irr:.2f}%")