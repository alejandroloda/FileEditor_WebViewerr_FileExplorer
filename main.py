#  __  __         _         _____
# |  \/  |       (_)       |  __ \
# | \  / |  __ _  _  _ __  | |__) |_ __  ___    __ _  _ __  __ _  _ __ ___
# | |\/| | / _` || || '_ \ |  ___/| '__|/ _ \  / _` || '__|/ _` || '_ ` _ \
# | |  | || (_| || || | | || |    | |  | (_) || (_| || |  | (_| || | | | | |
# |_|  |_| \__,_||_||_| |_||_|    |_|   \___/  \__, ||_|   \__,_||_| |_| |_|
#                                               __/ |
#                                              |___/
import sys

from PyQt5.QtWidgets import QApplication, QAction
from PyQt5.QtGui import QKeySequence

from mymainwindow import MyMainWindow

if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow("PyNotepad")
    window.show()

    #  __  __
    # |  \/  | ___  _ _  _  _
    # | |\/| |/ -_)| ' \| || |
    # |_|  |_|\___||_||_|\_,_|
    menu_bar = window.menuBar()
    file_menu = menu_bar.addMenu("&File")

    new_action = QAction("&New document")
    new_action.triggered.connect(window.new_document)
    new_action.setShortcut(QKeySequence.New)
    file_menu.addAction(new_action)

    open_action = QAction("&Open file...")
    open_action.triggered.connect(window.show_open_dialog)
    open_action.setShortcut(QKeySequence.Open)
    file_menu.addAction(open_action)

    save_action = QAction("&Save")
    save_action.triggered.connect(window.save)
    save_action.setShortcut(QKeySequence.Save)
    file_menu.addAction(save_action)

    close_action = QAction("&Close")
    close_action.triggered.connect(window.close)
    close_action.setShortcut(QKeySequence.Quit)
    file_menu.addAction(close_action)

    help_menu = menu_bar.addMenu("&Help")

    about_action = QAction("&About")
    about_action.triggered.connect(window.show_about_dialog)
    help_menu.addAction(about_action)

    update_menu = menu_bar.addMenu("&Update")

    update_action = QAction("&Update On/Off")
    update_action.triggered.connect(window.webView.reverse_check)
    update_menu.addAction(update_action)

    #  __  __                  ___  _
    # |  \/  | ___  _ _  _  _ | __|(_) _ _
    # | |\/| |/ -_)| ' \| || || _| | || ' \
    # |_|  |_|\___||_||_|\_,_||_|  |_||_||_|

    sys.exit(app.exec_())

# TODO:
# - Mover archivos entre directorios
# ? Tamaño por defecto de los dock
# - Recargar el checkbox si se abre una imagen
# - Mejorar el update
