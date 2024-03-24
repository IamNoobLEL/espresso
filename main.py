import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem
from PyQt5 import uic

class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDB()
        self.loadData()

    def initUI(self):
        uic.loadUi('main.ui', self)
        self.setWindowTitle("Coffee")

    def initDB(self):
        self.conn = sqlite3.connect("coffee.sqlite")
        self.cur = self.conn.cursor()

    def loadData(self):
        self.cur.execute("SELECT * FROM espresso")
        rows = self.cur.fetchall()

        self.configureTableWidget(rows)

    def configureTableWidget(self, rows):
        column_headers = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах',
                          'Описание вкуса', 'Цена', 'Объем упаковки']
        self.tableWidget.setColumnCount(len(column_headers))
        self.tableWidget.setRowCount(len(rows))

        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(col)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    coffeeApp = Coffee()
    coffeeApp.show()
    sys.exit(app.exec_())