# TECHIE SMART TEST 
# create an app to:
# upload any csv file 
# use a multiselectbox to get and display subjects users want to choose to plot (use st.multiselect)
# use a button to choose if to view the chart as a barchart or piechart
#use a button to choose what to do (ave, sum, count)

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')
st.title('Subjects Chart App')


col1,col2 = st.columns(2)

with col1:
    upload_csv= st.file_uploader("Upload CSV File",type=['csv'])

    st.write("")

if upload_csv:
    csv_file = pd.read_csv(upload_csv)
    

    # table1,table2 = st.columns(2)
    # with table1:
    with st.expander('Open Database Table'):
            # with col1:
                st.table(csv_file)


    col3,col4 = st.columns(2)
    with col3:
        subjects = csv_file.columns.tolist()
        subjects = st.multiselect('Choose Subjects to plot',subjects)

    if subjects:
            subjects_ave = csv_file[subjects].mean().reset_index()
            
            subjects_rename = subjects_ave.rename(columns={'index': 'Subject', 0: 'Average'})
            
            with  col4:
                chart = st.radio('Select chart to plot',['Bar Chart','Pie Chart'],horizontal=True)
                piechart = px.pie(subjects_rename, names='Subject', values='Average')
                barchart = px.bar(subjects_rename, x = 'Subject', y= 'Average')

            if chart == 'Bar Chart':
                st.plotly_chart(barchart)
            
            elif chart == 'Pie Chart':
                 st.plotly_chart(piechart)
