import sys
import os
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem, QDialog, QMessageBox
from PyQt5 import uic

from UI.main_ui import Ui_MainWindow
from UI.addEditCoffeeForm_ui import Ui_AddEditCoffeeForm

class AddEditCoffeeForm(QDialog, Ui_AddEditCoffeeForm):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        self.setupUi(self)

        self.conn = parent.conn
        self.coffee_id = coffee_id

        self.saveButton.clicked.connect(self.saveCoffee)
        self.cancelButton.clicked.connect(self.reject)

        if coffee_id is not None:
            self.loadCoffeeData()

    def loadCoffeeData(self):
        query = "SELECT `name of the variety`, `degree of roasting`, `ground/in grains`, `description of taste`, `price`, `volume` FROM espresso WHERE ID = ?"
        cur = self.conn.cursor()
        cur.execute(query, (self.coffee_id,))
        row = cur.fetchone()
        if row:
            self.sortNameLineEdit.setText(row[0])
            self.roastLevelLineEdit.setText(row[1])
            self.typeLineEdit.setText(row[2])
            self.flavorDescriptionTextEdit.setPlainText(row[3])
            self.priceLineEdit.setText(str(row[4]))
            self.packageVolumeLineEdit.setText(str(row[5]))

    def saveCoffee(self):
        sort_name = self.sortNameLineEdit.text()
        roast_level = self.roastLevelLineEdit.text()
        type_ = self.typeLineEdit.text()
        flavor_description = self.flavorDescriptionTextEdit.toPlainText()
        price = self.priceLineEdit.text()
        package_volume = self.packageVolumeLineEdit.text()

        cur = self.conn.cursor()
        try:
            if self.coffee_id is None:
                query = "INSERT INTO espresso (`name of the variety`, `degree of roasting`, `ground/in grains`, `description of taste`, `price`, `volume`) VALUES (?, ?, ?, ?, ?, ?)"
                cur.execute(query, (sort_name, roast_level, type_, flavor_description, price, package_volume))
            else:
                query = "UPDATE espresso SET `name of the variety` = ?, `degree of roasting` = ?, `ground/in grains` = ?, `description of taste` = ?, `price` = ?, `volume` = ? WHERE ID = ?"
                cur.execute(query, (sort_name, roast_level, type_, flavor_description, price, package_volume, self.coffee_id))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            QMessageBox.critical(self, 'Database Error', f'An error occurred with the database: {e}')
        finally:
            self.accept()
    
class Coffee(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDB()
        self.loadData()

    def initUI(self):
        self.setupUi(self)
        self.setWindowTitle("Coffee Database")

        self.addButton.clicked.connect(self.addNewCoffee)
        self.editButton.clicked.connect(self.editCoffee)

    def initDB(self):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        database_path = os.path.join(base_path, 'data', 'coffee.sqlite')
        
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()

    def loadData(self):
        self.cur.execute("SELECT ID, `name of the variety`, `degree of roasting`, `ground/in grains`, `description of taste`, `price`, `volume` FROM espresso")
        rows = self.cur.fetchall()

        self.configureTableWidget(rows)
        

    def configureTableWidget(self, rows):
        column_headers = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена', 'Объем упаковки']
        self.tableWidget.setColumnCount(len(column_headers))
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col) if col is not None else "")
                self.tableWidget.setItem(i, j, item)

    def addNewCoffee(self):
        dialog = AddEditCoffeeForm(self)
        if dialog.exec_() == QDialog.Accepted:
            self.loadData()

    def editCoffee(self):
        selected = self.tableWidget.currentRow()
        if selected >= 0:
            coffee_id = self.tableWidget.item(selected, 0).text()
            dialog = AddEditCoffeeForm(self, coffee_id)
            if dialog.exec_() == QDialog.Accepted:
                self.loadData()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    coffeeApp = Coffee()
    coffeeApp.show()
    sys.exit(app.exec_())