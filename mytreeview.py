#  _______             __      __ _
# |__   __|            \ \    / /(_)
#    | | _ __  ___   ___\ \  / /  _   ___ __      __
#    | || '__|/ _ \ / _ \\ \/ /  | | / _ \\ \ /\ / /
#    | || |  |  __/|  __/ \  /   | ||  __/ \ V  V /
#    |_||_|   \___| \___|  \/    |_| \___|  \_/\_/

import os

from PyQt5.QtWidgets import QMessageBox, QTreeView, QFileSystemModel, QMenu
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

import pyperclip
from shutil import copyfile, copytree
from send2trash import send2trash

from utils import show_pop_up


class MyTreeView(QTreeView):
    # Overwritten
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.model = QFileSystemModel()
        current_path = os.path.abspath(os.getcwd())
        self.model.setRootPath(current_path)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(current_path))
        self.setColumnWidth(0, 250)
        self.setSortingEnabled(True)
        self.sortByColumn(0, 0)

        self.setEditTriggers(QTreeView.NoEditTriggers)
        self.model.setReadOnly(False)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

    #   ___         _           _   __  __
    #  / __|___ _ _| |_ _____ _| |_|  \/  |___ _ _ _  _
    # | (__/ _ \ ' \  _/ -_) \ /  _| |\/| / -_) ' \ || |
    #  \___\___/_||_\__\___/_\_\\__|_|  |_\___|_||_\_,_|
    def context_menu(self):
        menu = QMenu()

        open_ = menu.addAction("Open / Display")
        open_.triggered.connect(self.c_m_open)

        web = menu.addAction("Load webView file")
        web.triggered.connect(self.c_m_web_load)

        menu.addSeparator()

        rename = menu.addAction("Rename")
        rename.triggered.connect(self.c_m_rename)

        copy_path = menu.addAction("Copy path")
        copy_path.triggered.connect(self.c_m_copy_path)

        duplicate = menu.addAction("Duplicate")
        duplicate.triggered.connect(self.c_m_duplicate)

        show_in_explorer = menu.addAction("Show in explorer")
        show_in_explorer.triggered.connect(self.c_m_explorer)

        menu.addSeparator()

        delete = menu.addAction("Delete")
        delete.triggered.connect(self.c_m_delete)

        cursor = QCursor()
        menu.exec_(cursor.pos())

    def c_m_open(self):
        """"Abre un archivo o despliega un fichero"""
        index = self.currentIndex()
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.main.open_file(path)
        else:
            self.setExpanded(index, True)

    def c_m_web_load(self):
        """Abre en el webViewer el fichero"""
        index = self.currentIndex()
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.main.webView.update_by_file(path)
        else:
            pass

    def c_m_rename(self):
        """"Renombrar archivo o directorio desde el TreeView"""
        index = self.currentIndex()
        self.edit(index)

    def c_m_copy_path(self):
        """"Copia la ruta de un archivo o directorio"""
        index = self.currentIndex()
        path = self.model.filePath(index)
        pyperclip.copy(path)

    def c_m_duplicate(self):
        """"Duplica un archivo o directorio"""
        index = self.currentIndex()
        path = self.model.filePath(index)
        if os.path.isfile(path):
            filename, file_extension = os.path.splitext(path)
            copyfile(path, f"{filename}(copy){file_extension}")
        else:
            copytree(path, path + "(copy)")

    def c_m_explorer(self):
        """"Abre el explorador en el path padre de un archivo o directorio"""
        index = self.currentIndex()
        path = self.model.filePath(index)
        path = os.path.realpath(path)
        path = os.path.dirname(path)
        os.startfile(path)

    def c_m_delete(self):
        """"Borra un archivo o directorio (lo manda a la papelera de reciclaje)"""
        index = self.currentIndex()
        path = self.model.filePath(index)
        path = os.path.realpath(path)
        # if os.path.isfile(path):
        #     os.remove(path)
        # else:
        #     rmtree(path)
        qm = QMessageBox
        ret = qm.question(self, '', f"Are you sure to delete '{os.path.basename(path)}' ?", qm.Yes | qm.No,
                          defaultButton=qm.No)
        if ret == qm.Yes:
            send2trash(path)
