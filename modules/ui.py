from ast import literal_eval
from os import path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton, QRadioButton, QScrollArea, QTabWidget, QVBoxLayout, QWidget
from requests import get
from shutil import copyfileobj
from modules.database.database_functions import get_card_from_db, get_card_ids_list
from modules.database.query import construct_query
from modules.database.collections import add_card_to_collection, create_collection, get_all_collections_names_as_array, get_card_from_collection
from modules.globals import config
from modules.logging import console_log

if path.exists('config.ini'):
    if config.get('COLLECTION', 'image_type') == 'png': image_extension = 'png'
    else: image_extension = 'jpg'

app = QApplication([])
app_lyt = QVBoxLayout()
tab_bar = QTabWidget()

#FIXME remove ids
filtered_cards = ['0000579f-7b35-4ed3-b44c-db2a538066fe', '0005968a-8708-441b-b9a1-9373aeb8114d', '000d609c-deb7-4bd7-9c1d-e20fb3ed4f5f', '00154b70-57d2-4c32-860f-1c36fc49b10c', '001cc57e-f3fc-4790-a9e5-171b2e3e8739']
add_cards_found_cards = []

widget_hierarchy = [
{'name': 'cor', 'type': 'QWidget'},
    {'name': 'cor_lyt', 'type': 'QHBoxLayout'},
        {'name': 'cor_lyt_chk', 'type': 'QCheckBox'},
        {'name': 'cor_lyt_btn', 'type': 'QPushButton'},
        {'name': 'cor_lyt_cmb', 'type': 'QComboBox'},

{'name': 'col = QWidget'},
    {'name': 'col_lyt', 'type': 'QHBoxLayout'},
        {'name': 'col_lyt_crd', 'type': 'QGroupBox'},
            {'name': 'col_lyt_crd_lyt', 'type': 'QVBoxLayout'},
                {'name': 'col_lyt_crd_lyt_flt', 'type': 'QGroupBox'},
                    {'name': 'col_lyt_crd_lyt_flt_lyt', 'type': 'QHBoxLayout'},
                        {'name': 'col_lyt_crd_lyt_flt_lyt_clr', 'type': '[QLabel]'},
                        {'name': 'col_lyt_crd_lyt_flt_lyt_and', 'type': 'QRadioButton'},
                        {'name': 'col_lyt_crd_lyt_flt_lyt_orr', 'type': 'QRadioButton'},
                        {'name': 'col_lyt_crd_lyt_flt_lyt_cmc', 'type': '[QLabel]'},
                        {'name': 'col_lyt_crd_lyt_flt_lyt_slb', 'type': 'QLabel'},
                        {'name': 'col_lyt_crd_lyt_flt_lyt_sbx', 'type': 'QLineEdit'},
                        {'name': 'col_lyt_crd_lyt_flt_lyt_sbu', 'type': 'QPushButton'},
                {'name': 'col_lyt_crd_lyt_tag', 'type': 'QGroupBox'},
                    {'name': 'col_lyt_crd_lyt_tag_lyt', 'type': 'QHBoxLayout'},
                {'name': 'col_lyt_crd_lyt_grd', 'type': 'QGroupBox'},
                    {'name': 'col_lyt_crd_lyt_grd_lyt', 'type': 'QGridLayout'},
                        #Inside col_lyt_crd_lyt_grd_lyt
                        {'name': 'col_lyt_crd_lyt_grd_lyt_crd', 'type': '[QGroupBox]'},
                            {'name': 'col_lyt_crd_lyt_grd_lyt_crd_lyt', 'type': '[QVBoxLayout]'},
                                {'name': 'col_lyt_crd_lyt_grd_lyt_crd_lyt_lbl', 'type': 'QLabel'},
                                {'name': 'col_lyt_crd_lyt_grd_lyt_crd_lyt_iml', 'type': 'QLabel'},
                                    {'name': 'col_lyt_crd_lyt_grd_lyt_crd_lyt_iml_pix', 'type': 'QPixMap'},
        {'name': 'col_lyt_pre', 'type': 'QGroupBox'},
            {'name': 'col_lyt_pre_lyt', 'type': 'QVBoxLayout'},
                {'name': 'col_lyt_pre_lyt_iml', 'type': 'QLabel'},
                    {'name': 'col_lyt_pre_lyt_iml_pix', 'type': 'QPixmap'},
                {'name': 'col_lyt_pre_lyt_inf', 'type': 'QLabel'},
                {'name': 'col_lyt_pre_lyt_des', 'type': 'QScrollArea'},
                    {'name': 'col_lyt_pre_lyt_des_lbl', 'type': 'QLabel'},
                {'name': 'col_lyt_pre_lyt_tag', 'type': 'QLabel'},

{'name': 'add', 'type': 'QWidget'},
    {'name': 'add_lyt', 'type': 'QHBoxLayout'},
        {'name': 'add_lyt_gbx', 'type': 'QGroupBox'},
            {'name': 'add_lyt_gbx_lyt', 'type': 'QHBoxLayout'},
                {'name': 'add_lyt_gbx_lyt_src', 'type': 'QGroupBox'},
                    {'name': 'add_lyt_gbx_lyt_src_lyt', 'type': 'QVBoxLayout'},
                        {'name': 'add_lyt_gbx_lyt_src_lyt_lbl', 'type': 'QLabel'},
                        {'name': 'add_lyt_gbx_lyt_src_lyt_sbx', 'type': 'QLineEdit'},
                        {'name': 'add_lyt_gbx_lyt_src_lyt_but', 'type': 'QPushButton'},
                {'name': 'add_lyt_gbx_lyt_lst', 'type': 'QListWidget'},
                {'name': 'add_lyt_gbx_lyt_res', 'type': 'QGroupBox'},
                    {'name': 'add_lyt_gbx_lyt_res_lyt', 'type': 'QVBoxLayout'},
                        {'name': 'add_lyt_gbx_lyt_res_lyt_lbl', 'type': 'QLabel'},
                        {'name': 'add_lyt_gbx_lyt_res_lyt_iml', 'type': 'QLabel'},
                            {'name': 'add_lyt_gbx_lyt_res_lyt_iml_pix', 'type': 'QPixmap'},
                        {'name': 'add_lyt_gbx_lyt_res_lyt_adr', 'type': 'QPushButton'},
                        {'name': 'add_lyt_gbx_lyt_res_lyt_adf', 'type': 'QPushButton'},
                        #TODO
                        #Set card count buttons

{'name': 'stt', 'type': 'QWidget'},
    {'name': 'stt_lyt', 'type': 'QVBoxLayout'},
]

