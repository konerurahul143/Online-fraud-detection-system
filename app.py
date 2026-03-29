import streamlit as st
import pickle
import pandas as pd

# Load model
model = pickle.load(open('fraud_model.pkl', 'rb'))

st.title("💳 Fraud Detection System")

st.write("Enter transaction details below:")

# Inputs
step = st.number_input("Step", min_value=0, value=1)
amount = st.number_input("Amount", min_value=0.0, value=1000.0)
oldbalanceOrg = st.number_input("Old Balance (Origin)", min_value=0.0, value=5000.0)
newbalanceOrig = st.number_input("New Balance (Origin)", min_value=0.0, value=3000.0)
oldbalanceDest = st.number_input("Old Balance (Destination)", min_value=0.0, value=0.0)
newbalanceDest = st.number_input("New Balance (Destination)", min_value=0.0, value=2000.0)

# Transaction type
type_option = st.selectbox("Transaction Type", ["CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"])

# Convert type to dummy variables
CASH_OUT = 1 if type_option == "CASH_OUT" else 0
DEBIT = 1 if type_option == "DEBIT" else 0
PAYMENT = 1 if type_option == "PAYMENT" else 0
TRANSFER = 1 if type_option == "TRANSFER" else 0

# Predict button
if st.button("Predict"):
    
    input_data = pd.DataFrame([[
        step, amount, oldbalanceOrg, newbalanceOrig,
        oldbalanceDest, newbalanceDest,
        CASH_OUT, DEBIT, PAYMENT, TRANSFER
    ]], columns=[
        'step', 'amount', 'oldbalanceOrg', 'newbalanceOrig',
        'oldbalanceDest', 'newbalanceDest',
        'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'
    ])
    
    prediction = model.predict(input_data)
    prob = model.predict_proba(input_data)
    
    if prediction[0] == 1:
        st.error(f"⚠️ Fraud Transaction (Confidence: {prob[0][1]:.2f})")
    else:
        st.success(f"✅ Legit Transaction (Confidence: {prob[0][0]:.2f})")