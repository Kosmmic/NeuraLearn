import os

from db_crud import FiszkaCRUD, UserCRUD
from models import session


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


class FiszkaCLI:
    def __init__(self, db):
        self.db = db

    def handle_add_fiszka(self):
        question = input("Podaj pytanie: ")
        answer = input("Podaj odpowiedź: ")
        self.db.dodaj(question=question, answer=answer)

    def handle_delete_fiszka_by_question(self):
        try:
            question = input("Podaj pytanie fiszki do usunięcia: ")
            self.db.usun(question, way="question")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    def handle_delete_fiszka_by_id(self):
        try:
            fiszka_id = int(input("Podaj ID fiszki do usunięcia: "))
            self.db.usun(fiszka_id, way="id")
        except ValueError:
            print("Nieprawidłowe ID. Proszę podać liczbę.")

    def handle_edit_fiszka(self):
        try:
            fiszka_id = int(input("Podaj ID fiszki do edycji: "))
            new_question = input(
                "Podaj nowe pytanie (lub zostaw puste, aby nie zmieniać): "
            )
            new_answer = input(
                "Podaj nową odpowiedź (lub zostaw puste, aby nie zmieniać): "
            )
            updates = {}
            if new_question.strip():
                updates["question"] = new_question.strip()
            if new_answer.strip():
                updates["answer"] = new_answer.strip()
            if not updates:
                print("Brak zmian do zapisania.")
                return
            if not self.db.edytuj(fiszka_id, **updates):
                print(f"Nie znaleziono fiszki o ID {fiszka_id}.")
        except ValueError:
            print("Nieprawidłowe ID. Proszę podać liczbę.")


class UserCLI:
    def __init__(self, db):
        self.db = db

    def handle_add_user(self):
        pass

    def handle_delete_user(self):
        pass

    def handle_delete_user_by_ID(self):
        pass

    def handle_edit_ser(self):
        pass


def menu(actions, title="Menu"):
    while True:
        print(f"\n=== {title} ===")
        for key, value in actions.items():
            print(f"{key}. {value['label']}")

        choice = input("\nWybierz opcję: ")
        if choice == "0":
            break

        if choice in actions:
            clear_terminal()
            akcja = actions[choice]["action"]
            try:
                if akcja is not None:
                    akcja()
            except Exception as e:
                print(f"\nWystąpił błąd: {e}")
        else:
            print("\nNieprawidłowy wybór. Spróbuj ponownie.")


fiszka_cli = FiszkaCLI(FiszkaCRUD(session))
user_cli = UserCLI(UserCRUD(session))

MENU_FISZKA = {
    "1": {
        "label": "Wyświetl wszystkie",
        "action": lambda: fiszka_cli.db.wypisz_wszystkie(),
    },
    "2": {"label": "Dodaj nową", "action": fiszka_cli.handle_add_fiszka},
    "3": {
        "label": "Usuń po pytaniu",
        "action": fiszka_cli.handle_delete_fiszka_by_question,
    },
    "4": {"label": "Usuń po ID", "action": fiszka_cli.handle_delete_fiszka_by_id},
    "5": {"label": "Edytuj fiszkę", "action": fiszka_cli.handle_edit_fiszka},
    "0": {"label": "Wyjdź", "action": None},
}

MENU_USER = {
    "1": {
        "label": "Wyświetl użytkowników",
        "action": lambda: user_cli.db.wypisz_wszystkie(),
    },
    "2": {"label": "Dodaj użytkownika", "action": user_cli.handle_add_user},
    "0": {"label": "Powrót", "action": None},
}

MENU_GLOWNE = {
    "1": {
        "label": "Zarządzaj Fiszkami",
        "action": lambda: menu(MENU_FISZKA, "Menu Fiszki"),
    },
    "2": {
        "label": "Zarządzaj Użytkownikami",
        "action": lambda: menu(MENU_USER, "Menu Użytkownicy"),
    },
    "0": {"label": "Wyjdź z programu", "action": None},
}
