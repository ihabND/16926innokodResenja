from fastapi import Depends, FastAPI
from sqlalchemy import desc
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
    {"id": 21, "title": "Catching Fire", "author": "Suzanne Collins", "year": 2009, "genre": "dystopian", "pages": 391, "rating": 4.3, "available": False},
    {"id": 22, "title": "Mockingjay", "author": "Suzanne Collins", "year": 2010, "genre": "dystopian", "pages": 390, "rating": 4.1, "available": True},
    {"id": 23, "title": "The Two Towers", "author": "J.R.R. Tolkien", "year": 1954, "genre": "fantasy", "pages": 352, "rating": 4.6, "available": True},
    {"id": 24, "title": "The Return of the King", "author": "J.R.R. Tolkien", "year": 1955, "genre": "fantasy", "pages": 416, "rating": 4.8, "available": True},
    {"id": 25, "title": "Harry Potter and the Prisoner of Azkaban", "author": "J.K. Rowling", "year": 1999, "genre": "fantasy", "pages": 317, "rating": 4.8, "available": False},
    {"id": 26, "title": "Harry Potter and the Goblet of Fire", "author": "J.K. Rowling", "year": 2000, "genre": "fantasy", "pages": 636, "rating": 4.7, "available": True},
    {"id": 27, "title": "Sense and Sensibility", "author": "Jane Austen", "year": 1811, "genre": "romance", "pages": 409, "rating": 4.2, "available": True},
    {"id": 28, "title": "Persuasion", "author": "Jane Austen", "year": 1817, "genre": "romance", "pages": 249, "rating": 4.3, "available": True},
    {"id": 29, "title": "Wuthering Heights", "author": "Emily Bronte", "year": 1847, "genre": "romance", "pages": 416, "rating": 4.0, "available": False},
    {"id": 30, "title": "Jane Eyre", "author": "Charlotte Bronte", "year": 1847, "genre": "romance", "pages": 532, "rating": 4.4, "available": True},
    {"id": 31, "title": "The Idiot", "author": "Fyodor Dostoevsky", "year": 1869, "genre": "classic", "pages": 652, "rating": 4.3, "available": True},
    {"id": 32, "title": "War and Peace", "author": "Leo Tolstoy", "year": 1869, "genre": "classic", "pages": 1225, "rating": 4.5, "available": False},
    {"id": 33, "title": "Anna Karenina", "author": "Leo Tolstoy", "year": 1878, "genre": "classic", "pages": 864, "rating": 4.4, "available": True},
    {"id": 34, "title": "Moby Dick", "author": "Herman Melville", "year": 1851, "genre": "classic", "pages": 635, "rating": 3.8, "available": True},
    {"id": 35, "title": "The Adventures of Tom Sawyer", "author": "Mark Twain", "year": 1876, "genre": "classic", "pages": 274, "rating": 4.1, "available": True},
    {"id": 36, "title": "Adventures of Huckleberry Finn", "author": "Mark Twain", "year": 1884, "genre": "classic", "pages": 366, "rating": 4.0, "available": False},
    {"id": 37, "title": "Of Mice and Men", "author": "John Steinbeck", "year": 1937, "genre": "classic", "pages": 107, "rating": 4.2, "available": True},
    {"id": 38, "title": "The Grapes of Wrath", "author": "John Steinbeck", "year": 1939, "genre": "classic", "pages": 464, "rating": 4.3, "available": True},
    {"id": 39, "title": "The Old Man and the Sea", "author": "Ernest Hemingway", "year": 1952, "genre": "fiction", "pages": 127, "rating": 4.0, "available": True},
    {"id": 40, "title": "One Hundred Years of Solitude", "author": "Gabriel Garcia Marquez", "year": 1967, "genre": "fiction", "pages": 417, "rating": 4.5, "available": False},
    {"id": 41, "title": "The Little Prince", "author": "Antoine de Saint-Exupery", "year": 1943, "genre": "fiction", "pages": 96, "rating": 4.7, "available": True},
    {"id": 42, "title": "Foundation", "author": "Isaac Asimov", "year": 1951, "genre": "science fiction", "pages": 255, "rating": 4.3, "available": True},
    {"id": 43, "title": "I, Robot", "author": "Isaac Asimov", "year": 1950, "genre": "science fiction", "pages": 253, "rating": 4.2, "available": True},
    {"id": 44, "title": "Neuromancer", "author": "William Gibson", "year": 1984, "genre": "science fiction", "pages": 271, "rating": 3.9, "available": False},
    {"id": 45, "title": "The Martian", "author": "Andy Weir", "year": 2011, "genre": "science fiction", "pages": 369, "rating": 4.6, "available": True},
    {"id": 46, "title": "Inferno", "author": "Dan Brown", "year": 2013, "genre": "thriller", "pages": 461, "rating": 3.8, "available": True},
    {"id": 47, "title": "Gone Girl", "author": "Gillian Flynn", "year": 2012, "genre": "thriller", "pages": 422, "rating": 4.1, "available": True},
    {"id": 48, "title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "year": 2005, "genre": "thriller", "pages": 465, "rating": 4.2, "available": False},
    {"id": 49, "title": "Gulliver's Travels", "author": "Jonathan Swift", "year": 1726, "genre": "satire", "pages": 306, "rating": 3.7, "available": True},
    {"id": 50, "title": "Catch-22", "author": "Joseph Heller", "year": 1961, "genre": "satire", "pages": 453, "rating": 4.0, "available": True},
]


