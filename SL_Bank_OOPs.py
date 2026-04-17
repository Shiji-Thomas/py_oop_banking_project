"""
================================================================================
SPRINGLAKE BANK - BANKING MANAGEMENT SYSTEM
================================================================================

PROGRAM OVERVIEW:
This is a command-line based banking application for SpringLake Bank that 
enables customers to perform various banking operations. The application 
connects to a SQL Server database (SL_Bank_DB) to store and manage customer 
account information persistently.

KEY FEATURES:
1. Open New Account - Create a new checking or savings account with initial deposit
2. View Account Balance - Check the current balance of an existing account
3. Deposit Amount - Add funds to an existing account
4. Withdraw Amount - Withdraw funds from an account with validation checks
5. Close Account - Delete an account from the system with confirmation
6. Exit - Terminate the application

MAIN COMPONENTS:
- SQLSRV_DB_conn_str() - Establishes connection to SQL Server database
- SL_Bank() - Main function that displays menu and routes user actions
- open_account() - Handles new account creation
- account_balance() - Retrieves and displays account balance
- deposit_amount() - Processes deposits and updates balance
- withdraw_amount() - Processes withdrawals with balance validation
- close_account() - Deletes account after user confirmation

DATABASE:
- Server: SQL Server (localhost)
- Database: SL_Bank_DB
- Table: Accounts
  Fields: Account_Number, Account_Type, Account_Status, Account_Curr_Bal,
          Customer_Name, Cust_Email, AC_Created_TS

SECURITY & VALIDATION:
- Input validation for account numbers and amounts
- Balance checks before withdrawal
- Error handling for database operations
- User confirmation prompts for critical operations (account closure)

DISCLAIMER: Comments and documentation in this program were generated with assistance 
from GitHub Copilot Chat.

================================================================================
"""

# Import required libraries for date/time operations, system control, and database connectivity
from datetime import datetime
import sys
import pyodbc

#====================================================================
# Function to establish connection to SQL Server database
def SQLSRV_DB_conn_str():
    # Create connection string with SQL Server credentials and database configuration
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"          
        "DATABASE=SL_Bank_DB;"     
        "Trusted_Connection=yes;"
        "Encrypt=no;"
    )
    # Return the database connection object
    return conn

#====================================================================
# Main function that runs the SpringLake Bank application
def SL_Bank():
    # Display welcome message to the user
    print ("\nHi Welcome to SpringLake Bank,\n")
  
    continue_flag = 'Y'
    # Main menu loop - continues until user chooses to exit
    while continue_flag.upper() == 'Y' or  continue_flag.upper() == 'YES' :
    #while True :
        print("\nWhat would you like to do today?")
        print("1. Open an Account")
        print("2. Account Balance Details")
        print("3. Deposit Amount")
        print("4. Withdraw Amount")
        print('5. Close Account')       

        print('\n9. Exit')        
        

        try:
            # Get user's menu choice
            customer_response = int(input('Enter your option ...: '))

            # Route to appropriate function based on user selection
            if customer_response == 1:
                open_account()
            if customer_response == 2:
                account_balance()
            elif customer_response == 3:
                deposit_amount()
            elif customer_response == 4:
                withdraw_amount()
            elif customer_response == 5:
                close_account()

            # Exit option - terminate the program
            elif customer_response == 9:
                print('THANK YOU for visiting SpringLake Bank!\n')                
                sys.exit()  

            else:
                # Display error message for invalid selection
                #continue_flag = input("Would you like to do another transaction? (Y/N): ")
                print('\nPlease enter a valid option! (1 / 2 / 3 / 4 / 5 / 9)\n')
                

        # Catch any exceptions during menu selection
        except Exception as error:
            print("Invalid input", error)

#====================================================================
# Function to handle opening a new bank account
def open_account():
    try:
        # Collect customer information for new account
        Customer_Name	 = input("Enter you name: ")
        Customer_Email	 = input("Enter you email id: ")
        Account_Type	 = input("Do you want to open Checking/Saving account: ")

        # Get and validate initial deposit amount
        deposit_amt_str = input("Amount to deposit for opening Balance: ")
        if isinstance(float(deposit_amt_str),float) :
            initial_amount = float(deposit_amt_str)
        else:
            initial_amount = float(input("Enter a valid positive amount to deposit: "))
  
        # Connect to database and insert new account record
        conn = SQLSRV_DB_conn_str()
        cursor = conn.cursor()

        # Capture account creation timestamp
        AC_Created_TS=datetime.now()
        # Insert new account with initial balance into Accounts table
        cursor.execute("""INSERT INTO Accounts (Account_Type,Account_Status,Account_Curr_Bal,Customer_Name,Cust_Email,AC_Created_TS)
                       VALUES (?,?,?,?,?,?)  
                       """,(Account_Type,'Active',initial_amount,Customer_Name,Customer_Email,AC_Created_TS))
        conn.commit()

        # Retrieve the newly created account number
        cursor.execute("""SELECT Account_Number FROM Accounts where Customer_Name =? and Cust_Email =? and AC_Created_TS =? """,(Customer_Name,Customer_Email,AC_Created_TS))
        row = cursor.fetchone()
   
        # Display confirmation with new account number
        print('\nNew Account #', row.Account_Number, ' for ', Customer_Name , 'created' ,'\n')      
 
        # Close database connection
        conn.close()
   
    # Handle any errors during account creation
    except Exception as error:
        print("Error while retrieving account balance-", error)

    # Exit after account creation
    #sys.exit()  

