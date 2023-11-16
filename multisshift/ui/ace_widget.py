# https://fonts.google.com/icons
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QVBoxLayout, QMenuBar,QStyleFactory
from PyQt6.QtGui import QIcon, QKeySequence, QAction
from PyQt6.QtCore import QSize
from multisshift.Library.editor import Editor
import os
import sys
class QtAceWidget(QtWidgets.QWidget):
    def __init__(self, peer_terminal=None, parent=None):
        super(QtAceWidget, self).__init__(parent)
        self.file_to_open = None
        self.setupUi()
        self.peer_terminal = peer_terminal

    def setupUi(self):

        self.setWindowTitle("Editor")
        self.resize(800, 600)

        self.layout = QVBoxLayout(self)
        self.layout.setObjectName("layout")

        self.createMenus()

        self.aceBrowser = Editor(self)
        self.aceBrowser.setMinimumSize(QSize(0, 400))
        self.layout.addWidget(self.aceBrowser)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setFixedHeight(25)
        self.layout.addWidget(self.statusbar)

    def createMenus(self):
        self.menuBar = QMenuBar(self)
        self.menuBar.setObjectName("menuBar")
        self.menuBar.setFixedHeight(25)
        self.layout.addWidget(self.menuBar)

        self.fileMenu = self.menuBar.addMenu("File")

        self.newAction = QAction(QIcon("icons/new.png"), "New", self)
        self.newAction.setShortcut(QKeySequence.StandardKey.New)
        self.newAction.setStatusTip("Create a new file")
        self.newAction.triggered.connect(self.newFile)
        self.fileMenu.addAction(self.newAction)

        self.openAction = QAction(QIcon("icons/open.png"), "Open", self)
        self.openAction.setShortcut(QKeySequence.StandardKey.Open)
        self.openAction.setStatusTip("Open an existing file")
        self.openAction.triggered.connect(self.openFile)
        self.fileMenu.addAction(self.openAction)

        self.saveAction = QAction(QIcon("icons/save.png"), "Save", self)
        self.saveAction.setShortcut(QKeySequence.StandardKey.Save)
        self.saveAction.setStatusTip("Save the current file")
        self.saveAction.triggered.connect(self.saveFile)
        self.fileMenu.addAction(self.saveAction)

        self.saveAsAction = QAction(QIcon("icons/saveas.png"), "Save As...", self)
        self.saveAsAction.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.saveAsAction.setStatusTip("Save the current file with a new name")
        self.saveAsAction.triggered.connect(self.saveFileAs)
        self.fileMenu.addAction(self.saveAsAction)

        self.exitAction = QAction(QIcon("icons/exit.png"), "Exit", self)
        self.exitAction.setShortcut(QKeySequence.StandardKey.Quit)
        self.exitAction.setStatusTip("Exit the application")
        self.exitAction.triggered.connect(self.close)
        self.fileMenu.addAction(self.exitAction)

        # self.codeMenu = self.menuBar.addMenu("Code")

        # self.runAction = QAction("Run", self)
        # self.runAction.setShortcut(QKeySequence("Ctrl+R"))  # Set the shortcut key as Ctrl+R
        # self.runAction.setStatusTip("Run the current script")
        # self.runAction.triggered.connect(self.runCode)
        # self.codeMenu.addAction(self.runAction)

    def runCode(self):
        # Implement your logic to run the script here
        full_path = os.path.abspath(self.file_to_open)
        parent_python = sys.executable
        print(f"Parent python interpreter: {sys.executable}")
        # Get the file extension
        _, extension = os.path.splitext(full_path)

        if self.peer_terminal is not None:
            if extension == '.py':
                # Run Python scripts with the Python interpreter
                # self.peer_terminal.backend.write_data(f"{sys.executable} {full_path}\r\n")
                self.peer_terminal.backend.write_data(f"python {full_path}\r\n")
            elif extension == '.bat':
                # Run batch scripts directly
                self.peer_terminal.backend.write_data(f"{full_path}\r\n")
            elif extension == '.ps1':
                # Run PowerShell scripts with the PowerShell interpreter
                self.peer_terminal.backend.write_data(f"powershell -File {full_path}\r\n")
            else:
                self.notify("runCode Error", f"Unsupported file type: {extension}")
        else:
            self.notify("runCode Error", "No Peer Terminal Window to run code in")

    def newFile(self):
        self.aceBrowser.page().runJavaScript("editor.setValue('');")
        self.file_to_open = None
        self.statusbar.showMessage("")

    def openFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_path:
            self.aceBrowser.loadFile(file_path)
            self.statusbar.showMessage(file_path)
            # self.aceBrowser.page().runJavaScript(f"editor.setValue(`{data}`);")

    def load(self, file_path=None):
        if file_path:
            self.aceBrowser.loadFile(file_path)
            self.statusbar.showMessage(file_path)


    def saveFile(self):
        if self.file_to_open:
            self.aceBrowser.page().runJavaScript("editor.getValue();", self.handleSaveResult(self.file_to_open))
        else:
            self.saveFileAs()

    def saveFileAs(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save As", "", "All Files (*)")
        if file_path:
            self.aceBrowser.page().runJavaScript("editor.getValue();", self.handleSaveAsResult(file_path))

    def handleSaveResult(self, file_path):
        def callback(result):
            if result:
                try:
                    with open(file_path, 'w') as file:
                        file.write(result)
                    self.statusbar.showMessage(file_path)
                except Exception as e:
                    self.notify("Save Error", f"Error saving file: {str(e)}")

        return callback

    def handleSaveAsResult(self, file_path):
        def callback(result):
            if result:
                try:
                    with open(file_path, 'w') as file:
                        file.write(result)
                    self.file_to_open = file_path
                    self.statusbar.showMessage(file_path)
                except Exception as e:
                    self.notify("Save Error", f"Error saving file: {str(e)}")

        return callback

    def notify(self, message, info):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(info)
        msg.setWindowTitle(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()


if __name__ == "__main__":
    print(f"Debug webengine here: http://127.0.0.1:9222/")
    print("cli python uglyeditor.py --webEngineArgs --remote-debugging-port=9222")
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    qtaceWidget = QtAceWidget()
    qtaceWidget.show()

    sys.exit(app.exec())
