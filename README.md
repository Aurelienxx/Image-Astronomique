# Collaborateurs :

    Dusannier Léothen
    Fontaine Aurélien

# Prérequis

- Python 3.9+

- Bibliothèques Python :

    - PyQt6
    - matplotlib
    - astropy
    - astroquery
    - scipy

- Installation des dépendances nécessaires :

    - Windows :

            pip install -r requirements.txt

    -Linux :
    
        pip3 install -r requirements.txt



# Lancer l'application

Pour démarrer l'application, il suffit d'exécuter le fichier Main.py situé à la racine du projet.

# Fonctionnalités

Une fois l'application lancée, vous pouvez choisir l'une des options suivantes :
1. Télécharger une image d'un objet céleste

    Entrez le nom de l'objet céleste ou ses coordonnées (par exemple : 47.62 -58.6).
    Indiquez la taille de l'objet en degrés (par exemple : 6.9).

2. Ouvrir une image existante

    Sélectionnez le dossier contenant les images .FIT de l'objet que vous souhaitez observer.

3. Application des filtres

    Une fois l'image de l'astre sélectionnée, vous pouvez déplacer les fichiers vers les différents filtres (R, V, B) en utilisant la fonctionnalité drag and drop.
