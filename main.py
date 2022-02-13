import imp
import sys
from PyQt5.QtWidgets import *
import time
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from tensorflow.keras.models import load_model

import cv2
from PIL import Image
from keras.preprocessing import image
import numpy as np

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
        self.labelmain.setAlignment(QtCore.Qt.AlignCenter)
        self.labelmain.setMaximumHeight(50)
        self.labelmain.setText("Emotion detector")
        self.labelmain.setStyleSheet("background-color : #62524D;"
                                     "color : white")
        self.central.setStyleSheet("background-color : #9B8888;")
        font = QtGui.QFont('SansSerif', 20)
        self.labelmain.setFont(font)
        self.mainbox.addWidget(self.labelmain)

        self.chooseBtn = QPushButton()
        self.chooseBtn.setText('Выбрать изображение')
        self.chooseBtn.setFixedSize(350,32)
        self.chooseBtn.setStyleSheet("background-color : #B7ADA1;"
                                     "border-radius : 10px;"
                                     "border-bottom: 4px solid #6F665A")
        self.aboutBtn = QPushButton(self)
        self.aboutBtn.setText('О приложении')
        self.aboutBtn.setFixedSize(350, 32)
        self.aboutBtn.setStyleSheet("background-color : #B7ADA1;"
                                     "border-radius : 10px;"
                                    "border-bottom: 4px solid #6F665A")

        self.groupbox = QGroupBox()
        self.box1 = QHBoxLayout()
        self.groupbox.setFixedHeight(40)
        self.groupbox.setLayout(self.box1)
        self.box1.addWidget(self.aboutBtn)
        self.groupbox.setStyleSheet("border : 0px")

        self.groupbox1 = QGroupBox()
        self.box2 = QHBoxLayout()
        self.box2.addWidget(self.chooseBtn)
        self.groupbox1.setLayout(self.box2)
        self.groupbox1.setFixedHeight(40)
        self.groupbox1.setStyleSheet("border : 0px")

        self.groupbox2 = QGroupBox()
        self.queryLayout = QHBoxLayout()
        self.groupbox2.setLayout(self.queryLayout)
        self.groupbox2.setStyleSheet("background-image : url(icon.png);"
                                     "background-repeat : no-repeat;"
                                     "background-position : center;"
                                     "border : 0px")


        self.mainbox.addWidget(self.groupbox2)
        self.mainbox.addWidget(self.groupbox1)
        self.mainbox.addWidget(self.groupbox)


        self.chooseBtn.clicked.connect(self.openFileNameDialog)
        self.aboutBtn.clicked.connect(self.start)


    def start(self):
        self.groupbox2.setStyleSheet("")
        self.labelmain.setText("О приложении")
        self.labelabout = QLabel()
        self.labelabout.setAlignment(QtCore.Qt.AlignHCenter)
        self.labelabout.setText("Выполнили:\n"
                                "Дегтярев А.В.\n"
                                "Заморщикова Д.А.\n"
                                "Лотов А.Р.\n"
                                "Цель проекта:\n"
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
        self.menuBtn.setFixedSize(350, 32)
        self.menuBtn.setStyleSheet("background-color : #B7ADA1;"
                                    "border-radius : 10px;"
                                    "border-bottom: 4px solid #6F665A")
        self.groupbox3 = QGroupBox()
        self.box3 = QHBoxLayout()
        self.groupbox3.setFixedHeight(40)
        self.groupbox3.setLayout(self.box3)
        self.box3.addWidget(self.menuBtn)
        self.groupbox3.setStyleSheet("border : 0px")

        self.menuBtn.clicked.connect(self.createUI)
        self.mainbox.addWidget(self.groupbox3)


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
        self.resultBtn.setFixedSize(350, 32)
        self.resultBtn.setStyleSheet("background-color : #B7ADA1;"
                                   "border-radius : 10px;"
                                   "border-bottom: 4px solid #6F665A")
        self.groupbox4 = QGroupBox()
        self.box4 = QHBoxLayout()
        self.groupbox4.setFixedHeight(40)
        self.groupbox4.setLayout(self.box4)
        self.box4.addWidget(self.resultBtn)
        self.groupbox4.setStyleSheet("border : 0px")
        self.resultBtn.clicked.connect(self.result)
        self.mainbox.addWidget(self.groupbox4)

        self.menuBtn = QPushButton()
        self.menuBtn.setText('В главное меню')
        self.menuBtn.setFixedSize(350, 32)
        self.menuBtn.setStyleSheet("background-color : #B7ADA1;"
                                     "border-radius : 10px;"
                                     "border-bottom: 4px solid #6F665A")
        self.groupbox5 = QGroupBox()
        self.box5 = QHBoxLayout()
        self.groupbox5.setFixedHeight(40)
        self.groupbox5.setLayout(self.box5)
        self.box5.addWidget(self.menuBtn)
        self.groupbox5.setStyleSheet("border : 0px")
        self.mainbox.addWidget(self.groupbox5)
        self.menuBtn.clicked.connect(self.createUI)

    def result(self):
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.mainbox.addWidget(self.pbar)

        self.thread = Thread()
        self.thread._signal.connect(self.signal_accept)
        self.thread.start()

        #код вставить тут
        #путь к изображению хранится в path_to_image = self.queryimg
        #результат сохранить в переменной result в def signal_accept
        #load_model
        model = load_model('model')
        
        path_to_image = self.queryimg
        
        # Загрузка изображения
        image_cv2 = cv2.imread(path_to_image)

        # преобразуем изображение к оттенкам серого
        image_gray = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)

        # инициализировать распознаватель лиц (каскад Хаара по умолчанию)
        face_cascade = cv2.CascadeClassifier("haarcascade_fontalface_default.xml")

        # обнаружение всех лиц на изображении
        faces = face_cascade.detectMultiScale(image_gray)
        # печатать количество найденных лиц

        numfaces = 0
        img_crop
        # для всех обнаруженных лиц рисуем синий квадрат
        for x, y, width, height in faces:
            if (width-x)>20:
                cv2.rectangle(image_cv2, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
                numfaces+=1
                img = Image.open(path_to_image)
                img_crop = img.crop((x, y, x + width, y + height))
                
        img_crop = image.smart_resize((48,48))
        
        label_dict = {0:'Angry',1:'Disgust',2:'Fear',3:'Happy',4:'Neutral',5:'Sad',6:'Surprise'}
        img_crop = np.expand_dims(img_crop,axis = 0) #makes image shape (1,48,48)
        img_crop = img_crop.reshape(1,48,48,1)
        result = model.predict(img_crop)
        result = list(result[0])
        img_index = result.index(max(result))
        resulting = label_dict[img_index]




    
    
    def signal_accept(self, msg):
        self.pbar.setValue(int(msg))
        if self.pbar.value() == 99:
            self.pbar.setValue(100)
            result = "Сюда надо вставить результат"  # В виде строки
            self.resultBtn.setText(result)
            self.resultBtn.setDisabled(True)
            self.pbar.setVisible(False)
            return

class Thread(QThread):
    _signal = pyqtSignal(int)
    def __init__(self):
        super(Thread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.01)
            self._signal.emit(i)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())