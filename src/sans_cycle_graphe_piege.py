import csv
import random

# Nouvelle génération avec un chemin optimal et plusieurs séparation de branches
def new_generation(width, depths):
    with open('noeuds.csv', 'w', newline='', encoding='utf-8') as fn, open('aretes.csv', 'w', newline='', encoding='utf-8') as fa:
        # Initialisation de la tete de lecture
        wn = csv.writer(fn)
        wa = csv.writer(fa)
        wn.writerow(['id', 'profit'])
        wa.writerow(['source', 'target', 'cost'])

        # Noeud de départ
        curr = "Depart"
        wn.writerow([curr, 0])

        for i in range(depths):
            next = f"Opt_{i}"
            if i != depths // 2:
                wn.writerow([next, random.randint(1, 3)])
            else:
                # Donner une valeur absurde pour être sûr que le chemin est le plus opti
                wn.writerow([next, width * depths])
            wa.writerow([curr, next, 1])
            curr = next

        wn.writerow(['Fin', random.randint(1, 3)])
        wa.writerow([curr, 'Fin', 1])

        for i in range(width):
            recursive_bait(i, depths, curr, wn, wa)


trap_node = 0
nodes = []


def recursive_bait(branch, depths, prev, wn, wa):
    global trap_node, nodes
    rand = random.choice([1] * 90 + [2] * 10)
    for i in range(rand):
        next = f"Piege_{trap_node}"
        trap_node += 1

        if next not in nodes:
            wn.writerow([next, random.randint(50, 100)])
            nodes.append(next)
        wa.writerow([prev, next, 1])

        if depths == 0:
            wa.writerow([next, 'Fin', 1])
        else:
            recursive_bait(branch, depths - 1, next, wn, wa)


if __name__ == "__main__":
    print("Génération des csv du graphe. ")
    # generer_graphe(nb_noeuds_optimaux=100, nb_branches_pieges=50000)
    new_generation(width=100, depths=50)
    print("Fichiers noeuds.csv et aretes.csv sont générés. ")
