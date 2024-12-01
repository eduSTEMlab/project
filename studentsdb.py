import streamlit as st #this is the webpage for our python projects
import pandas as pd #this helps to read, write CSV files, and convert them to a table 
import plotly.express as px #helps us to plot charts

# _________REMINDER TO ADD______________________________________

# create school fees invoice and to be able to send to mail
# --------------------------------



# submit students information (student name, scores) DONE
# The computer will calc the (total, average, grade of student) DONE
# save each submitted info into a CSV file (appear and fade singular table) DONE
# create a database with chart and with filter DONE
# teacher can edit the database DONE
# download the database csv file DONE
#how to make sure scores edited will be recalculated DONE
#sort database scores by grade DONE
#edit database page should have clear data button for all db or just one student
# search students file
# computer send a mail


#CSV file is a text file that has all it's data separated by a comma (COMMA SEPARETED VALUES)

csvlink = 'scores.csv'
readcsv = pd.read_csv(csvlink,dtype={'Average': str})


student_id = 'Student_' + str(len(readcsv) +1)

menu = st.sidebar.selectbox('Menu',['Submit Scores',  'Students Database','Scores Charts', 'Search Student'])
subjects = ['Maths','English','Science','Art','Geography','History'] #subjects for new table to plot

if menu == 'Submit Scores':
    st.header('Submit Students Scores Here')




    #----------------TAKING INPUTS--------------------------------------
    name = st.text_input("Enter the student's name")




    subject1, subject2 = st.columns(2)




    with subject1:
        maths = st.number_input("Enter student's score for Maths",0,100,step=10,value=50)
        science = st.number_input("Enter student's score for Science",0,100,step=10,value=50)
        art = st.number_input("Enter student's score for Art",0,100,step=10,value=50)




    with subject2:
        english = st.number_input("Enter student's score for English",0,100,step=10,value=50)
        history = st.number_input("Enter student's score for History",0,100,step=10,value=50)
        geography = st.number_input("Enter student's score for Geography",0,100,step=10,value=50)



# --------------------------CALCULATING SCORE TOTAL,AVE,GRADE-----------------------------
    totalscore = maths + science + art + english + history + geography




    average = totalscore /6
    average = round(average,2)



    #st.success, error, warning, info
    if average >= 90:
        grade = ("A+")
    elif average >= 85:
        grade = ("A")
    elif average >= 80:
        grade = ("A-")
    elif average >= 75:
        grade = ("B+")
    elif average >= 70:
        grade = ("B")
    elif average >= 65:
        grade = ("C+")
    else:
        grade = ("FAIL")



# ------------------------------------BUTTON FOR DICT TO DATAFRAME-------------------
    savebutton = st.button("Save Students Scores")


    if savebutton:
        if grade != ("FAIL"):
            st.success(f"{name}'s total score is {totalscore} points, their average is: {average}%, and their grade is: {grade}.")
        else:
            st.error(f"{name}'s total score is {totalscore} points, their average is: {average}%, and their grade is: {grade}.")
        
    
        #Here we create the dictionary to store the key and the data, then we convert to a df using pandas
        studentsdict = {'Student_ID':[student_id],'Name':[name],'Maths': [maths],'English':[english],'Science':[science],'Art':[art],
                        'Geography':[geography],'History':[history],'Total Score':[totalscore],'Average':[average],'Grade':[grade]}
        # st.write(studentsdict)
        studentsdf = pd.DataFrame(studentsdict) #converts to dataframe
        # st.table(studentsdf)
        newtable = pd.concat([readcsv,studentsdf],ignore_index=True) #joins the 2 tables together. old + new
        newtable.to_csv(csvlink,index=False) #saves the newtable into the csv file
        #Next we join the existing df with the new df and save it on the csv file
        


#--------------------------------EDIT DATABASE VALUES--------------------------------------------------
if menu == "Students Database":
    editcheckbox=st.sidebar.checkbox('Edit Database')
    if editcheckbox:
        edit_table = st.data_editor(readcsv,width=1500,height=800)
        if st.sidebar.button("Save Database"):
            saved_edit = edit_table.to_csv(csvlink,index=False)
            save1, save2 = st.sidebar.columns(2)
            with save1:
                st.success('Edits Saved')
                #how to make sure scores edite d will be recalculateddd
    else:
            
        #--------------------RECALCULATE DATABASE VALUES


        readcsv['Total Score'] = readcsv[subjects].sum(axis=1)
        readcsv['Average'] = readcsv['Total Score']/6
        readcsv['Grade'] = pd.cut(readcsv['Average'], bins=[0,65,70,75,80,85,90,100], labels=['FAIL','C+','B','B+','A-','A','A+'])
        readcsv.to_csv(csvlink,index=False)


            # -----------------------------VIEW DATABASE----------------------

        try:
            sort1,sort2,sort3,sort4 = st.columns(4)
            with sort1:
                
                sortsubjects = ['None','Maths','English','Science','Art','Geography','History','Total Score','Grade']
                sort = st.selectbox('Sort DataFrame',sortsubjects,index=0)

                            # Sort the DataFrame based on the selected order
            if sort == 'Maths'or 'English'or'Science'or 'Art'or 'Geography'or 'History'or 'Total Score' or 'Grade':
                sorted_table = readcsv.sort_values(by=sort, ascending=False)
                st.table(sorted_table)
        except KeyError:
                st.table(readcsv) #streamlit displays the csv file

