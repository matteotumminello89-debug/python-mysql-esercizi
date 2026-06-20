import mysql.connector
from mysql.connector import Error

def main():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",      # aggiungi la tua password se necessaria
            database="esercizi"
        )

        cursor = conn.cursor()

        query = """
            SELECT u.idUtente, u.nome, u.cognome
            FROM utenti u
            INNER JOIN biografie b ON u.idUtente = b.idUtente;
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print("Nessun utente con biografia trovata.")
            return

        # Calcolo larghezza colonne per tabella
        col_id = max(len("idUtente"), max(len(str(r[0])) for r in rows))
        col_nome = max(len("Nome"), max(len(r[1]) for r in rows))
        col_cognome = max(len("Cognome"), max(len(r[2]) for r in rows))

        # Header
        print(f"{'idUtente'.ljust(col_id)} | {'Nome'.ljust(col_nome)} | {'Cognome'.ljust(col_cognome)}")
        print("-" * (col_id + col_nome + col_cognome + 6))

        # Righe
        for r in rows:
            print(f"{str(r[0]).ljust(col_id)} | {r[1].ljust(col_nome)} | {r[2].ljust(col_cognome)}")

    except Error as e:
        print(f"Errore MySQL: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()
