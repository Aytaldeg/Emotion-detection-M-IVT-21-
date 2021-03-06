import imp
import sys
from PyQt5.QtWidgets import *
import time
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from pip import main
from tensorflow.keras.models import load_model

import cv2
from PIL import Image
from keras.preprocessing import image
import numpy as np
from skimage import io

mainresult = ""

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
        
        
        # Добаление данных
        prototxt_path = "./SSD/deploy.prototxt.txt"
        model_path = "./SSD/res10_300x300_ssd_iter_140000_fp16.caffemodel"

        # загрузим модель Caffe
        modelssd = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

        # читаем изображение
        img = io.imread(path_to_image)
        # получаем ширину и высоту изображения
        h, w = img.shape[:2]

        # предварительная обработка: изменение размера и вычитание среднего
        blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104.0, 177.0, 123.0))

        # устанавливаем на вход нейронной сети изображение
        modelssd.setInput(blob)
        # выполняем логический вывод и получаем результат
        output = np.squeeze(modelssd.forward())

        print(output.shape[0])

        font_scale = 1.0
        for i in range(0, output.shape[0]):
            # получить уверенность
            confidence = output[i, 2]
            # если достоверность выше 50%, то нарисуйте окружающий прямоугольник
            if confidence > 0.5:
                # получить координаты окружающего блока и масштабировать их до исходного изображения
                box = output[i, 3:7] * np.array([w, h, w, h])
                # преобразовать в целые числа
                start_x, start_y, end_x, end_y = box.astype(np.int)
                # рисуем прямоугольник вокруг лица
                cv2.rectangle(img, (start_x, start_y), (end_x, end_y), color=(255, 0, 0), thickness=2)
                # также нарисуем текст
                cv2.putText(img, f"{confidence*100:.2f}%", (start_x, start_y-5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), 2)

                x = (start_x + end_x) / 2
                y = (start_y + end_y) / 2 

                if end_x - start_x < end_y - start_y:
                    weith = end_x - start_x
                else: weith = end_y - start_y  

                weith = weith * 0.5

                print("----------------------------------------------------------------")
                print(box)

                img = Image.open(path_to_image)
                img_crop = img.crop((x - weith, y - weith, x + weith, y + weith))
                img_crop.save("testing.jpg", quality=100)
                
        img = image.load_img("./testing.jpg",target_size = (48,48),color_mode = "grayscale")
        img = np.array(img)
        label_dict = {0:'Злость',1:'Отвращение',2:'Страх',3:'Радость',4:'Нейтральный',5:'Грустный',6:'Удивление'}
        img = np.expand_dims(img,axis = 0) #makes image shape (1,48,48)
        img = img.reshape(1,48,48,1)
        result = model.predict(img)
        result = list(result[0])
        img_index = result.index(max(result))
        global mainresult
        mainresult = label_dict[img_index]


    def signal_accept(self, msg):
        self.pbar.setValue(int(msg))
        if self.pbar.value() == 99:
            self.pbar.setValue(100)
            result = mainresult # В виде строки
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