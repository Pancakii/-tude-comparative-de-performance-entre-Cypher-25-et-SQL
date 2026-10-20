import csv
import random

# Fonction qui génére le graphe massif en séparant les branches et les noeuds
def generer_graphe(nb_noeuds_optimaux, nb_branches_pieges):

    # On ouvre les fichiers directement pour écrire ligne par ligne
    with open('noeuds.csv', 'w', newline='', encoding='utf-8') as fn, open('aretes.csv', 'w', newline='', encoding='utf-8') as fa:

        #Initialisation de la tete de lecture
        writer_n = csv.writer(fn)
        writer_a = csv.writer(fa)
        writer_n.writerow(['id', 'profit'])
        writer_a.writerow(['source', 'target', 'cost'])

        # On s'occupe de faire d'abord le chemin optimal (pas rentable en cours terme)
        writer_n.writerow(['Depart', 0])
        noeud_courant = 'Depart'

        for i in range(1, nb_noeuds_optimaux + 1):

            noeud_suivant = f'Opt_{i}'
            writer_n.writerow([noeud_suivant, random.randint(1, 3)])
            writer_a.writerow([noeud_courant, noeud_suivant, 1])
            noeud_courant = noeud_suivant

        writer_n.writerow(['Fin', 50])
        writer_a.writerow([noeud_courant, 'Fin', 1])

        # On s'occupe fde faire les pieges 
        for i in range(nb_branches_pieges):
            piege_a = f'Piege_A_{i}'
            piege_b = f'Piege_B_{i}'

            # Des profits immédiats monstrueux pour aveugler l'optimiseur
            writer_n.writerow([piege_a, random.randint(50, 100)])
            writer_n.writerow([piege_b, random.randint(10, 20)])

            # On les connecte au départ
            writer_a.writerow(['Depart', piege_a, 1])

            # On les multiblie
            writer_a.writerow([piege_a, piege_b, 1])
            writer_a.writerow([piege_b, piege_a, 2]) 

if __name__ == "__main__":
    print("Génération des csv du graphe. ")
    
    generer_graphe(nb_noeuds_optimaux=100, nb_branches_pieges=50000)
    
    print("Fichiers noeuds.csv et aretes.csv sont générés. ")
