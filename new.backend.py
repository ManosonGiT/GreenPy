import sys
import ast
import graphviz
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QSplitter, QToolBar, QPushButton,
    QTextEdit, QDialog, QVBoxLayout, QTextBrowser, QGraphicsView,
    QGraphicsScene, QGraphicsPixmapItem, QAction
)
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor
from PyQt5.QtCore import QFile, QTextStream, Qt, QByteArray, QSize

def analyze_code(code):
    try:
        tree = ast.parse(code)
        dot = generate_dot(tree)
        results = analyze_ast(tree)
        show_results(dot, results)
    except Exception as e:
        notify(f"Error analyzing code: {str(e)}")
        
def analyze_ast(tree):
    while_statements = []
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            line_number = node.lineno
            while_statement = f"While found on line {line_number}. Consider using a for loop for better performance."
            while_statements.append(while_statement)
    return while_statements

def generate_dot(tree):
    dot = graphviz.Digraph(format='png')
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            dot.node(str(id(node)), label=f"While at line {node.lineno}", color='red', style='filled')
        else:
            dot.node(str(id(node)), label=str(type(node).__name__))
        if hasattr(node, 'parent'):
            dot.edge(str(id(node.parent)), str(id(node)))
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                dot.edge(str(id(node)), str(id(value)), label=field)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        dot.edge(str(id(node)), str(id(item)), label=field)
    return dot

def show_results(dot, results):
    app = QApplication.instance()
    dialog = ASTViewer()  # Supprimer la ligne existante d'instanciation de ASTViewer
    dialog.dot = dot  # Assigner dot à l'attribut dot de ASTViewer
    dialog.results = results  # Assigner results à l'attribut results de ASTViewer
    dialog.resize(800, 600)
    dialog.exec_()

def notify(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(message)
    msg_box.setWindowTitle("Code Analysis Notification")
    msg_box.exec_()

class ASTViewer(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AST Analysis Results")
        self.setWindowIcon(QIcon("GreenPy.png"))
        layout = QVBoxLayout()

        
        
        self.see_ast_button = QPushButton('See AST')
        self.apply_stylesheet_to_button(self.see_ast_button, "style.css")
        layout.addWidget(self.see_ast_button)
        self.see_ast_button.clicked.connect(self.show_ast_tree)
        
        self.text_browser = QTextBrowser()
        layout.addWidget(self.text_browser)
        self.splitter = QSplitter(Qt.Vertical)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.splitter.addWidget(self.view)
        layout.addWidget(self.splitter)

        self.setLayout(layout)
        self.dot = None
        self.results = None

    def apply_stylesheet_to_button(self, button, style_path):
        style_file = QFile(style_path)
        if not style_file.open(QFile.ReadOnly | QFile.Text):
            return

        text_stream = QTextStream(style_file)
        stylesheet = text_stream.readAll()

        button.setStyleSheet(stylesheet)
        style_file.close()

    def show_ast_tree(self):
        self.text_browser.setPlainText("\n".join(self.results))
        self.text_browser.moveCursor(QTextCursor.End)
        self.text_browser.ensureCursorVisible()
        if self.dot is not None and self.dot is not None:
            
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(self.dot.pipe(format='png')), "PNG")
            item = QGraphicsPixmapItem(pixmap)
            self.scene.clear()
            self.scene.addItem(item)
            self.view.fitInView(item, Qt.KeepAspectRatio)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            num_degrees = event.angleDelta().y() / 8
            num_steps = num_degrees / 15
            factor = 1.2 ** num_steps

            self.view.scale(factor, factor)
            event.accept()

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('GreenPy Editor')
        self.center()

        self.editor = QTextEdit(self)
        self.setCentralWidget(self.editor)

        toolbar = QToolBar("My Toolbar")
        self.addToolBar(toolbar)

        analyze_action = QAction(QIcon(), "Analyze Code", self)
        analyze_action.triggered.connect(self.analyze_code)
        toolbar.addAction(analyze_action)

    def center(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def analyze_code(self):
        code = self.editor.toPlainText()
        analyze_code(code)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ast_viewer = ASTViewer()
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())