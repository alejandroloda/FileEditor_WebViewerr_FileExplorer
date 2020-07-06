#  _    _  _    _  _
# | |  | || |  (_)| |
# | |  | || |_  _ | | ___
# | |  | || __|| || |/ __|
# | |__| || |_ | || |\__ \
#  \____/  \__||_||_||___/

from PyQt5.QtWidgets import QMessageBox


def show_pop_up(title, text, icon="critical"):
    """Muestra un popup con un titulo y texto dado, además agrega un icono al mismo"""
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)

    icon_options = {
        'critical': QMessageBox.Critical,
        'c': QMessageBox.Critical,
        'warning': QMessageBox.Warning,
        'w': QMessageBox.Warning,
        'information': QMessageBox.Information,
        'i': QMessageBox.Information,
        'question': QMessageBox.Question,
        'q': QMessageBox.Question,
    }
    icon = icon_options[icon.lower()]
    msg.setIcon(icon)
    x = msg.exec_()
