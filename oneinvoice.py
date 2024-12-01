#tax and discount by % (optional),change coy details send email, auto gen invoice number,currency

import streamlit as st #python module to create framework/page
from fpdf import FPDF #python module to generate PDFs
import base64 #python module to convert binary data (of your code) to printable characters
import pandas as pd

#food,recyling, donations, loan
st.set_page_config(page_title='Invoice Generator',page_icon="📑",layout="centered",initial_sidebar_state="expanded")

detailscsv = pd.read_csv("invoicedetails.csv")
# st.table(detailscsv)

imageurl = 'Logobiz.png'
menu = st.sidebar.selectbox('Menu',['Invoice Generator','Change Details'])


if menu == 'Change Details':
     #logo, name, addr, country,bank name, acc name, number, 
     # name,addr,country,bank,accname,accnumber,
     adminpass = st.sidebar.text_input("Enter Admin password",type='password')
     if adminpass == '12345':

          l1,l2,l3 = st.columns([1,2,1])
          with l2:
               logo = st.file_uploader("Change your logo here",type=['jpg','png','jpeg'])


          if st.button("Save new logo"):
               if logo is not None:
                    # Set the new file name
                    new_file_name = "Logobiz.png"

                    # Save the uploaded file with the new file name
                    with open(new_file_name, "wb") as f:
                         f.write(logo.getbuffer())
                    
                    st.write(f"File uploaded and saved as {new_file_name}")
               else:
                    st.write("No image uploaded yet.")

          left,right = st.columns(2)
          with left:
               name = st.text_input("Change company name here")
               country =  st.text_input("Change company country here")
               accname = st.text_input("Change bank account name here")


          with right:
               address = st.text_input("Change company address here")
               bankname = st.text_input("Change bank name here")
               accnumber = st.text_input("Change bank account number here")

          if st.button("Save Changes"):
               # name,addr,country,bank,accname,accnumber
               # invoicedict = {'name':[name],'addr':[address],'country':[country],'bank':[bankname],'accname':[accname],'accnumber':[accnumber]}
               invoicedict = {}
               if name: #check if name has a data
                    #now get what is in the name variable, assign to a key as the csv and put inside the dict
                    invoicedict['name'] = name
                    #replace an item in a list
                    # numbers[5] = 'yellow'
               else:
                    #get the index position of the name column and assign it to the dict key called name
                    invoicedict['name'] = detailscsv['name'].iloc[0]
               
               if name: #check if name has a data
                    #now get what is in the name variable, assign to a key as the csv and put inside the dict
                    invoicedict['addr'] = address
                    #replace an item in a list
                    # numbers[5] = 'yellow'
               else:
                    #get the index position of the name column and assign it to the dict key called name
                    invoicedict['addr'] = detailscsv['addr'].iloc[0]

               if country:
                    invoicedict['country'] = [country]
               else:
                    invoicedict['country']=detailscsv['country'].iloc[0]
               if bankname:
                    invoicedict['bank'] = [bankname]
               else:
                    invoicedict['bank']=detailscsv['bank'].iloc[0]
               if accname:
                    invoicedict['accname'] = [accname]
               else:
                    invoicedict['accname']=detailscsv['accname'].iloc[0]
               if accnumber:
                    invoicedict['accnumber'] = [accnumber]
               else:
                    invoicedict['accnumber']=detailscsv['accnumber'].iloc[0]


               
               invoicetable = pd.DataFrame(invoicedict)
               invoicetable.to_csv('invoicedetails.csv',index=False)
               st.success("Invoice saved")


