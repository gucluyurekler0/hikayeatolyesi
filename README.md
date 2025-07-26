# Hikaye Atölyesi

Hikaye Atölyesi, çizim yapabileceğiniz ve yazı yazabileceğiniz interaktif bir masaüstü uygulamasıdır. Kullanıcılar birden fazla sayfa oluşturabilir, her sayfaya özel çizimler ve metinler ekleyebilir ve bu sayfaları `.png` olarak kaydedebilir. Ek olarak, tüm sayfalardan otomatik bir video slayt gösterisi (MP4) de oluşturabilirsiniz.

## Özellikler

- 🖌️ Serbest çizim yapabilme
- 📝 Sayfaya not/öykü yazabilme
- 🗂️ Sayfa yönetimi (Yeni, Önceki, Sonraki)
- 🎨 Renk seçme aracı
- 💾 Sayfa kaydetme (PNG formatında)
- 🎬 Video slayt gösterisi oluşturma (MP4 formatında)

## Ekran Görüntüsü

![Hikaye Atölyesi Ekran Görüntüsü](assets/ekrangorntusu.png)

## Kurulum

Python ortamınızı oluşturduktan sonra:

```bash
pip install -r requirements.txt
```

### Uygulamayı çalıştırmak için:

```bash
python main.py
```

## Gereksinimler

- Python 3.8+
- PySide6 (Qt tabanlı GUI)
- OpenCV (video işleme için)
- NumPy

## Proje Yapısı

```
.
├── main.py
├── modules/
│   ├── drawing_area.py
│   └── text_editor.py
├── ui/
│   └── main_window.py
│   └── main_window.ui
├── assets/
│   └── screenshot.jpeg
├── requirements.txt
├── README.md
└── .gitignore
```