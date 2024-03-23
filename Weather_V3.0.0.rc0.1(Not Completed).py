# -*- coding: UTF-8 -*-
# Copyright (C) 2024 Chen Junren, Inc. All Rights Reserved
# @Author  : Chen Junren
# @Project : Weather
# @Product : Pycharm v2022.3.3
# @File    : Weather.py
import datetime
import json
import locale
import logging
import os
import sys
import time
import traceback
from json import JSONDecodeError

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication

locale.setlocale(locale.LC_CTYPE, "Chinese")
if not os.path.exists("./log"):
    os.mkdir("log")
current_date = (
    f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}"
    f" {time.localtime().tm_hour}_{time.localtime().tm_min}_{time.localtime().tm_sec}"
)
logging.basicConfig(
    level=logging.INFO,
    filename=f"./log/{current_date}.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)


def read_settings(filename="settings.txt"):
    """
    Reads settings from a file and returns them as a dictionary.

    Args:
        filename: The name of the file to read the settings from (default: "settings.txt").

    Returns:
        dict: A dictionary containing the settings.

    """
    with open(filename, "r") as s:
        setting = json.load(s)
    return setting


def read_code(filename="city_code.txt"):
    """
    Reads city codes from a file and returns them as a dictionary.

    Args:
        filename: The name of the file to read the city codes from (default: "city_code.txt").

    Returns:
        dict: A dictionary containing city codes.

    """
    with open(filename, "r") as f:
        city_code = json.load(f)
    return city_code


def get_code(table, city):
    """
    Retrieves the code for a specific city from a table.

    Args:
        table: A dictionary containing city codes.
        city: The name of the city.

    Returns:
        The code corresponding to the city.

    """
    return table[city]


def get_weather_1(city:str, code:str, dates:QtCore.QDate):
    """
    Retrieves weather information for a specific city.

    Args:
        city: The name of the city.
        code: The code of the city.

    Returns:
        str: The weather information for the city.

    Raises:
        KeyError: If the city code is not found.
        requests.ConnectionError: If there is a network error.
        JSONDecodeError: If there is an error decoding the JSON response.

    """
    global key
    key = read_settings().get("key")
    html = f"https://devapi.qweather.com/v7/weather/7d?key={key}&location={code}"
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
    print(info_json)
    info_2_json = info2.json()
    air_json = air.json()
    warning = warning.json()
    if (
            info_json["code"] == "401"
            or info_2_json["code"] == "401"
            or air_json["code"] == "401"
            or warning["code"] == "401"
    ):
        return "KeyERR"
    global warnings
    warn = warning["warning"]
    warnings = "预           警："
    if warn:
        for i, x in enumerate(warn):
            sender = warn[i]["sender"]
            date1 = datetime.datetime.strptime(
                warn[i]["pubTime"], "%Y-%m-%dT%H:%M+08:00"
            ).strftime("%Y年%m月%d日%H时%M分")
            typ = warn[i]["typeName"]
            color_li = {
                "Green": "绿色",
                "White": "白色",
                "Blue": "白色",
                "Yellow": "黄色",
                "Orange": "橙色",
                "Red": "红色",
                "Black": "黑色",
            }

            color = color_li.get(warn[i]["severityColor"])
            if warnings == "预           警：":
                warnings += f"{sender}{date1}发布{typ}{color}预警" + "\n"
            else:
                warnings += (
                        f"                           {sender}{date1}发布{typ}{color}预警"
                        + "\n"
                )
    else:
        warnings = "预           警：暂无预警信息"
    dated = str(dates)[19:-1].replace(', ', '-')
    global date, temp, temp_now, humidity, wind_direction, wind_speed, air_pollution, weather, settings
    city += "\n"
    date = f"日           期：{info_json['daily'][dated]['fxDate']}\n"
    temp = (
        f"温           度：最高温{info_json['daily'][dated]['tempMax']}℃ \n"
        f"                           最低温{info_json['daily'][dated]['tempMin']}℃\n"
    )
    temp_now = f"实时温度：{info_2_json['now']['temp']}℃\n"
    humidity = f"湿           度：{info_2_json['now']['humidity']}%\n"
    wind_direction = f"风           向：{info_2_json['now']['windDir']}\n"
    wind_speed = f"风           力：{info_2_json['now']['windScale']}级\n"
    air_pollution = f"空气污染：{air_json['daily'][dated]['category']}\n"
    weather = f"天           气：{info_2_json['now']['text']}\n"
    settings = read_settings()
    for i in settings:
        if settings.get(i) == 0:
            globals()[i] = ""
    return (
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


def get_weather_5(code2):
    """
    Get the 5-day weather forecast for a specific location.

    Args:
        code2: The location code for the desired weather forecast.

    Returns:
        A list of strings, each containing the weather information for a specific day.
        Each string includes the following details:
        - Date
        - Weather condition
        - Temperature range
        - Humidity
        - Wind direction
        - Wind scale

    Raises:
        KeyError: If the API response does not contain the expected data.
    """
    try:
        key = read_settings().get("key")
        html = f"https://devapi.qweather.com/v7/weather/7d?key={key}&location={code2}"
        info = requests.get(html)
        info.encoding = "utf-8"
        info_json = info.json()
        info_json = info_json["daily"]
        temp_li = []
        for index, data in enumerate(info_json):
            logging.info(f"{index}-{data}")
            temp_li.append(
                f"日期：{data['fxDate']}\n"
                f"天气：{data['textDay']}\n"
                f"温度：{data['tempMax']}℃-{data['tempMin']}℃\n"
                f"湿度：{data['humidity']}%\n"
                f"风向：{data['windDirDay']}\n"
                f"风力：{data['windScaleDay']}级\n"
            )
    except KeyError:
        return "KeyERR"
    return temp_li


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(599, 483)
        font = QtGui.QFont()
        font.setFamily("荆南麦圆体")
        Form.setFont(font)
        Form.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 70, 301, 62))
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
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(380, 300, 160, 30))
        self.label_3.setMinimumSize(QtCore.QSize(160, 30))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(380, 70, 160, 301))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("荆南麦圆体")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("荆南麦圆体")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.calendarWidget = QtWidgets.QCalendarWidget(Form)
        self.calendarWidget.setGeometry(QtCore.QRect(50, 150, 301, 221))
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.setMinimumDate(QtCore.QDate(QtCore.QDate.currentDate().year(),
                                                             QtCore.QDate.currentDate().month(),
                                                             QtCore.QDate.currentDate().day()))
        self.calendarWidget.setMaximumDate(
            QtCore.QDate(QtCore.QDate(QtCore.QDate.currentDate().addDays(7))))
        self.retranslateUi(Form)
        self.pushButton_2.clicked.connect(Form.close) # type: ignore
        self.pushButton.clicked.connect(Form.getWeather_1) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "今日天气"))
        self.label.setText(_translate("Form", "天气查询"))
        self.label_2.setText(_translate("Form", "城市"))
        self.pushButton.setText(_translate("Form", "查询选中日天气"))
        self.pushButton_3.setText(_translate("Form", "查询后五日天气"))
        self.pushButton_4.setText(_translate("Form", "帮助"))
        self.pushButton_2.setText(_translate("Form", "退出"))


