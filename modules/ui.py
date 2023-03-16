from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QMouseEvent, QPixmap
from PyQt6.QtWidgets import QApplication, QButtonGroup, QCheckBox, QComboBox, QDoubleSpinBox, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPlainTextEdit, QProgressBar, QPushButton, QRadioButton, QScrollArea, QTabWidget, QVBoxLayout, QWidget
from PyQt6.QtSvgWidgets import QSvgWidget
from modules.globals import config, TEMPLATE_PATTERNS, UI_PATTERN_LEGEND

app = QApplication([])
app_lyt = QVBoxLayout()
tab_bar = QTabWidget()

collection_last_width = 0
collection_last_height = 0

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
                        {'name': 'col_lyt_crd_lyt_flt_lyt_slb', 'type': 'QLabel'},
                        {'name': 'col_lyt_crd_lyt_flt_lyt_sbx', 'type': 'QLineEdit'},
                        {'name': 'col_lyt_crd_lyt_flt_lyt_sbu', 'type': 'QPushButton'},
                        {'name': 'col_lyt_crd_lyt_flt_lyt_sbc', 'type': 'QPushButton'},
                {'name': 'col_lyt_crd_lyt_tag', 'type': 'QGroupBox'},
                    {'name': 'col_lyt_crd_lyt_tag_lyt', 'type': 'QHBoxLayout'},
                        {'name': 'col_lyt_crd_lyt_tag_lyt_pag', 'type': 'QDoubleSpinBox'},
                        {'name': 'col_lyt_crd_lyt_tag_lyt_inf', 'type': 'QLabel'},
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
                {'name': 'col_lyt_pre_lyt_des', 'type': 'QPlainTextEdit'},
                {'name': 'col_lyt_pre_lyt_tag', 'type': 'QLabel'},

{'name': 'pro', 'type': 'QWidget'},
    {'name': 'pro_lyt', 'type': 'QHBoxLayout'},
        {'name': 'pro_lyt_scr', 'type': 'QScrollArea'},
            {'name': 'pro_lyt_scr_grd', 'type': 'QWidget'},
                {'name': 'pro_lyt_scr_grd_lyt', 'type': 'QGridLayout(pro_lyt_scr_grd)'},
                    {'name': 'pro_lyt_scr_grd_lyt_col', 'type': 'QButtonGroup'},
                    {'name': 'pro_lyt_scr_grd_lyt_dat', 'type': 'QButtonGroup'},
        {'name': 'pro_lyt_inf', 'type': 'QGroupBox'},
            {'name': 'pro_lyt_inf_lyt', 'type': 'QVBoxLayout'},
                {'name': 'pro_lyt_inf_lyt_typ', 'type': 'QButtonGroup'},
                {'name': 'pro_lyt_inf_lyt_shw', 'type': 'QButtonGroup'},

{'name': 'dck', 'type': 'QWidget'},

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

{'name': 'wsh', 'type': 'QWidget'},

{'name': 'imp', 'type': 'QWidget'},
    {'name': 'imp_lyt', 'type': 'QVBoxLayout'},
        {'name': 'imp_lyt_gbx', 'type': 'QGroupBox'},
            {'name': 'imp_lyt_gbx_lyt', 'type': 'QHBoxLayout'},
                {'name': 'imp_lyt_gbx_lyt_inp', 'type': 'QGroupBox'},
                    {'name': 'imp_lyt_gbx_lyt_inp_lyt', 'type': 'QVBoxLayout'},
                        {'name': 'imp_lyt_gbx_lyt_inp_lyt_lbl', 'type': 'QLabel'},
                        {'name': 'imp_lyt_gbx_lyt_inp_lyt_lin', 'type': 'QPlainTextEdit'},
                {'name': 'imp_lyt_gbx_lyt_par', 'type': 'QGroupBox'},
                    {'name': 'imp_lyt_gbx_lyt_par_lyt', 'type': 'QVBoxLayout'},
                        {'name': 'imp_lyt_gbx_lyt_par_lyt_lbl', 'type': 'QLabel'},
                        {'name': 'imp_lyt_gbx_lyt_par_lyt_cmb', 'type': 'QComboBox'},
                        {'name': 'imp_lyt_gbx_lyt_par_lyt_lin', 'type': 'QLineEdit'},
                        {'name': 'imp_lyt_gbx_lyt_par_lyt_chk', 'type': 'QCheckBox'},
                        {'name': 'imp_lyt_gbx_lyt_par_lyt_leg', 'type': 'QLabel'},
                        {'name': 'imp_lyt_gbx_lyt_par_lyt_imp', 'type': 'QPushButton'},
                        {'name': 'imp_lyt_gbx_lyt_par_lyt_exp', 'type': 'QPushButton'},
                        {'name': 'imp_lyt_gbx_lyt_par_lyt_inl', 'type': 'QLabel'},
                        {'name': 'imp_lyt_gbx_lyt_par_lyt_inp', 'type': 'QPlainTextEdit'},
                {'name': 'imp_lyt_gbx_lyt_res', 'type': 'QGroupBox'},
                    {'name': 'imp_lyt_gbx_lyt_res_lyt', 'type': 'QVBoxLayout'},
                        {'name': 'imp_lyt_gbx_lyt_res_lyt_lbl', 'type': 'QLabel'},
                        {'name': 'imp_lyt_gbx_lyt_res_lyt_scr', 'type': 'QPlainTextEdit'},

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
col_lyt_crd_lyt_flt_lyt_slb = QLabel('Search cards:')
col_lyt_crd_lyt_flt_lyt_sbx = QLineEdit('')
col_lyt_crd_lyt_flt_lyt_sbu = QPushButton('Search')
col_lyt_crd_lyt_flt_lyt_sbc = QPushButton('Clear')
col_lyt_crd_lyt_tag = QGroupBox()
col_lyt_crd_lyt_tag_lyt = QHBoxLayout()
col_lyt_crd_lyt_tag_lyt_pag = QDoubleSpinBox()
col_lyt_crd_lyt_tag_lyt_inf = QLabel('Found 0 cards and there are 0 pages.')
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
col_lyt_pre_lyt_inf = QLabel('Python Magic Collection 0.1.0')
col_lyt_pre_lyt_des = QPlainTextEdit('New in this version:\n\t-TODO')
col_lyt_pre_lyt_tag = QLabel()

pro = QWidget()
pro_lyt = QHBoxLayout()
pro_lyt_scr = QScrollArea()
pro_lyt_scr_grd = QWidget()
pro_lyt_scr_grd_lyt = QGridLayout(pro_lyt_scr_grd)
pro_lyt_scr_grd_lyt_col = QButtonGroup()
pro_lyt_scr_grd_lyt_dat = QButtonGroup()
pro_lyt_inf = QGroupBox()
pro_lyt_inf_lyt = QVBoxLayout()
pro_lyt_inf_lyt_typ = QButtonGroup()
pro_lyt_inf_lyt_shw = QButtonGroup()

