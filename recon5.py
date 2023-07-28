import streamlit as st
import pandas as pd

def calculate_unmatched(df1, df2):
    merged_df = pd.merge(df1, df2, on=['Date', 'Description', 'Amount'], how='outer', indicator=True)
    unmatched = merged_df[merged_df['_merge'] != 'both']
    return unmatched

def upload_form():
    file1 = st.file_uploader("Choose a XLSX file for df1", type="xlsx")
    file2 = st.file_uploader("Choose a XLSX file for df2", type="xlsx")
    
    if file1 and file2:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        
        st.write("Select columns from your files to match with the predefined columns")
        
        primary_columns = ["Date", "Description", "Debit", "Credit"]
        supplementary_columns = ["Trans. No.", "Ref. No."]
        
        for column in primary_columns:
            df1_col = st.selectbox(f'Select column in df1 to match with {column}', [''] + list(df1.columns))
            df2_col = st.selectbox(f'Select column in df2 to match with {column}', [''] + list(df2.columns))
            
            if df1_col:
                df1 = df1.rename(columns={df1_col: column})
            if df2_col:
                df2 = df2.rename(columns={df2_col: column})
        
        for column in supplementary_columns:
            df1_col = st.selectbox(f'Select column in df1 to match with {column} (Optional)', [''] + list(df1.columns))
            
            if df1_col:
                df1 = df1.rename(columns={df1_col: column})
            
        if st.button('Proceed with these column matches'):
            if all(elem in df1.columns and elem in df2.columns for elem in primary_columns):
                df1['Amount'] = df1['Debit'] - df1['Credit']
                df2['Amount'] = df2['Debit'] - df2['Credit']
                
                df1 = df1[['Date', 'Description', 'Amount']]
                df2 = df2[['Date', 'Description', 'Amount']]
                
                df_unmatched = calculate_unmatched(df1, df2)
                st.write(df_unmatched)
            else:
                st.error('Please make sure all primary columns are matched.')

def main():
    upload_form()

if __name__ == "__main__":
    main()
