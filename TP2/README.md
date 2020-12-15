# TP2 Données Cyber - Canal de diffusion anonyme et génération de secret



## Installation
Le tp a été réalisé en Python avec la version 3.9. Le code développé n'utilise que des modules natifs et devrait être compatible pour les versions de python 3.7+.

## Lancement
```
python diffusionAnonyme.py
```

ou 

```
python3 diffusionAnonyme.py
```
### Résolution des problèmes

En cas d'erreur, s'assurer que la version de python est égale ou supérieure à la 3.7.

Il est également nécéssaire que les fichiers `diffusionAnonyme.py` et `ValueThread.py` soient dans le même répertoire et qu'il s'agisse du répertoire d'exécution.

## Fonctionnement du code

1. Au lancement du code, la fonction `test_canal` est appelée. 
2. Deux interlocuteurs sont définis par leur nom.
3. La date de début est récupérée sous la forme d'un timestamp et la durée de l'échange entre les deux interlocuteurs est définie.
4. Un secret est généré et on récupère la vue des deux interlocuteurs.
5. Les messages postés anonymements sont également récupérés.
6. Les secrets sont ensuite générés et comparés. Pour s'assurer qu'il n'y a pas d'erreur, on vérifie que les secrets générés depuis les deux vues sont égaux et on affiche le résultat de leur égalité.

## Remarques supplémentaires

Les fonctions sont commentées en suivant la Docstring Conventions PEP 257.

Nous avons décidé d'utiliser une de base de données sqlite pour tester nos résultats avec persistance des données.

## Développeurs
Le TP a été réalisé par :

* [Flavien JOURDREN](https://github.com/fjourdren)
* [Jean-Baptiste DUCHÊNE](https://github.com/jbduchenee)