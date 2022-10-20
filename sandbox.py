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
app_groupbox = QGroupBox()
app_layout = QGridLayout()
app_groupbox.setLayout(app_layout)
app_layout.setParent(app_groupbox)

def create_ui():
    for i in reversed(range(app_layout.count())): 
        app_layout.itemAt(i).widget().setParent(None)

    for i in range(5):
        for j in range(5):
            groupbox = QGroupBox()
            groupbox_layout = QVBoxLayout()

            label = QLabel()
            label.setText(f"starting size: x:{groupbox.geometry().width()}, y:{groupbox.geometry().height()}")
            label.setObjectName('label')
            frame = QLabel()
            frame.setText(f"frame: x:{groupbox.frameGeometry().width()}, y:{groupbox.frameGeometry().height()}")
            frame.setObjectName('frame')
            geometry = QLabel()
            geometry.setText(f"geometry: x:{groupbox.geometry().width()}, y:{groupbox.geometry().height()}")
            geometry.setObjectName('geometry')
            size_hint = QLabel()
            size_hint.setText(f"size_hint: x:{groupbox.sizeHint().width()}, y:{groupbox.sizeHint().height()}")
            size_hint.setObjectName('size_hint')
            groupbox_layout.addWidget(label)
            groupbox_layout.addWidget(frame)
            groupbox_layout.addWidget(geometry)
            groupbox_layout.addWidget(size_hint)
            
            groupbox.setLayout(groupbox_layout)
            groupbox_layout.setParent(groupbox)

            app_layout.addWidget(groupbox, i, j)
    
    ui.setWindowTitle(f"W: {groupbox.geometry().width()}, H: {groupbox.geometry().height()}")

def resize_ui():
    #children = []
    for i, row in enumerate(range(app_layout.rowCount())):
        for j, col in enumerate(range(app_layout.columnCount())):
            if app_layout.count() != 0:
                current_groupbox = app_layout.itemAtPosition(row, col).widget()
                #children.append(current_groupbox.findChildren(QLabel, 'image'))
                for child in current_groupbox.findChildren(QLabel, 'frame'):
                    child.setText(f"frame: x:{current_groupbox.frameGeometry().width()}, y:{current_groupbox.frameGeometry().height()}")
                for child in current_groupbox.findChildren(QLabel, 'geometry'):
                    child.setText(f"geometry: x:{current_groupbox.geometry().width()}, y:{current_groupbox.geometry().height()}")
                for child in current_groupbox.findChildren(QLabel, 'size_hint'):
                    child.setText(f"size_hint: x:{child.sizeHint().width()}, y:{child.sizeHint().height()}")
    #print(children)

class UI(QWidget):
    def __init__(self, parent=None) -> None:
        super(UI, self).__init__(parent)
        self.setLayout(app_layout)
        
    def resizeEvent(self, event) -> None:
        resize_ui()
        QWidget.resizeEvent(self, event)

ui = UI()
create_ui()
ui.show()
#ui.showMaximized()
app.exec()