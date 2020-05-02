import sys
import numpy as np
import pandas as pd
from PyQt5 import QtGui, QtWidgets, QtCore
from Ui_scripts import Ui_MainWindow


class Main(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.file_selection_check()
        self.stop_btn.setDisabled(True)

        # btn/treeview
        self.selectFolder_toolButton.clicked.connect(self.GetDir)
        self.start_btn.clicked.connect(self.startMonitoring)
        self.stop_btn.clicked.connect(self.stopMonitoring)
        self.plot_btn.clicked.connect(self.plotSelected)
        self.export_btn.clicked.connect(self.exportXLSX)
        self.clear_btn.clicked.connect(self.clearPlot)
        self.folder_tree.clicked.connect(self.on_folder_tree_clicked)

        # config PlotWidgets
        self.plot_steam_temp.setTitle("Steam Heater Temperature against Time ")
        self.plot_steam_temp.setLabel("left", "Temperature (°C)")
        self.plot_steam_temp.setLabel("bottom", "Seconds after Start")
        self.plot_steam_temp.setYRange(0, 200, padding=0)
        self.plot_steam_temp.setMouseEnabled(x=True, y=False)

        self.plot_tip_temp.setLabel("left", "Temperature (°C)")
        self.plot_tip_temp.setLabel("bottom", "Seconds after Start")
        self.plot_tip_temp.setTitle("Tip Temperature against Time")
        self.plot_tip_temp.setYRange(0, 200, padding=0)
        self.plot_tip_temp.setMouseEnabled(x=True, y=False)

    def file_selection_check(self):
        global file_selected
        file_selected = False

    def GetDir(self):
        path = QtGui.QFileDialog.getExistingDirectory(
            self, "Select Directory")
        filter = ["*.dat"]
        self.directoryPath_lineEdit.setText(path)
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.model.setNameFilters(filter)
        self.model.setNameFilterDisables(0)
        self.folder_tree.setModel(self.model)
        self.folder_tree.setRootIndex(self.model.index(path))
        self.folder_tree.setSortingEnabled(True)

    def on_folder_tree_clicked(self):
        global file_selected
        index = self.folder_tree.currentIndex()
        file_path = self.model.filePath(index)
        file_name = self.model.fileName(index)
        file_path_str = str(file_path)
        self.status_lineEdit.setText(file_name)

        if ".dat" in file_path_str:
            file_selected = True
            return file_selected
        else:
            file_selected = False
            return file_selected

    def startMonitoring(self):
        if file_selected is True:
            self.timer = QtCore.QTimer()
            self.timer.setInterval(50)
            self.timer.timeout.connect(self.update_graph)
            self.timer.start()

            self.selectFolder_toolButton.setDisabled(True)
            self.start_btn.setDisabled(True)
            self.stop_btn.setDisabled(False)
            self.plot_btn.setDisabled(True)
            self.export_btn.setDisabled(True)
            self.clear_btn.setDisabled(True)
            self.folder_tree.setDisabled(True)

        else:
            self.status_lineEdit.setText("ERROR: FILE NOT SELECTED")

    def update_graph(self):
        index = self.folder_tree.currentIndex()
        file_path = self.model.filePath(index)
        date, time, sec, tip_temp, steam_temp = np.genfromtxt(
            file_path, dtype=str, delimiter=",", skip_header=1, unpack=True)
        sec = sec.astype(float)
        tip_temp = tip_temp.astype(float)
        steam_temp = steam_temp.astype(float)

        self.plot_tip_temp.plot(sec, tip_temp)
        self.plot_steam_temp.plot(sec, steam_temp)

    def stopMonitoring(self):
        self.timer.stop()
        self.start_btn.setDisabled(False)
        self.stop_btn.setDisabled(True)
        self.plot_btn.setDisabled(False)
        self.export_btn.setDisabled(False)
        self.clear_btn.setDisabled(False)
        self.folder_tree.setDisabled(False)

    def plotSelected(self):
        if file_selected is True:
            index = self.folder_tree.currentIndex()
            file_path = self.model.filePath(index)
            date, time, sec, tip_temp, steam_temp = np.genfromtxt(
                file_path, dtype=str, delimiter=",", skip_header=1, unpack=True)
            sec = sec.astype(float)
            tip_temp = tip_temp.astype(float)
            steam_temp = steam_temp.astype(float)

            self.plot_tip_temp.plot(sec, tip_temp)
            self.plot_steam_temp.plot(sec, steam_temp)

        else:
            self.status_lineEdit.setText("ERROR: FILE NOT SELECTED")

    def exportXLSX(self):
        if file_selected is True:
            index = self.folder_tree.currentIndex()
            file_path = self.model.filePath(index)
            file_name = self.model.fileName(index)
            file_name_mod = file_name[:-4] + ".xlsx"
            # print(file_name_mod)
            date, time, sec, tip_temp, steam_temp = np.genfromtxt(
                file_path, dtype=str, delimiter=",", skip_header=1, unpack=True)
            sec = sec.astype(float)
            tip_temp = tip_temp.astype(float)
            steam_temp = steam_temp.astype(float)
            data = [date, time, sec, tip_temp, steam_temp]
            data_pd = pd.DataFrame(data)
            data_pd = data_pd.T
            export_excel = pd.ExcelWriter(file_name_mod, engine="xlsxwriter")
            data_pd.to_excel(export_excel, sheet_name=file_name)
            export_excel.save()

        else:
            self.status_lineEdit.setText("ERROR: FILE NOT SELECTED")

    def clearPlot(self):
        self.status_lineEdit.setText("Plot Cleared")
        self.plot_steam_temp.clear()
        self.plot_tip_temp.clear()


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
