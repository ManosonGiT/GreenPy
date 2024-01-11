import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QAction, QDesktopWidget, QFileDialog,
    QMessageBox, QToolBar, QPushButton, QTextEdit, QScrollArea, QHBoxLayout,
    QComboBox, QWidget
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFile, QTextStream

from backend import analyze_code

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(800, 600)
        self.setWindowTitle('GreenPy Editor')
        self.center()

        with open('style.css', 'r') as style_file:
            self.setStyleSheet(style_file.read())

        self.setWindowIcon(QIcon('GreenPy.png'))

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        file_menu.addAction(open_action)
        open_action.triggered.connect(self.open_file_dialog)

        toolbar = QToolBar("My Toolbar")
        self.addToolBar(toolbar)

        analyze_button = QPushButton('Analyze Code', self)
        toolbar.addWidget(analyze_button)

        # Create a widget to hold the dropdown menus
        menu_widget = QWidget(self)
        menu_layout = QHBoxLayout(menu_widget)

        # Add "Country" dropdown menu
        self.country_combobox = QComboBox(self)
        country_dict = {'France': 50, 'Greece': 381, 'Germany': 624}
        self.country_combobox.addItems(country_dict.keys())
        self.country_combobox.setMinimumWidth(120)  # Set minimum width
        self.country_combobox.setMaximumWidth(120)  # Set maximum width
        menu_layout.addWidget(self.country_combobox)

        # Add "Processor" dropdown menu
        self.processor_combobox = QComboBox(self)
        processor_combobox = {'Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz': 44.99}
        self.processor_combobox.addItems(processor_combobox.keys())
        self.processor_combobox.setMinimumWidth(150)  # Set minimum width
        self.processor_combobox.setMaximumWidth(300)  # Set maximum width
        menu_layout.addWidget(self.processor_combobox)

        # Set the stylesheet for the QComboBoxes
        combo_box_style = """
            QComboBox {
                background-color: #2ecc71;
                color: white;
                padding: 10px 16px;
                border: none;
                border-radius: 4px;
            }
        """
        self.country_combobox.setStyleSheet(combo_box_style)
        self.processor_combobox.setStyleSheet(combo_box_style)

        # Set the widget with dropdowns to the right of the Analyze button
        toolbar.addWidget(menu_widget)

        analyze_button.clicked.connect(self.analyze_code_button_clicked)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.editor = QTextEdit(self)
        self.scroll_area.setWidget(self.editor)
        self.setCentralWidget(self.scroll_area)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(self.close)

    def center(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog(
            self, "Open File", "", "All Files (*);;Text Files (*.txt);;CSV Files (*.csv);;Python Files (*.py)"
        )
        dialog.setStyleSheet("""
            background-color: #ecf0f1;
            color: #2c3e50;
        """)

        dialog.setOptions(options)
        if dialog.exec_():
            file_name = dialog.selectedFiles()[0]
            print(f"Selected file: {file_name}")

            if not file_name.endswith('.py'):
                QMessageBox.warning(self, 'Warning', 'Invalid file type selected. Please choose a valid file type.')
                return None
            else:
                self.load_file(file_name)

    def load_file(self, file_path):
        with open(file_path, 'r') as file:
            self.editor.setPlainText(file.read())

    def analyze_code_button_clicked(self):
        code = self.editor.toPlainText()
        country = self.country_combobox.currentText()

        # Retrieve the numeric value for the selected country
        country_dict = {'France': 50, 'Greece': 381, 'Germany': 624}
        country_value = country_dict.get(country, 0)

        # Retrieve the selected processor from the combobox
        selected_processor = self.processor_combobox.currentText()

        # Dictionary mapping processor names to numeric values
        processor_dict = {'Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz': 44.99}

        # Get the numeric value for the selected processor
        processor_value = processor_dict.get(selected_processor, 0)

        analyze_code(code, country_value, processor_value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
