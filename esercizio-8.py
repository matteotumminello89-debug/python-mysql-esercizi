import mysql.connector
from mysql.connector import Error
import re
from datetime import datetime

# ---------------------------------------
# VALIDAZIONE INPUT
# ---------------------------------------

def input_nome(prompt):
    while True:
        nome = input(prompt).strip()
        if len(nome) < 2:
            print("❌ Errore: il nome deve contenere almeno 2 caratteri.")
        elif not nome.replace(" ", "").isalpha():
            print("❌ Errore: il nome può contenere solo lettere.")
        else:
            return nome

def input_cognome(prompt):
    while True:
        cognome = input(prompt).strip()
        if len(cognome) < 2:
            print("❌ Errore: il cognome deve contenere almeno 2 caratteri.")
        elif not cognome.replace(" ", "").isalpha():
            print("❌ Errore: il cognome può contenere solo lettere.")
        else:
            return cognome

def input_genere(prompt):
    while True:
        g = input(prompt).strip().upper()
        if g in ("M", "F"):
            return g
        print("❌ Errore: inserisci solo 'M' o 'F'.")

def input_data(prompt):
    while True:
        data = input(prompt).strip()
        if data == "":
            return None
        try:
            datetime.strptime(data, "%Y-%m-%d")
            return data
        except ValueError:
            print("❌ Errore: formato data non valido (usa YYYY-MM-DD).")

def input_biografia(prompt):
    while True:
        bio = input(prompt).strip()
        if len(bio) == 0:
            print("❌ Errore: la biografia non può essere vuota.")
        else:
            return bio

# ---------------------------------------
# CONNESSIONE DATABASE
# ---------------------------------------

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="esercizi"
    )

# ---------------------------------------
# FUNZIONI CRUD
# ---------------------------------------

def get_users_with_bio(cursor):
    cursor.execute("""
        SELECT u.idUtente, u.nome, u.cognome
        FROM utenti u
        INNER JOIN biografie b ON u.idUtente = b.idUtente
        WHERE u.cancellato = 0;
    """)
    return cursor.fetchall()

def add_user(cursor, conn):
    print("\n➕ Aggiunta nuovo utente con controlli")

    nome = input_nome("Nome: ")
    cognome = input_cognome("Cognome: ")
    genere = input_genere("Genere (M/F): ")
    data = input_data("Data di nascita (YYYY-MM-DD, opzionale): ")
    bio = input_biografia("Biografia: ")

    cursor.execute("""
        INSERT INTO utenti (nome, cognome, genere, dataNascita)
        VALUES (%s, %s, %s, %s);
    """, (nome, cognome, genere, data))
    conn.commit()

    user_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO biografie (idUtente, testo)
        VALUES (%s, %s);
    """, (user_id, bio))
    conn.commit()

    print(f"\n✔ Utente aggiunto correttamente (ID: {user_id})")

def update_user(cursor, conn):
    print("\n✏ Modifica utente")

    user_id = input("ID utente da modificare: ").strip()

    cursor.execute("SELECT nome, cognome, genere, dataNascita FROM utenti WHERE idUtente = %s AND cancellato = 0;", (user_id,))
    user = cursor.fetchone()

    if not user:
        print("❌ Utente non trovato.")
        return

    print(f"\nUtente attuale: {user[0]} {user[1]} ({user[2]})")

    nome = input_nome(f"Nuovo nome ({user[0]}): ") or user[0]
    cognome = input_cognome(f"Nuovo cognome ({user[1]}): ") or user[1]
    genere = input_genere(f"Nuovo genere ({user[2]}): ") or user[2]
    data = input_data(f"Nuova data nascita ({user[3]}): ") or user[3]

    cursor.execute("""
        UPDATE utenti
        SET nome = %s, cognome = %s, genere = %s, dataNascita = %s
        WHERE idUtente = %s;
    """, (nome, cognome, genere, data, user_id))
    conn.commit()

    print("\n✔ Utente aggiornato.")

def logical_delete_user(cursor, conn):
    print("\n🗑 Eliminazione logica utente")
    user_id = input("ID utente da eliminare: ").strip()

    cursor.execute("UPDATE utenti SET cancellato = 1 WHERE idUtente = %s;", (user_id,))
    conn.commit()

    print("\n✔ Utente eliminato logicamente.")

# ---------------------------------------
# STAMPA TABELLA
# ---------------------------------------

def print_table(rows):
    col_id = max(len("idUtente"), max(len(str(r[0])) for r in rows))
    col_nome = max(len("Nome"), max(len(r[1]) for r in rows))
    col_cognome = max(len("Cognome"), max(len(r[2]) for r in rows))

    print(f"{'idUtente'.ljust(col_id)} | {'Nome'.ljust(col_nome)} | {'Cognome'.ljust(col_cognome)}")
    print("-" * (col_id + col_nome + col_cognome + 6))

    for r in rows:
        print(f"{str(r[0]).ljust(col_id)} | {r[1].ljust(col_nome)} | {r[2].ljust(col_cognome)}")

# ---------------------------------------
# MENU PRINCIPALE
# ---------------------------------------

def main():
    try:
        conn = connect()
        cursor = conn.cursor()

        while True:
            print("\n==============================")
            print("   MENU GESTIONE UTENTI")
            print("==============================")
            print("1) Elenca utenti con biografia")
            print("2) Aggiungi utente (con controlli)")
            print("3) Modifica utente (con controlli)")
            print("4) Elimina logicamente utente")
            print("5) Esci")

            scelta = input("\nSeleziona un'opzione: ").strip()

            if scelta == "1":
                users = get_users_with_bio(cursor)
                print("\n📌 Utenti con biografia:\n")
                print_table(users)

            elif scelta == "2":
                add_user(cursor, conn)

            elif scelta == "3":
                update_user(cursor, conn)

            elif scelta == "4":
                logical_delete_user(cursor, conn)

            elif scelta == "5":
                print("\nUscita dal programma.")
                break

            else:
                print("❌ Opzione non valida.")

    except Error as e:
        print(f"Errore MySQL: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()