# =============================================================================
# DATABASE SETUP
# =============================================================================

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    year: int
    genre: str
    pages: int
    rating: float
    available: bool


engine = create_engine("sqlite:///books.db")
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
# GET /healthy
# Vrati {"status": "ok"}
@app.get("/healthy")
def healthy():
    return {"status": "ok"}


# Zadatak 2
# GET /books
# Vrati sve knjige.
@app.get("/books")
def get_books(session: Session = Depends(get_session)):
    statement = select(Book)
    result = session.exec(statement).all()
    return result


# Zadatak 3
# GET /books/count
# Vrati broj knjiga, npr. {"count": 20}
@app.get("/books/count")
def count_books(session: Session = Depends(get_session)):
    statement = select(Book)
    result = session.exec(statement).all()
    return {"count": len(result)}


# Zadatak 4
# GET /books/first
# Vrati knjigu sa najmanjim id-jem.
@app.get("/books/first")
def first_book(session: Session = Depends(get_session)):
    statement = select(Book).order_by(Book.id)
    result = session.exec(statement).all()
    if not result:
        return False
    return result[0]


# Zadatak 5
# GET /books/last
# Vrati knjigu sa najvećim id-jem.
@app.get("/books/last")
def last_book(session: Session = Depends(get_session)):
    statement = select(Book).order_by(desc(Book.id))
    result = session.exec(statement).all()
    if not result:
        return False
    return result[0]


# Zadatak 6
# GET /books/titles
# Vrati listu samo sa naslovima svih knjiga.
@app.get("/books/titles")
def book_titles(session: Session = Depends(get_session)):
    statement = select(Book)
    result = session.exec(statement).all()
    titles = []
    for book in result:
        titles.append(book.title)
    return titles


# Zadatak 7
# GET /books/available
# Vrati samo knjige koje su dostupne.
@app.get("/books/available")
def available_books(session: Session = Depends(get_session)):
    statement = select(Book).where(Book.available == True)
    result = session.exec(statement).all()
    return result


# Zadatak 8
# GET /books/best
# Vrati knjigu sa najvećom ocenom.
@app.get("/books/best")
def best_book(session: Session = Depends(get_session)):
    statement = select(Book).order_by(desc(Book.rating))
    result = session.exec(statement).all()
    if not result:
        return False
    return result[0]


# Zadatak 9
# GET /authors
# Vrati listu svih autora, bez duplikata.
@app.get("/authors")
def get_authors(session: Session = Depends(get_session)):
    statement = select(Book)
    result = session.exec(statement).all()
    authors = []
    for book in result:
        if book.author not in authors:
            authors.append(book.author)
    return authors


# =============================================================================
# DEO 2: PATH PARAMETRI
# =============================================================================

# Zadatak 10
# GET /books/{book_id}
# Vrati knjigu sa datim id-jem.
# Ako ne postoji, vrati False.
@app.get("/books/{book_id}")
def get_book(book_id: int, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).all()
    if not result:
        return False
    return result[0]


# Zadatak 11
# GET /books/{book_id}/title
# Vrati samo naslov knjige sa datim id-jem, npr. {"title": "1984"}
# Ako ne postoji, vrati False.
@app.get("/books/{book_id}/title")
def get_book_title(book_id: int, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).all()
    if not result:
        return False
    return {"title": result[0].title}


# Zadatak 12
# GET /books/title/{title}
# Vrati knjigu sa datim naslovom.
# Ako ne postoji, vrati False.
@app.get("/books/title/{title}")
def get_book_by_title(title: str, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.title == title)
    result = session.exec(statement).all()
    if not result:
        return False
    return result[0]


# Zadatak 13
# GET /books/author/{author}
# Vrati sve knjige datog autora.
# Ako nema nijedne, vrati False.
@app.get("/books/author/{author}")
def get_books_by_author(author: str, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.author == author)
    result = session.exec(statement).all()
    if not result:
        return False
    return result


