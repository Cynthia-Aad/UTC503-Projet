# Description du projet
Ce projet est un programme du jeu de la vie , construit en utilisant la bibliothèque graphique tkinter , ainsi qu'en utilisant le paradigme objet avec quelques aspects fonctionnels.
Le jeu consiste à choisir une configuration initiale sur la grille blanche , puis presser le bouton "Start Game". La simulation s'exécute indéfiniment , jusqu'à ce qu'elle atteigne un état stable ou que vous réinitialisez le jeux avec le bouton "Reset".

## Description de la classe
La structure de donnée principale du programme est une liste à deux dimensions (la grille des boutons).
Le paradigme objet apparait clairement d'apres la structure du programme qui est constituée d'une classe "JeuDeLaVie" qui , dans son constructeur construit l'interface graphique y compris la grille de boutons , et des methodes de classe qui simulent et stoppent le jeu.
L'aspect objet du programme est accompagné d'un aspect fonctionnel (l'utilisation du lambda calcul dans la methode "construire_grille()" pour changer la couleur d'un bouton cliqué lorsque le joueur choisit la configuration initiale).

## Documentation du code 
Toutes les methodes ainsi que les algorithmes sont bien documentés dans la classe.
