#Uncomment last line to test (Generate CSV)

import time
import asyncio
import pandas as pd
import requests

def generateCSV(regioni,filename,search,excluded_words,limit,limit_per_page,reasonable_min_price,reasonable_max_price,contain_check,limit_check,reasonable_price_check):
    url = "https://www.subito.it/hades/v1/search/items"
    res = []
    sum=0
    for regione in regioni:
        querystring = {"q":str(search),"r":str(regione),"t":"s","qso":"false","shp":"false","":"","sort":"datedesc","lim":str(limit_per_page),"start":'0'}
        payload = ""
        headers = {
            "cookie": "",
            "sec-ch-ua": "^\^"
        }
        r = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        data = r.json()
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
    avg = sum/len(res)
    print("prezzo medio: "+ str(avg))
    print("numero elementi: "+str(len(res)))
    df= pd.DataFrame(res, columns = ['Titolo','Regione','Data Pubblicazione','Prezzo', 'URL'])
    df.to_csv(filename+'.csv', index=False, sep=';')
    print(filename+".csv salvato nella directory corrente")


    
def generatePreview(regioni,search,excluded_words,limit,limit_per_page,reasonable_min_price,reasonable_max_price,contain_check,limit_check,reasonable_price_check):
    url = "https://www.subito.it/hades/v1/search/items"
    res = []
    sum=0
    for regione in regioni:
        querystring = {"q":str(search),"r":str(regione),"t":"s","qso":"false","shp":"false","":"","sort":"datedesc","lim":str(limit_per_page),"start":'0'}
        payload = ""
        headers = {
            "cookie": "kppid=9299A9A07B4B742A708E36F9",
            "sec-ch-ua": "^\^"
        }
        r = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        data = r.json()
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
    avg = sum/len(res)
    print("prezzo medio: "+ str(avg))
    print("numero elementi: "+str(len(res)))
    df= pd.DataFrame(res, columns = ['Titolo','Regione','Data Pubblicazione','Prezzo', 'URL'])
    return [res,avg]

def printa(word):
    print(word)
#---------GENERATE PREVIEW PARAMETERS---------
#regioni,search,excluded_words,limit,limit_per_page,reasonable_min_price,reasonable_max_price,contain_check,limit_checkreasonable_price_check

#---------GENERATE CSV PARAMETERS---------
#regioni,filename,search,excluded_words,limit,limit_per_page,reasonable_min_price,reasonable_max_price,contain_check,limit_checkreasonable_price_check
#generateCSV([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],"test","iphone 12",["max", "Max", "cover", "Cover", "Pro", "pro", "PRO", "MAX", "11", "xs", "XS", "13", "8", "6s","mini", "5s", "ipad", "7", "xr","XR","Xr", "samsung","Samsung", "se","SE"],50,1000,400,1000,True,False,True)

