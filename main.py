import zlib
import json
from modules.settings import check_if_settings_exist, build_folder_structure, load_settings
from modules.api import get_data_from_scryfall
from modules.collection import create_default_collection
from modules.deck import create_default_deck
from modules.consts import SETTINGS_FILE_PATH, DATABASE_PATH
from modules.database.create import create_main_table, create_sub_table
from modules.database.alpha import alpha_load
from modules.database.batch import create_connection, batch_load
from PyQt5.QtWidgets import QApplication, QLabel, QTabBar, QLayout, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap

build_folder_structure()
check_if_settings_exist(SETTINGS_FILE_PATH)
#settings = load_settings() - unnecessary for now
get_data_from_scryfall()
create_default_collection()
create_default_deck()
#build_db()

#debug
'''
with open('downloads/Default Cards.json', 'r', encoding='utf8') as f:
    j = json.load(f)
'''
settings_json = load_settings(SETTINGS_FILE_PATH)
if settings_json['debug_mode']:
    connection = create_connection(DATABASE_PATH)
    #create_main_table(connection)
    #create_sub_table(connection, 'multiverse_id')
    #alpha_load(connection)
    batch_load(connection)
    connection.close()

###APP###
'''
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
'''