# Projekt: System nauki fiszek (Spaced Repetition)

## Opis
Projekt realizuje plan stworzneia narzędzia wspierającego proces nauki , z wykorzystaniem programowania obiektowego. Wstępnie materiał będzie realizowany w postaci fiszek oraz nauki słówek. Program zakłada zbieranie metadanych sesji użytkownika w celu budowy sieci algorytmów ewaluacyjnych oraz predykcyjnych dla techniki spaced repetition.

## Techstack
- **Język:** Python
- **ORM:** SQLAlchemy 2.x, SQLite — plik bazy memory.db w katalogu projektu (tworzony przy pracy aplikacji; nie commituje się do repo).

## Struktura katalogów i plików
```
 Ścieżka | Opis |
|:--------|:-----|
| `main.py` | Punkt wejścia aplikacji CLI |
| `cli.py` | Menu tekstowe i obsługa poleceń użytkownika, w tym sesji treningowej |
| `models.py` | Definicje modeli SQLAlchemy (typed ORM: `Mapped`, `mapped_column`) i konfiguracja SQLite |
| `db_crud.py` | Wspólna klasa `BaseCRUD` i klasy CRUD dla encji |
| `app/persistence/session.py` | Dostęp do sesji DB (`get_db_session`) |
| `app/domain/answer_validation.py` | Walidacja odpowiedzi użytkownika (obecnie 0/1, exact match po normalizacji) |
| `app/domain/scheduling.py` | Logika harmonogramu powtórek (`schedule_next_review`) |
| `app/services/progress.py` | Obsługa postępu użytkownika i budowy zakresu nauki |
| `app/services/deck_builder.py` | Budowanie talii fiszek użytkownika na podstawie `progress` |
| `app/services/training_session.py` | Start i zakończenie sesji treningowej |
| `app/services/review_service.py` | Zapis recenzji (`review_logs`) i aktualizacja `progress` |
| `app/services/word_import.py` | Import fiszek z plików `.txt/.csv` |
| `app/services/word_file_format.py` | Parser linii `question;answer` i normalizacja danych wejściowych |
| `tests/test_word_file_format.py` | Testy parsera linii importu |
| `tests/test_word_import.py` | Testy importu fiszek do bazy |
| `tests/test_smoke.py` | Plik testów smoke (obecnie pusty / do rozbudowy) |
```

## Plan funkcjonalny: sesja treningowa

Poniższy diagram opisuje mierzalny proces nauki (logika produktu), a nie dokładny stan tabel w SQLite. Szczegóły wdrożenia są w `models.py`.

```mermaid
flowchart TB
    subgraph przygotowanie["Przygotowanie zestawu"]
        U[Użytkownik]
        L[Wybór listy / zakresu fiszek]
        T[Tagi i listy jako organizacja treści]
        U --> L
        L --> T
    end
    subgraph sesja["Sesja treningowa"]
        S_start[Rozpoczęcie sesji]
        S_loop[Pokaż fiszkę / pytanie]
        S_odp[Odpowiedź użytkownika]
        S_log[Zapis oceny i czasu odpowiedzi]
        S_prog[Aktualizacja postępu / harmonogram powtórki]
        S_end[Zakończenie sesji]
        S_start --> S_loop
        S_loop --> S_odp
        S_odp --> S_log
        S_log --> S_prog
        S_prog --> S_loop
        S_prog --> S_end
    end
    subgraph dane["Dane utrwalane w systemie"]
        DB_sess[(Sesja treningowa)]
        DB_log[(Logi recenzji)]
        DB_pr[(Postęp na fiszce)]
    end
    U --> S_start
    S_start --> DB_sess
    S_log --> DB_log
    S_prog --> DB_pr
    S_end --> DB_sess
```
## Architektura bazy danych

