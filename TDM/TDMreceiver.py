import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QTextCursor
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from ui import accept


def updateUi(sock, line):
    cursor = line.textCursor()
    cursor.movePosition(QTextCursor.End)
    cursor.insertText(sock.readAll().data().decode())


def new_socket_slot(win, server, line):
    win.sock = server.nextPendingConnection()
    sock = win.sock
    print("yes")

    sock.readyRead.connect(lambda: updateUi(sock, line))
    sock.disconnected.connect(sock.close)


class user(QMainWindow, accept.Ui_MainWindow):
    def __init__(self, port):
        super(user, self).__init__()
        self.setupUi(self)
        self.server = QTcpServer(self)
        if not self.server.listen(QHostAddress.LocalHost, port):
            print(self.server.errorString())
        self.server.newConnection.connect(lambda: new_socket_slot(self, self.server, self.textEdit))

    def closeEvent(self, event):
        self.server.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = user(8887)
    a.setWindowTitle("A")
    a.move(200, 0)
    a.show()
    b = user(8888)
    b.setWindowTitle("B")
    b.move(1000, 0)
    b.show()
    c = user(8889)
    c.setWindowTitle("C")
    c.move(1800, 0)
    c.show()
    sys.exit(app.exec_())
