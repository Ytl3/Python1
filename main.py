from function import login, add_book, search_books, borrow_book, return_book

FILE_ADMINS = "admins.json"
FILE_STUDENTS = "students.json"
FILE_BOOKS = "books.json"
FILE_AUTHORS = "authors.json"

def admin_menu(admin):
    while True:
        print("\n--- Menu Admin ---")
        print("1. Ajouter un livre")
        print("2. Rechercher un livre")
        print("3. Déconnexion")
        choice = input("Choix: ")
        if choice == "1":
            add_book(FILE_BOOKS)
        elif choice == "2":
            search_books(FILE_BOOKS)
        elif choice == "3":
            break
        else:
            print("Choix invalide.")

def student_menu(student):
    while True:
        print("\n--- Menu Étudiant ---")
        print("1. Rechercher un livre")
        print("2. Emprunter un livre")
        print("3. Rendre un livre")
        print("4. Déconnexion")
        choice = input("Choix: ")
        if choice == "1":
            search_books(FILE_BOOKS)
        elif choice == "2":
            borrow_book(FILE_BOOKS, FILE_STUDENTS, student)
        elif choice == "3":
            return_book(FILE_BOOKS, FILE_STUDENTS, student)
        elif choice == "4":
            break
        else:
            print("Choix invalide.")

def main():
    print("=== Bienvenue à la Bibliothèque ===")
    user_type = input("Êtes-vous (A)dmin ou (E)tudiant ? ").lower()
    if user_type == "a":
        admin = login("admin", FILE_ADMINS)
        if admin:
            admin_menu(admin)
    elif user_type == "e":
        student = login("student", FILE_STUDENTS)
        if student:
            student_menu(student)
    else:
        print("Type d'utilisateur invalide.")

if __name__ == "__main__":
    main()
