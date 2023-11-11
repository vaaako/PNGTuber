import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PIL import Image

class Window(QMainWindow):
	def __init__(self, start_image: Image, close_callback, title: str = "Window", size: tuple[int] = (200, 200)):
		super().__init__()
		self.callback = close_callback	
		image = start_image.toqpixmap() # Convert initial image to pixmap

		# Label
		self.label = QLabel(self)
		# self.label.setPixmap(image) # Use image (Image is just used to start window)

		# Layout
		layout = QVBoxLayout()
		layout.addWidget(self.label)
		central_widget = QWidget(self)
		central_widget.setLayout(layout)
		self.setCentralWidget(central_widget)

		# Create window
		self.setWindowTitle(title)
		self.setGeometry(100, 100, size[0], size[1])


		# Transparent background
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setAttribute(Qt.WA_NoSystemBackground, True)
		self.setWindowFlags(Qt.FramelessWindowHint)

	# Move window
	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.previous_pos = event.globalPos()

		# Close when press RMB
		if event.button() == Qt.RightButton:
			self.callback()

	def mouseMoveEvent(self, event):
		if self.previous_pos:
			delta = event.globalPos() - self.previous_pos
			self.move(self.pos() + delta)
			self.previous_pos = event.globalPos()

	def mouseReleaseEvent(self, event):
		self.previous_pos = None

	# Image
	def display_image(self, image):
		# if hasattr(self, 'label'):
		# 	self.layout().removeWidget(self.label)
		# 	self.label.deleteLater()

		# self.label = QLabel(self)
		self.label.setPixmap(image)
		self.layout().addWidget(self.label)
