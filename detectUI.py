import sys
from PyQt5.QtWidgets import (QCheckBox, QWidget, 
							QPushButton, QFileDialog, QApplication,
							QPlainTextEdit, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from completeness import run_detection

class ChangeDetectorApp(QWidget):
    
	image1 = ""
	image2 = ""
	result_path = ""
	AppSize = (600, 300)
	NUMBER_OF_SLICES = 9

	def __init__(self):
		super().__init__()
		self.AppTitle = "Satellite Images Change Detector"
		self.initUI()
		self.setFixedSize(*self.AppSize)
		self.setWindowTitle(self.AppTitle)
		self.show()
		self.output.insertPlainText(">>> Program Started\n")
		
	def initUI(self):

		#set background image of main window
		oImage = QImage("background.jpg")
		sImage = oImage.scaled(QSize(*self.AppSize))
		palette = QPalette()
		palette.setBrush(10, QBrush(sImage))
		self.setPalette(palette)

		#settings of image 1 button
		image1 = QPushButton('First Image', self)
		image1.setToolTip('Click to choose first photo')
		image1.resize(image1.sizeHint())
		image1.clicked.connect(self.openFile1NameDialog)

		#settings of image 2 button
		image2 = QPushButton('Second Image', self)
		image2.setToolTip('Click to choose second photo')
		image2.resize(image2.sizeHint())
		image2.clicked.connect(self.openFile2NameDialog)

		#settings of result button
		self.result = QPushButton('Result path', self)
		self.result.setToolTip('Click to choose where to save the result')
		self.result.resize(self.result.sizeHint())
		self.result.clicked.connect(self.saveFileDialog)
		self.result.setEnabled(False)

		#settings of save result check box
		self.save_res = QCheckBox('Save Result', self)
		self.save_res.setToolTip('Click this to save the output result on the disk')
		self.save_res.stateChanged.connect(self.saveResult)
		self.save_res.setAutoFillBackground(True)
		p = self.save_res.palette()
		p.setColor(self.save_res.backgroundRole(), Qt.white)
		self.save_res.setPalette(p)

		#settings of detect button
		detect = QPushButton('Detect', self)
		detect.setToolTip('Click to detect changes between inputs')
		detect.resize(detect.sizeHint())
		detect.clicked.connect(self.detectClicked)
		
		# creating a plainText box for output messages
		self.output = QPlainTextEdit(self)

		#settings of quit button
		quit = QPushButton('Quit', self)
		quit.setToolTip('Click to quit the app')
		quit.resize(quit.sizeHint())
		quit.clicked.connect(QApplication.instance().quit)

		# setting layout of main window
		resultBox = QHBoxLayout()
		resultBox.setSpacing(10)
		resultBox.addWidget(self.result)
		resultBox.addWidget(self.save_res)

		leftBox = QVBoxLayout()
		leftBox.addWidget(image1)
		leftBox.addWidget(image2)
		leftBox.addLayout(resultBox)
		leftBox.addStretch(1)
		leftBox.addWidget(detect)

		rightBox = QVBoxLayout()
		rightBox.addWidget(self.output)
		rightBox.addStretch(1)
		rightBox.addWidget(quit)
		
		layout = QHBoxLayout()
		layout.addLayout(leftBox)
		layout.addStretch(1)
		layout.addLayout(rightBox)

		self.setLayout(layout)

	def detectClicked(self):
		if self.image1 == "":
			self.output.insertPlainText("! Error: Enter first image\n")
		elif self.image2 == "":
			self.output.insertPlainText("! Error: Enter second image\n")
		else:
			self.output.insertPlainText(">>> Detection Started\n")
			run_detection(self.image1, self.image2, self.NUMBER_OF_SLICES)
            
	def openFile1NameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PNG Files (*.png);;JPG Files (*.jpg);;JPEG Files (*.jpeg)", options=options)
		if fileName:
			self.image1 = fileName
			self.output.insertPlainText(">>> First image is {}\n".format(self.image1))

	def openFile2NameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;PNG Files (*.png);;JPG Files (*.jpg);;JPEG Files (*.jpeg)", options=options)
		if fileName:
			self.image2 = fileName
			self.output.insertPlainText(">>> Second image is {}\n".format(self.image2))

	def saveFileDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;PNG Files (*.png)", options=options)
		if fileName:
			self.result_path = fileName
			self.output.insertPlainText(">>> Result save to {}\n".format(self.result_path))

	def saveResult(self, state):
		if state == Qt.Checked:
			self.result.setEnabled(True)
			self.result_path = ""
		else:
			self.result.setEnabled(False)
			self.result_path = ""
			
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = ChangeDetectorApp()
	sys.exit(app.exec_())
