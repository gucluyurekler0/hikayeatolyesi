from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QColorDialog
from ui.main_window import Ui_MainWindow
from modules.drawing_area import DrawingArea
from modules.text_editor import TextEditor
from PySide6.QtGui import QPixmap, QPainter, QImage, QColor, QFont
from PySide6.QtCore import Qt
import sys
import os
import cv2
import numpy as np

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Hayal Gücü Defteri")

        self.pages = []
        self.current_page_index = -1

        self.ui.pushButton.setText("KAYDET")
        self.ui.pushButton_2.setText("TEMİZLE")

        from PySide6.QtWidgets import QPushButton
        self.btn_new = QPushButton("YENİ SAYFA", self)
        self.btn_new.setGeometry(280, 510, 100, 24)
        self.btn_prev = QPushButton("ÖNCEKİ", self)
        self.btn_prev.setGeometry(400, 510, 75, 24)
        self.btn_next = QPushButton("SONRAKİ", self)
        self.btn_next.setGeometry(500, 510, 75, 24)

        self.btn_new.clicked.connect(self.add_new_page)
        self.btn_prev.clicked.connect(self.previous_page)
        self.btn_next.clicked.connect(self.next_page)

        self.btn_color = QPushButton("RENK SEÇ", self)
        self.btn_color.setGeometry(600, 510, 75, 24)
        self.btn_color.clicked.connect(self.select_color)

        self.btn_video = QPushButton("VIDEO OLUŞTUR", self)
        self.btn_video.setGeometry(700, 510, 100, 24)
        self.btn_video.clicked.connect(self.create_video_slideshow)

        self.ui.pushButton.clicked.connect(self.save_current_page)
        self.ui.pushButton_2.clicked.connect(self.clear_current_page)

        self.selected_color = QColor(0, 0, 0)

        self.add_new_page()

    def add_new_page(self):
        self.clear_layout(self.ui.drawingLayout)
        self.clear_layout(self.ui.textLayout)

        drawing_area = DrawingArea(self)
        text_editor = TextEditor(self)

        drawing_area.set_pen_color(self.selected_color)

        self.ui.drawingLayout.addWidget(drawing_area)
        self.ui.textLayout.addWidget(text_editor)

        self.pages.append({
            'drawing': drawing_area,
            'text': text_editor
        })
        self.current_page_index = len(self.pages) - 1

    def clear_current_page(self):
        if self.pages:
            self.pages[self.current_page_index]['drawing'].clear()
            self.pages[self.current_page_index]['text'].clear()

    def save_current_page(self):
        if not self.pages:
            return

        page = self.pages[self.current_page_index]
        drawing_pixmap = page['drawing'].grab()
        text = page['text'].toPlainText()

        text_height = 100
        width = drawing_pixmap.width()
        height = drawing_pixmap.height() + text_height

        final_image = QImage(width, height, QImage.Format_RGB32)
        final_image.fill(Qt.white)

        painter = QPainter(final_image)
        painter.drawPixmap(0, 0, drawing_pixmap)
        painter.setPen(QColor(0, 0, 0))
        font = QFont("Arial", 12)
        painter.setFont(font)
        painter.drawText(10, drawing_pixmap.height() + 30, text)
        painter.end()

        filename = f"sayfa_{self.current_page_index + 1}.png"
        final_image.save(filename)
        QMessageBox.information(self, "Kaydedildi", f"Sayfa {self.current_page_index + 1} '{filename}' olarak kaydedildi.")

    def previous_page(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.load_page(self.current_page_index)

    def next_page(self):
        if self.current_page_index < len(self.pages) - 1:
            self.current_page_index += 1
            self.load_page(self.current_page_index)

    def load_page(self, index):
        if index < 0 or index >= len(self.pages):
            return

        self.clear_layout(self.ui.drawingLayout)
        self.clear_layout(self.ui.textLayout)

        page = self.pages[index]
        self.ui.drawingLayout.addWidget(page['drawing'])
        self.ui.textLayout.addWidget(page['text'])

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

    def select_color(self):
        color = QColorDialog.getColor(self.selected_color, self)
        if color.isValid():
            self.selected_color = color
            if self.pages:
                self.pages[self.current_page_index]['drawing'].set_pen_color(self.selected_color)

    def create_video_slideshow(self):
        image_folder = "./"
        image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

        if not image_files:
            QMessageBox.warning(self, "Hata", "Hiçbir resim bulunamadı!")
            return

        def extract_number_from_filename(filename):
            number = ''.join(filter(str.isdigit, filename))
            return int(number) if number else 0

        image_files.sort(key=extract_number_from_filename)

        frame_size = (500, 500)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter("slideshow.mp4", fourcc, 1, frame_size)

        for image_file in image_files:
            image_path = os.path.join(image_folder, image_file)
            image = cv2.imread(image_path)

            resized_image = cv2.resize(image, frame_size)
            video.write(resized_image)

        video.release()
        QMessageBox.information(self, "Başarılı", "Slayt video başarıyla oluşturuldu!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
