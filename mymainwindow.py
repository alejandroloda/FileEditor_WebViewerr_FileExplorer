#  __  __         _     __          __ _             _
# |  \/  |       (_)    \ \        / /(_)           | |
# | \  / |  __ _  _  _ __\ \  /\  / /  _  _ __    __| |  ___ __      __
# | |\/| | / _` || || '_ \\ \/  \/ /  | || '_ \  / _` | / _ \\ \ /\ / /
# | |  | || (_| || || | | |\  /\  /   | || | | || (_| || (_) |\ V  V /
# |_|  |_| \__,_||_||_| |_| \/  \/    |_||_| |_| \__,_| \___/  \_/\_/

import os

from PyQt5.QtWidgets import QMainWindow, QPlainTextEdit, QMessageBox, QDockWidget, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from mytreeview import MyTreeView
from mywebview import MyWebView
from utils import show_pop_up


class MyMainWindow(QMainWindow):
    # Overwritten
    def __init__(self, window_title):
        super().__init__()
        self.setWindowTitle(window_title)
        self.geometry = (300, 300, 1000, 500)
        self.setGeometry(*self.geometry)

        # Editor
        self.editor = QPlainTextEdit()
        self.editor.document().setDefaultFont(QFont("monospace"))
        self.setCentralWidget(self.editor)

        # Selección de ficheros
        # # Crear dock
        self.dockWidget_tree = QDockWidget('Files List', self)
        self.dockWidget_tree.setFloating(False)
        # # Crear tree y asignar
        self.treeView = MyTreeView(self)
        self.dockWidget_tree.setWidget(self.treeView)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget_tree)

        # Web Viewer
        # # Crear dock
        self.dockWidget_web = QDockWidget('Web Viewer', self)
        self.dockWidget_web.setFloating(False)
        # # Crear WebView y asignar
        self.webView = MyWebView(self)
        self.dockWidget_web.setWidget(self.webView)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_web)

        # Doble click en elementos
        self.treeView.doubleClicked.connect(self.double_click_open_if_is_file)

        self.editor.textChanged.connect(self.change_text)

        self.file_path = None

        self.resizeDocks([self.dockWidget_tree, self.dockWidget_web], [250, 400], Qt.Horizontal)

        # Crear Menú
        # self.create_menu()

    def change_text(self):
        """Cuando el texto cambia llama al actualizador del webView"""
        self.webView.update_by_content(self.editor.toPlainText())

    def double_click_open_if_is_file(self, index):
        path = self.treeView.model.filePath(index)
        if os.path.isfile(path):
            self.open_file(path)

    def open_file(self, filename):
        try:
            file_contents = ""
            with open(filename, 'r', encoding="utf8") as f:
                file_contents = f.read()
            self.editor.setPlainText(file_contents)
            self.file_path = filename
        except Exception as e:
            print(e)
            show_pop_up("Error al abrir fichero", str(e))

    #  __  __                  ___
    # |  \/  | ___  _ _  _  _ | __|_  _  _ _   ___
    # | |\/| |/ -_)| ' \| || || _|| || || ' \ (_-<
    # |_|  |_|\___||_||_|\_,_||_|  \_,_||_||_|/__/
    def new_document(self):
        if self.editor.document().isModified():
            answer = self.ask_for_confirmation()
            if answer == QMessageBox.Save:
                if not self.save():
                    return
            elif answer == QMessageBox.Cancel:
                return
        self.editor.clear()
        self.file_path = None

    def show_open_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open...')
        if filename:
            self.open_file(filename)

    def save(self):
        if self.file_path is None:
            return self.show_save_dialog()
        else:
            try:
                with open(self.file_path, 'w') as f:
                    f.write(self.editor.toPlainText())
                self.editor.document().setModified(False)
                return True
            except Exception as e:
                show_pop_up("Error al guardar fichero", str(e))

    def show_save_dialog(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save as...')
            if filename:
                self.file_path = filename
                self.save()
                return True
            return False
        except Exception as e:
            show_pop_up("Error al guardar fichero", str(e))

    def show_about_dialog(self):
        text = """
            <center>
                <h1>PyNotepad</h1><br/>
                <img src=logo.png width=200 height=200>
            </center>
            <p>Version 0.0.1</p>
        """
        QMessageBox.about(self, "About PyNotepad", text)

    def ask_for_confirmation(self):
        return QMessageBox.question(self, "Confirm closing",
                                    "You have unsaved changes. Are you sure you want to exit?",
                                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

    # Overwritten
    def closeEvent(self, e):
        if not self.editor.document().isModified():
            return
        answer = self.ask_for_confirmation()
        if answer == QMessageBox.Save:
            if not self.save():
                e.ignore()
        elif answer == QMessageBox.Cancel:
            e.ignore()
