# Code réaliser par : 
#   Dusannier Léothen
#   Fontaine Aurélien 

from PyQt6.QtCore import QObject, QThread, pyqtSignal

from Algo.Query import classQuery 

class classDownload(QObject):
    finished = pyqtSignal()  
    error = pyqtSignal(str)  
    progress = pyqtSignal(str)  

    def __init__(self, coord:str, deg:float=None):
        """
        Une class qui a pour seul rôle de gerer le téléchargement des images astrales. Cette technique de téléchargement permet 
        a l'application de continuer a fonctionner durent le téléchargement des images 
        
        param :
            coord : str -> les coordonnées d'un astre (un nom ou une position)
            deg : flaot -> un angle compris entre 0.0 et 20.0
        """
        super().__init__()
        self.coord = coord
        self.deg = deg

    def run(self):
        try:
            if self.deg:
                query = classQuery(self.coord, str(self.deg))
            else:
                query = classQuery(self.coord)
                
            query.download_images()
            self.finished.emit()  
        except Exception as e:
            self.error.emit(str(e))  
