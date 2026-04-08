from models import Fiszka

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
