import os
import sys
from urllib.parse import quote

import yaml
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QMenu, QSplitter, QStackedWidget, QTextBrowser, QWidget, QVBoxLayout, \
    QLabel, QTabWidget, QFileDialog, QDialog, QMessageBox, QApplication, QToolBar
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QAction, QIcon, QPalette
from multisshift.session_manager.session_manager import SessionManager
from multisshift.dialogs.adhoc import AdhocConnectionDialog
from multisshift.ui.creds_widget import CredentialsManagerWidget as Ui_Creds
from multisshift.ui.themes import *
from multisshift.ui.log_viewer2 import FileViewer
from multisshift.ui.serialui import Ui_SerialWidget
from multisshift.ui.ace_widget import QtAceWidget
class MainWindow(QMainWindow):

    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.settings = None
        self.isClosing = False
        self.app = app
        self.setWindowTitle("MultiSSHift Terminal")
        self.setGeometry(200, 200, 800, 600)
        self.center_on_screen()
        # Menubar setup
        menubar = QMenuBar()
        file_menu = QMenu("File", self)
        self.options_menu = QMenu("Options", self)
        self.tools_menu = QMenu("Tools", self)
        help_menu = QMenu("Help", self)
        self.isCLosing = False

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(sys.exit)
        settings_action = QAction("Credentials", self)
        settings_action.triggered.connect(self.showSettings)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        load_sessions_action = QAction("Load Sessions", self)
        file_menu.addAction(load_sessions_action)
        load_sessions_action.triggered.connect(self.load_sessions_dialog)

        log_viewer_action = QAction("Log Viewer", self)
        self.tools_menu.addAction(log_viewer_action)
        log_viewer_action.triggered.connect(self.open_log_viewer)

        editor_action = QAction("Editor", self)
        self.tools_menu.addAction(editor_action)
        editor_action.triggered.connect(self.open_editor)

        # file_menu.addAction(open_action)
        file_menu.addAction(exit_action)
        self.options_menu.addAction(settings_action)
        help_menu.addAction(about_action)

        menubar.addMenu(file_menu)
        menubar.addMenu(self.options_menu)
        menubar.addMenu(self.tools_menu)
        menubar.addMenu(help_menu)
        self.setMenuBar(menubar)

        # Vertical Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        palette = splitter.palette()
        palette.setColor(QPalette.ColorRole.Window, QtGui.QColor(53, 53, 53))  # Set your desired color
        splitter.setPalette(palette)
        # Second number corresponds to the size of self.stack_widget

        # TreeWidget for session management
        self.tree_widget = SessionManager(self)
        self.tree_widget.setHeaderLabel("Sessions")
        self.tree_widget.sessionSelected.connect(self.initialize_session)

        # StackWidget
        self.stack_widget = QStackedWidget()
        palette = self.stack_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QtGui.QColor(53, 53, 53))  # Set your desired color
        self.stack_widget.setPalette(palette)

        web_view = QWebEngineView()
        web_view.setHidden(True)
        # Set the URL to the web view
        web_view.load(QUrl("http://localhost:8002/splash"))
        web_view.loadFinished.connect(lambda _: web_view.show())
        # Add the web view to the stack widget
        self.stack_widget.addWidget(web_view)

        # If you want to display the web view by default
        self.stack_widget.setCurrentWidget(web_view)
        tab_area = QWidget()
        tab_layout = QVBoxLayout()

        self.message_label = QLabel("")
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        tab_layout.addWidget(self.tabs)
        tab_layout.addWidget(self.message_label)
        tab_area.setLayout(tab_layout)

        # self.stack_widget.addWidget(text_browser)
        self.stack_widget.addWidget(tab_area)

        splitter.addWidget(self.tree_widget)
        splitter.addWidget(self.stack_widget)

        self.setCentralWidget(splitter)
        try:
            self.tree_widget.load_sessions_from_yaml("./sessions/sessions.yaml")
        except:
            pass
        splitter.setSizes([200, 600])
        self.init_toolbar()
        self.init_theme_menu()
        self.load_settings()
        if self.settings is not None:
            if self.settings['defaults']['theme'] == 'dark':
                set_theme_green(self.app)
            else:
                self.set_default_theme()

    def load_settings(self):
        with open('settings.yaml', 'r') as file:
            try:
                self.settings = yaml.safe_load(file)
            except:
                print("unable to load settings file")


    def open_log_viewer(self):
        self.logviewer = FileViewer()
        self.logviewer.show()

    def closeApp(self):
        self.isClosing = True
        self.close()

    def serial_action_triggered(self):
        self.serial_ui = Ui_SerialWidget()

        self.serial_ui.show()

    def adhoc_action_triggered(self):
        dialog = AdhocConnectionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            connection_details = dialog.get_connection_details()
            # Ensure that 'auth' key is present in the dictionary
            auth = connection_details.get('auth', '')
            self.add_new_ssh_tab(
                {'display_name': dialog.host_edit.text(), 'host': dialog.host_edit.text(),
                 "port": dialog.port_edit.text()},
                dialog.username_edit.text(),
                connection_details['auth_type'],
                auth
            )

    def add_new_ssh_tab(self, refBinding, username, auth_type, auth):
        self.stack_widget.setCurrentIndex(1)
        host = str(refBinding.get("host")).strip()
        port = refBinding.get("port")
        display_name = refBinding.get("display_name")

        # Create a new QWebEngineView as the terminal
        ssh_terminal_view = QWebEngineView()

        # Adjust the JavaScript for form submission based on auth_type
        js_populate_and_submit_form = f"""
            document.getElementById('auth_type').value = '{auth_type}';
            document.getElementById('auth').value = '{auth}';
            document.forms[0].submit();
        """

        def on_load_finished(ok):
            if ok:  # Check if the page loaded successfully
                ssh_terminal_view.page().runJavaScript(js_populate_and_submit_form)

        ssh_terminal_view.loadFinished.connect(on_load_finished)

        # Encode the auth (password or key file path) for URL
        encoded_auth = quote(auth)

        # Construct the URL to load in the QWebEngineView
        terminal_url = f"http://localhost:{self.server_thread.port}/?host={host}&port={port}&username={username}&auth_type={auth_type}&auth={encoded_auth}"

        # Load the URL into the QWebEngineView
        ssh_terminal_view.load(QUrl(terminal_url))

        # Add the new tab with the QWebEngineView and set the display name
        tab_index = self.tabs.addTab(ssh_terminal_view, display_name)
        self.tabs.setCurrentIndex(tab_index)

    def cleanup(self, tab_to_remove):
        # tab_to_remove.backend.shutdown()  # Close the SSH session and stop its thread
        # Perform any other cleanup activities here
        pass

    def load_sessions_dialog(self):
        # options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Sessions File", "", "YAML Files (*.yaml);;All Files (*)",)
        if filePath:
            try:
                self.tree_widget.load_sessions_from_yaml(filePath)
            except yaml.YAMLError as e:
                # Handle YAML parsing errors
                self.notify("YAML Error", f"YAML parsing error: {filePath}")
                return None  # or some other failure indicator

            except Exception as e:
                self.notify(f"Load Error", f"Unable to load session yaml file: {e}")

    def notify(self, message, info):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(info)
        msg.setWindowTitle(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
    def showSettings(self):
        credsapp = Ui_Creds()
        credsapp.show()

    def show_disconnect_confirm(self,tab_to_remove):
        msg = QMessageBox(text=f"Session to {tab_to_remove.host} is active, disconnect?", parent=self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok |
                               QMessageBox.StandardButton.Cancel)
        msg.setInformativeText("Disconnect?")
        return msg.exec()

    def close_tab(self, index):
        tab_to_remove = self.tabs.widget(index)  # Get the QWidget from the tab to be closed

        # Check if the session is active, you can implement is_session_active() based on your needs
        if self.is_session_active(tab_to_remove):
            try:

                reply = self.show_disconnect_confirm(tab_to_remove)
                if reply == QMessageBox.StandardButton.Ok:
                    print("closing tab...")
                    if self.isClosing:
                        return True
                    else:
                        self.cleanup(tab_to_remove)
                        self.tabs.removeTab(index)
                else:
                    return False
            except Exception as e:
                print(e)
        # Call your existing cleanup method to properly close the SSH session and perform other teardown activities
        self.cleanup(tab_to_remove)
        self.tabs.removeTab(index)

    def is_session_active(self, tab):
        # Implement your logic to check if the SSH session in the tab is active.
        # For example, you might check whether the SSH channel is open.
        try:
            return not tab.backend.channel.closed
        except:
            return False


    def init_toolbar(self):
        # Create a toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)


        #adhoc connection
        current_dir = os.path.dirname(__file__)

        icon_path = os.path.join(current_dir, 'images', 'terminal.svg')
        print(f"loading... {icon_path}")
        adhoc_icon = QIcon(icon_path)
        adhoc_action = QAction(adhoc_icon, "Connect", self)
        adhoc_action.triggered.connect(self.adhoc_action_triggered)  # Connect to a method
        toolbar.addAction(adhoc_action)

        icon_path = os.path.join(current_dir, 'images', 'bolt.svg')
        print(f"loading... {icon_path}")
        serial_icon = QIcon(icon_path)
        serial_action = QAction(serial_icon, "Serial", self)
        serial_action.triggered.connect(self.serial_action_triggered)  # Connect to a method
        toolbar.addAction(serial_action)


    def init_theme_menu(self):
        # Create a Theme submenu under the Options menu
        theme_menu = QMenu("Theme", self)
        self.options_menu.addMenu(theme_menu)

        # Create actions for the theme submenu
        default_action = QAction("Light", self)
        # fusion_action = QAction("Dark", self)
        green_action = QAction("Dark", self)
        # orange_action = QAction("Orange", self)

        # Add actions to the theme submenu
        theme_menu.addAction(default_action)
        # theme_menu.addAction(fusion_action)
        theme_menu.addAction(green_action)
        # theme_menu.addAction(orange_action)

        # Connect actions to methods
        default_action.triggered.connect(self.set_default_theme)
        # fusion_action.triggered.connect(self.set_fusion_theme)
        green_action.triggered.connect(lambda: set_theme_green(self.app))
        # orange_action.triggered.connect(lambda: set_theme_orange(self.app))

    def set_default_theme(self):
        style = QtWidgets.QStyleFactory.create('Windows')
        palette = QtGui.QPalette(style.standardPalette())
        self.app.setPalette(palette)

    def set_fusion_theme(self):
        fusion = QtWidgets.QStyleFactory.create('Fusion')
        palette = QtGui.QPalette(fusion.standardPalette())
        self.app.setPalette(palette)

    def center_on_screen(self):
        screen = self.screen()  # get the screen where this widget is displayed
        screen_geometry = screen.geometry()  # get the screen geometry
        center_point = screen_geometry.center()  # find its center point

        frame_geometry = self.frameGeometry()  # get the frame geometry of the main window
        frame_geometry.moveCenter(
            center_point)  # set the center point of frame_geometry to the center point of the screen

        self.move(frame_geometry.topLeft())

    def initialize_session(self, session_data):
        pass

    def closeEvent(self, event):
        active_tabs = self.tabs.count()

        if active_tabs > 0:
            reply = QMessageBox.question(self, 'Confirm Exit',
                                         "There are active sessions. Do you want to close all sessions and exit?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                for index in reversed(range(active_tabs)):  # Loop over a range of tab indices
                    self.close_tab(index)
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def open_editor(self):
        print("opening ace editor")
        editor = QtAceWidget()
        editor.show()
    def show_about_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About")

        layout = QVBoxLayout(dialog)

        text_browser = QtWidgets.QTextBrowser(dialog)
        text_browser.setOpenExternalLinks(True)
        text_browser.setHtml(
            "<p><b>Version:</b> 0.1.0</p>"
            "<p><b>Author:</b> Scott Peterman</p>"
            "<p><b>Github Repo:</b> <a href='https://github.com/scottpeterman/MultiSShift'>MultiSShift</a></p>"
            "<p><b>PyPI:</b> <a href='https://pypi.org/project/multisshift/'>Pip Install</a></p>"
        )

        layout.addWidget(text_browser)

        dialog.setLayout(layout)
        dialog.exec()