#====================================================================
# Function to retrieve and display account balance
def account_balance():
    try:
        # Get and validate account number from user
        ac_str = input("Enter your account number: ")
        if str(ac_str).isdigit():
            account_number = int(ac_str)
        else:
            account_number = int(input("Enter your account number (a valid integer number): "))
 
        # Connect to database
        conn = SQLSRV_DB_conn_str()
        cursor = conn.cursor()

        # Query account balance from database
        cursor.execute("""SELECT Account_Curr_Bal FROM Accounts where Account_Number = ? """,account_number)
        row = cursor.fetchone()

        # Display balance if account exists
        if row:
            print('Account balance of ', account_number , 'as of today is', row.Account_Curr_Bal, '\n')     
        else:
            print("No record found")

    # Handle any errors during balance retrieval
    except Exception as error:
        print("Error while retrieving account balance-", error)

    # Exit after displaying balance
    #sys.exit()  

#====================================================================
# Function to process deposit transactions and update account balance
def deposit_amount():
    try:
        # Get and validate account number
        ac_str = input("Enter your account number: ")
        if str(ac_str).isdigit():
            account_number = int(ac_str)
        else:
            account_number = int(input("Enter your account number (a valid integer number): "))

        # Get and validate deposit amount
        deposit_amt_str = input("Enter amount to deposit: ")
        if isinstance(float(deposit_amt_str),float) :
            deposit_amount = float(deposit_amt_str)
        else:
            deposit_amount = float(input("Enter a valid positive amount to deposit: "))
        
        # Connect to database
        conn = SQLSRV_DB_conn_str()
        cursor = conn.cursor()

        # Update account balance by adding the deposit amount
        cursor.execute("""UPDATE Accounts
                        SET Account_Curr_Bal = Account_Curr_Bal + ?
                        WHERE Account_Number = ? """,(deposit_amount,account_number))
        conn.commit()
   
        # Fetch the updated balance after deposit
        cursor.execute("""SELECT Account_Curr_Bal FROM Accounts where Account_Number = ? """,account_number)
        row = cursor.fetchone()

        # Display confirmation of deposit with new balance
        print('Amount', deposit_amount, 'has been deposited to account ',account_number ,' and new balance is', row.Account_Curr_Bal ,'\n')        

    # Handle any errors during deposit operation
    except Exception as error:
        print("Error while depositing amount-", error)

    # Exit after deposit completion
    #  sys.exit()  

#====================================================================
# Function to process withdrawal transactions with balance validation
def withdraw_amount():  
    try:
        # Get and validate account number
        ac_str = input("Enter your account number: ")
        if str(ac_str).isdigit():
            account_number = int(ac_str)
        else:
            account_number = int(input("Enter your account number (a valid integer number): "))

        # Connect to database and retrieve current balance
        conn = SQLSRV_DB_conn_str()
        cursor = conn.cursor()

        cursor.execute("""SELECT Account_Curr_Bal FROM Accounts where Account_Number = ? """,account_number)
        row = cursor.fetchone()

        # Get and validate withdrawal amount against current balance
        withdraw_amt_str = input("Enter amount to withdraw: ")
        if not isinstance(float(withdraw_amt_str),float) :
           # Prompt again if invalid amount entered
           withdraw_amount = float(input("Enter a valid positive amount to withdraw: "))
        elif float(withdraw_amt_str) > row.Account_Curr_Bal :
           # Ensure withdrawal does not exceed available balance
           withdraw_amount = float(input(f"Enter an amount less than account balance of {row.Account_Curr_Bal}: ") )          
        else:
            withdraw_amount = float(withdraw_amt_str)
        
        # Connect to database again for update operation
        conn = SQLSRV_DB_conn_str()
        cursor = conn.cursor()

        # Update account balance by subtracting the withdrawal amount
        cursor.execute("""UPDATE Accounts                       
                        SET Account_Curr_Bal = Account_Curr_Bal - ?
                        WHERE Account_Number = ? """,(withdraw_amount,account_number))
        conn.commit()
   
        # Fetch the updated balance after withdrawal
        cursor.execute("""SELECT Account_Curr_Bal FROM Accounts where Account_Number = ? """,account_number)
        row = cursor.fetchone()
   
        # Display confirmation of withdrawal with new balance
        print('Amount',withdraw_amount, 'has been withdrawn from account ',account_number ,' and new balance is', row.Account_Curr_Bal ,'\n')      
 
    # Handle any errors during withdrawal operation
    except Exception as error:
        print("Error while withdrawing amount-", error)

    # Exit after withdrawal completion
    #  sys.exit()  

 

#====================================================================
# Function to handle account closure with user confirmation and database deletion
def close_account():
    try:
        # Ask user for confirmation before closing account
        close_flag = input("Are you really sure that you want to close the account (Y/N): ")

        # Proceed with account closure if user confirms
        if close_flag.upper() == 'Y' or  close_flag.upper() == 'YES' :

            # Get and validate account number
            ac_str = input("Enter your account number: ")
            if str(ac_str).isdigit():
                account_number = int(ac_str)                
            else:
                account_number = int(input("Enter your account number (a valid integer number): "))

            # Connect to database
            conn = SQLSRV_DB_conn_str()
            cursor = conn.cursor()

            # Delete the account record from database
            cursor.execute("""DELETE FROM Accounts                       
                            WHERE Account_Number = ? """,account_number)
            conn.commit()
            conn.close()

            # Display success message
            print('Account', account_number, 'has been closed successfully!\n')
        
        else:
            # User opted not to close the account
            print('Account closure cancelled!')

    # Handle any errors during account closure
    except Exception as error:
        print("Error while closing account-", error)

    # Exit after account closure attempt
    #  sys.exit()  

#====================================================================
# Execute the main banking application when script is run directly

if __name__ == '__main__':
    # Start the SpringLake Bank application
    run_application = SL_Bank()