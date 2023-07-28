import streamlit as st
import pandas as pd

def calculate_unmatched(df1, df2):
    merged_df = pd.merge(df1, df2, on=['Date', 'Details', 'Amount'], how='outer', indicator=True)
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
            df1_col = st.selectbox(f'Select column in df1 to match with {column}', df1.columns)
            df2_col = st.selectbox(f'Select column in df2 to match with {column}', df2.columns)
            
            df1 = df1.rename(columns={df1_col: column})
            df2 = df2.rename(columns={df2_col: column})
        
        for column in supplementary_columns:
            df1_col = st.selectbox(f'Select column in df1 to match with {column} (Optional)', df1.columns)
            
            df1 = df1.rename(columns={df1_col: column})
            
        if st.button('Proceed with these column matches'):
            df1['Amount'] = df1['Debit'] - df1['Credit']
            df2['Amount'] = df2['Debit'] - df2['Credit']
            
            df1 = df1[['Date', 'Description', 'Amount']]
            df2 = df2[['Date', 'Description', 'Amount']]
            
            df_unmatched = calculate_unmatched(df1, df2)
            st.write(df_unmatched)

def main():
    upload_form()

if __name__ == "__main__":
    main()
