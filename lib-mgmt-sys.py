import pymysql

# Connect to MySQL
try:
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="@Rudransh123",
        database="librarymgmtdb"
    )
    cursor = connection.cursor()
    print("Connected to the database successfully!")
except pymysql.MySQLError as err:
    print(f"Error: {err}")
    exit()

# Create necessary tables if they do not exist
def initialize_database():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255),
            available INT DEFAULT 1
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowed (
            borrow_id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT,
            borrower_name VARCHAR(255),
            borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
    """)
    connection.commit()

# Add a book to the library
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
    connection.commit()
    print("Book added successfully!")

# View all books in the library
def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print("\nLibrary Books:")
    print("ID | Title | Author | Available")
    for book in books:
        print(f"{book[0]} | {book[1]} | {book[2]} | {'Yes' if book[3] else 'No'}")

# Borrow a book
def borrow_book():
    view_books()
    book_id = int(input("\nEnter the ID of the book to borrow: "))
    borrower_name = input("Enter your name: ")

    cursor.execute("SELECT available FROM books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()

    if result and result[0] == 1:
        cursor.execute("UPDATE books SET available = 0 WHERE book_id = %s", (book_id,))
        cursor.execute(
            "INSERT INTO borrowed (book_id, borrower_name) VALUES (%s, %s)",
            (book_id, borrower_name)
        )
        connection.commit()
        print("Book borrowed successfully!")
    else:
        print("Sorry, the book is not available.")

# Return a book
def return_book():
    borrower_name = input("Enter your name: ")
    cursor.execute("""
        SELECT b.borrow_id, bk.title FROM borrowed b
        JOIN books bk ON b.book_id = bk.book_id
        WHERE b.borrower_name = %s
    """, (borrower_name,))
    borrowed_books = cursor.fetchall()

    if borrowed_books:
        print("\nYour Borrowed Books:")
        for borrow_id, title in borrowed_books:
            print(f"{borrow_id} | {title}")

        borrow_id = int(input("Enter the borrow ID of the book to return: "))
        cursor.execute("""
            SELECT book_id FROM borrowed WHERE borrow_id = %s AND borrower_name = %s
        """, (borrow_id, borrower_name))
        result = cursor.fetchone()

        if result:
            book_id = result[0]
            cursor.execute("UPDATE books SET available = 1 WHERE book_id = %s", (book_id,))
            cursor.execute("DELETE FROM borrowed WHERE borrow_id = %s", (borrow_id,))
            connection.commit()
            print("Book returned successfully!")
        else:
            print("Invalid borrow ID.")
    else:
        print("No borrowed books found.")

# Main menu
def main():
    initialize_database()
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. View Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            borrow_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
