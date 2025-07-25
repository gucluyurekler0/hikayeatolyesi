from PySide6.QtWidgets import QTextEdit


class TextEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Buraya hikayeni yaz...")
        self.setFixedSize(600, 200)
        self.setStyleSheet("""
            QTextEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
        """)
