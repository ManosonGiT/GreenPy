import ast
from plyer import notification
from PyQt5.QtWidgets import QMessageBox

def analyze_code(code):
    try:
        tree = ast.parse(code)
        # Perform AST analysis, e.g., check for 'while' statements
        for node in ast.walk(tree):
            if isinstance(node, ast.While):
                line_number = node.lineno
                notify(f"While found on line {line_number} you can change it with a for loop which runs faster!")
    except Exception as e:
        notify(f"Error analyzing code: {str(e)}")

def notify(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(message)
    msg_box.setWindowTitle("Code Analysis Notification")
    msg_box.exec_()
