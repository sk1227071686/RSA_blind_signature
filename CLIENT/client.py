

#导入的模块
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtCore import QStringListModel,QDate,Qt
import sys
import os
sys.path.append('..')
from CLIENT.packages.encry_module import *
from CLIENT.packages.commen_method import *
from Ui_login_frame import *
import string,pickle
from pickle import dumps,loads
from uuid import uuid4
from PyQt5.QtGui import QPixmap




#读取认证服务器的公钥
with open(os.getcwd()+r'\keys\key1\Server_rsa_pub.pem','rb') as f:
    (lastModified1,e,n)=f.read()[31:-24].split(b'**^.^**')
(e,n)=map(bytes_to_int,(e,n))

#主窗口
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(751, 531)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_login = QtWidgets.QFrame(self.centralwidget)
        self.frame_login.setGeometry(QtCore.QRect(0, 0, 751, 531))
        self.frame_login.setStyleSheet("background-color: rgb(255, 170, 127);border-color: rgb(170, 85, 0);")
        self.frame_login.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_login.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_login.setObjectName("frame_login")

        self.showing_frame = self.frame_login
        self.showing_frame.setVisible(True)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame_login)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(330, 210, 231, 101))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit_userName = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.textEdit_userName.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_userName.setObjectName("textEdit_userName")
        self.verticalLayout.addWidget(self.textEdit_userName)
        self.plainTextEdit_passwd = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.plainTextEdit_passwd.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.plainTextEdit_passwd.setObjectName("plainTextEdit_passwd")
        self.verticalLayout.addWidget(self.plainTextEdit_passwd)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.frame_login)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(200, 210, 101, 151))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_userName = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_userName.setStyleSheet("")
        self.label_userName.setObjectName("label_userName")
        self.label_login = QtWidgets.QLabel(self.frame_login)
        self.label_login.setStyleSheet('font: 75 24pt "Arial";')
        self.label_login.setObjectName("label_login")
        self.label_login.setText('登录')
        self.label_login.setGeometry(QtCore.QRect(320, 60, 121, 61))
        self.label_login_msg = QtWidgets.QLabel(self.frame_login)
        self.label_login_msg.setStyleSheet('font: 75 10pt "Microsoft YaHei UI";')
        self.label_login_msg.setObjectName("label_login_msg")
        self.label_login_msg.setText('')
        self.label_login_msg.setGeometry(QtCore.QRect(290,160,281,31))
        self.verticalLayout_2.addWidget(self.label_userName)
        self.label_passwd = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_passwd.setObjectName("label_passwd")
        self.verticalLayout_2.addWidget(self.label_passwd)
        self.label_chapter = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_chapter.setObjectName("label_chapter")
        self.verticalLayout_2.addWidget(self.label_chapter)
        self.graphicsView_Chapter = QtWidgets.QLabel(self.frame_login)
        self.graphicsView_Chapter.setGeometry(QtCore.QRect(420, 320, 141, 41))
        self.graphicsView_Chapter.setObjectName("graphicsView_Chapter")
        self.pushButton_login = QtWidgets.QPushButton(self.frame_login)
        self.pushButton_login.setGeometry(QtCore.QRect(380, 380, 121, 41))
        self.pushButton_login.setObjectName("pushButton_login")
        self.pushButton_login.setText('登录')
        self.textEdit = QtWidgets.QTextEdit(self.frame_login)
        self.textEdit.setGeometry(QtCore.QRect(330, 320, 81, 41))
        self.textEdit.setObjectName("textEdit")
        self.frame_menu = QtWidgets.QFrame(self.centralwidget)
        self.frame_menu.setGeometry(QtCore.QRect(0, 0, 751, 531))
        self.frame_menu.setStyleSheet("background-color: rgb(170, 170, 127);")
        self.frame_menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_menu.setObjectName("frame_menu")

        self.frame_menu.setVisible(False)
        self.label = QtWidgets.QLabel(self.frame_menu)
        self.label.setGeometry(QtCore.QRect(330, 60, 61, 41))
        self.label.setStyleSheet("font: 75 18pt \"Arial\";")
        self.label.setObjectName("label")
        self.pushButton_startVoting = QtWidgets.QPushButton(self.frame_menu)
        self.pushButton_startVoting.setGeometry(QtCore.QRect(270, 140, 191, 51))
        self.pushButton_startVoting.setObjectName("pushButton_startVoting")
        self.pushButton_startVoting.clicked.connect(self.start_voting)
        self.pushButton_createVoting = QtWidgets.QPushButton(self.frame_menu)
        self.pushButton_createVoting.setGeometry(QtCore.QRect(270, 220, 191, 51))
        self.pushButton_createVoting.setObjectName("pushButton_createVoting")
        self.pushButton_createVoting.clicked.connect(self.create_voting)
        self.pushButton_viewResults = QtWidgets.QPushButton(self.frame_menu)
        self.pushButton_viewResults.setGeometry(QtCore.QRect(270, 300, 191, 51))
        self.pushButton_viewResults.setObjectName("pushButton_viewResults")
        self.pushButton_viewResults.clicked.connect(self.viewResults)
        self.pushButton_exit = QtWidgets.QPushButton(self.frame_menu)
        self.pushButton_exit.setGeometry(QtCore.QRect(272, 377, 191, 51))
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.frame_voting_list = QtWidgets.QFrame(self.centralwidget)
        self.frame_voting_list.setGeometry(QtCore.QRect(0, 0, 751, 531))
        self.frame_voting_list.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.frame_voting_list.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_voting_list.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_voting_list.setObjectName("frame_voting_list")

        self.frame_voting_list.setVisible(False)
        self.pushButton_optionChose = QtWidgets.QPushButton(self.frame_voting_list)
        self.pushButton_optionChose.setGeometry(QtCore.QRect(300, 490, 93, 28))
        self.pushButton_optionChose.setObjectName("pushButton_optionChose")
        self.pushButton_optionChose.setText('投票')
        self.pushButton_optionChose.clicked.connect(self.vote)
        self.pushButton_optionChose.setVisible(False)
        self.label_2 = QtWidgets.QLabel(self.frame_voting_list)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 691, 81))
        self.label_2.setStyleSheet("font: 75 9pt \"Arial\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame_voting_list)
        self.label_3.setGeometry(QtCore.QRect(290, 20, 131, 31))
        self.label_3.setStyleSheet("font: 75 18pt \"Arial\";")
        self.label_3.setObjectName("label_3")

        self.frame_startVoting = QtWidgets.QFrame(self.centralwidget)
        self.frame_startVoting.setGeometry(QtCore.QRect(0, 0, 751, 531))
        self.frame_startVoting.setStyleSheet("background-color: rgb(255, 183, 155);")
        self.frame_startVoting.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_startVoting.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_startVoting.setObjectName("frame_startVoting")

        self.frame_startVoting.setVisible(False)
        self.label_inputVotingId = QtWidgets.QLabel(self.frame_startVoting)
        self.label_inputVotingId.setGeometry(QtCore.QRect(260, 100, 191, 71))
        self.label_inputVotingId.setStyleSheet("font: 75 18pt \"Arial\";")
        self.label_inputVotingId.setObjectName("label_inputVotingId")
        self.label_inputVotingId.setText('请输入投票ID：')
        self.lineEdit = QtWidgets.QLineEdit(self.frame_startVoting)
        self.lineEdit.setGeometry(QtCore.QRect(220, 210, 271, 81))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 24pt \"Arial\";")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_votingID = QtWidgets.QPushButton(self.frame_startVoting)
        self.pushButton_votingID.setGeometry(QtCore.QRect(290, 340, 141, 51))
        self.pushButton_votingID.setObjectName("pushButton_votingID")
        self.pushButton_votingID.setText('继续')
        self.pushButton_votingID.clicked.connect(self.show_options)
        self.frame_voteSuccess = QtWidgets.QFrame(self.centralwidget)
        self.frame_voteSuccess.setGeometry(QtCore.QRect(0, 0, 751, 531))
        self.frame_voteSuccess.setStyleSheet("background-color: rgb(255, 206, 57);")
        self.frame_voteSuccess.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_voteSuccess.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_voteSuccess.setObjectName("frame_voteSuccess")

        self.frame_voteSuccess.setVisible(False)
        self.label_4 = QtWidgets.QLabel(self.frame_voteSuccess)
        self.label_4.setGeometry(QtCore.QRect(30, 180, 661, 101))
        self.label_4.setStyleSheet("font: 75 28pt \"Arial\";")
        self.label_4.setObjectName("label_4")
        self.frame_createVotingAddTitle = QtWidgets.QFrame(self.centralwidget)
        self.frame_createVotingAddTitle.setGeometry(QtCore.QRect(0, 0, 751, 531))
        self.frame_createVotingAddTitle.setStyleSheet("background-color: rgb(255, 239, 213);")
        self.frame_createVotingAddTitle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_createVotingAddTitle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_createVotingAddTitle.setObjectName("frame_createVotingAddTitle")

        self.frame_createVotingAddTitle.setVisible(False)
        self.label_5 = QtWidgets.QLabel(self.frame_createVotingAddTitle)
        self.label_5.setGeometry(QtCore.QRect(220, 70, 321, 81))
        self.label_5.setStyleSheet("font: 75 24pt \"Arial\";")
        self.label_5.setObjectName("label_5")
        self.label_5.setText('请输入投票标题：')
        self.label_15 = QtWidgets.QLabel(self.frame_createVotingAddTitle)
        self.label_15.setGeometry(QtCore.QRect(70, 360, 171, 51))
        self.label_15.setStyleSheet('font: 75 14pt "Arial";')
        self.label_15.setObjectName("label_15")
        self.label_15.setText('投票截止时间：')
        self.textEdit_2 = QtWidgets.QTextEdit(self.frame_createVotingAddTitle)
        self.textEdit_2.setGeometry(QtCore.QRect(70, 210, 601, 81))
        self.textEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 9pt \"Arial\";")
        self.textEdit_2.setObjectName("textEdit_2")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.frame_createVotingAddTitle)
        self.dateTimeEdit.setGeometry(QtCore.QRect(260, 360, 211, 51))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.dateTimeEdit.setStyleSheet('font: 75 14pt "Arial";')
        self.dateTimeEdit.setMinimumDate(QDate.currentDate())
        self.dateTimeEdit.setMaximumDate(QDate.currentDate().addDays(365))
        self.dateTimeEdit.setDateTime(datetime.today())
        self.dateTimeEdit.setCalendarPopup(True)
        self.pushButton_createVotingAddTitle = QtWidgets.QPushButton(self.frame_createVotingAddTitle)
        self.pushButton_createVotingAddTitle.setGeometry(QtCore.QRect(530, 360, 141, 51))
        self.pushButton_createVotingAddTitle.setObjectName("pushButton_createVotingAddTitle")
        self.pushButton_createVotingAddTitle.setText('继续')
        self.pushButton_createVotingAddTitle.clicked.connect(self.toAddOption)
        self.frame_createVotingAddOptions = QtWidgets.QFrame(self.centralwidget)
        self.frame_createVotingAddOptions.setGeometry(QtCore.QRect(0, 0, 751, 531))
        self.frame_createVotingAddOptions.setStyleSheet("background-color: rgb(170, 170, 127);")
        self.frame_createVotingAddOptions.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_createVotingAddOptions.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_createVotingAddOptions.setObjectName("frame_createVotingAddOptions")

        self.frame_createVotingAddOptions.setVisible(False)
        self.listView_options = QtWidgets.QListView(self.frame_createVotingAddOptions)
        self.listView_options.setGeometry(QtCore.QRect(430, 30, 271, 461))
        self.listView_options.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.listView_options.setObjectName("listView_options")
        self.listViewMode = QStringListModel()
        self.addedOptipnsList = []
        self.listViewMode.setStringList(self.addedOptipnsList)
        self.listView_options.setModel(self.listViewMode)
        self.listView_options.clicked.connect(self.removeOption)
        self.textEdit_3 = QtWidgets.QTextEdit(self.frame_createVotingAddOptions)
        self.textEdit_3.setGeometry(QtCore.QRect(40, 160, 331, 231))
        self.textEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_6 = QtWidgets.QLabel(self.frame_createVotingAddOptions)
        self.label_6.setGeometry(QtCore.QRect(50, 60, 341, 71))
        self.label_6.setStyleSheet("font: 75 20pt \"Arial\";")
        self.label_6.setObjectName("label_6")
        self.label_6.setText('请添加投票选项：')
        self.pushButton_addOption = QtWidgets.QPushButton(self.frame_createVotingAddOptions)
        self.pushButton_addOption.setGeometry(QtCore.QRect(40, 430, 151, 51))
        self.pushButton_addOption.setObjectName("pushButton_addOption")
        self.pushButton_addOption.clicked.connect(self.addOption)
        self.pushButton_addOption.setText('添加')
        self.pushButton_addFinish = QtWidgets.QPushButton(self.frame_createVotingAddOptions)
        self.pushButton_addFinish.setGeometry(QtCore.QRect(220, 430, 151, 51))
        self.pushButton_addFinish.setObjectName("pushButton_addFinish")
        self.pushButton_addFinish.setText('完成')
        self.pushButton_addFinish.clicked.connect(self.admitCreating)
        self.frame_createVotingSuccess = QtWidgets.QFrame(self.centralwidget)
        self.frame_createVotingSuccess.setGeometry(QtCore.QRect(0, 0, 751, 531))
        self.frame_createVotingSuccess.setStyleSheet("background-color: rgb(255, 74, 213);")
        self.frame_createVotingSuccess.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_createVotingSuccess.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_createVotingSuccess.setObjectName("frame_createVotingSuccess")

        self.frame_createVotingSuccess.setVisible(False)
        self.label_7 = QtWidgets.QLabel(self.frame_createVotingSuccess)
        self.label_7.setGeometry(QtCore.QRect(210, 80, 301, 101))
        self.label_7.setStyleSheet("font: 28pt \"Arial\";")
        self.label_7.setObjectName("label_7")
        self.label_createVotingSuccess = QtWidgets.QLabel(self.frame_createVotingSuccess)
        self.label_createVotingSuccess.setGeometry(QtCore.QRect(100, 210, 571, 131))
        self.label_createVotingSuccess.setStyleSheet("font: 75 16pt \"Arial\";")
        self.label_createVotingSuccess.setObjectName("label_createVotingSuccess")
        self.frame_viewListInputId = QtWidgets.QFrame(self.centralwidget)
        self.frame_viewListInputId.setGeometry(QtCore.QRect(0, 0, 751, 531))
        self.frame_viewListInputId.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.frame_viewListInputId.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_viewListInputId.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_viewListInputId.setObjectName("frame_viewListInputId")

        self.frame_viewListInputId.setVisible(False)
        self.label_8 = QtWidgets.QLabel(self.frame_viewListInputId)
        self.label_8.setGeometry(QtCore.QRect(200, 100, 371, 71))
        self.label_8.setStyleSheet("font: 75 28pt \"Arial\";")
        self.label_8.setObjectName("label_8")
        self.label_8.setText('请输入投票ID：')
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_viewListInputId)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 230, 461, 61))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 9pt \"Arial\";\n"
"font: 75 14pt \"Arial\";")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_ViewVotingInputId = QtWidgets.QPushButton(self.frame_viewListInputId)
        self.pushButton_ViewVotingInputId.setGeometry(QtCore.QRect(290, 350, 161, 51))
        self.pushButton_ViewVotingInputId.setObjectName("pushButton_ViewVotingInputId")
        self.pushButton_ViewVotingInputId.clicked.connect(self.admitViewId)
        self.pushButton_ViewVotingInputId.setText('继续')
        self.frame_5 = QtWidgets.QFrame(self.centralwidget)
        self.frame_5.setGeometry(QtCore.QRect(0, 0, 751, 531))
        self.frame_5.setStyleSheet("background-color: rgb(225, 74, 255);")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.frame_5.setVisible(False)
        self.label_9 = QtWidgets.QLabel(self.frame_5)
        self.label_9.setGeometry(QtCore.QRect(270, 10, 181, 51))
        self.label_9.setStyleSheet("font: 75 24pt \"Arial\";")
        self.label_9.setObjectName("label_9")
        self.label_9.setText('投票结果：')
        self.label_10 = QtWidgets.QLabel(self.frame_5)
        self.label_10.setGeometry(QtCore.QRect(20, 80, 41, 21))
        self.label_10.setStyleSheet("font: 75 10pt \"Arial\";")
        self.label_10.setObjectName("label_10")
        self.label_10.setText('开始')
        self.label_resultStartTime = QtWidgets.QLabel(self.frame_5)
        self.label_resultStartTime.setGeometry(QtCore.QRect(70, 70, 181, 41))
        self.label_resultStartTime.setStyleSheet("font: 75 10pt \"Arial\";")
        self.label_resultStartTime.setObjectName("label_resultStartTime")
        self.label_11 = QtWidgets.QLabel(self.frame_5)
        self.label_11.setGeometry(QtCore.QRect(520, 80, 41, 21))
        self.label_11.setStyleSheet("font: 75 10pt \"Arial\";")
        self.label_11.setObjectName("label_11")
        self.label_11.setText('结束')
        self.label_12 = QtWidgets.QLabel(self.frame_5)
        self.label_12.setGeometry(QtCore.QRect(570, 80, 171, 21))
        self.label_12.setStyleSheet("font: 75 10pt \"Arial\";")
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.frame_5)
        self.label_13.setGeometry(QtCore.QRect(100, 125, 571, 31))
        self.label_13.setObjectName("label_13")
        self.linen = QtWidgets.QFrame(self.frame_5)
        self.linen.setGeometry(QtCore.QRect(30, 160, 701, 20))
        self.linen.setFrameShape(QtWidgets.QFrame.HLine)
        self.linen.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.linen.setObjectName("linen")
        self.connected = False

        self.pushButton_exit.clicked.connect(self.toExit)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton_login.clicked.connect(self.login)
    #退出程序
    def toExit(self):
        self.s.close()
        exit()
    #显示投票结果窗口
    def viewResults(self):
        envelop(self.s,self.key,'view voting results'.encode())
        self.next_frame(self.frame_viewListInputId)
    #提交查询的投票序号
    def admitViewId(self):
        viewId = self.lineEdit_2.text()
        envelop(self.s,self.key,viewId.encode())
        viewMsg = de_envelop(self.s,self.key)
        print(viewMsg)
        if viewMsg == '查询成功...'.encode():
            votingResult = loads(de_envelop(self.s,self.key))
            title,options_,start_date,end_date = loads(de_envelop(self.s,self.key))
            self.label_13.setText(title)
            self.label_resultStartTime.setText(str(start_date))
            self.label_12.setText(str(end_date))
            options_ = eval(options_)
            for i in range(len(votingResult)):
                row = 180+40*i
                self.next_label = QtWidgets.QLabel(self.frame_5)
                self.next_label.setGeometry(QtCore.QRect(30, row, 691, 21))
                #self.next_label.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.next_label.setObjectName("next_label_{}".format(i))
                #print(len(options_),len(votingResult))
                self.next_label.setText(str(options_[i])+' : '+str(votingResult[i]))
                self.next_line = QtWidgets.QFrame(self.frame_5)
                self.next_line.setGeometry(QtCore.QRect(30, row+20, 701, 20))
                self.next_line.setFrameShape(QtWidgets.QFrame.HLine)
                self.next_line.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.next_line.setObjectName("line_{}".format(i))
            self.next_frame(self.frame_5)
        else:
            print('查询失败！')
    #提交创建的投票信息
    def toAddOption(self):
        self.addedTitle = self.textEdit_2.toPlainText()
        self.addedStartTime = self.dateTimeEdit.dateTime().toString(Qt.ISODate)
        self.next_frame(self.frame_createVotingAddOptions)
    #显示创建投票的窗口
    def addTitle(self):
        self.next_frame(self.frame_createVotingAddTitle)
    #显示创建投票的结果
    def admitCreating(self):
        if len(set(self.addedOptipnsList)) < len(self.addedOptipnsList):
            self.label_4.setText('创建失败!选项重复...')
        else:
            envelop(self.s,self.key,'create ok!'.encode())
            self.label_4.setText('正在创建投票...')
            self.next_frame(self.frame_voteSuccess)
            envelop(self.s,self.key,dumps((self.addedTitle,self.addedOptipnsList,self.addedStartTime)))
            print(self.addedTitle+'\n'+str(self.addedOptipnsList)+'\n'+self.addedStartTime)
            #创建信息：
            msg = de_envelop(self.s,self.key).decode()
            self.label_4.setText(msg)
        self.next_frame(self.frame_voteSuccess)
        self.addedOptipnsList.clear()
        self.listViewMode.setStringList(self.addedOptipnsList)

        #self.s.close()
    #添加选项的窗口
    def addOption(self):
        text = self.textEdit_3.toPlainText()
        self.addedOptipnsList.append(text)
        self.listViewMode.setStringList(self.addedOptipnsList)
        self.textEdit_3.setText('')
    #删除已添加的选项
    def removeOption(self,qModelIndex):
        self.addedOptipnsList.pop(qModelIndex.row())
        self.listViewMode.setStringList(self.addedOptipnsList)
    #用户登录的预处理
    def login_pre(self):
        global e,n
        self.s = socket.socket()
        self.s.connect(('127.0.0.1',5566))
        self.s.setblocking(1)
         #接收密钥版本
        global lastModified1
        rsa_key_version = self.s.recv(52).decode()
        if rsa_key_version==lastModified1:
            self.s.send(b'ok')
        else:
            self.s.send(b'no')
            length = bytes_to_int(self.s.recv(1024))
            new_key = self.s.recv(length)
            with open(os.getcwd()+r'\keys\key1\Server_rsa_pub.pem','wb') as f:
                f.write((b'===========PUBLICKEY==========\n'+new_key+b'\n==========END=========='))
        with open(os.getcwd()+r'\keys\key1\Server_rsa_pub.pem','rb') as f:
            (lastModified1,e,n)=f.read()[31:-24].split(b'**^.^**')
        print(self.s.recv(28).decode())
        (e,n)=map(bytes_to_int,(e,n))
        self.s.send(b'recv')
        #密钥交换
        print('交换主密钥...')
        key = gen_aes_key()
        self.key = key
        print(key)
        self.s.send(rsa_en_bytes(key,(e,n)))
        rc = self.s.recv(4)
        self.connected = True
        envelop(self.s,self.key,'login...'.encode())
        code = de_envelop(self.s,self.key)
        with open('captcha.png','wb') as f:
            f.write(code)
        os.system('pyrcc5 -o aaa_rc.py aaa.qrc')
        # self.graphicsView_Chapter.setStyleSheet("background-image: url(:/pic/captcha.png);")
        pic = QPixmap('./captcha.png')
        self.graphicsView_Chapter.setPixmap(pic)
        self.graphicsView_Chapter.setScaledContents(True) 
        self.graphicsView_Chapter.repaint()
        self.graphicsView_Chapter.show()
        self.graphicsView_Chapter.update()

    #更新显示的验证码
    def update_captcha(self):
        self.graphicsView_Chapter.setVisible(False)
        code = de_envelop(self.s,self.key)
        with open('captcha.png','wb') as f:
            f.write(code)
        os.system('pyrcc5 -o aaa_rc.py aaa.qrc')
        pic = QPixmap('./captcha.png')
        self.graphicsView_Chapter.setPixmap(pic)
        self.graphicsView_Chapter.setScaledContents(True) 
        # self.graphicsView_Chapter.setStyleSheet("background-image: url(:/pic/captcha.png);")
        self.graphicsView_Chapter.repaint()
        self.graphicsView_Chapter.setVisible(True)
        self.graphicsView_Chapter.show()
    #用户进行登录
    def login(self):
        key = self.key
        #发送用户名，密码
        code = self.textEdit.toPlainText()
        envelop(self.s,self.key,code.encode())
        code_msg = de_envelop(self.s,self.key)
        print(code_msg.decode())
        if code_msg == '验证码正确...'.encode():
            username = self.textEdit_userName.toPlainText()
            self.user = username
            passwd = self.plainTextEdit_passwd.toPlainText()
            envelop(self.s,self.key,username.encode())
            #获取salt值进行哈希
            salt = de_envelop(self.s,key)
            passwd =  SHA256.new(SHA256.new(passwd.encode()).digest()+salt).digest()
            envelop(self.s,key,passwd)
            identify_msg = de_envelop(self.s,key).decode()
            print(identify_msg)
            #确认服务器已准备
            self.s.recv(4)
            if identify_msg == '正在登录...':
                login_msg = de_envelop(self.s,key).decode()
                print(login_msg)
                if login_msg == '登录成功...':
                    self.userName = username
                    self.has_login = True
                    self.label_login_msg.setText('')
                    self.menu()
                else:
                    self.label_login_msg.setText('用户名或密码错误！')
                    envelop(self.s,self.key,'login...'.encode())
                    self.update_captcha()
                    return
        else:
            envelop(self.s,self.key,'login...'.encode())
            self.label_login_msg.setText('验证码错误！')
            self.update_captcha()
            return
        
    #显示投票的选项
    def show_options(self):
        self.id_ = self.lineEdit.text() #输入投票ID
        id_ = self.id_
        envelop(self.s,self.key,id_.encode())
        msg = de_envelop(self.s,self.key).decode()
        print(msg)
        self.label_3.setText('投票标题：')
        self.next_frame(self.frame_voting_list)
        id_ = self.id_
        key = self.key
        #查看状态
        status = de_envelop(self.s,key)
        print(status.decode())
        if status == 'plese sending the message...'.encode():
            vote_expire = de_envelop(self.s,key)
            if not vote_expire == 'The vote is in progress!'.encode():
                print(vote_expire.decode())
                #显示投票已经过期
                self.next_frame(self.frame_voteSuccess)
                self.label_4.setText('抱歉，投票已到截止日期...')
            else:
                title,options_ = loads(de_envelop(self.s,key)) 
                options_ = eval(options_)
                self.label_2.setText(title)
                #获得当前投票场次信息(标题,选项)
                print('投票标题：',title)
                for i in range(len(options_)):
                    print('for1')
                    row = 210+80*(i//4);column = 50+170*(i%4)
                    self.next_option=QtWidgets.QRadioButton(self.frame_voting_list)
                    self.next_option.setGeometry(QtCore.QRect(column, row, 115, 19))
                    self.next_option.setText(options_[i])
                    self.next_option.setObjectName("radioButton_option{}".format(i))
                    self.next_option.toggled.connect(lambda:self.optionChose(i))
                    self.next_option.setText(options_[i])
                    self.next_option.setVisible(True)
                    print('--',i+1,',',options_[i])
                    self.next_frame(self.frame_voting_list)
        else:
            self.label_4.setText(status.decode())
            self.next_frame(self.frame_voteSuccess)
            print('已经投过票了')
    #该方法完成窗口的切换
    def next_frame(self,frameShowing):
        self.label_14 = QtWidgets.QLabel(frameShowing)
        self.label_14.setGeometry(QtCore.QRect(560, 0, 41, 31))
        self.label_14.setObjectName("label_14")
        self.label_14.setText('您好：')
        self.label_user = QtWidgets.QLabel(frameShowing)
        self.label_user.setGeometry(QtCore.QRect(600, 5, 101, 21))
        self.label_user.setObjectName("label_user")
        self.label_user.setText(self.user)
        self.toolButton_user = QtWidgets.QToolButton(frameShowing)
        self.toolButton_user.setGeometry(QtCore.QRect(710, 0, 41, 31))
        self.toolButton_user.setObjectName("toolButton_user")
        self.toolButton_user.setText('菜单')
        self.toolButton_user.setIcon(QIcon("menu.ico"))
        self.toolButton_user.setToolTip("用户菜单")
        self.toolButton_user.setAutoRaise(True)
        #创建菜单
        menu = QMenu()
        #创建action并添加到菜单中
        action1 = QAction(QIcon("menu.ico"),"主菜单",menu)
        action2 = QAction(QIcon("menu.ico"),"登出",menu)
        action3 = QAction(QIcon("menu.ico"),"退出",menu)
        menu.addActions([action1,action2,action3])
        #响应action点击事件
        action1.triggered.connect(self.menu)
        action2.triggered.connect(self.logout)
        action3.triggered.connect(self.toExit)
        self.toolButton_user.setMenu(menu)
        self.toolButton_user.setPopupMode(QToolButton.MenuButtonPopup)
        self.showing_frame.setVisible(False)
        self.showing_frame = frameShowing
        frameShowing.setVisible(True)
    #登出
    def logout(self):
        self.user=None
        self.has_login = False
        self.next_frame(self.frame_login)
        self.s.close()
    #主菜单
    def menu(self):
        print('menu!')
        if self.has_login == True:
            self.next_frame(self.frame_menu)
        else:
            self.next_frame(self.frame_login)
    #显示已选择的选项
    def optionChose(self,i):
        self.option_Chose = i
        self.pushButton_optionChose.setVisible(True)
    #开始进行投票
    def start_voting(self):
        envelop(self.s,self.key,'start voting...'.encode())
        self.next_frame(self.frame_startVoting)
    #完成对选票的盲签名三方过程
    def vote(self):
        global e,n
        s = self.s
        id_ = self.id_
        key = self.key

        self.label_4.setText('正在投票...')

        self.next_frame(self.frame_voteSuccess)
        result_vote = self.option_Chose
        log('The result of the vote is being produced...')
        r = random.randint(1,n)
        log('Generating blind signature factor r={}...'.format(r))
        #把result 加上uuid进行哈希H(UUID,id_,result)
        UUID = str(uuid4())
        log('UUID：{}'.format(UUID))
        print('chose',self.option_Chose)
        h_msg = SHA256.new(dumps((UUID,self.id_,self.option_Chose))).digest()
 
        #发送盲化消息
        blind_msg = int_to_bytes((rsa_enc(r,e,n)*bytes_to_int(h_msg))%n)
        log('Send blind messages...')
        envelop(s,key,blind_msg)
        print('盲化消息：',blind_msg)
        #获得盲化后的签名
        print('收到来自认证服务器的签名...')
        log('Receive signatures for ballot message digest...')
        rcv = de_envelop(s,key)
        print('收到签名：',rcv)
        #对ID的签名
        sign_voting_id = de_envelop(s,key)
        r1 = inv(r,n)
        rcv = bytes_to_int(rcv)
        #s.close()
        
        #给服务器2发送结果
        result = (r1*rcv%n)
        print('h_msg:',bytes_to_int(h_msg))
        print('结果正确性:',rsa_enc(result,e,n))
        with open(os.getcwd()+r'\keys\key2\Server_rsa_pub.pem','rb') as f:
            (lastModified2,e1,n1)=f.read()[31:-24].split(b'**^.^**')
        e1,n1 = map(bytes_to_int,(e1,n1))
        key = gen_aes_key()
        s1 = socket.socket()
        s1.connect(('127.0.0.1',5567))
        #接收密钥版本
        rsa_key_version = s1.recv(52).decode()
        if rsa_key_version==lastModified2:
            s1.send(b'ok')
        else:
            s1.send(b'no')
            length = bytes_to_int(s1.recv(1024))
            new_key = s1.recv(length)
            with open(os.getcwd()+r'\keys\key2\Server_rsa_pub.pem','wb') as f:
                f.write((b'===========PUBLICKEY==========\n'+new_key+b'\n==========END=========='))
        with open(os.getcwd()+r'\keys\key2\Server_rsa_pub.pem','rb') as f:
            (lastModified2,e1,n1)=f.read()[31:-24].split(b'**^.^**')
        print(s1.recv(28).decode())
        (e1,n1)=map(bytes_to_int,(e1,n1))
        s1.send(b'recv')
        #密钥交换
        print('交换主密钥...')
        key = gen_aes_key()
        s1.send(rsa_en_bytes(key,(e1,n1)))
        s1.recv(4)
        #发送结果和签名
        envelop(s1,key,sign_voting_id)##############4/19#######################
        msg = dumps((UUID,id_,result_vote))
        log('Receive the signature of the message digest of the ballot and send the ballot to the counting server...')
        envelop(s1,key,msg)
        log('Send signature...')
        envelop(s1,key,int_to_bytes(result))
        status1 = de_envelop(s1,key)
        self.label_4.setText(status1.decode())
        print(status1.decode())
        s1.close()
        self.id_ = None
        self.option_Chose = None
    #开始创建选票
    def create_voting(self):

        envelop(self.s,self.key,'create a voting...'.encode())
        self.next_frame(self.frame_createVotingAddTitle)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_userName.setText(_translate("MainWindow", "用户名:"))
        self.label_passwd.setText(_translate("MainWindow", "密码:"))
        self.label_chapter.setText(_translate("MainWindow", "验证码"))
        self.pushButton_login.setText(_translate("MainWindow", "登录"))
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_userName.setText(_translate("MainWindow", "用户名:"))
        self.label_passwd.setText(_translate("MainWindow", "密码:"))
        self.label_chapter.setText(_translate("MainWindow", "验证码:"))
        self.pushButton_login.setText(_translate("MainWindow", "登录"))
        self.label.setText(_translate("MainWindow", "菜单"))
        self.pushButton_startVoting.setText(_translate("MainWindow", "投票"))
        self.pushButton_createVoting.setText(_translate("MainWindow", "发起投票"))
        self.pushButton_viewResults.setText(_translate("MainWindow", "查看结果"))
        self.pushButton_exit.setText(_translate("MainWindow", "退出"))
import aaa_rc
from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton
import sys
class DemoMain(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  #调用Ui_Mainwindow中的函数setupUi实现显示界面
if __name__=='__main__':
    app=QApplication(sys.argv)
    demo=DemoMain()
    demo.login_pre()
    demo.show()
    sys.exit(app.exec_())