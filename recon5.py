import streamlit as st
import pandas as pd
import io

def calculate_unmatched(df1, df2, df1_cols, df2_cols):
    df1 = df1[df1_cols].copy()
    df2 = df2[df2_cols].copy()

    df1['Amount'] = df1['Debit'].combine_first(-df1['Credit'])
    df2['Amount'] = df2['Debit'].combine_first(-df2['Credit'])

    merged = pd.merge(df1, df2, on=['Date', 'Description', 'Amount'], how='outer', indicator=True)

    return merged[merged['_merge'] != 'both']

def upload_form():
    st.write("Upload your files")
    file1 = st.file_uploader("Upload File 1 (Your data)", type=['xlsx'])
    file2 = st.file_uploader("Upload File 2 (Bank data)", type=['xlsx'])

    if file1 and file2:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)

        st.write("Columns in File 1:")
        columns1 = st.multiselect("Select the columns for Date, Description, Debit, Credit (in order)", df1.columns)
        
        st.write("Columns in File 2:")
        columns2 = st.multiselect("Select the columns for Date, Description, Debit, Credit (in order)", df2.columns)

        if len(columns1) == 4 and len(columns2) == 4:
            df1_mapping = {'Date': columns1[0], 'Description': columns1[1], 'Debit': columns1[2], 'Credit': columns1[3]}
            df2_mapping = {'Date': columns2[0], 'Description': columns2[1], 'Debit': columns2[2], 'Credit': columns2[3]}

            df_unmatched = calculate_unmatched(df1, df2, list(df1_mapping.values()), list(df2_mapping.values()))

            st.write(df_unmatched)

            towrite = io.BytesIO()
            downloaded_file = df_unmatched.to_excel(towrite, index=False, header=True)  
            towrite.seek(0)  
            st.download_button(
                label="Download Data as Excel",
                data=towrite,
                file_name="unmatched_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

def main():
    upload_form()

if __name__ == "__main__":
    main()
