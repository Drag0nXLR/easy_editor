from easy_editor_layout import *
from PyQt5.QtWidgets import (QFileDialog)
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import this
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)

import os
work_dir = None

ui = Ui_MainWindow()
def filter(files, extensions):
    """Filters images from list of images

    Args:
        files (list): All files
        extensions (list): Extensions like .jpg

    Returns:
        res: Returns filtered files
    """
    res = []
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                res.append(file)
    return res

def choose_work_dir():
    """Choosing a work dir
    """
    global work_dir
    work_dir = QFileDialog.getExistingDirectory()

def show_file_name_dist():
    """Shows filenames in list of files
    """
    extensions = ['.jpg', '.png','.jpeg', '.svg', '.bmp', '.eps']
    choose_work_dir()
    filenames = filter(os.listdir(work_dir), extensions)
    ui.files.clear()
    for filename in filenames:
        ui.files.addItem(filename)

class ImageProcessor:
    """class to make Image load
    """
    def __init__(self):
        self.filename = None
        self.dir = None
        self.image = None
        self.save_dir = 'modified\\'


    def loadImage(self, filename):
        """This is an extension for loading images

        Args:
            filename (image): The name of file
        """
        self.filename = filename
        image_path = os.path.join(work_dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        """Makes image shown

        Args:
            path (str): This is a path of working directory
        """
        ui.label.hide()
        pixmapimage = QPixmap(path)
        w, h = ui.label.width(), ui.label.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        ui.label.setPixmap(pixmapimage)
        ui.label.show()
    
    def saveImage(self):
        """saves an image
        """
        path = os.path.join(work_dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    
    def do_bw(self):
        """makes image black and white
        """
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(work_dir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_flip(self):
        """Mirrors an image
        """
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(
            work_dir, self.save_dir, self.filename
        )
        self.showImage(image_path)
        
    def rotateLeft(self):
        """Rotates image left
        """
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(
            work_dir, self.save_dir, self.filename
        )
        self.showImage(image_path)
        
    def rotateRight(self):
        """rotates image right
        """
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(
            work_dir, self.save_dir, self.filename
        )
        self.showImage(image_path)

    def sharpen(self):
        """
        Applies sharpening filter to the image.

        Applies sharpening filter to the image, saves the modified image
        and shows it.
        """
        # Applies sharpening filter
        self.image = self.image.filter(SHARPEN)
        # Saves an image
        self.saveImage()
        # Builds a path to the image
        image_path = os.path.join(
            work_dir, self.save_dir, self.filename
        )
        # Shows an image
        self.showImage(image_path)
    
    def blur(self):
        self.image = self.image.filter(BLUR)
        self.saveImage()
        image_path = os.path.join(
            work_dir, self.save_dir, self.filename
        )
        self.showImage(image_path)
        

workimage = ImageProcessor()

def showChosenImage():
    """Shows a chosen image
    """
    if ui.files.currentRow() >= 0:
        filename = ui.files.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(work_dir, workimage.filename)
        workimage.showImage(image_path)

if __name__ == "__main__":
    """Starts a programe
    """
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)
    ui.papka.clicked.connect(show_file_name_dist)
    ui.rizkist.clicked.connect(workimage.sharpen)
    ui.blur.clicked.connect(workimage.blur)
    ui.mirror.clicked.connect(workimage.do_flip)
    ui.left.clicked.connect(workimage.rotateLeft)
    ui.right.clicked.connect(workimage.rotateRight)
    ui.black_white.clicked.connect(workimage.do_bw)
    ui.files.currentRowChanged.connect(showChosenImage)
    MainWindow.show()
    sys.exit(app.exec_())





