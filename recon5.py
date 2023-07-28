import streamlit as st
import pandas as pd

def calculate_unmatched(df1, df2, col_mappings):
    # Adjust columns based on user input
    df1 = df1[[col_mappings['Date1'], col_mappings['Description1'], col_mappings['Debit1'], col_mappings['Credit1'], col_mappings['TransNo1'], col_mappings['RefNo1']]]
    df2 = df2[[col_mappings['Date2'], col_mappings['Description2'], col_mappings['Debit2'], col_mappings['Credit2']]]

    # Rename columns for consistency
    df1.columns = ['Date', 'Description', 'Debit', 'Credit', 'Trans. No.', 'Ref. No.']
    df2.columns = ['Date', 'Description', 'Debit', 'Credit']

    # Merge dataframes and identify unmatched rows
    df_all = pd.concat([df1.assign(Source='File 1'), df2.assign(Source='File 2')])

    # Sort by date for better presentation
    df_all = df_all.sort_values(by='Date')

    return df_all

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
            'Date1': st.selectbox('Select the Date column from first file', df1.columns, index=0),
            'Description1': st.selectbox('Select the Description column from first file', df1.columns, index=1),
            'Debit1': st.selectbox('Select the Debit column from first file', df1.columns),
            'Credit1': st.selectbox('Select the Credit column from first file', df1.columns),
            'TransNo1': st.selectbox('Select the Trans. No. column from first file', df1.columns),
            'RefNo1': st.selectbox('Select the Ref. No. column from first file', df1.columns),
            'Date2': st.selectbox('Select the Date column from bank statement', df2.columns, index=0),
            'Description2': st.selectbox('Select the Description column from bank statement', df2.columns, index=1),
            'Debit2': st.selectbox('Select the Debit column from bank statement', df2.columns),
            'Credit2': st.selectbox('Select the Credit column from bank statement', df2.columns)
        }

        df_unmatched = calculate_unmatched(df1, df2, col_mappings)

        st.write(df_unmatched)
        st.markdown(get_table_download_link(df_unmatched), unsafe_allow_html=True)

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    import base64
    import csv
    from io import StringIO

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_NONNUMERIC)
    b64 = base64.b64encode(csv_buffer.getvalue().encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="unmatched_transactions.csv">Download Unmatched Transactions as CSV</a>'
    return href

def main():
    upload_form()

if __name__ == '__main__':
    main()
