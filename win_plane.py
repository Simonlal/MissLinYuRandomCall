from PyQt5.Qt import *
from win import Ui_Form

import sys
import os


class My_win(QWidget, Ui_Form):
    path_signal = pyqtSignal(str, str)  # 人员名单地址和考察内容地址信号

    def __init__(self, parent=None):
        super(My_win, self).__init__(parent=parent)
        self.setupUi(self)
        # 初始lcd
        self.init_lcd = 3
        self.lcd = self.init_lcd

        self.timer = QTimer()
        self.timer.timeout.connect(self.Update_CountDown)

    # 选择内容路径
    def ChangeContent(self):
        self.ContentPath.clear()
        ContentPath = QFileDialog.getOpenFileName(None, "选择考察内容", os.getcwd(),
                                                  filter="文本文件(*.doc *.docx)")[0]
        self.ContentPath.setText(ContentPath)

    # 选择姓名路径
    def ChangeNameList(self):
        self.NameListPath.clear()
        ContentPath = QFileDialog.getOpenFileName(None, "选择人员名单", os.getcwd(),
                                                  filter="文本文件(*.xlsx *.xls)")[0]
        self.NameListPath.setText(ContentPath)

    # 开始按钮激活
    def StartCheckout(self):
        path1 = self.NameListPath.text()
        path2 = self.ContentPath.text()
        bool_path1 = bool(path1)
        bool_path2 = bool(path2)
        if (bool_path1 and bool_path2) and os.path.exists(path1) and os.path.exists(path2):
            self.StartPushButton.setEnabled(True)
        else:
            self.StartPushButton.setEnabled(False)

    # 触发定时器
    def Start(self):
        self.PushButtonRestart()
        self.ResultShow.clear()

        self.lcd = self.init_lcd
        self.CountDownlcd.display(self.init_lcd)
        self.timer.start(1000)

    # 全部重置
    def Restart(self):
        self.NameListPath.clear()
        self.ContentPath.clear()

        self.ResultShow.clear()
        self.CountDownlcd.display(self.init_lcd)

        self.StartPushButton.setEnabled(False)
        # 重置
        self.lcd = self.init_lcd

    # 按钮重置
    def PushButtonRestart(self):
        self.StartPushButton.setEnabled(True)
        self.RestartPushButton.setEnabled(True)

    #显示部分
    def TextShow(self, name, content):
        self.ResultShow.clear()
        result = "<h1>{}</h1><p>{}.</p>".format(name,content)
        result ="""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                h1 {{
                    color: white;
                    font-size: 8px;
                    text-align: left;
                }}

                p {{
                    color: white;
                    font-size: 24px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <h1>{0}</h1>
            <p>{1}</p>
        </body>
        </html>""".format(name,content)

        # print(result)
        self.ResultShow.setHtml(result)

    # 时间更新槽函数
    def Update_CountDown(self):
        self.lcd -= 1
        self.CountDownlcd.display(self.lcd)
        if self.lcd <= 0:
            self.timer.stop()
            NameListPath = self.NameListPath.text()
            ContentPath = self.ContentPath.text()
            self.path_signal.emit(NameListPath, ContentPath)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = My_win()

    t.show()
    sys.exit(app.exec_())
