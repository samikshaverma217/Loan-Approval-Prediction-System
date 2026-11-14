import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Loan Approval System", layout="wide")
st.title("🏦 Loan Approval Prediction System")
st.write("Apni details bharo, system batayega Loan milega ya nahi.")

# Sidebar - Input
st.sidebar.header("Applicant Details")
age = st.sidebar.slider("Age", 18, 70, 25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
income = st.sidebar.number_input("Monthly Income (Rs)", 10000, 500000, 50000)
loan_amount = st.sidebar.number_input("Loan Amount (Rs)", 50000, 5000000, 500000)
loan_term = st.sidebar.slider("Loan Term (Months)", 12, 360, 60)
credit_score = st.sidebar.slider("Credit Score (300-850)", 300, 850, 720)
emp_type = st.sidebar.selectbox("Employment", ["Salaried", "Self-Employed"])
education = st.sidebar.selectbox("Education", ["Graduate", "Not Graduate"])

# Prediction Logic
if credit_score > 650 and income > loan_amount * 0.05:
    status = "APPROVED"
    prob = min(95, 60 + (credit_score-650)//10)
    color = "green"
else:
    status = "REJECTED"
    prob = max(15, 70 - (650-credit_score)//10)
    color = "red"

# EMI Calculate
monthly_rate = 0.085 / 12
emi = (loan_amount * monthly_rate * (1+monthly_rate)**loan_term) / ((1+monthly_rate)**loan_term - 1)

# Result
if color == "green":
    st.success(f"### ✅ LOAN {status} - Approval Chance: {prob}%")
else:
    st.error(f"### ❌ LOAN {status} - Approval Chance: {prob}%")

st.write(f"**Estimated Monthly EMI:** Rs {emi:,.0f} | **Credit Score:** {credit_score} | **Employment:** {emp_type}")

# Graphs - 2 columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Credit Score Gauge")
    fig1 = go.Figure(go.Indicator(mode="gauge+number", value=credit_score,
        gauge={'axis': {'range': [300, 850]}, 'bar': {'color': color},
        'steps': [{'range': [300, 650], 'color': "#ffcccc"}, {'range': [650, 850], 'color': "#ccffcc"}]}))
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Approval Probability")
    fig2 = px.pie(values=[prob, 100-prob], names=["Approved Chance", "Reject Chance"], color_discrete_sequence=["green", "red"])
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Income vs Loan Amount")
    fig3 = px.bar(x=["Monthly Income", "Loan Amount"], y=[income, loan_amount], color=["Income", "Loan"], color_discrete_sequence=["blue", "orange"])
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Loan Term vs EMI")
    terms = [12, 24, 36, 60, 120, 240, 360]
    emis = [(loan_amount * monthly_rate * (1+monthly_rate)**t) / ((1+monthly_rate)**t - 1) for t in terms]
    fig4 = px.line(x=terms, y=emis, markers=True, labels={"x": "Months", "y": "EMI (Rs)"})
    st.plotly_chart(fig4, use_container_width=True)