if menu == 'Invoice Generator':
     st.sidebar.write("**OPTIONAL**")
     tax = st.sidebar.number_input("Enter tax %",0.0,100.0,step=5.0)
     discount = st.sidebar.number_input("Enter discount %",0.0,100.0,step=5.0)

    

     Image1,Image2,Image3=st.columns([0.5,2.5,1])
     with Image1:
          st.image(imageurl)
     col1,col2=st.columns(2)
     with Image3:
          st.header(":blue[INVOICE]")
     with col1:
          st.write(':blue[Faisaltech]')
          st.write(":blue[471, Camelia 7, Arabian Ranches 8]")
          st.write(':blue[Dubai, UAE]')
          st.write(" ")
          st.write(":blue[**Bill To:**]")


     colb1,colb2,colb3=st.columns([2,1,1])


     with colb1:
          customer = st.text_input('w',placeholder='Customer Name',label_visibility= 'collapsed')
          adress = st.text_input('w',placeholder='Enter Email Address',label_visibility= 'collapsed')  


     with colb2:
          st.write(":blue[**Invoice#:**]")
          st.write('')
          st.write(":blue[**Invoice Date:**]")
          st.write('')
          st.write(":blue[**Due Date:**]")
     with colb3:
          Invoicenum = st.text_input('w',placeholder='Invoice Number',label_visibility= 'collapsed')

          Date=st.date_input("Enter Invoice Date",label_visibility='collapsed')
          day = Date.day #7,9,10
          month = Date.strftime('%b') #December etc %b shortened Dec
          year = Date.year #2021
          Date = f'{day} {month} {year}'

          due=st.date_input("Enter Due Date",label_visibility='collapsed')
          day = due.day
          month = due.strftime('%b')
          year = due.year
          due = f'{day} {month} {year}'


     st.write("")
     st.write("")


     colc1,colc2,colc3,colc4=st.columns(4)
     with colc1:
          st.write(":blue[**Description**]")
          description=st.text_input("f",label_visibility='collapsed')


     with colc2:
          st.write(":blue[**Quantity**]")
          quantity=st.number_input("y",0,label_visibility='collapsed')


     with colc3:
          st.write(":blue[**Price|Unit**]")
          price=st.number_input("s",0,label_visibility='collapsed')

          taxcalc = ((tax/100) * (quantity*price))
          st.write(f":blue[**Tax: ${taxcalc:,}**]") #TAX

# 10% of 50 = 0.1 × 50 = 5
     with colc4:
          st.write(":blue[**Total Price**]")
          totalint = quantity*price
          total=st.text_input("g",value=f'{totalint:,}' ,label_visibility='collapsed',disabled=True)
          

          discountcalc = ((discount/100) * (quantity*price))
          st.write(f":blue[**Discount: ${discountcalc:,}**]") #DISCOUNT
          total=(totalint+taxcalc-discountcalc)
     st.divider()

#calculate the tax and discount percentage and make it show the discount & tax amount in their columns
# also deduct from the sumtotal  yes ke

     cold1,cold2=st.columns(2)
     with cold1:
          st.write(":blue[**Payment Info**]")
          st.write(":blue[Acc Name: Faisaltech]")
          st.write(":blue[Acc Number: 509 173 1594]")
          st.write(":blue[Bank Name: UAE Bank]")
     with cold2:
          st.write(":blue[**Payment Due:**]")
          st.header(f":violet[**${total:,}**]")

