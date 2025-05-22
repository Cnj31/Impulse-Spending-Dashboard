
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

st.set_page_config(page_title="Impulse Spending Insights", layout="wide")

st.title("💡 Impulse Spending Intelligence Dashboard")
st.markdown("Upload your transaction data to uncover patterns, triggers, and behavioral trends in your spending habits.")

# Theme toggle
theme = st.radio("🌓 Choose Theme:", ["Light", "Dark"])
plot_bgcolor = "white" if theme == "Light" else "#1e1e1e"
paper_bgcolor = plot_bgcolor
font_color = "black" if theme == "Light" else "white"

# Upload section
uploaded_file = st.file_uploader("📁 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    total_txns = len(df)
    impulse_txns = df["Is_Impulse"].sum()
    impulse_pct = round((impulse_txns / total_txns) * 100, 2)
    avg_txn = round(df["Amount_Magnitude"].mean(), 2)
    avg_impulse_amt = round(df[df["Is_Impulse"] == 1]["Amount_Magnitude"].mean(), 2)
    post_salary_impulses = df[df["Post_Salary_Window"] == 1]["Is_Impulse"].sum()
    weekend_impulses = df[df["Is_Weekend"] == 1]["Is_Impulse"].sum()

    st.subheader("📊 Key Performance Indicators (KPIs)")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Transactions", total_txns)
    k2.metric("Impulse Transactions", impulse_txns, f"{impulse_pct}%")
    k3.metric("Avg Spend (All)", f"€{avg_txn}")
    k4.metric("Avg Impulse Spend", f"€{avg_impulse_amt}")

    with st.expander("🧠 Behavioral Stats"):
        st.markdown(f"- 💥 **Weekend Impulses:** {weekend_impulses}")
        st.markdown(f"- 💸 **Post-Salary Impulses:** {post_salary_impulses}")
        st.markdown(f"- ⏱️ **Evening/Night Impulses:** {df[df['Time_Bucket_Score'] >= 0.7]['Is_Impulse'].sum()}")

    # Risk Meter
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
                   {'range': [70, 100], 'color': "red"}]},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    fig.update_layout(paper_bgcolor=paper_bgcolor, font_color=font_color)
    st.plotly_chart(fig, use_container_width=True)

    # Impulse by Category
    st.subheader("🛍️ Impulse Frequency by Category")
    cat_fig = px.bar(df[df["Is_Impulse"] == 1].groupby("Category").size().reset_index(name="Count"),
                     x="Category", y="Count", color="Count",
                     title="Impulse Transactions by Category",
                     template="plotly_dark" if theme == "Dark" else "plotly_white")
    st.plotly_chart(cat_fig, use_container_width=True)

    # Day of Week Chart
    st.subheader("📅 Impulse by Day of Week")
    df["Day of Week"] = pd.Categorical(df["Day of Week"],
                                       categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                       ordered=True)
    dow_fig = px.bar(df[df["Is_Impulse"] == 1].groupby("Day of Week").size().reset_index(name="Impulses"),
                     x="Day of Week", y="Impulses", color="Impulses",
                     title="Weekly Impulse Behavior",
                     template="plotly_dark" if theme == "Dark" else "plotly_white")
    st.plotly_chart(dow_fig, use_container_width=True)

    # Alerts
    st.subheader("🚨 Personalized Insight")
    if impulse_pct > 70:
        st.error("🚫 Critical: Your impulse spending is extremely high. Set strict budgets.")
    elif impulse_pct > 50:
        st.warning("⚠️ High impulse risk detected. Consider tracking your weekend and late-night spending.")
    elif impulse_pct > 30:
        st.info("🟡 Moderate impulse activity. Watch your discretionary expenses.")
    else:
        st.success("✅ Great job! Your spending is under control.")

    if impulse_pct < 25:
        st.balloons()
        st.success("🏅 Congratulations! Your impulse control is exceptional this month.")

    # Download Report
    st.subheader("⬇️ Download Clean Report")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Impulse_Report")
        writer.save()
        st.download_button(
            label="Download Excel Report",
            data=buffer,
            file_name="Impulse_Spending_Insights.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Data View
    with st.expander("📄 View Raw Transaction Data"):
        st.dataframe(df.head(100))

else:
    st.info("Please upload the feature-engineered Excel dataset to begin analysis.")
