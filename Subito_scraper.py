import time
import asyncio
import pandas as pd
import requests

res = []
reasonable_min_price=400
reasonable_max_price=1000
contain_check=True

url = "https://www.subito.it/hades/v1/search/items"

start=0
lim=1000
search="iphone 12"
excluded_words=["max", "Max", "cover", "Cover", "Pro", "pro", "PRO", "MAX", "11", "xs", "XS", "13", "8", "6s","mini", "5s", "ipad", "7", "xr","XR","Xr", "samsung","Samsung", "se","SE"]

sum=0
for regione in range (1,21):
    querystring = {"q":str(search),"r":str(regione),"t":"s","qso":"false","shp":"false","":"","sort":"datedesc","lim":str(lim),"start":str(start)}
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
                if(int(prezzo)<reasonable_min_price or int(prezzo)>reasonable_max_price):
                    flag=True
                else:
                    obj[3]=prezzo
                    sum=sum+int(prezzo)
        #PARAMETRI: URL
        obj[4]=annuncio['urls']['default']

        #controlli finali
        if flag or int(obj[3])<0:
            continue
        res.append(obj)
avg = sum/len(res)
print(avg)
df= pd.DataFrame(res, columns = ['Titolo','Regione','Data Pubblicazione','Prezzo', 'URL'])
df.to_csv('iphone12.csv', index=False, sep=';')
print("done")
