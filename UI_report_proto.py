import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,QThread
from PyQt5.QtGui import QPixmap, QIcon
import os
from pathlib import Path
from report import *

class Thread_report_table(QThread):
    def __init__(self, parent):     #parent means "self" of reportClass
        super().__init__(parent)
        self.parent=parent

    def run(self):
        for i in range(self.parent.row):
            self.parent.table1.setItem(i,3, QTableWidgetItem(self.parent.new_report[i+1][1]))
            self.parent.table1.setItem(i,4, QTableWidgetItem(self.parent.new_report[i+1][2]))
            self.parent.table1.setItem(i,5, QTableWidgetItem(self.parent.new_report[i+1][3]))
            self.parent.table1.setItem(i,6, QTableWidgetItem(self.parent.new_report[i+1][4]))
            self.parent.table1.setItem(i,7, QTableWidgetItem(self.parent.new_report[i+1][5]))

        '''
        x=Thread_report_table(self)
        x.start()
        '''

class Thread_click_img(QThread):
    def __init__(self, parent):     #parent means "self" of reportClass
        super().__init__(parent)
        self.parent=parent

    def run(self):
        index_ele=self.parent.table1.selectedIndexes()
        current_row=index_ele[0].row()
        
        try:
            self.parent.show_table_img(current_row, 1)

        except AttributeError:
            pass
        
        try:
            self.parent.show_table_img(current_row, 2)

        except AttributeError:
            pass

        #print("index_ele[0]:",index_ele[0])

        '''
        x=Thread_click_img(self)
        x.start()
        '''

