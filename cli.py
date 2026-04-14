import os
import time

from sqlalchemy.exc import IntegrityError

from app.domain.answer_validation import validate_answer
from app.persistence import get_db_session
from app.services import (
    DeckBuilder,
    ProgressService,
    ReviewService,
    TrainingSessionService,
    import_fiszki_from_path,
)
from db_crud import FiszkaCRUD, ProgressCRUD, UserCRUD
from models import Fiszka, session


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def handle_training_demo():
    """MVP: pełna pętla sesji (pytanie -> ocena -> log + update progress)."""
    raw = input("Podaj ID użytkownika (sesja treningowa): ").strip()
    try:
        user_id = int(raw)
    except ValueError:
        print("To musi być liczba.")
        return
    db = get_db_session()
    try:
        deck = DeckBuilder(db).build_deck(user_id)
    except ValueError as e:
        print(e)
        return
    if not deck:
        print(
            "Talia jest pusta — ten użytkownik nie ma fiszek w nauce "
            "(dodaj postęp w menu „Postęp nauki”)."
        )
        return

    print(f"Talia: {len(deck)} fiszek.")
    svc = TrainingSessionService(db)
    review_svc = ReviewService(db)

    sid = svc.start_training_session(user_id)
    print(f"Rozpoczęto sesję, id={sid}")

    answered = 0
    try:
        for idx, card in enumerate(deck, start=1):
            print(f"\n[{idx}/{len(deck)}] Pytanie: {card.question}")
            cmd = input("Enter = odpowiedz, q = przerwij sesję: ").strip().lower()
            if cmd == "q":
                print("Przerwano sesję przez użytkownika.")
                break
            started = time.perf_counter()
            user_answer = input("Twoja odpowiedź: ").strip()
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            # automatyczna walidacja odpowiedzi usera vs poprawna odpowiedź fiszki
            result = validate_answer(user_answer, card.answer)
            p = review_svc.register_review(
                user_id=user_id,
                fiszka_id=card.id,
                session_id=sid,
                is_correct=result.is_correct,
                response_time_ms=elapsed_ms,
            )
            answered += 1
            print(f"Poprawna odpowiedź: {card.answer}")
            print("Wynik:", "OK" if result.is_correct else "BŁĄD")
            print(
                f"Zapisano: czas={elapsed_ms}ms, "
                f"mastery={p.mastery_level}, next={p.review_date}"
            )
            # pokaz odpowiedzi "na chwilę"
            time.sleep(1.2)
    finally:
        svc.end_training_session(sid)
        print(f"Zakończono sesję id={sid}. Odpowiedziano: {answered}.")


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

    def handle_import_from_file(self):
        """Import z pliku UTF-8 (format jak nauka_ang: ``en;pl``, opcjonalny nagłówek)."""
        raw_path = input(
            'Ścieżka do pliku .txt / .csv (linie: "angielskie;polskie", nagłówek opcjonalny): '
        ).strip()
        path = raw_path.strip('"').strip("'")
        if not path:
            print("Brak ścieżki — anulowano.")
            return
        list_name = input(
            "Nazwa listy w bazie dla NOWYCH fiszek (Enter = tylko bank, bez listy): "
        ).strip()
        mode = (
            input("Pierwsza kolumna = pytanie fiszki (EN)? [t/n, domyślnie t]: ")
            .strip()
            .lower()
        )
        english_as_question = mode != "n"
        db = get_db_session()
        try:
            result = import_fiszki_from_path(
                db,
                path,
                list_name=list_name or None,
                english_as_question=english_as_question,
            )
        except FileNotFoundError:
            print("Nie znaleziono pliku.")
            return
        except Exception as e:
            print(f"Import nie powiódł się: {e}")
            return
        print(
            f"Zakończono import: dodano {result.added}, "
            f"pominięto duplikatów (pytanie już w bazie): {result.skipped_duplicate}, "
            f"pominięto linii bez poprawnej pary: {result.skipped_unparsed}."
        )


