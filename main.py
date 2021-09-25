from __future__ import division, print_function, absolute_import, unicode_literals
import sys
import json
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QPushButton, QFileDialog,QTableWidgetItem, QMainWindow, QApplication, QDialog, QHeaderView
from flask.wrappers import Response
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem
from PyQt5.uic import loadUi
import images
import keyring
import os
import win32api
import win32print
import sys
import preview
import mail
import threading
import sqlite3 as sl
import subprocess
# with self.con:
        #     self.con.execute("""
        #         CREATE TABLE invoiceHistory (
        #             Number INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        #             Date DATE,
        #             Name VARCHAR,
        #             Phone BIGINT,
        #             Address VARCHAR,
        #             Price FLOAT,
        #             Orders VARCHAR
        #         );
        #     """)
WINDOW_SIZE = 0
class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('Dashboard.ui', self)
        self.row = 0
        self.totalPrice = 0
        self.ivNo = int(keyring.get_password('BillingNumber', 'invoice_number'))
        if self.ivNo is None:
            self.ivNo = 1000
            keyring.set_password('BillingNumber', 'invoice_number', self.ivNo)
        print(self.ivNo)
        self.invoiceNo.setText(str(self.ivNo))
        self.invoiceDate.setDate(QDate.currentDate())
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.show()
        self.con = sl.connect('my-test.db')
        with self.con:
            self.checkData = list(self.con.execute("SELECT Date, Number, Name, Phone, Price, Address, Type, Payment, Aadhar, Orders FROM invoiceHistory"))
        self.folderInvoiceHtml = "filesHtml/"
        self.folderInvoicePdf = "invoices/"
        self.createTable()
        self.createTable2()
        self.phone.textEdited.connect(self.updateFields)
        self.btn_close.clicked.connect(lambda: self.close())
        self.add.clicked.connect(lambda: self.getItem())
        self.submit.clicked.connect(lambda: self.createInvoice())
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_maximize_restore.clicked.connect(lambda: self.window_size())
        self.btn_toggle_menu.clicked.connect(self.menu)
        # self.paymentRadio.isChecked(lambda: self.accDetails.setFixedWidth(800))
        self.paymentRadio.toggled.connect(self.radioBtn)
        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

        self.frame_label_top_btns.mouseMoveEvent = moveWindow
        self.frame_grip.mouseMoveEvent = moveWindow

    def radioBtn(self, b):
        print("1")
        if b:
            self.accDetails.setFixedWidth(100)
        else:
            self.accDetails.setFixedWidth(0)
    # def ifKissan(self, switch):
    #     if switch:
    #         self.toUser = "Kissan"
    #     else:
    #         self.toUser = "Customer"

    # def ifPayment(self, checked):
    #     if checked:
    #         self.accDetails.setFixedWidth(800)
    #     else:
    #         self.paymentType = "Cash"

    def updateFields(self):
        print("3")
        if len(self.phone.text()) == 10:
            for r in self.checkData:
                if self.phone.text() == str(r[3]):
                    self.name.setText(r[2])
                    self.address.setText(r[5])
                    self.aadharNo.setText(str(r[8]))
                    if r[6] == "Kissan":
                        self.kissanSwitch.setChecked(False)
                    else:
                        self.kissanSwitch.setChecked(True)
                    if r[7] == "Cash":
                        self.paymentRadio.setChecked(False)
                    else:
                        self.paymentRadio.setChecked(True)
                        self.accDetails.setText(r[7])
                    items = json.loads(r[9].replace("'", '"'))
                    for item,r2 in zip(items, range(len(items))):
                        self.addItem(r2,item)
                        self.row +=1
                    break

    def getItemOfCurrent(self, table, col):
        print("6")
        if table == "invoiceHistoryTable":
            return self.invoiceHistoryTable.item(self.invoiceHistoryTable.currentRow(),col).text()
        elif table == "itemTable":
            return self.itemTable.item(self.itemTable.currentRow(),col).text()
        else:
            pass

    def createTable(self):
        print("1")
        col = ['Item', 'Quantity', 'Rate/Kg', 'Total', 'Action']
        self.itemTable.setRowCount(0)
        self.itemTable.setColumnCount(5)
        self.itemTable.setHorizontalHeaderLabels(col)
        self.itemTable.horizontalHeader().setMinimumSectionSize(60)
        self.itemTable.horizontalHeader().setStretchLastSection(True)
        self.itemTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def createTable2(self):
        print("2")
        col = ['Date', 'Invoice Number','Name', 'Phone', 'Total', 'Address', 'Type', 'Payment', 'Aadhar','Open', 'Print', 'Send']
        self.invoiceHistoryTable.setRowCount(0)
        self.invoiceHistoryTable.setColumnCount(12)
        self.invoiceHistoryTable.setHorizontalHeaderLabels(col)
        self.invoiceHistoryTable.horizontalHeader().setMinimumSectionSize(60)
        self.invoiceHistoryTable.horizontalHeader().setStretchLastSection(True)
        self.invoiceHistoryTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.getInvoiceHistory()
        
    def getItem(self):
        print("5")
        itemData = []
        itemData.append(str(self.itemList.currentItem().text(0)))
        itemData.append(float(int(self.kgQuantity.text()) + int(self.gmQuantity.text())/1000))
        itemData.append(float(self.rate.text()))
        itemData.append(float(itemData[1] * float(self.rate.text())))
        self.addItem(self.row, itemData)
        self.row += 1
        self.itemReset()

    def addItem(self, rowing,itemData):
        print("4")
        rowPosition = self.itemTable.rowCount()
        self.itemTable.insertRow(rowPosition)
        for i,c in zip(itemData, range(len(itemData))):
            self.itemTable.setItem(rowing, c, QTableWidgetItem(str(i)))
            self.removeItem = QPushButton(self.itemTable)
            self.removeItem.setText("Remove")
            self.itemTable.setCellWidget(rowing, 4, self.removeItem)
            self.removeItem.clicked.connect(lambda: self.deleteItem())
            if c == 3:
                self.totalPrice += float(i)
                self.total.setText(str(self.totalPrice))
        
    
    def deleteItem(self):
        print("9")
        self.itemTable.removeRow(self.itemTable.currentRow())
        self.row -= 1

    def readTable(self):
        print("8")
        self.ord = []
        self.ord.append(self.invoiceNo.text())
        print("order no: ", self.invoiceNo.text())
        self.ord.append(self.invoiceDate.date().toString("dd.MM.yyyy"))
        self.ord.append(self.name.text())
        self.ord.append(self.phone.text())
        self.ord.append(self.address.text())
        rows = self.itemTable.rowCount()
        self.orders = []
        for r in range(rows):
            oneRow = []
            for c in range(4):
                try:
                    oneRow.append(self.itemTable.item(r,c).text())
                except:
                    break
            self.orders.append(oneRow)
        self.ord.append(sum([float(x[3]) for x in self.orders]))
        if self.kissanSwitch.isChecked():
            self.ord.append("Kissan")
        else:
            self.ord.append("User")
        if self.paymentRadio.isChecked():
            self.ord.append(self.accDetails.text())
        else:
            self.ord.append("Cash")
        self.ord.append(self.aadharNo.text())
        self.ord.append(str(self.orders))
        self.total.setText(str(self.ord[5]))
        self.html = preview.run(list(self.ord[:-1]), self.orders)

    def createInvoice(self):
        print("7")
        self.readTable()
        f = open(f"{self.folderInvoiceHtml}{self.ivNo}.html", "a")
        f.write(self.html)
        f.close()
        self.invoicePreview.load(QtCore.QUrl.fromLocalFile(os.path.abspath(f"{self.folderInvoiceHtml}{self.ivNo}.html")))
        self.invoicePreview.loadFinished.connect(self.emit_pdf)
        self.printing(f"{self.folderInvoicePdf}{self.ivNo}.pdf")
        self.toInvoiceHistory()
        self.finish()
        
    def emit_pdf(self):
        print("6")
        self.invoicePreview.show()
        self.invoicePreview.page().printToPdf(f"{self.folderInvoicePdf}{self.ivNo}.pdf")
        # self.printing(f"{self.folderInvoicePdf}{self.ivNo}.pdf")
        # self.toInvoiceHistory()
        # self.finish()
        
    def printing(self, invoicepdf):
        print("21")
        try:
            win32api.ShellExecute(0, "print", invoicepdf, win32print.GetDefaultPrinter(), ".", 0)
        except:
            print("niklo")

    def toInvoiceHistory(self):
        print("22")
        sql = 'INSERT OR REPLACE INTO invoiceHistory (Number, Date, Name, Phone, Address, Price, Type, Payment, Aadhar, Orders) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        data = []
        data.append(self.ord)
        print("##############\n", data, "\n##############")
        with self.con:
            self.con.executemany(sql, data)

    def mailingto(self, mailto, cusDetails, invoicePdf):
        print("23")
        t = threading.Thread(target=mail.mailing, args=[mailto, cusDetails, invoicePdf])
        t.start()

    def finish(self):
        print("32")
        self.mailingto("er.salilagrawal@gmail.com", list(self.ord[:-1]), f"{self.folderInvoicePdf}{self.ivNo}.pdf")
        self.ivNo += 1
        self.reset()
        self.itemTable.setRowCount(0)
        keyring.set_password('BillingNumber', 'invoice_number', self.ivNo)
        self.getInvoiceHistory()
        
    def getInvoiceHistory(self):
        print("43")  
        with self.con:
            data = list(self.con.execute("SELECT Date, Number, Name, Phone, Price, Address, Type, Payment, Aadhar FROM invoiceHistory"))
            self.invoiceHistoryTable.setRowCount(len(data))
            for r,rc in zip(data, range(len(data))):
                for c,cc in zip(r, range(len(r))):
                    self.invoiceHistoryTable.setItem(rc, cc, QTableWidgetItem(str(c)))
                self.openInvoice = QPushButton(self.invoiceHistoryTable)
                self.openInvoice.setText("Open")
                self.invoiceHistoryTable.setCellWidget(rc, 9, self.openInvoice)
                self.openInvoice.clicked.connect(lambda: self.openPdfThreading())
                self.printInvoice = QPushButton(self.invoiceHistoryTable)
                self.printInvoice.setText("Print")
                self.invoiceHistoryTable.setCellWidget(rc, 10, self.printInvoice)
                self.printInvoice.clicked.connect(lambda: self.printingThreading(f"{os.getcwd()}\\invoices\\{self.getItemOfCurrent('invoiceHistoryTable', 1)}.pdf"))  
                self.sendInvoice = QPushButton(self.invoiceHistoryTable)
                self.sendInvoice.setText("Send")
                self.invoiceHistoryTable.setCellWidget(rc, 11, self.sendInvoice)
                self.sendInvoice.clicked.connect(lambda: self.mailingto("er.salilagrawal@gmail.com", [self.getItemOfCurrent('invoiceHistoryTable', 1), self.getItemOfCurrent('invoiceHistoryTable', 0), self.getItemOfCurrent('invoiceHistoryTable', 2)], f"{os.getcwd()}\\invoices\\{self.invoiceHistoryTable.item(self.invoiceHistoryTable.currentRow(),1).text()}.pdf"))  

    def openPdf(self):
        print("34")
        # os.system(f"{os.getcwd()}\\invoices\\{self.getItemOfCurrent('invoiceHistoryTable', 1)}.pdf")
        subprocess.Popen([f"{os.getcwd()}\\invoices\\{self.getItemOfCurrent('invoiceHistoryTable', 1)}.pdf"], shell=True)

    def openPdfThreading(self):
        print("54")
        th = threading.Thread(target=self.openPdf, args=[])
        th.start()

    def printingThreading(self, invoicePdf):
        print("45")
        th = threading.Thread(target=self.printing, args=[invoicePdf])
        th.start()

    def reset(self):
        print("65")
        self.row = 0
        self.totalPrice = 0
        self.name.clear()
        self.phone.clear()
        self.address.clear()
        self.invoiceNo.setText(str(self.ivNo))
        self.invoiceDate.setDate(QDate.currentDate())
        self.total.clear()
        self.itemReset()
        
    def itemReset(self):
        print("56")    
        self.kgQuantity.clear()
        self.gmQuantity.clear()
        self.rate.clear()

    def menu(self):
        print("77")
        # global name, short_name
        if self.btn_toggle_menu.isChecked():
            self.frame_left_menu.setMaximumWidth(140)
            self.frame_toggle.setMaximumWidth(126)
            # self.label_8.setText(name.capitalize())
        else:
            # self.label_8.setText(short_name.upper())
            self.frame_left_menu.setMaximumWidth(60)
            self.frame_toggle.setMaximumWidth(60)

    def window_size(self):
        print("66")
        if self.btn_maximize_restore.isChecked():
            self.restore_or_maximize_window()
            self.btn_maximize_restore.setStyleSheet("QPushButton {	border: none; background-position: center; background-color: transparent; background-image: url(:/16x16/icons/16x16/cil-window-restore.png);  background-repeat: no-repeat; } QPushButton:hover { background-color: rgb(52, 59, 72); } QPushButton:pressed {background-color: rgb(85, 170, 255); }")
        else:
            self.restore_or_maximize_window()
            self.btn_maximize_restore.setStyleSheet(
                "QPushButton {	border: none; background-position: center; background-color: transparent; background-image: url(:/16x16/icons/16x16/cil-window-maximize.png);  background-repeat: no-repeat; } QPushButton:hover { background-color: rgb(52, 59, 72); } QPushButton:pressed {background-color: rgb(85, 170, 255); }")

    def mousePressEvent(self, event):
        print("87")
        self.clickPosition = event.globalPos()

    def restore_or_maximize_window(self):
        print("78")
        global WINDOW_SIZE
        win_status = WINDOW_SIZE
        if win_status == 0:
            WINDOW_SIZE = 1
            self.showMaximized()
        else:
            WINDOW_SIZE = 0
            self.showNormal()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
