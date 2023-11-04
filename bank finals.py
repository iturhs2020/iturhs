import mysql.connector
from datetime import datetime
import random

# Establish a connection to the MySQL database
mydb = mysql.connector.connect(host='localhost', user='root', password='1810')
mycon = mydb.cursor()

# Create the 'bank' database if it doesn't exist
mycon.execute("CREATE DATABASE IF NOT EXISTS bank")
mycon.execute("USE bank")

# Create the 'accounts' table to store account information
mycon.execute('''CREATE TABLE IF NOT EXISTS accounts (
    ACCOUNT_NO CHAR(5) PRIMARY KEY,
    USERNAME VARCHAR(40) UNIQUE,
    PASSWORD VARCHAR(30) NOT NULL)''')

# Create the 'Trans_history' table to store transaction history
mycon.execute('''CREATE TABLE IF NOT EXISTS Trans_history (
    ACCOUNT_NO CHAR(5),
    TRANS_DATE TIMESTAMP,
    DEPOSIT INT,
    WITHDRAW INT,
    BALANCE INT NOT NULL,
    FOREIGN KEY (ACCOUNT_NO) REFERENCES accounts(ACCOUNT_NO))''')

# Create the 'customer' table to store customer details
mycon.execute('''create table if not exists customer(
        ACCOUNT_NO char(5) PRIMARY KEY,  
        NAME varchar(150),
        DOB date,
        PHONE_NUMBER varchar(12),
        ADDRESS varchar(60),
        BALANCE int,
        FOREIGN KEY (ACCOUNT_NO) REFERENCES accounts(ACCOUNT_NO))''')

# Define a global variable for the account number
global ACCOUNT_NO

# Function to generate a random account number
def gen_accnum():
    p = random.randint(1000, 9999)
    mycon.execute('SELECT ACCOUNT_NO FROM accounts')
    acc1 = mycon.fetchall()
    mydb.commit()
    acc2 = []
    for i in range(len(acc1)):
        acc2.append(acc1[i][0])
    if p in acc2:
        p = random.randint(1000, 9999)
    return p

# Function to input a phone number
def phn():
    while True:
        ph = int(input('Enter your Phone number (10 digits): '))
        phns = str(ph)
        if len(phns) != 10:
            print('Invalid phone number. Please enter a 10-digit phone number.')
        else:
            return phns

# Function to get the opening balance
def getbal():
    while True:
        amt = int(input('Enter the opening balance (at least Rs. 1000): '))
        if amt < 1000:
            print('Low balance. Please enter a balance of at least Rs. 1000')
        else:
            return amt

# Function to create a new bank account
def create_account():
    try:
        dat = datetime.now()
        ACC = gen_accnum()
        USERNAME = input('Enter your username: ')
        PASSWORD = input('Enter your password: ')
        sql = "INSERT INTO accounts (ACCOUNT_NO, USERNAME, PASSWORD) VALUES (%s, %s, %s)"
        val = (ACC, USERNAME, PASSWORD)
        mycon.execute(sql, val)
        print('Your account number with the username', USERNAME, 'has been created. Your account number is', ACC)
        mydb.commit()

        # Collect customer details
        print('Enter the account holder\'s details:')
        nm = input('Name: ')
        dob = input('Date of Birth (yyyy-mm-dd): ')
        add = input('Address: ')
        phno = phn()
        print()
        print('Minimum balance to be entered is Rs. 1000')
        bal = getbal()

        # Insert customer details
        sql2 = 'INSERT INTO customer(ACCOUNT_NO, NAME, DOB, PHONE_NUMBER, ADDRESS, BALANCE) VALUES (%s, %s, %s, %s, %s, %s)'
        val2 = (ACC, nm, dob, phno, add, bal)
        mycon.execute(sql2, val2)

        # Insert initial transaction history
        sql3 = 'INSERT INTO Trans_history(ACCOUNT_NO, TRANS_DATE, DEPOSIT, WITHDRAW, BALANCE) VALUES (%s, %s, %s, %s, %s)'
        val3 = (ACC, dat, 0, 0, bal)
        mycon.execute(sql3, val3)
        mydb.commit()
        print(mycon.rowcount, 'record inserted')
        print('Please log in to your account to modify details')
    except mysql.connector.Error as e:
        print('An error occurred:', e)

