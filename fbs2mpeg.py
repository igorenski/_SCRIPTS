import sys
import os 
import time
from os.path import expanduser
import subprocess
from PyQt5 import QtWidgets
import fbs2mpeg_gui

input_files = None
output_path = expanduser("~")
number_of_files = None

class ConverterGUI(QtWidgets.QMainWindow, fbs2mpeg_gui.Ui_fbs2mpeg):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.listWidget.clear()
        self.btn_input_files.clicked.connect(self.browse_input_files)
        self.btn_output_path.clicked.connect(self.browse_output_path)
        self.btn_run.clicked.connect(self.run)
        
    def browse_input_files(self):
        self.listWidget.clear()
        global input_files
        global number_of_files
        input_files , checking = QtWidgets.QFileDialog.getOpenFileNames(None, "Select files", "/home/","All Files (*)")
        if checking:
            self.listWidget.addItem('File list:')
            number_of_files = len(input_files)
            for i in input_files:
                if i:
                    get_fname_only_1 = os.path.basename(i)
                    self.listWidget.addItem(get_fname_only_1)
        else:
            self.listWidget.addItem('No files have been selected')

    def browse_output_path(self):
        global output_path
        output_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose a directory to save")
        if output_path:
            self.listWidget.addItem('Files will be saved to:')
            self.listWidget.addItem(output_path)
        else:
            output_path = expanduser("~")
            self.listWidget.addItem('No directory selected, files will be saved to:')
            self.listWidget.addItem(output_path)
        
    def run(self):
        time.sleep(1)
        if input_files:
            self.progressBar.setValue(5)
            counter = 0
            for i in input_files:
                get_fname_only_2 = os.path.basename(i)
                output_file = output_path + '/' + get_fname_only_2 + '.mkv'
                counter += 1
                rfbproxy = subprocess.Popen(["/bin/rfbproxy","-x", i], stdout = subprocess.PIPE)
                ppmtoy4m = subprocess.Popen(["/bin/ppmtoy4m","-S","420mpeg2","-F","24000:1001"], stdin=rfbproxy.stdout, stdout=subprocess.PIPE)
                ffmpeg = subprocess.Popen(["/bin/ffmpeg",
                                           "-y",
                                           "-i","pipe:",
                                           output_file], stdin=ppmtoy4m.stdout)
                pipe_output = ffmpeg.communicate()[0]
                self.listWidget.addItem(get_fname_only_2 + ' - ok')
                self.progressBar.setValue(100*counter/number_of_files)
        else:
             self.listWidget.addItem('No files have been selected')
                
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ConverterGUI()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
