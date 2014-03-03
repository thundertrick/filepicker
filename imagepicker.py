#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013-2014, Aleksi Häkli <aleksi.hakli@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 2.1
# as published by the Free Software Foundation

"""
Imagepicker widget utility written with Python 2 and PySide Qt4 bindings.

The purpose of this utility is to offer an easy-to-use widget component
to use with programs to select images in Pythonic GUI context.

Utility is also runnable as standalone for testing and demonstration purposes:

    $ python imagepicker.py
"""

# pylint: disable=C0103,R0904,W0102

import sys
from PySide import QtGui


class ImagepickerSelector(QtGui.QWidget):
    """
    Imagepicker widget for picking image objects.
    """

    def __init__(self, parent=None):
        super(ImagepickerSelector, self).__init__(parent)
        self.addBitmaps(None)

    def setBitmaps(self, bitmaps=[]):
        pass

    def addBitmaps(self, bitmaps):
        for i in range(0, 5):
            label = QtGui.QLabel()
            path = '/home/aleksi/downloads/images.jpg'
            label.setPixmap(QtGui.QPixmap(path))

            self.setLayout(QtGui.QHBoxLayout())
            self.layout().addWidget(label)

class ImagepickerFolderMenu(QtGui.QWidget):
    """
    A selector for picking folder to use for images.
    """

    def __init__(self, parent=None):
        super(ImagepickerFolderMenu, self).__init__(parent)
        self.setLayout(QtGui.QHBoxLayout())

        self.folderPopupButton = QtGui.QPushButton('...')
        self.folderPopupButton.setFixedWidth(50)
        self.layout().addWidget(self.folderPopupButton)

        self.folderSelector = QtGui.QComboBox()
        self.layout().addWidget(self.folderSelector)

        self.setFolders(['foo', 'bar', 'biz'])

    def setFolders(self, folders=[]):
        for folder in folders:
            print('Adding folder %s to selector' % folder)
            self.folderSelector.addItem(folder)

        if not folders:
            print('Clearing folders from selector')
            self.folderSelector.clear()

    def addFolders(self, folders):
        pass

class Imagepicker(QtGui.QMainWindow):
    """
    MainWindow for the Qt application to be executed.
    """

    def __init__(self, parent=None):
        super(Imagepicker, self).__init__(parent)

        self.setWindowTitle('Imagepicker')

        self.setCentralWidget(QtGui.QWidget(self))
        self.centralWidget().setLayout(QtGui.QVBoxLayout())

        self.attachMenu()
        self.attachPicker()

        self.resize(640, 512)
        self.show()

    def attachMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        helpMenu = menubar.addMenu('&Help')

        openAction = QtGui.QAction('&Open directory', self)
        openAction.setShortcuts(QtGui.QKeySequence.Open)
        openAction.setStatusTip('Exit application')

        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcuts(QtGui.QKeySequence.Close)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        helpAction = QtGui.QAction('&Help for Imagepicker', self)
        helpAction.setShortcut(QtGui.QKeySequence.HelpContents)
        helpAction.setStatusTip('Help and documentation')

        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        helpMenu.addAction(helpAction)

    def attachPicker(self):
        menu = ImagepickerFolderMenu()
        menuContainer = QtGui.QHBoxLayout()
        menuContainer.addWidget(menu)

        picker = ImagepickerSelector()
        pickerContainer = QtGui.QHBoxLayout()
        pickerContainer.addWidget(picker)

        self.centralWidget().layout().addLayout(menuContainer)
        self.centralWidget().layout().addLayout(pickerContainer)

def main(argv=sys.argv):
    """
    Main can be called internally or externally to instantiate
    a widget utility to be shown or attached into existing PySide app.
    """

    _app = QtGui.QApplication(argv)
    _win = Imagepicker()
    sys.exit(_app.exec_())


if __name__ == '__main__':
    main()
