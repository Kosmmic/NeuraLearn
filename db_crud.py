from models import Fiszka, User


class FiszkaCRUD:
    def __init__(self, session):
        self.session = session

    def wypisz_fiszki(self):
        fiszki = self.session.query(Fiszka).all()
        print("All Fiszki:")
        for f in fiszki:
            print(f)

    def nowa_Fiszka(self, question, answer):
        try:
            istnieje = self.session.query(Fiszka).filter_by(question=question).first()
            if istnieje:
                print(f"Fiszka with question '{question}' already exists.")
                return

            fiszka = Fiszka(question=question, answer=answer)
            self.session.add(fiszka)
            self.session.commit()
            return fiszka
        except Exception as e:
            self.session.rollback()
            raise e

    def usun_fiszke(self, question):
        try:
            fiszka = self.session.query(Fiszka).filter_by(question=question).first()
            if fiszka:
                self.session.delete(fiszka)
                self.session.commit()
                print(f"Deleted: {fiszka}")
                return True
            print(f"No Fiszka found with question '{question}'")
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def usun_fiszke_po_id(self, fiszka_id):
        try:
            fiszka = self.session.get(Fiszka, fiszka_id)
            if fiszka:
                self.session.delete(fiszka)
                self.session.commit()
                print(f"Deleted: {fiszka}")
        except Exception as e:
            self.session.rollback()
            raise e
        else:
            print(f"No Fiszka found with id '{fiszka_id}'")

    def edytuj_fiszke(self, fiszka_id, new_question, new_answer):
        try:
            fiszka = self.session.get(Fiszka, fiszka_id)
            if fiszka:
                if new_question:
                    fiszka.question = new_question
                if new_answer:
                    fiszka.answer = new_answer
                self.session.commit()
                print(f"Updated: {fiszka}")
                return True
            print(f"No Fiszka found with id '{fiszka_id}'")
            return False
        except Exception as e:
            self.session.rollback()
            raise e


class UserCRUD:
    def __init__(self, session):
        self.session = session

    def wypisz_uzytkownikow(self):
        users = self.session.query(User).all()
        print("All Users:")
        for u in users:
            print(u)

    def nowy_uzytkownik(self, username, name, fullname):
        try:
            istnieje = self.session.query(User).filter_by(username=username).first()
            if istnieje:
                print(f"User with username '{username}' already exists.")
                return False

            user = User(username=username, name=name, fullname=fullname)
            self.session.add(user)
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise e

    def usun_uzytkownika(self, username):
        try:
            user = self.session.query(User).filter_by(username=username).first()
            if user:
                self.session.delete(user)
                self.session.commit()
                print(f"Deleted: {user}")
                return True
            print(f"No User found with username '{username}'")
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def usun_uzytkownika_po_id(self, user_id):
        try:
            user = self.session.get(User, user_id)
            if user:
                self.session.delete(user)
                self.session.commit()
                print(f"Deleted: {user}")
                return True
            print(f"No User found with id '{user_id}'")
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def edytuj_uzytkownika(self, user_id, new_username, new_name, new_fullname):
        try:
            user = self.session.get(User, user_id)
            if user:
                if new_username:
                    user.username = new_username
                if new_name:
                    user.name = new_name
                if new_fullname:
                    user.fullname = new_fullname
                self.session.commit()
                print(f"Updated: {user}")
                return True
            print(f"No User found with id '{user_id}'")
            return False
        except Exception as e:
            self.session.rollback()
            raise e
