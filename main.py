import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QDesktopWidget, QFileDialog, \
    QMessageBox, QToolBar, QPushButton, QTextEdit


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window size
        self.resize(800, 600)  # (x, y, width, height)
        self.setWindowTitle('GreenPy Editor')
        self.center()

        # Create menu bar
        menubar = self.menuBar()

        # Create File menu
        file_menu = menubar.addMenu('File')

        #File menu Open button
        open_action = QAction('Open', self)
        file_menu.addAction(open_action)
        open_action.triggered.connect(self.open_file_dialog)

        #
        toolbar = QToolBar("My Toolbar")
        self.addToolBar(toolbar)

        # Add  button to the toolbar
        square_button1 = QPushButton('Analyze code', self)
        toolbar.addWidget(square_button1)

        self.editor = QTextEdit(self)
        self.setCentralWidget(self.editor)

        #Exit menu button
        exit_action=QAction('Exit',self)
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(self.close)
    def center(self):
        # Center the window on the screen
        screen_geometry = QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "All Files (*);;Text Files (*.txt);;CSV Files (*.csv);;Python Files (*.py)",
                                                   options=options)
        if file_name:
            print(f"Selected file: {file_name}")

            if file_name[-3:] != '.py':
                QMessageBox.warning(self, 'Warning', 'Invalid file type selected. Please choose a valid file type.')
                return None
            else:
                self.load_file(file_name)

    def load_file(self, file_path):
        with open(file_path, 'r') as file:
            self.editor.setPlainText(file.read())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
