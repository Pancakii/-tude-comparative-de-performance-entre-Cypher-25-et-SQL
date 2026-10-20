import os
import csv
from dotenv import load_dotenv
from neo4j import GraphDatabase


# Connexion
load_dotenv()
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")


print("Connexion a :", URI)
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


# Fonction qui vide toute la bdd
def reset_database(session):

    # L'exécution doit se faire directement sur la session en mode "auto-commit"
    session.run("""
        MATCH (n)
        CALL { WITH n DETACH DELETE n } IN TRANSACTIONS OF 10000 ROWS
    """)

    print("Base de données Neo4j réinitialisée.")


# Insertion des noeuds
def ingest_nodes_batch(tx, batch):
    query = """
    UNWIND $batch AS row
    CREATE (:Node {id: row.id, profit: toInteger(row.profit)})
    """
    tx.run(query, batch=batch)


# Insertion des aretes entre les noeuds
def ingest_edges_batch(tx, batch):
    query = """
    UNWIND $batch AS row
    MATCH (source:Node {id: row.source})
    MATCH (target:Node {id: row.target})
    CREATE (source)-[:CONNECTED {cost: toInteger(row.cost)}]->(target)
    """
    tx.run(query, batch=batch)


# Fonction de lecture des csv et découpage en paquet
def process_csv_in_batches(session, filepath, batch_size, ingestion_function):

    # Ouverture du csv
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        batch = []
        total_processed = 0

        # Insertion des lignes 
        for row in reader:
            batch.append(row)
            if len(batch) >= batch_size:
                session.execute_write(ingestion_function, batch)
                total_processed += len(batch)
                batch = []

        # On insère le reste s'il y a un paquet incomplet à la fin
        if batch:
            session.execute_write(ingestion_function, batch)
            total_processed += len(batch)


# Execution principale
with driver.session() as session:
    
    reset_database(session)
    # Taille des paquets
    BATCH_SIZE = 10000

    # Injection des noeuds
    print("Injection des noeuds en cours. ")
    process_csv_in_batches(session, 'noeuds.csv', BATCH_SIZE, ingest_nodes_batch)

    # Création d'index
    session.run("CREATE INDEX node_id_index IF NOT EXISTS FOR (n:Node) ON (n.id)")
    session.run("CALL db.awaitIndexes()")
    print("Index de recherche créés. ")

    # Ajour aretes
    print("Injection des aretes en cours. ")
    process_csv_in_batches(session, 'aretes.csv', BATCH_SIZE, ingest_edges_batch)


print("Injection Neo4j terminée ! ")
driver.close()

