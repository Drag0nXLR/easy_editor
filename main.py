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
    """
    Filters the list of files, returning only those with the specified extensions.

    Args:
        files (list): List of filenames to filter.
        extensions (list): List of file extensions to include.

    Returns:
        list: A list of filenames that end with one of the specified extensions.
    """
    res = []
    for file in files:
        for ext in extensions:
            # Check if the file ends with the current extension
            if file.endswith(ext):
                # Add the file to the result list
                res.append(file)
    return res

def choose_work_dir():
    """
    Allows the user to select a directory as the working directory.

    The selected directory is stored globally in the work_dir variable.
    """
    global work_dir
    work_dir = QFileDialog.getExistingDirectory()

def show_file_name_dist():
    """
    Shows the list of files in the selected directory.

    This function is connected to the button in the UI that allows the user
    to select a directory. It filters out files with extensions that are not
    image files and populates the list in the UI with the filtered list.
    """
    extensions = ['.jpg', '.png','.jpeg', '.svg', '.bmp', '.eps']
    """
    List of file extensions that are considered image files.
    """
    choose_work_dir()
    """
    Allows the user to select a directory as the working directory.
    """
    filenames = filter(os.listdir(work_dir), extensions)
    """
    Filters out files with extensions that are not image files.
    """
    ui.files.clear()
    """
    Clears the list of files in the UI.
    """
    for filename in filenames:
        ui.files.addItem(filename)
    """
    Populates the list in the UI with the filtered list.
    """

