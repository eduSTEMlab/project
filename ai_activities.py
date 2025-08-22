import streamlit as st
import requests
from fpdf import FPDF #python module to generate PDFs
import base64 #python module to convert binary data (code) to printable character (PDF)
import re # Python module for text search and replace using regular expressions

# import os
imageurl = 'edustemlab2.png'

if 'get_response' not in st.session_state:
    st.session_state.get_response = 'Nothing Yet'

if 'submit' not in st.session_state:
    st.session_state.submit = False

def clean_for_pdf(text):
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

# st.write(st.session_state)

st.set_page_config(page_title='AI Activities', page_icon='📚')
st.sidebar.title(':rainbow[A.I Python Activities]')
st.sidebar.image(imageurl,width=120)
adminpass = st.sidebar.text_input('E',placeholder='Enter Pass',label_visibility='collapsed',type='password')
st.sidebar.divider()

if adminpass == 'Interactive79':

    # OpenRouter API key and model setup
    OPENROUTER_API_KEY = "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"  # Replace this with your actual key
    # MODEL_NAME = "openai/gpt-3.5-turbo"  # You can change this to claude-3-opus, llama3, etc.

    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    HEADERS = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }




    # Function to send prompt to OpenRouter
    def ask_openrouter(prompt):
        payload = {
            "model": "openai/gpt-3.5-turbo", # You can change this to claude-3-opus, llama3, etc.
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        try:
            res = requests.post(API_URL, headers=HEADERS, json=payload)
            res.raise_for_status()
            return res.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {e}"
        

    # -------------------------function to generate our PDF-----------------------------
    def generate_pdf():
        pdf = FPDF() #create a var to rep our FPDF module

        #Add a page
        pdf.add_page()

        #s=Set your default fonts
        pdf.set_font('Arial', size=12)

        #Set column1 x and y coord

        col1x = 20
        col1y = 25

        #Set column width
        colw = 90
        colh = 10

        #Add Logo
        pdf.image(imageurl,x=col1x+120,y=col1y-15,w=50)

        # FONTS TO USE: Courier, Helvetica/Arial,  Times, Symbol, ZapfDingbats
        #TOPIC
        # pdf.set_text_color(50,168,125)
        pdf.set_font(family='Courier',size=30,style='B')
        pdf.set_xy(20, col1y+5)
        pdf.multi_cell(170,10,txt=f'{st.session_state.topics} Class Activity',align='C')


        # FONTS TO USE: Courier, Helvetica/Arial,  Times, Symbol, ZapfDingbats
        #QUESTION
        # pdf.set_text_color(50,168,125)
        safe_text = clean_for_pdf(st.session_state.get_response)
        pdf.set_font(family='Courier',size=16)
        pdf.set_xy(20, col1y + 35)
        pdf.multi_cell(170,10,safe_text,align='C')

        #Save the PDF
        pdf_file = 'invoice.pdf'
        pdf.output(pdf_file)
        return pdf_file


    # -------------------------AI Variables-----------------------------
    def variables_prompt():
        prompt = f"""
        
    Write a Python program to display details about a student’s school life.

    Create a variable called student_name and assign it the student’s name (e.g., "Alex").
    Create a variable called school_name and assign it the name of the school (e.g., "Greenwood High").
    Create a variable called favorite_subject and assign it the name of the student’s favorite subject (e.g., "Math").
    Create a variable called grade_level and assign it the student’s grade level (e.g., 5).
    Use the print function to display the following:
    The student’s name and school: "The student’s name is [student_name], and they study at [school_name]."
    The favorite subject: "Their favorite subject is [favorite_subject]."
    The grade level: "They are currently in grade [grade_level]."
        
        
        
    Generate a python question on variables and data with a completely different child friendly story scenerio and tasks like the question above. Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points bullet points bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too


    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points bullet points of each instruction. clear text formmatting
    Only use characters that are compatible with the Latin-1 codec (no curly quotes, emojis, or special symbols).
    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too
    Do not include code. 
    Do not include headers, formatting, or asterisks. 
    Use only plain text. 
    Avoid any negative, dark, wizard, or magical story (it is for Christian kids). 
        """

        try:
            st.session_state.get_response = ask_openrouter(prompt)

            return True
        except:
            st.error('Error Generating Activity')
            return None



    # -------------------------AI Operators-----------------------------
    def operator_prompt(chooseoperators):
        prompt = f"""
        
    Liam is organizing a graduation party. He bought chairs for $120, food for $250, drinks for $80, and a sound system for $150.

    Write a Python program to calculate the total money Liam spent on all the items.

    Start by saving Liam’s name and store it in a variable called name.
    Define variables for the costs of the chairs, food, drinks, and sound system:
    Store the cost of chairs in a variable called chairs_cost and set it to 120.
    Store the cost of food in a variable called food_cost and set it to 250.
    Store the cost of drinks in a variable called drinks_cost and set it to 80.
    Store the cost of the sound system in a variable called sound_system_cost and set it to 150.
    Calculate the total amount spent by adding all the item costs.
    Store the total amount in a variable called total_cost.
    Print a message that includes Liam’s name and the total amount spent in a friendly sentence, like this:
    “Hi [name]! You spent a total of $[total_cost] on your graduation party preparations.”



        Include {chooseoperators} operators in the question

    Generate a python question on python operators with a completely different child friendly story scenerio and tasks like the question above. 
    Only use characters that are compatible with the Latin-1 codec (no curly quotes, emojis, or special symbols).
    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too
    Do not include code. 
    Do not include headers, formatting, or asterisks. 
    Use only plain text. 
    Avoid any negative, dark, wizard, or magical story (it is for Christian kids). 

        """

        try:
            st.session_state.get_response = ask_openrouter(prompt)

            return True
        except:
            st.error('Error Generating Activity')
            return None


    # -------------------------AI ifelse-----------------------------
    def ifelse_prompt(chooseoperators):
        prompt = f"""
        
    John has $250 saved up. He plans to spend some of this money on various activities and then split the remaining amount equally for his next few outings. Write a Python program to calculate how much money John has left after his expenses and how much money he can allocate for each outing. Use an if condition to tell him if he can still go for outings or if he spent all his money.

    Start by defining a variable for the initial savings and set it to $250.
    Ask John how much he spent on a new pair of shoes and store it in a variable called shoes_cost (as an integer).
    Ask how much he spent on groceries and store it in a variable called groceries_cost (as an integer).
    Ask how much he spent on a movie ticket and store it in a variable called movie_ticket_cost (as an integer).
    Ask how much he spent on a gift and store it in a variable called gift_cost (as an integer).
    Ask how much he spent on a meal and store it in a variable called meal_cost (as an integer).
    Calculate the total expenses by adding shoes_cost, groceries_cost, movie_ticket_cost, gift_cost, and meal_cost.
    Calculate the amount left by subtracting the total expenses from the initial savings.
    Ask John how many outings he wants to plan and store it in a variable called num_outings (as an integer).
    Calculate the amount per outing by dividing the amount left by num_outings if the amount left is greater than zero.
    Use an if else condition to check if there is still money left to go for outings or if he spent all his money.
        

    Generate a python question on python if else with a completely different child friendly story scenerio and tasks like the question above. Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too


        Include {chooseoperators} operators in the question

        Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points of each instruction. clear text formmatting
        Only use characters that are compatible with the Latin-1 codec (no curly quotes, emojis, or special symbols).
        Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too
        Do not include code. 
        Do not include headers, formatting, or asterisks. 
        Use only plain text. 
        Avoid any negative, dark, wizard, or magical story (it is for Christian kids). 
        """

        try:
            st.session_state.get_response = ask_openrouter(prompt)

            return True
        except:
            st.error('Error Generating Activity')
            return None

    # -------------------------AI ifelifelse-----------------------------
    def ifelifelse_prompt(chooseoperators):
        prompt = f"""
        
    Write a Python program to check the type of day a student will have based on the number of homework tasks they completed.

    Start by asking for the student’s name and store it in a variable called name.
    Ask how many homework tasks they have completed and store it in a variable called completed_tasks (as an integer).
    Use an if-elif-else structure to check the following:
    If completed_tasks is 10 or more, print:
    "Excellent work, [name]! You completed [completed_tasks] tasks. You can enjoy a free day!"
    If completed_tasks is between 5 and 9, print:
    "Good job, [name]! You completed [completed_tasks] tasks. You’re on track!"
    If completed_tasks is between 1 and 4, print:
    "Keep going, [name]! You completed [completed_tasks] tasks. A little more effort will pay off!"
    If completed_tasks is 0, print:
    "Don't give up, [name]! Start working on your tasks. You can do it!"    

    Generate a python question on python if elif else with a completely different child friendly story scenerio and tasks like the question above. Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too


        Include {chooseoperators} operators in the question

    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points of each instruction. clear text formmatting
    Only use characters that are compatible with the Latin-1 codec (no curly quotes, emojis, or special symbols).
    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too
    Do not include code. 
    Do not include headers, formatting, or asterisks. 
    Use only plain text. 
    Avoid any negative, dark, wizard, or magical story (it is for Christian kids). 
        """

        try:
            st.session_state.get_response = ask_openrouter(prompt)

            return True
        except:
            st.error('Error Generating Activity')
            return None

    # ------------------------------------------------------


    # -------------------------AI list-----------------------------
    def list_prompt(chooseoperators):
        prompt = f"""
        
    Fruit Basket Program
    Lara is preparing a fruit basket for her family’s picnic. She starts with a list of fruits she already has at home: 'apple', 'mango', and 'banana'.

    She wants to:

    See all the fruits she currently has.

    Check which fruit is the first in the list.

    Add 'pineapple' to her basket.

    Find out how many fruits she now has in total.

    Task:
    Write a Python program that helps Lara complete all these steps using a list.

    Your program should:

    Create a list called fruits with the three starting fruits.

    Print the entire list of fruits.

    Print the first fruit in the list.

    Add 'pineapple' to the list using .append().

    Print the updated list.

    Use len() to count how many fruits are now in the list and print the result.


    Generate a python question on python list with a completely different child friendly story scenerio and tasks like the question above. Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too


    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points of each instruction. clear text formmatting
    Only use characters that are compatible with the Latin-1 codec (no curly quotes, emojis, or special symbols).
    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too
    Do not include code. 
    Do not include headers, formatting, or asterisks. 
    Use only plain text. 
    Avoid any negative, dark, wizard, or magical story (it is for Christian kids). 
        """

        try:
            st.session_state.get_response = ask_openrouter(prompt)

            return True
        except:
            st.error('Error Generating Activity')
            return None

    # -------------------------AI Quiz-----------------------------
    def quiz_prompt(chooseoperators):
        prompt = f"""
    
    You will create a Python program that asks 3 medical awareness questions.
    The program will:

    Ask for the user’s name.

    Show each question and 3 choices.

    Use if…else to check if the answer is correct.

    Add 1 point for each correct answer.

    At the end, show the total correct score and give a grade message based on the score.

    Question 1 – Nosebleed
    Your friend’s nose suddenly starts bleeding 😮

    What should you do first?

    Press 1 for: Tilt their head back and pinch the nose
    Press 2 for: Tilt their head forward and pinch the nose
    Press 3 for: Make them lie flat on the ground

    ✅ Correct Answer: 2 – Tilt their head forward and pinch the nose

    Question 2 – Choking
    Someone is eating and suddenly starts coughing hard, can’t speak, and looks panicked 😨

    What should you do first?

    Press 1 for: Give them water to drink
    Press 2 for: Perform the Heimlich maneuver
    Press 3 for: Tell them to lie down and rest

    ✅ Correct Answer: 2 – Perform the Heimlich maneuver

    Question 3 – Fainting
    You see your friend faint while standing in the sun ☀️

    What should you do first?

    Press 1 for: Lay them on their back and lift their legs
    Press 2 for: Give them food immediately
    Press 3 for: Shake them to wake them up

    ✅ Correct Answer: 1 – Lay them on their back and lift their legs

    🛠 Your Job
    Ask the user to type their name.

    Show each question with the 3 choices.

    If the answer is correct, say:
    ✅ That's right, [name]!
    Add 1 point to the score.

    If the answer is wrong, say:
    ❌ Oops, not the best choice.

    If the answer is not 1, 2, or 3, say:
    ⚠️ Please pick 1, 2, or 3.

    After all 3 questions, show the total score in this format:
    "You got X out of 3 correct."

    Use a conditional statement to grade:

    If score is 3: "🎉 Excellent! You know your first aid well."

    If score is 2: "👍 Good job! Just a little more practice needed."

    If score is 0 or 1: "📚 Keep learning! First aid can save lives."



    Generate a python question on python quiz, create 1 to 5 questions and a correct answer with a completely different child friendly story scenerio and tasks like the question above. Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too


        Include {chooseoperators} operators in the question

    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points of each instruction. clear text formmatting
    Only use characters that are compatible with the Latin-1 codec (no curly quotes, emojis, or special symbols).
    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too
    Do not include code. 
    Do not include headers, formatting, or asterisks. 
    Use only plain text. 
    Avoid any negative, dark, wizard, or magical story (it is for Christian kids). 
        """

        try:
            st.session_state.get_response = ask_openrouter(prompt)

            return True
        except:
            st.error('Error Generating Activity')
            return None


    # -------------------------AI Selections Calculator-----------------------------
    def bill_prompt():
        prompt = f"""
        
    import streamlit as s

    bill = 0
    s.header('''Kozi's Super Restaurent!''')


    s.image('https://www.jusrol.co.uk/wp-content/uploads/2023/04/puff-pastry-cheese-stars-500x408.png')


    s.subheader('Main Food')


    food1, food2 , food3 , food4 = s.columns(4)


    with food1:
        if s.checkbox('Rice & Chicken: $10'):
            s.write('Ok! ')
            bill += 10
        if s.checkbox('Pap & Sauce: $10'):
            s.write('Ok! ')
            bill +=10
    with food2:
        if s.checkbox('Beans Porrdige: $5'):
            s.write('Ok! ')
            bill += 5
        if s.checkbox('Poutine: $15'):
            s.write('Ok! ')
            bill += 15
    with food3:
        if s.checkbox('Pasta & Sauce: $15'):
            s.write('Ok! ')
        if s.checkbox('Bacon and Eggs: $10'):
            s.write('Ok! ')
    with food4:


        if s.checkbox('Yam & Eggs: $10'):
            s.write('Ok! ')
        if s.checkbox('Burger & Fries: $15'):
            s.write('Ok!')


    s.subheader('Snacks')


    snack1, snack2, snack3, snack4 = s.columns(4)


    with snack1:
        if s.checkbox('Bear Paws Choco Chip: $1.50'):
            s.write('Ok!')
        if s.checkbox('Bear Paws Banana: $1.50'):
            s.write('Ok!')
    with snack2:
        if s.checkbox('Chips BBQ: $3'):
            s.write('Ok!')
        if s.checkbox('Chips Plain: $4'):
            s.write('Ok!')
    with snack3:
        if s.checkbox('Cookies: $7'):
            s.write('Ok! ')
        if s.checkbox('Ice Cream: $7'):
            s.write('Ok!')
    with snack4:
        if s.checkbox('Stars: $10'):
            s.write('Ok!')
        if s.checkbox('Moons: $10'):
            s.write('Ok! ')


    s.subheader('Drinks')


    drink1, drink2, drink3, drink4 = s.columns(4)


    with drink1:
        if s.checkbox('Kombucha: $8.50'):
            s.write('Ok!')
        if s.checkbox('Pepsi: $3'):
            s.write('Ok!')
    with drink2:
        if s.checkbox('Coke: $3'):
            s.write('Ok!')
        if s.checkbox('Fanta: $4'):
            s.write('Ok!')
    with drink3:
        if s.checkbox('Diet Coke: $7'):
            s.write('Ok! ')
        if s.checkbox('Diet Pepsi: $7'):
            s.write('Ok!')
    with drink4:
        if s.checkbox('Sparkling Water Oranges: $10'):
            s.write('Ok!')
        if s.checkbox('Sparkaling Water Coconut: $10'):
            s.write('Ok! ')


    s.subheader('Fruits')
    fruit1, fruit2, fruit3, fruit4 = s.columns(4)


    with fruit1:
        if s.checkbox('Apples: $8.50'):
            s.write('Ok!')
        if s.checkbox('Oranges: $3'):
            s.write('Ok!')
    with fruit2:
        if s.checkbox('Bananas: $3'):
            s.write('Ok!')
        if s.checkbox('Strawberries: $4'):
            s.write('Ok!')
    with fruit3:
        if s.checkbox('Blueberries: $7'):
            s.write('Ok! ')
        if s.checkbox('Rasberries: $7'):
            s.write('Ok!')
    with fruit4:
        if s.checkbox('Blackberries: $10'):
            s.write('Ok!')
        if s.checkbox('Dragonfruit: $10'):
            s.write('Ok! ')



    if s.button("Check total bill"):
        s.write("Your total bill is", bill, 'dollars')
        
    Generate a python question on python streamlit bill calculator with a completely different child friendly story scenerio and tasks like the question above. Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too

    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points of each instruction. clear text formmatting
    Only use characters that are compatible with the Latin-1 codec (no curly quotes, emojis, or special symbols).
    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too
    Do not include code. 
    Do not include headers, formatting, or asterisks. 
    Use only plain text. 
    Avoid any negative, dark, wizard, or magical story (it is for Christian kids). 
        """

        try:
            st.session_state.get_response = ask_openrouter(prompt)

            return True
        except:
            st.error('Error Generating Activity')
            return None

    # -------------------------AI Selections Calculator-----------------------------
    def selections_prompt():
        prompt = f"""
        
    Sarah, a devoted Christian, is preparing for an extraordinary journey of faith. She aims to purchase her Bible, select devotional books, buy modest outfits, adopt a pet, and perhaps stock up on some fancy artifacts to deepen her faith. Write a Python program to help Sarah calculate the total cost of her spiritual adventure.

    Sarah’s journey through the Christian marketplace involves several steps:

    Bible Purchase:

    Sarah needs to purchase her primary Bible, which costs $50.
    Account Login:

    Sarah will log in to her account using her username and password.
    Devotional Books Selection:

    Sarah can choose one or more devotional books:
    Daily Devotions for $10
    Bible Study Guide for $20
    Prayer Journal for $15
    Modest Outfits:

    Sarah can browse through three different modest outfits, each with its own price tag:
    Outfit 1 costs $30
    Outfit 2 costs $50
    Outfit 3 costs $70
    Pet Adoption:

    Sarah has the option to adopt a pet for $25 each.
    She can choose up to three pets.
    Religious Artifacts Purchase:

    Sarah can purchase fancy artifacts:
    Cross Necklace for $10
    Rosary Beads for $20
    Icon for $30
    Total Calculation:

    After making her selections, Sarah wants to see the total cost of her spiritual adventure.
    Python Blocks

    Generate a python question on python streamlit bill selections calculator with a completely different child friendly story scenerio and tasks like the question above. Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too

    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points of each instruction. clear text formmatting
    Only use characters that are compatible with the Latin-1 codec (no curly quotes, emojis, or special symbols).
    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too
    Do not include code. 
    Do not include headers, formatting, or asterisks. 
    Use only plain text. 
    Avoid any negative, dark, wizard, or magical story (it is for Christian kids). 
        """

        try:
            st.session_state.get_response = ask_openrouter(prompt)

            return True
        except:
            st.error('Error Generating Activity')
            return None


    # -------------------------AI Dict Table Calculator-----------------------------
    def dictable_prompt():
        prompt = f"""
        
    Scenario: Candy Shop Helper

    You are helping at a candy shop where kids buy sweets. The shopkeeper wants to quickly check how many sweets kids buy and do some math with the numbers.

    Step-by-step instructions:

    Ask the user to type the number of candies in the first box.

    Ask the user to type the number of candies in the second box.

    Add both numbers to find out the total candies and save it in a variable called addition.

    Multiply the two numbers to find out how many candies are in total packs and save it in a variable called multiplication.

    Create a dictionary that shows:

    Number of candies in the first box

    Number of candies in the second box

    Total candies (addition)

    Total packs (multiplication)

    Store all the information in a dictionary and display it on the screen.

    Display the dictionary in a neat streamlit table.


    Generate a python question on python streamlit dictionary task with a completely different child friendly story scenerio and tasks like the question above. Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too

    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points of each instruction. clear text formmatting
    Only use characters that are compatible with the Latin-1 codec (no curly quotes, emojis, or special symbols).
    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too
    Do not include code. 
    Do not include headers, formatting, or asterisks. 
    Use only plain text. 
    Avoid any negative, dark, wizard, or magical story (it is for Christian kids). 
        """

        try:
            st.session_state.get_response = ask_openrouter(prompt)

            return True
        except:
            st.error('Error Generating Activity')
            return None



    # -------------------------AI Dict Chart Calculator-----------------------------
    def dictchart_prompt():
        prompt = f"""
        
    Scenario: Fruit Sales Tracker

    You are helping your class keep track of how many fruits are sold at the school fruit stand.

    Step-by-step instructions:

    Create a page title that says “Fruit Sales Tracker.”

    Make two columns side by side.

    In the first column, add a dropdown list of fruits (Apple, Orange, Banana, Lemon, Lime, Blueberries, Grapes, Dragonfruit).

    In the second column, add a number box where kids can type how many of that fruit were sold (between 0 and 1000).

    Add a button called “Enter Sales.”

    When the button is pressed:

    Add the fruit name and number sold into a dictionary

    Display the dictionary as a table that shows all sales so far.

    Show a message that says “Sales Submitted!”

    Show a bar chart or pie chart to see each fruit total sales.


    Generate a python question on python streamlit plotly chart task with a completely different child friendly story scenerio and tasks like the question above. Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too

    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points of each instruction. clear text formmatting
    Only use characters that are compatible with the Latin-1 codec (no curly quotes, emojis, or special symbols).
    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too
    Do not include code. 
    Do not include headers, formatting, or asterisks. 
    Use only plain text. 
    Avoid any negative, dark, wizard, or magical story (it is for Christian kids). 
        """

        try:
            st.session_state.get_response = ask_openrouter(prompt)

            return True
        except:
            st.error('Error Generating Activity')
            return None
        


    # -------------------------AI Dict CSV Calculator-----------------------------
    def dictcsv_prompt():
        prompt = f"""
        
    Scenario: Fruit Market Helper

    You are helping at a fruit market where customers buy apples and oranges. The shopkeeper wants you to do some quick math to help him.

    Step-by-step instructions:

    Create a menu with two pages:

    User Input

    View Records

    If the page is on User Input:

    Ask the user to type the number of apples bought.

    Ask the user to type the number of oranges bought.

    Add both numbers to find out the total fruits and save it in a variable called addition.

    Multiply the two numbers to find out the fruit combos (apples × oranges) and save it in a variable called multiplication.

    Create a dictionary that shows:

    Number of apples

    Number of oranges

    Total fruits (addition)

    Fruit combos (multiplication)

    Store all the current information in a dictionary and display it on the screen.

    Save the information in a CSV file.

    If the menu is on View Records:

    Display the CSV file table.

    Plot a bar chart and a pie chart of the fruit records.

    Generate a python question on python streamlit plotly chart task with a completely different child friendly story scenerio and tasks like the question above. Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too

    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points of each instruction. clear text formmatting
    Only use characters that are compatible with the Latin-1 codec (no curly quotes, emojis, or special symbols).
    Do not include code, no magic, wizardry, evil or negative story. Write only the scenario and the step-by-step bullet points instructions. Do not include the header. No format, no asterisk. Do not include the code too
    Do not include code. 
    Do not include headers, formatting, or asterisks. 
    Use only plain text. 
    Avoid any negative, dark, wizard, or magical story (it is for Christian kids). 
        """

        try:
            st.session_state.get_response = ask_openrouter(prompt)

            return True
        except:
            st.error('Error Generating Activity')
            return None
    # -------------------------listboxes-----------------------------

    topics = ['Variables & Data', 'Python Operators','Input Statement','If Else','If Elif, Else','Quiz Maker','List','Bill Calculator','Selections Calculator','Dict & Table','Plotly Chart','Dict & CSV']
    questionmode = ['Practical','Quiz']
    operators = ['+','-','*','/','%']
    # -------------------------selections-----------------------------
    choosetopics = st.sidebar.selectbox('Choose topics',topics)

    if choosetopics == 'Python Operators'or choosetopics == 'Input Statement' or choosetopics == 'If Else'or choosetopics == 'If Elif, Else' or choosetopics == 'Quiz Maker':
        chooseoperators = st.sidebar.multiselect('Select operators *(optional)*',operators)
    # choosemode = st.sidebar.selectbox('Choose Mode', questionmode)



    # ---------------- Sidebar Form ----------------
    with st.sidebar.form("Activityform"):

        st.session_state.topics = choosetopics

        # Submit button
        activitybutton = st.form_submit_button(' :red[Generate Activity]')

        


    # ---------------- Handle Activity Generation ----------------
    if activitybutton:  # replaces st.session_state.submit
        if choosetopics == 'Variables & Data':
            with st.spinner(f'Generating Activity on {choosetopics}...'):
                success = variables_prompt()
                if success:
                    st.sidebar.success('Activity Generated!')
    # -------------------------AI Operators-----------------------------
        if choosetopics == 'Python Operators':
            with st.spinner(f'Generating Activity on {choosetopics}...'):
                success = operator_prompt(chooseoperators)
                if success:
                    st.sidebar.success('Activity Generated!')

    # -------------------------AI IfElse-----------------------------
        if choosetopics == 'If Else':
            with st.spinner(f'Generating Activity on {choosetopics}...'):
                success = ifelse_prompt(chooseoperators)
                if success:
                    st.sidebar.success('Activity Generated!')

    # -------------------------AI IfElifElse-----------------------------
        if choosetopics == 'If Elif, Else':
            with st.spinner(f'Generating Activity on {choosetopics}...'):
                success = ifelifelse_prompt(chooseoperators)
                if success:
                    st.sidebar.success('Activity Generated!')

    # -------------------------AI List-----------------------------
        if choosetopics == 'List':
            with st.spinner(f'Generating Activity on {choosetopics}...'):
                success = list_prompt()
                if success:
                    st.sidebar.success('Activity Generated!')

    # -------------------------AI Quiz Maker-----------------------------
        if choosetopics == 'Quiz Maker':
            with st.spinner(f'Generating Activity on {choosetopics}...'):
                success = quiz_prompt(chooseoperators)
                if success:
                    st.sidebar.success('Activity Generated!')

    # -------------------------AI Bill-----------------------------
        if choosetopics == 'Bill Calculator':
            with st.spinner(f'Generating Activity on {choosetopics}...'):
                success = bill_prompt()
                if success:
                    st.sidebar.success('Activity Generated!')

    # -------------------------AI Selections-----------------------------
        if choosetopics == 'Selections Calculator':
            with st.spinner(f'Generating Activity on {choosetopics}...'):
                success = selections_prompt()
                if success:
                    st.sidebar.success('Activity Generated!')

    # -------------------------AI Dictable-----------------------------
        if choosetopics == 'Dict & Table':
            with st.spinner(f'Generating Activity on {choosetopics}...'):
                success = dictable_prompt()
                if success:
                    st.sidebar.success('Activity Generated!')

    # -------------------------AI Charts-----------------------------
        if choosetopics == 'Plotly Chart':
            with st.spinner(f'Generating Activity on {choosetopics}...'):
                success = dictchart_prompt()
                if success:
                    st.sidebar.success('Activity Generated!')

    # -------------------------AI Dict CSV-----------------------------
        if choosetopics == 'Dict & CSV':
            with st.spinner(f'Generating Activity on {choosetopics}...'):
                success = dictcsv_prompt()
                if success:
                    st.sidebar.success('Activity Generated!')

    st.sidebar.warning('*Please proof-read the question generated. You can also click on Generate again if you dont like the question*')

    if st.session_state.get_response != 'Nothing Yet':
        #Generate the PDF
        pdf_func = generate_pdf()

        #Read the PDF FUNCT as binary data
        with open(pdf_func, 'rb') as binary:
            pdf_data = binary.read()


        safe_text = clean_for_pdf(st.session_state.get_response)
        st.info(safe_text)
        st.divider()
        but1, but2 = st.columns(2)

        with but1:
            # Display the download button
            if st.session_state.get_response:
                st.download_button(label=':blue[Download Class Activity]', data=pdf_data, file_name=f'{choosetopics}.pdf', mime='application/pdf')
            else:
                st.error('Kindly Select A Topic')

        # with but2:
        #     view = st.button(":blue[View Class Activity]")
                
        # if view:
        #         #Write the PDF using base64
        #         pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

        #         #Generate the HTML to embed the PDF
        #         pdf_embed = f'<embed src="data:application/pdf;base64,{pdf_base64}" type="application/pdf" width="100%" height="600px" />'

        #         #Display the embedded pdf (Markdown helps us use HTML in streamlit)
        #         st.markdown(pdf_embed,unsafe_allow_html=True)


