from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QColorDialog, QPushButton
from ui.main_window import Ui_MainWindow
from modules.drawing_area import DrawingArea
from modules.text_editor import TextEditor
from PySide6.QtGui import QPixmap, QPainter, QImage, QColor, QFont
from PySide6.QtCore import Qt
import sys
import os
import cv2
import numpy as np

class HikayeUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.arayuz = Ui_MainWindow()
        self.arayuz.setupUi(self)

        self.setWindowTitle("Hikaye Atölyesi")

        self.sayfalar = []
        self.secili_sayfa = -1

        self.arayuz.pushButton.setText("KAYDET")
        self.arayuz.pushButton_2.setText("TEMİZLE")

        self.buton_yeni = QPushButton("YENİ SAYFA", self)
        self.buton_yeni.setGeometry(280, 510, 100, 24)

        self.buton_geri = QPushButton("ÖNCEKİ", self)
        self.buton_geri.setGeometry(400, 510, 75, 24)

        self.buton_ileri = QPushButton("SONRAKİ", self)
        self.buton_ileri.setGeometry(500, 510, 75, 24)

        self.buton_renk = QPushButton("RENK SEÇ", self)
        self.buton_renk.setGeometry(600, 510, 75, 24)

        self.buton_video = QPushButton("VİDEO OLUŞTUR", self)
        self.buton_video.setGeometry(700, 510, 100, 24)

        self.buton_yeni.clicked.connect(self.sayfa_ekle)
        self.buton_geri.clicked.connect(self.onceki_sayfa)
        self.buton_ileri.clicked.connect(self.sonraki_sayfa)
        self.buton_renk.clicked.connect(self.renk_sec)
        self.buton_video.clicked.connect(self.video_olustur)

        self.arayuz.pushButton.clicked.connect(self.sayfayi_kaydet)
        self.arayuz.pushButton_2.clicked.connect(self.sayfayi_temizle)

        self.secili_renk = QColor(0, 0, 0)

        self.sayfa_ekle()

    def sayfa_ekle(self):
        self.tasarimi_temizle(self.arayuz.drawingLayout)
        self.tasarimi_temizle(self.arayuz.textLayout)

        cizim = DrawingArea(self)
        yazi = TextEditor(self)

        cizim.set_pen_color(self.secili_renk)

        self.arayuz.drawingLayout.addWidget(cizim)
        self.arayuz.textLayout.addWidget(yazi)

        self.sayfalar.append({
            'cizim': cizim,
            'yazi': yazi
        })

        self.secili_sayfa = len(self.sayfalar) - 1

    def sayfayi_temizle(self):
        if self.sayfalar:
            self.sayfalar[self.secili_sayfa]['cizim'].clear()
            self.sayfalar[self.secili_sayfa]['yazi'].clear()

    def sayfayi_kaydet(self):
        if not self.sayfalar:
            return

        sayfa = self.sayfalar[self.secili_sayfa]
        cizim_resmi = sayfa['cizim'].grab()
        yazi_metin = sayfa['yazi'].toPlainText()

        yazi_boy = 100
        genislik = cizim_resmi.width()
        yukseklik = cizim_resmi.height() + yazi_boy

        son_resim = QImage(genislik, yukseklik, QImage.Format_RGB32)
        son_resim.fill(Qt.white)

        kalem = QPainter(son_resim)
        kalem.drawPixmap(0, 0, cizim_resmi)
        kalem.setPen(QColor(0, 0, 0))
        yazi_font = QFont("Arial", 12)
        kalem.setFont(yazi_font)
        kalem.drawText(10, cizim_resmi.height() + 30, yazi_metin)
        kalem.end()

        dosya_adi = f"sayfa_{self.secili_sayfa + 1}.png"
        son_resim.save(dosya_adi)
        QMessageBox.information(self, "Kaydedildi", f"{dosya_adi} olarak kaydedildi.")

    def onceki_sayfa(self):
        if self.secili_sayfa > 0:
            self.secili_sayfa -= 1
            self.sayfa_yukle(self.secili_sayfa)

    def sonraki_sayfa(self):
        if self.secili_sayfa < len(self.sayfalar) - 1:
            self.secili_sayfa += 1
            self.sayfa_yukle(self.secili_sayfa)

    def sayfa_yukle(self, sira):
        if sira < 0 or sira >= len(self.sayfalar):
            return

        self.tasarimi_temizle(self.arayuz.drawingLayout)
        self.tasarimi_temizle(self.arayuz.textLayout)

        sayfa = self.sayfalar[sira]
        self.arayuz.drawingLayout.addWidget(sayfa['cizim'])
        self.arayuz.textLayout.addWidget(sayfa['yazi'])

    def tasarimi_temizle(self, tasarim):
        while tasarim.count():
            oge = tasarim.takeAt(0)
            kutu = oge.widget()
            if kutu is not None:
                kutu.setParent(None)

    def renk_sec(self):
        secim = QColorDialog.getColor(self.secili_renk, self)
        if secim.isValid():
            self.secili_renk = secim
            if self.sayfalar:
                self.sayfalar[self.secili_sayfa]['cizim'].set_pen_color(self.secili_renk)

    def video_olustur(self):
        klasor = "./"
        resimler = [dosya for dosya in os.listdir(klasor) if dosya.endswith('.png')]

        if not resimler:
            QMessageBox.warning(self, "Hata", "Hiçbir resim bulunamadı!")
            return

        def sirayi_al(dosya_adi):
            rakamlar = ''.join(filter(str.isdigit, dosya_adi))
            return int(rakamlar) if rakamlar else 0

        resimler.sort(key=sirayi_al)

        boyut = (500, 500)
        kodlayici = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter("slayt_gosterisi.mp4", kodlayici, 1/3, boyut)  # 3 saniyede 1 kare

        for resim in resimler:
            yol = os.path.join(klasor, resim)
            gorsel = cv2.imread(yol)
            gorsel = cv2.resize(gorsel, boyut)
            video.write(gorsel)

        video.release()
        QMessageBox.information(self, "Başarılı", "Slayt video başarıyla oluşturuldu!\nNot: Video program klasörüne kaydedildi.")

if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    pencere = HikayeUygulamasi()
    pencere.show()
    sys.exit(uygulama.exec())
