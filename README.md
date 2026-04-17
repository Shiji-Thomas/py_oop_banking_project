# SpringLake Bank - Banking Management System

## Overview

SpringLake Bank is a command-line based banking application that provides core banking functionalities. Customers can perform various banking operations such as opening accounts, checking balances, depositing and withdrawing funds, and closing accounts. The application uses SQL Server as its backend database to persist account information.

## Features

✅ **Open New Account** - Create a new checking or savings account with an initial deposit  
✅ **Check Account Balance** - View the current balance of any account  
✅ **Deposit Funds** - Add money to an existing account  
✅ **Withdraw Funds** - Withdraw money with validation against available balance  
✅ **Close Account** - Delete an account with confirmation  
✅ **User-Friendly Menu** - Interactive command-line interface with input validation  

## System Requirements

- **Python Version**: 3.7 or higher
- **Database**: SQL Server (localhost)
- **Database Name**: SL_Bank_DB
- **ODBC Driver**: ODBC Driver 18 for SQL Server
- **Authentication**: Windows Authentication

## Installation

### 1. Prerequisites
Ensure you have the following installed:
- Python 3.7+
- SQL Server with ODBC Driver 18
- pyodbc library

### 2. Install Dependencies
```bash
pip install pyodbc
```

### 3. Database Setup
Create the SQL Server database and table:

```sql
CREATE DATABASE SL_Bank_DB;

USE SL_Bank_DB;

CREATE TABLE Accounts (
    Account_Number INT PRIMARY KEY IDENTITY(1,1),
    Account_Type NVARCHAR(50),
    Account_Status NVARCHAR(20),
    Account_Curr_Bal FLOAT,
    Customer_Name NVARCHAR(100),
    Cust_Email NVARCHAR(100),
    AC_Created_TS DATETIME
);
```

## Usage

Run the program from the command line:

```bash
python SL_Bank_OOPs.py
```

### Menu Options

1. **Open an Account** - Follow the prompts to enter your name, email, account type, and initial deposit
2. **Account Balance Details** - Enter your account number to view balance
3. **Deposit Amount** - Enter account number and deposit amount
4. **Withdraw Amount** - Enter account number and withdrawal amount (validated against balance)
5. **Close Account** - Confirm and delete your account
6. **Exit** - Terminate the application

## Program Structure

### Main Functions

| Function               | Purpose                                                |
|------------------------|--------------------------------------------------------|
| `SQLSRV_DB_conn_str()` | Establishes connection to SQL Server database          |
| `SL_Bank()`            | Main function displaying menu and routing user actions |
| `open_account()`       | Handles new account creation with initial deposit      |
| `account_balance()`    | Retrieves and displays account balance                 |
| `deposit_amount()`     | Processes deposits and updates account balance         |
| `withdraw_amount()`    | Processes withdrawals with balance validation          |
| `close_account()`      | Deletes account after user confirmation                |

## Database Schema

### Accounts Table

| Column           | Type               | Description                |
|------------------|--------------------|--------------------------- |
| Account_Number   | INT (PK, Identity) | Unique account identifier  |
| Account_Type     | NVARCHAR(50)       | Checking or Savings        |
| Account_Status   | NVARCHAR(20)       | Active/Inactive status     |
| Account_Curr_Bal | FLOAT              | Current account balance    |
| Customer_Name    | NVARCHAR(100)      | Name of account holder     |
| Cust_Email       | NVARCHAR(100)      | Email address              |
| AC_Created_TS    | DATETIME           | Account creation timestamp |

## Security & Validation

- ✓ Input validation for account numbers (must be numeric)
- ✓ Balance validation before withdrawal (cannot exceed available balance)
- ✓ Amount validation (must be numeric and positive)
- ✓ Confirmation prompt for critical operations (account closure)
- ✓ Exception handling for all database operations
- ✓ Secure connection to SQL Server (Windows Authentication)

