####************************************
#### HEADER FILE USED IN PROJECT
####************************************

import sys




import tkinter
from PIL import Image,ImageTk
import tkinter.messagebox
from functools import partial
import tkinter.messagebox
import mysql.connector


####************************************

### Defining functions ###

##Button functions (functions which are executed after clicking buttons)

###***************************************************************************
### 1. transaction_fnc executed during the execution of Check_balance_fnc
###    it gives recent transaction details.
###*************************************************************************** 
def transaction_fnc(counter,amount=0,acc_no_receiver=None):
    global transaction    ## DECLARING GLOBAL
    if counter==1:
        #Sending data to sql table
        
        add="INSERT INTO Transaction Values (" +str(userprofile[0])+","+str(acc_no_receiver)+","+str(amount)+",NOW() )"
        cursor3.execute(add)
        connect1.commit()
        cursor3.execute("select* from transaction order by date_time desc")
        transaction=cursor3.fetchall()
    elif counter==2:
        check=0
        a=cursor3.rowcount
        ycord=300
        for x in range(a):
            if check<5:
                tup=transaction[x]
                if tup[0]==userprofile[0] or tup[1]==userprofile[0]:
                    sender_acc=tup[0]
                    receiver_acc=tup[1]
                    amount1=str(tup[2])+' ₹'
                    time=tup[3]
                    lb=tkinter.Label(CBB, text=sender_acc , fg='Black', font=("Times New Roman", 12,"bold")).place(x=140, y=ycord)
                    lb=tkinter.Label(CBB, text=receiver_acc , fg='Black', font=("Times New Roman", 12,"bold")).place(x=300, y=ycord)
                    lb=tkinter.Label(CBB, text=amount1 , fg='Black', font=("Times New Roman", 12,"bold")).place(x=470, y=ycord)
                    lb=tkinter.Label(CBB, text=time , fg='Black', font=("Times New Roman", 12,"bold")).place(x=550, y=ycord)
                    ycord=ycord+20
                    check=check+1


###***************************************************************************
### 2. Check_bank_balance_fnc executed when check balance option is selected
###    in home page it tells balance,credit and debit amount and exectues 
###    transaction_fnc.
###***************************************************************************
def check_bank_balance_fnc():
    global userstatement   #DECLARING GLOBAL
    a=cursor2.rowcount
    x=0
    for x in range(a):
        tup=data_bank_statement[x]
        if userprofile[0]==tup[0]:
            userstatement=tup
    balance=userstatement[1]
    credit=userstatement[2]
    debit=userstatement[3]
    transaction_fnc(counter=2)
    return balance,credit,debit


###***************************************************************************
### 3. amount_fnc executed while sending money from one person to another
###    it tells wheter you have sufficient amount to transfer money or not 
###    and also transfers the money.
###***************************************************************************
def anmount_fnc(amount,acc_no_receiver):
    global data_bank_statement    #DECLARING GLOBAL
    blank="   "*100
    a=int(0)
    a=cursor2.rowcount
    #function to apper msg box after successfully transfering money
    def msg():
        a=tkinter.messagebox.showinfo("Laxmi Cheat Fund",'Money Transfered',parent=FT)
    for x in range(a):
        tup=data_bank_statement[x]
        if userprofile[0]==tup[0]:
            
            if tup[1]<amount:
                lbl=tkinter.Label(FT, text="Insufficient Balance To transfer Money" , fg='red', font=("Times New Roman", 9)).place(x=260,y=290)
            elif tup[1]>=amount:
                lbl=tkinter.Label(FT, text=blank , fg='red', font=("Times New Roman", 9)).place(x=260,y=290)
                #Sending data to sql table
                
                minus="UPDATE bank_statement SET balance = balance - "+str(amount)+",credit_amount=credit_amount + " +str(amount) + " WHERE Account_no=" + str(userprofile[0])
                cursor2.execute(minus)
                plus="UPDATE bank_statement SET balance = balance + "+str(amount)+",debit_amount=debit_amount + " +str(amount) + " WHERE Account_no=" + str(acc_no_receiver)
                cursor2.execute(plus)
                connect1.commit()
                cursor2.execute("select* from bank_statement")
                data_bank_statement=cursor2.fetchall()
                msg()


