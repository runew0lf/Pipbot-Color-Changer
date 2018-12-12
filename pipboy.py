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

prefs_ini = f"{buf.value}\\My Games\\Fallout 76\\Fallout76Prefs.ini"
backup_ini = f"{buf.value}\\My Games\\Fallout 76\\Fallout76Prefs.bkp"
custom_ini = f"{buf.value}\\My Games\\Fallout 76\\Fallout76Custom.ini"

if os.path.isfile(backup_ini) is False:
    shutil.copyfile(prefs_ini, backup_ini)

if os.path.isfile(custom_ini) is False:
    open(custom_ini, 'a').close()

def percentage(part):
    return round(float(part)/float(255), 4)


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 800, 400)
        self.setWindowTitle("Fo76 PipBoy Color Changer")
        self.setWindowIcon(QIcon('logo.png'))
        self.home()

    def home(self):
        self.btnPipBoy = QPushButton("Set PipBoy Color", self)
        self.btnPipBoy.move(50, 150)

        self.btnQuickBoy = QPushButton("Set QuickBoy Color", self)
        self.btnQuickBoy.move(50, 190)

        self.dlgColor = QColorDialog(self)
        self.dlgColor.setWindowFlags(
            self.dlgColor.windowFlags() & ~Qt.Dialog)
        self.dlgColor.setOptions(
            QColorDialog.DontUseNativeDialog | QColorDialog.NoButtons)
        self.dlgColor.move(250, 0)

        self.text = QTextEdit(self)
        self.text.setFixedSize(200, 100)
        self.text.move(10, 10)
        self.text.setReadOnly(True)

        self.btnPipBoy.clicked.connect(self.set_pipboy_color)
        self.btnQuickBoy.clicked.connect(self.set_quickboy_color)
        
        self.show()

    def set_pipboy_color(self):
        color = self.dlgColor.currentColor()
        r, g, b, a = color.getRgb()
        self.text.setPlainText(
            f"[Pipboy]\nfPipboyEffectColorR={percentage(r)}\nfPipboyEffectColorG={percentage(g)}\nfPipboyEffectColorB={percentage(b)}")

        with open(prefs_ini, "r") as fh:
            inifile = fh.read().splitlines()

        writefh = open(prefs_ini, "w")
        for lines in inifile:
            if "fPipboyEffectColorR" in lines:
                lines = f"fPipboyEffectColorR={percentage(r)}"
            if "fPipboyEffectColorG" in lines:
                lines = f"fPipboyEffectColorG={percentage(g)}"
            if "fPipboyEffectColorB" in lines:
                lines = f"fPipboyEffectColorB={percentage(b)}"
            writefh.write(lines + '\n')
        writefh.close()
    
    def set_quickboy_color(self):
        color = self.dlgColor.currentColor()
        r, g, b, a = color.getRgb()
        self.text.setPlainText(
            f"[Pipboy]\nfQuickBoyEffectColorR={percentage(r)}\nfQuickBoyEffectColorG={percentage(g)}\nfQuickBoyEffectColorB={percentage(b)}")     
       
        with open(custom_ini, "r") as fh:
            inifile = fh.read().splitlines()

        if any("fQuickBoyEffect" in s for s in inifile):
            writefh = open(custom_ini, "w")
            for lines in inifile:
                if "nfQuickBoyEffectColorR" in lines:
                    lines = f"nfQuickBoyEffectColorR={percentage(r)}"
                if "nfQuickBoyEffectColorG" in lines:
                    lines = f"nfQuickBoyEffectColorG={percentage(g)}"
                if "nfQuickBoyEffectColorB" in lines:
                    lines = f"nfQuickBoyEffectColorB={percentage(b)}"
                writefh.write(lines + '\n')
            writefh.close()
        else:
            writefh = open(custom_ini, "w")
            writefh.write("[Pipboy]\n")
            writefh.write(f"nfQuickBoyEffectColorR={percentage(r)}\n")          
            writefh.write(f"nfQuickBoyEffectColorG={percentage(g)}\n")
            writefh.write(f"nfQuickBoyEffectColorB={percentage(b)}\n")
            for lines in inifile:
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
