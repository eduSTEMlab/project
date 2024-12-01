import streamlit as st
import pandas as pd
import random

@st.cache_data
def load_bible(data):
    df = pd.read_csv(data)
    return df

def code():
    st.title("Bible Project App")
    menu = st.sidebar.selectbox('Menu',['Bible Verse','About'])
    df = load_bible('KJV_Bible.csv')
    #st.dataframe(df)

    if menu =='Bible Verse':
        st.subheader("Bible Verse Search")

        book_list = df['book'].unique().tolist() #create a lit of unique values from book columns, removes diplicates
        book_name = st.sidebar.selectbox('Book',book_list)
        chapter = st.sidebar.number_input('Chapter',1)
        verse = st.sidebar.number_input('Verse',1)

        #we are now creating a new DataFrame called bible_df by filtering the original DataFrame df 
        # based on the selected book name (book_name). 
        bible_df = df[df['book'] == book_name] #we created a new df for the particular book selected
        #st.dataframe(bible_df) #this will only show df of selected bible name

        col1,col2 = st.columns([2,1])

        with col1:
            try: #some verses might not be there, this will help know what to do
                selected_passage = bible_df[(bible_df['chapter'] == chapter) & (bible_df['verse'] == verse)] 
                #here is the bible df to filter to match the bookname chapter and verse selected
                #st.write(selected_passage)
                passage_details = f'{book_name} Chapter::{chapter} Verse::{verse}'
                st.info(passage_details)
                passage = '{}'.format(selected_passage['text'].values[0])
                st.write(passage)
            except:
                st.warning("Book Out Of Range")
        
        with col2:
            st.info("Verse Of The Day") 
            randombook = random.choice(book_list )
            randomchapter = random.randint(1,21)
            randomverse = random.randint(1,21)
            
            #show the random book with random chapter and random verse
            st.write(f'Book:: {randombook} Chapter:: {randomchapter} Verse {randomverse}')

            # Filter the original DataFrame 'df' to create a DataFrame for the randomly selected book
            rand_bible_df = df[df['book'] == randombook]
            #st.write(rand_bible_df['chapter'])

            try:
                #the d
                randompassage = rand_bible_df[(rand_bible_df['chapter']==randomchapter) & (rand_bible_df['verse']==randomverse)]
                st.write(randompassage['text'].values[0])

            except:
                fixpassage = rand_bible_df[(rand_bible_df['chapter']==1) & (rand_bible_df['verse']==1)]
                st.write(fixpassage['text'].values[0])




code()