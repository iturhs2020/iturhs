import mysql.connector
from datetime import date
import random
#database connection 
mydb=mysql.connector.connect(host='localhost',user='root',password='1810')
mycon=mydb.cursor()   #cursor

def accno():
    p=random.randint(1000,9999)
    mycon.execute('select ACCOUNT_NO from accounts')
    acc1=mycon.fetchall()
    mydb.commit()
    acc2=[]
    for i in range (len(acc1)):
        acc2.append(acc1[i][0])
    if p in acc2:
        p=random.randint(1000,9999)
    return p



mycon.execute("create database  if not exists bank")
mycon.execute("use bank")   #database bank 
#create accounts table
mycon.execute('''create table if not exists accounts (ACCOUNT_NO  char(5) PRIMARY KEY ,
USERNAME varchar(40) UNIQUE,
PASSWORD varchar(30) NOT NULL)''')
mycon.execute('''create table if not exists Trans_history(ACCOUNT_NO char(5) PRIMARY KEY ,
TRANS_DATE date,
DEPOSIT int,
WITHDRAW int,
BALANCE int NOT NULL,
FOREIGN KEY (ACCOUNT_NO) REFERENCES accounts(ACCOUNT_NO))''')
global UNIQUE_NO

def phn():
    ph=int(input('Enter Phone number :'))
    phns=str(ph)
    if len(phns)!=10:
        print('Phone Number entered is invalid . Try again')
        phn()
    return phns

def ba():
    amt=int(input('Enter opening Balance :'))
    if amt<1000:
        print('\n LOW BALANCE . ENTER BALANCE MORE THAN Rs.1000')
        ba()
    return amt

#CREATE ACCOUNT 
def cracc():
    dat=date.today()
    ACC=accno()
    USERNAME=input('ENTER USERNAME: ')
    PASSWORD=input('ENTER PASSWORD: ')
    sql = "INSERT INTO accounts (ACCOUNT_NO,USERNAME ,PASSWORD) VALUES (%s, %s,%s)"
    val= (ACC,USERNAME,PASSWORD ) #insert value in customer 
    mycon.execute(sql,val)
    print('Your account number with username',USERNAME,'is',ACC)
    mydb.commit()

    print(mycon.rowcount,'record inserted')
    mycon.execute('use bank ')
    #create table customer 
    mycon.execute('''create table if not exists customer(
    ACCOUNT_NO char(5) PRIMARY KEY,  
    NAME varchar(150),
    DOB date,
    PHONE_NUMBER varchar(12),
    ADDRESS varchar(60),
    BALANCE int,
    FOREIGN KEY (ACCOUNT_NO) REFERENCES accounts(ACCOUNT_NO))''')

    nm=input('ENTER ACCOUNT HOLDER''S NAME :')
    dob=input('ENTER DATE OF BIRTH IN FORMAT yyyy-mm-dd: ')
    add=input('ENTER YOUR ADDRESS: ')
    phno=phn()
    print('\n Minimum balance to be entered is Rs 1000 \n')
    bal=ba()
    sql2='insert into customer(ACCOUNT_NO,NAME,DOB,PHONE_NUMBER,ADDRESS,BALANCE) values (%s,%s,%s,%s,%s,%s)'
    val2=(ACC,nm,dob,phno,add,bal)           
    mycon.execute(sql2,val2)
    
    sql3='''insert into Trans_history(ACCOUNT_NO,TRANS_DATE, DEPOSIT,WITHDRAW, BALANCE) values(%s,%s,%s,%s,%s)'''
    val3=(ACC,dat,0,0,bal)
    mycon.execute(sql3,val3)
    mydb.commit()
    print(mycon.rowcount,'record inserted')
    print('Login your account to modify  details') 

#LOGIN ACCOUNT 
def logac():
    USERNAME=input('Enter Username : ')
    PASSWORD=input('Enter password : ')
    mycon=mydb.cursor()
    mycon.execute('select username from accounts')
    user1=mycon.fetchall()
    mydb.commit()
    user2=[]
    for i in range (len(user1)):
        user2.append(user1[i][0])

    mycon=mydb.cursor()
    mycon.execute('select password from accounts')
    pd1=mycon.fetchall()
    pd2=[]
    for i in range (len(pd1)):
        pd2.append(pd1[i][0])
    mydb.commit()

    if (USERNAME not in  user2) or (PASSWORD not in pd2 ):
        print('Wrong username or password')
        f=1
        while True:
            f=int(input('Press 1 to try again \n Press 2 for exit : '))
            if f==1:
                logac()
            else:
                exit()
    else:
        mycon=mydb.cursor()
        mycon.execute("Select password from accounts where USERNAME={0}".format(USERNAME))
        pd=mycon.fetchone()

        print('\t\t\t---------------------*****LOGIN SUCCESFULLY*****--------------------')

        #MENU 2

#MENU 1
def menu1():
    print('\t\t\t\t_______________________________________________________')
    print('\t\t\t\t-------------------------BANK--------------------------')
    print('\t\t\t\t_______________________________________________________')
    print()
    print()
    while(1):
        print()
        print('MENU')
        print('PRESS 1 TO CREATE NEW ACCOUNT IN BANK ')
        print('PRESS 2 TO LOGIN ACCOUNT')
        print('PRESS 3 TO EXIT ')
        print()
        ch=int(input('ENTER YOUR CHOICE TO PROCEED FURTHER: '))
        print()

        if ch==1:
            cracc()
        elif ch==2:
            logac()

        elif ch==3:
            exit()
        else:
            print('INVALID CHOICE ')

menu1()