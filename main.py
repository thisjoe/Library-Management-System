from classes import Library

def main():
    library = Library()

    while True:
        print("\nMain Menu:")
        print("1. Register as a new user")
        print("2. View available books")
        print("3. Add a book")
        print("4. Borrow a book")
        print("5. Return a book")
        print("6. View registered users")
        print("7. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        # User registration
        if choice == "1":
            name = input("Enter your name: ").strip()
            user_id = input("Enter your user ID: ").strip()
            library.add_user(name, user_id)
            print(f"User {name} (ID: {user_id}) has been registered.")

        # View available books
        elif choice == "2":
            print("\nAvailable Books:")
            for book_info in library.display_books():
                print(book_info)

        # Add a book
        elif choice == "3":
            title = input("Enter the title of the book: ").strip()
            author = input("Enter the author of the book: ").strip()
            library.add_book(title, author)
            print(f"Book '{title}' by {author} has been added to the library.")

        # Borrow a book
        elif choice == "4":
            user_id = input("Enter your user ID: ").strip()
            user = library.get_user_by_id(user_id)
            if not user:
                print("User not found! Please register first.")
                continue

            title = input("Enter the title of the book you want to borrow: ").strip()
            book = next((b for b in library.books if b.title.lower() == title.lower()), None)
            if not book:
                print("Book not found!")
                continue

            if user.borrow_book(book):
                library.save_data()  # Save changes after borrowing
                print(f"You have successfully borrowed '{title}'.")
            else:
                print(f"'{title}' is currently unavailable.")

        # Return a book
        elif choice == "5":
            user_id = input("Enter your user ID: ").strip()
            user = library.get_user_by_id(user_id)
            if not user:
                print("User not found! Please register first.")
                continue

            title = input("Enter the title of the book you want to return: ").strip()
            book = next((b for b in user.borrowed_books if b.title.lower() == title.lower()), None)
            if not book:
                print("Book not found in your borrowed books!")
                continue

            if user.return_book(book):
                library.save_data()  # Save changes after returning
                print(f"You have successfully returned '{title}'.")
            else:
                print(f"Failed to return '{title}'.")

        # View registered users
        elif choice == "6":
            print("\nRegistered Users:")
            for user_info in library.display_users():
                print(user_info)

        # Exit
        elif choice == "7":
            print("Exiting the Library Management System. Goodbye!")
            break

        else:
            print("Invalid choice! Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
