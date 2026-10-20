import os
import psycopg2
from dotenv import load_dotenv


# Load .env file
load_dotenv()
# Read variables
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB = os.getenv("PG_DB", "postgres")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD")


# Optional: quick debug
print("Connecting to PostgreSQL at:", PG_HOST)
print("User:", PG_USER)


# Create driver (pour se connecter a la base de donnée de PostgreSQL)
conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    dbname=PG_DB,
    user=PG_USER,
    password=PG_PASSWORD
)


# Pour éviter de faire conn.commit() à chaque fois
conn.autocommit = True 
cursor = conn.cursor()


# Fonction qui vide toute la bdd
def reset_database(cur):
    cur.execute("DROP TABLE IF EXISTS aretes;")
    cur.execute("DROP TABLE IF EXISTS noeuds;")

    cur.execute("""
        CREATE TABLE noeuds (
            id VARCHAR(255) PRIMARY KEY,
            profit INTEGER
        );
    """)
    cur.execute("""
        CREATE TABLE aretes (
            source VARCHAR(255),
            target VARCHAR(255),
            cost INTEGER
        );
    """)
    print("Tables 'noeuds' et 'aretes' réinitialisées.")


# Pour compter le nombre de noeud dans la bdd (un petit check pour verifier qu'on a bien tout)
def get_nodes_count(cur):
    cur.execute("SELECT COUNT(*) FROM noeuds;")
    return cur.fetchone()[0]


def write_data(cur):
    # Write data (On utilise copy_from, la méthode la plus rapide pour PostgreSQL)
    print("Injection des noeuds en cours. ")

    with open('noeuds.csv', 'r', encoding='utf-8') as f:
        # On ignore la première ligne du CSV (les en-têtes id,profit)
        next(f)
        cur.copy_from(f, 'noeuds', sep=',')
    print("Noeuds insérés! ")

    print("Injection des aretes en cours. ")
    with open('aretes.csv', 'r', encoding='utf-8') as f:
        # On ignore la première ligne du CSV (les en-têtes source,target,cost)
        next(f)
        cur.copy_from(f, 'aretes', sep=',')
    print("Arêtes insérées!")

    # Création des index
    cur.execute("CREATE INDEX idx_aretes_source ON aretes(source);")
    cur.execute("CREATE INDEX idx_aretes_target ON aretes(target);")
    print("Index de recherche créés.")


# Execution du script
try:
    reset_database(cursor)
    write_data(cursor)

    nodes_count = get_nodes_count(cursor)
    print("nodes in database:", nodes_count)

except Exception as e:
    print("Une erreur est survenue :", e)

finally:
    cursor.close()
    conn.close()
    print("Connexion a PostgreSQL terminé.")

