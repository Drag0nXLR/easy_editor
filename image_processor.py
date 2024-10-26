import os
from main import ui, work_dir
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
class ImageProcessor:
    def __init__(self):
        self.filename = None
        self.dir = None
        self.image = None
        self.save_dir = 'modified\\'


    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(work_dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        ui.label.hide()
        pixmapimage = QPixmap(path)
        w, h = ui.label.width(), ui.label.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        ui.label.setPixmap(pixmapimage)
        ui.label.show()

workimage = ImageProcessor()

def showChosenImage():
    if ui.files.currentRow() >= 0:
        filename = ui.files.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(work_dir, workimage.filename)
        workimage.showImage(image_path)

ui.files.currentRowChanged.connect(showChosenImage)
