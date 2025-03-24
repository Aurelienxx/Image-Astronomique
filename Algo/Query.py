# Code réaliser par : 
#   Dusannier Léothen
#   Fontaine Aurélien 

from astroquery.skyview import SkyView
import os

from .Errors import MyError

class classQuery:
    
    def __init__(self, nom:str, field_view:str= "2.0" ) -> None: 
        """ 
        Prend en parametre un string qui représente soit un nom d'un astre ou alors une position astrale. 
        Elle prend également en compte une taille du champ de vision. On recommande un champ de vision supérieur a 1.0 pour avoir des images de bonne qualités
        
        param :
            nom : str -> le nom / position d'un astre 
            field_view : str -> la taille du champs de vision
        """
        self.nom = nom
        self.folder_path = "./Images/Images_Astrales/" + nom.replace(" ","")
        
        self.field_view = field_view + " " + "deg"
        
        self.layer_needed = {
            "sii": "DSS2 Red",  
            "oiii": "DSS2 Blue", 
            "halpha": "DSS2 IR",  
        }

        
    def create_folder(self) -> None:
        """ Cree le dossier ou seront stocker les images """
        os.makedirs(self.folder_path, exist_ok=True)
        
    def download_images(self) -> None:
        """ Telecharges les differentes layers d'une image vers le dossier prescedement creer """
        self.create_folder()
        
        succesful_download = {}
        
        for layer, survey in self.layer_needed.items():
            print(f"Téléchargement de l'image pour la layer {layer} depuis le relevé {survey} en cours...")
            try:
                
                # Appel de l'API pour récuperer une image
                images = SkyView.get_images(
                    position=self.nom,
                    survey=survey,
                    width=self.field_view,
                    height=self.field_view
                )
                
                if not images :
                    print(f"Aucune image trouvée pour la layer {layer} et le relevé {survey}")
                else : 
                    # enregistrement de l'image dans dossier 'iamges_astrales'
                    fits_path = os.path.join(self.folder_path, f"{self.nom.replace(" ","_")}-{layer}.fit")
                    images[0].writeto(fits_path, overwrite=True)
                    succesful_download[layer] = fits_path
                    print(f"Image {layer} téléchargé et enregistré dans : {fits_path}")
            
            except Exception as e:
                print(f"Erreur lors du téléchargement de la layer {layer}: {e}")

        # Verification des telechargement
        if len(succesful_download) == len(self.layer_needed):
            print("Toutes les images ont été téléchargés avec succès.")
        else : 
            if len(succesful_download)== 0:
                raise MyError("Aucune image de trouvée")
            else : 
                print("Au moins un fichier n'a pas pu être télécharger")
        
        

if __name__=="__main__":
    query = classQuery("Orion","4.0 deg") # la nebule 
    query.download_images()