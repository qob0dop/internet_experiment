import sys
import time
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QTextCursor
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from ui import FMDs


class Server(QMainWindow, FMDs.Ui_MainWindow):
    def __init__(self):
        super(Server, self).__init__()
        self.setupUi(self)
        self.server = QTcpServer(self)
        self.sockets = []
        if not self.server.listen(QHostAddress.LocalHost, 7777):
            print(self.server.errorString())
        self.server.newConnection.connect(lambda: self.new_socket_slot(self.server, self.textEdit, 7777))

    def prove(self, sock, line):
        data = sock.readAll().data().decode()
        cursor = line.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(data)
        cursor.movePosition(QTextCursor.End)
        cursor.insertText("\n")
        if data[0] == 'A':
            rdata = data.replace("A:", "")
            self.send_to_user(rdata, 8887)
        elif data[0] == 'B':
            rdata = data.replace("B:", "")
            self.send_to_user(rdata, 8888)
        elif data[0] == 'C':
            rdata = data.replace("C:", "")
            self.send_to_user(rdata, 8889)

    def new_socket_slot(self, server, line, port):
        print("yres1")
        sock = server.nextPendingConnection()
        self.sockets.append(sock)
        sock.readyRead.connect(lambda: self.prove(sock, line))

        sock.disconnected.connect(sock.close)

    def send_to_user(self, data, port):
        sock = QTcpSocket(self)
        sock.connectToHost(QHostAddress.LocalHost, port)
        sock.connected.connect(lambda: sock.write(data.encode()))

    def send_to_user1(self, data):
        sock = QTcpSocket(self)
        sock.connectToHost(QHostAddress.LocalHost, 8887)
        sock.connected.connect(lambda: sock.write(data.encode()))

    def closeEvent(self, event):
        self.serverlow.close()
        self.servermedium.close()
        self.serverhigh.close()
        for i in self.sockets:
            i.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Server()
    demo.show()
    sys.exit(app.exec_())
