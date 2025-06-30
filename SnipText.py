import sys
import os
from PyQt6 import QtWidgets, QtGui, QtCore
from modules.settings import SettingsManager
from modules.snipper import SnippingWidget

from PIL import Image
import numpy as np
import pytesseract
from docx import Document

# ✅ Define Tesseract path (update if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_image(np_img, lang='eng'):
    try:
        if np_img.shape[2] == 4:
            rgb_img = np_img[..., :3][..., ::-1]
        else:
            rgb_img = np_img[..., ::-1]
        pil_img = Image.fromarray(rgb_img)
        text = pytesseract.image_to_string(pil_img, lang=lang)
        return text
    except Exception as e:
        return f"[OCR Error]: {str(e)}"

def save_text_to_docx(text, output_path):
    doc = Document()
    for line in text.splitlines():
        doc.add_paragraph(line)
    doc.save(output_path)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snip & OCR App")
        self.setGeometry(100, 100, 500, 350)

        # Load settings
        self.settings = SettingsManager()

        # UI setup
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QtWidgets.QVBoxLayout(self.central_widget)

        # --- Button row ---
        button_layout = QtWidgets.QHBoxLayout()
        self.snip_button = QtWidgets.QPushButton("Take Screenshot")
        self.save_button = QtWidgets.QPushButton("Save as Word (.docx)")
        button_layout.addWidget(self.snip_button)
        button_layout.addWidget(self.save_button)
        main_layout.addLayout(button_layout)

        main_layout.addSpacing(10)

        # --- OCR output box ---
        self.ocr_text = QtWidgets.QPlainTextEdit()
        self.ocr_text.setReadOnly(False)
        main_layout.addWidget(self.ocr_text, stretch=1)

        # Snipping tool
        self.snipper = SnippingWidget()
        self.snipper.snip_complete.connect(self.handle_snip)

        # Button connections
        self.snip_button.clicked.connect(self.start_snip)
        self.save_button.clicked.connect(self.save_docx)

        self.last_ocr_text = ""

    def start_snip(self):
        self.hide()
        QtCore.QTimer.singleShot(200, self.snipper.start)

    def handle_snip(self, img_np):
        self.show()
        text = ocr_image(img_np)
        self.last_ocr_text = text
        self.ocr_text.setPlainText(text)

    def save_docx(self):
        text = self.ocr_text.toPlainText()
        if not text.strip():
            QtWidgets.QMessageBox.warning(self, "No text", "There is no text to save.")
            return

        save_dir = self.settings.get('General', 'save_location') or 'output'
        os.makedirs(save_dir, exist_ok=True)

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save as Word Document",
            os.path.join(save_dir, "snip_text.docx"),
            "Word Document (*.docx)"
        )
        if file_path:
            save_text_to_docx(text, file_path)
            QtWidgets.QMessageBox.information(self, "Saved", f"Text saved to {file_path}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