###***************************************************************************
### 4. transfer_fnc executed while sending money from one person to another
###    it tells wheter you have entered valid account number or not , and also 
###    calls the amount_fnc for execution.
###***************************************************************************
def transfer_fnc(account_entry,amount_entry):
    blank="    "*100
    data1=data_account_detail
    a=int(0)
    x=int(0)
    check=int(0)
    a=cursor1.rowcount
    for x in range (a):
        try:
            acc_no_receiver=int(account_entry.get())
            lbl=tkinter.Label(FT, text=blank , fg='red', font=("Times New Roman", 9)).place(x=260,y=290)
        except ValueError:
            lbl=tkinter.Label(FT, text="Enter Numbers only In Receivers Account Number" , fg='red', 
                              font=("Times New Roman", 9)).place(x=260,y=290)
            break

        try:
            amount=int(amount_entry.get())
            lbl=tkinter.Label(FT, text=blank , fg='red', font=("Times New Roman", 9)).place(x=260,y=290)
        except ValueError:
            lbl=tkinter.Label(FT,text="Enter Numbers only In Amount",fg='red',font=("Times New Roman",9)).place(x=260,y=290)
            break        

        if acc_no_receiver==userprofile[0]:
            lbl=tkinter.Label(FT, text="Don't Enter Your Account Number" , fg='red', font=("Times New Roman", 9)).place(x=260,y=290)
            break
        lbl=tkinter.Label(FT, text=blank , fg='red', font=("Times New Roman", 9)).place(x=260,y=290)
        if amount<0:
            lbl=tkinter.Label(FT, text="Enter valid amount" , fg='red', font=("Times New Roman", 9)).place(x=260,y=290)
            break
        lbl=tkinter.Label(FT, text=blank , fg='red', font=("Times New Roman", 9)).place(x=260,y=290)
        tup=data1[x]
        if acc_no_receiver==tup[0]:
            lbl=tkinter.Label(FT, text=blank , fg='red', font=("Times New Roman", 9)).place(x=260,y=290)
            anmount_fnc(amount,acc_no_receiver)
            check=check+1
            transaction_fnc(1,amount,acc_no_receiver)
        elif x==(a-1) and check==0:
            lbl=tkinter.Label(FT, text="Account Number Dosen't exist" , fg='red', font=("Times New Roman", 9)).place(x=260,y=290)
        

###***************************************************************************
### 5. continue_fnc executed after clicking continue button on home page 
###    it decides which window to open next .
###***************************************************************************
def continue_fnc():
    a=var.get()
    if a==1:
        Check_bank_balance()
    elif a==2:
        Fund_Transfer()
    elif a==3:
        Profile()
        

###***************************************************************************
### 6. login_fnc executes after clicking login button on login page
###    it takes user input of mobile no and password and check wheter they are 
###    valid or not, and open account if they are valid.
###***************************************************************************
def login_fnc(mob_entry,pass_entry):
    global userprofile     #DECLARING GLOBAL
    data1=data_account_detail
    check=0
    blank="   "*100
    a=int(0)
    x=int(0)
    a=cursor1.rowcount
    b=0
    for x in range (a):
        try:
            tup=data1[x]
            mobile_no=int(mob_entry.get())
            password=str(pass_entry.get())
            
        except ValueError:
            lbl=tkinter.Label(mainwindow, text="Enter Number in mobile number" , fg='red', font=("Times New Roman", 6)).place(x=300,y=150)
            break
        lbl=tkinter.Label(mainwindow, text=blank, fg='red', font=("Times New Roman", 6)).place(x=300,y=150)
        if tup[3]==mobile_no and tup[5]==password :
            userprofile=tup
            lbl1=tkinter.Label(mainwindow, text=blank, fg='red', font=("Times New Roman", 6)).place(x=300,y=195)
            check=1
            login_window()
        elif x==a-1 and check==0:
            lbl1=tkinter.Label(mainwindow, text="Invalid password or mobile number" , fg='red', 
                               font=("Times New Roman", 6)).place(x=300,y=195)


