import requests
import shutil
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont, QResizeEvent, QImage
from modules.consts import APP_NAME, APP_STYLE, APP_TAB_NAMES, APP_FONT_NAME, APP_FONT_SIZE, SETTINGS_FOLDER_STRUCTURE
from modules.config import Config
from modules.database.database_functions import get_card_from_db, find_cards_in_db, get_card_from_db_to_add_cards
from modules.database.query import construct_query
from modules.database.collections import create_collection, get_all_collections_names_as_array, add_card_to_collection, get_card_from_collection
from modules.logging import console_log
import os

config = Config()
if config.get_value('COLLECTION', 'image_type') == 'png': image_extension = 'png'
else: image_extension = 'jpg'

app = QApplication([])
app_layout = QVBoxLayout()
tab_bar = QTabWidget()

filtered_cards = []
add_cards_found_cards = []

hierarchy = [
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
                            {'name': 'col_lyt_crd_lyt_grd_lyt_crd_lbl', 'type': 'QLabel'},
                            {'name': 'col_lyt_crd_lyt_grd_lyt_crd_iml', 'type': 'QLabel'},
                                {'name': 'col_lyt_crd_lyt_grd_lyt_crd_iml_pix', 'type': 'QPixMap'},
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

col_lyt_pre = QGroupBox()
col_lyt_pre_lyt = QVBoxLayout()
col_lyt_pre_lyt_iml = QLabel('Image')
col_lyt_pre_lyt_iml_pix = QPixmap(f'images/muldrotha_normal.jpg')
col_lyt_pre_lyt_iml.setScaledContents(True)
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
    ui.showMaximized()
    app.exec()

#AddWindow Class
class AddCollectionWindow(QWidget):
    def __init__(self, parent=None):
        super(AddCollectionWindow, self).__init__(parent)
        
        self.setWindowTitle('Add collection')
        self.setMinimumSize(300,100)
        self.setMaximumSize(300,100)

        layout = QVBoxLayout()
        self.label = QLabel("Enter name of your new collection:")
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

        app_layout.addWidget(tab_bar)
        self.setLayout(app_layout)
        
        self.app_font = QFont(APP_FONT_NAME, APP_FONT_SIZE)
        self.setFont(self.app_font)
        self.setWindowTitle(APP_NAME)
        QApplication.setStyle(APP_STYLE)

    def resizeEvent(self, event) -> None:
        update_sizes_of_collection_tab()
        QWidget.resizeEvent(self, event)

#Global functions
def download_image_if_not_downloaded(id):
    file_name = f"{SETTINGS_FOLDER_STRUCTURE['cards']}/{id}.{image_extension}"

    if not os.path.exists(file_name):
        card = get_card_from_db(database_connection, id)
        r = requests.get(card['image_uris'][config.get_value('COLLECTION', 'image_type')], stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(file_name,'wb') as f:
                shutil.copyfileobj(r.raw, f)
def return_grid_cards_groupboxes_as_list():
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
    tab_bar.addTab(col, APP_TAB_NAMES['collection'])
    col.setLayout(col_lyt)
    col_lyt.addWidget(col_lyt_crd)
    col_lyt_crd.setLayout(col_lyt_crd_lyt)
    col_lyt_crd_lyt.addWidget(col_lyt_crd_lyt_flt)
    col_lyt_crd_lyt_flt.setLayout(col_lyt_crd_lyt_flt_lyt)
    [col_lyt_crd_lyt_flt_lyt.addWidget(element) for element in col_lyt_crd_lyt_flt_lyt_clr]
    col_lyt_crd_lyt_flt_lyt.addWidget(col_lyt_crd_lyt_flt_lyt_and)
    col_lyt_crd_lyt_flt_lyt.addWidget(col_lyt_crd_lyt_flt_lyt_orr)
    [col_lyt_crd_lyt_flt_lyt.addWidget(element) for element in col_lyt_crd_lyt_flt_lyt_cmc]
    col_lyt_crd_lyt_flt_lyt.addWidget(col_lyt_crd_lyt_flt_lyt_slb)
    col_lyt_crd_lyt_flt_lyt.addWidget(col_lyt_crd_lyt_flt_lyt_sbx)
    col_lyt_crd_lyt_flt_lyt.addWidget(col_lyt_crd_lyt_flt_lyt_sbu)
    col_lyt_crd_lyt.addWidget(col_lyt_crd_lyt_tag)
    col_lyt_crd_lyt_tag.setLayout(col_lyt_crd_lyt_tag_lyt)
    col_lyt_crd_lyt.addWidget(col_lyt_crd_lyt_grd)
    col_lyt_crd_lyt_grd.setLayout(col_lyt_crd_lyt_grd_lyt)
    col_lyt.addWidget(col_lyt_pre)
    col_lyt_pre.setLayout(col_lyt_pre_lyt)
    col_lyt_pre_lyt.addWidget(col_lyt_pre_lyt_iml)
    col_lyt_pre_lyt_iml.setPixmap(col_lyt_pre_lyt_iml_pix)
    col_lyt_pre_lyt.addWidget(col_lyt_pre_lyt_inf)
    col_lyt_pre_lyt.addWidget(col_lyt_pre_lyt_des)
    col_lyt_pre_lyt_des.setWidget(col_lyt_pre_lyt_des_lbl)
    col_lyt_pre_lyt.addWidget(col_lyt_pre_lyt_tag)

    create_collection_tab_filters()
    create_collection_tab_grid()
    #
    create_collection_tab_preview()
    update_sizes_of_collection_tab()
#Collection -> Sizes
def update_sizes_of_collection_tab():
    col_lyt_pre.setMinimumWidth(300)
    col_lyt_pre.setMaximumWidth(450)

    col_lyt_crd_lyt_flt.setMinimumHeight(65)
    col_lyt_crd_lyt_flt.setMaximumHeight(65)
    col_lyt_crd_lyt_tag.setMinimumHeight(50)
    col_lyt_crd_lyt_tag.setMaximumHeight(50)
    
    icon_size = col_lyt_crd_lyt_flt.height()-27
    for element in col_lyt_crd_lyt_flt_lyt_clr: element.setMaximumSize(icon_size, icon_size)
    for element in col_lyt_crd_lyt_flt_lyt_cmc: element.setMaximumSize(icon_size, icon_size)

    grid_card_height = int(col_lyt_crd_lyt_grd.frameGeometry().height() / config.get_int('COLLECTION', 'grid_number_of_rows') - 20)
    for element in return_grid_cards_groupboxes_as_list():
        element.setMaximumSize(int(grid_card_height * 0.72), grid_card_height)

#Collection -> Filters
def create_collection_tab_filters():
    for element in col_lyt_crd_lyt_flt_lyt_clr:
        element.setScaledContents(True)
        element.setPixmap(QPixmap(f'{SETTINGS_FOLDER_STRUCTURE["symbols"]}/{element.text()}'))

    for element in col_lyt_crd_lyt_flt_lyt_cmc:
        element.setScaledContents(True)
        element.setPixmap(QPixmap(f'{SETTINGS_FOLDER_STRUCTURE["symbols"]}/{element.text()}'))

    col_lyt_crd_lyt_flt_lyt_sbu.clicked.connect(collection_filters_searchbox_pressed)
#Collection -> Filters -> Events
def collection_filters_searchbox_pressed():
    if col_lyt_crd_lyt_flt_lyt_sbx.text():
        filtered_cards = find_cards_in_db(database_connection, construct_query(col_lyt_crd_lyt_flt_lyt_sbx.text()))
        for id in filtered_cards:
            download_image_if_not_downloaded(id)

        for i, element in enumerate(return_grid_cards_groupboxes_as_list()):
            if i == len(filtered_cards): break
            file_name = f"{SETTINGS_FOLDER_STRUCTURE['cards']}/{filtered_cards[i]}.{image_extension}"

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

    for i in range(n_rows):
        for j in range(cards_per_row):
            gbx = QGroupBox()
            gbx_lyt = QVBoxLayout()
            iml = QLabel()
            iml.setScaledContents(True)
            imp = QPixmap(f'images/muldrotha_normal.jpg')
            iml.setPixmap(imp)
            gbx_lyt.addWidget(QLabel())
            gbx_lyt.addWidget(iml)
            gbx.setLayout(gbx_lyt)
            col_lyt_crd_lyt_grd_lyt.addWidget(gbx, i, j)

#Collection -> Preview
def create_collection_tab_preview():
    col_lyt_pre_lyt_inf.setWordWrap(True)

#Decks
def create_decks_tab():
    pass

#Add cards
def create_add_cards_tab():
    tab_bar.addTab(add, APP_TAB_NAMES['add_cards'])
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
    add_cards_found_cards = find_cards_in_db(database_connection, construct_query(f'name:"{add_lyt_gbx_lyt_src_lyt_sbx.text()}"'))
    
    add_lyt_gbx_lyt_lst.clear()

    unsorted_list = []

    for element in add_cards_found_cards:
        card = get_card_from_db_to_add_cards(database_connection, element)
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
    file_name = f"{SETTINGS_FOLDER_STRUCTURE['cards']}/{add_cards_found_cards[current_index]}.{image_extension}"
    add_lyt_gbx_lyt_res_lyt_iml.setPixmap(QPixmap(file_name))
    add_cards_update_card_count()
def add_cards_add_regular():
    add_card_to_collection(
        collections_connection,
        config.get_value('COLLECTION', 'current_collection'), 
        add_cards_found_cards[add_lyt_gbx_lyt_lst.currentRow()],
        1,
        0,
        'add',
        add_cards_sorted_list[add_lyt_gbx_lyt_lst.currentRow()]['sort_key'])    
    add_cards_update_card_count()
def add_cards_add_foil():
    add_card_to_collection(
        collections_connection,
        config.get_value('COLLECTION', 'current_collection'), 
        add_cards_found_cards[add_lyt_gbx_lyt_lst.currentRow()],
        0,
        1,
        'add',
        add_cards_sorted_list[add_lyt_gbx_lyt_lst.currentRow()]['sort_key'])
    add_cards_update_card_count()
def add_cards_update_card_count():
    selected_card = get_card_from_collection(collections_connection, config.get_value('COLLECTION', 'current_collection'), add_cards_found_cards[add_lyt_gbx_lyt_lst.currentRow()])

    add_lyt_gbx_lyt_res_lyt_lbl.setText(f"You currently have {selected_card['regular']} regulars and {selected_card['foil']} foils in collection")

#Wishlist
def create_wishlist_tab():
    pass

#Import/export
def create_import_export_tab():
    pass

#Settings
def create_settings_tab():
    tab_bar.addTab(stt, APP_TAB_NAMES['settings'])
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