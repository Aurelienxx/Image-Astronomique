# Code réaliser par : 
#   Dusannier Léothen
#   Fontaine Aurélien 

import sys
from PyQt6.QtWidgets import QInputDialog, QMessageBox, QWidget, QHBoxLayout, \
    QVBoxLayout, QLabel, QVBoxLayout, QWidget, QSlider
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt,pyqtSignal

# --- class PopUpInfo : herite de QInputdialog --------------------------

class PopUpInfo(QMessageBox):

    def __init__(self,message:str="message par defaut",nom_fenetre:str="Info"):
        """Permet de créer une pop up avec un message personnalisé qui demande un input text a l'utilisateur"""
        super().__init__()

        self.setWindowTitle(nom_fenetre)
        self.setText(message)
        self.setWindowIcon(QIcon.fromTheme("dialog-information"))

# --- class Error : herite de QInputdialog --------------------------

class PopUpError(QMessageBox):
    def __init__(self,message:str="message par defaut",nom_fenetre:str="Erreur"):
        """Permet de créer une pop up avec un message personnalisé qui demande un input text a l'utilisateur"""
        super().__init__()

        self.setWindowTitle(nom_fenetre)
        self.setText(message)
        self.setWindowIcon(QIcon.fromTheme("dialog-error")) 
        
class PopUpError213(QMessageBox):

    def __init__(self,message:str="Cette action écrasera votre travail actuel, nous vous conseillons de sauvegarder",nom_fenetre:str="Progrès non sauvegardé"):
        """ Permet de créer une pop-up personnalisée, qui permet de prévenir l'utilisateur """
        super().__init__()
        self.setWindowIcon(QIcon(sys.path[0] + '/icones/reglages.png'))
        self.setWindowTitle(nom_fenetre)

        self.setText(message)
        self.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
        self.setDefaultButton(QMessageBox.StandardButton.Cancel)

