import streamlit as st
import pandas as pd

def calculate_unmatched(df1, df2, columns_mapping):
    # Use the user-provided mapping to rename columns in the dataframes
    df1 = df1.rename(columns=columns_mapping['file1'])
    df2 = df2.rename(columns=columns_mapping['file2'])
    
    # Merge the two dataframes based on Date and Description
    merged = pd.merge(df1, df2, on=['Date', 'Description'], how='outer', indicator=True)
    return merged[merged['_merge'] != 'both']

def upload_form():
    st.title("File Upload for Reconciliation")
    
    # Upload the Excel files
    file1 = st.file_uploader("Choose a file (e.g. Your main file)", type=['xlsx', 'xls'])
    file2 = st.file_uploader("Choose a second file (e.g. Bank statement)", type=['xlsx', 'xls'])
    
    if file1 and file2:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        
        # Allow user to map columns from their files to standard columns
        st.subheader("Please map the columns from your files to the standard columns:")
        
        columns_mapping = {
            'file1': {},
            'file2': {}
        }
        
        default_columns = ['Date', 'Description', 'Debit', 'Credit', 'Trans. No.', 'Ref. No.']
        for col in default_columns:
            col1_choice = st.selectbox(f"Column in File 1 that corresponds to '{col}'", [''] + list(df1.columns), key=col + "_file1")
            col2_choice = st.selectbox(f"Column in File 2 that corresponds to '{col}'", [''] + list(df2.columns), key=col + "_file2")
            
            if col1_choice:
                columns_mapping['file1'][col1_choice] = col
            if col2_choice:
                columns_mapping['file2'][col2_choice] = col
        
        # Calculate unmatched transactions
        df_unmatched = calculate_unmatched(df1, df2, columns_mapping)
        st.write(df_unmatched)

def main():
    upload_form()

if __name__ == "__main__":
    main()
