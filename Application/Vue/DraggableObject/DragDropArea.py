# Code réaliser par : 
#   Dusannier Léothen
#   Fontaine Aurélien 

from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QApplication, QHBoxLayout
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QDrag

import sys

from .DraggableButton import classDraggableButton

class classDragDropWidget(QWidget):
    nouvelle_ordre = pyqtSignal(list)

    def __init__(self, data:dict):
        """
        Créer une zone de ou seront afficher des boutons déplaceable. Pour chaque bouton est associé une couleur 
        qui est visuellement indiquer a l'utilisateur grace un widget de cette couleur. 
        
        param : 
            data : dict -> une valeur RGB associé a un nom 
        """
        super().__init__()
        self.setAcceptDrops(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.buttons = []  

        ordre = 0
        for color, name in data.items():
            row_layout = QHBoxLayout()

            color_block = QWidget(self)
            color_block.setFixedSize(20, 20)
            color_block.setStyleSheet(f"background-color: rgb({color});")

            button = classDraggableButton(f"{name}", ordre, self)
            button.button_dropped.connect(self.emit_nouvelle_ordre)

            row_layout.addWidget(color_block)
            row_layout.addWidget(button)

            self.layout.addLayout(row_layout)
            self.buttons.append(button)  
            ordre = ordre + 1
            
    def emit_nouvelle_ordre(self):
        order = []
        for i in range(self.layout.count()):
            row_layout = self.layout.itemAt(i).layout()
            if row_layout:
                button = row_layout.itemAt(1).widget()
                if button:
                    order.append(button.get_ordre())

        self.nouvelle_ordre.emit(order)
            
if __name__ == "__main__":
    data = {
        "255, 0, 0" : "red",
        "0, 0, 255" : "blue",
        "0, 255, 0" : "green",
        "255, 125, 0" : "Orange",
        "0, 125, 255" : "light blue"
    }
    
    app = QApplication(sys.argv)
    window = classDragDropWidget(data)
    window.show()
    sys.exit(app.exec())