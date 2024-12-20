from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import pandas as pd
import globaldata as gd
import fileanalysis as fa
import styles as st

class FirstPage(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = main_window
        self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut.activated.connect(self.startButtonClicked)

        label = QLabel("Select a CSV file to edit")
        font = QFont()
        font.setPointSize(26)
        label.setFont(font)

        fileselect = QPushButton("Browse Files")
        fileselect.clicked.connect(self.startButtonClicked)
        fileselect.setFixedSize(150, 30)
        fileselect.setStyleSheet(st.browseFiles)
        
        layout = QVBoxLayout()
        layout.addStretch(10)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(fileselect, alignment=Qt.AlignCenter)
        layout.addStretch(10)
        self.setLayout(layout)

    def startButtonClicked(self):
        gd.file_path, _ = QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser("~/Downloads"), "CSV Files (*.csv)")
        if gd.file_path:
            gd.df = pd.read_csv(gd.file_path, dtype="object", keep_default_na=False, header=None)
            gd.df = gd.df.where(pd.notna(gd.df), None)
            self.main_window.secondPageSetup()

        else:
            print("Failed to find filepath")


class CSVPage(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut.activated.connect(self.saveButtonClicked)
        self.shortcut2 = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut2.activated.connect(self.backButtonClicked)

        table = QTableWidget()
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setMinimumSize(900, 500)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setRowCount(gd.df.shape[0])
        table.setColumnCount(gd.df.shape[1]) 
        table.setStyleSheet(st.tableGrid) 

        # Populate Table
        for row in range(gd.df.shape[0]):
            for col in range(gd.df.shape[1]):
                table.setItem(row, col, QTableWidgetItem(str(gd.df.iat[row, col])))

        # Updates the dataframe with any changes made
        def updateDataframe(row, col):
            newValue = table.item(row, col).text()
            gd.df.iat[row, col] = newValue

        table.cellChanged.connect(updateDataframe)

        button = QPushButton("Go back")
        button2 = QPushButton("Save and Exit")
        button3 = QPushButton("File Analysis")
        button.clicked.connect(self.backButtonClicked)
        button2.clicked.connect(self.saveButtonClicked)
        button3.clicked.connect(self.analysisButtonClicked)
        button.setMaximumWidth(180)
        button2.setMaximumWidth(180)
        button3.setMaximumWidth(180)

        layout = QVBoxLayout() 
        layout.addWidget(table)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(4)
        buttonLayout.addWidget(button)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(button3)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(button2)
        buttonLayout.addStretch(4)

        layout.addLayout(buttonLayout)
        layout.setContentsMargins(0, 0, 0, 15)
        self.setLayout(layout)


    def backButtonClicked(self):
        self.main_window.mainwidget.setCurrentIndex(0)
        self.main_window.mainwidget.removeWidget(self.main_window.page2)

    def analysisButtonClicked(self):
        self.main_window.thirdPageSetup()
        self.main_window.mainwidget.setCurrentIndex(2)

    def saveButtonClicked(self):
        gd.df.to_csv(gd.file_path, index=False, header=None)
        QApplication.quit()


class AnalysisPage(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window

        rows, columns = fa.numAxis(gd.df)
        label1 = QLabel(f"Table has {rows} rows and {columns} columns")

        top3 = fa.mostPopular(gd.df)
        label2 = QLabel(f"There are {fa.numCells(gd.df)} cells in the file")
        label3 = QLabel(f"Most freqent cell values: \"{top3[0][0]}\" ({top3[0][1]} occurences), \"{top3[1][0]}\" ({top3[1][1]}) occurences, \"{top3[2][0]}\" ({top3[2][1]}) occurences.")
        button = QPushButton("Back")
        button.clicked.connect(self.back2Clicked)
        
        layout = QVBoxLayout()
        layout.addStretch(50)
        layout.addWidget(label1, alignment=Qt.AlignCenter)
        layout.addWidget(label2, alignment=Qt.AlignCenter)
        layout.addWidget(label3, alignment=Qt.AlignCenter)
        layout.addStretch(50)
        layout.addWidget(button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        

    def back2Clicked(self):
        self.main_window.mainwidget.setCurrentIndex(1)
        self.main_window.mainwidget.removeWidget(self.main_window.page3)