```mermaid
erDiagram
    USER ||--o{ SESSION : "rozpoczyna"
    USER ||--o{ PROGRESS : "posiada"
    USER ||--o{ REVIEW_LOG : "tworzy"

    SESSION ||--o{ REVIEW_LOG : "gromadzi"

    FISZKA ||--o{ REVIEW_LOG : "jest oceniana"
    FISZKA ||--o{ PROGRESS : "ma status"
    FISZKA ||--o{ FISH_LIST : "nalezy do listy"

    LIST ||--o{ FISH_LIST : "zawiera fiszki"
    LIST ||--o{ TAG_LIST : "ma tagi"
    TAG ||--o{ TAG_LIST : "definiuje"

    USER {
        int id PK
        string username UK
        string email
        string password_hash
    }

    SESSION {
        int id PK
        int user_id FK
        datetime start_time
        datetime end_time
    }

    FISZKA {
        int id PK
        string question UK
        string answer
    }

    REVIEW_LOG {
        int id PK
        int user_id FK
        int fiszka_id FK
        int session_id FK
        int grade
        int response_time_ms
        datetime created_at
    }

    PROGRESS {
        int id PK
        int user_id FK
        int fiszka_id FK
        int mastery_level
        datetime review_date
    }

    LIST {
        int id PK
        string name UK
        string describe
    }

    FISH_LIST {
        int list_id PK_FK
        int fiszka_id PK_FK
    }

    TAG_LIST {
        int list_id PK_FK
        int tag_id PK_FK
    }

    TAG {
        int id PK
        string name UK
    }
```

Projekt zakłada modułową budowę, która pozwala na utrzymanie czystego kodu oraz łatwą rozbudowę. 

## Nazwy tabel w SQLite (mapowanie)

| Encja na diagramie | Rzeczywista nazwa tabeli |
|:-------------------|:-------------------------|
| USER | `users` |
| SESSION | `sessions` |
| FISZKA | `fiszka` |
| REVIEW_LOG | `review_logs` |
| PROGRESS | `progress` |
| LIST | `lists` |
| FISH_LIST | `fiszka_list` |
| TAG_LIST | `tag_lists` |
| TAG | `tag` |

## Model danych i refaktor ORM

Projekt korzysta z SQLAlchemy 2.x oraz typed ORM (`Mapped`, `mapped_column`), co poprawia:
- czytelność typów w kodzie,
- kompatybilność z narzędziami statycznej analizy,
- bezpieczeństwo dalszej rozbudowy warstwy domenowej.

Kluczowe ograniczenia i zależności:
- `progress`: unikalność pary `(user_id, fiszka_id)`,
- `sessions`: unikalność pary `(user_id, start_time)`,
- `review_logs` przechowuje dane recenzji: `grade`, `response_time_ms`, `created_at`.

## Instalacja zależnosci

```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
```
## Jak uruchomić?

### Program:
    ```bash
    python main.py
    ```
### Testy:
    ```bash
    python -m pytest
    ```
## Funkcjonalności:

### Działa
- CLI menu główne i menu kontekstowe.
- CRUD użytkowników.
- CRUD fiszek.
- Import fiszek z plików (`.txt`/`.csv`) z obsługą duplikatów i błędnych linii.
- Dodawanie fiszek do nauki użytkownika (`progress`).
- Sesja treningowa:
  - wpisywanie odpowiedzi przez użytkownika,
  - automatyczna walidacja odpowiedzi (0/1),
  - automatyczne wyliczanie oceny,
  - zapis recenzji do `review_logs`,
  - aktualizacja harmonogramu i poziomu opanowania w `progress`.

### W trakcie / planowane
- Rozbudowa walidatora odpowiedzi o tolerancję literówek.
- Rozbudowa strategii harmonogramowania o bardziej zaawansowane heurystyki/algorytmy.
- Pełna obsługa list i tagów w warstwie CLI.
- Szersze pokrycie testami (sesja treningowa, review service, scheduling, walidator odpowiedzi).

## Aktualny flow sesji treningowej (MVP)
1. Użytkownik wybiera opcję sesji treningowej i podaje `user_id`.
2. System buduje talię na podstawie rekordów `progress` użytkownika.
3. Dla każdej fiszki:
   - wyświetlane jest pytanie,
   - użytkownik wpisuje odpowiedź,
   - odpowiedź jest walidowana automatycznie względem poprawnej odpowiedzi fiszki,
   - mierzony jest czas odpowiedzi (`response_time_ms`),
   - system wylicza ocenę (`grade`) automatycznie (na podstawie `is_correct` i czasu),
   - zapisywany jest `review_log`,
   - aktualizowany jest `progress` (`mastery_level`, `review_date`).
4. Sesja jest zamykana przez ustawienie `end_time` w tabeli `sessions`.
W MVP użytkownik **nie wpisuje oceny ręcznie** — ocena jest wyłącznie automatyczna.