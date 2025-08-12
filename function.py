import json
import random
from classes import Book, Author, Student, Admin


def read_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def write_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def generate_id(prefix):
   return prefix + str(random.randint(100000000, 999999999))

def login(user_type, file):
    data = read_json(file)
    user_id = input("entrez votre ID: ")
    password = input("entrez votre mot de passe: ")
    for u in data:
        if u["id"] == user_id and u["password"] == password:
            if user_type == "admin":
                return Admin(u["name"], u["email"], u["password"])
            elif user_type == "student":
                return Student(u["name"], u["password"], u["books"])
    print("Identifiants invalides")
    return None



def add_book(file_books):
    books = read_json(file_books)
    name = input("nom du livre: ")
    desc = input("description: ")
    booknbr = int(input("nombre initial d'exemplaires: "))
    book_id = generate_id("BK")
    new_book = {
        "id": book_id,
        "name": name,
        "description": desc,
        "authors": [],
        "booknbr": booknbr,
        "rembks": booknbr,
    }
    books.append(new_book)
    write_json(file_books, books)
    print(f"Livre '{name}' ajouté avec succès avec ID {book_id}.")

def search_books(file_books):
    books = read_json(file_books)
    query = input("rechercher un livre: ").lower()
    results = [b for b in books if query in b["name"].lower()]
    for b in results:
        print(f"{b['id']} - {b['name']} ({b['rembks']}/{b['booknbr']})")
    if not results:
        print("Aucun livre trouvé.")

def borrow_book(file_books, file_students, student):
    books = read_json(file_books)
    students = read_json(file_students)
    search_books(file_books)
    book_id = input("Entrez l'ID du livre à emprunter: ")

    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        print("Livre introuvable")
        return
    if book["rembks"] <= 0:
        print("Aucun exemplaire disponible")
        return
    if len(student.books) >= 3:
        print("Vous avez déjà emprunté 3 livres")
        return

    book["rembks"] -= 1
    student.books.append(book_id)

    for s in students:
        if s["id"] == student.id:
            s["books"] = student.books
    write_json(file_books, books)
    write_json(file_students, students)
    print(f"Livre {book['name']} emprunté avec succès")

def return_book(file_books, file_students, student):
    books = read_json(file_books)
    students = read_json(file_students)
    if not student.books:
        print("Vous n'avez aucun livre à rendre")
        return
    print("Vos livres empruntés :")
    for b_id in student.books:
        book = next((b for b in books if b["id"] == b_id), None)
        if book:
            print(f"{book['name']}")
    book_id = input("Entrez l'ID du livre à rendre: ")
    if book_id not in student.books:
        print("Ce livre n'est pas dans vos emprunts")
        return
    student.books.remove(book_id)
    for b in books:
        if b["id"] == book_id:
            b["rembks"] += 1
    for s in students:
        if s["id"] == student.id:
            s["books"] = student.books
    write_json(file_books, books)
    write_json(file_students, students)
    print("Livre rendu avec succès")
