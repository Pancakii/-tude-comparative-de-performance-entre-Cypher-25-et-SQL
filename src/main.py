import os


# Fonction d'affichage du menu de selection des actions
def afficher_menu():
    print("\n" + "="*50)
    print("NEO4J VS POSTGRESQL")
    print("="*50)
    print("1. Génération graphe piège avec cycle (CSV)")
    print("2. Génération graphe piège sans cycle (CSV)")
    print("3. Injection données PostgreSQL")
    print("4. Injection données Neo4j")
    print("5. Génération graphe avec cycle + Injection globale")
    print("6. Génération graphe sans cycle + Injection globale")
    print("7. Benchmarks Test")
    print("0. Quitter")
    print("="*50)


#Fonction principale d'affichage
def main():
    while True:
        afficher_menu()
        choix = input("Choisissez une action: \n")

        if choix == "1":
            print(">>> Lancement génération graphe avec cycle...")
            os.system("python3 cycle_graphe_piege.py")

        if choix == "2":
            print(">>> Lancement génération graphe sans cycle...")
            os.system("python3 sans_cycle_graphe_piege.py")

        elif choix == "3":
            print(">>> Lancement injection PostgreSQL...")
            os.system("python3 injection_postgres.py")

        elif choix == "4":
            print(">>> Lancement injection Neo4j...")
            os.system("python3 injection_cypher.py")

        elif choix == "5":
            print(">>> Lancement génération graphe avec cycle + injections...")
            os.system("python3 cycle_graphe_piege.py")
            os.system("python3 injection_postgres.py")
            os.system("python3 injection_cypher.py")

        elif choix == "6":
            print(">>> Lancement génération graphe sans cycle + injections...")
            os.system("python3 sans_cycle_graphe_piege.py")
            os.system("python3 injection_postgres.py")
            os.system("python3 injection_cypher.py")


        elif choix == "7":
            print(">>> Lancement tests Cypher Vs Postgres...")
            os.system("python3 benchmark.py")

        elif choix == "0":
            print("\nFermeture du programme !")
            break

        else:
            print("\nChoix invalide, veuillez réessayer.")


if __name__ == "__main__":
    main()

