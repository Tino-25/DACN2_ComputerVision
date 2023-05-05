from PyQt5.QtWidgets import QApplication, QDialog, QProgressBar, QVBoxLayout, QProgressDialog
import time

class Example(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.progress = QProgressBar(self)
        self.progress.setMinimum(0)
        self.progress.setMaximum(0)
        vbox = QVBoxLayout()
        vbox.addWidget(self.progress)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 250, 150)
        self.show()

    def run(self):
        dialog = QProgressDialog(self)
        dialog.setLabelText("Loading...")
        dialog.setRange(0, 0)
        dialog.show()
        for i in range(101):
            time.sleep(0.1) # giả lập quá trình tiến trình
            dialog.setValue(i)
        dialog.close()

if __name__ == '__main__':
    app = QApplication([])
    ex = Example()
    ex.run()
    app.exec_()