cor = QWidget()
cor_lyt = QHBoxLayout()
cor_lyt_chk = QCheckBox('Show whole database instead of just a collection')
cor_lyt_btn = QPushButton('Add new collection')
cor_lyt_cmb = QComboBox()

col = QWidget()
col_lyt = QHBoxLayout()
col_lyt_crd = QGroupBox()
col_lyt_crd_lyt = QVBoxLayout()
col_lyt_crd_lyt_flt = QGroupBox()
col_lyt_crd_lyt_flt_lyt = QHBoxLayout()
col_lyt_crd_lyt_flt_lyt_clr = [QLabel('W'), QLabel('U'), QLabel('B'), QLabel('R'), QLabel('G')]
col_lyt_crd_lyt_flt_lyt_and = QRadioButton('And')
col_lyt_crd_lyt_flt_lyt_orr = QRadioButton('Or')
col_lyt_crd_lyt_flt_lyt_cmc = [QLabel('0'), QLabel('1'), QLabel('2'), QLabel('3'), QLabel('4'), QLabel('5'), QLabel('6'), QLabel('7'), QLabel('8'), QLabel('9')]
col_lyt_crd_lyt_flt_lyt_slb = QLabel('Search cards:')
col_lyt_crd_lyt_flt_lyt_sbx = QLineEdit('thassa')
col_lyt_crd_lyt_flt_lyt_sbu = QPushButton('Search')
col_lyt_crd_lyt_tag = QGroupBox()
col_lyt_crd_lyt_tag_lyt = QHBoxLayout()
col_lyt_crd_lyt_grd = QGroupBox()
col_lyt_crd_lyt_grd_lyt = QGridLayout()
col_lyt_crd_lyt_grd_lyt_crd = [] #[QGroupBox]
col_lyt_crd_lyt_grd_lyt_crd_lyt = [] #[QVBoxLayout]
col_lyt_crd_lyt_grd_lyt_crd_lyt_lbl = [] #[QLabel]
col_lyt_crd_lyt_grd_lyt_crd_lyt_iml = [] #[QLabel]
col_lyt_crd_lyt_grd_lyt_crd_lyt_iml_pix = [] #[QPixmap]
col_lyt_pre = QGroupBox()
col_lyt_pre_lyt = QVBoxLayout()
col_lyt_pre_lyt_iml = QLabel()
col_lyt_pre_lyt_iml_pix = QPixmap()
col_lyt_pre_lyt_inf = QLabel('Regular: X Foil: X   EUR: 1345.99E USD: 1345.99D')
col_lyt_pre_lyt_des = QScrollArea()
col_lyt_pre_lyt_des_lbl = QLabel('This is card description')
col_lyt_pre_lyt_tag = QLabel('These are card tags')

