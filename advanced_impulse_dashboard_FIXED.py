# Corrected export block for advanced_impulse_dashboard.py

    # Download button (corrected)
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
