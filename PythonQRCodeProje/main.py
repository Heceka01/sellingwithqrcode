from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication
from sekmegecis import *

app=QApplication([])
window=HesapTuruSecme()
window.show()
app.exec_()