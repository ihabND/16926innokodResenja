from knjiga_app_2 import Author, Book, engine
from sqlmodel import select, func, Session, select
from sqlalchemy import desc


def print_results(comment, data):
    """Print a comment/title, then loop through the result(s) and print each one."""
    print(comment)
    if isinstance(data, list):
        for item in data:
            print(item)
    else:
        print(data)
    print("-----------------------------------")


with Session(engine) as session:

    ### Get all authors
    statement = select(Author)
    authors = session.exec(statement).all()
    print_results("### Get all authors", authors)

    ### Get all books
    statement = select(Book)
    books = session.exec(statement).all()
    print_results("### Get all books", books)

    ### Find an author by ID
    statement = select(Author).where(Author.id == 3)
    author = session.exec(statement).first()
    print_results("### Find an author by ID = 3", author)

    ### Find a book by title
    statement = select(Book).where(Book.naslov == "1984")
    book = session.exec(statement).first()
    print_results("### Find a book by title", book)

    ### Find books with rating >= 4.5
    statement = select(Book).where(Book.ocena >= 4.5)
    books = session.exec(statement).all()
    print_results("### Find books with rating >= 4.5", books)

    ### Find available books
    statement = select(Book).where(Book.dostupna == True)
    books = session.exec(statement).all()
    print_results("### Find available books", books)

    ### Find unavailable books
    statement = select(Book).where(Book.dostupna == False)
    books = session.exec(statement).all()
    print_results("### Find unavailable books", books)

    ### Find books with more than 400 pages
    statement = select(Book).where(Book.broj_strana > 400)
    books = session.exec(statement).all()
    print_results("### Find books with more than 400 pages", books)

    ### Find fantasy books
    statement = select(Book).where(Book.zanr == "Fantasy")
    books = session.exec(statement).all()
    print_results("### Find fantasy books", books)

    ### Find authors born before 1900
    statement = select(Author).where(Author.godina_rodjenja < 1900)
    authors = session.exec(statement).all()
    print_results("### Find authors born before 1900", authors)

    ### Find available books with rating >= 4.5
    statement = select(Book).where(
        Book.dostupna == True,
        Book.ocena >= 4.5
    )
    books = session.exec(statement).all()
    print_results("### Find available books with rating >= 4.5", books)

    ### Find books between 200 and 400 pages
    statement = select(Book).where(
        Book.broj_strana >= 200,
        Book.broj_strana <= 400
    )
    books = session.exec(statement).all()
    print_results("### Find books between 200 and 400 pages", books)

    ### Find highly rated fantasy books
    statement = select(Book).where(
        Book.zanr == "Fantasy",
        Book.ocena >= 4.7
    )
    books = session.exec(statement).all()
    print_results("### Find highly rated fantasy books", books)

    ### Find books by George Orwell
    statement = select(Book).where(Book.autor_id == 2)
    books = session.exec(statement).all()
    print_results("### Find books by George Orwell", books)

    ### Order books by rating, highest first
    statement = select(Book).order_by(desc(Book.ocena))
    books = session.exec(statement).all()
    print_results("### Order books by rating, highest first", books)

    ### Order books by page count
    statement = select(Book).order_by(Book.broj_strana)
    books = session.exec(statement).all()
    print_results("### Order books by page count", books)

    ### Order authors by year of birth
    statement = select(Author).order_by(Author.godina_rodjenja)
    authors = session.exec(statement).all()
    print_results("### Order authors by year of birth", authors)

    ### Get the top 5 highest-rated books
    statement = (
        select(Book)
        .order_by(desc(Book.ocena))
        .limit(5)
    )
    books = session.exec(statement).all()
    print_results("### Get the top 5 highest-rated books", books)

    ### Find titles containing "The"
    statement = select(Book).where(Book.naslov.contains("The"))
    books = session.exec(statement).all()
    print_results('### Find titles containing "The"', books)

    ### Find authors whose last name starts with "S"
    statement = select(Author).where(Author.prezime.startswith("S"))
    authors = session.exec(statement).all()
    print_results('### Find authors whose last name starts with "S"', authors)

    ### Find titles containing "King"
    statement = select(Book).where(Book.naslov.contains("King"))
    books = session.exec(statement).all()
    print_results('### Find titles containing "King"', books)

    ### Get books together with their authors
    statement = (
        select(Book, Author)
        .join(Author, Book.autor_id == Author.id)
    )
    results = session.exec(statement).all()
    print_results("### Get books together with their authors", results)

    for book, author in results:
        print(book.naslov, "-", author.ime, author.prezime)

    ### Find books written by Jane Austen
    statement = (
        select(Book)
        .join(Author)
        .where(Author.prezime == "Austen")
    )
    books = session.exec(statement).all()
    print_results("### Find books written by Jane Austen", books)

    ### Find books written by Mark Twain
    statement = (
        select(Book)
        .join(Author)
        .where(
            Author.ime == "Mark",
            Author.prezime == "Twain"
        )
    )
    books = session.exec(statement).all()
    print_results("### Find books written by Mark Twain", books)

    ### Find highly rated books with author information
    statement = (
        select(Book, Author)
        .join(Author)
        .where(Book.ocena >= 4.7)
        .order_by(desc(Book.ocena))
    )
    results = session.exec(statement).all()
    print_results("### Find highly rated books with author information", results)

    ### Count all books
    statement = select(func.count(Book.id))
    count = session.exec(statement).one()
    print_results("### Count all books", count)

    ### Count all authors
    statement = select(func.count(Author.id))
    count = session.exec(statement).one()
    print_results("### Count all authors", count)

    ### Calculate the average book rating
    statement = select(func.avg(Book.ocena))
    average_rating = session.exec(statement).one()
    print_results("### Calculate the average book rating", average_rating)

    ### Find the maximum number of pages
    statement = select(func.max(Book.broj_strana))
    max_pages = session.exec(statement).one()
    print_results("### Find the maximum number of pages", max_pages)

    ### Find the minimum number of pages
    statement = select(func.min(Book.broj_strana))
    min_pages = session.exec(statement).one()
    print_results("### Find the minimum number of pages", min_pages)

    ### Count books per author
    statement = (
        select(
            Author.ime,
            Author.prezime,
            func.count(Book.id)
        )
        .join(Book)
        .group_by(Author.id)
    )
    results = session.exec(statement).all()
    print_results("### Count books per author", results)

    ### Calculate average rating per author
    statement = (
        select(
            Author.ime,
            Author.prezime,
            func.avg(Book.ocena)
        )
        .join(Book)
        .group_by(Author.id)
    )
    results = session.exec(statement).all()
    print_results("### Calculate average rating per author", results)

    ### Count books per genre
    statement = (
        select(
            Book.zanr,
            func.count(Book.id)
        )
        .group_by(Book.zanr)
    )
    results = session.exec(statement).all()
    print_results("### Count books per genre", results)

    ### Calculate average rating per genre
    statement = (
        select(
            Book.zanr,
            func.avg(Book.ocena)
        )
        .group_by(Book.zanr)
    )
    results = session.exec(statement).all()
    print_results("### Calculate average rating per genre", results)

    ### Find authors with at least 5 books
    statement = (
        select(
            Author.ime,
            Author.prezime,
            func.count(Book.id).label("book_count")
        )
        .join(Book)
        .group_by(Author.id)
        .having(func.count(Book.id) >= 5)
    )
    results = session.exec(statement).all()
    print_results("### Find authors with at least 5 books", results)

    ### Find genres with at least 3 books
    statement = (
        select(
            Book.zanr,
            func.count(Book.id).label("book_count")
        )
        .group_by(Book.zanr)
        .having(func.count(Book.id) >= 3)
    )
    results = session.exec(statement).all()
    print_results("### Find genres with at least 3 books", results)

    ### Find books rated above the overall average
    average_rating = select(func.avg(Book.ocena)).scalar_subquery()

    statement = select(Book).where(
        Book.ocena > average_rating
    )
    books = session.exec(statement).all()
    print_results("### Find books rated above the overall average", books)

    ### Find books with more pages than the average book
    average_pages = select(func.avg(Book.broj_strana)).scalar_subquery()

    statement = select(Book).where(
        Book.broj_strana > average_pages
    )
    books = session.exec(statement).all()
    print_results("### Find books with more pages than the average book", books)

    ### Find authors with at least one book rated >= 4.8
    high_rated_author_ids = (
        select(Book.autor_id)
        .where(Book.ocena >= 4.8)
        .distinct()
    )

    statement = select(Author).where(
        Author.id.in_(high_rated_author_ids)
    )
    authors = session.exec(statement).all()
    print_results("### Find authors with at least one book rated >= 4.8", authors)

    ### Find the best-rated book for each author
    statement = (
        select(
            Author.ime,
            Author.prezime,
            func.max(Book.ocena).label("best_rating")
        )
        .join(Book)
        .group_by(Author.id)
    )
    results = session.exec(statement).all()
    print_results("### Find the best-rated book for each author", results)

    ### Find authors with average rating >= 4.5
    statement = (
        select(
            Author.ime,
            Author.prezime,
            func.avg(Book.ocena).label("average_rating")
        )
        .join(Book)
        .group_by(Author.id)
        .having(func.avg(Book.ocena) >= 4.5)
    )
    results = session.exec(statement).all()
    print_results("### Find authors with average rating >= 4.5", results)

    ### Find available books rated above average
    average_rating = select(func.avg(Book.ocena)).scalar_subquery()

    statement = select(Book).where(
        Book.dostupna == True,
        Book.ocena > average_rating
    )
    books = session.exec(statement).all()
    print_results("### Find available books rated above average", books)

    ### Find authors with a book longer than 500 pages
    long_book_authors = (
        select(Book.autor_id)
        .where(Book.broj_strana > 500)
        .distinct()
    )

    statement = select(Author).where(
        Author.id.in_(long_book_authors)
    )
    authors = session.exec(statement).all()
    print_results("### Find authors with a book longer than 500 pages", authors)

    ### Get the top 10 books with author information
    statement = (
        select(Book, Author)
        .join(Author)
        .order_by(desc(Book.ocena), desc(Book.broj_strana))
        .limit(10)
    )
    results = session.exec(statement).all()
    print_results("### Get the top 10 books with author information", results)

    ### Count available books grouped by genre
    statement = (
        select(
            Book.zanr,
            func.count(Book.id)
        )
        .where(Book.dostupna == True)
        .group_by(Book.zanr)
    )
    results = session.exec(statement).all()
    print_results("### Count available books grouped by genre", results)

    ### Find the author with the highest average rating
    statement = (
        select(
            Author.ime,
            Author.prezime,
            func.avg(Book.ocena).label("avg_rating")
        )
        .join(Book)
        .group_by(Author.id)
        .order_by(desc("avg_rating"))
        .limit(1)
    )
    result = session.exec(statement).first()
    print_results("### Find the author with the highest average rating", result)

    ### Find the genre with the highest average rating
    statement = (
        select(
            Book.zanr,
            func.avg(Book.ocena).label("avg_rating")
        )
        .group_by(Book.zanr)
        .order_by(desc("avg_rating"))
        .limit(1)
    )
    result = session.exec(statement).first()
    print_results("### Find the genre with the highest average rating", result)

    ### Find authors whose average rating is above the overall average
    overall_average = select(
        func.avg(Book.ocena)
    ).scalar_subquery()

    statement = (
        select(
            Author.ime,
            Author.prezime,
            func.avg(Book.ocena).label("avg_rating")
        )
        .join(Book)
        .group_by(Author.id)
        .having(func.avg(Book.ocena) > overall_average)
    )
    results = session.exec(statement).all()
    print_results("### Find authors whose average rating is above the overall average", results)

    ### Find the longest available book
    statement = (
        select(Book, Author)
        .join(Author)
        .where(Book.dostupna == True)
        .order_by(desc(Book.broj_strana))
        .limit(1)
    )
    result = session.exec(statement).first()
    print_results("### Find the longest available book", result)

    ### Find authors with a highly rated book and an unavailable book
    high_rating_authors = (
        select(Book.autor_id)
        .where(Book.ocena >= 4.7)
        .distinct()
    )

    unavailable_authors = (
        select(Book.autor_id)
        .where(Book.dostupna == False)
        .distinct()
    )

    statement = select(Author).where(
        Author.id.in_(high_rating_authors),
        Author.id.in_(unavailable_authors)
    )
    authors = session.exec(statement).all()
    print_results("### Find authors with a highly rated book and an unavailable book", authors)