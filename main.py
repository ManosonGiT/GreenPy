import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QDesktopWidget, QFileDialog, \
    QMessageBox


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
            return file_name



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