dck = QWidget()

add = QWidget()
add_lyt = QHBoxLayout()
add_lyt_gbx = QGroupBox()
add_lyt_gbx_lyt = QHBoxLayout()
add_lyt_gbx_lyt_src = QGroupBox()
add_lyt_gbx_lyt_src_lyt = QVBoxLayout()
add_lyt_gbx_lyt_src_lyt_lbl = QLabel('Type name of searched card:')
add_lyt_gbx_lyt_src_lyt_sbx = QLineEdit('')
add_lyt_gbx_lyt_src_lyt_but = QPushButton('Search')
add_lyt_gbx_lyt_lst = QListWidget()
add_lyt_gbx_lyt_res = QGroupBox()
add_lyt_gbx_lyt_res_lyt = QVBoxLayout()
add_lyt_gbx_lyt_res_lyt_lbl = QLabel()
add_lyt_gbx_lyt_res_lyt_iml = QLabel()
add_lyt_gbx_lyt_res_lyt_iml_pix = QPixmap()
add_lyt_gbx_lyt_res_lyt_adr = QPushButton('Add 1 regular')
add_lyt_gbx_lyt_res_lyt_adf = QPushButton('Add 1 foil')

wsh = QWidget()

imp = QWidget()
imp_lyt = QVBoxLayout()
imp_lyt_gbx = QGroupBox()
imp_lyt_gbx_lyt = QHBoxLayout()
imp_lyt_gbx_lyt_inp = QGroupBox()
imp_lyt_gbx_lyt_inp_lyt = QVBoxLayout()
imp_lyt_gbx_lyt_inp_lyt_lbl = QLabel('Paste your imported list here:')
imp_lyt_gbx_lyt_inp_lyt_lin = QPlainTextEdit()
imp_lyt_gbx_lyt_par = QGroupBox()
imp_lyt_gbx_lyt_par_lyt = QVBoxLayout()
imp_lyt_gbx_lyt_par_lyt_lbl = QLabel('Choose your list pattern:')
imp_lyt_gbx_lyt_par_lyt_cmb = QComboBox()
imp_lyt_gbx_lyt_par_lyt_lin = QLineEdit()
imp_lyt_gbx_lyt_par_lyt_chk = QCheckBox('Does imported list contain header?')
imp_lyt_gbx_lyt_par_lyt_leg = QLabel(UI_PATTERN_LEGEND)
imp_lyt_gbx_lyt_par_lyt_imp = QPushButton('Import cards as new collection')
imp_lyt_gbx_lyt_par_lyt_exp = QPushButton('Export cards from current collection')
imp_lyt_gbx_lyt_par_lyt_inl = QLabel('Import errors:')
imp_lyt_gbx_lyt_par_lyt_inp = QPlainTextEdit()
imp_lyt_gbx_lyt_res = QGroupBox()
imp_lyt_gbx_lyt_res_lyt = QVBoxLayout()
imp_lyt_gbx_lyt_res_lyt_lbl = QLabel('Import status:')
imp_lyt_gbx_lyt_res_lyt_scr = QPlainTextEdit()

stt = QWidget()
stt_lyt = QVBoxLayout()

def create_user_interface(db_connection, cl_connection, dk_connection):
    from modules.database.collections import get_cards_from_collection
    from modules.database.functions import get_cards_ids_prices_sets_flip_list
    from modules.logging import console_log
    global database_connection, collections_connection, decks_connection, database_cards, collection_cards, collection_filtered_cards, add_cards_found_cards
    console_log('info', 'Creating UI')

    database_connection = db_connection
    collections_connection = cl_connection
    decks_connection = dk_connection
    
    database_cards = get_cards_ids_prices_sets_flip_list(database_connection, config.get('COLLECTION', 'price_source'))
    collection_cards = get_cards_from_collection(collections_connection, config.get('COLLECTION', 'current_collection'))
    collection_filtered_cards = []

    tab_bar.currentChanged.connect(tab_changed)
    
    ui = UI()
    ui.showMaximized()
    #ui.show()
    app.exec()
#Main -> Events
def tab_changed(event):
    #0 - collection, 1 - progression, 2 - decks, 3 - add cards, 4 - wishlist, 5 - import/export, 6 - settings
    if event == 0 and config.get_boolean('FLAG', 'collection_needs_refreshing'):
        create_collection_tab_grid()
        config.set('FLAG', 'collection_needs_refreshing', 'false')
        
    elif event == 1 and config.get_boolean('FLAG', 'progression_needs_refreshing'):
        progression_refresh()
        config.set('FLAG', 'progression_needs_refreshing', 'false')
        
    elif event == 2 and config.get_boolean('FLAG', 'decks_needs_refreshing'):
        config.set('FLAG', 'decks_needs_refreshing', 'false')
        
    elif event == 4 and config.get_boolean('FLAG', 'wishlist_needs_refreshing'):
        config.set('FLAG', 'wishlist_needs_refreshing', 'false')

#UI Class and its Events
class UI(QWidget):
    def __init__(self, parent=None) -> None:
        from modules.ui_functions import refresh_collection_names_in_corner
        
        super(UI, self).__init__(parent)

        create_corner_widget()
        create_collection_tab()
        create_progression_tab()
        create_decks_tab()
        create_add_cards_tab()
        create_wishlist_tab()
        create_import_export_tab()
        create_settings_tab()

        refresh_collection_names_in_corner(collections_connection, cor_lyt_cmb, config.get('COLLECTION', 'current_collection'))

        app_lyt.addWidget(tab_bar)
        self.setLayout(app_lyt)
        
        self.app_font = QFont(config.get('APP', 'font'), config.get_int('APP', 'font_size'))
        self.setFont(self.app_font)
        self.setWindowTitle(f"{config.get('APP', 'name')} - X:{self.x()}, Y:{self.y()}, W:{self.width()}, H:{self.height()}")
        QApplication.setStyle(config.get('APP', 'style'))

    def resizeEvent(self, event) -> None:
        self.setWindowTitle(f"{config.get('APP', 'name')} - X:{self.x()}, Y:{self.y()}, W:{self.width()}, H:{self.height()}")
        #update_sizes_of_cards_in_grid()
        create_collection_tab_grid()
        QWidget.resizeEvent(self, event)
        
    def keyPressEvent(self, event) -> None:
        #FIXME
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Enter:
            col_lyt_crd_lyt_flt_lyt_sbx.setFocus()
        event.accept()
        QWidget.keyPressEvent(self, event)

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
        from modules.database.collections import create_collection
        from modules.ui_functions import refresh_collection_names_in_corner
        
        create_collection(collections_connection, self.line_edit.text())
        refresh_collection_names_in_corner(collections_connection, cor_lyt_cmb)
        #Add window prompt - succesful or not
        self.close()