class ImageProcessor:
    def __init__(self):
        """
        Initializes the ImageProcessor instance.

        Sets up initial values for attributes related to image processing.
        """
        self.filename = None  # Name of the file to be processed
        self.dir = None  # Directory where the file is located
        self.image = None  # Image object to perform operations on
        self.save_dir = 'modified\\'  # Directory to save modified images

    def loadImage(self, filename):
        """
        Loads an image from a file and assigns it to the `image` attribute.

        Args:
            filename (str): Name of the file to load the image from
        """
        self.filename = filename
        image_path = os.path.join(work_dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        """
        Displays an image on the UI label.
        
        Args:
            path (str): The file path of the image to be displayed.
        """
        # Hide the label before setting the pixmap
        ui.label.hide()
        
        # Load the image from the provided path
        pixmapimage = QPixmap(path)
        
        # Retrieve the dimensions of the label
        w, h = ui.label.width(), ui.label.height()
        
        # Scale the image to fit the label while maintaining aspect ratio
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        
        # Set the scaled pixmap on the label
        ui.label.setPixmap(pixmapimage)
        
        # Show the label with the new image
        ui.label.show()
    
    def saveImage(self):
        """
        Saves the image in the 'modified' directory in the same directory
        as the original file.

        The image is saved with the same name as the original file.
        """
        path = os.path.join(work_dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            # Create the 'modified' directory if it does not already exist
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        # Save the image in the 'modified' directory
        self.image.save(image_path)
    
    def _save(self):
        """
        Saves the image in the 'modified' directory in the same directory
        as the original file, and then displays the saved image.
        
        The image is saved with the same name as the original file.
        """
        self.saveImage()
        # Builds a path to the image
        image_path = os.path.join(
            work_dir, self.save_dir, self.filename
        )
        # Shows an image
        self.showImage(image_path)
    
    def do_bw(self):
        """
        Converts the image to black and white.

        Applies the luminance filter to the image, saving the result
        in the 'modified' directory, and then displays the new image.
        """
        # Convert the image to grayscale (black and white)
        self.image = self.image.convert("L")

        self._save()
    
    def do_flip(self):
        """
        Flips the image horizontally.

        Flips the image along the vertical axis, saving the result
        in the 'modified' directory, and then displays the new image.
        """
        # Flip the image horizontally
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)

        self._save()
        
    def rotateLeft(self):
        """
        Rotate the image 90 degrees to the left.

        Saves the rotated image in the 'modified' directory and then
        displays the new image.
        """
        # Rotate the image 90 degrees to the left
        self.image = self.image.transpose(Image.ROTATE_90)

        self._save()
        
    def rotateRight(self):
        """
        Rotate the image 90 degrees to the right.

        Saves the rotated image in the 'modified' directory and then
        displays the new image.
        """
        # Rotate the image 90 degrees to the right
        self.image = self.image.transpose(Image.ROTATE_270)

        self._save()

    def sharpen(self):
        """
        Applies sharpening filter to the image.

        Applies sharpening filter to the image, saves the modified image
        and shows it.
        """
        # Applies sharpening filter
        self.image = self.image.filter(SHARPEN)
        self._save()
    
    def blur(self):
        """Applies blur filter to the image.

        Applies blur filter to the image, saves the modified image
        and shows it.
        """
        # Applies blur filter
        self.image = self.image.filter(BLUR)
        self._save()
    
    def gaussianBlur(self):
        """
        Applies a Gaussian Blur to the image.

        Applies a Gaussian Blur to the image, saves the modified image
        and shows it.
        """
        # Applies Gaussian Blur filter
        self.image = self.image.filter(GaussianBlur(radius=5))
        # Saves an image
        self._save()

    def unsharpMask(self):
        """
        Applies Unsharp Mask to the image.

        Applies Unsharp Mask to the image, saves the modified image
        and shows it.
        """
        # Applies Unsharp Mask filter
        self.image = self.image.filter(UnsharpMask)
        # Saves an image
        self._save()
    
    def contour(self):
        """
        Applies a contour filter to the image.

        Applies a contour filter to the image, saves the modified image
        and shows it.
        """
        # Applies contour filter
        self.image = self.image.filter(CONTOUR)
        # Saves an image
        self._save()
    
    def detail(self):
        """
        Applies a detail filter to the image.

        Applies a detail filter to the image, saves the modified image
        and shows it.
        """
        # Applies detail filter
        self.image = self.image.filter(DETAIL)
        # Saves an image
        self._save()
    
    def edge_enhance(self, level=1):
        """
        Applies an edge enhance filter to the image.

        Applies an edge enhance filter to the image, saves the modified image
        and shows it.

        Args:
            level (int): The level of edge enhancement (default is 1).
        """
        # Applies edge enhance filter
        self.image = self.image.filter(EDGE_ENHANCE_MORE if level > 1 else EDGE_ENHANCE)
        self._save()
    
    def emboss(self):
        """
        Applies an emboss filter to the image.

        Applies an emboss filter to the image, saves the modified image
        and shows it.
        """
        # Applies emboss filter
        self.image = self.image.filter(EMBOSS)
        # Saves an image
        self._save()
    
    def smooth(self, level=1):
        """
        Applies a smooth filter to the image.

        Applies a smooth filter to the image, saves the modified image
        and shows it.

        Args:
            level (int): The level of smoothing (default is 1).
        """
        # Applies smooth filter
        self.image = self.image.filter(SMOOTH_MORE if level > 1 else SMOOTH)
        # Saves an image
        self._save()
        
    def findEdges(self):
        """
        Applies a find edges filter to the image.

        Applies a find edges filter to the image, saves the modified image
        and shows it.
        """
        # Applies find edges filter
        self.image = self.image.filter(FIND_EDGES)
        # Saves an image
        self._save()
    
workimage = ImageProcessor()

def showChosenImage():
    """Displays the selected image from the UI file list.

    Retrieves the filename of the currently selected file in the UI list,
    loads the image using the ImageProcessor instance, constructs the full
    image path, and displays the image on the UI label.
    """
    # Check if a file is selected in the list
    if ui.files.currentRow() >= 0:
        # Get the filename of the selected file
        filename = ui.files.currentItem().text()
        
        # Load the image using the ImageProcessor instance
        workimage.loadImage(filename)
        
        # Construct the full path of the image
        image_path = os.path.join(work_dir, workimage.filename)
        
        # Display the image on the UI label
        workimage.showImage(image_path)
        

if __name__ == "__main__":
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
    ui.contour.clicked.connect(workimage.contour)
    ui.detail.clicked.connect(workimage.detail)
    ui.edge_enhance.clicked.connect(workimage.edge_enhance)
    ui.emboss.clicked.connect(workimage.emboss)
    ui.smooth.clicked.connect(workimage.smooth)
    ui.find_edges.clicked.connect(workimage.findEdges)
    ui.unsharp.clicked.connect(workimage.unsharpMask)
    ui.gaussianBlur.clicked.connect(workimage.gaussianBlur)  
    ui.files.currentRowChanged.connect(showChosenImage)
    MainWindow.show()
    sys.exit(app.exec_())