# Zadatak 14
# GET /books/genre/{genre}
# Vrati sve knjige datog žanra.
# Ako nema nijedne, vrati False.
@app.get("/books/genre/{genre}")
def get_books_by_genre(genre: str, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.genre == genre)
    result = session.exec(statement).all()
    if not result:
        return False
    return result


# Zadatak 15
# GET /books/year/{year}
# Vrati sve knjige objavljene date godine.
# Ako nema nijedne, vrati False.
@app.get("/books/year/{year}")
def get_books_by_year(year: int, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.year == year)
    result = session.exec(statement).all()
    if not result:
        return False
    return result


# Zadatak 16
# GET /books/{book_id}/is-available
# Vrati {"available": True} ili {"available": False} za datu knjigu.
# Ako knjiga ne postoji, vrati False.
@app.get("/books/{book_id}/is-available")
def is_book_available(book_id: int, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).all()
    if not result:
        return False
    return {"available": result[0].available}


# =============================================================================
# DEO 3: QUERY PARAMETRI
# =============================================================================

# Zadatak 17
# GET /search?title=Potter
# Vrati sve knjige čiji naslov sadrži dati tekst.
# Ako nema nijedne, vrati False.
@app.get("/search")
def search_books(title: str, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.title.contains(title))
    result = session.exec(statement).all()
    if not result:
        return False
    return result


# Zadatak 18
# GET /filter/rating?min_rating=4.5
# Vrati sve knjige sa ocenom većom ili jednakom min_rating.
# Ako min_rating nije između 0 i 5, vrati False.
@app.get("/filter/rating")
def filter_by_rating(min_rating: float, session: Session = Depends(get_session)):
    if min_rating < 0 or min_rating > 5:
        return False
    statement = select(Book).where(Book.rating >= min_rating)
    result = session.exec(statement).all()
    return result


# Zadatak 19
# GET /filter/available?available=true
# Vrati knjige kod kojih se "available" poklapa sa query parametrom.
@app.get("/filter/available")
def filter_by_available(available: bool, session: Session = Depends(get_session)):
    statement = select(Book).where(Book.available == available)
    result = session.exec(statement).all()
    return result


# Zadatak 20
# GET /filter/pages?min_pages=200&max_pages=400
# Vrati knjige sa brojem strana između min_pages i max_pages (uključujući i njih).
# Oba parametra su opciona. Primeni samo one koji su prosleđeni.
# Ako su prosleđena oba i min_pages je veće od max_pages, vrati False.
@app.get("/filter/pages")
def filter_by_pages(
    min_pages: int | None = None,
    max_pages: int | None = None,
    session: Session = Depends(get_session),
):
    if min_pages is not None and max_pages is not None and min_pages > max_pages:
        return False
    statement = select(Book)
    if min_pages is not None:
        statement = statement.where(Book.pages >= min_pages)
    if max_pages is not None:
        statement = statement.where(Book.pages <= max_pages)
    result = session.exec(statement).all()
    return result


# Zadatak 21
# GET /filter/years?start=1900&end=2000
# Vrati knjige objavljene između start i end (uključujući i njih).
# Ako je start veće od end, vrati False.
@app.get("/filter/years")
def filter_by_years(start: int, end: int, session: Session = Depends(get_session)):
    if start > end:
        return False
    statement = select(Book).where(Book.year >= start, Book.year <= end)
    result = session.exec(statement).all()
    return result


# Zadatak 22
# GET /top?limit=5
# Vrati "limit" knjiga sa najvećom ocenom.
# "limit" je opcioni, podrazumevano 5.
# Ako je limit manji od 1, vrati False.
@app.get("/top")
def top_books(limit: int | None = None, session: Session = Depends(get_session)):
    if limit is None:
        limit = 5
    if limit < 1:
        return False
    statement = select(Book).order_by(desc(Book.rating)).limit(limit)
    result = session.exec(statement).all()
    return result


# Zadatak 23
# GET /sort?by=year
# Vrati sve knjige sortirane po datom polju (od najmanjeg ka najvećem).
# "by" može biti: title, year, pages, rating (podrazumevano: title)
# Ako "by" ima neku drugu vrednost, vrati False.
@app.get("/sort")
def sort_books(by: str | None = None, session: Session = Depends(get_session)):
    if by is None or by == "title":
        statement = select(Book).order_by(Book.title)
    elif by == "year":
        statement = select(Book).order_by(Book.year)
    elif by == "pages":
        statement = select(Book).order_by(Book.pages)
    elif by == "rating":
        statement = select(Book).order_by(Book.rating)
    else:
        return False
    result = session.exec(statement).all()
    return result


