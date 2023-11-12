import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

# Create a PyQt application instance
app = QApplication(sys.argv)

# Create a main window
window = QWidget()
window.setWindowTitle('GreenPY')


label = QLabel('Hello, PyQt!')
button = QPushButton('Click Me')


layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)


window.setLayout(layout)


def on_button_click():
    label.setText('Button Clicked!')


button.clicked.connect(on_button_click)

window.show()

sys.exit(app.exec_())
