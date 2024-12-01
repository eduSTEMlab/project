import streamlit as st
import pandas as pd
import time

st.set_page_config(layout='wide')
st.title('Data Editor App')

timestamp = int(time.time())

col1,col2 = st.columns(2)

with col1:
    upload_csv= st.file_uploader("Upload CSV File",type=['csv'])



if upload_csv:
    st.divider()
    st.write("")
    csv_file = pd.read_csv(upload_csv)
    edit_csv = st.data_editor(csv_file,use_container_width=True)

    save1, save2,space = st.columns([1,1,4])
    message1,message2 = st.columns([1.5,3.5])

    with save1:
        if st.button('Save on Original File'):    
            saved_csv = edit_csv.to_csv(upload_csv.name,index=False)
            with message1:
                st.success("Edited CSV File Saved")

    #what if you want to edit and save a copy, not overwrite the original data??

    with save2:
        if st.button("Save A Copy"):
            new_filename = f'{upload_csv.name}_{timestamp}.csv'
            st.write(new_filename)
            csv_copy = edit_csv.to_csv(new_filename,index=False)
            with message1:
                st.success('CSV Copy Saved')



#homework: create a program that reads the 