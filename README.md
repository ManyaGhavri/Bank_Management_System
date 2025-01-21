# 💸Bank Management System

This project is a web-based **Bank Management System** built using **Flask**, a Python microframework, **MySQL** as the database, and **HTML/CSS** for the frontend. It allows users to perform banking operations such as account creation, login, balance inquiry, money credit and debit, viewing transactions, and deleting accounts.

---

## 🌟Features

### 1. **User Authentication**
   - Login functionality for customers using their account number and password.
   - Ensures security with a session-based approach using a secret key.

### 2. **Account Management**
   - **Create Account**: Users can create a new account with an initial balance and password.
   - **Delete Account**: Delete an existing account along with its transaction history.

### 3. **Transactions**
   - **Credit Account**: Deposit money into a specific account.
   - **Debit Account**: Withdraw money from an account, ensuring sufficient balance.
   - **View Transactions**: Retrieve the history of all transactions for a given account, ordered by the most recent.

### 4. **Balance Inquiry**
   - Allows users to check the current balance of their account.

### 5. **Frontend with HTML and CSS**
   - The application includes user-friendly interfaces built with **HTML** for structure and **CSS** for styling.
   - Responsive design ensures compatibility across various devices.

### 6. **Website Preview**
   - Below are screenshots of the website's main pages to give you a quick preview of the interface:
     - **Home Page**
       ![Home Page](screenshots/home_page.png)
     - **Login Page**
       ![Login Page](screenshots/login_page.png)
     - **Account Creation Page**
       ![Create Account Page](screenshots/create_account_page.png)
     - **Transaction Page**
       ![Transaction Page](screenshots/transaction_page.png)

---

## 📚Prerequisites

- **Python 3.x** installed on your system.
- **MySQL Server** installed and configured.
- Required Python libraries (see installation section below).
- Basic knowledge of **HTML/CSS** if you wish to customize the frontend.

---

## ⚙️Installation and Setup

### 1. **Clone the Repository**
```bash
$ git clone <repository-url>
$ cd bank-management-system
```

### 2. **Install Dependencies**
Install required Python libraries using `pip`:
```bash
$ pip install flask mysql-connector-python
```

### 3. **Set Up the Database**
   - Create a database in MySQL:
     ```sql
     CREATE DATABASE bankdb;
     ```
   - Create the required tables:
     ```sql
     CREATE TABLE customers (
         id INT AUTO_INCREMENT PRIMARY KEY,
         name VARCHAR(100),
         account_number VARCHAR(20) UNIQUE,
         balance DECIMAL(15, 2),
         password VARCHAR(100)
     );

     CREATE TABLE transactions (
         id INT AUTO_INCREMENT PRIMARY KEY,
         account_number VARCHAR(20),
         transaction_type VARCHAR(10),
         amount DECIMAL(15, 2),
         balance DECIMAL(15, 2),
         transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         FOREIGN KEY (account_number) REFERENCES customers(account_number)
     );
     ```

### 4. **Run the Application**
   - Start the Flask application:
     ```bash
     $ python app.py
     ```
   - Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🗂️File Structure

- **app.py**: The main application file containing all the routes and logic.
- **templates/**: Directory containing HTML templates for the frontend.
  - `index.html`: Home page template.
  - `login.html`: Login page template.
  - `create_account.html`: Template for creating a new account.
  - `view_user.html`: Template for viewing user details.
  - `credit.html`: Template for crediting an account.
  - `debit.html`: Template for debiting an account.
  - `view_balance.html`: Template for checking account balance.
  - `view_transactions.html`: Template for viewing transaction history.
  - `delete_account.html`: Template for deleting an account.
- **static/**: Directory containing CSS files for styling the frontend.
  - `styles.css`: Main stylesheet for the application.
- **screenshots/**: Directory containing screenshots of the website pages.

---

## 🔒Security Considerations
- **Password Storage**: Passwords are stored in plaintext in this implementation. For a production-grade system, ensure passwords are hashed using libraries like `bcrypt` or `argon2`.
- **SQL Injection Prevention**: Use parameterized queries to prevent SQL injection attacks.
- **Session Management**: Use secure session handling and consider implementing user roles and authentication tokens.

---

## 🚀Future Enhancements

1. **Enhanced Security**
   - Implement password hashing.
   - Add account locking after multiple failed login attempts.

2. **Admin Panel**
   - Allow administrators to manage accounts and transactions.

3. **Reports**
   - Generate reports for customers, accounts, and transactions.

4. **REST API Integration**
   - Provide a RESTful API for mobile and external integrations.

5. **UI Improvements**
   - Use a modern frontend framework like React or Vue.js for a better user experience.

---

## 👩‍💻Developer
- **Manya Ghavri**
- 🌐 [GitHub Profile](https://github.com/ManyaGhavri)  
- 📧 Email: manyaghavri3211@gmail.com
- 🔗 LinkedIn: [Linkedin_link](https://www.linkedin.com/in/manya-ghavri-b00773310/)
