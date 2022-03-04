import time
import asyncio
import pandas as pd
import requests
from PyQt5 import QtCore, QtGui, QtWidgets

regioni=[]
filename=""
search=""
excluded_words=[]
limit=0
limit_per_page=10000
reasonable_min_price=0
reasonable_max_price=0
contain_check=False
limit_check=False
reasonable_price_check=False


def generateCSV(self,regioni,filename,search,excluded_words,limit,limit_per_page,reasonable_min_price,reasonable_max_price,contain_check,limit_check,reasonable_price_check):
    url = "https://www.subito.it/hades/v1/search/items"
    res = []
    sum=0
    j=0
    all_data=[]
    total=0
    for regione in regioni:
        querystring = {"q":str(search),"r":str(regione),"t":"s","qso":"false","shp":"false","":"","sort":"datedesc","lim":str(limit_per_page),"start":'0'}
        payload = ""
        headers = {
            "cookie": "",
            "sec-ch-ua": "^\^"
        }
        r = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        data = r.json()
        total=total+len(data["ads"])
        all_data.append(data)
    for data in all_data:
        regione_text=data['filters']['r']
        for annuncio in data['ads']:
            obj = ["","","","-100",""]
            flag=False
            #PARAMETRI: titolo dell'annuncio, verifica che non contenga parole escluse e contenga ricerca
            subject=annuncio['subject']
            for excl_word in excluded_words:
                if subject.find(excl_word) != -1:
                    flag=True
            if contain_check:
                flag_contain=True
                for piece in search.split():
                    if subject.find(piece) != -1:
                        flag_contain=False
                if flag_contain:
                    flag=True
            if flag:
                continue
            obj[0]=subject
            #PARAMETRI: regione
            obj[1]=regione_text
            #PARAMETRI: data pubblicazione annuncio
            obj[2]=annuncio['dates']['display']
            #PARAMETRI: prezzo, controllo che rispetti il range di ragionevolezza
            for feature in annuncio['features']:
                if feature['uri'] == "/price":
                    prezzo=str(feature['values'][0]['key'])
                    if(int(prezzo)<reasonable_min_price or int(prezzo)>reasonable_max_price) and reasonable_price_check:
                        flag=True
                    else:
                        obj[3]=prezzo
                        sum=sum+int(prezzo)
            #PARAMETRI: URL
            obj[4]=annuncio['urls']['default']

            #controlli finali
            if flag or int(obj[3])<0:
                continue
            if len(res)>=limit and limit_check:
                break;
            res.append(obj)
            self.progressBar.setValue(int(round(j*100/total,0)))
            j=j+1
    avg = sum/len(res)
    df= pd.DataFrame(res, columns = ['Titolo','Regione','Data Pubblicazione','Prezzo', 'URL'])
    try:
        df.to_csv(filename+'.csv', index=False, sep=';')
        print(filename+".csv salvato nella directory corrente")
    except:
        print("il file è aperto, impossibile modificarlo")


