import json
import os
from PyQt5.QtWidgets import QApplication, QLabel, QTabBar, QLayout, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from modules.settings import check_if_settings_exist, load_settings_json
from modules.api import get_data_from_scryfall
from dotenv import load_dotenv

load_dotenv()
SETTINGS_FILE_PATH = os.getenv('SETTINGS_FILE_PATH')

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

check_if_settings_exist(SETTINGS_FILE_PATH)
get_data_from_scryfall()

with open('downloads/Default Cards.json', 'r', encoding='utf8') as f:
    j = json.load(f)

###DEBUG###
def check_max_and_count(str):
    max = 0
    for element in j:
        try:
            if len(element[str]) > max:
                max = len(element[str])
        except:
            pass
    print(f'Maximum number of occurences: {max}')

check_max_and_count('multiverse_ids')