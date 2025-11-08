# demo.py
import pickle

# Define class for Book (Object-Oriented)
class Book:
    def __init__(self, book_id, title, author, price):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = price

    def display(self):
        print(f"{self.book_id}. {self.title} by {self.author} - Rs.{self.price}")

# Create book objects
book1 = Book(1, "ADBMS", "Navathe", 500)
book2 = Book(2, "Python Programming", "Guido", 450)
book3 = Book(3, "Data Science", "James", 600)

books = [book1, book2, book3]

# Save objects to a file (like a small OODB)
with open("books_db.pkl", "wb") as f:
    pickle.dump(books, f)

print("✅ Books stored successfully in Object-Oriented Database!\n")

# Retrieve and display data
with open("books_db.pkl", "rb") as f:
    loaded_books = pickle.load(f)

print("📚 Stored Books in Database:")
for b in loaded_books:
    b.display()
