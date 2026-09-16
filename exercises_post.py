import copy
from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel

BOOKS = [
    {"id": 1, "title": "1984", "author": "George Orwell", "year": 1949, "genre": "dystopian", "pages": 328, "rating": 4.7, "available": True},
    {"id": 2, "title": "Animal Farm", "author": "George Orwell", "year": 1945, "genre": "satire", "pages": 112, "rating": 4.5, "available": False},
    {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960, "genre": "classic", "pages": 281, "rating": 4.8, "available": True},
    {"id": 4, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925, "genre": "classic", "pages": 180, "rating": 4.2, "available": True},
    {"id": 5, "title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813, "genre": "romance", "pages": 432, "rating": 4.6, "available": True},
    {"id": 6, "title": "Emma", "author": "Jane Austen", "year": 1815, "genre": "romance", "pages": 474, "rating": 4.1, "available": False},
    {"id": 7, "title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "genre": "fantasy", "pages": 310, "rating": 4.7, "available": True},
    {"id": 8, "title": "The Fellowship of the Ring", "author": "J.R.R. Tolkien", "year": 1954, "genre": "fantasy", "pages": 423, "rating": 4.8, "available": False},
    {"id": 9, "title": "Brave New World", "author": "Aldous Huxley", "year": 1932, "genre": "dystopian", "pages": 311, "rating": 4.3, "available": True},
    {"id": 10, "title": "Fahrenheit 451", "author": "Ray Bradbury", "year": 1953, "genre": "dystopian", "pages": 194, "rating": 4.4, "available": True},
    {"id": 11, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951, "genre": "classic", "pages": 234, "rating": 3.9, "available": False},
    {"id": 12, "title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "year": 1997, "genre": "fantasy", "pages": 223, "rating": 4.9, "available": True},
    {"id": 13, "title": "Harry Potter and the Chamber of Secrets", "author": "J.K. Rowling", "year": 1998, "genre": "fantasy", "pages": 251, "rating": 4.7, "available": True},
    {"id": 14, "title": "The Da Vinci Code", "author": "Dan Brown", "year": 2003, "genre": "thriller", "pages": 489, "rating": 3.9, "available": True},
    {"id": 15, "title": "Angels & Demons", "author": "Dan Brown", "year": 2000, "genre": "thriller", "pages": 616, "rating": 4.0, "available": False},
    {"id": 16, "title": "The Alchemist", "author": "Paulo Coelho", "year": 1988, "genre": "fiction", "pages": 208, "rating": 4.3, "available": True},
    {"id": 17, "title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "year": 1866, "genre": "classic", "pages": 671, "rating": 4.6, "available": True},
    {"id": 18, "title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky", "year": 1880, "genre": "classic", "pages": 796, "rating": 4.7, "available": False},
    {"id": 19, "title": "Dune", "author": "Frank Herbert", "year": 1965, "genre": "science fiction", "pages": 688, "rating": 4.6, "available": True},
    {"id": 20, "title": "The Hunger Games", "author": "Suzanne Collins", "year": 2008, "genre": "dystopian", "pages": 374, "rating": 4.4, "available": True},
]

ORIGINAL_BOOKS = copy.deepcopy(BOOKS)

REVIEWS = []


# =============================================================================
# MODELS (request bodies)
# =============================================================================

class Message(BaseModel):
    text: str


class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    genre: str
    pages: int
    rating: float
    available: bool = True


class BookWithoutAuthor(BaseModel):
    title: str
    year: int
    genre: str
    pages: int
    rating: float
    available: bool = True


class ReviewCreate(BaseModel):
    name: str | None = None
    text: str
    stars: int


app = FastAPI()


# =============================================================================
# DEO 1: JEDNOSTAVNI ENDPOINTI (bez parametara)
# =============================================================================

# Zadatak 1
# POST /hello
# Vrati {"message": "Hello from POST"}
@app.post("/hello")
def hello():
    return {"message": "Hello from POST"}


# Zadatak 2
# POST /books/reset
# Vrati originalnih 20 knjiga u BOOKS i obriši sve recenzije.
# Vrati {"count": 20}
@app.post("/books/reset")
def reset_books():
    BOOKS.clear()
    BOOKS.extend(copy.deepcopy(ORIGINAL_BOOKS))
    REVIEWS.clear()
    return {"count": len(BOOKS)}


# =============================================================================
# DEO 2: TELO ZAHTEVA (body)
# =============================================================================

# Zadatak 3
# POST /echo
# Body: {"text": "hi"}
# Vrati istu poruku nazad.
@app.post("/echo")
def echo(message: Message):
    return message


# Zadatak 4
# POST /books
# Body: nova knjiga (bez id-ja).
# Dodeli knjizi novi id (najveći id + 1), dodaj je u BOOKS i vrati je.
# Ako knjiga sa istim naslovom već postoji (ignoriši velika/mala slova), vrati False.
@app.post("/books")
def create_book(new_book: BookCreate):
    for book in BOOKS:
        if book["title"].lower() == new_book.title.lower():
            return False
    new_id = 1
    for book in BOOKS:
        if book["id"] >= new_id:
            new_id = book["id"] + 1
    book = new_book.model_dump()
    book["id"] = new_id
    BOOKS.append(book)
    return book


# Zadatak 5
# POST /books/validated
# Body: nova knjiga (bez id-ja).
# Isto kao zadatak 4, ali proveri i:
#   - naslov nije prazan
#   - ocena je između 0 i 5
#   - broj strana je veći od 0
#   - godina nije u budućnosti
# Ako nešto nije ispravno, vrati False.
@app.post("/books/validated")
def create_validated_book(new_book: BookCreate):
    if new_book.title.strip() == "":
        return False
    if new_book.rating < 0 or new_book.rating > 5:
        return False
    if new_book.pages <= 0:
        return False
    if new_book.year > date.today().year:
        return False
    return create_book(new_book)


# Zadatak 6
# POST /books/bulk
# Body: lista novih knjiga.
# Dodaj svaku knjigu čiji naslov još ne postoji i vrati dodate knjige.
# Ako je lista prazna, vrati False.
@app.post("/books/bulk")
def create_books(new_books: list[BookCreate]):
    if not new_books:
        return False
    added = []
    for new_book in new_books:
        book = create_book(new_book)
        if book:
            added.append(book)
    return added


# =============================================================================
# DEO 3: PATH PARAMETRI
# =============================================================================

# Zadatak 7
# POST /books/{book_id}/borrow
# Postavi "available" na False za datu knjigu i vrati knjigu.
# Ako knjiga ne postoji ili je već pozajmljena, vrati False.
@app.post("/books/{book_id}/borrow")
def borrow_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            if not book["available"]:
                return False
            book["available"] = False
            return book
    return False


# Zadatak 8
# POST /books/{book_id}/return
# Postavi "available" na True za datu knjigu i vrati knjigu.
# Ako knjiga ne postoji ili nije pozajmljena, vrati False.
@app.post("/books/{book_id}/return")
def return_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            if book["available"]:
                return False
            book["available"] = True
            return book
    return False


# Zadatak 9
# POST /books/{book_id}/copy
# Napravi kopiju date knjige sa novim id-jem i " (copy)" dodatim na naslov.
# Vrati novu knjigu.
# Ako knjiga ne postoji, vrati False.
@app.post("/books/{book_id}/copy")
def copy_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            new_book = BookCreate(**book)
            new_book.title = book["title"] + " (copy)"
            return create_book(new_book)
    return False


# Zadatak 10
# POST /authors/{author}/books
# Body: nova knjiga bez autora.
# Napravi knjigu sa autorom iz putanje i vrati je.
# Ako knjiga sa istim naslovom već postoji, vrati False.
@app.post("/authors/{author}/books")
def create_book_for_author(author: str, new_book: BookWithoutAuthor):
    book = BookCreate(**new_book.model_dump(), author=author)
    return create_book(book)


# =============================================================================
# DEO 4: QUERY PARAMETRI
# =============================================================================

# Zadatak 11
# POST /books/quick?title=Dune Messiah&author=Frank Herbert&year=1969
# Napravi knjigu iz query parametara.
# "title" i "author" su obavezni. Ostali su opcioni, sa ovim podrazumevanim vrednostima:
#   year = tekuća godina, genre = "unknown", pages = 100, rating = 0, available = True
# Ako knjiga sa istim naslovom već postoji, vrati False.
@app.post("/books/quick")
def quick_create_book(
    title: str,
    author: str,
    year: int | None = None,
    genre: str | None = None,
    pages: int | None = None,
    rating: float | None = None,
    available: bool | None = None,
):
    if year is None:
        year = date.today().year
    if genre is None:
        genre = "unknown"
    if pages is None:
        pages = 100
    if rating is None:
        rating = 0
    if available is None:
        available = True
    book = BookCreate(
        title=title,
        author=author,
        year=year,
        genre=genre,
        pages=pages,
        rating=rating,
        available=available,
    )
    return create_book(book)


# Zadatak 12
# POST /borrow?title=1984
# Pozajmi knjigu po naslovu (ignoriši velika/mala slova).
# Ako knjiga ne postoji ili je već pozajmljena, vrati False.
@app.post("/borrow")
def borrow_by_title(title: str):
    for book in BOOKS:
        if book["title"].lower() == title.lower():
            return borrow_book(book["id"])
    return False


# Zadatak 13
# POST /availability?author=Dan Brown&available=false
# Postavi "available" za sve knjige datog autora (ignoriši velika/mala slova).
# "available" je opcioni, podrazumevano True.
# Vrati izmenjene knjige. Ako autor nema nijednu knjigu, vrati False.
@app.post("/availability")
def set_author_availability(author: str, available: bool | None = None):
    if available is None:
        available = True
    changed = []
    for book in BOOKS:
        if book["author"].lower() == author.lower():
            book["available"] = available
            changed.append(book)
    if not changed:
        return False
    return changed


# =============================================================================
# DEO 5: PATH + QUERY PARAMETRI (+ BODY) ZAJEDNO
# =============================================================================

# Zadatak 14
# POST /books/{book_id}/rate?rating=4.5
# Postavi novu ocenu za datu knjigu i vrati knjigu.
# Ako knjiga ne postoji ili ocena nije između 0 i 5, vrati False.
@app.post("/books/{book_id}/rate")
def rate_book(book_id: int, rating: float):
    if rating < 0 or rating > 5:
        return False
    for book in BOOKS:
        if book["id"] == book_id:
            book["rating"] = rating
            return book
    return False


# Zadatak 15
# POST /books/{book_id}/copy-as?title=New Title&year=2020
# Napravi kopiju date knjige sa novim naslovom.
# "year" je opcioni: ako je prosleđen, kopija dobija tu godinu.
# Ako knjiga ne postoji ili naslov već postoji, vrati False.
@app.post("/books/{book_id}/copy-as")
def copy_book_as(book_id: int, title: str, year: int | None = None):
    for book in BOOKS:
        if book["id"] == book_id:
            new_book = BookCreate(**book)
            new_book.title = title
            if year is not None:
                new_book.year = year
            return create_book(new_book)
    return False


# Zadatak 16
# POST /books/{book_id}/reviews?anonymous=true
# Body: {"name": "Ana", "text": "Great book!", "stars": 5}
# Dodaj recenziju u REVIEWS za datu knjigu i vrati je.
# Recenzija dobija: id (broj recenzija + 1), book_id, name, text, stars.
# Ako je anonymous=true (ili name nije prosleđen), ime je "Anonymous".
# Ako knjiga ne postoji ili stars nije između 1 i 5, vrati False.
@app.post("/books/{book_id}/reviews")
def create_review(book_id: int, review: ReviewCreate, anonymous: bool | None = None):
    if review.stars < 1 or review.stars > 5:
        return False
    for book in BOOKS:
        if book["id"] == book_id:
            name = review.name
            if anonymous or name is None:
                name = "Anonymous"
            new_review = {
                "id": len(REVIEWS) + 1,
                "book_id": book_id,
                "name": name,
                "text": review.text,
                "stars": review.stars,
            }
            REVIEWS.append(new_review)
            return new_review
    return False
