import mysql.connector
from mysql.connector import Error

def main():
    try:
        # Connessione al database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",      # aggiungi la tua password se necessaria
            database="esercizi"
        )

        cursor = conn.cursor()

        # Query per ottenere tutti gli utenti
        cursor.execute("SELECT idUtente, nome, cognome, genere, dataNascita FROM utenti;")
        rows = cursor.fetchall()

        if not rows:
            print("Nessun utente trovato.")
            return

        # Calcolo larghezza colonne
        col_id = max(len("idUtente"), max(len(str(r[0])) for r in rows))
        col_nome = max(len("Nome"), max(len(r[1]) for r in rows))
        col_cognome = max(len("Cognome"), max(len(r[2]) for r in rows))
        col_genere = len("Genere")
        col_data = len("DataNascita")

        # Header tabella
        print(
            f"{'idUtente'.ljust(col_id)} | "
            f"{'Nome'.ljust(col_nome)} | "
            f"{'Cognome'.ljust(col_cognome)} | "
            f"{'Genere'.ljust(col_genere)} | "
            f"{'DataNascita'.ljust(col_data)}"
        )
        print("-" * (col_id + col_nome + col_cognome + col_genere + col_data + 12))

        # Righe tabella
        for r in rows:
            print(
                f"{str(r[0]).ljust(col_id)} | "
                f"{r[1].ljust(col_nome)} | "
                f"{r[2].ljust(col_cognome)} | "
                f"{r[3].ljust(col_genere)} | "
                f"{str(r[4]) if r[4] else ''}"
            )

    except Error as e:
        print(f"Errore MySQL: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()