# Function to display the main menu
def main_menu():
    print('\t\t\t\t_______________________________________________________')
    print('\t\t\t\t_-------------------------ABC BANK--------------------------')
    print('\t\t\t\t________________________________________________________')
    print()
    print('YOUR TRUSTED FINANCIAL PARTNER')
    print()
    while(1):
        print()
        print('MENU')
        print('1. Create New Account in Bank')
        print('2. Login to Your Account')
        print('3. Exit')
        print()
        ch = int(input('Enter your choice to proceed further: '))
        print()
        if ch == 1:
            create_account()
        elif ch == 2:
            login_account()
        elif ch == 3:
            exit()
        else:
            print('Invalid choice')

# Function to display the login menu
def login_menu():
    print()
    print('MENU')
    print('1. Deposit Money')
    print('2. Withdraw Money')
    print('3. View Transaction History')
    print('4. View Account Details')
    print('5. Modify Account Details')
    print('6. Exit')
    print()

# Function to handle user login
def login_account():
    try:
        ACCOUNT_NO = input('Enter your account number: ')
        USERNAME = input('Enter your username: ')
        PASSWORD = input('Enter your password: ')

        mycon.execute('SELECT ACCOUNT_NO FROM accounts')
        acc1 = mycon.fetchall()
        mydb.commit()
        acc2 = [item[0] for item in acc1]

        mycon.execute('SELECT username FROM accounts')
        user1 = mycon.fetchall()
        mydb.commit()
        user2 = [item[0] for item in user1]

        mycon.execute('SELECT password FROM accounts')
        pd1 = mycon.fetchall()
        pd2 = [item[0] for item in pd1]
        mydb.commit()

        if (USERNAME not in user2) or (PASSWORD not in pd2) and (ACCOUNT_NO not in acc2):
            print('Incorrect username, password, or account number')
            f = 1
            while True:
                f = int(input('Press 1 to try again\nPress 2 to exit: '))
                if f == 1:
                    login_account()
                else:
                    exit()
        else:
            mycon.execute("SELECT PASSWORD FROM accounts WHERE USERNAME = %s", (USERNAME,))
            pd = mycon.fetchone()
    except mysql.connector.Error as e:
        print('An error occurred:', e)

    print('Login successful')
    print()

    while True:
        login_menu()
        ch = int(input('Enter your choice to proceed further: '))
        print()

        if ch == 1:
            deposit(ACCOUNT_NO)
        elif ch == 2:
            withdraw(ACCOUNT_NO)
        elif ch == 3:
            trans_hisview(ACCOUNT_NO)
        elif ch == 4:
            viewacc_det(ACCOUNT_NO)            
        elif ch == 5:            
            modaccdet(ACCOUNT_NO)
        elif ch == 6:
            exit()
        else:
            print('Invalid choice')

# Function to deposit money into an account
def deposit(ACCOUNT_NO):
    try:
        dat = datetime.now()
        dep = int(input('Enter deposit amount:'))
        v = 'SELECT BALANCE FROM Trans_history WHERE ACCOUNT_NO = %s ORDER BY TRANS_DATE DESC'
        mycon.execute(v, (ACCOUNT_NO,))
        r = mycon.fetchall()
        o = r[0][0]
        t = o + dep

        print('Current balance:', t)

        # Update the balance in the 'Trans_history' table
        sql = 'INSERT INTO Trans_history(ACCOUNT_NO, TRANS_DATE, DEPOSIT, WITHDRAW, BALANCE) VALUES(%s, %s, %s, %s, %s)'
        val = (ACCOUNT_NO, dat, dep, 0, t)
        mycon.execute(sql, val)

        # Update the balance in the 'customer' table
        sql = 'UPDATE customer SET BALANCE = %s WHERE ACCOUNT_NO = %s'
        val = (t, ACCOUNT_NO)
        mycon.execute(sql, val)

        mydb.commit()
    except mysql.connector.Error as e:
        print('An error occurred:', e)

