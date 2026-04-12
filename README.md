# Projekt: System nauki fiszek (Spaced Repetition)

## Opis
    Projekt realizuje plan stworzneia narzędzia wspierającego proces nauki , z wykorzystaniem programowania obiektowego. Wstępnie materiał będzie realizowany w postaci fiszek oraz nauki słówek. Program zakłada zbieranie metadanych sesji użytkownika w celu budowy sieci algorytmów ewaluacyjnych oraz predykcyjnych dla techniki spaced repetition.

## Techstack
- **Język:** Python
- **ORM:** SQLAlchemy 2.x, SQLite — plik bazy memory.db w katalogu projektu (tworzony przy pracy aplikacji; nie commituje się do repo).

## Plan funkcjonalny: sesja treningowa
Poniższy diagram opisuje **zamierzony przepływ nauki** (logika produktu), a nie dokładny stan tabel w SQLite. Szczegóły wdrożenia są w `models.py`.
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

## Struktura katalogów i plików
| Ścieżka | Opis |
|:--------|:-----|
| `main.py` | Punkt wejścia aplikacji CLI |
| `cli.py` | Menu tekstowe i obsługa poleceń użytkownika |
| `models.py` | Definicje tabel SQLAlchemy oraz silnik SQLite (`memory.db`) |
| `db_crud.py` | Wspólna klasa `BaseCRUD` i klasy CRUD dla encji |
| `requirements.txt` | Zależności projektu |
| `pytest.ini` | Konfiguracja pytest (`testpaths`, `pythonpath`) |
| `tests/test_smoke.py` | Pliki testów |
| `.vscode/settings.json` | Ustawienia workspace (np. uruchamianie pytest) |
| `.gitignore` | Reguły ignorowania plików dla Gita |

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

    Baza danych jest przechowywana w pliku models.py z uzyciem SQLite

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

## Instalacja zależnosci

   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt

## Jak uruchomić?
Program:

    python main.py

Testy:

    python -m pytest
    work in progress...

## Funkcjonalności:

    zunifikowany system wyświetlania menu CLI, trzy menu kontekstowe:
        CLI menu główne
        CLI crud użytkowników
        CLI crud fiszek
    systemy CRUD do obsługi bazy danych:
        CRUD użytkowników
        CRUD fiszek
        przygotowano klasy CRUD dla postepu, sesji, logow, tagow i list bez pelnego menu CLI

    work in progress...