class FiveDays(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, city):
        """
            Initialize the AnotherWindow object.

            Args:
                city: The name of the city for which the weather information is displayed.

            Returns:
                None
        """
        super().__init__()
        layout = QtWidgets.QHBoxLayout()
        self.setWindowTitle(f"五日天气 - {city}市")
        self.setLayout(layout)
        self.setFixedSize(1000, 400)
        self.resize(1000, 400)
        self.setWindowIcon(QtGui.QIcon("Weather.png"))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily("荆南麦圆体")
        self.setFont(font)
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.label)
        self.label.setText(info[0])
        self.label.setAlignment(QtCore.Qt.AlignLeft | Qt.AlignVCenter)
        self.label1 = QtWidgets.QLabel()
        layout.addWidget(self.label1)
        self.label1.setText(info[1])
        self.label1.setAlignment(QtCore.Qt.AlignLeft | Qt.AlignVCenter)
        self.label2 = QtWidgets.QLabel()
        layout.addWidget(self.label2)
        self.label2.setText(info[2])
        self.label2.setAlignment(QtCore.Qt.AlignLeft | Qt.AlignVCenter)
        self.label3 = QtWidgets.QLabel()
        layout.addWidget(self.label3)
        self.label3.setText(info[3])
        self.label3.setAlignment(QtCore.Qt.AlignLeft | Qt.AlignVCenter)
        self.label4 = QtWidgets.QLabel()
        layout.addWidget(self.label4)
        self.label4.setText(info[4])
        self.label4.setAlignment(QtCore.Qt.AlignLeft | Qt.AlignVCenter)

class OneDay(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, city, dated):
        """
            Initialize the AnotherWindow object.

            Args:
                city: The name of the city for which the weather information is displayed.

            Returns:
                None
        """
        super().__init__()
        layout = QtWidgets.QHBoxLayout()
        self.setWindowTitle(f"{dated} - 天气 - {city}市")
        self.setLayout(layout)
        self.setFixedSize(1000, 400)
        self.resize(1000, 400)
        self.setWindowIcon(QtGui.QIcon("Weather.png"))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily("荆南麦圆体")
        self.setFont(font)
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.label)
        self.label.setText(info[0])
        self.label.setAlignment(QtCore.Qt.AlignLeft | Qt.AlignVCenter)
        self.label1 = QtWidgets.QLabel()


