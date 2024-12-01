import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Résumé Generator",layout='wide')



st.subheader("Updated AI Résumé Preview")
api_key = "AIzaSyC5v3v3Dof5PTWAMo473IiPvHNOt3pkn3E"

def config_ai():
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

# start up Gemini AI
model = config_ai()

# cv_template

def ai_cv(name,email,phone,cv_text, education, keyskills):
    prompt = f"""
    Extract the information below to rewrite to create a good composed, comprehensive Résumé starting with my Professional Summary,
    and a comprehensive Key skills with complete sentences each of what i can do, and my comprehensive Career experience

    Name:
    {name}
    
    Email:
    {email}
    
    Phone:
    {phone}
    
    Key skills here for professional summary:
    {keyskills}
    
    Career experience:
    {cv_text}

    Educationa:
    {education}




    Please provide the updated Résumé content.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error updating Résumé: {str(e)}")
        return None


st.sidebar.title("AI Résumé Generator")
st.sidebar.write("Paste your details to generate a good résumé.")


name = st.sidebar.text_input("Please enter your full name",placeholder='James Wade')

if st.sidebar.checkbox('Add Email'):
    email = st.sidebar.text_input("Please enter your email (Optional)",placeholder='james@gmail.com')
else:
    email = ''

if st.sidebar.checkbox('Add Phone number'):
    phone = st.sidebar.text_input("Please enter your phone number (Optional)",placeholder='+2349169096941')
else:
    phone = ''
        
keyskills = st.sidebar.text_area("Key skills for your Résumé (New lines)",
placeholder="""Tv analyst

Experienced quality control expert
etc""")

cv_text = st.sidebar.text_area("Type details about your career experience here", height=300,
placeholder="""I have worked with Samsung tv department as an analyst, 2012-2022

I also worked with Apple screen department as a quality control expert, 2022-2024
etc""")

education = st.sidebar.text_area("Type details on your education & year here",
placeholder="""Project management, Harvard, 2000-2004
Screen expert, China University, 2004-2006
etc""")




if st.sidebar.button("Generate Résumé"):
    if cv_text and education and keyskills:
        with st.spinner("Processing... This may take a few moments."):
            updated_cv = ai_cv(name,email,phone,cv_text, education, keyskills) 
            

        if updated_cv:
            st.sidebar.success("Résumé and Cover Letter generated successfully!")

            st.write(updated_cv)
            st.download_button(
                label="Download Updated Résumé",
                data=updated_cv,
                file_name="updated_Résumé.txt",
                mime="text/plain"
            )

    else:
        st.sidebar.info("Please provide your Résumé content started.")
