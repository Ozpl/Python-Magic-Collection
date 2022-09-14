from operator import and_
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from modules.consts import UI_TAB_NAMES
#from consts import UI_TAB_NAMES

class UI(QWidget):
    def __init__(self, parent=None) -> None:
        super(UI, self).__init__(parent)

        self.color_palette = QApplication.palette()
        
        self.app_layout = QHBoxLayout()

        self.tab_bar = QTabWidget()
        self.collection_tab = self.create_collection_tab()
        self.tab_bar.addTab(self.collection_tab, 'Collection')

        #todo
        decks_tab = QWidget()
        decks_lyt = QVBoxLayout()
        decks_tab.setLayout(decks_lyt)
        self.tab_bar.addTab(decks_tab, 'Decks')

        self.app_layout.addWidget(self.tab_bar)
        self.setLayout(self.app_layout)
        
        self.setWindowTitle('Python Magic Collection')
        QApplication.setStyle('Fusion')

    def create_collection_tab(self) -> QWidget:
        collection_tab = QWidget()
        collection_tab_lyt = QHBoxLayout()
        self.create_cards_layout(collection_tab_lyt)
        self.create_preview_layout(collection_tab_lyt)
        collection_tab.setLayout(collection_tab_lyt)
        return collection_tab

    def create_cards_layout(self, collection_tab_lyt: QHBoxLayout):
        cards_gbx = QGroupBox()
        cards_lyt = QVBoxLayout()
        cards_lyt.addWidget(self.create_filter_group_box())
        cards_lyt.addWidget(self.create_grid_group_box())
        cards_lyt.addWidget(self.create_page_controls_group_box())
        cards_gbx.setLayout(cards_lyt)
        collection_tab_lyt.addWidget(cards_gbx)

    def create_filter_group_box(self) -> QGroupBox:
        filter_gbx = QGroupBox()
        filter_gbx.setMaximumHeight(35+27)
        filter_lyt = QHBoxLayout()

        for symbol in ['W', 'U', 'B', 'R', 'G', 'C']:
            image_lbl = QLabel()
            image = QPixmap(f'images/symbols/{symbol}.svg')
            image_lbl.setPixmap(image)
            image_lbl.setScaledContents(True)
            image_lbl.setMaximumSize(35,35)
            #image_lbl.setStyleSheet("background-image: url(./images/muldrotha.png)")
            image_lbl.setStyleSheet("")
            filter_lyt.addWidget(image_lbl)

        and_rbt = QRadioButton('And')
        and_rbt.setChecked(True)
        and_rbt.setMaximumSize(60,30)
        #and_rbt.setSizePolicy(QSizePolicy.Policy)
        filter_lyt.addWidget(and_rbt)
        or_rbt = QRadioButton('Or')
        or_rbt.setMaximumSize(60,30)
        filter_lyt.addWidget(or_rbt)

        for symbol in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            image_lbl = QLabel()
            image = QPixmap(f'images/symbols/{symbol}.svg')
            image_lbl.setPixmap(image)
            image_lbl.setScaledContents(True)
            image_lbl.setMaximumSize(35,35)
            #image_lbl.setStyleSheet("background-image: url(./images/muldrotha.png)")
            image_lbl.setStyleSheet("")
            filter_lyt.addWidget(image_lbl)

        filter_gbx.setLayout(filter_lyt)
        return filter_gbx

    def create_grid_group_box(self) -> QGroupBox:
        grid_gbx = QGroupBox()
        grid_lyt = QHBoxLayout()

        for i in range(5):
            image_lbl = QLabel()
            image = QPixmap(f'images/muldrotha.png')
            image_lbl.setPixmap(image)
            image_lbl.setScaledContents(True)
            image_lbl.setMaximumSize(210,int(210*1.39))
            grid_lyt.addWidget(image_lbl)
        
        grid_gbx.setLayout(grid_lyt)
        return grid_gbx

    def create_page_controls_group_box(self) -> QGroupBox:
        page_controls_gbx = QGroupBox()
        page_controls_lyt = QVBoxLayout()
        page_controls_gbx.setMaximumHeight(35+27)

        page_controls_label = QLabel('PageControlsGroupBox -> PageControlsLayout -> PageControlsLabel')
        page_controls_lyt.addWidget(page_controls_label)
        page_controls_gbx.setLayout(page_controls_lyt)
        return page_controls_gbx

    def create_preview_layout(self, collection_tab_lyt: QHBoxLayout):
        preview_gbx = QGroupBox()
        preview_lyt = QHBoxLayout()

        image_lbl = QLabel()
        image = QPixmap(f'images/muldrotha.png')
        image_lbl.setPixmap(image)
        image_lbl.setScaledContents(True)
        image_lbl.setMaximumSize(400,int(400*1.39))

        #create components
        preview_lyt.addWidget(image_lbl)
        preview_gbx.setLayout(preview_lyt)
        collection_tab_lyt.addWidget(preview_gbx)

