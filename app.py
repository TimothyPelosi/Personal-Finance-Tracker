from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS expenses 
                   (Date TEXT, Description TEXT, Category TEXT, Price REAL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        
        conn = sqlite3.connect('expenses.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO expenses (Date, Description, Category, Price) VALUES (?, ?, ?, ?)",
                    (date, description, category, price))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/summary')
def view_summary():
    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()
    cur.execute("SELECT SUM(Price) FROM expenses")
    total_expense = cur.fetchone()[0]
    conn.close()
    
    return render_template('summary.html', expenses=expenses, total=total_expense)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