add = QWidget()
add_lyt = QHBoxLayout()
add_lyt_gbx = QGroupBox()
add_lyt_gbx_lyt = QHBoxLayout()
add_lyt_gbx_lyt_src = QGroupBox()
add_lyt_gbx_lyt_src_lyt = QVBoxLayout()
add_lyt_gbx_lyt_src_lyt_lbl = QLabel('Type name of searched card:')
add_lyt_gbx_lyt_src_lyt_sbx = QLineEdit('Thassa')
add_lyt_gbx_lyt_src_lyt_but = QPushButton('Search')
add_lyt_gbx_lyt_lst = QListWidget()
add_lyt_gbx_lyt_res = QGroupBox()
add_lyt_gbx_lyt_res_lyt = QVBoxLayout()
add_lyt_gbx_lyt_res_lyt_lbl = QLabel()
add_lyt_gbx_lyt_res_lyt_iml = QLabel()
add_lyt_gbx_lyt_res_lyt_iml_pix = QPixmap()
add_lyt_gbx_lyt_res_lyt_adr = QPushButton('Add 1 regular')
add_lyt_gbx_lyt_res_lyt_adf = QPushButton('Add 1 foil')

stt = QWidget()
stt_lyt = QVBoxLayout()

#Main
def create_user_interface(db_connection, cl_connection, cd_connection):
    global database_connection, collections_connection, cards_connection
    database_connection = db_connection
    collections_connection = cl_connection
    cards_connection = cd_connection
    console_log('info', 'Creating UI...')
    ui = UI()
    #ui.showMaximized()
    ui.show()
    app.exec()

#AddWindow Class
class AddCollectionWindow(QWidget):
    def __init__(self, parent=None):
        super(AddCollectionWindow, self).__init__(parent)
        
        self.setWindowTitle('Add collection')
        self.setMinimumSize(300,100)
        self.setMaximumSize(300,100)

        layout = QVBoxLayout()
        self.label = QLabel("Enter the name of your new collection:")
        self.line_edit = QLineEdit()
        self.button = QPushButton('Confirm')
        self.button.clicked.connect(self.confirm_button_pressed)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def confirm_button_pressed(self):
        create_collection(collections_connection, self.line_edit.text())
        refresh_collection_names()
        #Add window prompt - succesful or not
        self.close()

#UI Class and its Events
class UI(QWidget):
    def __init__(self, parent=None) -> None:
        super(UI, self).__init__(parent)

        create_corner_widget()
        create_collection_tab()
        create_decks_tab()
        create_add_cards_tab()
        create_wishlist_tab()
        create_import_export_tab()
        create_settings_tab()

        refresh_collection_names()

        app_lyt.addWidget(tab_bar)
        self.setLayout(app_lyt)
        
        self.app_font = QFont(config.get('APP', 'font'), config.get_int('APP', 'font_size'))
        self.setFont(self.app_font)
        self.setWindowTitle(f"{config.get('APP', 'name')} - X:{self.x()}, Y:{self.y()}, W:{self.width()}, H:{self.height()}")
        QApplication.setStyle(config.get('APP', 'style'))

    def resizeEvent(self, event) -> None:
        self.setWindowTitle(f"{config.get('APP', 'name')} - X:{self.x()}, Y:{self.y()}, W:{self.width()}, H:{self.height()}")
        update_sizes_of_collection_tab()
        QWidget.resizeEvent(self, event)

