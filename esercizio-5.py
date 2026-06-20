import mysql.connector
from mysql.connector import Error

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      # inserisci la tua password se necessaria
        database="esercizi"
    )

def fetch_users_with_bio(cursor):
    query = """
        SELECT u.idUtente, u.nome, u.cognome
        FROM utenti u
        INNER JOIN biografie b ON u.idUtente = b.idUtente;
    """
    cursor.execute(query)
    return cursor.fetchall()

def fetch_user_id_by_surname(cursor, cognome):
    query = """
        SELECT idUtente
        FROM utenti
        WHERE cognome = %s;
    """
    cursor.execute(query, (cognome,))
    return cursor.fetchone()

def main():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("\n📌 Utenti con biografia associata:\n")

        users = fetch_users_with_bio(cursor)

        if not users:
            print("Nessun utente con biografia trovata.")
            return

        for user in users:
            print(f"- {user[1]} {user[2]} (idUtente: {user[0]})")

        print("\n--------------------------------------")
        cognome = input("Inserisci un cognome per ottenere l'idUtente: ").strip()

        result = fetch_user_id_by_surname(cursor, cognome)

        if result:
            print(f"\n➡️  idUtente corrispondente: {result[0]}")
        else:
            print("\n❌ Nessun utente trovato con quel cognome.")

    except Error as e:
        print(f"Errore MySQL: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()
