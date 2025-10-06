import streamlit as st
import pandas as pd
from io import BytesIO

st.title("SAP MM PO/GR/IR Reconciliation Tool")

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

    # Display summary
    st.subheader("Summary Metrics")
    st.write(f"Total POs: {len(merged_df)}")
    st.write(f"Missing GRs: {merged_df['missing_gr'].sum()}")
    st.write(f"Missing IRs: {merged_df['missing_ir'].sum()}")

    # Show merged data
    st.subheader("Reconciled Data")
    st.dataframe(merged_df)

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