# allow user to upload and view an image
#allow user to upload audio
#allow user to upload video or take a picture

import streamlit as st

menu = st.sidebar.selectbox('Choose an option',['Upload Image','Upload Audio','Upload Video'])

if menu == 'Upload Image':
    selectoption = st.radio('Choose option',["Upload a Picture",'Take a Picture'],horizontal=True)
    
    if selectoption == "Upload a Picture":
        uploadimage = st.file_uploader("Upload your image here",type=['jgp','jpeg','png'])
        if uploadimage:
            st.image(uploadimage)
    
    elif selectoption ==  'Take a Picture':
        camera = st.camera_input("Smile to the camera")
        
elif menu == 'Upload Audio':
    uploadaudio = st.file_uploader("Upload your audio here", type=['mp3','wav'])
    if uploadaudio:
        st.audio(uploadaudio,format='audio/mp3')
        
        

elif menu == 'Upload Video':
    youtubelink = st.text_input("Paste in your Youtube link here")
    if st.button("Play YouTube video"):
        if youtubelink:
            st.video(youtubelink)
        else:
            st.info("Please paste your link first")