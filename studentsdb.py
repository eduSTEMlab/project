import streamlit as st
import time

# create an app for your friends on how much they know you or know something or general quiz
# asks the user to enter his/her name on the questionnaire page
# the questionnaire page can be arranged in 3 or more columns (use your own ideas(-radio - selecbox))
# a button under after all to submit and this checks the right questions and add the scores and save the user score under the user name


if "current_page" not in st.session_state:
    st.session_state.current_page = "start"
    st.rerun()


if "score" not in st.session_state:
    st.session_state.score = 0

# st.write(st.session_state)

def countdown():
    x = 0
    with st.spinner('Loading Next Page', show_time = True):
        time.sleep(1)

def start():
    st.title("Sam's Quizzes")
    name = st.text_input("First, your name?")
    if st.pills('a',['Start Quiz'],label_visibility='collapsed'):
        if name:
            countdown()
            st.session_state.current_page = "q1"
            st.rerun()
        else:
            ('Name First Please..')
            

                
def q1():
    st.info("Started Quiz!")
    st.subheader("Question 1")
    st.divider()
    q1 = st.radio("What function outputs to the user's screen?", ["Options:", "output()", "write()", "print()", "text()"])
    if q1 != "Options:":
        if st.button("Next Question"):
            if q1 == "print()":
                st.success("Correct answer!")
                st.session_state.score += 1
                countdown()
                st.session_state.current_page = "q2"
                st.rerun()
            else:
                st.error("Wrong answer!")
                countdown()
                st.session_state.current_page = "q2"
                st.rerun()

def q2():
    st.subheader("Question 2")
    st.divider()
    q2 = st.radio("How do you add a module to your code?", ["Options:", "module()", "package.add", "use()", "import"])
    if q2 != "Options:":
        if st.button("Next Question"):
            if q2 == "import":
                st.success("Correct answer!")
                st.session_state.score += 1
                countdown()
                st.session_state.current_page = "q3"
                st.rerun()
            else:
                st.error("Wrong answer!")
                countdown()
                st.session_state.current_page = "q3"
                st.rerun()


def q3():
    st.subheader("Question 3")
    st.divider()
    q3 = st.radio("What is used to add a block comment in python?", ["Options:", "<!-- -->", "//", "'''", "+++"])
    if q3 != "Options:":
        if st.button("Next Question"):
            if q3 == "'''":
                st.success("Correct answer!")
                st.session_state.score += 1
                countdown()
                st.session_state.current_page = "q4"
                st.rerun()
            else:
                st.error("Wrong answer!")
                countdown()
                st.session_state.current_page = "q4"
                st.rerun()


def q4():
    st.subheader("Question 4")
    st.divider()
    q4 = st.radio("What is the extension for a python file?", ["Options:", ".pth", ".py", ".pyt", ".python"])
    if q4 != "Options:":
        if st.button("Next Question"):
            if q4 == ".py":
                st.success("Correct answer!")
                st.session_state.score += 1
                countdown()
                st.session_state.current_page = "q5"
                st.rerun()
            else:
                st.error("Wrong answer!")
                countdown()
                st.session_state.current_page = "q5"
                st.rerun()


def q5():
    st.subheader("Question 5")
    st.divider()
    q5 = st.radio("How do you ask the user for a piece of information?", ["Options:", "input()", "ask()", "question()", "answer()"])
    if q5 != "Options:":
        if st.button("Next Question"):
            if q5 == "input()":
                st.success("Correct answer!")
                st.session_state.score += 1
                countdown()
                st.session_state.current_page = "q6"
                st.rerun()
            else:
                st.error("Wrong answer!")
                countdown()
                st.session_state.current_page = "q6"
                st.rerun()


def q6():
    st.subheader("Question 6")
    st.divider()
    q6 = st.radio("What stores information?", ["Options:", "box", "log", "store", "variable"])
    if q6 != "Options:":
        if st.button("Next Question"):
            if q6 == "variable":
                st.success("Correct answer!")
                st.session_state.score += 1
                countdown()
                st.session_state.current_page = "q7"
                st.rerun()
            else:
                st.error("Wrong answer!")
                countdown()
                st.session_state.current_page = "q7"
                st.rerun()


