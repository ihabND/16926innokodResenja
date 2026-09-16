from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

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


# =============================================================================
# MODELS
# =============================================================================

# Request body models (no table=True)

class Message(SQLModel):
    text: str


class BookCreate(SQLModel):
    title: str
    author: str
    year: int
    genre: str
    pages: int
    rating: float
    available: bool = True


class BookWithoutAuthor(SQLModel):
    title: str
    year: int
    genre: str
    pages: int
    rating: float
    available: bool = True


class ReviewCreate(SQLModel):
    name: str | None = None
    text: str
    stars: int


# Database tables (table=True)

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    year: int
    genre: str
    pages: int
    rating: float
    available: bool


class Review(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    name: str
    text: str
    stars: int


# =============================================================================
# DATABASE SETUP
# =============================================================================

engine = create_engine("sqlite:///books_post.db")
SQLModel.metadata.create_all(engine)

# Seed only if the table is empty
with Session(engine) as session:
    statement = select(Book)
    result = session.exec(statement).all()
    if not result:
        for book in BOOKS:
            session.add(Book(**book))
        session.commit()


def get_session():
    with Session(engine) as session:
        yield session


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
# Obriši sve recenzije i knjige, pa ponovo dodaj originalnih 20 knjiga.
# Vrati {"count": 20}
@app.post("/books/reset")
def reset_books(session: Session = Depends(get_session)):
    statement = select(Review)
    result = session.exec(statement).all()
    for review in result:
        session.delete(review)

    statement = select(Book)
    result = session.exec(statement).all()
    for book in result:
        session.delete(book)
    session.commit()

    for book in BOOKS:
        session.add(Book(**book))
    session.commit()
    return {"count": len(BOOKS)}


# =============================================================================
# DEO 2: TELO ZAHTEVA (body)
# =============================================================================

# Zadatak 3
# POST /echo
# Body: {"text": "hi"}
# Vrati istu poruku nazad. (Baza nije potrebna.)
@app.post("/echo")
def echo(message: Message):
    return message


# Zadatak 4
# POST /books
# Body: nova knjiga (bez id-ja).
# Sačuvaj knjigu u bazu i vrati je (baza joj dodeljuje id).
# Ako knjiga sa istim naslovom već postoji, vrati False.
@app.post("/books")
def create_book(new_book: BookCreate, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.title == new_book.title)
    result = session.exec(statement).all()
    if result:
        return False
    book = Book(
        title=new_book.title,
        author=new_book.author,
        year=new_book.year,
        genre=new_book.genre,
        pages=new_book.pages,
        rating=new_book.rating,
        available=new_book.available,
    )
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


# Zadatak 5
# POST /books/validated
# Body: nova knjiga (bez id-ja).
# Isto kao zadatak 4, ali proveri i:
#   - naslov nije prazan
#   - ocena je između 0 i 5
#   - broj strana je veći od 0
#   - godina nije veća od 2026
# Ako nešto nije ispravno, vrati False.
@app.post("/books/validated")
def create_validated_book(new_book: BookCreate, session: Session = Depends(get_session)):
    if new_book.title == "":
        return False
    if new_book.rating < 0 or new_book.rating > 5:
        return False
    if new_book.pages <= 0:
        return False
    if new_book.year > 2026:
        return False
    statement = select(Book).where(Book.title == new_book.title)
    result = session.exec(statement).all()
    if result:
        return False
    book = Book(
        title=new_book.title,
        author=new_book.author,
        year=new_book.year,
        genre=new_book.genre,
        pages=new_book.pages,
        rating=new_book.rating,
        available=new_book.available,
    )
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


# Zadatak 6
# POST /books/bulk
# Body: lista novih knjiga.
# Dodaj svaku knjigu čiji naslov još ne postoji i vrati dodate knjige.
# Ako je lista prazna, vrati False.
@app.post("/books/bulk")
def create_books(new_books: list[BookCreate], session: Session = Depends(get_session)):
    if not new_books:
        return False
    added = []
    for new_book in new_books:
        statement = select(Book).where(Book.title == new_book.title)
        result = session.exec(statement).all()
        if result:
            continue
        book = Book(
            title=new_book.title,
            author=new_book.author,
            year=new_book.year,
            genre=new_book.genre,
            pages=new_book.pages,
            rating=new_book.rating,
            available=new_book.available,
        )
        session.add(book)
        session.commit()
        session.refresh(book)
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
def borrow_book(book_id: int, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).all()
    if not result:
        return False
    book = result[0]
    if book.available == False:
        return False
    book.available = False
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


# Zadatak 8
# POST /books/{book_id}/return
# Postavi "available" na True za datu knjigu i vrati knjigu.
# Ako knjiga ne postoji ili nije pozajmljena, vrati False.
@app.post("/books/{book_id}/return")
def return_book(book_id: int, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).all()
    if not result:
        return False
    book = result[0]
    if book.available == True:
        return False
    book.available = True
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


# Zadatak 9
# POST /books/{book_id}/copy
# Napravi kopiju date knjige sa " (copy)" dodatim na naslov.
# Vrati novu knjigu.
# Ako knjiga ne postoji, vrati False.
@app.post("/books/{book_id}/copy")
def copy_book(book_id: int, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).all()
    if not result:
        return False
    book = result[0]
    new_book = Book(
        title=book.title + " (copy)",
        author=book.author,
        year=book.year,
        genre=book.genre,
        pages=book.pages,
        rating=book.rating,
        available=book.available,
    )
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book


# Zadatak 10
# POST /authors/{author}/books
# Body: nova knjiga bez autora.
# Napravi knjigu sa autorom iz putanje i vrati je.
# Ako knjiga sa istim naslovom već postoji, vrati False.
@app.post("/authors/{author}/books")
def create_book_for_author(
    author: str,
    new_book: BookWithoutAuthor,
    session: Session = Depends(get_session),
):
    statement = select(Book).where(Book.title == new_book.title)
    result = session.exec(statement).all()
    if result:
        return False
    book = Book(
        title=new_book.title,
        author=author,
        year=new_book.year,
        genre=new_book.genre,
        pages=new_book.pages,
        rating=new_book.rating,
        available=new_book.available,
    )
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


# =============================================================================
# DEO 4: QUERY PARAMETRI
# =============================================================================

# Zadatak 11
# POST /books/quick?title=Dune Messiah&author=Frank Herbert&year=1969
# Napravi knjigu iz query parametara.
# "title" i "author" su obavezni. Ostali su opcioni, sa ovim podrazumevanim vrednostima:
#   year = 2026, genre = "unknown", pages = 100, rating = 0, available = True
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
    session: Session = Depends(get_session),
):
    if year is None:
        year = 2026
    if genre is None:
        genre = "unknown"
    if pages is None:
        pages = 100
    if rating is None:
        rating = 0
    if available is None:
        available = True
    statement = select(Book).where(Book.title == title)
    result = session.exec(statement).all()
    if result:
        return False
    book = Book(
        title=title,
        author=author,
        year=year,
        genre=genre,
        pages=pages,
        rating=rating,
        available=available,
    )
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