###*******************************************************************************
### 7. create_acc_fnc executes after clicking create button on create new account
###    window. it takes input from user and send them in sql table to create 
###    new account.
###*******************************************************************************
def create_acc_fnc(acc_no_entry,name_entry,dob_entry,email_entry,mob_no_entry,pass_entry,confirm_pass_entry):
    global data_account_detail    #DECLARING GLOBAL
    global data_bank_statement    #DECLARING GLOBAL
    blank="   "*100
    check=0
    cond=True
    a=cursor1.rowcount
    lbl=tkinter.Label(create_new_acc, text=blank , fg='red', font=("Times New Roman", 6)).place(x=300,y=313)
    ##function to appear msg box after succesfully creating account
    
    def msg():
        a=tkinter.messagebox.showinfo("Laxmi Cheat Fund",'Account Created Sucessfully',parent=create_new_acc)
    
    while True:
        try:
            name=name_entry.get()
            email=email_entry.get()
            password=pass_entry.get()
            password_confirm=confirm_pass_entry.get()
            dob=int(dob_entry.get())
            acc_no=int(acc_no_entry.get())
            mob_no=int(mob_no_entry.get())
            lbl=tkinter.Label(create_new_acc, text=blank , fg='red', font=("Times New Roman", 6)).place(x=350,y=313)
        except ValueError:
            lbl=tkinter.Label(create_new_acc, text="Enter Valid details" , fg='red', font=("Times New Roman", 6)).place(x=350,y=313)
            break
        
        for x in range(a):
            tup=data_account_detail[x]
            if tup[0]==acc_no:
                lbl=tkinter.Label(create_new_acc, text="account number already registered." , fg='red', 
                                  font=("Times New Roman", 6)).place(x=300,y=313)
                check=0
                break
            elif tup[2]==email:
                lbl=tkinter.Label(create_new_acc, text=" E-mail already registered." , fg='red', 
                                  font=("Times New Roman", 6)).place(x=300,y=313)
                check=0
                break
            elif tup[3]==mob_no:
                lbl=tkinter.Label(create_new_acc, text="Mobile number already registered." , fg='red', 
                                  font=("Times New Roman", 6)).place(x=300,y=313)
                check=0
                break
            elif len(email)>30:
                lbl=tkinter.Label(create_new_acc, text="E-mail id too long." , fg='red', 
                                  font=("Times New Roman", 6)).place(x=300,y=313)
                check=0
                break
            elif len(str(acc_no))>16:
                lbl=tkinter.Label(create_new_acc, text="Max 16 digit account number is allowed." , fg='red', 
                                  font=("Times New Roman", 6)).place(x=300,y=313)
                check=0
                break
            elif len(str(mob_no))>10:
                lbl=tkinter.Label(create_new_acc, text="Mobile Number invalid" , fg='red', 
                                  font=("Times New Roman", 6)).place(x=300,y=313)
                check=0
                break
            elif len(name)>30:
                lbl=tkinter.Label(create_new_acc, text="Name is too long" , fg='red', 
                                  font=("Times New Roman", 6)).place(x=300,y=313)
                check=0
                break
            elif len(password)>20:
                lbl=tkinter.Label(create_new_acc, text="Password too long" , fg='red', 
                                  font=("Times New Roman", 6)).place(x=300,y=313)
                check=0
                break
            else:
                check=1

        dob1=str(dob)

        if check==1:
            
            if dob<10000000 or dob>99999999 or dob1[4:6]<'01' or dob1[4:6]>'12' or dob1[6:8]<'01' or dob1[6:8]>'30' :
                lbl=tkinter.Label(create_new_acc, text="Enter Valid DOB." , fg='red', font=("Times New Roman", 6)).place(x=300,y=313)
                check=1
            else:
                
                check=2
        if check==2:
            if password==password_confirm:
                check=3
            else:
                lbl=tkinter.Label(create_new_acc, text="Enter same password." , fg='red', font=("Times New Roman", 6)).place(x=300,y=313)

        if check==3:
            #Sending data to sql table

            lbl=tkinter.Label(create_new_acc, text=blank , fg='red', font=("Times New Roman", 6)).place(x=300,y=313)
            add="INSERT INTO account_detail(Account_no,name,E_mail,Mobile_No,DOB,Password) VALUES (" + str(acc_no) + "," +"'"+str(name)+"'" + "," +"'"+ email +"'" + "," + str(mob_no) + ","+ str(dob)+"," +"'"+ password+"'"+" )"          
            cursor1.execute(add)
            connect1.commit()
            
            cursor1.execute("select* from account_detail")
            data_account_detail=cursor1.fetchall()
            
            add2="INSERT INTO bank_statement(Account_no,Balance,credit_amount,debit_amount) VALUES (" + str(acc_no)+", 0,0,0)"
            cursor2.execute(add2)
            connect1.commit()
            cursor2.execute("select* from bank_statement")
            data_bank_statement=cursor2.fetchall()
            msg()   
            create_new_acc.destroy()
            break
        break
    
    
