import streamlit as st
import time
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_icon='📚',page_title='Fun Quiz')

# -------------------------------------------
# CSV file setup
CSV_FILE = "quiz_results.csv"
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Name", "Score"]).to_csv(CSV_FILE, index=False)

# -------------------------------------------
# Session state setup
if "score" not in st.session_state:
    st.session_state.score = 0
if "name" not in st.session_state:
    st.session_state.name = ""
if "current_question" not in st.session_state:
    st.session_state.current_question = "q1"

# -------------------------------------------
def countdown():
    time.sleep(0.5)

def save_results():
    df = pd.read_csv(CSV_FILE)
    new_entry = {
        "Name": st.session_state.name,
        "Score": st.session_state.score
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# -------------------------------------------
# Navigation Menu
menu = st.sidebar.selectbox("📌 Menu", ["📝 Quiz", "📊 Results"])

# -------------------------------------------
def start_quiz():
    st.title("📚 Fun Quiz For Kids")
    name = st.text_input("Enter your name to start:")
    if st.button("Start Quiz"):
        if name:
            st.session_state.name = name
            st.session_state.score = 0
            st.session_state.current_question = "q1"
            st.rerun()
        else:
            st.warning("Please enter your name first.")

# -------------------------------------------
def question(num, question_text, options, correct, next_q, last=False):
    st.subheader(f"Question {num}")
    st.divider()
    answer = st.pills(question_text, options, selection_mode="single", key=f"q{num}_ans")

    if answer:
        if st.button("Next Question" if not last else "Finish Quiz", key=f"btn_q{num}"):
            if answer == correct:
                st.success("✅ Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct was: {correct}")

            countdown()
            st.session_state.current_question = next_q
            if last:
                save_results()
            st.rerun()

# -------------------------------------------
def finish():
    st.success(f"🎉 Congrats {st.session_state.name}! Your final score is {st.session_state.score}/20")
    st.info("👉 Check the 📊 Results page to see how everyone scored.")

# -------------------------------------------
def results_page():
    st.title("📊 Quiz Results")

    df = pd.read_csv(CSV_FILE)
    if df.empty:
        st.warning("No results yet.")
        return


    with st.expander("All Students' Scores"):
        st.dataframe(df)

    view = st.radio("Choose chart view:", ["Pie Chart", "Bar Chart"],horizontal=True)

    if view == "Pie Chart":
        fig = px.pie(df, values="Score", names="Name")
        st.plotly_chart(fig, use_container_width=True)

    elif view == "Bar Chart":
        fig = px.bar(df, x="Name", y="Score")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------
# 20 Mixed Reasoning Questions (Math, English, Science, Space, Computer)
def q1(): question(1, "What is 15 + 7?", ["20", "21", "22", "23"], "22", "q2")
def q2(): question(2, "Which planet is known as the Red Planet?", ["Earth", "Venus", "Mars", "Jupiter"], "Mars", "q3")
def q3(): question(3, "Which one is a mammal?", ["Shark", "Dolphin", "Frog", "Lizard"], "Dolphin", "q4")
def q4(): question(4, "Opposite of 'hot' is?", ["Warm", "Cold", "Cool", "Boil"], "Cold", "q5")
def q5(): question(5, "Which key is used to erase letters on a computer?", ["Shift", "Enter", "Backspace", "Ctrl"], "Backspace", "q6")
def q6(): question(6, "What is 9 × 8?", ["72", "81", "64", "69"], "72", "q7")
def q7(): question(7, "The Sun rises in the?", ["North", "South", "East", "West"], "East", "q8")
def q8(): question(8, "Which gas do humans need to breathe in?", ["Oxygen", "Carbon dioxide", "Hydrogen", "Nitrogen"], "Oxygen", "q9")
def q9(): question(9, "What is the plural of 'child'?", ["Childs", "Children", "Childes", "Childrens"], "Children", "q10")
def q10(): question(10, "Which device is used to print documents?", ["Monitor", "Printer", "Keyboard", "Mouse"], "Printer", "q11")
def q11(): question(11, "What is 100 ÷ 4?", ["20", "25", "30", "40"], "25", "q12")
def q12(): question(12, "Which is the largest planet?", ["Earth", "Mars", "Jupiter", "Saturn"], "Jupiter", "q13")
def q13(): question(13, "Which part of the plant makes food?", ["Root", "Stem", "Leaf", "Flower"], "Leaf", "q14")
def q14(): question(14, "Choose the correct spelling:", ["Enviroment", "Envirnment", "Environment", "Envaironment"], "Environment", "q15")
def q15(): question(15, "Shortcut to copy text on computer?", ["Ctrl + P", "Ctrl + V", "Ctrl + C", "Ctrl + X"], "Ctrl + C", "q16")
def q16(): question(16, "What is 45 − 19?", ["24", "25", "26", "27"], "26", "q17")
def q17(): question(17, "Which galaxy do we live in?", ["Andromeda", "Whirlpool", "Milky Way", "Sombrero"], "Milky Way", "q18")
def q18(): question(18, "Which organ pumps blood in the body?", ["Lungs", "Liver", "Heart", "Kidney"], "Heart", "q19")
def q19(): question(19, "Past tense of 'go' is?", ["Goed", "Went", "Gone", "Go"], "Went", "q20")
def q20(): question(20, "Binary numbers are made of?", ["0s and 1s", "1s and 2s", "2s and 3s", "5s and 10s"], "0s and 1s", "finish", last=True)

# -------------------------------------------
# Page Navigation
if menu == "📝 Quiz":
    if not st.session_state.name:
        start_quiz()
    else:
        if st.session_state.current_question == "q1": q1()
        elif st.session_state.current_question == "q2": q2()
        elif st.session_state.current_question == "q3": q3()
        elif st.session_state.current_question == "q4": q4()
        elif st.session_state.current_question == "q5": q5()
        elif st.session_state.current_question == "q6": q6()
        elif st.session_state.current_question == "q7": q7()
        elif st.session_state.current_question == "q8": q8()
        elif st.session_state.current_question == "q9": q9()
        elif st.session_state.current_question == "q10": q10()
        elif st.session_state.current_question == "q11": q11()
        elif st.session_state.current_question == "q12": q12()
        elif st.session_state.current_question == "q13": q13()
        elif st.session_state.current_question == "q14": q14()
        elif st.session_state.current_question == "q15": q15()
        elif st.session_state.current_question == "q16": q16()
        elif st.session_state.current_question == "q17": q17()
        elif st.session_state.current_question == "q18": q18()
        elif st.session_state.current_question == "q19": q19()
        elif st.session_state.current_question == "q20": q20()
        elif st.session_state.current_question == "finish": finish()

elif menu == "📊 Results":
    results_page()
