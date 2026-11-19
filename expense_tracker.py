
import sqlite3

DB_NAME = "expenses.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                description TEXT
            )
        """)

def add_expense():
    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()
    date = input("Enter date (YYYY-MM-DD): ").strip()

    try:
        amount = float(input("Enter amount: "))

        if not category or not date or amount <= 0:
            print("Invalid expense details!")
            return

        with connect_db() as conn:
            conn.execute("""
                INSERT INTO expenses
                (category, amount, date, description)
                VALUES (?, ?, ?, ?)
            """, (category, amount, date, description))

        print("Expense added successfully!")

    except ValueError:
        print("Please enter a valid amount!")

def view_expenses():
    with connect_db() as conn:
        records = conn.execute("""
            SELECT * FROM expenses ORDER BY id
        """).fetchall()

    if not records:
        print("No expenses found!")
        return

    print("\n===== ALL EXPENSES =====")

    for row in records:
        print(
            f"ID: {row[0]} | Category: {row[1]} | "
            f"Amount: Rs. {row[2]:.2f} | "
            f"Date: {row[3]} | Description: {row[4]}"
        )

def show_summary():
    with connect_db() as conn:
        total = conn.execute("""
            SELECT SUM(amount) FROM expenses
        """).fetchone()[0]

        categories = conn.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            GROUP BY category
        """).fetchall()

    print("\n===== EXPENSE SUMMARY =====")
    print(f"Total Expenses: Rs. {total or 0:.2f}")

    for category, amount in categories:
        print(f"{category}: Rs. {amount:.2f}")

def search_category():
    category = input("Enter category: ").strip()

    with connect_db() as conn:
        records = conn.execute("""
            SELECT * FROM expenses
            WHERE LOWER(category) = LOWER(?)
        """, (category,)).fetchall()

    if not records:
        print("No matching expenses found!")
        return

    for row in records:
        print(row)

def main():
    create_table()

    while True:
        print("\n===== SQLITE EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Expense Summary")
        print("4. Search by Category")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            search_category()
        elif choice == "5":
            print("Thank you!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
