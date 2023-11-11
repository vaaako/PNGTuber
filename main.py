import pyaudio, aubio, sys, threading
import numpy as np

from time import sleep
from PIL import Image, ImageDraw, ImageFont, ImageTk
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from window import Window

class PNGTuber:
	def __init__(self, title: str = "Vako PNG Tuber", size: tuple[int] = (200, 200), imgs_path: tuple[str] = ('media/1.png', 'media/2.png')):
		self.title = title
		self.size = size

		# self.frames = (Image.open(imgs_path[0]), Image.open(imgs_path[1]))
		print(imgs_path[0], imgs_path[1])
		self.frames = [Image.open(path).resize(self.size, Image.LANCZOS) for path in imgs_path]

		# Threading
		self.stop = False
		self.window = None
		self.app = None
		self.window_thread = threading.Thread(target=self._window_thread)
		self.window_thread.start()

		# PyAudio
		self.p = pyaudio.PyAudio()
		self.CHUNK = 1024
		# self.FORMAT = pyaudio.paInt16
		self.FORMAT = pyaudio.paFloat32
		self.CHANNELS = 1
		self.RATE = 44100
		self.stream = self.p.open(format=self.FORMAT,
							 channels=self.CHANNELS,
							 rate=self.RATE,
							 input=True,
							 frames_per_buffer=self.CHUNK)

		## Setup Pitch
		self.TOLERANCE = 0.8
		self.FFT_S = 4096 # FFT Size
		self.HOP_S = self.CHUNK # Hop Size
		self.pitch_o = aubio.pitch('default', self.FFT_S, self.HOP_S, self.RATE)
		self.pitch_o.set_unit('midi')
		self.pitch_o.set_tolerance(self.TOLERANCE)

	def _window_thread(self):
		self.app = QApplication(sys.argv)
		self.window = Window(self.frames[0], self.set_stop, self.title, self.size) # Initial image (just to start the window), Exit callback, Title
		self.window.show()
		sys.exit(self.app.exec_())

	# Stop main loop
	def set_stop(self):
		self.stop = True

	def listen(self, limit: int = 40):
		audiobuffer = self.stream.read(self.CHUNK)
		signal = np.frombuffer(audiobuffer, dtype=np.float32)

		pitch = self.pitch_o(signal)[0]
		confidence = self.pitch_o.get_confidence()

		print(f"{pitch} / {confidence}")

		if pitch > float(limit):
			png.display(1)
		else:
			png.display(0)

	def close_window(self):
		self.app.quit() # It actually crashes, but works

		# Stop thread
		self.window_thread.join() # Wait for the thread to finish

		# Close PyAudio
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()



	def display(self, frame):
		# pass
		if self.window:
			img = self.frames[frame].toqpixmap()
			self.window.display_image(img)

if __name__ == '__main__':
	png = PNGTuber("Vako PNG Tuber", (200, 200), ('media/1.png', 'media/2.png'))

	limit = 40 # Default value
	if len(sys.argv) > 1:
		limit = sys.argv[1]

	while not png.stop:
		png.listen(limit)
	png.close_window() # KeyboardInterrupt only