#Window function (mains windows)

###***************************************************************************
### 1. Check_bank_balance execute after select check bank balance in home page
###    open check bank balance window 
###***************************************************************************

# main windows
def Check_bank_balance(): 
    global CBB      #DECLARING GLOBAL
    
    CBB=tkinter.Toplevel(mainwindow)
    CBB.geometry("800x450")
    CBB.title("Laxmi Cheat Fund")
    balance,credit,debit=check_bank_balance_fnc() ##calling function
    
    balance1=str(balance)+" ₹"
    debit1="Debit Amount: " +str(debit) +" ₹"
    credit1="Credit Amount: " +str(credit) +" ₹"

    # label widget
    lbl=tkinter.Label(CBB, text="Bank Balance" , fg='Black', font=("Times New Roman", 32,"bold")).place(x=250, y=25)
    lb2=tkinter.Label(CBB, text=balance1 , fg='dimgray', font=("Times New Roman", 24,"bold")).place(x=300, y=80)
    lb3=tkinter.Label(CBB, text="Accumulative:" , fg='Black', font=("Times New Roman", 16,"bold")).place(x=140, y=140)
    lb4=tkinter.Label(CBB ,text=debit1, fg='Black', font=("Times New Roman", 12,"bold")).place(x=160, y=170)
    lb5=tkinter.Label(CBB, text=credit1,fg='Black', font=("Times New Roman", 12,"bold")).place(x=160, y=200)
    lb6=tkinter.Label(CBB, text="Recent Transactions:" , fg='Black', font=("Times New Roman", 16,"bold")).place(x=140, y=250)
    lb7=tkinter.Label(CBB, text="Sender's Account No     Receiver's Account No     Amount     Date and Time" , fg='Black', 
                      font=("Times New Roman", 12,"bold")).place(x=140, y=280)


    # insterting picture
    canvas=tkinter.Canvas(CBB,width=0,height=0)
    canvas.place(x=0,y=0)
    img=ImageTk.PhotoImage(Image.open("arrow3.png"))
    canvas.create_image(00,0,image=img)
    label = tkinter.Label(CBB,image=img)
    label.image =img # keep a reference

    canvas2=tkinter.Canvas(CBB,width=800,height=5)
    canvas2.place(x=100,y=120)
    img2=ImageTk.PhotoImage(Image.open("line1.png"))
    label2=tkinter.Label(CBB,image=img2)
    label2.image=img2
    canvas2.create_image(200,10,image=img2)

    canvas3=tkinter.Canvas(CBB,width=800,height=5)
    canvas3.place(x=100,y=230)
    img3=ImageTk.PhotoImage(Image.open("line1.png"))
    label3=tkinter.Label(CBB,image=img3)
    label3.image=img3
    canvas3.create_image(200,10,image=img3)
    


    #button
    b1=tkinter.Button(CBB,image=img,text="pic",font=("arial",14),bd=0,command=CBB.destroy).place(x=30,y=20)


