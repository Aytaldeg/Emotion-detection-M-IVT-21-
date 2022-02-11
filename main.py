import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'M-IVT-21 Group3 app'
        self.left = 200
        self.top = 200
        self.width = 350
        self.height = 500
        self.queryimg=None
        self.dir_path=None #"C:/Users/vovaz/Documents/example/Image-Classifier/images/001_0007.jpg"
        self.initUI()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.threadpool = QtCore.QThreadPool()

    def initUI(self):
        self.central=QWidget()
        self.setCentralWidget(self.central)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.mainbox=QVBoxLayout()
        self.central.setLayout(self.mainbox)
        self.createUI()
        self.show()


    def createUI(self):
        for i in reversed(range(self.mainbox.count())):
            self.mainbox.itemAt(i).widget().setParent(None)

        self.labelmain = QLabel()
        self.labelmain.setAlignment(QtCore.Qt.AlignHCenter)
        self.labelmain.setMaximumHeight(50)
        self.labelmain.setText("Emotion detector")
        self.central.setStyleSheet("background-color : #9B8888;")
        font = QtGui.QFont('SansSerif', 20)
        self.labelmain.setFont(font)

        self.mainbox.addWidget(self.labelmain)

        self.chooseBtn = QPushButton()
        self.chooseBtn.setText('Выбрать изображение')
        self.chooseBtn.setFixedSize(350,32)
        self.chooseBtn.setStyleSheet("background-color : #CBBFAF;"
                                     "border-radius : 10px;")
        self.aboutBtn = QPushButton(self)
        self.aboutBtn.setText('О приложении')


        self.groupbox2 = QGroupBox()
        self.queryLayout = QHBoxLayout()
        self.groupbox2.setLayout(self.queryLayout)
        self.groupbox2.setStyleSheet("background-image : url(icon.png);"
                                     "background-repeat : no-repeat;"
                                     "background-position : center;"
                                     "border : 0px")


        self.mainbox.addWidget(self.groupbox2)
        self.mainbox.addWidget(self.chooseBtn)
        self.mainbox.addWidget(self.aboutBtn)

        self.chooseBtn.clicked.connect(self.openFileNameDialog)
        self.aboutBtn.clicked.connect(self.start)


    def start(self):
        self.groupbox2.setStyleSheet("")
        self.labelmain.setText("О приложении")
        self.labelabout = QLabel()
        self.labelabout.setAlignment(QtCore.Qt.AlignHCenter)
        self.labelabout.setText("Цель проекта:\n"
                                "Разработать модель нейронной сети \n"
                                "по распознаванию эмоций по \n"
                                "фотографиям и разработать к нему\n"
                                "графический интерфейс.\n"
                                "\n"
                                "\n"
                                "Основные функциональные особенности\n"
                                "и свойства:\n"
                                "1) Определение и выделение лица\n"
                                "на фотографиях, если на фотографии\n"
                                " не только лицо.\n" 
                                "2) Особенность распознавать 7 видов\n"
                                " эмоций человека по выражениям лица:\n"
                                "Злость, отвращение, страх, счастье,\n"
                                " нейтральный, грусть, удивление.\n "
                                "3) Распознавания и выделения эмоций\n"
                                "и количественный анализ различных эмоций\n"
                                "(добавить цвета выделения и вывод количества).")
        font = QtGui.QFont('SansSerif', 10)
        self.labelabout.setFont(font)
        self.queryLayout.addWidget(self.labelabout)
        self.groupbox2.setStyleSheet("border : 0px")
        self.chooseBtn.setVisible(False)
        self.aboutBtn.setVisible(False)
        self.menuBtn = QPushButton()
        self.menuBtn.setText('В главное меню')
        self.menuBtn.clicked.connect(self.createUI)
        self.mainbox.addWidget(self.menuBtn)


    def openFileNameDialog(self): ## USE THIS TO GET PATH OF QUERY IMAGE...
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select Image", "","Image files (*.jpg *.gif *.png)")
        self.groupbox2.setStyleSheet("")
        if fileName:
            self.queryimg = fileName
            self.im1 = QtGui.QPixmap(fileName).scaled(400, 300, QtCore.Qt.KeepAspectRatio)
            self.label1 = QLabel()
            self.label1.setAlignment(QtCore.Qt.AlignCenter)
            self.label1.setPixmap(self.im1)
            if self.queryLayout.count()==0:
                self.queryLayout.addWidget(self.label1)
            else:
                self.queryLayout.itemAt(0).widget().setParent(None)
                self.queryLayout.addWidget(self.label1)



        self.groupbox2.setStyleSheet("border : 0px")
        self.chooseBtn.setVisible(False)
        self.aboutBtn.setVisible(False)
        self.resultBtn = QPushButton()
        self.resultBtn.setText('Результат')
        self.resultBtn.clicked.connect(self.result)
        self.mainbox.addWidget(self.resultBtn)
        self.menuBtn = QPushButton()
        self.menuBtn.setText('В главное меню')
        self.menuBtn.clicked.connect(self.createUI)
        self.mainbox.addWidget(self.menuBtn)

    def result(self):
        self.resultBtn.setText("Сюда надо вставить результат")
        self.resultBtn.setDisabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())