#Corner
def create_corner_widget():
    cor.setMinimumHeight(40)
    cor_lyt_cmb.setMinimumWidth(200)
    tab_bar.setCornerWidget(cor)
    cor.setLayout(cor_lyt)
    cor_lyt.addWidget(cor_lyt_btn)
    cor_lyt_btn.clicked.connect(add_collection_button_pressed)
    cor_lyt.addWidget(cor_lyt_cmb)
    cor_lyt_cmb.currentIndexChanged.connect(current_collection_index_changed)
    cor_lyt.addWidget(cor_lyt_chk)
    cor_lyt_chk.setChecked(True) if config.get_boolean('COLLECTION', 'show_database') else cor_lyt_chk.setChecked(False)
    cor_lyt_chk.clicked.connect(show_database_checked)
#Corner -> Events
add_collection_window = AddCollectionWindow()
def add_collection_button_pressed():
    add_collection_window.show()
    add_collection_window.line_edit.setText('')
def current_collection_index_changed():
    from modules.database.collections import format_collection_name, get_cards_from_collection
    from modules.ui_functions import refresh_collection_names_in_corner
    
    if not config.get_boolean('FLAG', 'corner_refreshing'):
        global collection_last_width, collection_last_height, collection_cards, collection_filtered_cards
        
        collection_name = format_collection_name(cor_lyt_cmb.currentText())
        config.set('COLLECTION', 'current_collection', collection_name)
        refresh_collection_names_in_corner(collections_connection, cor_lyt_cmb, collection_name)
        
        col_lyt_crd_lyt_flt_lyt_sbx.setText('')
        
        collection_cards = get_cards_from_collection(collections_connection, config.get('COLLECTION', 'current_collection'))
        collection_filtered_cards = []
        collection_last_width = -1
        collection_last_height = -1
        
        if tab_bar.currentIndex() == 0: create_collection_tab_grid()
        else: config.set('FLAG', 'collection_needs_refreshing', 'true')
        
        if tab_bar.currentIndex() == 1: progression_refresh()
        else: config.set('FLAG', 'progression_needs_refreshing', 'true')
def show_database_checked():
    global collection_last_width, collection_last_height
    config.set('COLLECTION', 'show_database', 'true') if cor_lyt_chk.isChecked() else config.set('COLLECTION', 'show_database', 'false')
    collection_last_width = -1
    collection_last_height = -1
    create_collection_tab_grid()

#Collection
def create_collection_tab():
    tab_bar.addTab(col, config.get('APP', 'collection'))
    col.setLayout(col_lyt)
    col_lyt.addWidget(col_lyt_crd)
    col_lyt_crd.setLayout(col_lyt_crd_lyt)
    col_lyt_crd_lyt.addWidget(col_lyt_crd_lyt_flt)
    col_lyt_crd_lyt_flt.setLayout(col_lyt_crd_lyt_flt_lyt)
    [col_lyt_crd_lyt_flt_lyt.addWidget(element) for element in col_lyt_crd_lyt_flt_lyt_clr]
    col_lyt_crd_lyt_flt_lyt.addWidget(col_lyt_crd_lyt_flt_lyt_and)
    col_lyt_crd_lyt_flt_lyt.addWidget(col_lyt_crd_lyt_flt_lyt_orr)
    col_lyt_crd_lyt_flt_lyt_orr.setChecked(True)
    col_lyt_crd_lyt_flt_lyt.addWidget(col_lyt_crd_lyt_flt_lyt_slb)
    col_lyt_crd_lyt_flt_lyt.addWidget(col_lyt_crd_lyt_flt_lyt_sbx)
    col_lyt_crd_lyt_flt_lyt_sbx.editingFinished.connect(searchbox_editing_finished)
    col_lyt_crd_lyt_flt_lyt.addWidget(col_lyt_crd_lyt_flt_lyt_sbu)
    col_lyt_crd_lyt_flt_lyt_sbu.clicked.connect(collection_filters_searchbox_button_pressed)
    col_lyt_crd_lyt_flt_lyt.addWidget(col_lyt_crd_lyt_flt_lyt_sbc)
    col_lyt_crd_lyt_flt_lyt_sbc.clicked.connect(searchbox_clear_button_pressed)
    for element in col_lyt_crd_lyt_flt_lyt_clr:
        element.setScaledContents(True)
        element.setPixmap(QPixmap(f"{config.get('FOLDER', 'symbols')}/{element.text()}"))
    col_lyt_crd_lyt.addWidget(col_lyt_crd_lyt_tag)
    col_lyt_crd_lyt_tag.setLayout(col_lyt_crd_lyt_tag_lyt)
    col_lyt_crd_lyt_tag_lyt.addWidget(col_lyt_crd_lyt_tag_lyt_pag)
    col_lyt_crd_lyt_tag_lyt_pag.setValue(config.get_int('COLLECTION', 'current_page'))
    if col_lyt_crd_lyt_tag_lyt_pag.value() == 0: col_lyt_crd_lyt_tag_lyt_pag.setValue(1)
    col_lyt_crd_lyt_tag_lyt_pag.setWrapping(False)
    col_lyt_crd_lyt_tag_lyt_pag.setDecimals(0)
    col_lyt_crd_lyt_tag_lyt_pag.setMinimum(1)
    col_lyt_crd_lyt_tag_lyt_pag.setMaximum(99999)
    col_lyt_crd_lyt_tag_lyt_pag.valueChanged.connect(page_control_value_changed)
    col_lyt_crd_lyt_tag_lyt.addWidget(col_lyt_crd_lyt_tag_lyt_inf)
    col_lyt_crd_lyt.addWidget(col_lyt_crd_lyt_grd)
    col_lyt_crd_lyt_grd.setLayout(col_lyt_crd_lyt_grd_lyt)
    col_lyt.addWidget(col_lyt_pre)
    col_lyt_pre.setLayout(col_lyt_pre_lyt)
    col_lyt_pre_lyt.addWidget(col_lyt_pre_lyt_iml)
    col_lyt_pre_lyt_iml.mousePressEvent = card_image_mouse_pressed
    col_lyt_pre_lyt_inf.setWordWrap(True)
    col_lyt_pre_lyt.addWidget(col_lyt_pre_lyt_inf)
    col_lyt_pre_lyt.addWidget(col_lyt_pre_lyt_des)
    col_lyt_pre_lyt_des.setReadOnly(True)
    col_lyt_pre_lyt.addWidget(col_lyt_pre_lyt_tag)
    col_lyt_pre.setMinimumWidth(458)
    col_lyt_pre.setMaximumWidth(458)
    col_lyt_crd_lyt_flt.setMinimumHeight(65)
    col_lyt_crd_lyt_flt.setMaximumHeight(65)
    col_lyt_crd_lyt_flt_lyt_sbx.setMinimumWidth(125)
    col_lyt_crd_lyt_tag.setMinimumHeight(50)
    col_lyt_crd_lyt_tag.setMaximumHeight(50)
    icon_size = col_lyt_crd_lyt_flt.height()-27 
    [element.setMaximumSize(icon_size, icon_size) for element in col_lyt_crd_lyt_flt_lyt_clr]
    
    if config.get('COLLECTION', 'current_filter'): col_lyt_crd_lyt_flt_lyt_sbx.setText(config.get('COLLECTION', 'current_filter'))
    collection_filters_searchbox_button_pressed()
