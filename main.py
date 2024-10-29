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
    # Initialize an empty list to store the filtered filenames
    res = []
    # Iterate through each file in the list of files
    for file in files:
        # Iterate through each extension in the list of extensions
        for ext in extensions:
            # Check if the file ends with the current extension
            if file.endswith(ext):
                # Add the file to the result list
                res.append(file)
    # Return the filtered list of filenames
    return res

def choose_work_dir():
    """
    Opens a dialog to allow the user to select a directory as the working directory.

    This function uses a file dialog to prompt the user to choose a directory.
    The selected directory's path is stored in the global variable `work_dir`.
    """
    global work_dir  # Declare work_dir as a global variable to modify it
    # Open a dialog to select a directory and assign the result to work_dir
    work_dir = QFileDialog.getExistingDirectory()

def show_file_name_dist():
    """
    Shows the list of files in the selected directory.

    This function is connected to the button in the UI that allows the user
    to select a directory. It filters out files with extensions that are not
    image files and populates the list in the UI with the filtered list.
    """
    # Define the list of file extensions considered as image files
    extensions = ['.jpg', '.png', '.jpeg', '.svg', '.bmp', '.eps']
    
    # Allow the user to select a directory as the working directory
    choose_work_dir()
    
    # Filter out files with extensions that are not image files
    filenames = filter(os.listdir(work_dir), extensions)
    
    # Clear the current list of files in the UI
    ui.files.clear()
    
    # Populate the UI list with the filtered filenames
    for filename in filenames:
        ui.files.addItem(filename)

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

        # Constructor method for ImageProcessor class
        # Sets up initial values for attributes related to image processing


    def loadImage(self, filename):
        """
        Loads an image from a file and assigns it to the `image` attribute.

        This function sets the initial state of the image object by loading
        an image from a file and assigning it to the `image` attribute.

        Args:
            filename (str): Name of the file to load the image from
        """
        self.filename = filename
        """
        Name of the file to load the image from.
        """
        image_path = os.path.join(work_dir, filename)
        """
        Full path of the image file to be loaded.
        """
        self.image = Image.open(image_path)
        """
        Image object to perform operations on.
        """

    def showImage(self, path):
        """
        Displays an image on the UI label.
        
        Args:
            path (str): The file path of the image to be displayed.
        
        This function loads an image from the specified file path,
        scales it to fit the label while maintaining the aspect ratio,
        and then displays it on the UI label.
        """
        # Hide the label to prevent flickering during the update
        ui.label.hide()
        
        # Load the image from the provided file path
        pixmapimage = QPixmap(path)
        
        # Retrieve the dimensions of the label to scale the image accordingly
        w, h = ui.label.width(), ui.label.height()
        
        # Scale the image to fit the label's dimensions while maintaining aspect ratio
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        
        # Set the scaled image on the label
        ui.label.setPixmap(pixmapimage)
        
        # Show the label with the updated image
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
        # Saves the image in the 'modified' directory
        self.saveImage()
        
        # Builds a path to the saved image
        image_path = os.path.join(
            work_dir, self.save_dir, self.filename
        )
        
        # Shows the saved image
        self.showImage(image_path)
    
    def do_bw(self):
        """
        Converts the image to black and white.

        Applies the luminance filter to the image, which converts each
        pixel to its grayscale value, saving the result in the 'modified'
        directory, and then displays the new image.

        This method is equivalent to calling `convert` with the "L" argument.
        """
        # Convert the image to grayscale (black and white)
        self.image = self.image.convert("L")

        # Save the modified image and display it
        self._save()
    
    def do_flip(self):
        """
        Flips the image horizontally.

        Flips the image along the vertical axis, saving the result
        in the 'modified' directory, and then displays the new image.

        This method is equivalent to calling `transpose` with the
        `FLIP_LEFT_RIGHT` argument.  The image is flipped along the
        vertical axis, meaning that the left and right sides of the
        image are swapped.
        """
        # Flip the image horizontally
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)

        # Save the modified image
        self._save()
        
    def rotateLeft(self):
        """
        Rotate the image 90 degrees to the left.

        Saves the rotated image in the 'modified' directory and then
        displays the new image.

        The image is rotated 90 degrees to the left, which is
        equivalent to rotating it 270 degrees to the right.
        """
        # Rotate the image 90 degrees to the left. This is equivalent
        # to rotating it 270 degrees to the right.
        self.image = self.image.transpose(Image.ROTATE_90)

        # Save the modified image
        self._save()
        
    def rotateRight(self):
        """
        Rotate the image 90 degrees to the right.

        Saves the rotated image in the 'modified' directory and then
        displays the new image.

        The image is rotated 90 degrees to the right, which is
        equivalent to rotating it 270 degrees to the left.
        """
        # Rotate the image 90 degrees to the right
        self.image = self.image.transpose(Image.ROTATE_270)

        # Save the modified image
        self._save()

    def sharpen(self):
        """
        Applies sharpening filter to the image.

        Applies sharpening filter to the image, which helps to highlight
        the details in the image. It then saves the modified image and
        displays it.

        The sharpening filter works by emphasizing the difference between
        adjacent pixels in the image. This can be useful for reducing
        the appearance of noise and making the image appear more crisp.
        """
        # Apply the sharpening filter to the image
        self.image = self.image.filter(SHARPEN)

        # Save the modified image
        self._save()
    
    def blur(self):
        """
        Applies a blur filter to the image.

        This function applies a blur filter to the image, which helps
        to reduce noise and detail, creating a smooth effect. It then
        saves the modified image and displays it.
        """
        # Apply the blur filter to the image
        self.image = self.image.filter(BLUR)
        
        # Save the blurred image
        self._save()
    
    def gaussianBlur(self):
        """
        Applies a Gaussian Blur to the image.

        This function applies a Gaussian Blur filter to the image, which
        helps to reduce noise and detail. The Gaussian Blur smoothens the
        image by averaging the pixels around each pixel. It then saves the
        modified image and displays it.
        """
        # Apply a Gaussian Blur filter with a radius of 5
        self.image = self.image.filter(GaussianBlur(radius=5))
        
        # Save the blurred image
        self._save()

    def unsharpMask(self):
        """
        Applies Unsharp Mask to the image.

        Applies Unsharp Mask to the image, which is a sharpening filter
        that highlights the details in the image. It then saves the modified
        image and displays it.

        Unsharp Mask is a filter that accentuates the difference between
        the image and a blurred version of it, which helps to highlight
        the details in the image.
        """
        # Applies Unsharp Mask filter
        self.image = self.image.filter(UnsharpMask)
        
        # Saves an image
        self._save()
    
    def contour(self):
        """
        Applies a contour filter to the image.

        This function applies a contour filter to the image, which helps 
        to emphasize the edges and outlines of objects within the image. 
        It then saves the modified image and displays it.
        """
        # Apply the contour filter to the image
        self.image = self.image.filter(CONTOUR)
        
        # Save the modified image
        self._save()
    
    def detail(self):
        """
        Applies a detail filter to the image.

        Applies a detail filter to the image, which helps to
        highlight the details in the image. This filter is often
        used to sharpen the image and make the details more
        visible. It then saves the modified image and displays it.
        """
        # Applies detail filter
        self.image = self.image.filter(DETAIL)
        # Saves an image
        self._save()
    
    def edge_enhance(self, level=1):
        """
        Applies an edge enhance filter to the image.

        Applies an edge enhance filter to the image, which helps to
        enhance the edges in the image. The level parameter determines
        the strength of the edge enhancement. A level of 1 gives a
        moderate edge enhancement, while a level of 2 gives a stronger
        enhancement.

        Args:
            level (int): The level of edge enhancement (default is 1).
        """
        # Applies edge enhance filter
        self.image = self.image.filter(EDGE_ENHANCE_MORE if level > 1 else EDGE_ENHANCE)
        self._save()
    
    def emboss(self):
        """
        Applies an emboss filter to the image.

        Applies an emboss filter to the image, which helps to create
        a raised appearance. This filter is often used to create a
        3D effect on images. It then saves the modified image and
        displays it.
        """
        # Applies emboss filter
        self.image = self.image.filter(EMBOSS)
        # Saves an image
        self._save()
    
    def smooth(self, level=1):
        """
        Applies a smoothing filter to the image.

        This function applies a smoothing filter to the image, which helps to
        reduce noise and soften the image. It then saves the modified image
        and displays it.

        Args:
            level (int): The level of smoothing (default is 1). A level greater
                         than 1 applies a stronger smoothing effect.
        """
        # Determine the appropriate smoothing filter based on the level
        smoothing_filter = SMOOTH_MORE if level > 1 else SMOOTH
        
        # Apply the determined smoothing filter to the image
        self.image = self.image.filter(smoothing_filter)
        
        # Save the modified image
        self._save()
        
    def findEdges(self):
        """
        Applies a find edges filter to the image.

        Applies a find edges filter to the image, saves the modified image
        and shows it.

        The find edges filter is a type of image processing filter that
        highlights the edges in an image. It works by applying the
        gradient operator to the image, which detects areas of the
        image with high gradient values. The gradient values are then
        used to create an image that is a visual representation of the
        gradient values.

        The find edges filter is commonly used as a preprocessing step
        for other image processing algorithms, such as edge detection
        and segmentation.
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