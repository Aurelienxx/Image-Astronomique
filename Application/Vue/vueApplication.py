# Code réaliser par : 
#   Dusannier Léothen
#   Fontaine Aurélien 

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit, QFrame, QFileDialog, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt, QThread

import numpy as np

from .ImageWidget import ImageWidget
from .PopUp import PopUpError, PopUpInfo

from Algo.RenderImage import classRenderImage 
from .DraggableObject.DragDropArea import classDragDropWidget

from Application.Controler.ImageDownloader import classDownload

import sys
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application Astro")
        self.setMinimumSize(1000, 600)
        self.setupUI()

    def setupUI(self):
        mainLayout = QHBoxLayout(self)

        self.image = ImageWidget()
        self.image.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        mainLayout.addWidget(self.image)

        # parametre 
        
        Parametre = QVBoxLayout()

        choixLayout = QVBoxLayout()

        self.dossierButton = QPushButton("Choix d'un dossier")
        self.dossierButton.clicked.connect(self.charger_images_fit)
        choixLayout.addWidget(self.dossierButton)

        recherche = QHBoxLayout()

        self.barre_recherche = QLineEdit()
        self.barre_recherche.setPlaceholderText("Recherchez un astre")

        self.barre_degre = QLineEdit()
        self.barre_degre.setPlaceholderText("2.0")

        self.bouton_recherche = QPushButton("Recherche")
        self.bouton_recherche.clicked.connect(self.recherche_Images_Astrale)

        recherche.addWidget(self.barre_recherche, 3)
        recherche.addWidget(self.barre_degre, 1)
        recherche.addWidget(self.bouton_recherche)

        Parametre.addLayout(recherche)

        Parametre.addLayout(choixLayout)

        # separation 
        
        separation = QFrame()
        separation.setFrameShape(QFrame.Shape.HLine)
        separation.setFrameShadow(QFrame.Shadow.Sunken)
        choixLayout.addWidget(separation)

        # layer selection
        
        self.choix_layer = QVBoxLayout()
        Parametre.addLayout(self.choix_layer)
        
        # separation 
        
        choixLayout.addWidget(separation)

        # 
        
        label_info = QLabel("(Valeur R,G,B)")
        label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        choixLayout.addWidget(label_info)
        
        Parametre.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        mainLayout.addLayout(Parametre)

    def recherche_Images_Astrale(self):
        deg = self.barre_degre.text()

        if deg:
            try:
                deg = float(deg)

                if deg > 20.0 or deg < 0.0:
                    deg = None

            except ValueError:
                PopUpError("Attention, votre angle de vue doit etre un nombre a virgule de la force : '3.5'").exec()
                self.barre_degre.clear()
                deg = None

        coord = self.barre_recherche.text()
        if coord:
            self.download_thread = QThread()
            self.download_worker = classDownload(coord, deg)

            self.download_worker.finished.connect(self.on_download_finished)
            self.download_worker.error.connect(self.on_download_error)

            self.download_worker.moveToThread(self.download_thread)

            self.download_thread.started.connect(self.download_worker.run)

            self.download_worker.finished.connect(self.download_thread.quit)
            self.download_worker.finished.connect(self.download_worker.deleteLater)
            self.download_thread.finished.connect(self.download_thread.deleteLater)

            self.download_thread.start()

    def on_download_finished(self):
        PopUpInfo("Le téléchargement des images est terminé !").exec()

    def on_download_error(self, message):
        PopUpError(f"Erreur lors du téléchargement : {message}").exec()

    def charger_images_fit(self):
        dossier_path = QFileDialog.getExistingDirectory(self, "Choisir un dossier contenant des fichiers FIT")
        if dossier_path:
            try:
                self.render = classRenderImage(dossier_path)
                
                self.render.compilation_rgb()
                self.render.compilation_noir_blanc()

                image_rgb = self.render.get_image_rgb()
                
                self.image.setPixmap(image_rgb)
                self.charger_layer(dossier_path)
                
                #self.render.get_images_utiliser()
            except Exception as e:
                PopUpError("Une erreur est survenue").exec()
                print(e)

    def charger_layer(self, chemin):
        while self.choix_layer.count():
            item = self.choix_layer.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        fichiers = []
        for fichier in os.listdir(chemin):
            if fichier.endswith((".fit", ".fits")):
                fichiers.append(os.path.basename(fichier))

        colors = ["255, 0, 0", "0, 255, 0", "0, 0, 255"]
        data = {}

        for i in range(len(fichiers)):
            data[colors[i % len(colors)]] = fichiers[i]

        widget = classDragDropWidget(data)
        widget.nouvelle_ordre.connect(self.ordre_changer)
        
        self.choix_layer.addWidget(widget)
        
        label_info = QLabel("(Vue noir et blanc)")
        label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
        self.choix_layer.addWidget(label_info)
        
        valeur_noir_blanc = np.dstack([self.render.image_noir_blanc] * 3)
        
        image_noir_blanc = ImageWidget()
        image_noir_blanc.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        image_noir_blanc.setPixmap(valeur_noir_blanc)
        
        self.choix_layer.addWidget(image_noir_blanc)
        

    def ordre_changer(self, nouvel_ordre):
        self.render.compilation_rgb(nouvel_ordre)
        
        image_rgb = self.render.get_image_rgb()

        self.image.setPixmap(image_rgb)
        #print("Nouvel ordre :", nouvel_ordre)
        
    """ 
    def bouton_cliquer(self):
        bouton = self.sender()
        if bouton:
            fichier_path = bouton.property("filepath")
            if "Retirer" in bouton.text():
                self.render.change_valeur(fichier_path)
                bouton.setText(f"Ajouter {os.path.basename(fichier_path)}")
            else:
                self.render.change_valeur(fichier_path)
                bouton.setText(f"Retirer {os.path.basename(fichier_path)}")

            self.render.compilation()
            image_rgb = self.render.get_image_values()
            self.image.setPixmap(image_rgb)
     """        
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
