import random
import sys
import time
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from ui import user_accept
import asyncio


class Data():
    data = b""


def split_string_by_length(string, length):
    return [string[i:i + length] for i in range(0, len(string), length)]


def combin(cutA, cutB, cutC, i):
    str = 'A:'
    str += cutA[i]
    str += 'B:'
    str += cutB[i]
    str += 'C:'
    str += cutC[i]
    return str


class Server(QMainWindow, user_accept.Ui_MainWindow):
    def __init__(self):
        super(Server, self).__init__()
        self.setupUi(self)
        self.serverA = QTcpServer(self)
        self.serverB = QTcpServer(self)
        self.serverC = QTcpServer(self)
        self.sock = QTcpSocket(self)
        self.sock.connectToHost(QHostAddress.LocalHost, 7777)
        self.sockets = []
        self.DataA = Data()
        self.DataB = Data()
        self.DataC = Data()
        str1 = "connect!"
        self.sock.connected.connect(lambda: self.write_data(self.sock, str1))
        if not self.serverA.listen(QHostAddress.LocalHost, 6666):
            print(self.serverA.errorString())
        if not self.serverB.listen(QHostAddress.LocalHost, 6667):
            print(self.serverB.errorString())
        if not self.serverC.listen(QHostAddress.LocalHost, 6668):
            print(self.serverC.errorString())
        self.serverA.newConnection.connect(lambda: self.new_socket_slot(self.serverA, self.lineEdit_A, self.DataA))
        self.serverB.newConnection.connect(lambda: self.new_socket_slot(self.serverB, self.lineEdit_B, self.DataB))
        self.serverC.newConnection.connect(lambda: self.new_socket_slot(self.serverC, self.lineEdit_C, self.DataC))

    def write_data(self, sock, str):
        sock.write(str.encode())

    def prove(self, sock, line, str):
        data = sock.read(100)
        line.setText(data.decode())
        str.data += data
        print(data)
        print("str:", str.data)
        print("self.DataA:", self.DataA.data)

    def new_socket_slot(self, server, line, str):
        print("yes")
        sock = server.nextPendingConnection()
        self.sockets.append(sock)
        sock.readyRead.connect(lambda: self.prove(sock, line, str))
        sock.disconnected.connect(sock.close)

    def send_to_user(self, data, port):
        sock = QTcpSocket(self)
        sock.connectToHost(QHostAddress.LocalHost, port)
        print(data)
        sock.connected.connect(lambda: sock.write(data))

    def send_to_user1(self, data):
        sock = QTcpSocket(self)
        sock.connectToHost(QHostAddress.LocalHost, 7777)
        sock.connected.connect(lambda: sock.write(data.encode()))

    def write_data1(self, data):
        self.sock.write(data.encode)

    def closeEvent(self, event):
        self.serverA.close()
        self.serverB.close()
        self.serverC.close()
        for i in self.sockets:
            i.close()
        event.accept()

    def cut(self, sock):
        length = 10
        cutA = split_string_by_length(self.DataA.data.decode(), length)
        cutB = split_string_by_length(self.DataB.data.decode(), length)
        cutC = split_string_by_length(self.DataC.data.decode(), length)
        lengthA = len(cutA)
        lengthB = len(cutB)
        lengthC = len(cutC)
        i = 0

        def label(i, lengthA, lengthB, lengthC):
            num = random.randint(0, 1)
            if num == 0:
                QTimer.singleShot(1000, lambda: label(i, lengthA, lengthB, lengthC))
            else:
                if i == 10:
                    return
                str = 'A:'
                if lengthA > 0:
                    str += cutA[i]
                    self.send_to_user1(str)
                    lengthA -= 1
                    QTimer.singleShot(400, lambda: label1(i, lengthA, lengthB, lengthC))
                else:
                    QTimer.singleShot(400, lambda: label1(i, lengthA, lengthB, lengthC))


        def label1(i, lengthA, lengthB, lengthC):
            str = 'B:'
            if lengthB > 0:
                str += cutB[i]
                self.send_to_user1(str)
                lengthB -= 1
                QTimer.singleShot(400, lambda: label2(i, lengthA, lengthB, lengthC))
            else:

                QTimer.singleShot(400, lambda: label2(i, lengthA, lengthB, lengthC))

        def label2(i, lengthA, lengthB, lengthC):
            str = 'C:'
            if lengthC > 0:
                str += cutC[i]
                self.send_to_user1(str)
                lengthC -= 1
                i += 1
                QTimer.singleShot(300, lambda: label(i, lengthA, lengthB, lengthC))
            else:
                i += 1
                QTimer.singleShot(300, lambda: label(i, lengthA, lengthB, lengthC))

        label(i, lengthA, lengthB, lengthC)
        self.DataA.data= b""
        self.DataB.data = b""
        self.DataC.data = b""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Server()
    demo.move(1000,750)
    demo.show()
    demo.pushButton.clicked.connect(lambda: demo.cut(demo.sock))
    sys.exit(app.exec_())
