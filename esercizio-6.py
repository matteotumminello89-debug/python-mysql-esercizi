import mysql.connector
from mysql.connector import Error

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # aggiungi la tua password se necessaria
        database="esercizi"
    )

def get_users_with_bio(cursor):
    query = """
        SELECT u.idUtente, u.nome, u.cognome
        FROM utenti u
        INNER JOIN biografie b ON u.idUtente = b.idUtente;
    """
    cursor.execute(query)
    return cursor.fetchall()

def get_user_details(cursor, user_id):
    query = """
        SELECT u.idUtente, u.nome, u.cognome, u.genere, u.dataNascita, b.testo
        FROM utenti u
        INNER JOIN biografie b ON u.idUtente = b.idUtente
        WHERE u.idUtente = %s;
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

def print_table(rows):
    col_id = max(len("idUtente"), max(len(str(r[0])) for r in rows))
    col_nome = max(len("Nome"), max(len(r[1]) for r in rows))
    col_cognome = max(len("Cognome"), max(len(r[2]) for r in rows))

    print(f"{'idUtente'.ljust(col_id)} | {'Nome'.ljust(col_nome)} | {'Cognome'.ljust(col_cognome)}")
    print("-" * (col_id + col_nome + col_cognome + 6))

    for r in rows:
        print(f"{str(r[0]).ljust(col_id)} | {r[1].ljust(col_nome)} | {r[2].ljust(col_cognome)}")

def main():
    try:
        conn = connect()
        cursor = conn.cursor()

        print("\n📌 Utenti con biografia associata:\n")
        users = get_users_with_bio(cursor)

        if not users:
            print("Nessun utente con biografia trovata.")
            return

        print_table(users)

        print("\n--------------------------------------")
        user_id = input("Inserisci l'idUtente per visualizzare i dettagli: ").strip()

        details = get_user_details(cursor, user_id)

        if not details:
            print("\n❌ Nessun utente trovato con questo ID.")
            return

        print("\n📄 Dettagli profilo selezionato:\n")
        print(f"ID:          {details[0]}")
        print(f"Nome:        {details[1]}")
        print(f"Cognome:     {details[2]}")
        print(f"Genere:      {details[3]}")
        print(f"Nascita:     {details[4]}")
        print(f"Biografia:\n{details[5]}")

    except Error as e:
        print(f"Errore MySQL: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()