# Function to withdraw money from an account
def withdraw(ACCOUNT_NO):
    try:
        dat = datetime.now()
        wit = int(input('Enter withdrawal amount:'))
        v = 'SELECT BALANCE FROM Trans_history WHERE ACCOUNT_NO = %s ORDER BY TRANS_DATE DESC'
        mycon.execute(v, (ACCOUNT_NO,))
        r = mycon.fetchall()
        o = r[0][0]

        if wit > o:
            print('Withdrawal failed. Insufficient funds.')
        else:
            k = o - wit
            print('Withdrawal successful. Current balance:', k)

            # Update the balance in the 'Trans_history' table
            sql = 'INSERT INTO Trans_history(ACCOUNT_NO, TRANS_DATE, DEPOSIT, WITHDRAW, BALANCE) VALUES(%s, %s, %s, %s, %s)'
            val = (ACCOUNT_NO, dat, 0, wit, k)
            mycon.execute(sql, val)

            # Update the balance in the 'customer' table
            sql = 'UPDATE customer SET BALANCE = %s WHERE ACCOUNT_NO = %s'
            val = (k, ACCOUNT_NO)
            mycon.execute(sql, val)

            mydb.commit()
    except mysql.connector.Error as e:
        print('An error occurred:', e)

# Function to modify account details
def modaccdet(ACCOUNT_NO):
    print('Modify Account Details for Account:', ACCOUNT_NO)
    try:
        mycon.execute("SELECT * FROM customer WHERE ACCOUNT_NO = %s", (ACCOUNT_NO,))
        acc_data = mycon.fetchone()

        if not acc_data:
            print('Account not found.')
            return

        while True:
            print()
            print('Select the field you want to modify:')
            print('1. Name')
            print('2. Date of Birth')
            print('3. Phone Number')
            print('4. Address')
            print('5. Go back to the main menu')

            ch = int(input('Enter your choice: '))
            
            if ch == 1:
                new_value = input('Enter the new name: ')
                field_name = 'NAME'
            elif ch == 2:
                new_value = input('Enter the new date of birth (yyyy-mm-dd): ')
                field_name = 'DOB'
            elif ch == 3:
                new_value = input('Enter the new phone number: ')
                field_name = 'PHONE_NUMBER'
            elif ch == 4:
                new_value = input('Enter the new address: ')
                field_name = 'ADDRESS'
            elif ch == 5:
                mydb.commit()
                print('Account details updated successfully.')
                return
            else:
                print('Invalid choice. Please select a valid option.')
                continue

            mycon.execute(f"UPDATE customer SET {field_name} = %s WHERE ACCOUNT_NO = %s", (new_value, ACCOUNT_NO))
            print('Details updated successfully')
            mydb.commit()
    except mysql.connector.Error as e:
        print('An error occurred:', e)

# Function to view transaction history
def trans_hisview(ACCOUNT_NO):
    print('Transaction History for Account:', ACCOUNT_NO)
    try:
        sql = 'SELECT TRANS_DATE, DEPOSIT, WITHDRAW, BALANCE FROM Trans_history WHERE ACCOUNT_NO = %s ORDER BY TRANS_DATE DESC'
        mycon.execute(sql, (ACCOUNT_NO,))
        transactions = mycon.fetchall()
        for trans in transactions:
            trans_date, deposit, withdraw, balance = trans
            print(f'Transaction Date: {trans_date}')
            print(f'Deposit: {deposit}')
            print(f'Withdraw: {withdraw}')
            print(f'Balance: {balance}')
            print()
    except mysql.connector.Error as e:
        print('An error occurred:', e)

# Function to view account details
def viewacc_det(ACCOUNT_NO):
    try:
        mycon.execute('''SELECT c.ACCOUNT_NO, c.NAME, c.ADDRESS, c.DOB, c.BALANCE, a.PASSWORD
        FROM customer c INNER JOIN accounts a ON c.ACCOUNT_NO = a.ACCOUNT_NO WHERE c.ACCOUNT_NO = %s''', (ACCOUNT_NO,))
        account_details = mycon.fetchone()

        if not account_details:
            print('Account not found.')
            return

        account_no, name, address, dob, balance, password = account_details

        print('Account Number:', account_no)
        print('Name:', name)
        print('Address:', address)
        print('Date of Birth:', dob)
        print('Current Balance:', balance)
        print('Password:', password)

    except mysql.connector.Error as e:
        print('An error occurred:', e)

# Start the main menu
main_menu()