class Weather(QWidget, Ui_Form):
    """
    Represents a weather application that allows users to retrieve weather information for a specific city.

    Args:
        parent: The parent widget (default: None).

    Attributes:
        table: A dictionary containing city codes.

        lineEdit: A QLineEdit widget for entering the city name.
        label_3: A QLabel widget for displaying status messages.

    Methods:
        __init__: Initializes the weather application.
        InitializeUi: Initializes the user interface.
        getWeather_1: Retrieves weather information based on the user's input.
        keyPressEvent: Handles key press events in the weather application.

    """

    def __init__(self, parent=None):
        super(Weather, self).__init__(parent)
        self.setupUi(self)
        self.InitializeUi()
        self.setFixedSize(600, 500)

    def InitializeUi(self):
        """
        Initializes the user interface of the weather application.

        Returns:
            None

        """
        self.table = read_code()
        #self.textEdit.setReadOnly(True)
        self.lineEdit.setFocus()

    def getWeather_1(self):
        """
        Retrieves weather information based on the user's input.

        Returns:
            None

        """
        city = self.lineEdit.text()
        dated = self.calendarWidget.selectedDate()


        err_msg = ""
        logging.info(f"输入：{city}")
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
                info = get_weather_1(city, citycode, dated)
                print(info)
                if info == "KeyERR":
                    err_msg = "设置错误"
                    logging.warning(
                        f"设置错误：请检查Key:[{read_settings()['key']}]是否正确"
                    )
                logging.info(f"查询:{city}-{citycode}\n[{info}]")
                logging.info(f"当前设置:{read_settings()}")
            except requests.ConnectionError:
                err_msg = "网络错误"
                logging.warning(f"网络错误:{city} 请检查网络连接")
            except JSONDecodeError:
                err_msg = "输入错误"
                logging.warning(f"输入错误 JSONDecodeError:{city} 请检查输入")
            except KeyError:
                err_msg = "输入错误"
                print(repr(traceback.print_exc()))
                logging.warning(f"输入错误 KeyError:{city} 请检查输入")
            except Exception as e:
                err_msg = "未知错误"
                logging.warning(repr(e))

        self.lineEdit.setFocus()
        if not err_msg:
            #self.textEdit.setText(info)
            self.one = OneDay(city, date)
            self.one.show()
            # self.textEdit.setText()
            self.label_3.setText("查询成功")
            self.label_3.setText("查询成功")
        else:
            self.label_3.setText(f"查询失败 {err_msg}")
            #self.textEdit.setText("")

        self.lineEdit.clear()

    def getWeather_5(self):
        """
            Perform a weather query based on user input.

            Returns:
                None

            Raises:
                KeyError: If there is an error with the user input.
                requests.ConnectionError: If there is a network error.
                JSONDecodeError: If there is an error decoding the JSON response.
                Exception: If there is an unknown error.

            Examples:
                This function is typically called when the user wants to query the weather.
                It retrieves the user input, performs a weather query, and displays the result.
        """
        city = self.lineEdit.text()
        err_msg = ""
        logging.info(f"输入：{city}")
        try:
            citycode = get_code(self.table, city)
            # print(citycode, city)
        except KeyError:
            logging.warning(f"输入错误：{city}")
            err_msg = "输入错误"
        except Exception as e:
            logging.error(repr(e))
            err_msg = "未知错误"
        self.label_3.setText("正在查询中...")
        if not err_msg:
            try:
                global info
                logging.info(f"查询：{city}-{citycode}")
                info = get_weather_5(citycode)
                if info == "KeyERR":
                    err_msg = "设置错误"
                    logging.warning(
                        f"设置错误：请检查Key:[{read_settings()['key']}]是否正确"
                    )
                logging.info(f"查询:{city}-{citycode}\n[{info}]")
                logging.info(f"当前设置:{read_settings()}")
            except requests.ConnectionError:
                err_msg = "网络错误"
                logging.warning(f"网络错误:{city} 请检查网络连接")
            except JSONDecodeError:
                err_msg = "输入错误"
                logging.warning(f"输入错误 JSONDecodeError:{city} 请检查输入")
            except KeyError:
                err_msg = "输入错误"
                logging.warning(f"输入错误 KeyError:{city} 请检查输入")
            except Exception as e:
                err_msg = "未知错误"
                logging.warning(repr(e))
                self.lineEdit.setText(repr(e))
        self.lineEdit.setFocus()
        if not err_msg:
            self.w = FiveDays(city)
            self.w.show()
            # self.textEdit.setText()
            self.label_3.setText("查询成功")
        else:
            self.label_3.setText(f"查询失败 {err_msg}")
            #self.textEdit.setText("")

        self.lineEdit.clear()

    def keyPressEvent(self, e):
        """
        Handles key press events in the weather application.

        Args:
            e: The key event object.

        Returns:
            None

        """
        if e.key() == Qt.Key_Return:
            self.getWeather_1()
        if e.key() == Qt.Key_R:
            self.label_3.setText("打开设置文件")
            os.system(".\\settings.txt")
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
    logging.info(f"读取设置:{read_settings()}")
    main.show()
    sys.exit(app.exec_())
