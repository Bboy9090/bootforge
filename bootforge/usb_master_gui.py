import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class BootForge(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BootForge")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        welcome = QLabel("Welcome to BootForge!\nThis is your USB toolkit.")
        layout.addWidget(welcome)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BootForge()
    window.show()
    sys.exit(app.exec_())
