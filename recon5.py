import streamlit as st
import pandas as pd

def calculate_unmatched(df1, df2):
    df1 = df1[['Date', 'Details', 'Amount']]
    df2 = df2[['Date', 'Description', 'Amount']]
    merged = df1.merge(df2, how='outer', left_on=['Date', 'Amount'], right_on=['Date', 'Amount'], indicator=True)
    unmatched = merged[merged['_merge'] != 'both']
    return unmatched

def display_unmatched(unmatched_df):
    st.subheader('Unmatched Transactions')
    st.write(unmatched_df)

def match_transactions(df_unmatched):
    display_unmatched(df_unmatched)
    # Εδώ μπορείτε να προσθέσετε περαιτέρω λειτουργίες για το manual matching

def upload_form():
    st.title('Upload your Excel files')
    
    file1 = st.file_uploader("Upload the Bank Statement Excel file", type=['xlsx'])
    file2 = st.file_uploader("Upload the Accounting Statement Excel file", type=['xlsx'])
    
    if file1 and file2:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        df_unmatched = calculate_unmatched(df1, df2)
        match_transactions(df_unmatched)

def main():
    upload_form()

if __name__ == "__main__":
    main()
