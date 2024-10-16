from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import pandas as pd

app = Flask(__name__)

# Initialize SQLite database.
def init_db():
    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS expenses 
                   (Date TEXT, Description TEXT, Category TEXT, Price REAL)''')
    conn.commit()
    conn.close()

# Create index route.
@app.route('/')
def index():
    return render_template('index.html')

# Create route to add expenses to DB manually.
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    # Handles form submissions.
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        
        # Connect to database and insert from form into database.
        conn = sqlite3.connect('expenses.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO expenses (Date, Description, Category, Price) VALUES (?, ?, ?, ?)",
                    (date, description, category, price))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add.html')

# Create finances summary route.
@app.route('/summary', methods=['GET', 'POST'])
def view_summary():
    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()

    # Choose time month and year for summary.
    if request.method == 'POST':
        month = request.form['month']
        year = request.form['year']
        cur.execute("SELECT * FROM expenses WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?", (month, year))
        expenses = cur.fetchall()
        cur.execute("SELECT SUM(Price) FROM expenses WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?", (month, year))
        total_expense = cur.fetchone()[0]
    # If not POST then retrieve sum of prices and stores in total.
    else:
        cur.execute("SELECT * FROM expenses")
        expenses = cur.fetchall()
        cur.execute("SELECT SUM(Price) FROM expenses")
        total_expense = cur.fetchone()[0]

    conn.close()
    
    return render_template('summary.html', expenses=expenses, total=total_expense)

# Create a route to search.
@app.route('/search')
def search():
    return render_template('search.html')

# Create a route to upload csv from Bank of America.
@app.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        # Use pandas to read csv, skip unnecessary rows, iterate through and grab relevant data for local database.
        if file:
            df = pd.read_csv(file, skiprows=5)
            conn = sqlite3.connect('expenses.db')
            cur = conn.cursor()
            for index, row in df.iterrows():
                date = row['Date']
                description = row['Description']
                amount = row['Amount']
                cur.execute("INSERT INTO expenses (Date, Description, Category, Price) VALUES (?, ?, ?, ?)",
                            (date, description, 'Imported', amount))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('upload.html')

# Create route to edit database entries individually.
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()

    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        
        cur.execute("""
            UPDATE expenses 
            SET Date = ?, Description = ?, Category = ?, Price = ? 
            WHERE id = ?
        """, (date, description, category, price, id))
        
        conn.commit()
        conn.close()
        return redirect(url_for('view_summary'))

    cur.execute("SELECT * FROM expenses WHERE id = ?", (id,))
    expense = cur.fetchone()
    conn.close()
    return render_template('edit.html', expense=expense)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