###***************************************************************************
### 2. Fund_Transfer executes after select transfer money in home page
###    open window to send money to other
###***************************************************************************
def Fund_Transfer():
    global FT       #DECLARING GLOBAL
    FT=tkinter.Toplevel(mainwindow)
    FT.geometry("800x450")
    FT.title("Laxmi Cheat Fund")
    
    acc_no=userprofile[0]
    # label widget
    lbl=tkinter.Label(FT, text="Transfer Money" , fg='Black', font=("Times New Roman", 32,"bold")).place(x=250, y=25)
    lb2=tkinter.Label(FT, text="Your Account Number:" , fg='Black', font=("Times New Roman", 14,"bold")).place(x=140, y=100)
    lb3=tkinter.Label(FT, text=acc_no , fg="dimgray", font=("Times New Roman", 16,"bold")).place(x=140, y=130)
    lb4=tkinter.Label(FT ,text="Receivers Account Number:", fg='Black', font=("Times New Roman", 16,"bold")).place(x=140, y=160)
    lb5=tkinter.Label(FT, text="Amount:",fg='Black', font=("Times New Roman", 16,"bold")).place(x=140, y=220)

    #entry
    account_entry=tkinter.Entry(FT,width=30,fg='Grey',font=("Times New Roman",14))
    account_entry.place(x=140,y=190)
    amount_entry=tkinter.Entry(FT,width=12,fg='Grey',font=("Times New Roman",14))
    amount_entry.place(x=230,y=220)
         
    # insterting picture
    canvas=tkinter.Canvas(FT,width=0,height=0)
    canvas.place(x=0,y=0)
    img=ImageTk.PhotoImage(Image.open("arrow3.png"))
    canvas.create_image(00,0,image=img)
    label = tkinter.Label(FT,image=img)
    label.image =img # keep a reference

    canvas2=tkinter.Canvas(FT,width=800,height=5)
    canvas2.place(x=100,y=80)
    img2=ImageTk.PhotoImage(Image.open("line1.png"))
    label2=tkinter.Label(FT,image=img2)
    label2.image=img2
    canvas2.create_image(200,10,image=img2)

    #button
    b1=tkinter.Button(FT,text="Transfer",bg='green',fg='white',font=("arial",14),activebackground='light green',
                      command=partial(transfer_fnc,account_entry,amount_entry)).place(x=320,y=310)
    b2=tkinter.Button(FT,image=img,text="pic",font=("arial",14),bd=0,command=FT.destroy).place(x=30,y=20)
    

###***************************************************************************
### 3. Check_bank_balance execute after selecting profile in home page
###    open profile window which show all available detail about account 
###***************************************************************************
def Profile():
    global Profile      #DECLARING GLOBAL
    profile=tkinter.Toplevel(mainwindow)
    profile.geometry("800x450")
    profile.title("Laxmi Cheat Fund")
    # label widget
   
    lb=tkinter.Label(profile, text="User Profile" , fg='Black', font=("Times New Roman", 32,"bold")).place(x=280, y=25)
    lb1=tkinter.Label(profile, text="User Name:" , fg='Black', font=("Times New Roman", 16,"bold")).place(x=140, y=110)
    lb2=tkinter.Label(profile, text="Account No:" , fg='Black', font=("Times New Roman", 16,"bold")).place(x=140, y=145)
    lb3=tkinter.Label(profile, text="Date of Birth:" , fg='Black', font=("Times New Roman", 16,"bold")).place(x=140, y=180)
    lb4=tkinter.Label(profile, text="Mobile No:" , fg='Black', font=("Times New Roman", 16,"bold")).place(x=140, y=215)
    lb5=tkinter.Label(profile, text="E-mail ID:" , fg='Black', font=("Times New Roman", 16,"bold")).place(x=140, y=250)
    lb6=tkinter.Label(profile, text="Password:" , fg='Black', font=("Times New Roman", 16,"bold")).place(x=140, y=285)
    acc_no,name,email,mob_no,dob,password=userprofile
    Lb1=tkinter.Label(profile, text=name , fg='Black', font=("Times New Roman", 16,"bold")).place(x=270, y=110)
    Lb2=tkinter.Label(profile, text=acc_no , fg='Black', font=("Times New Roman", 16,"bold")).place(x=270, y=145)
    Lb3=tkinter.Label(profile, text=dob , fg='Black', font=("Times New Roman", 16,"bold")).place(x=270, y=180)
    Lb4=tkinter.Label(profile, text=mob_no , fg='Black', font=("Times New Roman", 16,"bold")).place(x=270, y=215)
    Lb5=tkinter.Label(profile, text=email , fg='Black', font=("Times New Roman", 16,"bold")).place(x=270, y=250)
    Lb6=tkinter.Label(profile, text=password , fg='Black', font=("Times New Roman", 16,"bold")).place(x=270, y=285)
    # insterting picture
    canvas=tkinter.Canvas(profile,width=0,height=0)
    canvas.place(x=0,y=0)
    img=ImageTk.PhotoImage(Image.open("arrow3.png"))
    canvas.create_image(00,0,image=img)
    label = tkinter.Label(profile,image=img)
    label.image =img # keep a reference

    canvas2=tkinter.Canvas(profile,width=800,height=5)
    canvas2.place(x=100,y=80)
    img2=ImageTk.PhotoImage(Image.open("line1.png"))
    label2=tkinter.Label(profile,image=img2)
    label2.image=img2
    canvas2.create_image(200,10,image=img2)

    #button
    b1=tkinter.Button(profile,image=img,text="pic",font=("arial",14),bd=0,command=profile.destroy).place(x=30,y=20)


