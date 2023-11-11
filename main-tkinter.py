import pyaudio, sys, aubio
import tkinter as tk
import numpy as np
from time import sleep
from PIL import Image, ImageDraw, ImageFont, ImageTk


class PNGTuber:
	def __init__(self, title: str = "Vako PNG Tuber", width: int = 200, height: int = 200, imgs_path: tuple[str] = ('media/1.png', 'media/2.png')):
		self.title = title
		self.width = width
		self.height = height

		# self.frames = (Image.open(imgs_path[0]), Image.open(imgs_path[1]))

		print(imgs_path[0], imgs_path[1])
		self.frames = [Image.open(path).resize((width, height), Image.LANCZOS) for path in imgs_path]

		# Tkinter
		self.window = tk.Tk()
		self.window.title(self.title)
		self.window.geometry(f'{self.width}x{self.height}')
		
		# self.window.overrideredirect(True) # Hide the root window drag bar and close button

		# self.window.wait_visibility(self.window)
		# self.window.wm_attributes('-alpha', 0.5)
		self.window.wm_attributes('-transparentcolor','black')

		self.label = tk.Label(self.window)
		self.label.pack()



		# PyAudio
		p = pyaudio.PyAudio()
		self.CHUNK = 1024
		# self.FORMAT = pyaudio.paInt16
		self.FORMAT = pyaudio.paFloat32
		self.CHANNELS = 1
		self.RATE = 44100
		self.stream = p.open(format=self.FORMAT,
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

	def _update_window(self):
		self.window.update_idletasks()



	def listen(self, limit: int = 40):
		audiobuffer = self.stream.read(self.CHUNK)
		signal = np.frombuffer(audiobuffer, dtype=np.float32)

		pitch = self.pitch_o(signal)[0]
		confidence = self.pitch_o.get_confidence()

		print(f"{pitch} / {confidence}")

		if pitch > limit:
			png.display(1)
		else:
			png.display(0)


	def display(self, frame, time: int = None):
		img = ImageTk.PhotoImage(self.frames[frame])
		self.label.config(image=img)
		self.label.image = img


		self._update_window()


if __name__ == '__main__':
	png = PNGTuber("Vako PNG Tuber", 200, 200, ('media/1.png', 'media/2.png'))
	
	# png.start()
	while True:
		pitch = png.listen(50) # What pitch change frame

