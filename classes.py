import json

class Book:
    def __init__(self, title, author, availability=True):
        self.title = title
        self.author = author
        self.__availability = availability

    def display_info(self):
        status = "Available" if self.__availability else "Unavailable"
        return f"Title: {self.title}, Author: {self.author}, Status: {status}"

    def borrow_book(self):
        if self.__availability:
            self.__availability = False
            return True
        return False

    def return_book(self):
        self.__availability = True


class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.borrow_book():
            self.borrowed_books.append(book)
            return True
        return False

    def return_book(self, book):
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            return True
        return False


class Library:
    def __init__(self, filename="library_data.json"):
        self.filename = filename
        self.books = []
        self.users = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"No data file found ({self.filename}). Starting with an empty library.")
            return

        for book_data in data.get("books", []):
            book = Book(book_data["title"], book_data["author"], book_data["availability"])
            self.books.append(book)

        for user_data in data.get("users", []):
            user = User(user_data["name"], user_data["user_id"])
            for borrowed_title in user_data["borrowed_books"]:
                book = next((b for b in self.books if b.title == borrowed_title), None)
                if book:
                    user.borrowed_books.append(book)
            self.users.append(user)

    def save_data(self):
        data = {
            "books": [
                {"title": book.title, "author": book.author, "availability": book._Book__availability}
                for book in self.books
            ],
            "users": [
                {
                    "name": user.name,
                    "user_id": user.user_id,
                    "borrowed_books": [book.title for book in user.borrowed_books],
                }
                for user in self.users
            ],
        }
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Library data saved to {self.filename}.")

    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)
        self.save_data()

    def add_user(self, name, user_id):
        user = User(name, user_id)
        self.users.append(user)
        self.save_data()

    def get_user_by_id(self, user_id):
        return next((user for user in self.users if user.user_id == user_id), None)

    def display_books(self):
        return [book.display_info() for book in self.books]

    def display_users(self):
        return [f"Name: {user.name}, ID: {user.user_id}" for user in self.users]