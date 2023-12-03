# pip install openpyxl
import pandas as pd
import streamlit as st
import zipfile
import base64
import os
import datetime as dt
import plotly.express as px  # pip install plotly-express
from dateutil.relativedelta import relativedelta # to add days or years
from datetime import datetime, date ,time
from PIL import Image

def app ():
# Web App Title
#    st.title('Online Business Registration Data Anslysis')

#add a sidebar
    #st.sidebar.header('User Input Features')
    #selected_year = st.sidebar.selectbox('Year',list(reversed(range(1950,2051))))

    def excel_file_merge(zip_file_name):
        df = pd.DataFrame()
        archive = zipfile.ZipFile(zip_file_name,'r')
        with zipfile.ZipFile(zip_file_name,"r") as f:
            for file in f.namelist():
                xlfile = archive.open(file)
                if file.endswith('.xlsx'):
                    df_xl = pd.read_excel(xlfile,engine='openpyxl')
                    df = df.append(df_xl,ignore_index=True)
        return df

# with CSV data
    with st.sidebar.subheader('Upload ZIP file'):
        uploaded_file = st.sidebar.file_uploader("Excel-containing ZIP file", type=["zip"])
        st.sidebar.markdown("""
        [Example  ZIP input file""")

    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="merged_file.csv">Download Merged File as CSV</a>'
              # sidebar
        return href

    st.sidebar.subheader('Upload Excel File')
    uploaded_file = st.sidebar.file_uploader("Choose a XLSX file", type="xlsx")
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)
        st.table(df)
        st.dataframe(df.style.highlight_max(axis=0))

        sorted_licened = sorted(df.လိုင်စင်အမျိုးအစား.unique())
        selected_licened = st.sidebar.multiselect('လိုင်စင်အမျိုးအစား',sorted_licened,sorted_licened)

        sorted_sub_licened = sorted(df.စီးပွားရေးလုပ်ငန်းအမျိုးအစား.unique())
        selected_sub_licened = st.sidebar.multiselect('စီးပွားရေးလုပ်ငန်းအမျိုးအစား',sorted_sub_licened,sorted_sub_licened)

        # Filtering DataFrame
        df_selected_licence = df[(df.လိုင်စင်အမျိုးအစား.isin(selected_licened)) & (df.စီးပွားရေးလုပ်ငန်းအမျိုးအစား.isin(selected_sub_licened))]

        st.header('Display Selected Licence')
        st.write('Data Dimension: ' + str(df_selected_licence.shape[0]) + ' rows and ' + str(df_selected_licence.shape[1]) + ' columns.')
        st.dataframe(df_selected_licence)

        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="ရွေးထားသည့်လိုင်စင်စာရင်းများ.csv">Download CSV File</a>'
            return href
        st.markdown(filedownload(df_selected_licence),unsafe_allow_html=True)


        chart_data = pd.DataFrame(columns=['လိုင်စင်နံပါတ်','လိုင်စင်အမျိုးအစား'])

        st.bar_chart(chart_data)
# bar chart
        df_grouped = (df.groupby(by=["လိုင်စင်အမျိုးအစား"]).count()[["လိုင်စင်နံပါတ်"]].sort_values(by="လိုင်စင်နံပါတ်"))

        bar_chart = px.bar(
            df_grouped,
            x='လိုင်စင်နံပါတ်',
            y='လိုင်စင်နံပါတ်',
            text='လိုင်စင်နံပါတ်',
            title="<b>လိုင်စင်အရေအတွက်</b>",
            color_discrete_sequence=["#0083B8"] * len(df_grouped),
            template="plotly_white")
        st.plotly_chart(bar_chart)
# pie chart

        pie_chart = px.pie(df_selected_licence,title='Total No.of Licence',values='လိုင်စင်နံပါတ်',names='စီးပွားရေးလုပ်ငန်းအမျိုးအစား')
        st.plotly_chart(pie_chart)

        # ---- HIDE STREAMLIT STYLE ----
        hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
        st.markdown(hide_st_style, unsafe_allow_html=True)

        df1 = df['လိုင်စင်နံပါတ်'].value_counts().rename_axis('unique_values').reset_index(name='counts')
        st.header('Filtered Licence Number')
        st.dataframe(df1)