#Collection -> Filters -> Events
def searchbox_editing_finished():
    collection_filters_searchbox_button_pressed()
def collection_filters_searchbox_button_pressed():
    from modules.database.functions import get_card_ids_list
    from modules.database.query import construct_query
    global collection_filtered_cards, collection_last_width, collection_last_height
    
    collection_filtered_cards = []
    
    if col_lyt_crd_lyt_flt_lyt_sbx.text():
        collection_filtered_cards = get_card_ids_list(database_connection, construct_query(col_lyt_crd_lyt_flt_lyt_sbx.text()))
        config.set('COLLECTION', 'current_filter', f"{col_lyt_crd_lyt_flt_lyt_sbx.text()}")
    else:
        config.set('COLLECTION', 'current_filter', '')
        
    col_lyt_crd_lyt_tag_lyt_pag.setMaximum(99999)
    col_lyt_crd_lyt_tag_lyt_pag.setValue(config.get_int('COLLECTION', 'current_page'))
    if len(collection_filtered_cards) > 0: col_lyt_crd_lyt_tag_lyt_pag.setValue(1)
    
    collection_last_width = -1
    collection_last_height = -1
    col_lyt_crd_lyt_tag_lyt_pag.setFocus()
    col_lyt_crd_lyt_tag_lyt_pag.selectAll()
    create_collection_tab_grid()
def searchbox_clear_button_pressed():
    global collection_filtered_cards, collection_last_width, collection_last_height
    col_lyt_crd_lyt_flt_lyt_sbx.clear()
    config.set('COLLECTION', 'current_filter', '')
    collection_filtered_cards = []
    collection_last_width = -1
    collection_last_height = -1
    col_lyt_crd_lyt_tag_lyt_pag.setMaximum(99999)
    col_lyt_crd_lyt_tag_lyt_pag.setValue(config.get_int('COLLECTION', 'current_page'))
    create_collection_tab_grid()
#Collection -> Tags -> Events
def page_control_value_changed():
    global collection_last_width, collection_last_height
    if col_lyt_crd_lyt_tag_lyt_pag.value() > 0:
        if len(collection_filtered_cards) > 0: config.set('COLLECTION', 'current_filtered_page', str(int(col_lyt_crd_lyt_tag_lyt_pag.value())))
        else: config.set('COLLECTION', 'current_page', str(int(col_lyt_crd_lyt_tag_lyt_pag.value())))
    else:
        if len(collection_filtered_cards) > 0: config.set('COLLECTION', 'current_filtered_page', '1')
        else: config.set('COLLECTION', 'current_page', '1')
    collection_last_width = -1
    collection_last_height = -1
    create_collection_tab_grid()
#Collection -> Grid
def create_collection_tab_grid():
    from modules.ui_functions import calculate_grid_sizes, create_card_image, create_card_extra_info, create_card_info, create_currency_string, create_price_string, delete_widgets_from_layout, download_card_images_for_current_page, prepare_list_of_cards_to_show, set_maximum_number_of_pages_and_update_info
    global collection_cards_on_grid, collection_filtered_cards, collection_last_width, collection_last_height

    grid_sizes = calculate_grid_sizes(col_lyt_crd_lyt_grd)

    if grid_sizes['spacing_horizontal'] < 15: grid_sizes['cards_in_row'] = grid_sizes['cards_in_row'] - 1
    if grid_sizes['spacing_vertical'] < 23: grid_sizes['cards_in_col'] = grid_sizes['cards_in_col'] - 1
    
    if collection_last_width != grid_sizes['cards_in_row'] or collection_last_height != grid_sizes['cards_in_col']:
        delete_widgets_from_layout(col_lyt_crd_lyt_grd_lyt)
        
        cards_to_display = prepare_list_of_cards_to_show(collection_filtered_cards, database_cards, collection_cards)
        collection_cards_on_grid = []
        
        if len(collection_filtered_cards) > 0: current_page = config.get_int('COLLECTION', 'current_filtered_page')
        else: current_page = config.get_int('COLLECTION', 'current_page')

        starting_index = (current_page - 1) * grid_sizes['cards_on_grid']
        ending_index = (current_page - 1) * grid_sizes['cards_on_grid'] + grid_sizes['cards_on_grid']
        if starting_index < 0: starting_index = 0
        if ending_index < 0: ending_index = 0

        set_maximum_number_of_pages_and_update_info(cards_to_display, grid_sizes['cards_on_grid'], col_lyt_crd_lyt_tag_lyt_pag, col_lyt_crd_lyt_tag_lyt_inf)
        download_card_images_for_current_page(database_connection, cards_to_display, starting_index, ending_index, config.get('COLLECTION', 'image_extension'))
        
        x, y = 1, 1
        for i in range(starting_index, ending_index):
            if i > len(cards_to_display) - 1:
                #TODO
                #Keep grid layout even when there's less element than intended for full page of cards
                break
            else:                
                #Card image
                card_image = QLabel()
                create_card_image(card_image, cards_to_display[i], config.get('COLLECTION', 'image_extension'), grid_sizes['card_width'], grid_sizes['card_height'])
                
                #Card info label
                price_string = create_price_string(cards_to_display[i], database_cards)
                currency_symbol = ''
                if price_string: currency_symbol = create_currency_string()
                
                card_info = QLabel()
                if cards_to_display[i] in collection_cards['id']: create_card_info(card_info, True, collection_cards, cards_to_display[i], price_string, currency_symbol)
                else: create_card_info(card_info, False, collection_cards, cards_to_display[i], price_string, currency_symbol)
                card_image.setObjectName(cards_to_display[i])
                card_image.mousePressEvent = card_image_mouse_pressed
                collection_cards_on_grid.append(card_image)
                
                #Card extra info
                card_extra_info = QLabel()
                create_card_extra_info(card_extra_info)
                
                #TODO
                #Fix style for card_info label
                groupbox = QGroupBox()
                layout = QVBoxLayout()
                stylesheet = f"""
                    font: {config.get('APP', 'font')};
                    font-size: {config.get('APP', 'font_size')}px;
                    """
                if config.get_boolean('COLLECTION', 'show_database'):
                    stylesheet += "background-color: LightGrey" if 'Not collected' in card_info.text() else "background-color: LightSteelBlue"
                else:
                    stylesheet += "background-color: LightGrey"
                groupbox.setStyleSheet(stylesheet)
                groupbox.setLayout(layout)
                layout.addWidget(card_info)
                layout.addWidget(card_image)
                                
                if database_cards['flip'][database_cards['id'].index(cards_to_display[i])]: card_extra_info.setText('Right click to flip card')
                
                layout.addWidget(card_extra_info)
                col_lyt_crd_lyt_grd_lyt.addWidget(groupbox, (y-1), (x-1))
                
                if x % grid_sizes['cards_in_row'] != 0: x = x + 1
                else:
                    x = 1
                    y = y + 1
    
    collection_last_width = grid_sizes['cards_in_row']
    collection_last_height = grid_sizes['cards_in_col']
