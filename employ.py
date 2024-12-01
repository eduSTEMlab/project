import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

menu = ['Register Staff','Staff Database','Staff File']

choice = st.sidebar.selectbox('Menu',menu)
st.sidebar.write(':orange[**Made By eduSTEMlab**] 😎')

df = pd.read_csv('employee.csv')
user_id = 'USER' + str(len(df) + 1)

if choice == 'Staff Database':
    st.dataframe(df,use_container_width=True)



if choice == 'Register Staff':
 st.subheader("Register Here")
 fn,ln = st.columns(2)
 with fn:
     name = st.text_input("First Name: ")
 with ln:
     name2 = st.text_input("Last Name: ")
 mail,gender = st.columns(2)
 with mail:
     mail = st.text_input("Email Adress: ")
 with gender:
     gender = st.selectbox(
         'Gender',
         ('Male', 'Female', 'Other'))
     
 department = st.selectbox(
    'Department',
    ('Management', 'Accounting', 'Engineering', 'Human Resources', 'Security', 'Medical', 'Transportation')) 

 jobttle = st.selectbox(
    'Job Title',
    ('Board Of Directors', 'Supervisor', 'Senior Staff', 'Junior Staff', 'Paid Intern', 'Unpaid Intern'))
 
 tmspent,salary = st.columns(2)
 with tmspent:
     timespent = st.selectbox(
         'Contract Status',
         ('Full Time', 'Part Time'))
 with salary:
     salary = st.number_input("Monthly Income: ",0,value=10000,step=100)

 edulevel = st.selectbox(
     'Educational Degree',
     ('None', 'Associate Degree', 'Bachelor Degree', 'Graduate Degree', 'Professional Degree', 'Doctoral Degree'))
 
 date = st.date_input("Employememt Date")
 
 df= pd.read_csv('employee.csv')

 if st.button("Submit Employee Data"):
     if (user_id and name and name2 and date and salary and gender and mail and department and jobttle and edulevel and timespent):

             employees_df = pd.DataFrame({'User ID':[user_id],'First Name':[name],'Last Name':[name2],'Date of Employment':[date],'Salary':[salary],'Gender':[gender],'Mail Address':[mail],'Department':[department],
                    'Seniority Level':[jobttle],'Education Level':[edulevel],'Contract Status':[timespent]})
             new_df = pd.concat([df,employees_df],ignore_index=True)
             new_df.to_csv('employee.csv',index=False)
             st.success('Employee Data Saved')
     else :
         st.error('Kindly Fill All The Boxes')

if choice == 'Staff File':
   if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False
    
   st.write(st.session_state)
   space1,space2,finder = st.columns([2,1,1.7])
   with finder:
        st.subheader("Find Employee Details")
        st.write("")
        find1, find2 = st.columns([2,1])
        with find1:
            find = st.text_input("Enter Employee ID ") #Jeida == jeida == JEIDA
            findbutton = st.button("Find Employee")
        

   if findbutton:
        st.session_state.button_clicked = True
   if st.session_state.button_clicked == True:
            if find:
                try:
                    find_result = df[df['User ID'].str.lower() == find.lower() ] 


                    getfn = find_result['First Name'].iloc[0]
                    getln = find_result['Last Name'].iloc[0]
                    getmail = find_result['Mail Address'].iloc[0]
                    getgender = find_result['Gender'].iloc[0]
                    getdep = find_result['Department'].iloc[0]
                    getuser = find_result['User ID'].iloc[0]
                    getemploydate = find_result['Date of Employment'].iloc[0]
                    getsl = find_result['Seniority Level'].iloc[0]
                    getcs = find_result['Contract Status'].iloc[0]
                    getsal = find_result['Salary'].iloc[0]
                    getedulevel = find_result['Education Level'].iloc[0]
            
                
                    st.write("")
                    st.write("")
                    sp1,sp2,sp3 = st.columns([0.5,2,0.5])
                
                    with sp2:
                        space = " "
                        
                        
                        fullname = getfn + space + getln
                        st.subheader(f':orange[{fullname}]')
                        st.write('')
                        st.write('')
                        st.subheader("**Personal Information**")
                        st.divider()
                        mmail,ggender,other = st.columns(3)
                        with mmail:
                            st.write("**Email**")
                            st.write(getmail)
                        with ggender:
                            st.write("**Gender**")
                            st.write(getgender)
                        with other:
                            st.write("**Education Level**")
                            st.write(getedulevel)

                        st.divider()
                        st.subheader("**Job Information**")
                        st.divider()
                        one,two,thre = st.columns(3)
                        with one:
                            st.write("**Department**")
                            st.write(getdep)
                        with two:
                            st.write("**Employee ID**")
                            st.write(getuser)
                        with thre:
                            st.write("**Date Of Employement**")
                            st.write(getemploydate)
                        
                        st.divider()
                        fou,fiv,six = st.columns(3)
                        with fou:
                            st.write("**Seniority Level**")
                            st.write(getsl)
                        with fiv:
                            st.write("**Contract Status**")
                            st.write(getcs)
                        with six:
                            st.write("**Salary**")
                            st.write(f'#{getsal:,}')

                            st.write('')

                        with fou:
                            if st.button('Delete User'):
                                pass

                except IndexError:
                    with find1:
                        st.error("Incorrect User ID")

            else:
                with find1:
                    st.error("Please Enter a User ID")

                



                    # def delete():
                    #     df = pd.read_csv('employee.csv')
                    #     df = df.drop(df[df['User ID'].str.lower() == find.lower()].index)
                    #     df.to_csv('employee.csv', index=False)


                        # if st.button('Delete User',on_click=delete):
                        #   st.success("User deleted successfully.")