# Zadatak 24
# GET /filter?genre=classic&available=true&min_rating=4
# Svi parametri su opcioni. Primeni samo filtere koji su prosleđeni.
@app.get("/filter")
def filter_books(
    genre: str | None = None,
    available: bool | None = None,
    min_rating: float | None = None,
    session: Session = Depends(get_session),
):
    statement = select(Book)
    if genre is not None:
        statement = statement.where(Book.genre == genre)
    if available is not None:
        statement = statement.where(Book.available == available)
    if min_rating is not None:
        statement = statement.where(Book.rating >= min_rating)
    result = session.exec(statement).all()
    return result


# =============================================================================
# DEO 4: PATH + QUERY PARAMETRI ZAJEDNO
# =============================================================================

# Zadatak 25
# GET /authors/{author}/books?available=true
# Vrati knjige datog autora. Ako je "available" prosleđen, filtriraj i po njemu.
# Ako nema nijedne, vrati False.
@app.get("/authors/{author}/books")
def author_books(
    author: str,
    available: bool | None = None,
    session: Session = Depends(get_session),
):
    statement = select(Book).where(Book.author == author)
    if available is not None:
        statement = statement.where(Book.available == available)
    result = session.exec(statement).all()
    if not result:
        return False
    return result


# Zadatak 26
# GET /genres/{genre}/books?min_rating=4.5
# Vrati knjige datog žanra. Ako je "min_rating" prosleđen, filtriraj i po njemu.
# Ako nema nijedne, vrati False.
@app.get("/genres/{genre}/books")
def genre_books(
    genre: str,
    min_rating: float | None = None,
    session: Session = Depends(get_session),
):
    statement = select(Book).where(Book.genre == genre)
    if min_rating is not None:
        statement = statement.where(Book.rating >= min_rating)
    result = session.exec(statement).all()
    if not result:
        return False
    return result


# Zadatak 27
# GET /genres/{genre}/top?limit=3
# Vrati "limit" knjiga datog žanra sa najvećom ocenom.
# "limit" je opcioni, podrazumevano 3.
# Ako žanr nema nijednu knjigu ili je limit manji od 1, vrati False.
@app.get("/genres/{genre}/top")
def genre_top(
    genre: str,
    limit: int | None = None,
    session: Session = Depends(get_session),
):
    if limit is None:
        limit = 3
    if limit < 1:
        return False
    statement = select(Book).where(Book.genre == genre).order_by(desc(Book.rating)).limit(limit)
    result = session.exec(statement).all()
    if not result:
        return False
    return result


# Zadatak 28
# GET /years/{year}/books?before=true
# Ako je before=true, vrati knjige objavljene pre date godine.
# Ako je before=false, vrati knjige objavljene te godine ili kasnije.
# Ako "before" nije prosleđen, vrati knjige objavljene tačno te godine.
# Ako nema nijedne, vrati False.
@app.get("/years/{year}/books")
def books_around_year(
    year: int,
    before: bool | None = None,
    session: Session = Depends(get_session),
):
    if before is None:
        statement = select(Book).where(Book.year == year)
    elif before:
        statement = select(Book).where(Book.year < year)
    else:
        statement = select(Book).where(Book.year >= year)
    result = session.exec(statement).all()
    if not result:
        return False
    return result


# Zadatak 29
# GET /genres/{genre}/search?title=Harry
# Vrati knjige datog žanra čiji naslov sadrži dati tekst.
# "title" je opcioni: ako nije prosleđen, vrati sve knjige tog žanra.
# Ako nema nijedne, vrati False.
@app.get("/genres/{genre}/search")
def genre_search(
    genre: str,
    title: str | None = None,
    session: Session = Depends(get_session),
):
    statement = select(Book).where(Book.genre == genre)
    if title is not None:
        statement = statement.where(Book.title.contains(title))
    result = session.exec(statement).all()
    if not result:
        return False
    return result


# Zadatak 30
# GET /books/{book_id}/similar?limit=3
# Vrati druge knjige istog žanra kao data knjiga (bez same te knjige).
# Ako je "limit" prosleđen, vrati najviše toliko knjiga.
# Ako knjiga ne postoji ili je limit manji od 1, vrati False.
@app.get("/books/{book_id}/similar")
def similar_books(
    book_id: int,
    limit: int | None = None,
    session: Session = Depends(get_session),
):
    if limit is not None and limit < 1:
        return False
    statement = select(Book).where(Book.id == book_id)
    result = session.exec(statement).all()
    if not result:
        return False
    book = result[0]
    statement = select(Book).where(Book.genre == book.genre, Book.id != book_id)
    if limit is not None:
        statement = statement.limit(limit)
    result = session.exec(statement).all()
    return result