#Collection -> Grid -> Events
def card_image_mouse_pressed(event: QMouseEvent):
    from os import path
    from modules.database.functions import get_card_from_db
    
    click_pos = event.globalPosition()
    chosen_card = None
    
    checking_area = [col_lyt_pre_lyt_iml, *collection_cards_on_grid]
    
    for element in checking_area:
        element_pos = element.mapToGlobal(QPoint(0, 0))
        element_size = element.geometry().size()
        
        if click_pos.x() > element_pos.x() and click_pos.x() < (element_pos.x() + element_size.width()) and click_pos.y() > element_pos.y() and click_pos.y() < element_pos.y() + element_size.height():
            is_face = True if element.objectName()[-2] == '-' else False
            face_number = int(element.objectName()[-1]) if is_face else 0
                
            card_id = element.objectName() if not is_face else element.objectName()[:-2]
            
            chosen_card = get_card_from_db(database_connection, card_id)
            
            if event.buttons() == Qt.MouseButton.LeftButton:
                update_preview(chosen_card, element.objectName())
            elif event.buttons() == Qt.MouseButton.RightButton:
                if chosen_card['card_faces']:
                    front_face_path = f"{config.get('FOLDER', 'cards')}/{card_id}.{config.get('COLLECTION', 'image_extension')}"
                    next_face_path = f"{config.get('FOLDER', 'cards')}/{card_id}-{face_number+1}.{config.get('COLLECTION', 'image_extension')}"
                    if path.exists(next_face_path):
                        pixmap = QPixmap(next_face_path)
                        pixmap_scaled = pixmap.scaled(element_size.width(), element_size.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        element.setPixmap(QPixmap(pixmap_scaled))
                        element.setObjectName(f"{card_id}-{face_number+1}")
                    else:
                        pixmap = QPixmap(front_face_path)
                        pixmap_scaled = pixmap.scaled(element_size.width(), element_size.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                        element.setPixmap(QPixmap(pixmap_scaled))
                        element.setObjectName(f"{card_id}")
            return
#Collection -> Preview -> Events
def update_preview(card: dict, object_name: str):
    from modules.database.collections import get_card_from_collection
    from modules.ui_functions import prepare_card_description
    from forex_python.converter import CurrencyRates, RatesNotAvailableError
    
    currency_rates = CurrencyRates()
    currency = config.get('COLLECTION', 'price_currency')
    try: exchange_rate = currency_rates.get_rate('USD', currency.upper())
    except RatesNotAvailableError: exchange_rate = 1
    
    card_in_col = get_card_from_collection(collections_connection, config.get('COLLECTION', 'current_collection'), card['id'])
    regular = card_in_col['regular']
    foil = card_in_col['foil']
    tags = card_in_col['tags']
    count_string = f"{regular + foil} card(s) in collection - regular: {regular} foil: {foil}"
    
    prices = [card['prices']['usd'], card['prices']['usd_foil'], card['prices']['usd_etched'], card['prices']['eur'], card['prices']['eur_foil'], card['prices']['tix']]
    source = config.get('COLLECTION', 'price_source')
    if currency not in ['usd', 'eur', 'tix']:
        if card['prices'][f"{source}"]:
            price = str(round(float(card['prices'][f"{source}"]) * exchange_rate, 2))
            if price.index('.') == len(price)-2: price += '0'
            prices.append(price)
        else: prices.append('N/A')
        
        if card['prices'][f"{source}_foil"]:
            price = str(round(float(card['prices'][f"{source}_foil"]) * exchange_rate, 2))
            if price.index('.') == len(price)-2: price += '0'
            prices.append(price)
        else: prices.append('N/A')
        
        if source == 'usd':
            price = str(round(float(card['prices'][f"{source}_etched"]) * exchange_rate, 2))
            if price.index('.') == len(price)-2: price += '0'
            prices.append(price)
        else: prices.append('N/A')
        
    for i in range(len(prices)):
        if prices[i] is None or prices[i] == 'N/A': prices[i] = 'N/A'
        elif i in range(0,3): prices[i] += '$'
        elif i in range(3,5): prices[i] += '€'
        elif i == 5: prices[i] += ' TIX'
        else: prices[i] += f' {currency.upper()}'
    
    prices_string = f"\nRegular: {prices[0]} / {prices[3]}"
    if len(prices) > 6: prices_string += f" / {prices[6]}"
    prices_string += f"\nFoil: {prices[1]} / {prices[4]}"
    if len(prices) > 6: prices_string += f" / {prices[7]}"
    prices_string += f"\nEtched: {prices[2]}"
    prices_string += f"\nTickets: {prices[5]}"
    
    col_lyt_pre_lyt_iml_pix = QPixmap(f"{config.get('FOLDER', 'cards')}/{object_name}.{config.get('COLLECTION', 'image_extension')}")
    pix_scaled = col_lyt_pre_lyt_iml_pix.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    col_lyt_pre_lyt_iml.setPixmap(pix_scaled)
    col_lyt_pre_lyt_iml.setObjectName(object_name)
    col_lyt_pre_lyt_inf.setText(f"{count_string}\n{prices_string}")
    description = prepare_card_description(card)
    col_lyt_pre_lyt_des.setPlainText(description)
    col_lyt_pre_lyt_tag.setText(f"Tags: {tags}")

#Progression
def create_progression_tab():
    tab_bar.addTab(pro, config.get('APP', 'progression'))
    pro.setLayout(pro_lyt)
    pro_lyt.addWidget(pro_lyt_scr)
    pro_lyt_scr.setWidget(pro_lyt_scr_grd)
    pro_lyt_scr.setWidgetResizable(True)
    pro_lyt.addWidget(pro_lyt_inf)
    pro_lyt_inf.setMinimumWidth(300)
    pro_lyt_inf.setMaximumWidth(300)
    pro_lyt_inf.setLayout(pro_lyt_inf_lyt)
    progression_create_widgets()
    progression_refresh()
#Progression -> Events
def progression_create_widgets():
    pro_lyt_inf_lyt_typ.setExclusive(False)
    pro_lyt_inf_lyt_typ.buttonClicked.connect(type_checked)
    pro_lyt_inf_lyt.addWidget(QLabel('Set types to show:'))
    
    for i, type in enumerate(config.config_parser['PROGRESSION_TYPES']):
        type_checkbox = QCheckBox(type.title().replace('_', ' '))
        pro_lyt_inf_lyt_typ.addButton(type_checkbox, i)
        if config.get_boolean('PROGRESSION_TYPES', type): type_checkbox.setChecked(True)
        else: type_checkbox.setChecked(False)
        pro_lyt_inf_lyt.addWidget(type_checkbox)
        
    pro_lyt_inf_lyt_shw.setExclusive(False)
    pro_lyt_inf_lyt_typ.buttonClicked.connect(type_checked)
    pro_lyt_inf_lyt.addWidget(QLabel('Set showing rules:'))
    
    for i, show in enumerate(config.config_parser['PROGRESSION_SHOW']):
        show_checkbox = QCheckBox(f"Don't show {show} sets")
        pro_lyt_inf_lyt_shw.addButton(show_checkbox, i)
        if config.get_boolean('PROGRESSION_SHOW', show): show_checkbox.setChecked(True)
        else: show_checkbox.setChecked(False)
        pro_lyt_inf_lyt.addWidget(show_checkbox)
        
    pro_lyt_inf_lyt_shw.buttonClicked.connect(show_checked)
    
    pro_lyt_inf_lyt.addWidget(QPlainTextEdit(f"Statistics:"))
def progression_refresh():
    from os import path
    from modules.ui_functions import create_currency_string, delete_widgets_from_layout, find_all_sets_in_db
    global progression_set_abbreviations
    
    delete_widgets_from_layout(pro_lyt_scr_grd_lyt)
    
    progression_sets = find_all_sets_in_db(database_connection)
    [progression_sets[_set].append(0) for _set in progression_sets]
    [progression_sets[_set].append(0) for _set in progression_sets]
    progression_sets_in_collection = []
    progression_value = []
    progression_set_abbreviations = []
    for i, id in enumerate(database_cards['id']):
        if id in collection_cards['id']:
            progression_sets_in_collection.append(database_cards['set'][i])
            index = collection_cards['id'].index(id)
            value = 0
            if database_cards['prices_regular'][i]: value += float(database_cards['prices_regular'][i]) * collection_cards['regular'][index]
            if database_cards['prices_foil'][i]: value += float(database_cards['prices_foil'][i]) * collection_cards['foil'][index]
            progression_value.append(value)
        if database_cards['prices_regular'][i]:
            progression_sets[database_cards['set'][i]][5] += float(database_cards['prices_regular'][i])
    
    for i, _set in enumerate(progression_sets_in_collection): progression_sets[_set][4] += progression_value[i]
    for _set in progression_sets:
        progression_sets[_set][4] = round(progression_sets[_set][4], 2)
        progression_sets[_set][5] = round(progression_sets[_set][5], 2)
    
    fixed_width = 240
    groupbox_width = 265
    color_scale = ['c3d2c3', 'bbd2bb', 'b3d2b3', 'abd2ab', 'a3d1a3', '9bd19b', '93d193', '8bd08b', '82d082', '7ad07a', '72cf72', '6acf6a', '62cf62', '5ace5a', '52ce52', '4ace4a', '42ce42', '3acd3a', '32cd32']
    
    i, j = 0, 0
    for _set in progression_sets:
        if config.get_boolean('PROGRESSION_TYPES', f"{progression_sets[_set][1]}"):
            if config.get_boolean('PROGRESSION_SHOW', 'completed'):
                if progression_sets_in_collection.count(_set) / progression_sets[_set][3] >= 1: continue
            if config.get_boolean('PROGRESSION_SHOW', 'partial'):
                if progression_sets_in_collection.count(_set) / progression_sets[_set][3] < 1 and progression_sets_in_collection.count(_set) != 0: continue
            if config.get_boolean('PROGRESSION_SHOW', 'empty'):
                if progression_sets_in_collection.count(_set) <= 0: continue
        
            if progression_sets_in_collection.count(_set) == 0: groupbox_stylesheet = f"background-color: #D3D3D3"
            else: groupbox_stylesheet = f"background-color: #{color_scale[0]}"
            
            for index in range(len(color_scale)):
                percentage = (index+1)/(len(color_scale)-1)
                current_value = progression_sets_in_collection.count(_set) / progression_sets[_set][3]
                if current_value > percentage:
                    groupbox_stylesheet = f"background-color: #{color_scale[index]}"
            
            groupbox = QGroupBox()
            groupbox.setStyleSheet(groupbox_stylesheet)
            layout = QVBoxLayout()
            groupbox.setLayout(layout)
            
            name = QLabel(f"{progression_sets[_set][0]} [{_set.upper()}]")
            name.setWordWrap(True)
            name.setFixedHeight(60)
            name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(name)
            
            image = QSvgWidget(f"{config.get('FOLDER', 'sets')}/dpa.svg")
            if path.isfile(f"{config.get('FOLDER', 'sets')}/{_set}.svg"): image = QSvgWidget(f"{config.get('FOLDER', 'sets')}/{_set}.svg")
            image.setFixedSize(150, 150)
            image.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
            layout.addWidget(image, alignment=Qt.AlignmentFlag.AlignCenter)        
            
            progress_bar = QProgressBar()
            value = progression_sets_in_collection.count(_set)
            maximum = progression_sets[_set][3]
            division = round(value/maximum*100)
            if division == 0 and value > 0: division = 1 
            progress_bar.setMaximum(100)
            progress_bar.setTextVisible(True)
            progress_bar.setValue(division)
            progress_bar.setFixedWidth(fixed_width)
            layout.addWidget(progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)
            
            progress_label = QLabel(f"{value} / {maximum}")
            layout.addWidget(progress_label, alignment=Qt.AlignmentFlag.AlignCenter)
            
            value = QLabel(f"Current value of set: {round(progression_sets[_set][4], 2)}{create_currency_string()}")
            layout.addWidget(value, alignment=Qt.AlignmentFlag.AlignCenter)
            
            price_1 = QLabel(f"Price of whole regular set x1: {round(progression_sets[_set][5], 2)}{create_currency_string()}")
            layout.addWidget(price_1, alignment=Qt.AlignmentFlag.AlignCenter)
            
            show_set_col = QPushButton('Show set in collection')
            show_set_col.setFixedWidth(fixed_width)
            layout.addWidget(show_set_col, alignment=Qt.AlignmentFlag.AlignCenter)
            
            show_set_db = QPushButton('Show set in database')
            show_set_db.setFixedWidth(fixed_width)
            layout.addWidget(show_set_db, alignment=Qt.AlignmentFlag.AlignCenter)
            
            groupbox.setFixedWidth(groupbox_width)
            pro_lyt_scr_grd_lyt.addWidget(groupbox, i, j)
            
            pro_lyt_scr_grd_lyt_col.addButton(show_set_col, i * 8 + j)
            pro_lyt_scr_grd_lyt_dat.addButton(show_set_db, i * 8 + j)
            progression_set_abbreviations.append(_set)
            
            j += 1
            if j % 8 == 0:
                j = 0
                i += 1
    
    pro_lyt_scr_grd_lyt_col.buttonClicked.connect(collection_search)
    pro_lyt_scr_grd_lyt_dat.buttonClicked.connect(database_search)
def type_checked(object):
    button_pressed = f"{pro_lyt_inf_lyt_typ.buttons()[pro_lyt_inf_lyt_typ.id(object)].text().lower().replace(' ', '_')}"
    button_value = f"{str(pro_lyt_inf_lyt_typ.buttons()[pro_lyt_inf_lyt_typ.id(object)].isChecked()).lower()}"
    config.set('PROGRESSION_TYPES', button_pressed, button_value)
    progression_refresh()
def show_checked(object):
    button_pressed = f"{pro_lyt_inf_lyt_shw.buttons()[pro_lyt_inf_lyt_shw.id(object)].text()}"
    button_value = f"{str(pro_lyt_inf_lyt_shw.buttons()[pro_lyt_inf_lyt_shw.id(object)].isChecked()).lower()}"
    buttons = ['completed', 'partial', 'empty']
    [config.set('PROGRESSION_SHOW', element, button_value) for element in buttons if element in button_pressed]
    progression_refresh()
def collection_search(object):
    cor_lyt_chk.setChecked(False)
    col_lyt_crd_lyt_flt_lyt_sbx.setText(f"s:{progression_set_abbreviations[pro_lyt_scr_grd_lyt_col.id(object)]}")
    show_database_checked()
    collection_filters_searchbox_button_pressed()
    tab_bar.setCurrentIndex(0)
def database_search(object):
    cor_lyt_chk.setChecked(True)
    col_lyt_crd_lyt_flt_lyt_sbx.setText(f"s:{progression_set_abbreviations[pro_lyt_scr_grd_lyt_dat.id(object)]}")
    show_database_checked()
    collection_filters_searchbox_button_pressed()
    tab_bar.setCurrentIndex(0)

#Decks
def create_decks_tab():
    tab_bar.addTab(dck, config.get('APP', 'decks'))

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
    add_lyt_gbx_lyt_src_lyt_sbx.editingFinished.connect(add_cards_search_button_pressed)
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
    add_lyt_gbx_lyt_res_lyt_adr.clicked.connect(add_regular_button_pressed)
    add_lyt_gbx_lyt_res_lyt.addWidget(add_lyt_gbx_lyt_res_lyt_adf)
    add_lyt_gbx_lyt_res_lyt_adf.clicked.connect(add_foil_button_pressed)

    cards_height = 680
    add_lyt_gbx_lyt_res.setMinimumWidth(int(cards_height * 0.72))
    add_lyt_gbx_lyt_res_lyt_iml.setMinimumSize(int(cards_height * 0.72), cards_height)
    add_lyt_gbx_lyt_res_lyt_iml.setMaximumSize(int(cards_height * 0.72), cards_height)
#Add cards -> Search -> Events
def add_cards_search_button_pressed():
    from modules.database.functions import get_card_from_db, get_card_ids_list
    from modules.database.query import construct_query
    global add_cards_found_cards, add_cards_sorted_list
    add_cards_found_cards = get_card_ids_list(database_connection, construct_query(f'name:"{add_lyt_gbx_lyt_src_lyt_sbx.text()}"'))
    
    add_lyt_gbx_lyt_lst.clear()

    unsorted_list = []

    for element in add_cards_found_cards:
        card = get_card_from_db(database_connection, element)
        unsorted_list.append({
            'id': card['id'],
            'name': card['name'],
            'collector_number': card['collector_number'],
            'released_at': card['released_at'],
            'display': f"{card['name']} ({card['collector_number']}) [{card['set_name']}] - {card['released_at']}"
            })

    add_cards_sorted_list = sorted(unsorted_list, key=lambda d: (d['released_at'], d['name'], d['collector_number']))
    add_cards_found_cards = list(map(lambda d: d['id'], add_cards_sorted_list))

    add_lyt_gbx_lyt_lst.addItems(list(map(lambda d: d['display'], add_cards_sorted_list)))
    add_lyt_gbx_lyt_lst.setFocus()
    add_lyt_gbx_lyt_lst.setCurrentRow(add_lyt_gbx_lyt_lst.count()-1)
#Add cards -> List -> Events
def add_cards_list_selection_changed():
    from modules.ui_functions import download_image_if_not_downloaded, update_card_count_in_add_cards
    
    current_index = add_lyt_gbx_lyt_lst.currentRow() if add_lyt_gbx_lyt_lst.currentRow() <= len(add_cards_found_cards)-1 else len(add_cards_found_cards)-1
    download_image_if_not_downloaded(database_connection, add_cards_found_cards[current_index], config.get('COLLECTION', 'image_extension'))
    file_name = f"{config.get('FOLDER', 'cards')}/{add_cards_found_cards[current_index]}.{config.get('COLLECTION', 'image_extension')}"
    pix = QPixmap(file_name)
    pix_scaled = pix.scaled(int(680 * 0.72), 680, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    add_lyt_gbx_lyt_res_lyt_iml.setPixmap(pix_scaled)
    update_card_count_in_add_cards(collections_connection, add_cards_found_cards, current_index, add_lyt_gbx_lyt_res_lyt_lbl)
#Add cards -> Regular -> Events
def add_regular_button_pressed():
    from modules.database.collections import get_card_ids_from_collection
    from modules.ui_functions import add_card_to_collection_in_add_cards, update_card_count_in_add_cards
    global cards_in_collection
    
    current_index = add_lyt_gbx_lyt_lst.currentRow()
    add_card_to_collection_in_add_cards(database_connection, collections_connection, add_cards_found_cards, add_cards_sorted_list, current_index, 1, 0, 'add')
    update_card_count_in_add_cards(collections_connection, add_cards_found_cards, current_index, add_lyt_gbx_lyt_res_lyt_lbl)
    cards_in_collection = get_card_ids_from_collection(collections_connection, config.get('COLLECTION', 'current_collection'))
    config.set('FLAG', 'collection_needs_refreshing', 'true')
    config.set('FLAG', 'progression_needs_refreshing', 'true')
#Add cards -> Foil -> Events
def add_foil_button_pressed():
    from modules.database.collections import get_card_ids_from_collection
    from modules.ui_functions import add_card_to_collection_in_add_cards, update_card_count_in_add_cards
    global cards_in_collection
    
    current_index = add_lyt_gbx_lyt_lst.currentRow()
    add_card_to_collection_in_add_cards(database_connection, collections_connection, add_cards_found_cards, add_cards_sorted_list, current_index, 0, 1, 'add')
    update_card_count_in_add_cards(collections_connection, add_cards_found_cards, current_index, add_lyt_gbx_lyt_res_lyt_lbl)
    cards_in_collection = get_card_ids_from_collection(collections_connection, config.get('COLLECTION', 'current_collection'))
    config.set('FLAG', 'collection_needs_refreshing', 'true')
    config.set('FLAG', 'progression_needs_refreshing', 'true')

#Wishlist
def create_wishlist_tab():
    tab_bar.addTab(wsh, config.get('APP', 'wishlist'))

#Import/export
def create_import_export_tab():
    tab_bar.addTab(imp, config.get('APP', 'import_export'))
    imp.setLayout(imp_lyt)
    imp_lyt.addWidget(imp_lyt_gbx)
    imp_lyt_gbx.setLayout(imp_lyt_gbx_lyt)
    imp_lyt_gbx_lyt.addWidget(imp_lyt_gbx_lyt_inp)
    imp_lyt_gbx_lyt_inp.setLayout(imp_lyt_gbx_lyt_inp_lyt)
    imp_lyt_gbx_lyt_inp_lyt.addWidget(imp_lyt_gbx_lyt_inp_lyt_lbl)
    imp_lyt_gbx_lyt_inp_lyt.addWidget(imp_lyt_gbx_lyt_inp_lyt_lin)
    imp_lyt_gbx_lyt.addWidget(imp_lyt_gbx_lyt_par)
    imp_lyt_gbx_lyt_par.setLayout(imp_lyt_gbx_lyt_par_lyt)
    imp_lyt_gbx_lyt_par_lyt.addWidget(imp_lyt_gbx_lyt_par_lyt_lbl)
    imp_lyt_gbx_lyt_par_lyt.addWidget(imp_lyt_gbx_lyt_par_lyt_cmb)
    imp_lyt_gbx_lyt_par_lyt_cmb.addItems([TEMPLATE_PATTERNS[0]['name'], 'Custom pattern'])
    imp_lyt_gbx_lyt_par_lyt_cmb.currentIndexChanged.connect(pattern_combobox_index_changed)
    imp_lyt_gbx_lyt_par_lyt_cmb.setCurrentIndex(1)
    imp_lyt_gbx_lyt_par_lyt_cmb.setCurrentIndex(0)
    imp_lyt_gbx_lyt_par_lyt.addWidget(imp_lyt_gbx_lyt_par_lyt_lin)
    imp_lyt_gbx_lyt_par_lyt.addWidget(imp_lyt_gbx_lyt_par_lyt_chk)
    imp_lyt_gbx_lyt_par_lyt.addWidget(imp_lyt_gbx_lyt_par_lyt_leg)
    imp_lyt_gbx_lyt_par_lyt.addWidget(imp_lyt_gbx_lyt_par_lyt_imp)
    imp_lyt_gbx_lyt_par_lyt_imp.clicked.connect(import_button_pressed)
    imp_lyt_gbx_lyt_par_lyt.addWidget(imp_lyt_gbx_lyt_par_lyt_exp)
    imp_lyt_gbx_lyt_par_lyt.addWidget(imp_lyt_gbx_lyt_par_lyt_inl)
    imp_lyt_gbx_lyt_par_lyt.addWidget(imp_lyt_gbx_lyt_par_lyt_inp)
    imp_lyt_gbx_lyt.addWidget(imp_lyt_gbx_lyt_res)
    imp_lyt_gbx_lyt_res.setLayout(imp_lyt_gbx_lyt_res_lyt)
    imp_lyt_gbx_lyt_res_lyt.addWidget(imp_lyt_gbx_lyt_res_lyt_lbl)
    imp_lyt_gbx_lyt_res_lyt.addWidget(imp_lyt_gbx_lyt_res_lyt_scr)
    imp_lyt_gbx_lyt_res_lyt_scr.setReadOnly(True)
#Import/export -> Events
def import_button_pressed():
    from modules.ui_functions import process_import_list, refresh_collection_names_in_corner
    
    import_list = imp_lyt_gbx_lyt_inp_lyt_lin.toPlainText().splitlines()
    process_import_list(database_connection, collections_connection, import_list, imp_lyt_gbx_lyt_par_lyt_lin.text(), imp_lyt_gbx_lyt_res_lyt_scr, imp_lyt_gbx_lyt_par_lyt_inp, imp_lyt_gbx_lyt_par_lyt_chk)
    refresh_collection_names_in_corner(collections_connection, cor_lyt_cmb, config.get('COLLECTION', 'current_collection'))
def pattern_combobox_index_changed():
    i = imp_lyt_gbx_lyt_par_lyt_cmb.currentIndex()
    TEMPLATE_PATTERNS
    if i == len(TEMPLATE_PATTERNS):
        imp_lyt_gbx_lyt_par_lyt_lin.setText('')
        imp_lyt_gbx_lyt_par_lyt_lin.setEnabled(True)
        imp_lyt_gbx_lyt_par_lyt_chk.setEnabled(True)
    else:
        imp_lyt_gbx_lyt_par_lyt_lin.setText(TEMPLATE_PATTERNS[i]['pattern'])
        imp_lyt_gbx_lyt_par_lyt_lin.setEnabled(False)
        imp_lyt_gbx_lyt_par_lyt_chk.setChecked(True) if TEMPLATE_PATTERNS[i]['header'] else imp_lyt_gbx_lyt_par_lyt_chk.setChecked(False)
        imp_lyt_gbx_lyt_par_lyt_chk.setEnabled(False)

#Settings
def create_settings_tab():
    tab_bar.addTab(stt, config.get('APP', 'settings'))
    stt.setLayout(stt_lyt)
    
    download = QPushButton('Download all images in collection')
    download.clicked.connect(download_all_clicked)
    stt_lyt.addWidget(download)
#Settings -> Events
def download_all_clicked():
    from modules.ui_functions import download_all_images_in_collection
    from modules.database.collections import get_card_ids_from_collection, get_collections_formatted_name
    
    ids = get_card_ids_from_collection(collections_connection, config.get('COLLECTION', 'current_collection'))
    download_all_images_in_collection(database_connection, ids)

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