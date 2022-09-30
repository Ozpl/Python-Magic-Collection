from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from modules.consts import APP_NAME, APP_STYLE, APP_TAB_NAMES, APP_FONT_NAME, APP_FONT_SIZE
from modules.database.functions import get_card_from_db
from modules.logging import log

app = QApplication([])

collection_tab = QWidget()
collection_tab_lyt = QHBoxLayout()

cards_gbx = QGroupBox()
cards_lyt = QVBoxLayout()

filter_gbx = QGroupBox()
filter_lyt = QHBoxLayout()
filter_colors_lbls = []
filter_colors_flags = []
filter_and_rbt = QRadioButton('And')
filter_or_rbt = QRadioButton('Or')
filter_mv = []
filter_search_lbl = QLabel('Search box:')
filter_search_txb = QLineEdit()
filter_search_button = QPushButton('Find cards')

page_controls_gbx = QGroupBox()
page_controls_lyt = QVBoxLayout()

preview_gbx = QGroupBox()
preview_lyt = QHBoxLayout()

#Main
def create_user_interface(db_connection, cl_connection, cd_connection):
    global database_connection, collections_connection, cards_connection
    database_connection = db_connection
    collections_connection = cl_connection
    cards_connection = cd_connection
    log('info', 'Creating UI...')
    ui = UI()
    ui.showMaximized()
    app.exec()

#UI Class
class UI(QWidget):
    def __init__(self, parent=None) -> None:
        super(UI, self).__init__(parent)

        self.app_layout = QVBoxLayout()

        self.tab_bar = QTabWidget()
        create_collection_tab(self.tab_bar)
        create_decks_tab(self.tab_bar)
        create_add_cards_tab(self.tab_bar)
        create_wishlist_tab(self.tab_bar)
        create_import_export_tab(self.tab_bar)
        create_settings_tab(self.tab_bar)

        self.collection_cbx = QComboBox()
        self.collection_cbx.addItems(['Whole database', 'Add new collection...'])

        self.tab_bar.setCornerWidget(self.collection_cbx)
        self.app_layout.addWidget(self.tab_bar)
        self.setLayout(self.app_layout)
        
        self.app_font = QFont(APP_FONT_NAME, APP_FONT_SIZE)
        self.setFont(self.app_font)
        self.setWindowTitle(APP_NAME)
        QApplication.setStyle(APP_STYLE)

#Collection Tab
def create_collection_tab(tab_widget) -> QWidget:
    create_cards_layout(collection_tab_lyt)
    create_preview_layout(collection_tab_lyt)
    
    collection_tab.setLayout(collection_tab_lyt)
    tab_widget.addTab(collection_tab, APP_TAB_NAMES['collection'])
#Collection Tab -> Cards Layout
def create_cards_layout(collection_tab_lyt: QHBoxLayout):
    cards_lyt.addWidget(create_filter_group_box())
    cards_lyt.addWidget(create_grid_group_box())
    cards_lyt.addWidget(create_page_controls_group_box())
    cards_gbx.setLayout(cards_lyt)
    collection_tab_lyt.addWidget(cards_gbx)
#Collection Tab -> Cards Layout -> 1. Filter Buttons
def create_filter_group_box() -> QGroupBox:
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
    return filter_gbx
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
#Collection Tab -> Cards Layout -> 2. Grid
def create_grid_group_box() -> QGroupBox:
    grid_gbx = QGroupBox()
    grid_lyt = QHBoxLayout()

    for element in ['_small.jpg', '_normal.jpg', '_large.jpg', '.png']:
        image_lbl = QLabel()
        image = QPixmap(f'images/muldrotha{element}')
        image_lbl.setPixmap(image)
        image_lbl.setScaledContents(True)
        image_lbl.setMaximumSize(210,int(210*1.39))
        grid_lyt.addWidget(image_lbl)
    
    grid_gbx.setLayout(grid_lyt)
    return grid_gbx
#Collection Tab -> Cards Layout -> 3. Page Controls
def create_page_controls_group_box() -> QGroupBox:
    page_controls_gbx.setMaximumHeight(35+27)

    page_controls_label = QLabel('PageControlsGroupBox -> PageControlsLayout -> PageControlsLabel')

    debug_button_fetch_card = QPushButton('Fetch card')
    debug_button_fetch_card.clicked.connect(lambda: print(get_card_from_db(database_connection, '002ad179-ddf4-4f48-9504-cfa02e11a52e')))

    page_controls_lyt.addWidget(debug_button_fetch_card)
    page_controls_lyt.addWidget(page_controls_label)
    page_controls_gbx.setLayout(page_controls_lyt)
    return page_controls_gbx

#Collection Tab -> Preview Layout
def create_preview_layout(collection_tab_lyt: QHBoxLayout):
    image_lbl = QLabel()
    image = QPixmap(f'images/muldrotha_normal.jpg')
    image_lbl.setPixmap(image)
    image_lbl.setScaledContents(True)
    image_lbl.setMaximumSize(400,int(400*1.39))

    #create components
    preview_lyt.addWidget(image_lbl)
    preview_gbx.setLayout(preview_lyt)
    collection_tab_lyt.addWidget(preview_gbx)



#Decks Tab
def create_decks_tab(tab_widget) -> QWidget:
    decks_tab = QWidget()
    decks_tab_lyt = QHBoxLayout()

    #TODO
    
    decks_tab.setLayout(decks_tab_lyt)
    tab_widget.addTab(decks_tab, APP_TAB_NAMES['decks'])

#Add cards Tab
def create_add_cards_tab(tab_widget) -> QWidget:
    add_cards_tab = QWidget()
    add_cards_tab_lyt = QHBoxLayout()

    #TODO
    
    add_cards_tab.setLayout(add_cards_tab_lyt)
    tab_widget.addTab(add_cards_tab, APP_TAB_NAMES['add_cards'])

#Import/export Tab
def create_wishlist_tab(tab_widget) -> QWidget:
    wishlist_tab = QWidget()
    wishlist_tab_lyt = QHBoxLayout()

    #TODO
    
    wishlist_tab.setLayout(wishlist_tab_lyt)
    tab_widget.addTab(wishlist_tab, APP_TAB_NAMES['wishlist'])

#Import/export Tab
def create_import_export_tab(tab_widget) -> QWidget:
    import_export_tab = QWidget()
    import_export_tab_lyt = QHBoxLayout()

    #TODO
    
    import_export_tab.setLayout(import_export_tab_lyt)
    tab_widget.addTab(import_export_tab, APP_TAB_NAMES['import_export'])

#Settings Tab
def create_settings_tab(tab_widget) -> QWidget:
    settings_tab = QWidget()
    settings_tab_lyt = QHBoxLayout()

    #TODO
    
    settings_tab.setLayout(settings_tab_lyt)
    tab_widget.addTab(settings_tab, APP_TAB_NAMES['settings'])

'''
*MainWindow

**MainPanel
***TabBar
****FilterBar
****GridView
*****QuantityLabel
*****CardImage
****PageControl

**PreviewPanel/DeckPanel
***Collection/DeckSelector
***CardImage
***CardLabel
****CardDesc
****CardQuantities
****CardTags
'''