L’objectif est de développer un moteur capable de :
- raisonner logiquement à partir d’une base de connaissances ;
- conserver toutes les étapes de raisonnement dans une base SQL ;
- expliquer ses conclusions à l’utilisateur sous forme de justification textuelle ;
- gérer la calculabilité (certaines inférences peuvent ne pas se terminer, ce que le moteur doit détecter).

Exemple :

Type Contenu
Fait mammifere(chien)
Fait a_des_poils(X) → mammifere(X)
Règle mammifere(X) → respire_air(X)

Question utilisateur : “Le chien respire-t-il de l’air ?”
Réponse attendue : Oui, parce que :
Le chien est un mammifère (mammifere(chien) connu) ;
Tous les mammifères respirent de l’air (mammifere(X) → respire_air(X)). 


Fondamentaux :
- Stockage de la tracabilité des etapes dans une base SQL
- Codage en Java 
- Détection de cycle
- Porte logigique simple (and, or, not) et logique épistémique
- Dérouler toute la logique qui permet d'avoir eu la réponse finale


Idées pour aggrandir le projet :

1- Épistémique dynamique :
De ce fait cela fait évoluer les croyances de l'ia et fait évoluer au fur et a mesure ses connaissances

2- Mémoire réseau :
Partage de la base de donnée et change le contenu dynamiquement

3- Métalogique :
Le moteur raisonne sur son propre raisonnement 

4- Logique probabiliste :
On peut faire en sorte de rajouter une sorte de probabilité; a quel point l'ia pense qu'une information est vrai, en prenant en compte :
· Les informations qu'il a dans la base de donnée sur le sujet
· L'estimation peut se baser sur la réponse de l'utilisateur ( met a 0 si il réponds non ce n'est pas le cas, augmente l'estimation si l'utilisateur ne le corrige pas, ...)

=> Grace a la logique épistémique + probabiliste (et un systeme de temps) :
Nous pouvons estimer qu'une information est vrai que sur un laps de temps; 
Exemple :

Question : Est ce qu'il pleut aujourd'hui ?

Réponse : 
Aujourd'hui : Oui mais la reponse si on lui demande Demain : Non







L'idée précédente est trop courte, juste en donnant a chatgpt il peut le generer sans probleme. 


- Faire un moteur de jeu 4D


1- Savoir quoi rajouter

2- Gestion de la 4D, comment on introduit ca ? se baser sur la 3D et rajouter une couche par dessus puis modifier l'affichage de la camera ?


- Analyser et developper une facon intelligente de planifier des trajets a l'aide des transports en commun a l'aide de données en temps réel


1- Algorithme capable de calculer en temps réel les changements et indiquer l'itinéraire avec quel moyen le plus court d'un endroit A a B

2- Analyser si le probleme est realisable ou non ( NP complet/NP difficile)

3- Comment optimiser les choix des trajets ? heuristique ou minmax avec elagage alpha beta ?


- Comparaison des requetes analytiques SQL sur des données massives


1- Toute les requetes SQL bien écrit (sans probleme dans le code) est calculable, mais est ce que c'est possible de calculer dans un temps raisonnable ?

2- Analyse de PostgreSQL (avec SparkSQL). (PostgreSQL est centralisé et SparkSQL est distribué)

3- Déterminer les limites de calculabilité et des criteres de comparaisons


- Recherche de la délimitation de la puissance de calcul du langage SQL ( il n'y a pas d'algorithme générale qui dit si une requete SQL est terminable ou non)

1- On essaye de trouver qu'est ce qu'il est calculable, ce qu'il ne l'est pas et ce ceux indécidables

2- Peut-on caractériser, détecter ou approximer automatiquement les recherches SQL qui sont calculables

3- On devra utiliser Datalog







