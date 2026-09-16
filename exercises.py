from fastapi import FastAPI

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
def get_books():
    return BOOKS


# Zadatak 3
# GET /books/count
# Vrati broj knjiga, npr. {"count": 20}
@app.get("/books/count")
def count_books():
    return {"count": len(BOOKS)}


# Zadatak 4
# GET /books/first
# Vrati prvu knjigu iz liste.
@app.get("/books/first")
def first_book():
    return BOOKS[0]


# Zadatak 5
# GET /books/last
# Vrati poslednju knjigu iz liste.
@app.get("/books/last")
def last_book():
    return BOOKS[-1]


# Zadatak 6
# GET /books/titles
# Vrati listu samo sa naslovima svih knjiga.
@app.get("/books/titles")
def book_titles():
    titles = []
    for book in BOOKS:
        titles.append(book["title"])
    return titles


# Zadatak 7
# GET /books/available
# Vrati samo knjige koje su dostupne.
@app.get("/books/available")
def available_books():
    result = []
    for book in BOOKS:
        if book["available"]:
            result.append(book)
    return result


# Zadatak 8
# GET /books/best
# Vrati knjigu sa najvećom ocenom.
@app.get("/books/best")
def best_book():
    best = BOOKS[0]
    for book in BOOKS:
        if book["rating"] > best["rating"]:
            best = book
    return best


# Zadatak 9
# GET /authors
# Vrati listu svih autora, bez duplikata.
@app.get("/authors")
def get_authors():
    authors = []
    for book in BOOKS:
        if book["author"] not in authors:
            authors.append(book["author"])
    return authors


# =============================================================================
# DEO 2: PATH PARAMETRI
# =============================================================================

# Zadatak 10
# GET /books/{book_id}
# Vrati knjigu sa datim id-jem.
# Ako ne postoji, vrati False.
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return False


