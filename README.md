Traffic Jam Game

il faut faire sortir la voiture rouge vers la droite en bougeant les autres voitures.

Principe rapide

    La voiture rouge est horizontale, elle doit atteindre la case verte à droite.

    Les autres véhicules se déplacent seulement dans leur axe (de haut-bas et gauche-droite).

    Pas de rotation, pas de chevauchement(les voitures ne se traversent pas entre elles).

Fonctions

    3 niveaux fixes (bouton Configs 1-2-3).

    Générateur aléatoire (plateau toujours possible à résoudre).

    Deux tailles : 6×6 ou 8×8 (menu Options).

    Chrono et compteur de coups.

    Solveur qui utilise l'algorythme A*.

    Scores sauvegardés dans un fichier scores.txt.

Fichiers

vehicle.py   -> classe Vehicle (générique dont les autres héritent)
car.py       -> classe Car (hérite de vehicle)
truck.py     -> classe Truck (hérite de vehicle)
board.py     -> logique du plateau + solveur
scores.py    -> lecture / écriture des scores
game.py      -> interface Tkinter
main.py      -> lancer le jeu

Comment lancer

"python main.py"

(je suis sur python 3.9.13)

Format des scores

nom - joueur_coups - temps_seconde - taille (séparé en point virgules)