## UML Class Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    SpringLake Bank Application                  │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
         ┌──────────▼──┐  ┌───────▼─────┐  ┌────▼─────────┐
         │   Database  │  │  User Input │  │ Error Handler│
         │  Connection │  │  Validation │  │              │
         └──────────┬──┘  └─────────────┘  └──────────────┘
                    │
         ┌──────────┴────┌──────────────┌────────────────┌────────────┌
         │               │              │                │            │                                          
    ┌────▼─────┐  ┌──────▼──────┐  ┌────▼──────┐   ┌─────▼─────┐ ┌────▼──────┐
    │ Account  │  │   Account   │  │  Deposit  │   │  Withdraw │ │  close    │
    │ Creation │  │ Balance     │  │ Operations│   │ Operations│ │ account   │
    └────┬─────┘  └─────┬───────┘  └────┬──────┘   └────┬──────┘ └──┬────────┘
         │              │               │               │           │                                            
      ┌──▼──────────────▼───────────────▼───────────────▼──────────▼─┐
      │                  Accounts Table (SQL Server)                 │
      │          ┌──────────────────────────────────────┐            │
      │          │ Account_Number                       │            │
      │          │ Account_Type                         │            │
      │          │ Account_Status                       │            │
      │          │ Account_Curr_Bal                     │            │
      │          │ Customer_Name                        │            │
      │          │ Cust_Email                           │            │
      │          │ AC_Created_TS                        │            │
      │          └──────────────────────────────────────┘            │
      └──────────────────────────────────────────────────────────────┘
```

## Program Flow

```
START
  │
  ├─► Display Welcome Message
  │
  ├─► Enter Menu Loop
  │    │
  │    ├─► [1] Open Account
  │    │    ├─ Input: Name, Email, Type, Initial Amount
  │    │    ├─ Action: INSERT into Accounts table
  │    │    └─ Output: New Account Number
  │    │
  │    ├─► [2] Check Balance
  │    │    ├─ Input: Account Number
  │    │    ├─ Action: SELECT balance from table
  │    │    └─ Output: Current Balance
  │    │
  │    ├─► [3] Deposit
  │    │    ├─ Input: Account Number, Amount
  │    │    ├─ Action: UPDATE balance (+amount)
  │    │    └─ Output: New Balance
  │    │
  │    ├─► [4] Withdraw
  │    │    ├─ Input: Account Number, Amount
  │    │    ├─ Validation: Amount ≤ Current Balance
  │    │    ├─ Action: UPDATE balance (-amount)
  │    │    └─ Output: New Balance
  │    │
  │    ├─► [5] Close Account
  │    │    ├─ Confirmation: User confirms (Y/N)
  │    │    ├─ Action: DELETE from Accounts table
  │    │    └─ Output: Success Message
  │    │
  │    └─► [9] Exit
  │         └─ Terminate Program
  │
  └─► END
```

## Error Handling

The application includes comprehensive error handling for:
- Invalid user inputs
- Non-existent account numbers
- Insufficient balance for withdrawals
- Database connectivity issues
- SQL execution errors

All errors are caught and displayed with descriptive messages to guide the user.

## Example Usage

```
Hi Welcome to SpringLake Bank,

What would you like to do today?
1. Open an Account
2. Account Balance Details
3. Deposit Amount
4. Withdraw Amount
5. Close Account

9. Exit
select an option ( 1 / 2 / 3 / 4 / 5/ 9 )

Enter your option ...: 1
Enter you name: John Doe
Enter you email id: john@example.com
Do you want to open Checking/Saving account: Checking
Amount to deposit for opening Balance: 1000

New Account # 101 for John Doe created
```

## License

This is a sample educational project for banking operations.

## Author Notes

- Ensure SQL Server is running before starting the application
- The application exits after each operation for security (can be modified)
- All monetary amounts should be positive numbers
- Email validation is not enforced at input level

## Disclaimer

Comments and documentation in this program were generated with assistance from GitHub Copilot Chat. 

For more information about the code structure, refer to the inline comments in `SL_Bank_OOPs.py`.
