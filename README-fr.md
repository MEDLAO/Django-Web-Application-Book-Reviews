## Projet : Développez une application Web en utilisant Django

[**English**](README.md)

### Tables des matières :
1. Description générale du projet/Scénario.
2. Configurations compatibles.
3. Installation du programme.
4. Fonctionnalités.
5. Démarrage du programme.

## 1. Descripton générale du projet/Scénario :

Ce projet a été réalisé dans le cadre de la formation de
développeur Python proposée par OpenClassrooms. 

La startup LITReview a pour objectif de commercialiser  un produit permettant à une communauté d'utilisateurs
de consulter ou de solliciter une critique de livres à la demande.
Par conséquent, LITReview cherche à mettre en place une application Web pour son MVP (minimum viable product,
ou produit viable minimum).

Le back-end de cette application Web a été développé avec le framework Django et le front-end avec HTML et CSS.


## 2. Configurations compatibles :

* Python 3
* Windows 10
* Mac
* Linux

## 3. Installation du programme :
Ce programme utilise les librairies Python suivantes :

```
asgiref 3.6.0
Django 4.1.7
Pillow 9.4.0
sqlparse 0.4.3
```

## 4. Fonctionnalités :

### *Authentification* : 
  * Inscription
  * Connexion
### *Menu* : 
  * Flux
  * Posts 
  * Abonnements
  * Déconnexion
### *Flux* : 
  * Affichage par ordre chronologique (le plus récent en haut de page) de l'ensemble des tickets et des critiques :
    * de l'utilisateur
    * des utilisateurs auxquels est abonné l'utilisateur 
  * Demander une critique sur un livre/article (c'est-à-dire créer un ticket)
  * Créer une critique:
    * en réponse à un ticket précédemment publié par un autre utilisateur
    * et un ticket (pas en réponse à un ticket précédent)
  * Modifier/Supprimer un ticket
  * Modifier/Supprimer une critique
### *Posts* : 
  * Affichage par ordre chronologique (le plus récent en haut de page) de l'ensemble des tickets et des critiques 
publiés par l'utilisateur
### *Abonnements* :
  * Consulter la liste:
    * des utilisateurs suivant l'utilisateur connecté
    * des utilisateurs suivis par l'utilisateur connecté
  * Chercher un utilisateur à suivre avec la barre de recherche
  * S'abonner à un utilisateur
  * Se désabonner d'un utilisateur
 
    
## 5. Démarrage du programme :

1. Ouvrir un terminal (ex: Cygwin pour Windows, le terminal pour Mac) ou dans un IDE (ex: PyCharm).
2. Télécharger le dossier contenant le projet puis se placer dans ce dossier sur le terminal.
3. Créer un environnement virtuel avec :
  > $<b> python -m venv <nom de l'environnement></b> 
4. Activer l'environnement virtuel en éxécutant :
  > $ <b>source env/bin/activate</b>  (sur Mac) 

  > $ <b>env\Scripts\activate.bat</b> (sur Windows)
5. Installer les paquets présents dans le fichier requirements.txt (ce fichier se trouve dans le dossier du projet) avec :
  > $ <b>pip install -r requirements.txt</b> 
6. Finalement, exécuter le serveur de développement avec :
> $ <b>python manage.py runserver</b>
7. Consulter le site à l'adresse suivante :

      **http://127.0.0.1:8000/**
---