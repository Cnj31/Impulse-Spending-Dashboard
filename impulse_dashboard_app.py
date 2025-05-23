
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Impulse Spending Predictor", layout="wide")

# Step 1: File Upload
st.title("📂 Upload Your Bank Transaction Data")
file = st.file_uploader("Upload Excel or CSV file", type=['csv', 'xlsx'])

if file:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.success("✅ File uploaded successfully!")

    # Sidebar filter
    st.sidebar.title("User Filters")
    if "User_ID" in df.columns:
        user_id = st.sidebar.selectbox("Select User ID", df['User_ID'].unique())
        df = df[df['User_ID'] == user_id]

    st.title("📊 Impulse Spending Dashboard")

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", len(df))
    col2.metric("Impulse Purchases", int(df['Is_Impulse'].sum()) if 'Is_Impulse' in df else "N/A")
    col3.metric("Avg Impulse Score", f"{df['Impulse_Score'].mean():.2f}" if 'Impulse_Score' in df else "N/A")

    # Weekly Spend Trend
    if 'Week' in df.columns:
        st.subheader("📅 Weekly Spending Trend")
        weekly = df.groupby('Week')['Amount'].sum().reset_index()
        fig1 = px.line(weekly, x='Week', y='Amount', title='Spending Over Time')
        st.plotly_chart(fig1)

    # Trigger Analysis Bar Chart
    trigger_cols = ['Post_Salary_Window', 'Weekend_Flag', 'Time_of_Day_Bucket']
    existing_triggers = [col for col in trigger_cols if col in df.columns]
    if existing_triggers:
        st.subheader("🎯 Trigger Breakdown")
        trigger_counts = df[existing_triggers].apply(pd.Series.value_counts).fillna(0)
        st.bar_chart(trigger_counts)

    # Real-Time Alert Simulation
    st.subheader("🚨 Impulse Risk Alert")
    if 'Impulse_Score' in df.columns:
        last = df.sort_values('Timestamp').iloc[-1]
        if last['Impulse_Score'] > 0.7:
            st.warning("High Impulse Risk Detected on Last Transaction")
        else:
            st.success("Last Transaction is Low Risk")

    # Monthly Summary
    st.subheader("📅 Monthly Summary")
    if 'Month' in df.columns:
        monthly = df.groupby('Month').agg({'Amount': 'sum', 'Is_Impulse': 'sum'})
        st.dataframe(monthly)
else:
    st.info("Please upload a transaction file to continue.")