def generatePreview(self,regioni,search,excluded_words,limit,limit_per_page,reasonable_min_price,reasonable_max_price,contain_check,limit_check,reasonable_price_check):
    url = "https://www.subito.it/hades/v1/search/items"
    res = []
    sum=0
    j=0
    all_data=[]
    total=0
    for regione in regioni:
        querystring = {"q":str(search),"r":str(regione),"t":"s","qso":"false","shp":"false","":"","sort":"datedesc","lim":str(limit_per_page),"start":'0'}
        payload = ""
        headers = {
            "cookie": "",
            "sec-ch-ua": "^\^"
        }
        r = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        data = r.json()
        total=total+len(data["ads"])
        all_data.append(data)
    for data in all_data:
        regione_text=data['filters']['r']
        for annuncio in data['ads']:
            obj = ["","","","-100",""]
            flag=False
            #PARAMETRI: titolo dell'annuncio, verifica che non contenga parole escluse e contenga ricerca
            subject=annuncio['subject']
            for excl_word in excluded_words:
                if subject.find(excl_word) != -1:
                    flag=True
            if contain_check:
                flag_contain=True
                for piece in search.split():
                    if subject.find(piece) != -1:
                        flag_contain=False
                if flag_contain:
                    flag=True
            if flag:
                continue
            obj[0]=subject
            #PARAMETRI: regione
            obj[1]=regione_text
            #PARAMETRI: data pubblicazione annuncio
            obj[2]=annuncio['dates']['display']
            #PARAMETRI: prezzo, controllo che rispetti il range di ragionevolezza
            for feature in annuncio['features']:
                if feature['uri'] == "/price":
                    prezzo=str(feature['values'][0]['key'])
                    if(int(prezzo)<reasonable_min_price or int(prezzo)>reasonable_max_price) and reasonable_price_check:
                        flag=True
                    else:
                        obj[3]=prezzo
                        sum=sum+int(prezzo)
            #PARAMETRI: URL
            obj[4]=annuncio['urls']['default']

            #controlli finali
            if flag or int(obj[3])<0:
                continue
            if len(res)>=limit and limit_check:
                break;
            res.append(obj)
            self.progressBar.setValue(int(round(j*100/total,0)))
            j=j+1
    avg = sum/len(res)
    df= pd.DataFrame(res, columns = ['Titolo','Regione','Data Pubblicazione','Prezzo', 'URL'])
    return [res,avg]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 630)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 630))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 630))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        MainWindow.setPalette(palette)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1001, 601))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label.setMaximumSize(QtCore.QSize(1000, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.search_textbox = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.search_textbox.setObjectName("search_textbox")
        self.verticalLayout.addWidget(self.search_textbox)
        self.title_filter_checkbox = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.title_filter_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.title_filter_checkbox.setObjectName("title_filter_checkbox")
        self.verticalLayout.addWidget(self.title_filter_checkbox)
        self.label_9 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.region_check_2 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_2.setObjectName("region_check_2")
        self.gridLayout.addWidget(self.region_check_2, 0, 1, 1, 1)
        self.region_check_7 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_7.setObjectName("region_check_7")
        self.gridLayout.addWidget(self.region_check_7, 1, 2, 1, 1)
        self.region_check_12 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_12.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_12.setObjectName("region_check_12")
        self.gridLayout.addWidget(self.region_check_12, 2, 3, 1, 1)
        self.region_check_5 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_5.setObjectName("region_check_5")
        self.gridLayout.addWidget(self.region_check_5, 1, 0, 1, 1)
        self.region_check_1 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_1.setObjectName("region_check_1")
        self.gridLayout.addWidget(self.region_check_1, 0, 0, 1, 1)
        self.region_check_13 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_13.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_13.setObjectName("region_check_13")
        self.gridLayout.addWidget(self.region_check_13, 3, 0, 1, 1)
        self.region_check_10 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_10.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_10.setObjectName("region_check_10")
        self.gridLayout.addWidget(self.region_check_10, 2, 1, 1, 1)
        self.region_check_9 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_9.setObjectName("region_check_9")
        self.gridLayout.addWidget(self.region_check_9, 2, 0, 1, 1)
        self.region_check_4 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_4.setObjectName("region_check_4")
        self.gridLayout.addWidget(self.region_check_4, 0, 3, 1, 1)
        self.region_check_16 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_16.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_16.setObjectName("region_check_16")
        self.gridLayout.addWidget(self.region_check_16, 3, 3, 1, 1)
        self.region_check_15 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_15.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_15.setObjectName("region_check_15")
        self.gridLayout.addWidget(self.region_check_15, 3, 2, 1, 1)
        self.region_check_11 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_11.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_11.setObjectName("region_check_11")
        self.gridLayout.addWidget(self.region_check_11, 2, 2, 1, 1)
        self.region_check_3 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_3.setObjectName("region_check_3")
        self.gridLayout.addWidget(self.region_check_3, 0, 2, 1, 1)
        self.region_check_6 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_6.setObjectName("region_check_6")
        self.gridLayout.addWidget(self.region_check_6, 1, 1, 1, 1)
        self.region_check_14 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_14.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_14.setObjectName("region_check_14")
        self.gridLayout.addWidget(self.region_check_14, 3, 1, 1, 1)
        self.region_check_8 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_8.setObjectName("region_check_8")
        self.gridLayout.addWidget(self.region_check_8, 1, 3, 1, 1)
        self.region_check_17 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_17.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_17.setObjectName("region_check_17")
        self.gridLayout.addWidget(self.region_check_17, 4, 0, 1, 1)
        self.region_check_18 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_18.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_18.setObjectName("region_check_18")
        self.gridLayout.addWidget(self.region_check_18, 4, 1, 1, 1)
        self.region_check_19 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_19.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_19.setObjectName("region_check_19")
        self.gridLayout.addWidget(self.region_check_19, 4, 2, 1, 1)
        self.region_check_20 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.region_check_20.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_check_20.setObjectName("region_check_20")
        self.gridLayout.addWidget(self.region_check_20, 4, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.excluded_words_textbox = QtWidgets.QTextEdit(self.horizontalLayoutWidget_2)
        self.excluded_words_textbox.setObjectName("excluded_words_textbox")
        self.verticalLayout.addWidget(self.excluded_words_textbox)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.price_range_checkbox = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.price_range_checkbox.sizePolicy().hasHeightForWidth())
        self.price_range_checkbox.setSizePolicy(sizePolicy)
        self.price_range_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.price_range_checkbox.setText("")
        self.price_range_checkbox.setObjectName("price_range_checkbox")
        self.horizontalLayout_6.addWidget(self.price_range_checkbox)
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.min_reasonable_price_spinbox = QtWidgets.QSpinBox(self.horizontalLayoutWidget_2)
        self.min_reasonable_price_spinbox.setMaximum(999999999)
        self.min_reasonable_price_spinbox.setProperty("value", 0)
        self.min_reasonable_price_spinbox.setObjectName("min_reasonable_price_spinbox")
        self.horizontalLayout_3.addWidget(self.min_reasonable_price_spinbox)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.max_reasonable_price_spinbox = QtWidgets.QSpinBox(self.horizontalLayoutWidget_2)
        self.max_reasonable_price_spinbox.setMaximum(999999999)
        self.max_reasonable_price_spinbox.setObjectName("max_reasonable_price_spinbox")
        self.horizontalLayout_3.addWidget(self.max_reasonable_price_spinbox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.limit_checkbox = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.limit_checkbox.sizePolicy().hasHeightForWidth())
        self.limit_checkbox.setSizePolicy(sizePolicy)
        self.limit_checkbox.setText("")
        self.limit_checkbox.setObjectName("limit_checkbox")
        self.horizontalLayout.addWidget(self.limit_checkbox)
        self.label_6 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.lim_spinbox = QtWidgets.QSpinBox(self.horizontalLayoutWidget_2)
        self.lim_spinbox.setMaximum(999999999)
        self.lim_spinbox.setSingleStep(0)
        self.lim_spinbox.setProperty("value", 100)
        self.lim_spinbox.setObjectName("lim_spinbox")
        self.horizontalLayout.addWidget(self.lim_spinbox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem2)
        self.preview_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.preview_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.preview_button.setObjectName("preview_button")
        self.verticalLayout.addWidget(self.preview_button)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.filename_textbox = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filename_textbox.sizePolicy().hasHeightForWidth())
        self.filename_textbox.setSizePolicy(sizePolicy)
        self.filename_textbox.setInputMask("")
        self.filename_textbox.setObjectName("filename_textbox")
        self.horizontalLayout_7.addWidget(self.filename_textbox)
        self.csv_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(61, 181, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(100, 255, 75))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(80, 218, 58))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(30, 90, 21))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(40, 121, 28))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(61, 181, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(158, 218, 148))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(61, 181, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(100, 255, 75))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(80, 218, 58))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(30, 90, 21))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(40, 121, 28))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(61, 181, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(158, 218, 148))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(30, 90, 21))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(61, 181, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(100, 255, 75))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(80, 218, 58))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(30, 90, 21))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(40, 121, 28))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(30, 90, 21))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(30, 90, 21))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(61, 181, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(61, 181, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(61, 181, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.csv_button.setPalette(palette)
        self.csv_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.csv_button.setObjectName("csv_button")
        self.horizontalLayout_7.addWidget(self.csv_button)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.progressBar = QtWidgets.QProgressBar(self.horizontalLayoutWidget_2)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem4)
        self.label_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_10.setMaximumSize(QtCore.QSize(1000, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_2.addWidget(self.label_10)
        self.tableWidget = QtWidgets.QTableWidget(self.horizontalLayoutWidget_2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem5 = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.label_8 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        self.average_label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.average_label.setText("")
        self.average_label.setObjectName("average_label")
        self.horizontalLayout_5.addWidget(self.average_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem6 = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.label_7 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.ads_n_label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.ads_n_label.setText("")
        self.ads_n_label.setObjectName("ads_n_label")
        self.horizontalLayout_4.addWidget(self.ads_n_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem7 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Subito scraper"))
        self.label.setText(_translate("MainWindow", "Ricerca"))
        self.title_filter_checkbox.setText(_translate("MainWindow", "Filtro titolo (verifica che la ricerca sia effettivamente contenuta nel titolo dell\'annuncio)"))
        self.label_9.setText(_translate("MainWindow", "Regioni"))
        self.region_check_2.setText(_translate("MainWindow", "Piemonte"))
        self.region_check_7.setText(_translate("MainWindow", "Friuli-Venezia Giulia"))
        self.region_check_12.setText(_translate("MainWindow", "Marche"))
        self.region_check_5.setText(_translate("MainWindow", "Trentino-Alto Adige"))
        self.region_check_1.setText(_translate("MainWindow", "Valle d\'Aosta"))
        self.region_check_13.setText(_translate("MainWindow", "Abruzzo"))
        self.region_check_10.setText(_translate("MainWindow", "Umbria"))
        self.region_check_9.setText(_translate("MainWindow", "Toscana"))
        self.region_check_4.setText(_translate("MainWindow", "Lombardia"))
        self.region_check_16.setText(_translate("MainWindow", "Puglia"))
        self.region_check_15.setText(_translate("MainWindow", "Campania"))
        self.region_check_11.setText(_translate("MainWindow", "Lazio"))
        self.region_check_3.setText(_translate("MainWindow", "Liguria"))
        self.region_check_6.setText(_translate("MainWindow", "Veneto"))
        self.region_check_14.setText(_translate("MainWindow", "Molise"))
        self.region_check_8.setText(_translate("MainWindow", "Emilia-Romagna"))
        self.region_check_17.setText(_translate("MainWindow", "Basilicata"))
        self.region_check_18.setText(_translate("MainWindow", "Calabria"))
        self.region_check_19.setText(_translate("MainWindow", "Sardegna"))
        self.region_check_20.setText(_translate("MainWindow", "Sicilia"))
        self.label_2.setText(_translate("MainWindow", "Parole escluse (andare a capo per ogni parola)"))
        self.label_5.setText(_translate("MainWindow", "Range prezzo ragionevole"))
        self.label_3.setText(_translate("MainWindow", "Minimo"))
        self.label_4.setText(_translate("MainWindow", "Massimo"))
        self.label_6.setText(_translate("MainWindow", "Limite numero massimo annunci:"))
        self.preview_button.setText(_translate("MainWindow", "Anteprima"))
        self.filename_textbox.setPlaceholderText(_translate("MainWindow", "nome del file"))
        self.csv_button.setText(_translate("MainWindow", "Genera CSV"))
        self.label_10.setText(_translate("MainWindow", "Anteprima"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Titolo"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Regione"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Data"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Prezzo"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Link"))
        self.label_8.setText(_translate("MainWindow", "Prezzo medio:"))
        self.label_7.setText(_translate("MainWindow", "Numero annunci:"))
        #button connections
        self.preview_button.clicked.connect(self.on_preview_click)
        self.csv_button.clicked.connect(self.on_csv_click)
    def on_preview_click(self):
        #initialization -----------------------
        self.progressBar.setValue(0)
        regioni=[]
        filename=""
        search=""
        excluded_words=[]
        limit=0
        limit_per_page=10000
        reasonable_min_price=0
        reasonable_max_price=0
        contain_check=False
        limit_check=False
        reasonable_price_check=False
        #get data from UI ---------------------
        search=self.search_textbox.text()
        contain_check = self.title_filter_checkbox.isChecked()
        region_checks = [self.region_check_1.isChecked(),self.region_check_2.isChecked(),self.region_check_3.isChecked(),self.region_check_4.isChecked(),self.region_check_5.isChecked(),self.region_check_6.isChecked(),self.region_check_7.isChecked(),self.region_check_8.isChecked(),self.region_check_9.isChecked(),self.region_check_10.isChecked(),self.region_check_11.isChecked(),self.region_check_12.isChecked(),self.region_check_13.isChecked(),self.region_check_14.isChecked(),self.region_check_15.isChecked(),self.region_check_16.isChecked(),self.region_check_17.isChecked(),self.region_check_18.isChecked(),self.region_check_19.isChecked(),self.region_check_20.isChecked()]
        i=1
        for check in region_checks:
            if check:
                regioni.append(i)
            i=i+1
        excluded_words =  self.excluded_words_textbox.toPlainText().split()
        reasonable_price_check=self.price_range_checkbox.isChecked()
        limit_check=self.limit_checkbox.isChecked()
        limit=self.lim_spinbox.value()
        reasonable_min_price=self.min_reasonable_price_spinbox.value()
        reasonable_max_price=self.max_reasonable_price_spinbox.value()
        
        #--------------------------------------
        ret=generatePreview(self,regioni,search,excluded_words,limit,limit_per_page,reasonable_min_price,reasonable_max_price,contain_check,limit_check,reasonable_price_check)
        
        results = ret[0]
        avg=ret[1]
        row=0
        self.tableWidget.setRowCount(len(results))
        for res in results:
            self.tableWidget.setItem(row,0,QtWidgets.QTableWidgetItem(res[0]))
            self.tableWidget.setItem(row,1,QtWidgets.QTableWidgetItem(res[1]))
            self.tableWidget.setItem(row,2,QtWidgets.QTableWidgetItem(res[2]))
            self.tableWidget.setItem(row,3,QtWidgets.QTableWidgetItem(res[3]))
            self.tableWidget.setItem(row,4,QtWidgets.QTableWidgetItem(res[4]))
            row=row+1

        self.average_label.setText("{:.2f}".format(avg))
        self.ads_n_label.setText(str(len(results)))
        self.progressBar.setValue(100)

    def on_csv_click(self):
        #initialization -----------------------
        self.progressBar.setValue(0)
        regioni=[]
        filename=""
        search=""
        excluded_words=[]
        limit=0
        limit_per_page=10000
        reasonable_min_price=0
        reasonable_max_price=0
        contain_check=False
        limit_check=False
        reasonable_price_check=False
        #get data from UI ---------------------
        search=self.search_textbox.text()
        contain_check = self.title_filter_checkbox.isChecked()
        region_checks = [self.region_check_1.isChecked(),self.region_check_2.isChecked(),self.region_check_3.isChecked(),self.region_check_4.isChecked(),self.region_check_5.isChecked(),self.region_check_6.isChecked(),self.region_check_7.isChecked(),self.region_check_8.isChecked(),self.region_check_9.isChecked(),self.region_check_10.isChecked(),self.region_check_11.isChecked(),self.region_check_12.isChecked(),self.region_check_13.isChecked(),self.region_check_14.isChecked(),self.region_check_15.isChecked(),self.region_check_16.isChecked(),self.region_check_17.isChecked(),self.region_check_18.isChecked(),self.region_check_19.isChecked(),self.region_check_20.isChecked()]
        i=1
        for check in region_checks:
            if check:
                regioni.append(i)
            i=i+1
        excluded_words =  self.excluded_words_textbox.toPlainText().split()
        reasonable_price_check=self.price_range_checkbox.isChecked()
        limit_check=self.limit_checkbox.isChecked()
        limit=self.lim_spinbox.value()
        reasonable_min_price=self.min_reasonable_price_spinbox.value()
        reasonable_max_price=self.max_reasonable_price_spinbox.value()
        filename=self.filename_textbox.text()
        #--------------------------------------
        generateCSV(self,regioni,filename,search,excluded_words,limit,limit_per_page,reasonable_min_price,reasonable_max_price,contain_check,limit_check,reasonable_price_check)
        self.progressBar.setValue(100)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
