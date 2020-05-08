from PySide2.QtCore import QRect, Slot, qApp, QDir
from PySide2.QtWidgets import QMainWindow, QAction, QFileDialog, QInputDialog, QLineEdit, QMessageBox
import os
import pandas as pd
import xlsxwriter
import numpy as np
# Import scikit-learn for machine learning
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn import metrics

class MainWindow(QMainWindow):
    # Build a vectorizer that splits strings into sequence of 1 to 3
    # characters instead of word tokens
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), analyzer='char', use_idf=True)

    pipeline = Pipeline([
        ('vect', vectorizer),
        ('clf', LinearSVC()),
    ])

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("ATS Assistant")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        ## Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        ## Select File QAction
        open_action = QAction("Open Drop", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.openDrop)

        self.file_menu.addAction(open_action)
        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

    def openDrop(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self, self.tr("Open Drop"), "", self.tr("All Files (*);;Excel Files (*.xlsx)"), options=options)
        if fileName:
            self.mail_drop_file = os.path.basename(fileName[0])
            self.file_name = os.path.splitext(self.mail_drop_file)[0]
            self.file_ext = os.path.splitext(self.mail_drop_file)[1]
            print(self.file_ext)
            if self.file_ext == ".xlsx":
                self.initMachineLearning()
    
    def initMachineLearning(self):
        # Hardcode data for machine learning (Maybe read from internet?)
        data = [
            ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Plaintiff', 'Creditor'], ['Filing NUMBER', 'Filingnum'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['Respond by', 'Respondby'], ['Number', 'Phone'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Plaintiff', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['Number', 'Phone'], ['Respond by', 'Respondby'], ['Filing Number', 'Filingnum'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['S', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Filingnum', 'Filingnum'], ['Phone', 'Phone'], ['respond by', 'Respondby'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Filingnum', 'Filingnum'], ['Phone', 'Phone'], ['Respondby', 'Respondby'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St ', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Filingnum', 'Filingnum'], ['Phone', 'Phone'], ['RespondBy', 'Respondby'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Phone', 'Phone'], ['Filingnum', 'Filingnum'], ['Respondby', 'Respondby'], ['First', 'First'], ['Last', 'Last'], ['Address', 'Address'], ['CITY', 'City'], ['ST', 'St'], ['ZIP', 'Zip'], ['LienTYPE', 'Lientype'], ['CREDITOR', 'Creditor'], ['AMOUNTT', 'Amount'], ['Filingnum', 'Filingnum'], ['FILEDATE', 'Filingdate'], ['respondby', 'Respondby'], ['Phone', 'Phone'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['respondby', 'Respondby'], ['Phone', 'Phone'], ['Filingnum', 'Filingnum'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Filingnum', 'Filingnum'], ['Phone', 'Phone'], ['Respondby', 'Respondby'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['Ste', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['Phone', 'Phone'], ['Respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St ', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Phone', 'Phone'], ['Filingnum', 'Filingnum'], ['Respondby', 'Respondby'], ['First Name', 'First'], ['Last Name', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['Number', 'Phone'], ['Respond by', 'Respondby'], ['First Name', 'First'], ['Last Name', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['number', 'Phone'], ['respond by', 'Respondby'], ['First Name', 'First'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['Number', 'Phone'], ['Respond By ', 'Respondby'], ['First Name', 'First'], ['Last Name', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['Respond by', 'Respondby'], ['First Name', 'First'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['Phone Number', 'Phone'], ['Respond By', 'Respondby'], ['First Name', 'First'], ['Last Name', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['number', 'Phone'], ['respond by', 'Respondby'], ['First Name', 'First'], ['Last Name', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['Respond by ', 'Respondby'], ['Number', 'Phone'], ['First Name', 'First'], ['Last Name', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['respond by', 'Respondby'], ['Number', 'Phone'], ['First Name', 'First'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['number', 'Phone'], ['respond by', 'Respondby'], ['First Name', 'First'], ['Last Name', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['number', 'Phone'], ['Respond by', 'Respondby'], ['First Name', 'First'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['respond by', 'Respondby'], ['Number', 'Phone'], ['First Name', 'First'], ['Last Name', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['Respond by', 'Respondby'], ['Number', 'Phone'], ['First Name', 'First'], ['Last Name', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['respond by', 'Respondby'], ['Number', 'Phone'], ['First Name', 'First'], ['Last Name', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['Respond by', 'Respondby'], ['Number ', 'Phone'], ['First Name', 'First'], ['Last Name', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['respond by ', 'Respondby'], ['Number', 'Phone'], ['10% amount', 'M_10amount'], ['15% amount', 'M_15amount'], ['10 amount', 'M_10amount'], ['15 amount', 'M_15amount'], ['10%amount', 'M_10amount'], ['15%amount', 'M_15amount'], ['10amount', 'M_10amount'], ['15amount', 'M_15amount'], ['10% amountt', 'M_10amount'], ['15% amountt', 'M_15amount'], ['total', 'totalamount'], ['ttotal', 'totalamount'], ['First ', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St ', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Phone', 'Phone'], ['Filingnum', 'Filingnum'], ['Respondby', 'Respondby'], ['First', 'First'], ['Last ', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['phone ', 'Phone'], ['respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['respondby ', 'Respondby'], ['phone', 'Phone'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St ', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['phone', 'Phone'], ['respondby ', 'Respondby'], ['filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St ', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Phone', 'Phone'], ['Filingnum', 'Filingnum'], ['respondby', 'Respondby'], ['First', 'First'], ['Last', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['number', 'Phone'], ['respond by', 'Respondby'], ['filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['10% amount', 'M_10amount'], ['15% amount', 'M_15amount'], ['Total', 'totalamount'], ['Phone', 'Phone'], ['Respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['10% amount', 'M_10amount'], ['15% amount', 'M_15amount'], ['total', 'totalamount'], ['Phone', 'Phone'], ['Respond by', 'Respondby'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['number', 'Phone'], ['respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['respondby ', 'Respondby'], ['Phone', 'Phone'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St ', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['phone ', 'Phone'], ['Respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Phone ', 'Phone'], ['Respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St ', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Phone ', 'Phone'], ['Respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Phone ', 'Phone'], ['Respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Phone ', 'Phone'], ['Respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['Phone ', 'Phone'], ['Respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['First Name', 'First'], ['Full Name', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['State ', 'St'], ['Zip+4', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Phone', 'Phone'], ['Respond By', 'Respondby'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Phone ', 'Phone'], ['Respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St ', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Phone ', 'Phone'], ['Respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['respond by', 'Respondby'], ['Phone', 'Phone'], ['Filingnum', 'Filingnum'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['Filingnum', 'Filingnum'], ['Phone', 'Phone'], ['Respondby', 'Respondby'], ['First', 'First'], ['Last', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St ', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['LienType', 'Lientype'], ['Creditor ', 'Creditor'], ['FilingDate', 'Filingdate'], ['Amount', 'Amount'], ['Phone', 'Phone'], ['Respondby', 'Respondby'], ['Filingnum', 'Filingnum'], ['First ', 'First'], ['Last ', 'Last'], ['FullName', 'Fullname'], ['Address', 'Address'], ['City', 'City'], ['St', 'St'], ['Zip', 'Zip'], ['County', 'County'], ['Lien Type', 'Lientype'], ['Creditor ', 'Creditor'], ['Filing Date', 'Filingdate'], ['Amount', 'Amount'], ['respondby', 'Respondby'], ['phone', 'Phone'], ['Filingnum', 'Filingnum']
            ]
        training_df = pd.DataFrame(data, columns = ['Given_Header', 'Adjusted_Header'])
        X = training_df['Given_Header']
        y = training_df['Adjusted_Header']
        if y.isnull().any():
            print("Some fields are missing in the training file.")
            exit()

        # Fit pipeline to training data
        self.pipeline.fit(X, y)
        self.getMailDate()
    
    def getMailDate(self):
        self.mail_date_input, ok = QInputDialog().getText(self, "Mail Date",
                                     "Enter the mailing date of this job(format is \"Month Day Year\" with no comma after day)", QLineEdit.Normal,
                                     self.mail_drop_file)
        if ok:
            if self.mail_date_input:
                # textLabel.setText(text)
                print(self.mail_date_input)
        else:
            if self.alert("Alert", "Please re-enter the Mail Date") == "ok":
                self.getMailDate()
                # print("Alert was ok")
            else:
                print("User cancelled import")
            # msg = self.alert()
            # msg.open()

    def alert(self, title, content):
        buttonReply = QMessageBox.question(self, title, content, QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        # print(int(buttonReply))
        if buttonReply == QMessageBox.Ok:
            # print('Ok clicked.')
            return "ok"
        if buttonReply == QMessageBox.Cancel:
            # print('Cancel')
            return "cancel"

    @Slot()
    def exit_app(self, checked):
        sys.exit()