class UserCLI:
    def __init__(self, db):
        self.db = db

    def handle_add_user(self):
        try:
            username = input("Wprowadz Login")
            if username.strip() == "":
                print("Musisz podac Login")
                return
            email = input("Wprowadz adres email")
            if email.strip() == "":
                print("Musisz podac email")
                return
            password = input("Wprowadz hasło")
            if password.strip() == "":
                print("Musisz podac hasło")
                return
            password_hash = ""
            username = username.strip()
            email = email.strip()
            self.db.dodaj(username=username, email=email, password_hash=password_hash)
        except IntegrityError:
            print("Login jest zajęty")

    def handle_delete_user(self):
        username = input("Podaj Login użytkownika do usunięcia")
        ok = self.db.usun(username.strip(), way="username")
        if not ok:
            print(f"Nie ma uzytkownika o loginie={username}")

    def handle_delete_user_by_ID(self):
        try:
            user_id = input("Podaj ID użytkownika do usunięcia")
            user_id = user_id.strip()
            user_id = int(user_id)
            ok = self.db.usun(user_id, way="id")
            if not ok:
                print(f"Nie ma uzytkownika o ID: {user_id}")
        except ValueError:
            print("Wprowadzony tekst nie jest liczbą")

    def handle_edit_user(self):
        try:
            user_id = int(input("Podaj ID Usera do edycji: "))
            new_username = input(
                "Podaj nowy Login (lub zostaw puste, aby nie zmieniać): "
            )
            new_email = input(
                "Podaj nowy adres email (lub zostaw puste, aby nie zmieniać): "
            )
            updates = {}
            if new_username.strip():
                updates["username"] = new_username.strip()
            if new_email.strip():
                updates["email"] = new_email.strip()
            if not updates:
                print("Brak zmian do zapisania.")
                return
            if not self.db.edytuj(user_id, **updates):
                print(f"Nie znaleziono użytkownika o ID {user_id}.")
        except ValueError:
            print("Nieprawidłowe ID. Proszę podać liczbę.")


class ProgressCLI:
    def __init__(self, db_session):
        self._session = db_session
        self._svc = ProgressService(db_session)
        self._progress_crud = ProgressCRUD(db_session)

    def handle_add_fiszka_to_learning(self):
        try:
            user_id = int(input("ID użytkownika: ").strip())
            fiszka_id = int(input("ID fiszki (z globalnego banku): ").strip())
        except ValueError:
            print("ID muszą być liczbami całkowitymi.")
            return
        try:
            p = self._svc.add_fiszka_for_user(user_id, fiszka_id)
            print(f"OK — postęp: user_id={p.user_id}, fiszka_id={p.fiszka_id}")
        except ValueError as e:
            print(e)

    def handle_add_all_fiszki_to_learning(self):
        try:
            user_id = int(input("ID użytkownika: ").strip())
        except ValueError:
            print("ID musi być liczbą całkowitą.")
            return
        try:
            added, already = self._svc.add_all_fiszki_for_user(user_id)
            print(f"Dodano nowych powiązań: {added}, już było w nauce: {already}.")
        except ValueError as e:
            print(e)

    def handle_list_progress(self):
        try:
            user_id = int(input("ID użytkownika: ").strip())
        except ValueError:
            print("ID musi być liczbą całkowitą.")
            return
        rows = self._progress_crud.pobierz_dla_uzytkownika(user_id)
        if not rows:
            print("Brak rekordów postępu dla tego użytkownika.")
            return
        for p in rows:
            f = self._session.get(Fiszka, p.fiszka_id)
            q = f.question if f else "?"
            print(
                f"  fiszka_id={p.fiszka_id} | {q!r} | "
                f"mastery={p.mastery_level} | review_date={p.review_date}"
            )


progress_cli = ProgressCLI(session)


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
    "6": {
        "label": "Importuj z pliku (.txt / .csv)",
        "action": fiszka_cli.handle_import_from_file,
    },
    "0": {"label": "Wyjdź", "action": None},
}

MENU_USER = {
    "1": {
        "label": "Wyświetl użytkowników",
        "action": lambda: user_cli.db.wypisz_wszystkie(),
    },
    "2": {"label": "Dodaj użytkownika", "action": user_cli.handle_add_user},
    "3": {"label": "Usuń po loginie", "action": user_cli.handle_delete_user},
    "4": {"label": "Usuń po ID", "action": user_cli.handle_delete_user_by_ID},
    "5": {"label": "Edytuj użytkownika", "action": user_cli.handle_edit_user},
    "0": {"label": "Powrót", "action": None},
}

MENU_POSTEP = {
    "1": {
        "label": "Dodaj fiszkę do nauki użytkownika",
        "action": progress_cli.handle_add_fiszka_to_learning,
    },
    "2": {
        "label": "Dodaj wszystkie fiszki do nauki użytkownika",
        "action": progress_cli.handle_add_all_fiszki_to_learning,
    },
    "3": {
        "label": "Wyświetl postęp użytkownika",
        "action": progress_cli.handle_list_progress,
    },
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
    "3": {
        "label": "Sesja treningowa (demo szkieletu)",
        "action": handle_training_demo,
    },
    "4": {
        "label": "Postęp nauki (talia użytkownika)",
        "action": lambda: menu(MENU_POSTEP, "Postęp nauki"),
    },
    "0": {"label": "Wyjdź z programu", "action": None},
}
