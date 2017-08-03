#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui, QtSql
from datetime import datetime, date, timedelta
import application_rc
import sql
from functools import total_ordering
from shutil import copyfile
import os
import trim
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self, None)
        self.setStyleSheet('font-size: 10pt;')
        self.setWindowTitle(u'고객정보변환')

    def closeEvent(self, event):
        event.accept()

    def deFormatContact(self, contact):
        return ''.join(ele for ele in contact if ele.isdigit())

    def formatContact(self, contact):
        digitString = ''.join(ele for ele in contact if ele.isdigit())
        if len(digitString) == 11:
            return digitString[:3] + '-' + digitString[3:7] + '-' + digitString[7:]
        elif len(digitString) == 10:
            return digitString[:3] + '-' + digitString[3:6] + '-' + digitString[6:]
        elif len(digitString) == 9:
            return digitString[:2] + '-' + digitString[2:5] + '-' + digitString[5:]
        else:
            return digitString


    def save(self):
        time = datetime.now()
        filename = QtGui.QFileDialog.getSaveFileName(caption = u'백업 파일 저장하기',dir = u'마실백업-{}년-{}월-{}일-{}시-{}분'.format(time.year, time.month, time.day, time.hour, time.minute)
            , filter = '.enc')[0]

        if filename != '':
            backup.encrypt_file(backup.key,'masil.db')
            fromfile = QtCore.QFile('masil.db.enc')
            tofile = QtCore.QFile(filename)
            success = fromfile.copy(filename)
            if success:
                self.displaySimpleMessageBox(u'성공적으로 백업했습니다.')
            else:
                self.displaySimpleMessageBox(u'백업하는 데 실패했습니다.')

    def load(self):
        filename = QtGui.QFileDialog.getOpenFileName(caption = u'백업 파일 불러오기')[0]
        time = datetime.now()
        if len(filename) == 0:
            self.displaySimpleMessageBox(u'불러오기를 취소합니다.')
            return
        #nameAndExtension = filename.split('.')
        #if filename.split('.')[-1] != 'db':
            #self.displaySimpleMessageBox(u'db 확장자인 파일을 선택하여 주십시오.')
            #return
        try:
            if filename.split('.')[-1] == 'db':
                copyfile(os.path.abspath('masil.db'), os.path.abspath('masil.db')[:-8]+'db_before_load_{}_{}_{}_{}_{}_{}.db'.format(time.year, time.month, time.day, time.hour, time.minute, time.second))
                copyfile(filename, os.path.abspath('masil.db'))
            elif filename.split('.')[-1] == 'enc':
                copyfile(os.path.abspath('masil.db'), os.path.abspath('masil.db')[:-8]+'db_before_load_{}_{}_{}_{}_{}_{}.db'.format(time.year, time.month, time.day, time.hour, time.minute, time.second))
                backup.decrypt_file(backup.key,filename,out_filename='masil.db')
            else:
                self.displaySimpleMessageBox(u'db 또는 enc 확장자인 파일을 선택하여 주십시오.')
                return
        except:
            #raise
            self.displaySimpleMessageBox(u'파일을 불러오는 데 실패했습니다.')
        else:
            self.displaySimpleMessageBox(u'성공적으로 불러왔습니다. 프로그램을 다시 실행하여 주십시오.')
            sys.exit()

    def displaySimpleMessageBox(self,text):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(text)
        msgBox.addButton(u'확인', QtGui.QMessageBox.AcceptRole)
        msgBox.exec_()

    def formattedExportedContact(self, contact):
        '''assuming contact is correct and starts with 0, which will be right in this case'''
        return '82'+contact[1:]

    def extractGivenContactIfCellNumber(self, file, contact):
        if len(contact) == 11 and contact.startswith('010'):
            file.write(self.formattedExportedContact(contact)+'\n')

    def extractContact(self):
        time = datetime.now()
        filename = QtGui.QFileDialog.getSaveFileName(caption = u'연락처 저장하기',dir = u'마실연락처-{}년-{}월-{}일-{}시-{}분'.format(time.year, time.month, time.day, time.hour, time.minute)
            , filter = '.txt')[0]

        if filename != '':
            query = QtSql.QSqlQuery("SELECT contact FROM customer")
            with open(filename,'w') as f:
                while query.next():
                    self.extractGivenContactIfCellNumber(f, query.value(0))
            self.displaySimpleMessageBox(u'저장을 완료했습니다.')


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load("qt_ko"):
        app.installTranslator(qtTranslator)
    mainWindow = MainWindow()
    app.exec_()
    sys.exit()