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
        self.db.nowa_Fiszka(question, answer)

    def handle_delete_fiszka_by_question(self):
        try:
            question = input("Podaj pytanie fiszki do usunięcia: ")
            self.db.usun_fiszke(question)
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    def handle_delete_fiszka_by_id(self):
        try:
            fiszka_id = int(input("Podaj ID fiszki do usunięcia: "))
            self.db.usun_fiszke_po_id(fiszka_id)
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
            self.db.edytuj_fiszke(fiszka_id, new_question, new_answer)
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


MENU_FISZKA = {
    "1": {"label": "Wyświetl wszystkie", "action": lambda: FiszkaCLI.wypisz_fiszki},
    "2": {"label": "Dodaj nową", "action": FiszkaCLI.handle_add_fiszka},
    "3": {
        "label": "Usuń po pytaniu",
        "action": FiszkaCLI.handle_delete_fiszka_by_question,
    },
    "4": {"label": "Usuń po ID", "action": FiszkaCLI.handle_delete_fiszka_by_id},
    "5": {"label": "Edytuj fiszkę", "action": FiszkaCLI.handle_edit_fiszka},
    "0": {"label": "Wyjdź", "action": None},
}

MENU_USER = {
    "1": {
        "label": "Wyświetl użytkowników",
        "action": lambda: cli_user.db.wypisz_uzytkownikow(),
    },
    "2": {"label": "Dodaj użytkownika", "action": cli_user.handle_add_user},
    # ... reszta opcji
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


def menu(actions, title="Menu"):
    while True:
        print("\n=== {title} ===")
        for key, value in actions.items():
            print(f"{key}. {value['label']}")

        choice = input("\nWybierz opcję: ")
        if choice == "0":
            break

        if choice in actions:
            clear_terminal()
            akcja = actions[choice]["action"]
            try:
                akcja()
            except Exception as e:
                print(f"\nWystąpił błąd: {e}")
        else:
            print("\nNieprawidłowy wybór. Spróbuj ponownie.")


user_cli = UserCLI(UserCRUD(session))
fiszka_cli = FiszkaCLI(FiszkaCRUD(session))