def q7():
    st.subheader("Question 7")
    st.divider()
    q7 = st.radio("Who created python?", ["Options:", "Isaac Watts", "David Bazsucki", "Guido van Rossum", "Mike Wazowski"])
    if q7 != "Options:":
        if st.button("Next Question"):
            if q7 == "Guido van Rossum":
                st.success("Correct answer!")
                st.session_state.score += 1
                countdown()
                st.session_state.current_page = "q8"
                st.rerun()
            else:
                st.error("Wrong answer!")
                countdown()
                st.session_state.current_page = "q8"
                st.rerun()


def q8():
    st.subheader("Question 8")
    st.divider()
    q8 = st.radio("What is '//' in python?", ["Options:", "Double Division", "Modulus", "Floor division", "Division"])
    if q8 != "Options:":
        if st.button("Next Question"):
            if q8 == "Floor division":
                st.success("Correct answer!")
                st.session_state.score += 1
                countdown()
                st.session_state.current_page = "q9"
                st.rerun()
            else:
                st.error("Wrong answer!")
                countdown()
                st.session_state.current_page = "q9"
                st.rerun()


def q9():
    st.subheader("Question 9")
    st.divider()
    q9 = st.radio("What is the '%' operator in python?", ["Options:", "Modulus", "Exponential", "Floor Division", "Percentage"])
    if q9 != "Options:":
        if st.button("Next Question"):
            if q9 == "Modulus":
                st.success("Correct answer!")
                st.session_state.score += 1
                countdown()
                st.session_state.current_page = "q10"
                st.rerun()
            else:
                st.error("Wrong answer!")
                countdown()
                st.session_state.current_page = "q10"
                st.rerun()


def q10():
    st.subheader("Question 10")
    st.divider()
    q10 = st.radio("All loops run forever", ["Options:", "True", "False"])
    if q10 != "Options:":
        if st.button("Next Question"):
            if q10 == "False":
                st.success("Correct answer!")
                st.session_state.score += 1
                countdown()
                st.session_state.current_page = "q11"
                st.rerun()
            else:
                st.error("Wrong answer!")
                countdown()
                st.session_state.current_page = "q11"
                st.rerun()


def q11():
    st.subheader("Question 11")
    st.divider()
    q11 = st.radio("How many 'z' does this code output? \n\nx = 0 \n\nwhile x <= 5:\n\n   x += 1\n\n   print('z')", ["Options:", "7", "4", "6", "5"])
    if q11 != "Options:":
        if st.button("Next Question"):
            if q11 == "6":
                st.success("Correct answer!")
                st.session_state.score += 1
                countdown()
                st.session_state.current_page = "q12"
                st.rerun()
            else:
                st.error("Wrong answer!")
                countdown()
                st.session_state.current_page = "q12"
                st.rerun()


def q12():
    st.subheader("Question 12")
    st.divider()
    q12 = st.radio("What type of programming language is python?", ["Options:", "Front end", "Back end", "Both", "Neither"])
    if q12 != "Options:":
        if st.button("Finish Quiz"):
            if q12 == "Back end":
                st.success("Correct answer!")
                st.session_state.score += 1
                countdown()
                st.session_state.current_page = "finish"
                st.rerun()
            else:
                st.error("Wrong answer!")
                countdown()
                st.session_state.current_page = "finish"
                st.rerun()


def finish():
    st.info(f"Congrats! You have finished Sam's python quiz.\n\n Your score was {st.session_state.score}/12\n\n Would you like to take another quiz??")
    if st.button("Back to Homepage"):
        st.session_state.score = 0
        st.session_state.current_page = "start"
        st.rerun()
#--------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

if st.session_state.current_page == "start":
    start()
if st.session_state.current_page == "q1":
    q1()
elif st.session_state.current_page == "q2":
    q2()
elif st.session_state.current_page == "q3":
    q3()
elif st.session_state.current_page == "q4":
    q4()
elif st.session_state.current_page == "q5":
    q5()
elif st.session_state.current_page == "q6":
    q6()
elif st.session_state.current_page == "q7":
    q7()
elif st.session_state.current_page == "q8":
    q8()
elif st.session_state.current_page == "q9":
    q9()
elif st.session_state.current_page == "q10":
    q10()
elif st.session_state.current_page == "q11":
    q11()
elif st.session_state.current_page == "q12":
    q12()
elif st.session_state.current_page == "finish":
    finish()
