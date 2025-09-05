import json
import logging

logging.basicConfig(filename="library.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s: %(message)s")


class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author

    def to_dict(self):
        return {"book_id": self.book_id, "title": self.title, "author": self.author}

    @classmethod
    def from_dict(cls, data):
        return cls(data["book_id"], data["title"], data["author"])


class Reader:
    def __init__(self, reader_id, name):
        self.reader_id = reader_id
        self.name = name

    def to_dict(self):
        return {"reader_id": self.reader_id, "name": self.name}

    @classmethod
    def from_dict(cls, data):
        return cls(data["reader_id"], data["name"])


class Librarian:
    def __init__(self, librarian_id, name):
        self.librarian_id = librarian_id
        self.name = name

    def to_dict(self):
        return {"librarian_id": self.librarian_id, "name": self.name}

    @classmethod
    def from_dict(cls, data):
        return cls(data["librarian_id"], data["name"])


class Library:
    def __init__(self):
        self.books = {}
        self.readers = {}
        self.librarians = {}

    # Добавление сущностей
    def add_book(self, book):
        self.books[book.book_id] = book
        logging.info(f"Book added: {book.book_id} - {book.title}")

    def remove_book(self, book_id):
        if book_id in self.books:
            removed = self.books.pop(book_id)
            logging.info(f"Book removed: {removed.book_id} - {removed.title}")

    def update_book(self, book_id, title=None, author=None):
        if book_id in self.books:
            book = self.books[book_id]
            if title:
                book.title = title
            if author:
                book.author = author
            logging.info(f"Book updated: {book.book_id} - {book.title}")

    def add_reader(self, reader):
        self.readers[reader.reader_id] = reader
        logging.info(f"Reader added: {reader.reader_id} - {reader.name}")

    def remove_reader(self, reader_id):
        if reader_id in self.readers:
            removed = self.readers.pop(reader_id)
            logging.info(f"Reader removed: {removed.reader_id} - {removed.name}")

    def update_reader(self, reader_id, name=None):
        if reader_id in self.readers:
            reader = self.readers[reader_id]
            if name:
                reader.name = name
            logging.info(f"Reader updated: {reader.reader_id} - {reader.name}")

    def add_librarian(self, librarian):
        self.librarians[librarian.librarian_id] = librarian
        logging.info(f"Librarian added: {librarian.librarian_id} - {librarian.name}")

    def remove_librarian(self, librarian_id):
        if librarian_id in self.librarians:
            removed = self.librarians.pop(librarian_id)
            logging.info(f"Librarian removed: {removed.librarian_id} - {removed.name}")

    def update_librarian(self, librarian_id, name=None):
        if librarian_id in self.librarians:
            librarian = self.librarians[librarian_id]
            if name:
                librarian.name = name
            logging.info(f"Librarian updated: {librarian.librarian_id} - {librarian.name}")

    # Сохранение и загрузка из файла
    def save_to_file(self, filename):
        data = {
            "books": [book.to_dict() for book in self.books.values()],
            "readers": [reader.to_dict() for reader in self.readers.values()],
            "librarians": [librarian.to_dict() for librarian in self.librarians.values()]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Library data saved to {filename}")

    def load_from_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = {b["book_id"]: Book.from_dict(b) for b in data.get("books", [])}
                self.readers = {r["reader_id"]: Reader.from_dict(r) for r in data.get("readers", [])}
                self.librarians = {l["librarian_id"]: Librarian.from_dict(l) for l in data.get("librarians", [])}
            logging.info(f"Library data loaded from {filename}")
        except FileNotFoundError:
            logging.warning(f"File {filename} not found, starting with empty library")

    # Поиск по атрибутам (пример для книг)
    def search_books(self, keyword):
        results = []
        for book in self.books.values():
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
                results.append(book)
        logging.info(f"Search performed for keyword '{keyword}', {len(results)} result(s) found")
        return results

    # Вывод результатов на экран и в файл
    def print_books(self, books, to_file=None):
        output = "\n".join([f"{b.book_id}: {b.title} by {b.author}" for b in books])
        if to_file:
            with open(to_file, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Search results saved to {to_file}")
        else:
            print(output)


# Пример использования
if __name__ == "__main__":
    library = Library()

    # Загрузка данных из файла
    library.load_from_file("library_data.json")

    # Добавление сущностей
    library.add_book(Book("b1", "War and Peace", "Lev Tolstoy"))
    library.add_book(Book("b2", "Crime and Punishment", "Fyodor Dostoevsky"))
    library.add_reader(Reader("r1", "Ivan Ivanov"))
    library.add_librarian(Librarian("l1", "Anna Petrova"))

    # Изменение сущностей
    library.update_book("b2", author="F. Dostoevsky")
    library.update_reader("r1", name="Ivan I.")

    # Сохранение в файл
    library.save_to_file("library_data.json")

    # Поиск
    results = library.search_books("war")
    library.print_books(results)

    # Лог-файл library.log будет фиксировать все действия