# Zadatak 11
# GET /books/{book_id}/title
# Vrati samo naslov knjige sa datim id-jem, npr. {"title": "1984"}
# Ako ne postoji, vrati False.
@app.get("/books/{book_id}/title")
def get_book_title(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            return {"title": book["title"]}
    return False


# Zadatak 12
# GET /books/title/{title}
# Vrati knjigu sa datim naslovom (ignoriši velika/mala slova).
# Ako ne postoji, vrati False.
@app.get("/books/title/{title}")
def get_book_by_title(title: str):
    for book in BOOKS:
        if book["title"].lower() == title.lower():
            return book
    return False


# Zadatak 13
# GET /books/author/{author}
# Vrati sve knjige datog autora (ignoriši velika/mala slova).
# Ako nema nijedne, vrati False.
@app.get("/books/author/{author}")
def get_books_by_author(author: str):
    result = []
    for book in BOOKS:
        if book["author"].lower() == author.lower():
            result.append(book)
    if not result:
        return False
    return result


# Zadatak 14
# GET /books/genre/{genre}
# Vrati sve knjige datog žanra (ignoriši velika/mala slova).
# Ako nema nijedne, vrati False.
@app.get("/books/genre/{genre}")
def get_books_by_genre(genre: str):
    result = []
    for book in BOOKS:
        if book["genre"].lower() == genre.lower():
            result.append(book)
    if not result:
        return False
    return result


# Zadatak 15
# GET /books/year/{year}
# Vrati sve knjige objavljene date godine.
# Ako nema nijedne, vrati False.
@app.get("/books/year/{year}")
def get_books_by_year(year: int):
    result = []
    for book in BOOKS:
        if book["year"] == year:
            result.append(book)
    if not result:
        return False
    return result


# Zadatak 16
# GET /books/{book_id}/is-available
# Vrati {"available": True} ili {"available": False} za datu knjigu.
# Ako knjiga ne postoji, vrati False.
@app.get("/books/{book_id}/is-available")
def is_book_available(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            return {"available": book["available"]}
    return False


# =============================================================================
# DEO 3: QUERY PARAMETRI
# =============================================================================

# Zadatak 17
# GET /search?title=potter
# Vrati sve knjige čiji naslov sadrži dati tekst (ignoriši velika/mala slova).
# Ako nema nijedne, vrati False.
@app.get("/search")
def search_books(title: str):
    result = []
    for book in BOOKS:
        if title.lower() in book["title"].lower():
            result.append(book)
    if not result:
        return False
    return result


# Zadatak 18
# GET /filter/rating?min_rating=4.5
# Vrati sve knjige sa ocenom većom ili jednakom min_rating.
# Ako min_rating nije između 0 i 5, vrati False.
@app.get("/filter/rating")
def filter_by_rating(min_rating: float):
    if min_rating < 0 or min_rating > 5:
        return False
    result = []
    for book in BOOKS:
        if book["rating"] >= min_rating:
            result.append(book)
    return result


# Zadatak 19
# GET /filter/available?available=true
# Vrati knjige kod kojih se "available" poklapa sa query parametrom.
@app.get("/filter/available")
def filter_by_available(available: bool):
    result = []
    for book in BOOKS:
        if book["available"] == available:
            result.append(book)
    return result


# Zadatak 20
# GET /filter/pages?min_pages=200&max_pages=400
# Vrati knjige sa brojem strana između min_pages i max_pages (uključujući i njih).
# Oba parametra su opciona: min_pages je podrazumevano 0, max_pages je podrazumevano 1000.
# Ako je min_pages veće od max_pages, vrati False.
@app.get("/filter/pages")
def filter_by_pages(min_pages: int = 0, max_pages: int = 1000):
    if min_pages > max_pages:
        return False
    result = []
    for book in BOOKS:
        if min_pages <= book["pages"] <= max_pages:
            result.append(book)
    return result


# Zadatak 21
# GET /filter/years?start=1900&end=2000
# Vrati knjige objavljene između start i end (uključujući i njih).
# Ako je start veće od end, vrati False.
@app.get("/filter/years")
def filter_by_years(start: int, end: int):
    if start > end:
        return False
    result = []
    for book in BOOKS:
        if start <= book["year"] <= end:
            result.append(book)
    return result


# Zadatak 22
# GET /paginate?skip=0&limit=5
# Preskoči prvih "skip" knjiga i vrati sledećih "limit" knjiga.
# Podrazumevano: skip=0, limit=5.
# Ako je skip ili limit negativan, vrati False.
@app.get("/paginate")
def paginate_books(skip: int = 0, limit: int = 5):
    if skip < 0 or limit < 0:
        return False
    return BOOKS[skip:skip + limit]


# Zadatak 23
# GET /sort?by=year&order=asc
# Vrati sve knjige sortirane po datom polju.
# "by" može biti: title, year, pages, rating (podrazumevano: title)
# "order" može biti: asc, desc (podrazumevano: asc)
# Ako "by" ili "order" ima neku drugu vrednost, vrati False.
@app.get("/sort")
def sort_books(by: str = "title", order: str = "asc"):
    if by not in ["title", "year", "pages", "rating"]:
        return False
    if order not in ["asc", "desc"]:
        return False
    return sorted(BOOKS, key=lambda book: book[by], reverse=(order == "desc"))


# Zadatak 24
# GET /filter?genre=classic&available=true&min_rating=4
# Svi parametri su opcioni. Primeni samo filtere koji su prosleđeni.
@app.get("/filter")
def filter_books(genre: str | None = None, available: bool | None = None, min_rating: float | None = None):
    result = []
    for book in BOOKS:
        if genre is not None and book["genre"].lower() != genre.lower():
            continue
        if available is not None and book["available"] != available:
            continue
        if min_rating is not None and book["rating"] < min_rating:
            continue
        result.append(book)
    return result


# =============================================================================
# DEO 4: PATH + QUERY PARAMETRI ZAJEDNO
# =============================================================================

# Zadatak 25
# GET /authors/{author}/books?available=true
# Vrati knjige datog autora, filtrirane po dostupnosti.
# Ako autor nema nijednu knjigu, vrati False.
@app.get("/authors/{author}/books")
def author_books(author: str, available: bool | None = None):
    result = []
    for book in BOOKS:
        if book["author"].lower() != author.lower():
            continue
        if available is not None and book["available"] != available:
            continue
        result.append(book)
    if not result:
        return False
    return result


# Zadatak 26
# GET /genres/{genre}/books?min_rating=4.5
# Vrati knjige datog žanra sa ocenom >= min_rating (podrazumevano 0).
# Ako nema nijedne, vrati False.
@app.get("/genres/{genre}/books")
def genre_books(genre: str, min_rating: float = 0):
    result = []
    for book in BOOKS:
        if book["genre"].lower() == genre.lower() and book["rating"] >= min_rating:
            result.append(book)
    if not result:
        return False
    return result


# Zadatak 27
# GET /genres/{genre}/sorted?by=rating&order=desc
# Vrati knjige datog žanra sortirane po datom polju.
# "by" može biti: title, year, pages, rating (podrazumevano: rating)
# "order" može biti: asc, desc (podrazumevano: desc)
# Ako žanr nema nijednu knjigu, ili je "by"/"order" neispravan, vrati False.
@app.get("/genres/{genre}/sorted")
def genre_sorted(genre: str, by: str = "rating", order: str = "desc"):
    if by not in ["title", "year", "pages", "rating"]:
        return False
    if order not in ["asc", "desc"]:
        return False
    result = []
    for book in BOOKS:
        if book["genre"].lower() == genre.lower():
            result.append(book)
    if not result:
        return False
    return sorted(result, key=lambda book: book[by], reverse=(order == "desc"))


# Zadatak 28
# GET /years/{year}/books?before=true
# Ako je before=true, vrati knjige objavljene pre date godine.
# Ako je before=false, vrati knjige objavljene te godine ili kasnije.
# Podrazumevano: before=true.
# Ako nema nijedne, vrati False.
@app.get("/years/{year}/books")
def books_around_year(year: int, before: bool = True):
    result = []
    for book in BOOKS:
        if before and book["year"] < year:
            result.append(book)
        if not before and book["year"] >= year:
            result.append(book)
    if not result:
        return False
    return result


# Zadatak 29
# GET /books/{book_id}/field?name=author
# Vrati samo jedno polje knjige, npr. {"author": "George Orwell"}
# Ako knjiga ne postoji ili polje ne postoji, vrati False.
@app.get("/books/{book_id}/field")
def book_field(book_id: int, name: str):
    for book in BOOKS:
        if book["id"] == book_id:
            if name not in book:
                return False
            return {name: book[name]}
    return False


# Zadatak 30
# GET /books/{book_id}/similar?limit=3
# Vrati druge knjige istog žanra kao data knjiga (bez same te knjige).
# Vrati najviše "limit" knjiga (podrazumevano 3).
# Ako knjiga ne postoji ili je limit manji od 1, vrati False.
@app.get("/books/{book_id}/similar")
def similar_books(book_id: int, limit: int = 3):
    if limit < 1:
        return False
    current = None
    for book in BOOKS:
        if book["id"] == book_id:
            current = book
    if current is None:
        return False
    result = []
    for book in BOOKS:
        if book["genre"] == current["genre"] and book["id"] != book_id:
            result.append(book)
    return result[:limit]
