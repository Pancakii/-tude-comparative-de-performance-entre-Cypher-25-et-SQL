import os
import time
import psycopg2
from neo4j import GraphDatabase
from dotenv import load_dotenv
import matplotlib.pyplot as plt  # Ajout de matplotlib pour le graphique


load_dotenv()

# Connexion PostgreSQL
pg_conn = psycopg2.connect(
    host=os.getenv("PG_HOST", "localhost"),
    port=os.getenv("PG_PORT", "5432"),
    dbname=os.getenv("PG_DB", "postgres"),
    user=os.getenv("PG_USER", "postgres"),
    password=os.getenv("PG_PASSWORD")
)

# Connexion Cypher
neo4j_driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)


# Fonction de test sur PostgreSQL
def test_postgresql(budget):
    # Boucle WITH RECURSIVE qui parcours les chemins
    query = """
    WITH RECURSIVE exploration AS (

        -- On force le type en ::TEXT pour éviter l'erreur de typage
        SELECT id AS noeud_actuel, ARRAY[id::TEXT] AS chemin, 0 AS cout_total, profit AS profit_total
        FROM noeuds WHERE id = 'Depart'

        UNION ALL

        -- On force aussi la cible en ::TEXT au moment de l'ajouter
        SELECT a.target, e.chemin || a.target::TEXT, e.cout_total + a.cost, e.profit_total + n.profit
        FROM exploration e
        JOIN aretes a ON e.noeud_actuel = a.source
        JOIN noeuds n ON a.target = n.id
        WHERE (e.cout_total + a.cost) <= %(budget)s
    )

    -- On prend le chemin qui a généré le plus de profit
    SELECT chemin, cout_total, profit_total 
    FROM exploration 
    ORDER BY profit_total DESC 
    LIMIT 1;
    """

    # Timeur
    start_time = time.time()

    # Étant donné qu'on a pas vraiment de brider postgres, nous allons nous meme le faire crasher manuellement
    try:
        with pg_conn.cursor() as cur:
            # Un timeout dans le pire cas
            cur.execute("SET statement_timeout = '10s';")
            cur.execute(query, {'budget': budget})
            resultat = cur.fetchone()

        elapsed = time.time() - start_time
        return elapsed  # Retourne un float pour le graphique

    except Exception as e:
        pg_conn.rollback()
        print(f"CRASH: {e}")
        return None  # Retourne None en cas de crash


# Fonction de test sur Cypher
def test_neo4j(budget):
    # Parcours des chemins en utilisant allreduce()
    query = """
    MATCH p = (d:Node {id: 'Depart'})-[:CONNECTED*]->(end:Node)

    // allReduce(accumulateur, variable de boucle | fonction d'accumulation, condition de survie)
    WHERE allReduce(cout = 0, r IN relationships(p) | cout + r.cost, cout <= $budget)

    RETURN [n IN nodes(p) | n.id] AS chemin, reduce(c = 0, r IN relationships(p) | c + r.cost) AS cout_total, reduce(pr = d.profit, n IN nodes(p)[1..] | pr + n.profit) AS profit_total
    ORDER BY profit_total DESC 
    LIMIT 1
    """

    # Code pas du tout optimal pour faire cracher 
    # query = """
    #    MATCH p = (d:Node {id: 'Depart'})-[:CONNECTED*]->(end:Node)
    #    WITH p, 
    #        reduce(c = 0, r IN relationships(p) | c + r.cost) AS cout_total,
    #        reduce(pr = toInteger(d.profit), n IN nodes(p)[1..] | pr + toInteger(n.profit)) AS profit_total
    #
    #    RETURN [n IN nodes(p) | n.id] AS chemin, cout_total, profit_total
    #    ORDER BY profit_total DESC 
    #    LIMIT 1000
    #"""

    # Timeur
    start_time = time.time()
    # Il faudra nous meme brider la RAM que le moteur JAVA a le droit d'utiliser, on ouvre le fichier neo4j.conf,
    # puis on modifie ces 2 lignes | server.memory.heap.initial_size=512m server.memory.heap.max_size=1G |
    try:
        with neo4j_driver.session() as session:
            session.run(query, budget=budget).single()

        elapsed = time.time() - start_time
        return elapsed  # Retourne un float pour le graphique

    except Exception as e:
        print(f"CRASH: {e}")
        return None  # Retourne None en cas de crash


if __name__ == "__main__":
    print("\n" + "="*50)
    print("Lancement test PostgreSQL vs Cypher")
    print("="*50 +"\n")

    # Liste des budgets
    budgets = [10, 20, 50, 100, 200, 500, 1000]

    # Listes pour stocker les résultats du graphique
    temps_pg_list = []
    temps_neo4j_list = []

    for budget in budgets:
        print(f"Test avec budget max = {budget}")

        # Chrono Cypher
        print("Test Cypher (RAM)... ", end="", flush=True)
        t_neo4j = test_neo4j(budget)
        if t_neo4j is not None:
            print(f"{t_neo4j:.3f} secondes")
        temps_neo4j_list.append(t_neo4j)

        # Chrono PostgreSQL
        print("Test PostgreSQL (Disque)... ", end="", flush=True)
        t_pg = test_postgresql(budget)
        if t_pg is not None:
            print(f"{t_pg:.3f} secondes")
        temps_pg_list.append(t_pg)

        print("-" * 30)
        time.sleep(1) # Laisse les processeurs respirer une seconde

    pg_conn.close()
    neo4j_driver.close()

    print("\nFin des tests, génération du graphique...")

    # Génération du graphique
    plt.figure(figsize=(10, 6))

    # Trace les lignes (les valeurs 'None' interrompront automatiquement la courbe)
    plt.plot(budgets, temps_pg_list, marker='o', color='blue', linewidth=2, label='PostgreSQL')
    plt.plot(budgets, temps_neo4j_list, marker='s', color='green', linewidth=2, label='Neo4j (Cypher)')

    # Personnalisation du graphique
    plt.title('Comparaison des temps de requêtes : PostgreSQL vs Neo4j', fontsize=14)
    plt.xlabel('Budget Maximum (Profondeur/Complexité)', fontsize=12)
    plt.ylabel('Temps d\'exécution (secondes)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)

    # Échelle logarithmique si la différence de temps est extrême (décommenter si besoin)
    # plt.yscale('log')

    plt.tight_layout()
    plt.show() # Affiche le graphique dans une fenêtre