###***************************************************************************
### 4. login_window opens after succesfully logging in
###    opens home page to select further options
###***************************************************************************
def login_window():
    global login    #DECLARING GLOBAl
    login= tkinter.Toplevel(mainwindow)
    login.geometry("800x450")
    login.title("Laxmi Cheat Fund")
    #Create a Label in New window
    tkinter.Label(login, text="Laxmi Cheat Fund", font=("Times New Roman", 32,  'bold')).place(x=220,y=25)
    
    #adding check box
    global var
    var=tkinter.IntVar()
    R1=tkinter.Radiobutton(login,text="Check bank balance",font=("Times New Roman",16),variable=var,value=1).place(x=250,y=100)
    R2=tkinter.Radiobutton(login,text="Fund Transfer/Transfer money",font=("Times New Roman",16),variable=var,value=2).place(x=250,y=150)
    R3=tkinter.Radiobutton(login,text="Profile",font=("Times New Roman",16),variable=var,value=3).place(x=250,y=200)
    
    
    #adding button
    

    #inserting picture
    canvas=tkinter.Canvas(login,width=0,height=0)
    canvas.place(x=0,y=0)
    img=ImageTk.PhotoImage(Image.open("info2.png"))
    canvas.create_image(0,0,image=img)
    canvas2=tkinter.Canvas(login,width=0,height=0)
    canvas2.place(x=0,y=0)
    img2=ImageTk.PhotoImage(Image.open("arrow3.png"))
    canvas2.create_image(00,0,image=img)
    label = tkinter.Label(login,image=img)
    label.image =img # keep a reference
    label2 = tkinter.Label(login,image=img2)
    label2.image =img2 # keep a referenc

    #defining function
    def msg():
        text='Developed by:\nVikram Sarkar\nUtkarsh Saxena\nNischay Sharma'
        a=tkinter.messagebox.showinfo("Laxmi Cheat Fund",text,parent=login)


    #button
    B1=tkinter.Button(login,text="continue",font=("arial",16),bg='green',fg='white',command=continue_fnc).place(x=290,y=270)
    B2=tkinter.Button(login,image=img,text="pic",font=("arial",14),bd=0,command=msg).place(x=35,y=380)
    b2=tkinter.Button(login,image=img2,text="pic",font=("arial",14),bd=0,command=login.destroy).place(x=30,y=20)


###****************************************************************************************
### 5. create_new_acc_window opens after clicking create new account button on login window
###    open create new account window to create account 
###****************************************************************************************
def create_new_acc_window():
    global create_new_acc     #DECLARING GLOBAL
    create_new_acc=tkinter.Toplevel(mainwindow)
    create_new_acc.geometry("800x450")
    create_new_acc.title("Laxmi Cheat Fund")



    # label widget
    lbl=tkinter.Label(create_new_acc, text="Create New Account" , fg='Black', font=("Times New Roman", 32,"bold")).place(x=220, y=25)
    lb2=tkinter.Label(create_new_acc, text="Account Number:" , fg='Black', font=("Times New Roman", 12,"bold")).place(x=160, y=110)
    lb3=tkinter.Label(create_new_acc, text="Name:" , fg='Black', font=("Times New Roman", 12,"bold")).place(x=160, y=140)
    lb4=tkinter.Label(create_new_acc, text="Date of Birth:" , fg='Black', font=("Times New Roman", 12,"bold")).place(x=160, y=170)
    lb5=tkinter.Label(create_new_acc, text="E-mail ID:" , fg='Black', font=("Times New Roman", 12,"bold")).place(x=160, y=200)
    lb6=tkinter.Label(create_new_acc, text="Mobile No.:" , fg='Black', font=("Times New Roman", 12,"bold")).place(x=160, y=230)
    lb7=tkinter.Label(create_new_acc, text="Password:" , fg='Black', font=("Times New Roman", 12,"bold")).place(x=160, y=260)
    lb8=tkinter.Label(create_new_acc, text="Confirm Password:" , fg='Black', font=("Times New Roman", 12,"bold")).place(x=160, y=290)

    #entry
    acc_no_entry=tkinter.Entry(create_new_acc,width=30,fg='Black',font=("Times New Roman",12))
    acc_no_entry.place(x=300,y=110)
    name_entry=tkinter.Entry(create_new_acc,width=30,fg='Black',font=("Times New Roman",12))
    name_entry.place(x=300,y=140)
    dob_entry=tkinter.Entry(create_new_acc,width=30,fg='Black',font=("Times New Roman",12))
    dob_entry.insert(12,"YYYY/MM/DD")
    dob_entry.place(x=300,y=170)
    email_entry=tkinter.Entry(create_new_acc,width=30,fg='Black',font=("Times New Roman",12))
    email_entry.place(x=300,y=200)
    mob_no_entry=tkinter.Entry(create_new_acc,width=30,fg='Black',font=("Times New Roman",12))
    mob_no_entry.place(x=300,y=230)
    pass_entry=tkinter.Entry(create_new_acc,width=30,fg='Black',font=("Times New Roman",12))
    pass_entry.place(x=300,y=260)
    confirm_pass_entry=tkinter.Entry(create_new_acc,width=30,fg='Black',font=("Times New Roman",12))
    confirm_pass_entry.place(x=300,y=290)
    # insterting picture
    canvas=tkinter.Canvas(create_new_acc,width=0,height=0)
    canvas.place(x=0,y=0)
    img=ImageTk.PhotoImage(Image.open("arrow3.png"))
    canvas.create_image(00,0,image=img)
    label = tkinter.Label(create_new_acc,image=img)
    label.image =img # keep a reference



    #button
    b1=tkinter.Button(create_new_acc,text="Create account",bg='green',fg='white',font=("arial",14),activebackground='light green',
                      command=partial(create_acc_fnc,acc_no_entry,name_entry,dob_entry,email_entry,mob_no_entry,
                                      pass_entry,confirm_pass_entry)).place(x=320,y=330)
    b2=tkinter.Button(create_new_acc,image=img,text="pic",font=("arial",14),bd=0,command=create_new_acc.destroy).place(x=30,y=20)

    
    
