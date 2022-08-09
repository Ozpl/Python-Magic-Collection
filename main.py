import json
from modules.settings import check_if_settings_exist
from modules.api import get_data_from_scryfall
from PyQt5.QtWidgets import QApplication, QLabel, QTabBar, QLayout, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap

SETTINGS_FILE_PATH = './settings.json'

#build_file_structures()
check_if_settings_exist(SETTINGS_FILE_PATH)
get_data_from_scryfall()
#build_db()

#swap Default Cards to variable from settings
with open('downloads/Default Cards.json', 'r', encoding='utf8') as f:
    j = json.load(f)

###APP###
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
#app.exec()