#function to generate our PDF

     def generate_pdf():
          pdf = FPDF()

          #Add a page
          pdf.add_page()

          #Set your default fonts
          pdf.set_font("Courier", size=12, style='B')

          #Set column1 x and y coord
          col1x = 10
          col1y = 25

          #Set column width
          colw = 90
          #Set column height
          colh = 10


          #Add image
          pdf.image(imageurl,x=col1x, y=col1y-8,w=25)

          #INVOICE
          pdf.set_font(family='Courier',size=22,style='B')
          pdf.set_xy(col1x+125,col1y+2)
          pdf.cell(colw,colh, txt='INVOICE',ln=True,align='L')


          #FAISALTECH
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+20)
          pdf.cell(colw,colh,txt='Faisaltech',ln=True,align='L')
          

          #ADDRESS
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+30)
          pdf.cell(colw,colh,txt='471, Camelia 7, Arabian Ranches 8',ln=True,align='L')
          
          #COUNTRY
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+40)
          pdf.cell(colw,colh,txt='Dubai, UAE',ln=True,align='L')
          

          #BILL TO
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+70)
          pdf.cell(colw,colh,txt='BILL TO:',ln=True,align='L')
          

          #NAME
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+80)
          pdf.cell(colw,colh,txt=f'{customer}',ln=True,align='L')   

          #EMAIL
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+90)
          pdf.cell(colw,colh,txt=f'{adress}',ln=True,align='L') 

          #INVOICE#
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x+125,col1y+80)
          pdf.cell(colw,colh,txt=f'Invoice#: {Invoicenum}',ln=True,align='L') 

          #INVOICE DATE
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x+125,col1y+90)
          pdf.cell(colw,colh,txt=f'Invoice Date: {Date}',ln=True,align='L') 


          #DESCRIPTION
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+120)
          pdf.cell(colw,colh,txt=f'DESCRIPTION',ln=True,align='L') 


          #QUANTITY
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x+80,col1y+120)
          pdf.cell(colw,colh,txt=f'QUANTITY',ln=True,align='L') 


          #PRICE|UNIT
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x+110,col1y+120)
          pdf.cell(colw,colh,txt=f'PRICE|UNIT',ln=True,align='L') 


          #TOTAL PRICE
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x+145,col1y+120)
          pdf.cell(colw,colh,txt=f'TOTAL PRICE',ln=True,align='L') 


          #LINE
          pdf.set_line_width(0.5) #set the width of the line
          pdf.line(col1x,col1y+130,col1x+190,col1y+130) #startxy and the stopxy

          #DESCRIPTION
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+132)
          pdf.cell(colw,colh,txt=f'{description}',ln=True,align='L') 

          #QUANTITY
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x+85,col1y+132)
          pdf.cell(colw,colh,txt=f'{quantity:,}',ln=True,align='L') 

          #PRICE|UNIT
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x+115,col1y+132)
          pdf.cell(colw,colh,txt=f'{price:,}',ln=True,align='L')


          #TOTAL PRICE
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x+148,col1y+132)
          pdf.cell(colw,colh,txt=f'${total:,}',ln=True,align='L') 

          #Discount
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x+148,col1y+142)
          pdf.cell(colw,colh,txt=f'Discount: ${discountcalc:,}',ln=True,align='L') 

          #TAX
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x+148,col1y+152)
          pdf.cell(colw,colh,txt=f'Tax: ${taxcalc:,}',ln=True,align='L') 

          #PAYMENT INFO
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+175)
          pdf.cell(colw,colh,txt=f'PAYMENT INFORMATION',ln=True,align='L') 


          #ACCOUNT NAME
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+182)
          pdf.cell(colw,colh,txt=f'Acc Name: Faisaltech',ln=True,align='L') 

          #ACCOUNT NUMBER
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+189)
          pdf.cell(colw,colh,txt=f'Acc Number: 509 173 1594',ln=True,align='L') 


          #BANK NAME
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+196)
          pdf.cell(colw,colh,txt=f'Bank Name: UAE Bank',ln=True,align='L') 

          #DUE DATE
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x,col1y+203)
          pdf.cell(colw,colh,txt=f'Pay Before {due}',ln=True,align='L') 


          #PAYMENT DUE
          pdf.set_font("Courier", size=12, style='B')
          pdf.set_xy(col1x+125,col1y+175)
          pdf.cell(colw,colh,txt=f'PAYMENT DUE',ln=True,align='L') 


          #TOTAL DUE
          pdf.set_font("Times", size=18, style='B')
          pdf.set_xy(col1x+125,col1y+195)
          pdf.cell(colw,colh,txt=f'${total:,}',ln=True,align='L') 

          #Save the PDF
          pdf_file = 'invoice.pdf'
          pdf.output(pdf_file)
          return pdf_file

     # Payment Info

     # Acc Name: Faisaltech

     # Acc Number: 509 173 1594

     # Bank Name: UAE Bank



     #Generate the PDF
     pdf_func = generate_pdf()

     #Read the PDF FUNCT as binary data
     with open(pdf_func, 'rb') as binary:
          pdf_data = binary.read()

     but1, but2 = st.columns(2)

     with but1:
          # Display the download button
          if customer and adress and Invoicenum and description and quantity and price and Date and due:
               st.download_button(label=':blue[Download PDF]', data=pdf_data, file_name='faisalinvoice.pdf', mime='application/pdf')
          else:
               st.error('Kindly Fill All Boxes')

     with but1:
          if st.button(":blue[View Invoice]"):
               #Write the PDF using base64
               pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

               #Generate the HTML to embed the PDF
               pdf_embed = f'<embed src="data:application/pdf;base64,{pdf_base64}" type="application/pdf" width="100%" height="600px" />'

               #Display the embedded pdf (Markdown helps us use HTML in streamlit)
               st.markdown(pdf_embed,unsafe_allow_html=True)


