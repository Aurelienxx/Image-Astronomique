# Code réaliser par : 
#   Dusannier Léothen
#   Fontaine Aurélien 

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import os

class classRenderImage:
    def __init__(self, nom):
        self.image_rgb = None
        self.image_noir_blanc = None
        self.nom = nom
        self.fichiers_fits = []
        self.get_bande()

    def get_bande(self):
        for f in os.listdir(self.nom):
            chemin_complet = os.path.join(self.nom, f)
            if f.endswith((".fit", ".fits")) and os.path.isfile(chemin_complet):
                self.fichiers_fits.append(chemin_complet)

    def render(self, couleurs):
        return np.dstack(couleurs)
    
    def compilation_rgb(self, ordre=[0,1,2]):
        images = []
        for bande in self.fichiers_fits: 
            images.append(fits.getdata(bande))
        
        couleurs = []
        for img in images:
            img = np.nan_to_num(img, nan=0.0, posinf=0.0, neginf=0.0)
            min_val, max_val = np.percentile(img, [2, 98])
            normalisee = np.clip((img - min_val) / (max_val - min_val), 0, 1)
            couleurs.append(normalisee)

        empilement = []
        for i in ordre:
            empilement.append(couleurs[i])
            
        self.image_rgb = np.dstack(empilement)

    def compilation_noir_blanc(self):
        if self.image_rgb is None:
            self.compilation()  # Génère l'image RGB si elle n'existe pas encore
        
        # Convertir l'image RGB en niveaux de gris
        self.image_noir_blanc = np.dot(self.image_rgb, [0.2989, 0.5870, 0.1140])

    
        
    def affiche(self):
        plt.imshow(self.image_rgb, origin='lower')
        plt.title("Image Astro")
        plt.show()
        
    def get_image_noir_blanc(self):
        if self.image_noir_blanc is None:
            self.compilation_noir_blanc()
        return self.image_noir_blanc
            
    def get_image_rgb(self):
        if self.image_rgb is None:
            self.compilation_rgb()  
        return self.image_rgb
    
    def get_images_utiliser(self):
        return self.fichiers_fits
    
    def change_valeur(self, nouvelle_image):
        if nouvelle_image in self.fichiers_fits :
            self.fichiers_fits.remove(nouvelle_image)
        else :
            self.fichiers_fits.append(nouvelle_image)
            
        self.compilation()  

if __name__ == "__main__":
    chemin_dossier = "/../Images/Images_Astrales/23.865_76.4754"

    render_image = classRenderImage(chemin_dossier)
    render_image.compilation()
    render_image.affiche()