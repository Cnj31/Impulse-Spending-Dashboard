
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

st.set_page_config(page_title="Impulse Spending Predictor", layout="wide")

st.title("💸 Advanced Impulse Spending Dashboard")
st.markdown("Upload your cleaned transaction data to view deep insights into impulsive behavior.")

# Theme Toggle
theme = st.radio("🌓 Choose Theme:", ["Light", "Dark"])
plot_bgcolor = "white" if theme == "Light" else "#1e1e1e"
paper_bgcolor = plot_bgcolor
font_color = "black" if theme == "Light" else "white"

# Upload file
uploaded_file = st.file_uploader("📁 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Basic KPIs
    total_txns = len(df)
    impulse_txns = df["Is_Impulse"].sum()
    impulse_pct = round((impulse_txns / total_txns) * 100, 2)

    st.subheader("📊 Overview Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", total_txns)
    col2.metric("Impulse Transactions", impulse_txns)
    col3.metric("Impulse Rate", f"{impulse_pct}%")

    # Gauge chart
    st.subheader("🧭 Impulse Risk Meter")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=impulse_pct,
        title={'text': "Impulse Risk Level"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "crimson"},
               'bgcolor': paper_bgcolor,
               'steps': [
                   {'range': [0, 30], 'color': "lightgreen"},
                   {'range': [30, 70], 'color': "orange"},
                   {'range': [70, 100], 'color': "red"}]}
    ))
    fig.update_layout(paper_bgcolor=paper_bgcolor, font_color=font_color)
    st.plotly_chart(fig, use_container_width=True)

    # Trigger insights
    st.subheader("🎯 Trigger Summary")
    triggers = {
        "Weekend": df[df["Is_Impulse"] == 1]["Is_Weekend"].sum(),
        "Low Amount (< €60)": df[df["Is_Impulse"] == 1]["Is_Low_Amount"].sum(),
        "Evening/Night Time": df[df["Is_Impulse"] == 1]["Time_Bucket_Score"].ge(0.7).sum(),
        "Post-Salary Window": df[df["Is_Impulse"] == 1]["Post_Salary_Window"].sum(),
        "High-Risk Merchant": df[df["Is_Impulse"] == 1]["Is_Impulse_Merchant"].sum(),
        "High-Risk Category": df[df["Is_Impulse"] == 1]["Is_Impulse_Category"].sum()
    }
    for k, v in triggers.items():
        st.markdown(f"- ✅ **{k}** triggered **{v}** impulse transactions")

    # Weekly pattern
    st.subheader("📅 Weekly Behavior Summary")
    df["Day of Week"] = pd.Categorical(df["Day of Week"],
                                       categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                       ordered=True)
    weekly_summary = df[df["Is_Impulse"] == 1].groupby("Day of Week").size().reset_index(name="Impulse Count")
    fig_bar = px.bar(weekly_summary, x="Day of Week", y="Impulse Count",
                     title="Impulse Spending by Day of Week", color="Impulse Count",
                     template="plotly_dark" if theme == "Dark" else "plotly_white")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Recommendation system
    st.subheader("🚨 Alerts & Recommendations")
    if impulse_pct > 60:
        st.error("⚠️ High Risk: Spending control strongly recommended.")
    elif impulse_pct > 30:
        st.warning("🟠 Moderate Risk: Monitor spending on weekends and late nights.")
    else:
        st.success("🟢 Low Risk: Great job managing spending impulses!")

    # Achievement
    if impulse_pct < 25:
        st.balloons()
        st.success("🏅 Excellent! Impulse rate is below 25%.")

    # Downloadable report (corrected)
    st.subheader("⬇️ Download Clean Report")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Impulse Report")
    buffer.seek(0)
    st.download_button(
        label="Download Excel Report",
        data=buffer,
        file_name="Impulse_Spending_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Data view
    with st.expander("🔍 View Sample Data"):
        st.dataframe(df.head(50))

else:
    st.info("Please upload a processed transaction Excel file.")
