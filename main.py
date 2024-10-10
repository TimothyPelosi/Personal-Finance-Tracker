import sqlite3
import datetime

conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

while True:
    print("Select an option: ")
    print("1. Enter a new expense")
    print("2. View expenses summary")

    choice = int(input())

    if choice == 1:
        datetime = input("Enter the date of the expense (YYYY-MM-DD): ")
        description = input("Enter the description of the expense: ")

        cur.execute("SELECT DISTINCT category FROM expenses")

        categories = cur.fetchall()

        print("Select a category by number: ")
        for index, category in enumerate(categories):
            print(f"{index + 1}. {category[0]}")
        print(f"{len(categories) + 1}. Create a new category")

        category_choice = int(input())
        if category_choice == len(categories) + 1:
            category = input("Enter the new category name: ")
        else: 
            category = categories[category_choice -1][0]

        price = input("Enter the price of the expense: ")

        cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES(?,?,?,?)", (date, description, category, price))

        conn.commit()
        
    elif choice == 2:
        pass

    else:
        exit()
