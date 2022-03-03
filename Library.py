class Book:
    def __init__(self, title, author, dewey, isbn):
        self.title = title.title()
        self.author = author
        self.dewey = dewey
        self.isbn = isbn
        self.available = True
        self.borrower = None

    def append_to_list(self, book_list):
        book_list.append(self)

    def print_details(self):
        for key, value in self.__dict__.items():
            print(f"{key}: {value}".capitalize())
        print('#' * 20)


class User:
    def __init__(self, name, address):
        self.name = name.title()
        self.address = address
        self.fees = 0.0
        self.borrowed_books = []

    def append_to_list(self, user_list):
        user_list.append(self)

    def print_details(self):
        for key, value in list(self.__dict__.items())[:-1]:
            print(f"{key}: {'$' if key == 'fees' else ''}{value}".capitalize())
        print('#' * 20)


def create_book(details, book_list):
    instance = Book(*details)
    instance.append_to_list(book_list)


def create_user(details, user_list):
    instance = User(*details)
    instance.append_to_list(user_list)


def print_info(info_list):
    for item in info_list:
        item.print_details()


def add_user(user_list):
    name = input("Enter the new user's name: ")
    address = input("Enter the new user's address: ")
    create_user([name, address], user_list)
    print(f"{name} at address {address} has been added to the user list.")


def add_book(book_list):
    title = input("Enter the new book's title: ")
    author = input("Enter the new book's author: ").title()
    dewey = input("Enter the new book's dewey code: ").upper()
    isbn = input("Enter the new book's ISBN: ")
    create_book([title, author, dewey, isbn], book_list)
    print(f"{title} by {author} has been added to the book list.")


def find_user(user_list, messages=True):
    user_to_find = input("Enter the user's name: ").title()
    for user in user_list:
        if user.name == user_to_find:
            if messages:
                print(f"Hello {user.name}!")
            return user
    else:
        if messages:
            print(f"{user_to_find} is not in the user list.")
        return


def find_book(book_list, user_list, messages=True):
    user = find_user(user_list)
    assert isinstance(user, User)
    book_to_find = input("Enter the book's title: ").title()
    for book in book_list:
        if book.title == book_to_find:
            if book.available and messages:
                print(f"{book.title} is available.")
                return book, user
            elif book.borrower == user.name:
                print("This book can be returned.")
                return book, user
    else:
        if messages:
            print(f"{book_to_find} is either not in the book list or is"
                  f" currently being borrowed.")
        return


def lend_book(book_list, user_list):
    if data := find_book(book_list, user_list):
        book, user = data
        assert isinstance(user, User), "User does not exist in User class"
        assert isinstance(book, Book), "Book does not exist in Book class"
        if book.available:
            while True:
                confirm = input(f"Do you want to loan {book.title}?"
                                " (y/n) ").lower()
                if confirm == 'y':
                    book.available = False
                    book.borrower = user.name
                    user.borrowed_books.append(book.title)
                    print(f"{book.title} is now borrowed on"
                          f" {user.name}'s account.")
                    return
                elif confirm == 'n':
                    print("Loan canceled.")
                    return
                else:
                    print("Invalid input, please enter again.")


def return_book(book_list, user_list):
    if data := find_book(book_list, user_list):
        book, user = data
        assert isinstance(user, User), "User does not exist in User class"
        assert isinstance(book, Book), "Book does not exist in Book class"
        if book.title in user.borrowed_books:
            while True:
                confirm = input("Are you sure you want to return"
                                " this book? (y/n) ").lower()
                if confirm == 'y':
                    book.available = True
                    book.borrower = None
                    user.borrowed_books.remove(book.title)
                    print(f"'{book.title}' has been returned to"
                          " the library.")
                    return
                elif confirm == 'n':
                    print("Return canceled.")
                    return
                else:
                    print("Invalid input, please enter again.")
        else:
            print(f"You have not borrowed this book.")


def main():
    book_list = []
    user_list = []

    def menu():
        nonlocal book_list, user_list
        choices = {
            '1': "lend_book(book_list, user_list)",
            '2': "return_book(book_list, user_list)",
            '3': "add_user(user_list)",
            '4': "add_book(book_list)",
            '5': "print('Goodbye!');exit(0)"}
        while True:
            print("1. Lend a book\n2. Return a book\n3. Add a user\n4."
                  " Add a book\n5. Exit")
            choice = input("Please enter a number: ")
            if choices.get(choice) is None:
                print("Please enter a number from 1 to 5.")
                continue
            confirm = input("Confirm? (y/n) ").lower()
            if confirm == 'y':
                if choices.get(choice) is None:
                    print("Please enter a number from 1 to 5.")
                else:
                    exec(choices.get(choice))
            elif confirm == 'n':
                continue
            else:
                print("Please enter y or n.")

    create_book(["Lord of the Rings", "J.R.R Tolkien", "TOL",
                 "9780261103252"], book_list)
    create_book(["The Hunger Games", "Suzanne Collins", "COL",
                 "9781407132082"], book_list)
    create_book(["A Tale of Two Cities", "Charles Dickens", "DIC",
                 "9781853262647"], book_list)
    create_book(["Harry Potter", "J.K Rowling", "ROW",
                 "9780439321624"], book_list)

    create_user(["John", "12 Example St"], user_list)
    create_user(["Susan", "1011 Binary Rd"], user_list)
    create_user(["Paul", "25 Appletree Dr"], user_list)
    create_user(["Mary", "8 Moon Cres"], user_list)
    while True:
        menu()


if __name__ == '__main__':
    main()
