import os

from db_crud import FiszkaCRUD
from models import session


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def menu():
    db = FiszkaCRUD(session)
    while True:
        print("\nMenu:")
        print("1. Wypisz wszystkie fiszki")
        print("2. Dodaj nową fiszkę")
        print("3. Usuń fiszkę po pytaniu")
        print("4. Usuń fiszkę po ID")
        print("5. Edytuj fiszkę")
        print("0. Wyjdź")

        choice = input("Wybierz opcję: ")
        if choice == "1":
            clear_terminal()
            db.wypisz_fiszki()
        elif choice == "2":
            clear_terminal()
            question = input("Podaj pytanie: ")
            answer = input("Podaj odpowiedź: ")
            db.nowa_Fiszka(question, answer)
        elif choice == "3":
            clear_terminal()
            question = input("Podaj pytanie fiszki do usunięcia: ")
            db.usun_fiszke(question)
        elif choice == "4":
            try:
                clear_terminal()
                fiszka_id = int(input("Podaj ID fiszki do usunięcia: "))
                db.usun_fiszke_po_id(fiszka_id)
            except ValueError:
                print("Nieprawidłowe ID. Proszę podać liczbę.")
        elif choice == "5":
            try:
                clear_terminal()
                fiszka_id = int(input("Podaj ID fiszki do edycji: "))
                new_question = input(
                    "Podaj nowe pytanie (lub zostaw puste, aby nie zmieniać): "
                )
                new_answer = input(
                    "Podaj nową odpowiedź (lub zostaw puste, aby nie zmieniać): "
                )
                db.edytuj_fiszke(fiszka_id, new_question, new_answer)
            except ValueError:
                print("Nieprawidłowe ID. Proszę podać liczbę.")
        elif choice == "0":
            print("Do widzenia!")
            session.close()
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")
