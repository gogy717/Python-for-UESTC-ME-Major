from PyQt5.QtWidgets import QApplication
import sys
from src.ServerGUI import ServerGUI

def run_gui():
    app = QApplication(sys.argv)
    window = ServerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_gui()
    