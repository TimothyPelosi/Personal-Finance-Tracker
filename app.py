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

@app.route('/summary', methods=['GET', 'POST'])
def view_summary():
    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()

    if request.method == 'POST':
        month = request.form['month']
        year = request.form['year']
        cur.execute("SELECT * FROM expenses WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?", (month, year))
        expenses = cur.fetchall()
        cur.execute("SELECT SUM(Price) FROM expenses WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?", (month, year))
        total_expense = cur.fetchone()[0]
    else:
        cur.execute("SELECT * FROM expenses")
        expenses = cur.fetchall()
        cur.execute("SELECT SUM(Price) FROM expenses")
        total_expense = cur.fetchone()[0]

    conn.close()
    
    return render_template('summary.html', expenses=expenses, total=total_expense)

@app.route('/search')
def search():
    return render_template('search.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
