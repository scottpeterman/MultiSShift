from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys

import sys
import traceback
# Import the SSHLib or replace it with your own terminal backend
class TabTerminal(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab)

    def addBrowserTab(self, url):
        browser = QWebEngineView()
        browser.setUrl(url)
        index = self.addTab(browser, "Browser")
        self.setCurrentIndex(index)

        # Customize Tab with Close Button
        closeButton = QPushButton("X")
        closeButton.clicked.connect(lambda: self.closeTab(index))
        self.tabBar().setTabButton(index, QTabWidget.TabButtonPosition.RightSide, closeButton)

    def closeTab(self, index):
        self.removeTab(index)
