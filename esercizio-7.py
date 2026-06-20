import mysql.connector
from mysql.connector import Error

# -----------------------------
# Connessione al database
# -----------------------------
def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # aggiungi la tua password se necessaria
        database="esercizi"
    )

# -----------------------------
# Query di utilità
# -----------------------------
def get_users_with_bio(cursor):
    query = """
        SELECT u.idUtente, u.nome, u.cognome
        FROM utenti u
        INNER JOIN biografie b ON u.idUtente = b.idUtente
        WHERE u.cancellato = 0;
    """
    cursor.execute(query)
    return cursor.fetchall()

def add_user(cursor, conn):
    print("\n➕ Aggiunta nuovo utente")

    nome = input("Nome: ").strip()
    cognome = input("Cognome: ").strip()
    genere = input("Genere (M/F): ").strip().upper()
    data = input("Data di nascita (YYYY-MM-DD, opzionale): ").strip()
    bio = input("Biografia: ").strip()

    query_user = """
        INSERT INTO utenti (nome, cognome, genere, dataNascita)
        VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query_user, (nome, cognome, genere, data if data else None))
    conn.commit()

    user_id = cursor.lastrowid

    query_bio = "INSERT INTO biografie (idUtente, testo) VALUES (%s, %s);"
    cursor.execute(query_bio, (user_id, bio))
    conn.commit()

    print("\n✔ Utente aggiunto con ID:", user_id)

def update_user(cursor, conn):
    print("\n✏ Modifica utente")

    user_id = input("Inserisci l'idUtente da modificare: ").strip()

    query = "SELECT nome, cognome, genere, dataNascita FROM utenti WHERE idUtente = %s AND cancellato = 0;"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    if not user:
        print("❌ Utente non trovato.")
        return

    print(f"\nUtente attuale: {user[0]} {user[1]} ({user[2]})")

    nome = input(f"Nuovo nome ({user[0]}): ").strip() or user[0]
    cognome = input(f"Nuovo cognome ({user[1]}): ").strip() or user[1]
    genere = input(f"Nuovo genere ({user[2]}): ").strip().upper() or user[2]
    data = input(f"Nuova data nascita ({user[3]}): ").strip() or user[3]

    query_update = """
        UPDATE utenti
        SET nome = %s, cognome = %s, genere = %s, dataNascita = %s
        WHERE idUtente = %s;
    """
    cursor.execute(query_update, (nome, cognome, genere, data, user_id))
    conn.commit()

    print("\n✔ Utente aggiornato.")

def logical_delete_user(cursor, conn):
    print("\n🗑 Eliminazione logica utente")

    user_id = input("Inserisci l'idUtente da eliminare: ").strip()

    query = "UPDATE utenti SET cancellato = 1 WHERE idUtente = %s;"
    cursor.execute(query, (user_id,))
    conn.commit()

    print("\n✔ Utente eliminato logicamente.")

# -----------------------------
# Stampa tabella
# -----------------------------
def print_table(rows):
    col_id = max(len("idUtente"), max(len(str(r[0])) for r in rows))
    col_nome = max(len("Nome"), max(len(r[1]) for r in rows))
    col_cognome = max(len("Cognome"), max(len(r[2]) for r in rows))

    print(f"{'idUtente'.ljust(col_id)} | {'Nome'.ljust(col_nome)} | {'Cognome'.ljust(col_cognome)}")
    print("-" * (col_id + col_nome + col_cognome + 6))

    for r in rows:
        print(f"{str(r[0]).ljust(col_id)} | {r[1].ljust(col_nome)} | {r[2].ljust(col_cognome)}")

# -----------------------------
# Menu principale
# -----------------------------
def main():
    try:
        conn = connect()
        cursor = conn.cursor()

        while True:
            print("\n==============================")
            print("   MENU GESTIONE UTENTI")
            print("==============================")
            print("1) Elenca utenti con biografia")
            print("2) Aggiungi utente")
            print("3) Modifica utente")
            print("4) Elimina logicamente utente")
            print("5) Esci")

            scelta = input("\nSeleziona un'opzione: ").strip()

            if scelta == "1":
                users = get_users_with_bio(cursor)
                if users:
                    print("\n📌 Utenti con biografia:\n")
                    print_table(users)
                else:
                    print("\nNessun utente con biografia trovato.")

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
