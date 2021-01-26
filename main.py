import sys  # sys потрібний для передачі argv в QApplication
from PyQt5 import QtWidgets, QtGui # бібліотеки для роботи
import design  #  наш конвертирований файл дизайна
import LTV_Analyzer
path = 'data/data_analytics.csv'
LTV_Analyzer1 = LTV_Analyzer.LTV_Analyzer(path)
counter = 0  # допоміжний рахувальник
count = 0 # допоміжний рахувальник
arr_names = LTV_Analyzer1.get_and_save_plots()# масив із назвами фотографій (твоя функція сюди мені їх кидає)


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    
    
    def __init__(self):
        # потрібно для доступа до змінних і методів
        super().__init__()
        self.setupUi(self)  # для ініціалізації нашого дизайну
        self.initUI() 
      
    

    def initUI(self):# функція для передачі дій під час нажаття кнопок
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_7.setEnabled(False)
        self.pushButton.clicked.connect(self.active_7_push) 
        self.pushButton_2.clicked.connect(self.active_3_push)
        self.pushButton_3.clicked.connect(self.browse_file)
        self.pushButton_4.clicked.connect(self.show_image)
        self.pushButton_5.clicked.connect(self.photo_left)
        self.pushButton_6.clicked.connect(self.photo_right)
        self.pushButton_7.clicked.connect(self.analyze)
      




    def deactivate_3_push(self):   #деактивація browse
        self.pushButton_3.setEnabled(False)

    def active_3_push(self):# Активація кнопки browse
        self.pushButton_3.setEnabled(True)
        


    def active_7_push(self):# Активація кнопки проанілузвати та деактивація browse
        self.pushButton_7.setEnabled(True)
        self.deactivate_3_push()
        global path, LTV_Analyzer1
        path = 'data/data_analytics.csv'
        LTV_Analyzer1 = LTV_Analyzer.LTV_Analyzer(path)
    

    def analyze(self):
        global path
        result = LTV_Analyzer1.get_LTV()
        self.LTV_print(result[0])

    

    def showImage(self, number):# функція вставки фото
        global counter, arr_names
        if counter != -1 and counter != len(arr_names): # перевірка чи ми не вийшли за границі масива
            self.pushButton_5.setEnabled(True)#включення перемикачів
            self.pushButton_6.setEnabled(True)
            self.labelImage.setScaledContents(True)
            self.labelImage.setPixmap(QtGui.QPixmap(arr_names[number]))

    


    def show_image(self):# функція для кнопок показати менше і більше
        global count, arr_names
        if count == 0:# перевірка умови
            self.labelImage.setScaledContents(True) # фотографія на всю рамку
            self.labelImage.setPixmap(QtGui.QPixmap(arr_names[0])) # показ першого елемента
            self.pushButton_4.setText("Показати менше")
            self.pushButton_5.setEnabled(True)#активація перемикачів
            self.pushButton_6.setEnabled(True)

            count = 1 
        else:
            self.labelImage.clear()#очистка поля
            self.pushButton_4.setText("Показати більше")
            self.pushButton_5.setEnabled(False)# вимкнення перемикачів
            self.pushButton_6.setEnabled(False)
            count = 0


    def LTV_print(self, result):#функція яка показує результат
        self.pushButton_3.setEnabled(False) # вимкнення кнопки browse
        self.listWidget.clear()  # На случай, если в списке уже есть элементы
        self.listWidget.addItem(str(result)) # виведення результату лтв
        self.pushButton_4.setEnabled(True) # активація кнопки показати більше менше


    def browse_file(self): # ось  ця функція повертає шлях до вибраного файла
        self.active_7_push()
        global LTV_Analyzer1, path
        filename = QtWidgets.QFileDialog.getOpenFileName() #взяття шляху у вибраного файла
        path = filename[0]
        self.listWidget_2.clear()  # На випадок якщо в списку є елементи
        self.listWidget_2.addItem(filename[0])   # добавити шлях до файлу в listWidget_2
        LTV_Analyzer1 = LTV_Analyzer.LTV_Analyzer(path)
        


       

    
    def photo_left(self): #функція для лівого перемикача
        global counter, arr_names
        if counter == 0: # перевірка чи ми не вийшли за границі масива
            self.pushButton_5.setEnabled(False)#вимкнення лівого перемикача


        else:
            self.pushButton_5.setEnabled(True)#вімкнення лівого перемикача
            counter -= 1 #зменшуємо рахівник
            self.showImage(counter)


    def photo_right(self):
        global counter, arr_names
        if counter == len(arr_names) - 1: # перевірка чи ми не вийшли за границі масива
            self.pushButton_6.setEnabled(False)#вимкнення правого перемикача

        else:
            self.pushButton_6.setEnabled(True)#вімкнення правого перемикача
            counter += 1#зменшуємо рахівник
            self.showImage(counter)
            

def main():
    app = QtWidgets.QApplication(sys.argv)  # новий екземпляр QApplication
    window = ExampleApp()  #об'єкт класа ExampleApp
    window.show()  # показуєм вікно
    app.exec_()  # запускаємо додаток

if __name__ == '__main__':  #Якщо запускаємо файл на пряму, а не імпортуємо
    main()  # то запускаємо функцію main