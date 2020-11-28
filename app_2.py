import sys, os
from datetime import datetime
from functools import partial
import json
import time

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QDesktopWidget

from movielist import MovieList

FILE_SAVE_LOCATION = "/home/eglis/Desktop/repos/MovieList" #probably change to getting the current directory

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('lister.ui', self)
        self.setWindowTitle("Eglis Listing")
        self.center()
        self.setWindowIcon(QIcon('movielist.png'))

        # dropdown selector
        self.inputType = self.findChild(QtWidgets.QComboBox, 'inputSelect')
        self.inputType.activated[str].connect(self.inputTypeSelector)

        # input field
        self.inputPath = self.findChild(QtWidgets.QLineEdit, 'TxtPath')

        # output field
        self.outputPath = self.findChild(QtWidgets.QLineEdit, 'ListPath')

        # name add field
        self.nameadd = self.findChild(QtWidgets.QLineEdit, 'NameAdd')

        # browse button for file
        self.btnBrowsein = self.findChild(QtWidgets.QPushButton, 'btnBrowseIn')
        self.btnBrowsein.clicked.connect(partial(self.fileSelector, "in"))

        self.btnBrowseout = self.findChild(QtWidgets.QPushButton, 'btnBrowseout')
        self.btnBrowseout.clicked.connect(partial(self.fileSelector, "out"))

        # start stop button
        self.isRunning = False
        self.startBtn = self.findChild(QtWidgets.QPushButton, 'btnStart')
        self.startBtn.clicked.connect(self.startBtnPress)

        # scale button
        self.scaleBtn = self.findChild(QtWidgets.QPushButton, 'btnScale')
        self.scaleBtn.clicked.connect(self.scaleBtnPress)

        # top list button
        self.topBtn = self.findChild(QtWidgets.QPushButton, 'btnTop')
        self.topBtn.clicked.connect(self.topBtnPress)

        # remove button
        self.removeBtn = self.findChild(QtWidgets.QPushButton, 'btnRemove')
        self.removeBtn.clicked.connect(self.removeBtnPress)

        # add button
        self.addBtn = self.findChild(QtWidgets.QPushButton, 'btnAdd')
        self.addBtn.clicked.connect(self.addBtnPress)

        # error msg
        self.errorLbl = self.findChild(QtWidgets.QLabel, 'error_msg')
        self.errorLbl.hide()

        # the config id reading part
        self.configId = self.findChild(QtWidgets.QLineEdit, 'inptConfigId')
        self.lblConf = self.findChild(QtWidgets.QLabel, 'lblConfig')
        self.inputConf = self.findChild(QtWidgets.QComboBox, 'selectConf')
        self.getConfigs()
        self.inputConf.activated[str].connect(self.selectConfig)
        self.savedConfigFile = ""

        # the nr of points to add should only be int
        self.onlyInt = QIntValidator()
        self.points = self.findChild(QtWidgets.QLineEdit, 'Points')
        self.points.setValidator(self.onlyInt)

        # the nr of top movies to add show should only be int
        self.onlyInt = QIntValidator()
        self.top = self.findChild(QtWidgets.QLineEdit, 'Top')
        self.top.setValidator(self.onlyInt)

        #calling the function for creating the first instance
        self.inputTypeSelector(self.inputType.currentText())

        self.show()  # Show the GUI

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def enableDisableUIEle(self, enable):
        self.inputType.setEnabled(enable)
        self.inputConf.setEnabled(enable)
        self.inputPath.setEnabled(enable)
        self.outputPath.setEnabled(enable)
        self.configId.setEnabled(enable)
    
    def printing(self, string_to_print):
        self.errorLbl.setText(string_to_print)
        self.errorLbl.setStyleSheet('color: green')
        self.errorLbl.show()

    def scaleBtnPress(self):
        self.algorithms.scale(self.outputPath.text())
        self.printing("Finish Scaling the file!")

    def topBtnPress(self):
        top_movies = self.algorithms.topmovies(int(self.top.text()), self.outputPath.text())
        print(top_movies) #print them in there so it is printed better
        self.printing("Finish Showing top movies!")

    def removeBtnPress(self):
        self.algorithms.remove(self.nameadd.text(), self.outputPath.text())
        self.printing("Finish Removing the movie!")
    
    def addBtnPress(self):
        self.algorithms.add(self.nameadd.text(), self.outputPath.text(), int(self.points.text()))
        self.printing("Finish Adding the movie!")

    def processtest(self):
        self.algorithms.readnotes(self.inputPath.text(), self.outputPath.text())

    def startBtnPress(self):
        if not self.isRunning:
            self.enableDisableUIEle(False)
            self.isRunning = True
            self.startBtn.setText("Stop")
            print("Processing starting from file: {}".format(self.inputPath.text()))
            start_time = time.time()
            self.processtest()
            print('... done. it took {} seconds'.format(time.time()-start_time))
            self.enableDisableUIEle(True)
            self.isRunning = False
            self.startBtn.setText("Start")
            self.printing("Finish processing the file")

        else:
            self.enableDisableUIEle(True)
            self.isRunning = False
            self.startBtn.setText("Start")

    def getConfigs(self):
        saved_config = []
        self.inputConf.clear()
        if str(self.inputType.currentText()) == "Movies":
            saved_config = os.listdir("Movies")
        elif str(self.inputType.currentText()) == "Books":
            saved_config = os.listdir("Books")
        
        if len(saved_config) > 0:
            self.inputConf.addItem("")
            for conf in saved_config:
                if not conf.startswith('.'):
                    self.inputConf.addItem(conf.replace(".json", ""))
            self.inputConf.show()
            self.lblConf.show()
        else:
            self.inputConf.hide()
            self.lblConf.hide()

    def selectConfig(self, value):
        if value == "":
            self.savedConfigFile = value
            self.configId.setText(value)
            self.inputPath.setText(value)
            self.outputPath.setText(value)
        else:
            self.configId.setText(value)
            self.generateConfigFile()
            with open(self.savedConfigFile) as json_file:
                config_data = json.load(json_file)
                self.inputPath.setText(config_data["input_path"])
                self.outputPath.setText(config_data["output_path"])

    def generateConfigFile(self):
        if self.configId.text() == "":
            now = datetime.now()
            self.configId.setText(now.strftime("%d%m%Y_%H%M%S"))
        if str(self.inputType.currentText()) == "Movies":
            self.savedConfigFile = "Movies/" + self.configId.text() + ".json"
        elif str(self.inputType.currentText()) == "Books":
            self.savedConfigFile = "Books/" + self.configId.text() + ".json"

    def saveAreasMarked(self):
        self.generateConfigFile()
        config_data = {"input_path": self.inputPath.text(), "output_path": self.outputPath.text()}
        with open(self.savedConfigFile, 'w') as outfile:
            json.dump(config_data, outfile)
        if self.configId.text() not in [self.inputConf.itemText(i) for i in range(self.inputConf.count())]:
            self.getConfigs()

    def inputTypeSelector(self, value):
        if value == "Movies":
            self.algorithms = MovieList()
        elif value == "Books":
            print("Books is Work in Progress")

        self.inputPath.setText("")
        self.outputPath.setText("")
        self.configId.setText("")
        self.savedConfigFile = ""
        self.errorLbl.hide()
        self.getConfigs()

    def fileSelector(self, type):
        if type == "in":
            win_name = 'Select a txt file'
            fileName = QtWidgets.QFileDialog.getOpenFileName(self, win_name, FILE_SAVE_LOCATION)
            self.inputPath.setText(fileName[0])
        elif type == "out":
            win_name = 'Select a txt file'
            fileName = QtWidgets.QFileDialog.getOpenFileName(self, win_name, FILE_SAVE_LOCATION)
            self.outputPath.setText(fileName[0])


app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
window = Ui()  # Create an instance of our class
app.exec_()  # Start the application