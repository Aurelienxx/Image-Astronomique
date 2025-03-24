# Code réaliser par : 
#   Dusannier Léothen
#   Fontaine Aurélien 

from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QApplication, QHBoxLayout
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QDrag

import sys

class classDraggableButton(QPushButton):
    button_dropped = pyqtSignal()

    def __init__(self, text, ordre: int, parent=None):
        super().__init__(text, parent)
        self.setAcceptDrops(True)
        self.ordre = ordre

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        dragged_text = event.mimeData().text()
        current_text = self.text()

        self.setText(dragged_text)
        source = event.source()

        if isinstance(source, classDraggableButton):
            source.setText(current_text)

            # Échange l'ordre des boutons et leur valeur d'ordre assigner
            source_ordre = source.get_ordre()
            source.set_ordre(self.get_ordre())
            self.set_ordre(source_ordre)

            self.button_dropped.emit()

    def get_ordre(self):
        return self.ordre

    def set_ordre(self, new_ordre):
        self.ordre = new_ordre
            
if __name__ == "__main__":
    data = "Bouton"
    
    app = QApplication(sys.argv)
    window = classDraggableButton(data)
    window.show()
    sys.exit(app.exec())