# Zadatak 12
# POST /borrow?title=1984
# Pozajmi knjigu po naslovu.
# Ako knjiga ne postoji ili je već pozajmljena, vrati False.
@app.post("/borrow")
def borrow_by_title(title: str, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.title == title)
    result = session.exec(statement).all()
    if not result:
        return False
    book = result[0]
    if book.available == False:
        return False
    book.available = False
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


# Zadatak 13
# POST /availability?author=Dan Brown&available=false
# Postavi "available" za sve knjige datog autora.
# "available" je opcioni, podrazumevano True.
# Vrati izmenjene knjige. Ako autor nema nijednu knjigu, vrati False.
@app.post("/availability")
def set_author_availability(
    author: str,
    available: bool | None = None,
    session: Session = Depends(get_session),
):
    if available is None:
        available = True
    statement = select(Book).where(Book.author == author)
    result = session.exec(statement).all()
    if not result:
        return False
    for book in result:
        book.available = available
        session.add(book)
    session.commit()
    for book in result:
        session.refresh(book)
    return result


# =============================================================================
# DEO 5: PATH + QUERY PARAMETRI (+ BODY) ZAJEDNO
# =============================================================================

# Zadatak 14
# POST /books/{book_id}/rate?rating=4.5
# Postavi novu ocenu za datu knjigu i vrati knjigu.
# Ako knjiga ne postoji ili ocena nije između 0 i 5, vrati False.
@app.post("/books/{book_id}/rate")
def rate_book(book_id: int, rating: float, session: Session = Depends(get_session)):
    if rating < 0 or rating > 5:
        return False
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).all()
    if not result:
        return False
    book = result[0]
    book.rating = rating
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


# Zadatak 15
# POST /books/{book_id}/copy-as?title=New Title&year=2020
# Napravi kopiju date knjige sa novim naslovom.
# "year" je opcioni: ako je prosleđen, kopija dobija tu godinu.
# Ako knjiga ne postoji ili naslov već postoji, vrati False.
@app.post("/books/{book_id}/copy-as")
def copy_book_as(
    book_id: int,
    title: str,
    year: int | None = None,
    session: Session = Depends(get_session),
):
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).all()
    if not result:
        return False
    book = result[0]

    statement = select(Book).where(Book.title == title)
    result = session.exec(statement).all()
    if result:
        return False

    if year is None:
        year = book.year
    new_book = Book(
        title=title,
        author=book.author,
        year=year,
        genre=book.genre,
        pages=book.pages,
        rating=book.rating,
        available=book.available,
    )
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book


# Zadatak 16
# POST /books/{book_id}/reviews?anonymous=true
# Body: {"name": "Ana", "text": "Great book!", "stars": 5}
# Sačuvaj recenziju za datu knjigu i vrati je.
# Ako je anonymous=true (ili name nije prosleđen), ime je "Anonymous".
# Ako knjiga ne postoji ili stars nije između 1 i 5, vrati False.
@app.post("/books/{book_id}/reviews")
def create_review(
    book_id: int,
    review: ReviewCreate,
    anonymous: bool | None = None,
    session: Session = Depends(get_session),
):
    if review.stars < 1 or review.stars > 5:
        return False
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).all()
    if not result:
        return False
    name = review.name
    if anonymous == True or name is None:
        name = "Anonymous"
    new_review = Review(book_id=book_id, name=name, text=review.text, stars=review.stars)
    session.add(new_review)
    session.commit()
    session.refresh(new_review)
    return new_review
