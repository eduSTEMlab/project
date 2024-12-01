import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')
menu = st.sidebar.selectbox('select option',['create note', 'view notes', 'update notes'])

notes = pd.read_csv('notes.csv')
if menu == 'create note':
    bd1,bd2,bd3 = st.columns([0.2,4,0.2])

    with bd2:
        with st.form('create notes form',clear_on_submit=True):
            st.header(':green[**create note**]')
            st.divider()
            
            nt1,nt2 = st.columns(2)
        
            with nt1:
                notitle = st.text_input('enter the title for your new note: ')
            with nt2:
                notedate = st.date_input('select the note date: ')

            notecontent = st.text_area('enter your new notes: ',height=220)
            
            sv1,sv2 = st.columns(2)
            
            with sv1:
             if st.form_submit_button('save note'):
                 if notitle and notecontent:
                     notedict = {'title':[notitle],'dates':[notedate],'note content':[notecontent]}
                     note_df = pd.DataFrame(notedict)
                     notejoin = pd.concat([notes,note_df],ignore_index=True)
                     notejoin.to_csv('notes.csv',index=False)
                     
                     st.success('succesfully saved!')
            
elif menu == 'view notes':
    st.header(':green[**view notes**]')
    st.divider()

    note_title = notes['title'].to_list()
    nt1,nt2 = st.columns([0.4,0.2])

    with nt1:
     select_title = st.selectbox('select note to view',note_title)
    
    filter_title = notes[notes['title'] == select_title]
    # st.table(filter_title)
    content = filter_title['note content'].iloc[0]
    space = ''

    st.divider()


    st.write(space)
    nc1,nc2 = st.columns([0.3,0.3])

    with nc1:
       st.subheader(f':green[**selected note content:**]')
    with nc2:
       date = filter_title['dates'].iloc[0]
       st.subheader(f':green[**note date: {date}**]')
       
    st.divider()
    st.write(space)
    st.write(content)

elif menu == 'update notes':
   st.header(':green[**update notes**]')
   st.divider()

   note_title = notes['title'].to_list()
   nt1,nt2 = st.columns([0.4,0.2])

   with nt1:
     select_title = st.selectbox('select note to update',note_title)
   
   st.write('')
   st.divider()

   filter_title = notes[notes['title'] == select_title]
   content = filter_title['note content'].iloc[0]

   upd1,upd2 = st.columns([0.5,0.2])

   with upd1:
     update_note = st.text_area('edit note',content,350)

   if st.button('save edits'):
      notes.loc[notes['title'] == select_title, 'note content'] = update_note
      notes.to_csv('notes.csv',index=False)
      
      ed1,ed2 = st.columns([0.3,0.3])
      with ed1:
         st.success('successfuly edited!')