# -----------------------------DOWNLOAD CSV FILE------------------------------------------
    
    with open(csvlink, 'rb') as file: #open to make the file readable as each character
        data = file.read() #read the content
    st.sidebar.download_button(label = 'Download Database CSV', data=data,file_name='Students Scores Database.csv')

 
#--------------------------------PLOT SCORES BAR/PIE CHARTS--------------------------------------------------


if menu == 'Scores Charts':
    #what if teach wants to see gender based score chart?

    radio1, radio2 = st.columns(2)

    with radio1:
        selectchart = st.radio('Choose Preferred Chart to Plot', ['Bar Chart', 'Pie Chart'],horizontal=True)
    #now let's plot the bar chart
    
    subjectstable = readcsv[subjects].mean().reset_index() #displays only the 5 columns on the table
    renamedcolumns = subjectstable.rename(columns = {'index': 'Subject', 0: "Score"})
    # st.table(renamedcolumns)

    if selectchart == 'Bar Chart':
        barchart = px.bar(renamedcolumns, x = 'Subject', y = 'Score')
        st.plotly_chart(barchart)

    elif selectchart == 'Pie Chart':
        piechart = px.pie(renamedcolumns, names='Subject', values='Score')
        st.plotly_chart(piechart)


if menu == 'Search Student':
    space1,space2,finder = st.columns([2,1,1.7])
    with finder:
        st.subheader("Find Student's File")
        st.write("")
        find1, find2 = st.columns([2,1])
        with find1:
            findID = st.text_input("Enter Student's ID ")
            findbutton = st.button("Find Student")

# Maths,English,Science,Art,Geography,History,Total Score,Average,Grade
    if findbutton: #check if button pressed
        if findID: #check if text in the box
            try:
                searchresult = readcsv[readcsv['Student_ID'].str.lower() == findID.lower()]
                # st.table(searchresult)
                ID = searchresult['Student_ID'].iloc[0]
                name = searchresult['Name'].iloc[0]
                eng = searchresult['English'].iloc[0]
                maths = searchresult['Maths'].iloc[0]
                sci = searchresult['Science'].iloc[0]
                art = searchresult['Art'].iloc[0]
                geo = searchresult['Geography'].iloc[0]
                hist = searchresult['History'].iloc[0]
                total = searchresult['Total Score'].iloc[0]
                ave = searchresult['Average'].iloc[0]
                grade = searchresult['Grade'].iloc[0]


                head1,head2,head3 = st.columns([1,2,1])
                with head2:
                    st.title(':blue[GRANGE SCHOOL]')
                    sub1,sub2,sub3 = st.columns([0.5,2,0.5])
                    with sub2:
                        st.write(":orange[**FAUGET MODERN SCHOOL**]")
                st.divider()

                st.header(f':blue[{name}]')

                st.write("")
                st.write("")
                subject, score = st.columns([2,1])

                with subject:
                    st.subheader("Subject List")
                    st.write('Mathematics')
                    st.write('English')
                    st.write('Science')
                    st.write('Art')
                    st.write('Geography')
                    st.write('History')
                    st.write("Total Score")
                    
                with score:
                    st.subheader("Score")
                    st.write(f'{maths}')
                    st.write(f'{eng}')
                    st.write(f'{sci}')
                    st.write(f'{art}')
                    st.write(f'{geo}')
                    st.write(f'{hist}')
                    st.write(f'{total}')
                last1,last2,last3 = st.columns(3)
                with last2:
                    st.subheader(f':orange[GRADE:] {grade}')
            except:
                with find1:
                    st.error("ID not Found")

        
reader_name = "Emma"
books_read = 25
book_club_meetings = 8
hours_spent = 120.5

print(reader_name, "is an avid reader who loves tracking her reading progress.")
print("This year, she read", books_read, "books.")
print("She also attended", book_club_meetings, "book club meetings.")
print("Emma spent a total of", hours_spent, "hours reading.")