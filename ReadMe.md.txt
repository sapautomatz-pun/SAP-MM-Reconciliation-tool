# SAP MM PO/GR/IR Reconciliation Tool

This Streamlit app allows SAP consultants and analysts to upload and reconcile Purchase Orders (PO), Goods Receipts (GR), and Invoice Receipts (IR) data. It highlights missing entries, calculates delays, and provides a downloadable report for analysis and audit purposes.

---

## 🚀 Features

- Upload `po.csv`, `gr.csv`, and `ir.csv` files
- Automatically merges and reconciles data
- Highlights missing GR and IR entries
- Calculates delivery and invoice delay durations
- Displays summary metrics and detailed report
- Allows downloading the final reconciled report as CSV

---

## 📁 Sample File Formats

### `po.csv`
| PO     | vendor   | order_date | expected_delivery | net_price | currency |
|--------|----------|------------|-------------------|-----------|----------|
| PO1001 | VendorA  | 2023-07-01 | 2023-07-10        | 15000     | INR      |

### `gr.csv`
| PO     | vendor   | gr_date    |
|--------|----------|------------|
| PO1001 | VendorA  | 2023-07-11 |

### `ir.csv`
| PO     | vendor   | ir_date    | invoice_amount |
|--------|----------|------------|----------------|
| PO1001 | VendorA  | 2023-07-12 | 15000          |

---

## ⚙️ Setup Instructions

1. Clone this repository or download the files manually.
2. Ensure you have **Python 3.8+** installed.
3. Install required packages:
   ```bash
   pip install streamlit pandas