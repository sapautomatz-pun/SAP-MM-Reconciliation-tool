import streamlit as st
import pandas as pd
from io import BytesIO

st.title("SAP MM PO/GR/IR Reconciliation Tool with Gen AI Summary")

# Upload CSV files
po_file = st.file_uploader("Upload PO File (po.csv)", type="csv")
gr_file = st.file_uploader("Upload GR File (gr.csv)", type="csv")
ir_file = st.file_uploader("Upload IR File (ir.csv)", type="csv")

if po_file and gr_file and ir_file:
    # Read the uploaded files
    po_df = pd.read_csv(po_file)
    gr_df = pd.read_csv(gr_file)
    ir_df = pd.read_csv(ir_file)

    # Merge PO with GR and IR
    merged_df = po_df.merge(gr_df, on=["PO", "vendor"], how="left")
    merged_df = merged_df.merge(ir_df, on=["PO", "vendor"], how="left")

    # Convert date columns to datetime
    merged_df["order_date"] = pd.to_datetime(merged_df["order_date"])
    merged_df["expected_delivery"] = pd.to_datetime(merged_df["expected_delivery"])
    merged_df["gr_date"] = pd.to_datetime(merged_df["gr_date"])
    merged_df["ir_date"] = pd.to_datetime(merged_df["ir_date"])

    # Calculate delays
    merged_df["delivery_delay_days"] = (merged_df["gr_date"] - merged_df["expected_delivery"]).dt.days
    merged_df["invoice_delay_days"] = (merged_df["ir_date"] - merged_df["gr_date"]).dt.days

    # Highlight missing GR or IR
    merged_df["missing_gr"] = merged_df["gr_date"].isna()
    merged_df["missing_ir"] = merged_df["ir_date"].isna()

    # Display summary metrics
    st.subheader("Summary Metrics")
    total_pos = len(merged_df)
    missing_grs = merged_df["missing_gr"].sum()
    missing_irs = merged_df["missing_ir"].sum()
    avg_delivery_delay = merged_df["delivery_delay_days"].mean()
    avg_invoice_delay = merged_df["invoice_delay_days"].mean()

    st.write(f"Total POs: {total_pos}")
    st.write(f"Missing GRs: {missing_grs}")
    st.write(f"Missing IRs: {missing_irs}")
    st.write(f"Average Delivery Delay (days): {avg_delivery_delay:.2f}")
    st.write(f"Average Invoice Delay (days): {avg_invoice_delay:.2f}")

    # Display reconciled data
    st.subheader("Reconciled Data")
    st.dataframe(merged_df)

    # Gen AI-powered summary (simulated)
    st.subheader("🧠 Gen AI-Powered Summary")
    ai_summary = f"""
    📊 Summary Report:
    Out of {total_pos} purchase orders, {missing_grs} are missing goods receipts and {missing_irs} are missing invoice receipts.
    The average delivery delay is {avg_delivery_delay:.2f} days, indicating moderate delays in vendor deliveries.
    The average invoice delay is {avg_invoice_delay:.2f} days, suggesting potential bottlenecks in invoice processing.
    ✅ Recommendation: Follow up with vendors for missing GRs and streamline the IR process to improve efficiency.
    """
    st.info(ai_summary)

    # Download reconciled report
    def convert_df(df):
        output = BytesIO()
        df.to_csv(output, index=False)
        return output.getvalue()

    csv_data = convert_df(merged_df)
    st.download_button(
        label="Download Reconciliation Report",
        data=csv_data,
        file_name="reconciliation_report.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload all three files (PO, GR, IR) to proceed.")