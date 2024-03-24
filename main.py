from PyQt5.Qt import *
from PyQt5 import QtCore

from  qdarkgraystyle import load_stylesheet_pyqt5

import sys
from win_plane import My_win
from RandQthread import Rand

if __name__ == '__main__':
    # setAttribute 会导致一丢丢的模糊和虚化
    QtCore.QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    # 解决分辨率和缩放比例导致的错位
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)

    win = My_win()

    win.setStyleSheet(load_stylesheet_pyqt5())

    # 业务线程
    r = Rand()

    # 传入地址、启动随机
    def PathTransfer(NameListPath, ContentPath):
        r.DataPrepare(NameListPath, ContentPath)
        r.start()


    # 传出结果、停止线程
    def ResultsTransfer(RandName, RandContent):
        # print(RandName, RandContent)
        win.TextShow(RandName, RandContent)
        win.PushButtonRestart()
        r.quit()


    win.path_signal.connect(PathTransfer)
    r.finishSignal.connect(ResultsTransfer)

    win.show()

    sys.exit(app.exec_())