#Global functions
def download_image_if_not_downloaded(id):
    file_name = f"{config.get('FOLDER', 'cards')}/{id}.{image_extension}"

    if not path.exists(file_name):
        card = get_card_from_db(database_connection, id)
        image_uris = literal_eval(card['image_uris'])
        r = get(image_uris[config.get('COLLECTION', 'image_type')], stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(file_name,'wb') as f:
                copyfileobj(r.raw, f)
def return_grid_cards_groupboxes():
    groupboxes = []
    n_cards = config.get_int('COLLECTION', 'grid_number_of_cards')
    n_rows = config.get_int('COLLECTION', 'grid_number_of_rows')
    cards_per_row = int(n_cards / n_rows)

    for i in range(n_rows):
        for j in range(cards_per_row):
            groupboxes.append(col_lyt_crd_lyt_grd_lyt.itemAtPosition(i,j).widget())
    return groupboxes

#Corner
def create_corner_widget():
    cor.setMinimumHeight(40)
    cor_lyt_cmb.setMinimumWidth(200)
    tab_bar.setCornerWidget(cor)
    cor.setLayout(cor_lyt)
    cor_lyt.addWidget(cor_lyt_btn)
    cor_lyt_btn.clicked.connect(add_collection_button_pressed)
    cor_lyt.addWidget(cor_lyt_cmb)
    cor_lyt.addWidget(cor_lyt_chk)
#Corner -> Events
add_collection = AddCollectionWindow()
def add_collection_button_pressed():
    add_collection.show()
    add_collection.line_edit.setText('')
def refresh_collection_names():
    cor_lyt_cmb.clear()
    cor_lyt_cmb.addItems(get_all_collections_names_as_array(collections_connection))

#Collection
def create_collection_tab():
    #Hierarchy
    tab_bar.addTab(col, config.get('APP', 'collection'))
    col.setLayout(col_lyt)
    col_lyt.addChildWidget(col_lyt_crd)
    col_lyt_crd.setLayout(col_lyt_crd_lyt)
    col_lyt_crd_lyt.addChildWidget(col_lyt_crd_lyt_flt)
    col_lyt_crd_lyt_flt.setLayout(col_lyt_crd_lyt_flt_lyt)
    [col_lyt_crd_lyt_flt_lyt.addChildWidget(element) for element in col_lyt_crd_lyt_flt_lyt_clr]
    col_lyt_crd_lyt_flt_lyt.addChildWidget(col_lyt_crd_lyt_flt_lyt_and)
    col_lyt_crd_lyt_flt_lyt.addChildWidget(col_lyt_crd_lyt_flt_lyt_orr)
    [col_lyt_crd_lyt_flt_lyt.addChildWidget(element) for element in col_lyt_crd_lyt_flt_lyt_cmc]
    col_lyt_crd_lyt_flt_lyt.addChildWidget(col_lyt_crd_lyt_flt_lyt_slb)
    col_lyt_crd_lyt_flt_lyt.addChildWidget(col_lyt_crd_lyt_flt_lyt_sbx)
    col_lyt_crd_lyt_flt_lyt.addChildWidget(col_lyt_crd_lyt_flt_lyt_sbu)
    col_lyt_crd_lyt.addChildWidget(col_lyt_crd_lyt_tag)
    col_lyt_crd_lyt_tag.setLayout(col_lyt_crd_lyt_tag_lyt)
    col_lyt_crd_lyt.addChildWidget(col_lyt_crd_lyt_grd)
    col_lyt_crd_lyt_grd.setLayout(col_lyt_crd_lyt_grd_lyt)
    col_lyt.addChildWidget(col_lyt_pre)
    col_lyt_pre.setLayout(col_lyt_pre_lyt)
    col_lyt_pre_lyt.addChildWidget(col_lyt_pre_lyt_iml)
    col_lyt_pre_lyt_iml.setPixmap(col_lyt_pre_lyt_iml_pix)
    col_lyt_pre_lyt.addChildWidget(col_lyt_pre_lyt_inf)
    col_lyt_pre_lyt.addChildWidget(col_lyt_pre_lyt_des)
    col_lyt_pre_lyt_des.setWidget(col_lyt_pre_lyt_des_lbl)
    col_lyt_pre_lyt.addChildWidget(col_lyt_pre_lyt_tag)

    create_collection_tab_filters()
    create_collection_tab_grid()
    create_collection_tab_preview()
    update_sizes_of_collection_tab()
#Collection -> Sizes
def update_sizes_of_collection_tab():
    col_lyt_pre.setMinimumWidth(383)
    col_lyt_pre.setMaximumWidth(383)

    col_lyt_crd_lyt_flt.setMinimumHeight(65)
    col_lyt_crd_lyt_flt.setMaximumHeight(65)
    col_lyt_crd_lyt_flt_lyt_sbx.setMinimumWidth(125)

    col_lyt_crd_lyt_tag.setMinimumHeight(50)
    col_lyt_crd_lyt_tag.setMaximumHeight(50)
    
    icon_size = col_lyt_crd_lyt_flt.height()-27
    for element in col_lyt_crd_lyt_flt_lyt_clr: element.setMaximumSize(icon_size, icon_size)
    for element in col_lyt_crd_lyt_flt_lyt_cmc: element.setMaximumSize(icon_size, icon_size)

    create_collection_tab_grid()
    #update_sizes_of_cards_in_grid()

#Collection -> Filters
def create_collection_tab_filters():
    for element in col_lyt_crd_lyt_flt_lyt_clr:
        element.setScaledContents(True)
        element.setPixmap(QPixmap(f"{config.get('FOLDER', 'symbols')}/{element.text()}"))

    for element in col_lyt_crd_lyt_flt_lyt_cmc:
        element.setScaledContents(True)
        element.setPixmap(QPixmap(f"{config.get('FOLDER', 'symbols')}/{element.text()}"))

    col_lyt_crd_lyt_flt_lyt_sbu.clicked.connect(collection_filters_searchbox_pressed)
#Collection -> Filters -> Events
def collection_filters_searchbox_pressed():
    if col_lyt_crd_lyt_flt_lyt_sbx.text():
        filtered_cards = get_card_ids_list(database_connection, construct_query(col_lyt_crd_lyt_flt_lyt_sbx.text()))
        for id in filtered_cards:
            download_image_if_not_downloaded(id)

        for i, element in enumerate(return_grid_cards_groupboxes()):
            if i == len(filtered_cards): break
            file_name = f"{config.get('FOLDER', 'cards')}/{filtered_cards[i]}.{image_extension}"

            #0 - layout, 1 - label, 2 - image
            element.children()[1].setText(f'{filtered_cards[i]}')
            element.children()[2].setPixmap(QPixmap(file_name))
    else:
        filtered_cards = []
#Collection -> Grid
def create_collection_tab_grid():
    n_cards = config.get_int('COLLECTION', 'grid_number_of_cards')
    n_rows = config.get_int('COLLECTION', 'grid_number_of_rows')
    cards_per_row = int(n_cards / n_rows)
    
    gbx_width = int(col_lyt_crd_lyt_grd.geometry().width() / cards_per_row)
    gbx_height = int(col_lyt_crd_lyt_grd.geometry().height() / n_rows)

    #Clear all cards in grid
    for i in reversed(range(col_lyt_crd_lyt_grd_lyt.count())):
        col_lyt_crd_lyt_grd_lyt.itemAt(i).widget().setParent(None)
    col_lyt_crd_lyt_grd_lyt_crd.clear()
    col_lyt_crd_lyt_grd_lyt_crd_lyt.clear()
    col_lyt_crd_lyt_grd_lyt_crd_lyt_lbl.clear()
    col_lyt_crd_lyt_grd_lyt_crd_lyt_iml.clear()
    col_lyt_crd_lyt_grd_lyt_crd_lyt_iml_pix.clear()

    if len(filtered_cards) > 0:
        for i in range(n_rows):
            for j in range(cards_per_row):
                if (cards_per_row * i + j) + 1 <= len(filtered_cards):
                    card = get_card_from_db(database_connection, filtered_cards[cards_per_row * i + j])
                    image_uris = literal_eval(card['image_uris'])
                    [download_image_if_not_downloaded(card['id']) for element in image_uris if element == config.get('COLLECTION', 'image_type')]

                    gbx = QGroupBox()
                    #gbx.setMaximumWidth(gbx_width)
                    #gbx.setMaximumHeight(gbx_height)
                    gbx_lyt = QVBoxLayout()
                    gbx_lyt.setAlignment(Qt.AlignCenter)
                    lbl = QLabel('Owned: 12/14 (26)')
                    lbl.setAlignment(Qt.AlignCenter)
                    lbl.setMaximumHeight(50)
                    iml = QLabel()
                    iml.setObjectName('Image')
                    temp = QPixmap(f"{config.get('FOLDER', 'cards')}/{card['id']}.{image_extension}")
                    imp = temp.scaled(gbx_height-50, gbx_height-50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    iml.setPixmap(imp)
                    gbx_lyt.addChildWidget(lbl)
                    gbx_lyt.addChildWidget(iml)
                    gbx.setLayout(gbx_lyt)
                    gbx_lyt.setParent(gbx)
                    #col_lyt_crd_lyt_grd_lyt.addWidget(gbx, i, j)
                    col_lyt_crd_lyt_grd_lyt.addChildWidget(gbx)
                    col_lyt_crd_lyt_grd_lyt_crd.append(gbx)
                    col_lyt_crd_lyt_grd_lyt_crd_lyt.append(gbx_lyt)
                    col_lyt_crd_lyt_grd_lyt_crd_lyt_lbl.append(lbl)
                    col_lyt_crd_lyt_grd_lyt_crd_lyt_iml.append(iml)
                    col_lyt_crd_lyt_grd_lyt_crd_lyt_iml_pix.append(temp)
                else:
                    gbx = QGroupBox()
                    gbx.setMaximumWidth(gbx_width)
                    gbx.setMaximumHeight(gbx_height)
                    gbx_lyt = QVBoxLayout()
                    gbx.setLayout(gbx_lyt)
                    col_lyt_crd_lyt_grd_lyt.addWidget(gbx, i, j)
                    #col_lyt_crd_lyt_grd_lyt.addChildWidget(gbx)
                    col_lyt_crd_lyt_grd_lyt_crd.append(gbx)
                    col_lyt_crd_lyt_grd_lyt_crd_lyt.append(gbx_lyt)
#Collection -> Grid -> Events
def update_sizes_of_cards_in_grid():
    n_cards = config.get_int('COLLECTION', 'grid_number_of_cards')
    n_rows = config.get_int('COLLECTION', 'grid_number_of_rows')
    cards_per_row = int(n_cards / n_rows)

    gbx_height = int(col_lyt_crd_lyt_grd_lyt.itemAtPosition(0,0).geometry().height() / n_rows)

    results = col_lyt_crd_lyt_grd_lyt.findChildren(QVBoxLayout)

    '''
    for i, row in enumerate(range(col_lyt_crd_lyt_grd_lyt.rowCount())):
        for j, column in enumerate(range(col_lyt_crd_lyt_grd_lyt.columnCount())):
            current_index = (cards_per_row * i + j)
            item = col_lyt_crd_lyt_grd_lyt.itemAtPosition(row, column)
            if item is not None:
                groupbox = item.widget()
                groupbox_layout = groupbox.layout()
                for position in range(groupbox_layout.count()):
                    item = groupbox_layout.itemAt(position)
                    if item is not None:
                        if position == 1:
                            pix = col_lyt_crd_lyt_grd_lyt_crd_lyt_iml_pix[current_index].scaled(gbx_height-50, gbx_height-50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                            image = QLabel()
                            image.setPixmap(pix)
                            groupbox_layout.insertItem(position, image)
                            '''
#Collection -> Preview
def create_collection_tab_preview():
    col_lyt_pre_lyt_iml_pix = QPixmap(f'images/muldrotha_normal.jpg')
    pix = col_lyt_pre_lyt_iml_pix.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    col_lyt_pre_lyt_iml.setPixmap(pix)
    col_lyt_pre_lyt_inf.setWordWrap(True)

#Decks
def create_decks_tab():
    pass

#Add cards
def create_add_cards_tab():
    tab_bar.addTab(add, config.get('APP', 'add_cards'))
    add.setLayout(add_lyt)
    add_lyt.addWidget(add_lyt_gbx)
    add_lyt_gbx.setLayout(add_lyt_gbx_lyt)
    add_lyt_gbx_lyt.addWidget(add_lyt_gbx_lyt_src)
    add_lyt_gbx_lyt_src.setLayout(add_lyt_gbx_lyt_src_lyt)
    add_lyt_gbx_lyt_src_lyt.addWidget(add_lyt_gbx_lyt_src_lyt_lbl)
    add_lyt_gbx_lyt_src_lyt.addWidget(add_lyt_gbx_lyt_src_lyt_sbx)
    add_lyt_gbx_lyt_src_lyt.addWidget(add_lyt_gbx_lyt_src_lyt_but)
    add_lyt_gbx_lyt_src_lyt_but.clicked.connect(add_cards_search_button_pressed)
    add_lyt_gbx_lyt.addWidget(add_lyt_gbx_lyt_lst)
    add_lyt_gbx_lyt_lst.itemSelectionChanged.connect(add_cards_list_selection_changed)
    add_lyt_gbx_lyt.addWidget(add_lyt_gbx_lyt_res)
    add_lyt_gbx_lyt_res.setLayout(add_lyt_gbx_lyt_res_lyt)
    add_lyt_gbx_lyt_res_lyt.addWidget(add_lyt_gbx_lyt_res_lyt_lbl)
    add_lyt_gbx_lyt_res_lyt.addWidget(add_lyt_gbx_lyt_res_lyt_iml)
    add_lyt_gbx_lyt_res_lyt_iml.setPixmap(add_lyt_gbx_lyt_res_lyt_iml_pix)
    add_lyt_gbx_lyt_res_lyt.addWidget(add_lyt_gbx_lyt_res_lyt_adr)
    add_lyt_gbx_lyt_res_lyt_adr.clicked.connect(add_cards_add_regular)
    add_lyt_gbx_lyt_res_lyt.addWidget(add_lyt_gbx_lyt_res_lyt_adf)
    add_lyt_gbx_lyt_res_lyt_adf.clicked.connect(add_cards_add_foil)
#Add cards -> Search -> Events
def add_cards_search_button_pressed():
    global add_cards_found_cards, add_cards_sorted_list
    add_cards_found_cards = get_card_ids_list(database_connection, construct_query(f'name:"{add_lyt_gbx_lyt_src_lyt_sbx.text()}"'))
    
    add_lyt_gbx_lyt_lst.clear()

    unsorted_list = []

    for element in add_cards_found_cards:
        card = get_card_from_db(database_connection, element)
        unsorted_list.append({
            'id': card['id'],
            'name': card['name'],
            'set_name': card['set_name'],
            'collector_number': card['collector_number'],
            'released_at': card['released_at'],
            'sort_key': f"{str(int(card['cmc']))}{card['name'].lower()}",
            'display': f"{card['name']} ({card['collector_number']}) [{card['set_name']}] - {card['released_at']}"
            })
        download_image_if_not_downloaded(element)

    add_cards_sorted_list = sorted(unsorted_list, key=lambda d: d['released_at'])
    add_cards_found_cards = list(map(lambda d: d['id'], add_cards_sorted_list))

    add_lyt_gbx_lyt_lst.addItems(list(map(lambda d: d['display'], add_cards_sorted_list)))
def add_cards_list_selection_changed():
    current_index = add_lyt_gbx_lyt_lst.currentRow()
    file_name = f"{config.get('FOLDER', 'cards')}/{add_cards_found_cards[current_index]}.{image_extension}"
    add_lyt_gbx_lyt_res_lyt_iml.setPixmap(QPixmap(file_name))
    add_cards_update_card_count()
def add_cards_add_regular():
    add_card_to_collection(
        collections_connection,
        config.get('COLLECTION', 'current_collection'), 
        add_cards_found_cards[add_lyt_gbx_lyt_lst.currentRow()],
        1,
        0,
        'add',
        add_cards_sorted_list[add_lyt_gbx_lyt_lst.currentRow()]['sort_key'])    
    add_cards_update_card_count()
def add_cards_add_foil():
    add_card_to_collection(
        collections_connection,
        config.get('COLLECTION', 'current_collection'), 
        add_cards_found_cards[add_lyt_gbx_lyt_lst.currentRow()],
        0,
        1,
        'add',
        add_cards_sorted_list[add_lyt_gbx_lyt_lst.currentRow()]['sort_key'])
    add_cards_update_card_count()
def add_cards_update_card_count():
    selected_card = get_card_from_collection(collections_connection, config.get('COLLECTION', 'current_collection'), add_cards_found_cards[add_lyt_gbx_lyt_lst.currentRow()])

    add_lyt_gbx_lyt_res_lyt_lbl.setText(f"You currently have {selected_card['regular']} regulars and {selected_card['foil']} foils in collection")

#Wishlist
def create_wishlist_tab():
    pass

#Import/export
def create_import_export_tab():
    pass

#Settings
def create_settings_tab():
    tab_bar.addTab(stt, config.get('APP', 'settings'))
    stt.setLayout(stt_lyt)


'''
#Collection Tab -> Cards Layout -> 1. Filter Buttons
def create_filter_group_box():
    filter_gbx.setMaximumHeight(35+27)

    for symbol in ['W', 'U', 'B', 'R', 'G', 'C']:
        image_lbl = QLabel()
        image_lbl.setObjectName(symbol)
        image = QPixmap(f'images/symbols/{symbol}.svg')
        image_lbl.setPixmap(image)
        image_lbl.setScaledContents(True)
        image_lbl.setMaximumSize(35,35)
        #image_lbl.setStyleSheet("background-image: url(./images/muldrotha.png)")
        image_lbl.setStyleSheet("")
        filter_colors_lbls.append(image_lbl)
        image_lbl.mousePressEvent = test_mouse_pressed_event
        filter_lyt.addWidget(image_lbl)

    filter_and_rbt.setChecked(True)
    filter_and_rbt.setMaximumSize(60,30)
    #and_rbt.setSizePolicy(QSizePolicy.Policy)
    filter_lyt.addWidget(filter_and_rbt)
    filter_or_rbt.setMaximumSize(60,30)
    filter_lyt.addWidget(filter_or_rbt)

    for symbol in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        image_lbl = QLabel()
        image = QPixmap(f'images/symbols/{symbol}.svg')
        image_lbl.setObjectName(symbol)
        image_lbl.setPixmap(image)
        image_lbl.setScaledContents(True)
        image_lbl.setMaximumSize(35,35)
        #image_lbl.setStyleSheet("background-image: url(./images/muldrotha.png)")
        image_lbl.setStyleSheet("")
        filter_mv.append(image_lbl)
        image_lbl.mousePressEvent = test_mouse_pressed_event
        filter_lyt.addWidget(image_lbl)

    filter_lyt.addWidget(filter_search_lbl)

    filter_search_txb.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    filter_search_txb.setMinimumWidth(200)
    filter_lyt.addWidget(filter_search_txb)

    filter_lyt.addWidget(filter_search_button)

    filter_gbx.setLayout(filter_lyt)
#Collection Tab -> Cards Layout -> 1. Filter Buttons -> Events
def test_mouse_pressed_event(event):
    #from mapToGlobal and widgets size you can grab which image was pressed
    for element in (filter_colors_lbls + filter_mv):
        mouse_x = event.globalPos().x()
        mouse_y = event.globalPos().y()
        element_x = element.mapToGlobal(QPoint(0, 0)).x()
        element_y = element.mapToGlobal(QPoint(0, 0)).y()
        element_w = element.width()
        element_h = element.height()
        if mouse_x > element_x and mouse_x < (element_x + element_w) and mouse_y > element_y and mouse_y < (element_y + element_h):
            if element in filter_colors_flags:
                element.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
                del filter_colors_flags[filter_colors_flags.index(element)]
            else:
                element.setStyleSheet("background-color: rgb(250, 0, 150)")
                filter_colors_flags.append(element)
'''