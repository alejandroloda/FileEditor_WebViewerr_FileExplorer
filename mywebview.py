# __          __  _ __      ___
# \ \        / / | |\ \    / (_)
#  \ \  /\  / /__| |_\ \  / / _  _____      __
#   \ \/  \/ / _ \ '_ \ \/ / | |/ _ \ \ /\ / /
#    \  /\  /  __/ |_) \  /  | |  __/\ V  V /
#     \/  \/ \___|_.__/ \/   |_|\___| \_/\_/

import os

from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

from markdown2 import Markdown
from utils import show_pop_up


class MyWebView(QWebEngineView):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.auto_update = True
        self.mark2html("# Ready for you!")
        self.checkBox_update = QCheckBox("Update", self)
        self.checkBox_update.move(5, 5)
        self.checkBox_update.toggle()
        self.checkBox_update.stateChanged.connect(self.change_auto_update)

    def url(self, url):
        """Carga un archivo, algunos tipos de archivo no es posible cargarlos"""
        self.setUrl(QUrl(url))

    def html(self, content):
        """Carga un texto como si fuera html"""
        self.setHtml(content)

    def mark2html(self, text):
        """Transforma un texto, presumiblemete markdown, a html y lo carga"""
        markdowner = Markdown()
        html = markdowner.convert(text)
        self.html("\n.\n" + html)

    def change_auto_update(self, checked):
        """Actualiza la booleana que permite que el texto escrito se actualize a html con cada nuevo caracter"""
        self.auto_update = True if checked else False

    def reverse_check(self):
        self.off_on_auto_update()

    def off_on_auto_update(self, boo=None):
        """Da el valor a la booleana y actualiza el check con el valor propio"""
        if boo is None:
            boo = not self.auto_update
        if boo != self.auto_update:
            self.auto_update = boo
            self.checkBox_update.toggle()

    def update_by_content(self, content):
        """Se llama periódicamente si se cambia el archivo"""
        if self.auto_update:
            self.mark2html(content)

    def update_by_file(self, filename):
        """Si se hace hace click en el archivo lo carga y desactiva el auto update
            Permite imágenes, archivos de texto, markdown y html
        """
        try:
            _, file_extension = os.path.splitext(filename)
            if file_extension not in ['.exe', '.bat', '.lkn']:
                if file_extension in ['.md', '.mkd']:
                    with open(filename, 'r', encoding="utf8") as f:
                        file_contents = f.read()
                    self.mark2html(file_contents)
                else:
                    self.url(filename)
                # self.off_on_auto_update(False)

        except Exception as e:
            print(e)
            show_pop_up("Error al abrir fichero", str(e))
