from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from decimal import Decimal

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# MySQL database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',        # Your MySQL username
            password='password', # Your MySQL password
            database='bankdb'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Route to display the home page
@app.route('/')
def index():
    return render_template('index.html')
# Route to login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account_number = request.form['account_number']
        password = request.form['password']

        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT * FROM customers WHERE account_number = %s AND password = %s",
                               (account_number, password))
                user = cursor.fetchone()
                if user:
                    flash("Login successful!")
                    return redirect(url_for('index'))  # Redirect to homepage or dashboard
                else:
                    flash("Invalid account number or password!")
            except Error as e:
                flash(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
    return render_template('login.html')


# Route to create a new user account
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        # Code for processing form submission
        name = request.form['name']
        account_number = request.form['account_number']
        initial_balance = request.form['initial_balance']
        password = request.form['password']

        initial_balance = float(initial_balance)
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Check if account number already exists
                cursor.execute("SELECT * FROM customers WHERE account_number = %s", (account_number,))
                if cursor.fetchone():
                    flash("Account number already exists!")
                    return redirect(url_for('create_account'))
                
                cursor.execute("INSERT INTO customers (name, account_number, balance, password) VALUES (%s, %s, %s, %s)", 
                               (name, account_number, initial_balance, password))
                connection.commit()
                flash(f"Account created successfully for {name} with account number {account_number}!")
                return redirect(url_for('index'))
            except KeyError as e:
                flash(f"Form key error: {e}", "error")
            except ValueError:
                flash("Invalid input for balance. Please enter a valid number.", "error")
            except Exception as e:
                flash(f"Unexpected error: {e}", "error")
            finally:
                cursor.close()
                connection.close()

    # Render the create_account.html template for GET requests
    return render_template('create_account.html')


# Route to view an existing user's details
@app.route('/view_user', methods=['GET', 'POST'])
def view_user():
    if request.method == 'POST':
        account_number = request.form['account_number']
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT * FROM customers WHERE account_number = %s", (account_number,))
                user = cursor.fetchone()
                if user:
                    return render_template('view_user.html', user=user)
                else:
                    flash("User not found!")
            except Error as e:
                flash(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
    
    return render_template('view_user.html')





# Route to  credit an account
@app.route('/credit', methods=['GET', 'POST'])
def credit_account():
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = float(request.form['amount'])

        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Retrieve current balance
                cursor.execute("SELECT balance FROM customers WHERE account_number = %s", (account_number,))
                user = cursor.fetchone()
                if user:
                    # Update balance
                    current_balance = Decimal(user[0])
                    new_balance = current_balance + Decimal(amount)
                    cursor.execute("UPDATE customers SET balance = %s WHERE account_number = %s", 
                                   (new_balance, account_number))
                    cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount, balance) VALUES (%s, %s, %s, %s)",
                                   (account_number, 'Credit', amount, new_balance))
                    connection.commit()
                    flash(f"Successfully credited {amount} to account {account_number}. New balance: {new_balance}")
                    return redirect(url_for('index'))
                else:
                    flash("Account not found!")
            except Error as e:
                flash(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()

    return render_template('credit.html', action="Credit")

# Route to debit an account
''' @app.route('/debit', methods=['GET', 'POST'])
def debit_account():
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = float(request.form['amount'])
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT balance FROM customers WHERE account_number = %s", (account_number,))
                user = cursor.fetchone()
                if user:
                    amount = Decimal(amount)
                    current_balance = Decimal(user[0])
                    if current_balance >= amount:
                        new_balance = current_balance - amount
                        cursor.execute("UPDATE customers SET balance = %s WHERE account_number = %s", 
                                       (new_balance, account_number))
                        cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount, balance) VALUES (%s, %s, %s, %s)",
                                       (account_number, 'Debit', amount, new_balance))
                        connection.commit()
                        flash(f"Successfully debited {amount} from account {account_number}. New balance: {new_balance}")
                        return redirect(url_for('debit.html'))
                    else:
                        flash("Insufficient balance!")
                else:
                    flash("Account not found!")
            except Error as e:
                flash(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()

    return render_template('debit.html', action="Debit")'''
@app.route('/debit', methods=['GET', 'POST'])
def debit_account():
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = float(request.form['amount'])

        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Retrieve current balance
                cursor.execute("SELECT balance FROM customers WHERE account_number = %s", (account_number,))
                user = cursor.fetchone()
                if user:
                    # Update balance
                    current_balance = Decimal(user[0])
                    new_balance = current_balance - Decimal(amount)
                    cursor.execute("UPDATE customers SET balance = %s WHERE account_number = %s", 
                                   (new_balance, account_number))
                    cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount, balance) VALUES (%s, %s, %s, %s)",
                                   (account_number, 'Debit', amount, new_balance))
                    connection.commit()
                    flash(f"Successfully debited {amount} to account {account_number}. New balance: {new_balance}")
                    return redirect(url_for('index'))
                else:
                    flash("Account not found!")
            except Error as e:
                flash(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()

    return render_template('debit.html', action="Debit")

# Route to view balance
# @app.route('/view_balance', methods=['GET', 'POST'])
# def view_balance():
#     if request.method == 'POST':
#         account_number = request.form['account_number']
#         connection = create_connection()
#         if connection:
#             cursor = connection.cursor()
#             try:
#                 # Fetch balance for the provided account number
#                 cursor.execute("SELECT balance FROM customers WHERE account_number = %s", (account_number,))
#                 user = cursor.fetchone()
#                 if user:
#                     return render_template('view_balance.html', balance=user[0])
#                 else:
#                     flash("Account not found!")
#             except Error as e:
#                 flash(f"Error: {e}")
#             finally:
#                 cursor.close()
#                 connection.close()
    
#     return render_template('view_balance.html')




@app.route('/view_balance', methods=['GET', 'POST'])
def view_balance():
    balance = None
    if request.method == 'POST':
        account_number = request.form['account_number']
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Query the balance from the database
                cursor.execute("SELECT balance FROM customers WHERE account_number = %s", (account_number,))
                result = cursor.fetchone()
                if result:
                    balance = result[0]
                else:
                    flash("Account not found!")
            except Error as e:
                flash(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()

    return render_template('view_balance.html', balance=balance)



# Route to view transactions
'''@app.route('/view_transactions', methods=['GET', 'POST'])
def view_transactions():
    if request.method == 'POST':
        account_number = request.form['account_number']
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT * FROM transactions WHERE account_number = %s ORDER BY transaction_date DESC", (account_number,))
                transactions = cursor.fetchall()
                if transactions:
                    return render_template('view_transactions.html', transactions=transactions, account_number=account_number)
                else:
                    flash("No transactions found!")
            except Error as e:
                flash(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
    
    return render_template('view_transactions.html')'''
@app.route('/view_transactions', methods=['GET', 'POST'])
def view_transactions():
    if request.method == 'POST':
        account_number = request.form.get('account_number')  # Use .get() for safer access
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = "SELECT * FROM transactions WHERE account_number = %s ORDER BY transaction_date DESC"
                cursor.execute(query, (account_number,))
                transactions = cursor.fetchall()
                if transactions:
                    return render_template('view_transactions.html', transactions=transactions, account_number=account_number)
                else:
                    flash("No transactions found!")
            except Error as e:
                flash(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()
    
    return render_template('view_transactions.html')


# Route to delete customer account
@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        account_number = request.form['account_number']
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT * FROM customers WHERE account_number = %s", (account_number,))
                user = cursor.fetchone()
                if user:
                    cursor.execute("DELETE FROM transactions WHERE account_number = %s", (account_number,))
                    cursor.execute("DELETE FROM customers WHERE account_number = %s", (account_number,))
                    connection.commit()
                    flash(f"Account {account_number} has been deleted successfully.")
                    return redirect(url_for('index'))
                else:
                    flash("Account not found!")
            except Error as e:
                flash(f"Error: {e}")
            finally:
                cursor.close()
                connection.close()

    return render_template('delete_account.html')

if __name__ == '__main__':
    app.run(debug=True)
print(request.form)