def manage_ui():
    app = QApplication([])
    ui = UI()
    ui.showMaximized()
    app.exec()

#debug
#manage_ui()

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

'''
class UI(QWidget):
    def __init__(self, parent=None) -> None:
        super(UI, self).__init__(parent)

        self.color_palette = QApplication.palette()

        collecion_combo_box = QComboBox()
        collecion_combo_box.addItems(['Col1', 'Col2'])

        collection_label = QLabel('Current Collection:')
        collection_label.setBuddy(collecion_combo_box)

        self.create_main_panel()
        self.create_preview_panel()

        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.preview_group_box)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.main_group_box)
        main_layout.addLayout(preview_layout)

        self.setLayout(main_layout)

        self.setWindowTitle('Python Magic Collection')
        QApplication.setStyle('Fusion')

    def create_collection_grid(self):
        collection_grid = QGridLayout()

        for i in range(0,9):
            for j in range(0,6,2):
                label = QLabel(f'Muldrotha: Kolumna: {i} Wiersz: {j}')
                image_label = QLabel()
                image = QPixmap('images/muldrotha.png')
                image_label.setPixmap(image)
                image_label.setScaledContents(True)
                image_label.setMinimumSize(215,int(215*1.39))
                image_label.setMaximumSize(215,int(215*1.39))
                collection_grid.addWidget(label, j, i)
                collection_grid.addWidget(image_label, j+1, i)
        return collection_grid
        

    def create_main_panel(self):
        self.main_group_box = QGroupBox()

        tab_bar = QTabWidget()
        font = tab_bar.font()
        font.setPixelSize(32)
        tab_bar.setFont(font)

        tab1 = QWidget()
        font = tab_bar.font()
        font.setPixelSize(12)
        tab1.setFont(font)
        tab1_hbox = QHBoxLayout()
        tab1_hbox.setContentsMargins(5, 5, 5, 5)
        tab1_hbox.addLayout(self.create_collection_grid())
        tab1.setLayout(tab1_hbox)
        tab_bar.addTab(tab1, 'Collection')

        tab2 = QWidget()
        font = tab_bar.font()
        font.setPixelSize(12)
        tab2.setFont(font)
        tab2_text_edit = QTextEdit()
        tab2_hbox = QHBoxLayout()
        tab2_hbox.setContentsMargins(5, 5, 5, 5)
        tab2_hbox.addWidget(tab2_text_edit)
        tab2.setLayout(tab2_hbox)
        tab_bar.addTab(tab2, 'Decks')

        for element in UI_TAB_NAMES[2:]:
            tab_bar.addTab(QWidget(), element)

        layout = QVBoxLayout()
        layout.addWidget(tab_bar)
        self.main_group_box.setLayout(layout)
        
    def create_preview_panel(self):
        self.preview_group_box = QGroupBox()
        self.preview_group_box.setMinimumWidth(350)
        self.preview_group_box.setMaximumWidth(350)

        combo = QComboBox()
        font = combo.font()
        font.setPixelSize(28)
        combo.setFont(font)
        combo.addItems(['Collection 1', 'Collection 2', 'Collection 3'])
        combo.setMaximumHeight(60)

        image_label = QLabel()
        image = QPixmap('images/muldrotha.png')
        image_label.setPixmap(image)
        image_label.setScaledContents(True)
        image_label.setMaximumSize(350-20,int(350*1.396))

        text = QTextBrowser()
        text.setMinimumSize(200,int(200*1.396))
        text.setMaximumWidth(350)
        text.setPlainText('Muldrotha\nTest card')

        layout = QVBoxLayout()
        layout.addWidget(combo)
        layout.addWidget(image_label)
        layout.addWidget(text)
        self.preview_group_box.setLayout(layout)
'''