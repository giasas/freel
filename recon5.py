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
        
        st.write("Select columns from df1 to match with df2")
        
        df1_date_col = st.selectbox('Select Date column for df1', df1.columns)
        df2_date_col = st.selectbox('Select Date column for df2', df2.columns)
        
        df1_details_col = st.selectbox('Select Details column for df1', df1.columns)
        df2_details_col = st.selectbox('Select Details column for df2', df2.columns)
        
        df1_amount_col = st.selectbox('Select Amount column for df1', df1.columns)
        df2_amount_col = st.selectbox('Select Amount column for df2', df2.columns)
        
        if st.button('Proceed with these column matches'):
            df1 = df1.rename(columns={df1_date_col: 'Date', df1_details_col: 'Details', df1_amount_col: 'Amount'})
            df2 = df2.rename(columns={df2_date_col: 'Date', df2_details_col: 'Details', df2_amount_col: 'Amount'})
        
            df_unmatched = calculate_unmatched(df1, df2)
            st.write(df_unmatched)

def main():
    upload_form()

if __name__ == "__main__":
    main()
