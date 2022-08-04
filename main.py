import json
import os
from PyQt5.QtWidgets import QApplication, QLabel
from modules.settings import check_if_settings_exists
from dotenv import load_dotenv

load_dotenv()

'''
app = QApplication([])
label = QLabel('Hello World!')
label.show()

app.exec()
'''

check_if_settings_exists(os.getenv('SETTINGS_FILE_PATH'))

with open('downloads/Default Cards.json', 'r', encoding='utf8') as f:
    j = json.load(f)

for element in j:
    if element['id'] == '8fc108a3-15e5-44ab-a6e2-182b309f9c0c':
        print(element)
print(len(j))