###********************************************************************************
### 7. main_window main function of the program executes just after running the 
###    program, it opens login window which allows further operation to take place 
###********************************************************************************
def main_window():
    global mainwindow       #DECLARING GLOBAL
    mainwindow=tkinter.Tk()
    # add widgets here

    mainwindow.title('Banking management system')
    mainwindow.geometry("800x450")
    
    # label widget
    lbl=tkinter.Label(mainwindow, text="Laxmi Cheat Fund" , fg='Black', font=("Times New Roman", 32,"bold"))
    lbl.place(x=220, y=25)

    #inserting entry
    mob_entry=tkinter.Entry(mainwindow,fg='black',font=("Times New Roman",12))
    mob_entry.insert(10,"Mobile Number")
    mob_entry.place(x=300,y=120)

    pass_entry=tkinter.Entry(mainwindow,fg='black',font=("Times New Roman",12))
    pass_entry.insert(10,"Password")
    pass_entry.place(x=300,y=170)

    # insterting picture
    canvas=tkinter.Canvas(mainwindow,width=800,height=5)
    canvas.place(x=120,y=270)
    img=ImageTk.PhotoImage(Image.open("line1.png"))
    canvas.create_image(200,10,image=img)

  
    # intsert button
    b1=tkinter.Button(mainwindow,text="Login",bg="sky blue",font=("arial",14),fg="white",activebackground="Light blue",
                      command=partial(login_fnc,mob_entry,pass_entry))
    b1.place(x=345,y=220)

    b2=tkinter.Button(mainwindow ,text="Create New Account",bg="green",font=("arial",14),fg="white",activebackground="light green",
                      command=create_new_acc_window)
    b2.place(x=290,y=310)

    mainwindow.mainloop()


###***************************************************************************
### 1. connector_function connects mysql with python
###***************************************************************************
def connector_function():
    connect1=mysql.connector.connect(host="localhost",user="root",passwd='raaj0420',database="banking_management_system")
    return connect1

connect1 = connector_function()
if connect1.is_connected()==False:
    print("error")
cursor1=connect1.cursor()

#### Taking data from all the tables present in banking_management_system database
cursor1.execute("select* from account_detail")
data_account_detail=cursor1.fetchall()

cursor2=connect1.cursor()
cursor2.execute("select* from bank_statement")
data_bank_statement=cursor2.fetchall()

cursor3=connect1.cursor()
cursor3.execute("select* from transaction order by time desc")
transaction=cursor3.fetchall()

main_window()
connect1.close()

