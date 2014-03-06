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

import re
import sys
import os
from PySide import QtGui, QtCore

def nameFilters():
    """
    Returns a list of valid file names for the picker.
    """

    return ['*.bmp', '*.jpg', '*.jpeg', '*.png']

def nameExp():
    """
    Returns a compiled regexp matcher object for bitmap names.
    """

    return re.compile('^.*\.bmp$|^.*\.jpg$|^.*\.jpeg$|^.*\.png$', re.IGNORECASE)

def scaledBitmap(imgPath, size=100):
    """
    Takes a fully qualified image path, returns QImage scaled to size.
    """

    return QtGui.QPixmap(imgPath).scaled(QtCore.QSize(size, size))

class ImagePicker(QtGui.QWidget):
    """
    Widget for picking image files from a directory.
    """

    # Emits the fully qualified path to the picked image
    imagePicked = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(ImagePicker, self).__init__(parent)

        self.listModel = QtGui.QStandardItemModel()

        self.listView = QtGui.QListView()
        self.listView.setUniformItemSizes(True)
        self.listView.setViewMode(QtGui.QListView.ViewMode.IconMode)
        self.listView.setResizeMode(QtGui.QListView.ResizeMode.Adjust)
        self.listView.setModel(self.listModel)
        self.listView.setEditTriggers(
                QtGui.QAbstractItemView.EditTrigger.NoEditTriggers)

        # Transforming slot-signal combo for emitting file names as strings
        self.listView.activated.connect(self.bitmapSelected)

        self.setLayout(QtGui.QHBoxLayout())
        self.layout().addWidget(self.listView)

    @QtCore.Slot(str)
    def setBitmapFolder(self, folder):
        """
        Sets view path to given folder.
        """

        if not os.path.isdir(folder):
            return

        self.rootPath = folder
        self.listModel.clear()
        matchImg = nameExp().match

        for fileName in os.listdir(folder):
            if matchImg(fileName):
                abspath = os.path.join(folder, fileName)
                icon = QtGui.QIcon(scaledBitmap(abspath))
                item = QtGui.QStandardItem(icon, fileName)
                self.listModel.appendRow(item)

    @QtCore.Slot(QtCore.QModelIndex)
    def bitmapSelected(self, modelIndex):
        """
        Intermittently transforms folder name signal emits from
        QFileSystemModel QModelIndex emits to unicode strings emits.

        Returned file name is a fully qualified file name for the platform.
        """

        fullName = os.path.abspath(os.path.join(self.rootPath,
            self.listModel.itemFromIndex(modelIndex).text()))

        # This could be fairly slow
        for f in nameFilters():
            if fullName.lower().endswith(f.lower().strip('*')):
                print('Selected %s' % fullName)
                self.imagePicked.emit(fullName)

    def event(self, ev):
        """
        Catches tooltip type events. Propagates events forward.
        """

        if ev.type() == QtCore.QEvent.ToolTip:
            index = self.listView.indexAt(ev.pos())

            if index.isValid():
                item = self.listModel.itemFromIndex(index)
                path = os.path.join(self.rootPath, item.text())
                text = '%s<br><img width="240" src="%s">' % (path, path)
                QtGui.QToolTip.showText(ev.globalPos(), text)
            else:
                QtGui.QToolTip.hideText()

        return QtGui.QWidget().event(ev)


class FolderPicker(QtGui.QWidget):
    """
    A selector for picking folder to use for images.
    """

    # Emits fully qualified path to the picked folder
    folderPicked = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(FolderPicker, self).__init__(parent)
        self.setLayout(QtGui.QHBoxLayout())

        self.folderPopupButton = QtGui.QPushButton('...')
        self.folderPopupButton.clicked.connect(self.selectFolder)
        self.folderPopupButton.setFixedWidth(50)
        self.layout().addWidget(self.folderPopupButton)

        self.folderSelector = QtGui.QComboBox()
        self.layout().addWidget(self.folderSelector)

    def folders(self):
        """
        Returns the folders that are in the selector.
        """

        return self.folderSelector.items()

    def clearFolders(self):
        """
        Clears folders from the dropdown selector.
        """

        self.folderSelector.clear()

    def addFolder(self, folder):
        """
        Adds a folder to the dropdown selector.
        """

        self.folderSelector.addItem(folder)

    def selectFolder(self):
        """
        Selects a new folder for the picker, emits a folderPicked signal.
        """

        dirName = QtGui.QFileDialog.getExistingDirectory(self,
            self.tr("Choose Directory"),
            os.path.expanduser('~'),
            QtGui.QFileDialog.ShowDirsOnly)

        self.folderPicked.emit(dirName)

class WrapperWidget(QtGui.QMainWindow):
    """
    MainWindow for the Qt application to be executed.
    """

    def __init__(self, parent=None):
        super(WrapperWidget, self).__init__(parent)

        self.setWindowTitle('Imagepicker')

        self.setCentralWidget(QtGui.QWidget(self))
        self.centralWidget().setLayout(QtGui.QVBoxLayout())

        self.createMenus()
        self.createWrappers()

        self.resize(640, 512)
        self.show()

    def createMenus(self):
        """
        Creates file and help menus for the QMainWindow wrapper.
        """

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        helpMenu = menubar.addMenu('&Help')

        openAction = QtGui.QAction('&Open directory', self)
        openAction.setShortcuts(QtGui.QKeySequence.Open)
        openAction.setStatusTip('Open directory for images')

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

    def createWrappers(self):
        """
        Creates layout wrappers for the folder and file pickers.
        """

        self.menu = FolderPicker()
        self.picker = ImagePicker()
        self.menu.folderPicked.connect(self.picker.setBitmapFolder)
        self.menu.folderSelector.activated[str].connect(self.picker.setBitmapFolder)

        menuContainer = QtGui.QHBoxLayout()
        menuContainer.addWidget(self.menu)
        pickerContainer = QtGui.QHBoxLayout()
        pickerContainer.addWidget(self.picker)

        self.centralWidget().layout().addLayout(menuContainer)
        self.centralWidget().layout().addLayout(pickerContainer)

def main(argv=sys.argv):
    """
    Main can be called internally or externally to instantiate
    a widget utility to be shown or attached into existing PySide app.
    """

    _app = QtGui.QApplication(argv)
    _win = WrapperWidget()
    return _app.exec_()

if __name__ == '__main__':
    main()
