import json
from json import JSONDecodeError
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication
import requests
import logging
import time
import os
import traceback
import locale

locale.setlocale(locale.LC_CTYPE, "Chinese")
if not os.path.exists("./log"):
    os.mkdir("log")
current_date = f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}" \
               f" {time.localtime().tm_hour}_{time.localtime().tm_min}_{time.localtime().tm_sec}"
logging.basicConfig(
    level=logging.INFO,
    filename=f"./log/{current_date}.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)


def read_settings(filename="settings.txt"):
    with open(filename, "r") as s:
        setting = json.load(s)
    return setting


def read_code(filename="city_code.txt"):
    with open(filename, "r") as f:
        city_code = json.load(f)
    return city_code


def get_code(table, city):
    code = table[city]
    return code


def get_weather(city, code):
    global key
    key = read_settings().get("key")
    html = f"https://devapi.qweather.com/v7/weather/3d?key={key}&location={code}"
    hef = f"https://devapi.qweather.com/v7/weather/now?key={key}&location={code}"
    air = f"https://devapi.qweather.com/v7/air/5d?key={key}&location={code}"
    warning = f"https://devapi.qweather.com/v7/warning/now?key={key}&location={code}"
    info = requests.get(html)
    info.encoding = "utf-8"
    info2 = requests.get(hef)
    info2.encoding = "utf-8"
    air = requests.get(air)
    air.encoding = "utf-8"
    warning = requests.get(warning)
    warning.encoding = "utf-8"
    # logging.info(info,info2,air,warning)
    info_json = info.json()
    info_2_json = info2.json()
    air_json = air.json()
    warning = warning.json()
    global warnings
    warn = warning["warning"]
    if warn:
        sender = warn[0]["sender"]
        date1 = datetime.datetime.strptime(
            warn[0]["pubTime"], "%Y-%m-%dT%H:%M+08:00"
        ).strftime("%Y年%m月%d日%H时%M分")
        typ = warn[0]["typeName"]
        color_li = {
            "Green": "绿色",
            "White": "白色",
            "Blue": "白色",
            "Yellow": "黄色",
            "Orange": "橙色",
            "Red": "红色",
            "Black": "黑色",
        }
        color = color_li.get(warn[0]["severityColor"])
        warnings = (
                "预           警：" + sender + date1 + "发布" + typ + color + "预警" + "\n"
        )
    else:
        warnings = "预           警：暂无预警信息"
    global date, temp, temp_now, humidity, wind_direction, wind_speed, air_pollution, weather, settings
    city += "\n"
    date = f"日           期：{info_json['daily'][0]['fxDate']}\n"
    temp = (
        f"温           度：最高温{info_json['daily'][0]['tempMax']}℃ \n"
        f"                           最低温{info_json['daily'][0]['tempMin']}℃\n"
    )
    temp_now = f"实时温度：{info_2_json['now']['temp']}℃\n"
    humidity = f"湿           度：{info_2_json['now']['humidity']}%\n"
    wind_direction = f"风           向：{info_2_json['now']['windDir']}\n"
    wind_speed = f"风           力：{info_2_json['now']['windScale']}级\n"
    air_pollution = f"空气污染：{air_json['daily'][0]['category']}\n"
    weather = f"天           气：{info_2_json['now']['text']}\n"
    settings = read_settings()
    for i in settings:
        if settings.get(i) != 0:
            pass
        else:
            globals()[i] = ""
    showed = (
            city
            + date
            + temp
            + temp_now
            + humidity
            + wind_direction
            + wind_speed
            + air_pollution
            + weather
            + warnings
    )
    # logging.info(showed)

    return showed


# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'Ui_weather-2.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(599, 483)
        font = QtGui.QFont()
        font.setFamily("荆南麦圆体")
        Form.setFont(font)
        Form.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(125, 140, 330, 231))
        font = QtGui.QFont()
        font.setFamily("荆南麦圆体")
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(130, 70, 122, 62))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("荆南麦圆体")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("荆南麦圆体")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(260, 70, 195, 61))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("荆南麦圆体")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("荆南麦圆体")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(210, 360, 160, 30))
        self.label_3.setMinimumSize(QtCore.QSize(160, 90))
        self.label_3.setText(
            "请先输入城市再查询\n按回车或单击按钮查询\n按R键打开设置文件\n按I键显示此页面"
        )
        self.label_3.setObjectName("label_3")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        Form.setWindowIcon(QtGui.QIcon("Weather.png"))
        self.retranslateUi(Form)
        self.pushButton_2.clicked.connect(Form.close)  # type: ignore
        self.pushButton.clicked.connect(Form.getWeather)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "今日天气"))
        self.label.setText(_translate("Form", "天气查询"))
        self.label_2.setText(_translate("Form", "城市"))
        self.pushButton.setText(_translate("Form", "查询"))
        self.pushButton_2.setText(_translate("Form", "退出"))


# -*- coding: utf-8 -*-


class Weather(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Weather, self).__init__(parent)
        self.setupUi(self)
        self.InitializeUi()

    def InitializeUi(self):
        self.table = read_code()
        self.textEdit.setReadOnly(True)
        self.lineEdit.setFocus()

    def getWeather(self):
        city = self.lineEdit.text()
        err_msg = ""
        logging.info("输入：" + city)
        try:
            citycode = get_code(self.table, city)
        except KeyError:
            logging.warning(f"输入错误：{city}")
            err_msg = "输入错误"
        # logging.info(citycode)
        # logging.info(f"错误：{city}")
        self.label_3.setText("正在查询中...")
        if not err_msg:
            # logging.info("Not ERROR MESSAGE")
            try:
                # logging.info(2)
                info = get_weather(city, citycode)
                logging.info(f"查询:{city}-{citycode}\n[{info}]")
            except requests.ConnectionError:
                err_msg = "网络错误"
                logging.warning(f"网络错误:{city} 请检查网络连接")
            except JSONDecodeError:
                err_msg = "输入错误"
                logging.warning(f"输入错误 JSONDecodeError:{city} 请检查输入")
            except KeyError:
                err_msg = "输入错误"
                logging.warning(f"输入错误 KeyError:{city} 请检查输入")
            except:
                err_msg = "未知错误"
                logging.warning(traceback.format_exc())
        if not err_msg:
            self.lineEdit.setFocus()
            self.textEdit.setText(info)
            self.label_3.setText("查询成功")
            self.lineEdit.clear()
        else:
            self.lineEdit.setFocus()
            self.label_3.setText(f"查询失败 {err_msg}")
            self.textEdit.setText("")
            self.lineEdit.clear()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.getWeather()
        if e.key() == Qt.Key_R:
            self.label_3.setText("打开设置文件")
            os.system(".\settings.txt")
            logging.info("打开设置文件")
        if e.key() == Qt.Key_I:
            self.label_3.setText(
                "请先输入城市再查询\n按回车或单击按钮查询\n按R键打开设置文件\n按I键显示此页面"
            )
            logging.info("显示帮助")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Weather()
    logging.info("初始化成功")
    logging.info(f"设置:{read_settings()}")
    main.show()
    sys.exit(app.exec_())
