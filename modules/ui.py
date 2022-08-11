from PyQt5.QtWidgets import QApplication, QLabel, QTabBar, QLayout, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap

def create_ui():
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle('QHBoxLayout')
    layout = QVBoxLayout()
    layout.addWidget(QPushButton('Left'))
    layout.addWidget(QPushButton('Center'))
    layout.addWidget(QPushButton('Right'))
    bar = QTabBar()
    bar.addTab('xD')
    bar.addTab('kek')
    layout.addWidget(bar)
    image_label = QLabel()
    image = QPixmap('images/topkek.jpg')
    image_label.setPixmap(image)
    layout.addWidget(image_label)
    window.setLayout(layout)
    window.show()
    app.exec()