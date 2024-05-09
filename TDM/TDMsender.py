
import sys
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtNetwork import QTcpServer,QTcpSocket, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMainWindow
from ui import user_send
class Client(QMainWindow,user_send.Ui_MainWindow):
    def __init__(self,port,name):
        super(Client, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(name)
        self.sock = QTcpSocket(self)
        self.sock.connectToHost(QHostAddress.LocalHost, port)
        #str1="connect!"
        #self.sock.connected.connect(lambda :self.write_data(self.sock, str1))
    def write_data(self,sock,str):
        sock.write(str.encode())
    def write_data1(self,sock):
        str2=self.lineEdit.text()
        sock.write(str2.encode())
    def closeEvent(self, event):
        self.sock.close()
        self.sockmedium.close()
        self.sockhigh.close()
        event.accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo1 = Client(6666,"clientA")
    demo1.move(200,1000)
    demo1.show()
    demo1.pushButton.clicked.connect(lambda :demo1.write_data1(demo1.sock))
    demo2 = Client(6667, "clientB")
    demo2.move(1000,1000)
    demo2.show()
    demo2.pushButton.clicked.connect(lambda: demo2.write_data1(demo2.sock))
    demo3 = Client(6668, "clientC")
    demo3.move(1800,1000)
    demo3.show()
    demo3.pushButton.clicked.connect(lambda: demo3.write_data1(demo3.sock))
    sys.exit(app.exec_())