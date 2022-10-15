from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton, QRadioButton, QScrollArea, QTabWidget, QVBoxLayout, QWidget

#1. Create grid QGridLayout()
#2. Create item QGroupBox()
#3. Create item's layout QVBoxLayout()
#4. Create widgets
#5. Add widgets to layout
#6. Set item's layout
#7. Set layout's parent to item
#8. Add groupbox to grid
#9. Search results in grid via itemAtPosition and findChildren

app = QApplication([])
app_layout = QGridLayout()

for i in range(5):
    for j in range(5):
        groupbox = QGroupBox()
        groupbox_layout = QVBoxLayout()

        label = QLabel()
        label.setText(f"label: {i+1}{j+1}")
        label.setObjectName('label')
        image_label = QLabel()
        image_label.setText(f"image: {i+1}{j+1}")
        image_label.setObjectName('image')
        groupbox_layout.addWidget(label)
        groupbox_layout.addWidget(image_label)
        
        groupbox.setLayout(groupbox_layout)
        groupbox_layout.setParent(groupbox)

        app_layout.addWidget(groupbox, i, j)

####
class UI(QWidget):
    def __init__(self, parent=None) -> None:
        super(UI, self).__init__(parent)
        self.setLayout(app_layout)

ui = UI()

children = []
for i, row in enumerate(range(app_layout.rowCount())):
    for j, col in enumerate(range(app_layout.columnCount())):
        current_groupbox = app_layout.itemAtPosition(row, col).widget()
        children.append(current_groupbox.findChildren(QLabel, 'image'))
        for child in current_groupbox.findChildren(QLabel, 'image'):
            child.setText(f"found: {i}{j}")
print(children)

ui.show()
#ui.showMaximized()
app.exec()