import sys
from PyQt5.QtWidgets import QApplication

from GUI.GUI import ProductAnalyzer




def main():
    app = QApplication(sys.argv)
    analyzer = ProductAnalyzer()
    analyzer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
