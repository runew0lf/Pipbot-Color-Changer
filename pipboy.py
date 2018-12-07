import ctypes.wintypes
import os.path
import shutil
import sys


from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

CSIDL_PERSONAL = 5       # My Documents
SHGFP_TYPE_CURRENT = 0   # Get current, not default value

buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(
    None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
fpath = f"{buf.value}\\My Games\\Fallout 76\\Fallout76Prefs.ini"
backuppath = f"{buf.value}\\My Games\\Fallout 76\\Fallout76Prefs.bkp"

if os.path.isfile(backuppath) is False:
    shutil.copyfile(fpath, backuppath)  

def percentage(part):
    return round(float(part)/float(255), 4)


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 800, 400)
        self.setWindowTitle("Fo76 PipBoy Color Editor")
        self.setWindowIcon(QIcon('logo.png'))
        self.home()

    def home(self):
        self.button = QPushButton("Set Color", self)
        self.button.move(50, 150)
        self.color_dialog = QColorDialog(self)
        self.color_dialog.setWindowFlags(
            self.color_dialog.windowFlags() & ~Qt.Dialog)
        self.color_dialog.setOptions(
            QColorDialog.DontUseNativeDialog | QColorDialog.NoButtons)
        self.color_dialog.move(250, 0)

        self.text = QTextEdit(self)
        self.text.setFixedSize(200, 100)
        self.text.move(10, 10)
        self.text.setReadOnly(True)

        self.button.clicked.connect(self.color_picker)
        self.show()

    def color_picker(self):
        color = self.color_dialog.currentColor()
        r, g, b, a = color.getRgb()
        self.text.setPlainText(
            f"[Pipboy]\nfPipboyEffectColorR={percentage(r)}\nfPipboyEffectColorG={percentage(g)}\nfPipboyEffectColorB={percentage(b)}")

        with open(fpath, "r") as fh:
            inifile = fh.read().splitlines()

        writefh = open(fpath, "w")
        for lines in inifile:
            if "fPipboyEffectColorR" in lines:
                lines = f"fPipboyEffectColorR={percentage(r)}"
            if "fPipboyEffectColorG" in lines:
                lines = f"fPipboyEffectColorG={percentage(g)}"
            if "fPipboyEffectColorB" in lines:
                lines = f"fPipboyEffectColorB={percentage(b)}"
            writefh.write(lines + '\n')
        writefh.close()


def run():
    app = QApplication(sys.argv)
    GUI = Window()
    try:
        sys.exit(app.exec_())
    except:
        pass


run()
