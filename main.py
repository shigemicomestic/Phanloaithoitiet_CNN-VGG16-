import sys
import PIL.Image
import numpy as np
from PIL import Image, ImageOps
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from keras.models import load_model
from Newtest import Ui_MainWindow

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        # Khai bao nut load
        self.uic.btnload.clicked.connect(self.linkto)
        # Khai bao nut phan loai
        self.uic.btnPhanTich.clicked.connect(self.Scanpic)

    def Scanpic(self):
        try:
            # Load the model
            model = load_model('Weather_80_20.h5')
            # Load ảnh từ link
            image = Image.open(linkchange)
            # Khai báo size ảnh
            size = (150, 150)
            # Fit ảnh theo kích cỡ model
            image = ImageOps.fit(image, size, method=0, bleed=0.0, centering=(0.5, 0.5))
            # Chuẩn ảnh về dạng array
            image_array = np.asarray(image)
            # Chia mảng cho 255.0
            normalized_image_array = (image_array.astype(np.float32) / 255.0)
            # Tạo biến data với mảng 4 chiều
            data = np.ndarray(shape=(1, 150, 150, 3), dtype=np.float32)
            # Lấy biến đầu trong mảng
            data[0] = normalized_image_array
            prediction = model.predict(data)
            print(prediction)
            # Khai báo thư viện thời tiết
            name = ['Cloudy', 'Foggy', 'Rainy', 'Shine', 'Sunrise']
            position_1 = prediction.argmax()
            # Tìm số lớn nhất trong mảng
            max_value_1 = np.amax(prediction)
            # Lấy tên thời tiết
            self.uic.lblkq.setText(name[position_1])
            # Lấy phần trăm chính xác
            self.uic.lblPhanTram.setText(str(round(max_value_1 * 100, 2)) + ' %')
        except:
            self.uic.lblkq.setText('Không nhận diện được hình ảnh !')
            self.uic.lblPhanTram.setText('Độ chính xác : 0%')
            print('Không nhận diện được')

    def linkto(self):
        # Tim duong dan
        link = QFileDialog.getOpenFileName(filter='*.jpg *.png *.jpeg')
        # load hinh len
        self.uic.imageload.setPixmap(QPixmap(link[0]))
        # hien link hinh
        self.uic.lineEdit.setText(link[0])
        # lay link hinh tren edit text
        global linkchange
        linkpic = self.uic.lineEdit.text()
        # thay the ky tu link
        linkchange = linkpic.replace('/', '//')

    def show(self):
        self.main_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
