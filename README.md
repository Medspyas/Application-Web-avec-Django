# LITRevu - Installation et Configuration 

## Présentation du projet

** Literevu est une plateforme de partage et de suivi de blogs. Elle permet aux utilisateurs de :
- Publier des articles et les partager
- Suivre d'autre utilisateurs
- Gérer sa propre liste d'abonnés et d'abonnement.

## Installation


- Avant toute procédure vérifier que votre connexion internet est activée et aussi vérifier que vous avez installer python sur votre machine ("https://www.python.org")
- Installez git sur votre appareil sur le site "https://git-scm.com/download/win", vérifiez que git est correctement installé en tapant sur le terminal de votre machine git --version, s'il- est correctement installé alors une version de git sera affiché.
- Ensuite, tapez "git clone https://github.com/Medspyas/Application-Web-avec-Django" pour copier le repository de l'application sur votre appareil (placez-vous dans un répertoire spécifique que vous aurais- créé au préalable.).
- Dans le dossier où vous avez cloné le projet, créez un environnement virtuel pour utiliser les bonnes versions des dépendances nécessaires à l'application.
- Tapez la commande python -m venv "le nom de votre environnement" dans le cas général, on le nomme "venv".
- Activer l'environnement virtuel : Pour windows : Excecutez la commande "venv/Sripts/activate" Pour macOS/Linux : Exécutez la commande "source venv/bin/activate"
- Installez les dépendances, tapez la commande "pip install -r requirements.txt"


# Utilisation

Pour utiliser le projet Django, suivez les étapes ci-dessous : 
1. **Appliquer les migrations**
Avant de lancer le projet, assurez-vous que toutes les migrations. 
nécessaires ont été appliquées à la base de données. Exécutez la commande suivante :
"python manage.py migrate"

2. **Créer un super utilisateur**
Créez un superutilisateur pour accéder à l'interface d'administration de Django en exécutez la commande suivante : 
"python manage.py createsuperuser"
    
3. **Lancer le serveur de développement**
Pour utiliser l'application localement, démarrez le serveur Django avec la commande suivante :
"python manage.py runserver"
