import streamlit as st
import pandas as pd
import numpy as np

def calculate_unmatched(df1, df2, col_mappings):
    # Adjust columns based on user input
    df1_cols = [col_mappings[key] for key in ['Date1', 'Description1', 'Debit1', 'Credit1', 'TransNo1', 'RefNo1'] if col_mappings[key] is not None]
    df1 = df1[df1_cols]

    df2_cols = [col_mappings[key] for key in ['Date2', 'Description2', 'Debit2', 'Credit2'] if col_mappings[key] is not None]
    df2 = df2[df2_cols]

    # Rename columns for consistency
    df1.columns = ['Date', 'Description', 'Debit', 'Credit', 'TransNo', 'RefNo'][:len(df1_cols)]
    df2.columns = ['Date', 'Description', 'Debit', 'Credit'][:len(df2_cols)]

    # Combine Debit and Credit columns
    df1["Amount"] = df1["Debit"].fillna(0) - df1["Credit"].fillna(0)
    df2["Amount"] = df2["Debit"].fillna(0) - df2["Credit"].fillna(0)

    # Drop the original Debit and Credit columns
    df1 = df1.drop(columns=["Debit", "Credit"])
    df2 = df2.drop(columns=["Debit", "Credit"])

    # Merge dataframes on Amount and Date (with a tolerance of 10 days)
    merged = pd.merge_asof(df1.sort_values('Amount'), df2.sort_values('Amount'), 
                           on='Amount', by='Date', direction='nearest', 
                           tolerance=pd.Timedelta('10D'), suffixes=('', '_y'))

    # Filter out matched transactions
    unmatched = merged[merged['Description_y'].isna()].drop(columns=['Description_y', 'Date_y'])

    return unmatched

def upload_form():
    st.title("Reconciliation Tool")

    file1 = st.file_uploader("Upload the first file", type=['xlsx', 'xls', 'csv'])
    file2 = st.file_uploader("Upload the second file (e.g. Bank Statement)", type=['xlsx', 'xls', 'csv'])

    if file1 and file2:
        if file1.name.endswith('.csv'):
            df1 = pd.read_csv(file1)
        else:
            df1 = pd.read_excel(file1)

        if file2.name.endswith('.csv'):
            df2 = pd.read_csv(file2)
        else:
            df2 = pd.read_excel(file2)

        col_mappings = {
            'Date1': st.selectbox('Select the Date column from first file', [None] + list(df1.columns), index=1),
            'Description1': st.selectbox('Select the Description column from first file', [None] + list(df1.columns), index=2),
            'Debit1': st.selectbox('Select the Debit column from first file', [None] + list(df1.columns)),
            'Credit1': st.selectbox('Select the Credit column from first file', [None] + list(df1.columns)),
            'TransNo1': st.selectbox('Select the Trans. No. column from first file (optional)', [None] + list(df1.columns)),
            'RefNo1': st.selectbox('Select the Ref. No. column from first file (optional)', [None] + list(df1.columns)),
            'Date2': st.selectbox('Select the Date column from bank statement', [None] + list(df2.columns), index=1),
            'Description2': st.selectbox('Select the Description column from bank statement', [None] + list(df2.columns), index=2),
            'Debit2': st.selectbox('Select the Debit column from bank statement', [None] + list(df2.columns)),
            'Credit2': st.selectbox('Select the Credit column from bank statement', [None] + list(df2.columns))
        }

        df_unmatched = calculate_unmatched(df1, df2, col_mappings)

        st.write(df_unmatched)
        st.markdown(get_table_download_link_excel(df_unmatched), unsafe_allow_html=True)

def get_table_download_link_excel(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    import base64
    from io import BytesIO

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Unmatched Transactions', index=False)
    output.seek(0)
    b64 = base64.b64encode(output.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="unmatched_transactions.xlsx">Download Unmatched Transactions as Excel</a>'
    return href

def main():
    upload_form()

if __name__ == '__main__':
    main()
