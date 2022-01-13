from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtGui
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic.uiparser import QtWidgets
import numpy as np
import pyzbar.pyzbar as pyzbar
import sqlite3
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import pyqrcode
import os

giris_eposta=""
girislabel=""
sayac=0
girisdogrulama=0
    

class HesapGiris(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("hesapgiris.ui",self)
        if girislabel=="musteri":
            self.label_baslik.setText("Müşteri Giriş Ekranı")
        if girislabel=="firma":
            self.label_baslik.setText("Firma Giriş Ekranı")
        self.pushButton_girisyap.clicked.connect(self.open_giriscesidi)
        self.pushButton_hesapolustur.clicked.connect(self.open_hesapolustur)
        self.pushButton_home.setIcon(QtGui.QIcon('icon\home.png'))
        self.pushButton_return.setIcon(QtGui.QIcon('icon\\return.png'))
        self.pushButton_home.clicked.connect(self.evedon)
        self.pushButton_return.clicked.connect(self.geridon)
    
    def evedon(self):
        self.close()
        self.gecisyap=HesapTuruSecme()
        self.gecisyap.show()
    def geridon(self):
        self.close()
        self.gecisyap=HesapTuruSecme()
        self.gecisyap.show() 
    def open_giriscesidi(self):
            global girisdogrulama
            global giris_eposta
            if girislabel=="musteri":
                eposta=self.lineEdit_eposta.text()
                sifre=self.lineEdit_sifre.text()
                if len(eposta)==0 or len(sifre)==0:
                    QMessageBox.information(self, "Giriş Başarısız ", "Boş Alanları Doldurunuz..")
                else:
                    con=sqlite3.connect("musteriler.db")
                    cursor=con.cursor()
                    cursor.execute("Select eposta,sifre From bilgiler")
                    liste=cursor.fetchall()
                    for i in liste:
                        if (i[0]==eposta and i[1]==sifre):
                            giris_eposta=i[0]
                            girisdogrulama=1
                            QMessageBox.information(self, "Giriş Başarılı ", "Ekrana Yönlendiriliyorsunuz..")
                            self.gecisyap=MusteriEkrani()
                            self.close()
                            self.gecisyap.show()  
                    if girisdogrulama==0:
                        QMessageBox.information(self, "Giriş Başarısız ", "E-posta veya Şifre yanlış..")
                        self.lineEdit_eposta.setText("")
                        self.lineEdit_sifre.setText("")
            if girislabel=="firma":
                eposta=self.lineEdit_eposta.text()
                sifre=self.lineEdit_sifre.text()
                if len(eposta)==0 or len(sifre)==0:
                    QMessageBox.information(self, "Giriş Başarısız ", "Boş Alanları Doldurunuz")
                else:
                    con=sqlite3.connect("firma.db")
                    cursor=con.cursor()
                    cursor.execute("Select firmaEposta,firmaSifre From firma_bilgisi")
                    liste=cursor.fetchall()
                    for i in liste:
                        if (i[0]==eposta and i[1]==sifre):
                            QMessageBox.information(self, "Giriş Başarılı ", "Ekrana Yönlendiriliyorsunuz..")
                            giris_eposta=i[0]
                            girisdogrulama=1
                            self.gecisyap=FirmaEkrani()
                            self.close()
                            self.gecisyap.show()
                    if girisdogrulama==0:
                        QMessageBox.information(self, "Giriş Başarısız ", "E-posta veya Şifre yanlış..")
                        self.lineEdit_eposta.setText("")
                        self.lineEdit_sifre.setText("")
    def open_hesapolustur(self):
        self.gecisyap=KayitHesapTuruSecme()
        self.close()
        self.gecisyap.show()

class HesapTuruSecme(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("hesapturusecme.ui",self)
        self.radioButton_musteri.setChecked(True)
        self.pushButton_hesapturusec.clicked.connect(self.open_hesapgirme)  
        self.pushButton_kayitol.clicked.connect(self.open_kayithesapturusecme)      
    def open_hesapgirme(self):
        global girislabel
        if(self.radioButton_musteri.isChecked()):
            girislabel="musteri"
            self.gecisyap=HesapGiris()
        if(self.radioButton_firma.isChecked()):
            girislabel="firma"
            self.gecisyap=HesapGiris() 
        self.close()  
        self.gecisyap.show()
    def open_kayithesapturusecme(self):
        self.gecisyap=KayitHesapTuruSecme()
        self.close()
        self.gecisyap.show()
        
class KayitFirma(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("kayitfirma.ui",self)
        self.pushButton_firmaKayit.clicked.connect(self.open_girisedon) 
        self.pushButton_home.setIcon(QtGui.QIcon('icon\home.png'))
        self.pushButton_return.setIcon(QtGui.QIcon('icon\\return.png'))
        self.pushButton_home.clicked.connect(self.evedon)
        self.pushButton_return.clicked.connect(self.geridon)
    
    def evedon(self):
        self.close()
        self.gecisyap=HesapTuruSecme()
        self.gecisyap.show()
    def geridon(self):
        self.close()
        self.gecisyap=KayitHesapTuruSecme()
        self.gecisyap.show()  
    def open_girisedon(self):
        firma_adi=self.lineEdit_firmaAdi.text()
        firma_adres=self.lineEdit_adres.text()
        firma_eposta=self.lineEdit_eposta.text()
        firma_sifre=self.lineEdit_sifre.text()
        if len(firma_adi)==0 or len(firma_adres)==0 or len(firma_eposta)==0 or len(firma_sifre)==0:
            QMessageBox.information(self, "Kayıt Başarısız", "Boş Alanları Doldurunuz..")

        else:
            con=sqlite3.connect("firma.db")
            cursor=con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS firma_bilgisi(firmaAd TEXT,firmaAdres TEXT,firmaEposta TEXT,firmaSifre TEXT)")
            cursor.execute("select firmaEposta from firma_bilgisi")
            firmalistesi=cursor.fetchall()
            for bilgiler in firmalistesi:
                if(bilgiler[0]==firma_eposta):
                    QMessageBox.information(self, "Kayıt Başarısız", "Bu E posta sistemimizde zaten mevcut..")
                else:
                    cursor.execute("insert into firma_bilgisi Values(?,?,?,?)",(firma_adi,firma_adres,firma_eposta,firma_sifre))
                    cursor.execute("CREATE TABLE IF NOT EXISTS firma_bakiye(firmaEposta TEXT,firmaBakiye REAL)")
                    cursor.execute("insert into firma_bakiye Values(?,?)",(firma_eposta,0))
                    con.commit()
                    QMessageBox.information(self, "Kayıt Olundu", "Girişe Yönlendiriliyorsunuz..")
                    self.gecisyap=HesapTuruSecme()
                    self.close()
                    self.gecisyap.show()

class KayitMusteri(QMainWindow):
    
    global giris_eposta
    def __init__(self):
        super().__init__()
        loadUi("kayitmusteri.ui",self)
        self.pushButton_musteriKayit.clicked.connect(self.open_girisedon) 
        self.pushButton_home.setIcon(QtGui.QIcon('icon\home.png'))
        self.pushButton_return.setIcon(QtGui.QIcon('icon\\return.png'))
        self.pushButton_home.clicked.connect(self.evedon)
        self.pushButton_return.clicked.connect(self.geridon)
    
    def evedon(self):
        self.close()
        self.gecisyap=HesapTuruSecme()
        self.gecisyap.show()
    def geridon(self):
            self.close()
            self.gecisyap=KayitHesapTuruSecme()
            self.gecisyap.show() 
    def open_girisedon(self):
         kisi_ad=self.lineEdit_ad.text()
         kisi_soyad=self.lineEdit_soyad.text()
         kisi_adres=self.lineEdit_adres.text()
         kisi_eposta=self.lineEdit_eposta.text()
         kisi_sifre=self.lineEdit_sifre.text()
         if len(kisi_ad)==0 or len(kisi_soyad)==0 or len(kisi_adres)==0 or len(kisi_eposta)==0 or len(kisi_sifre)==0:
             QMessageBox.information(self, "Kayıt Başarısız", "Boş Alanları Doldurunuz..")
         else:
            con=sqlite3.connect("musteriler.db")
            cursor=con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS bilgiler(ad TEXT,soyad TEXT,adres TEXT,eposta TEXT,sifre)")
            cursor.execute("select eposta from bilgiler")
            musterilistesi=cursor.fetchall()
            for bilgiler in musterilistesi:
                if(bilgiler[0]==kisi_eposta):
                    QMessageBox.information(self, "Kayıt Başarısız", "Bu E posta sistemimizde zaten mevcut..")
                else:
                    cursor.execute("insert into bilgiler Values(?,?,?,?,?)",(kisi_ad,kisi_soyad,kisi_adres,kisi_eposta,kisi_sifre))
                    con.commit()
                    con.close()
                    data=sqlite3.connect("mustericuzdan.db")
                    a=data.cursor()
                    a.execute("insert into cuzdanbilgisi Values(?,?)",(kisi_eposta,0))
                    data.commit()
                    data.close()
                    QMessageBox.information(self, "Kayıt Olundu", "Girişe Yönlendiriliyorsunuz..")
                    self.gecisyap=HesapTuruSecme()
                    self.close()
                    self.gecisyap.show()
        
class KayitHesapTuruSecme(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("kayithesapturusecme.ui",self)
        self.radioButton_musteri.setChecked(True)
        self.pushButton_hesapturusec.clicked.connect(self.open_kayitekrani)
        self.pushButton_home.setIcon(QtGui.QIcon('icon\home.png'))
        self.pushButton_return.setIcon(QtGui.QIcon('icon\\return.png'))
        self.pushButton_home.clicked.connect(self.evedon)
        self.pushButton_return.clicked.connect(self.geridon)
    
    def evedon(self):
        self.close()
        self.gecisyap=HesapTuruSecme()
        self.gecisyap.show()
    def geridon(self):
            self.close()
            self.gecisyap=HesapTuruSecme()
            self.gecisyap.show()
    def open_kayitekrani(self):
        if(self.radioButton_musteri.isChecked()):
            self.gecisyap=KayitMusteri()
        if(self.radioButton_firma.isChecked()):
            self.gecisyap=KayitFirma() 
        self.close()  
        self.gecisyap.show()

class FirmaEkrani(QMainWindow):
    global giris_eposta
    def __init__(self):
        super().__init__()
        loadUi("firmaekrani.ui",self)
        con=sqlite3.connect("firma.db")
        cursor=con.cursor()
        cursor.execute("Select firmaEposta,firmaBakiye From firma_bakiye")
        liste=cursor.fetchall()
        for i in liste:
           if(i[0]==giris_eposta):
              yenibakiye="Firma Bakiyeniz:"+str(i[1])+" ₺"
              self.label_firmabakiye.setText(yenibakiye)
        con.close()
        self.pushButton_qrolustur.clicked.connect(self.qrolustur)
        self.label_qrcodeshow.setScaledContents(True)
        self.pushButton_cikis.setIcon(QtGui.QIcon('icon\cikis.png'))
        self.pushButton_cikis_2.setIcon(QtGui.QIcon('icon\cikis.png'))
        self.pushButton_cikis.clicked.connect(self.evedon)
        self.pushButton_cikis_2.clicked.connect(self.evedon)
        self.tabWidget.currentChanged.connect(self.bilgiguncelle)
    def evedon(self):
        self.close()
        self.gecisyap=HesapTuruSecme()
        self.gecisyap.show()
    def qrolustur(self):
        if self.lineEdit_tl.text() != '' :
            path = os.getcwd()
            qr = pyqrcode.create(self.lineEdit_tl.text()+","+giris_eposta)
            img = qr.png(path+"\\qrcodlar/"+self.lineEdit_tl.text()+".png", scale = 8)      
            self.label_qrcodeshow.setPixmap(QtGui.QPixmap(path+"\\qrcodlar/"+self.lineEdit_tl.text()+".png"))
            self.label_qrbilgi.setText(self.lineEdit_tl.text()+" ₺")
    def bilgiguncelle(self):
        con=sqlite3.connect("firma.db")
        cursor=con.cursor()
        cursor.execute("Select firmaEposta,firmaBakiye From firma_bakiye")
        liste=cursor.fetchall()
        for i in liste:
           if(i[0]==giris_eposta):
              yenibakiye="Firma Bakiyeniz:"+str(i[1])+" ₺"
              self.label_firmabakiye.setText(yenibakiye)
        connection=sqlite3.connect('firma.db')
        bilgiler=connection.execute("SELECT * FROM firma_satislar where FirmaEposta=?",(giris_eposta,))
        self.tableWidget.setRowCount(1)
        for satir_sayisi,satir_bilgisi in enumerate(bilgiler):
            self.tableWidget.insertRow(satir_sayisi+1)
            for kolon_sayisi,bilgi in enumerate(satir_bilgisi):
                self.tableWidget.setItem(satir_sayisi+1,kolon_sayisi,QTableWidgetItem(str(bilgi)))   
        connection.close()

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
    def run(self):
        global sayac
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        con=sqlite3.connect("musteriler.db")
        cursor=con.cursor()
        cursor.execute("Select * from bilgiler")
        musteriliste=cursor.fetchall()
        for k in musteriliste:
            if(giris_eposta==k[3]):
                ad=k[0]
                soyad=k[1]
                adres=k[2]
                eposta=k[3]
                break
        con.close()
        while self._run_flag:
            ret, cv_img = cap.read()
            decodefObj=pyzbar.decode(cv_img)   
            for obj in decodefObj:
                if sayac==0:
                    tutar=0
                    con=sqlite3.connect("mustericuzdan.db")
                    cursor=con.cursor()
                    cursor.execute("Select eposta,bakiye From cuzdanbilgisi")
                    liste=cursor.fetchall()
                    for i in liste:
                        if(i[0]==giris_eposta):
                            para=obj.data.decode("utf-8").split(",")
                            if(i[1]<np.double(para[0])):
                                font = cv2.FONT_HERSHEY_SIMPLEX
                                cv2.putText(cv_img, 
                                "Yetersiz Bakiye",     
                                (200, 40), 
                                font, 1, 
                                (0, 0, 255), 
                                2, 
                                cv2.LINE_4)
                            else:
                                tutar=i[1]-np.double(para[0])
                                sayac+=1
                                cursor.execute("update cuzdanbilgisi set bakiye=? where eposta=?",(str(tutar),giris_eposta))
                                con.commit()
                                con.close()
                                con=sqlite3.connect("firma.db")
                                cursor=con.cursor()
                                cursor.execute("Select firmaEposta,firmaBakiye From firma_bakiye")
                                liste2=cursor.fetchall()
                                for j in liste2:
                                    if(j[0]==para[1]):
                                        yenibakiye=0
                                        yenibakiye=j[1]+np.double(para[0])
                                        cursor.execute("update firma_bakiye set firmaBakiye=? where firmaEposta=?",(np.double(yenibakiye),str(para[1])))
                                        cursor.execute("insert into firma_satislar Values(?,?,?,?,?,?)",(ad,soyad,adres,eposta,np.double(para[0]),str(para[1])))  
                                        con.commit()
                                        con.close() 
                                                                      
                if sayac>0:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(cv_img, 
                    "Odeme Gerceklesti",     
                    (175, 40), 
                    font, 1, 
                    (0, 0, 255), 
                    2, 
                    cv2.LINE_4)            
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


class MusteriEkrani(QMainWindow):
    global giris_eposta
    
    def __init__(self):
        super().__init__()
        loadUi("musteriekrani.ui",self)
        con=sqlite3.connect("mustericuzdan.db")
        cursor=con.cursor()
        cursor.execute("Select eposta,bakiye From cuzdanbilgisi")
        liste=cursor.fetchall()
        for i in liste:
           if(i[0]==giris_eposta):
              yenibakiye="Güncel Bakiyeniz:"+str(i[1])+" ₺"
              self.label_guncelbakiye.setText(yenibakiye)
        self.pushButton_yukle.clicked.connect(self.open_bakiyeyukle)
        self.pushButton_sifirla.clicked.connect(self.sayacsifirla)
        con.close()
        self.disply_width = 300
        self.display_height = 300
        self.image_label = QLabel(self.tab_3)
        self.image_label.setGeometry(QtCore.QRect(45, 70, 300, 300))
        self.image_label.resize(self.disply_width, self.display_height)
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        self.tabWidget.currentChanged.connect(self.labelguncelle)
        self.pushButton_cikis.setIcon(QtGui.QIcon('icon\cikis.png'))
        self.pushButton_cikis2.setIcon(QtGui.QIcon('icon\cikis.png'))
        self.pushButton_cikis.clicked.connect(self.evedon)
        self.pushButton_cikis2.clicked.connect(self.evedon)
    
    def evedon(self):
        self.close()
        self.gecisyap=HesapTuruSecme()
        self.gecisyap.show()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()
        
    def labelguncelle(self):
        con=sqlite3.connect("mustericuzdan.db")
        cursor=con.cursor()
        cursor.execute("Select eposta,bakiye From cuzdanbilgisi")
        liste=cursor.fetchall()
        for i in liste:
           if(i[0]==giris_eposta):
              yenibakiye="Güncel Bakiyeniz:"+str(i[1])+" ₺"
              self.label_guncelbakiye.setText(yenibakiye)
        con.close()
    
    def sayacsifirla(self):
        global sayac
        sayac=0

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QtGui.QPixmap.fromImage(p) 
    
    def open_bakiyeyukle(self):
        tutar=int(self.lineEdit_yuklenen.text())
        con=sqlite3.connect("mustericuzdan.db")
        cursor=con.cursor()
        cursor.execute("Select eposta,bakiye From cuzdanbilgisi")
        liste=cursor.fetchall()
        for i in liste:
           if(i[0]==giris_eposta):
              tutar+=i[1]
              yenibakiye="Güncel Bakiyeniz:"+str(tutar)+" ₺"
        cursor.execute("update cuzdanbilgisi set bakiye=? where eposta=?",(str(tutar),giris_eposta))
        con.commit()
        self.label_guncelbakiye.setText(str(yenibakiye))
        self.lineEdit_yuklenen.setText("")
        QMessageBox.information(self, "Bakiye Eklendi.",yenibakiye)     
        