class reportClass(QWidget):
    def __init__(self):
        super().__init__()

        appWidth = 1200
        appHeight = 800
        self.setWindowTitle('YOLO Reporting Tool')
        self.setGeometry(100, 100, appWidth, appHeight)
        self.setWindowIcon(QIcon(r"E:\Works\Data\etc\1629416.png"))

        self.text_org_dir=QLineEdit(self)
        self.text_result_dir=QLineEdit(self)

        self.btn_set_org_dir=QPushButton(self)
        self.btn_set_org_dir.setText("Select Original Dir")
        self.btn_set_org_dir.clicked.connect(self.set_org_dir)
        self.btn_set_org_dir.setStyleSheet("background-color: #cccccc")

        self.btn_set_result_dir=QPushButton(self)
        self.btn_set_result_dir.setText("Select Results Dir")
        self.btn_set_result_dir.clicked.connect(self.set_result_dir)
        self.btn_set_result_dir.setStyleSheet("background-color: #cccccc")


        self.btn_report=QPushButton(self)
        self.btn_report.setText("Report")
        self.btn_report.clicked.connect(self.report_n_save)
        self.btn_report.setStyleSheet("background-color: #cccccc")

        self.label_report_dir=QLineEdit(self)
        self.label_notice_report_dir=QLabel(self)
        self.label_notice_report_dir.setText("Reports saved in: ")

        self.label_report=QLabel(self)
        self.label_report.setText("report")
        self.label_report.setStyleSheet("background-color:white")
        self.label_report.setAlignment(Qt.AlignCenter)
        
        scroll_report=QScrollArea()
        self.text_report=QLabel(self)
        self.text_report.setStyleSheet("background-color:white")
        #self.text_report.setWordWrap(True)
        scroll_report.setWidget(self.text_report)
        scroll_report.setWidgetResizable(True)
        scroll_bar=scroll_report.horizontalScrollBar()
        scroll_bar.setSingleStep(1)
        scroll_bar.setPageStep(1)


        self.table1=QTableWidget(self)
        self.table1.setStyleSheet("background-color:white; border:1px solid black")
        self.table1.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
        self.table_label=["Original Images","Label file", "(YOLO)Result Images"]
        self.set_table_header(self.table_label,3)
        

        self.label_img1=QLabel(self)
        self.label_img1.setText("Select Images.")
        self.label_img1.setStyleSheet("background-color:white")
        self.label_img1.setAlignment(Qt.AlignCenter)
        self.label_img1.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
        #self.label_img1.setScaledContents(True)

        self.label_img2=QLabel(self)
        self.label_img2.setText("Select Images.")
        self.label_img2.setStyleSheet("background-color:white")
        self.label_img2.setAlignment(Qt.AlignCenter)
        self.label_img2.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
        #self.label_img2.setScaledContents(True)

        main_window=QGridLayout()
        window_left=QGridLayout()
        window_right_top=QGridLayout()
        window_right_bottom=QGridLayout()
        window_right=QGridLayout()

        
        window_left.addWidget(self.text_org_dir,1,0,1,4)
        window_left.addWidget(self.btn_set_org_dir,1,4,1,1)
        window_left.addWidget(self.text_result_dir,2,0,1,4)
        window_left.addWidget(self.btn_set_result_dir,2,4,1,1)
        window_left.addWidget(self.label_notice_report_dir,3,0,1,4)
        window_left.addWidget(self.label_report_dir,4,0,1,4)
        window_left.addWidget(self.btn_report,4,4,1,1)
        window_left.addWidget(self.table1, 5,0, 10,5)

        window_right_top.addWidget(self.label_img1, 0,0)
        window_right_top.addWidget(self.label_img2, 0,1)

        window_right_bottom.addWidget(self.label_report, 0,0,1,1)
        window_right_bottom.addWidget(scroll_report, 1,0,5,10)

        window_right.addLayout(window_right_top, 0,0,3,1)
        window_right.addLayout(window_right_bottom, 3,0,1,1)

        main_window.addLayout(window_left, 0,0, 1,1)
        main_window.addLayout(window_right, 0,1, 1,4)   ######(1,1) => left window resize x

        self.setLayout(main_window)

        self.img_ext = ["jpg", "gif", "bmp", "tif", "png","jpeg"]

        self.table1.itemClicked.connect(self.click_ele)

    
    def resizeEvent(self, event) : #override
        self.width=self.frameGeometry().width()
        self.height=self.frameGeometry().height()
        

    def set_org_dir(self):

        try:
            for i in range(self.row):
                self.table1.setItem(i,0, QTableWidgetItem(""))
                self.table1.setItem(i,1, QTableWidgetItem(""))

        except:
            pass

        dir_path=QFileDialog.getExistingDirectory(self,"Select Data Directory")
        #self.data_dir=dir_path
        self.dir_label=dir_path
        self.text_org_dir.setText(dir_path)

        if self.text_org_dir.text():

            org_img_list=[]

            org_list=os.listdir(dir_path)
            for ext in self.img_ext:
                for file in org_list:
                    if file.endswith(ext) or file.endswith(ext.upper()):
                        org_img_list.append(file)

            self.row=len(org_img_list)
            self.table1.setRowCount(self.row)

            org_txt_ox=[]
            self.org_txt_x_list=[]

            for i,org_img_name in enumerate(org_img_list):
                org_img_path=Path(org_img_name)
                org_file_name=org_img_path.stem
                org_txt_name=str(org_file_name)+".txt"
                org_txt_path=os.path.join(dir_path,org_txt_name)

                if os.path.exists(org_txt_path):
                    org_txt_ox.append("O")
                else:
                    org_txt_ox.append("X")
                    self.org_txt_x_list.append(i)


            for i in range(self.row):
                self.table1.setItem(i,0, QTableWidgetItem(org_img_list[i]))
                self.table1.setItem(i,1, QTableWidgetItem(org_txt_ox[i]))

        self.set_valid_img_list()

    def set_result_dir(self):

        try:

            for i in range(self.row):
                self.table1.setItem(i,2, QTableWidgetItem(""))

        except:
            pass

        dir_path=QFileDialog.getExistingDirectory(self,"Select Data Directory")
        self.result_dir=dir_path
        self.dir_result=dir_path
        self.text_result_dir.setText(dir_path)

        if  self.text_org_dir.text() and self.text_result_dir.text():

            result_img_list=[]

            result_list=os.listdir(dir_path)
            for ext in self.img_ext:
                for file in result_list:
                    if file.endswith(ext) or file.endswith(ext.upper()):
                        result_img_list.append(file)

            self.row=len(result_img_list)
            self.table1.setRowCount(self.row)

            for i in range(self.row):
                self.table1.setItem(i,2, QTableWidgetItem(result_img_list[i]))
        
        self.set_valid_img_list()

    
    def set_valid_img_list(self):

        

        if self.text_org_dir.text() and self.text_result_dir.text():

            self.table1.clear()
            self.table_label=["Original Images","Label file", "(YOLO)Result Images"]
            self.set_table_header(self.table_label,3)
            _, list_org_img, _, list_result_img=get_list(self.dir_label, self.dir_result)

            self.row=len(list_result_img)
            self.table1.setRowCount(self.row)

            for i in range(self.row):
                self.table1.setItem(i,0, QTableWidgetItem(list_org_img[i]))
                self.table1.setItem(i,1, QTableWidgetItem("O"))
                self.table1.setItem(i,2, QTableWidgetItem(list_result_img[i]))

        else:
            pass
        
    def click_ele(self):

        x2=Thread_click_img(self)
        x2.start()


    def show_table_img(self, current_row, index):

        if index==2:
            dir=self.report_dir
            img_box=self.label_img2
        elif index==1:
            dir=self.result_dir
            img_box=self.label_img1
        else:
            pass
        img_name=self.table1.item(current_row, 0)
        show_img=os.path.join(dir,img_name.text())
        self.my_pixmap=QPixmap(show_img)
        self.set_image(self.my_pixmap, img_box)

    def set_image(self, img, img_box):
        if img.width()==0:
            pass
        
        else:
            img=img.scaled(img_box.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        img_box.setPixmap(img)

    def set_table_header(self,table_label, table_col):
        self.table1.setColumnCount(table_col)
        self.table1.setHorizontalHeaderLabels(table_label) 
        self.header=self.table1.horizontalHeader()
        for i in range(table_col):
            self.header.setSectionResizeMode(i,QHeaderView.ResizeToContents)


    def report_n_save(self):
        

        if self.text_org_dir.text() and self.text_result_dir.text():

            report_dir,report1=report(self.dir_label, self.dir_result)
            self.report_dir=report_dir

            self.table_label2=self.table_label[:]
            self.table_label2.extend(["correct", "incorrect","miss","class:O", "class:X"])
            self.set_table_header(self.table_label2, 8)
            
            self.label_notice_report_dir.setText("Reports saved in: ")
            self.label_report_dir.setText(report_dir)
            self.label_report_dir.setStyleSheet("background-color:white;")
            
            self.new_report=[]
            self.text_report.setText(report1+"\n\nReports saved in: "+report_dir)
            report_list=report1.split("\n")
            for reports in report_list:
                report_result=reports.split(",")
                self.new_report.append(report_result)
            

            self.set_table_item()

        else:
            pass
    
    def set_table_item(self):
        x=Thread_report_table(self)
        x.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_window1 = reportClass()
    my_window1.show()
    
    app.exec_()

