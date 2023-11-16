import socket
from multisshift.ui.themes import set_theme_green, set_theme_orange
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal
import sys
import os

import uvicorn
from multisshift.ui.main_window import MainWindow
from multisshift.utils.util import generate_key, create_db, create_sftp_key, create_session_file, create_settings
from .vt import app as fastapi_app

class ServerThread(QThread):
    server_started = pyqtSignal(int)
    server_error = pyqtSignal(str)

    def __init__(self, app, start_port=8002):
        super().__init__()
        self.app = app
        self.port = start_port
        self.server = None

    def find_available_port(self):
        port = self.port
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('127.0.0.1', port))

                    return port  # The port is available
                except OSError as e:
                    if e.errno in (98, 10048):  # Port is in use
                        port += 1  # Try the next port
                    else:
                        raise  # An unexpected error occurred

    def run(self):
        self.port = self.find_available_port()  # Find an available port before starting Uvicorn
        try:
            config = uvicorn.Config(self.app, host="127.0.0.1", port=self.port)
            print(f"Server trying to start on port: {self.port}")
            self.server = uvicorn.Server(config)
            self.server.run()
            # If server.run() returns without exception, the server has started successfully
            print(f"Server started on port: {self.port}")
            self.server_started.emit(self.port)
        except Exception as e:
            print(f"Failed to start server: {e}")
            self.server_error.emit(str(e))
        self.server_started.emit(self.port)


    def stop_server(self):
        if self.server is not None:
            self.server.handle_exit(None, None)

class IntegratedMainWindow(MainWindow):
    def __init__(self, app):
        super().__init__(app)
        self.server_thread = ServerThread(fastapi_app)
        self.server_thread.server_started.connect(self.on_server_started)
        self.server_thread.server_error.connect(self.on_server_error)
        self.server_thread.start()
        self.resize(1000, 600)

    def on_server_started(self, port):
        # You can update the GUI or status bar with the port number if necessary
        print(f"Server started on port {port}")

    def on_server_error(self, message):
        # You can update the GUI or status bar with the error message if necessary
        print(message)

    def closeEvent(self, event):
        self.server_thread.stop_server()
        self.server_thread.wait()
        super().closeEvent(event)


def load_stylesheet(file_path):
    with open(file_path, "r") as file:
        return file.read()

def main():
    if not os.path.isfile('crypto.key'):
        generate_key()

    if not os.path.isfile('settings.sqlite'):
        create_db()

    if not os.path.exists("./sessions/sessions.yaml"):
        create_session_file()

    if not os.path.exists("./settings.yaml"):
        create_settings()

    app = QApplication(sys.argv)

    app.setStyle("fusion")
    window = IntegratedMainWindow(app)
    window.show()
    result = app.exec()

    # Ensure the server is stopped when the application closes
    window.server_thread.stop_server()
    window.server_thread.wait()

    sys.exit(result)


if __name__ == "__main__":
    main()
