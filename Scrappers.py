#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures


timeOutDict={
    "site1":0,
    "site2":0,
    "site4":0,
    "site5":0,
    "site6":0,
    "site7":0,
    "site8":0,
    "site9":0,
    "site10":0,
    "site11":0,
    "site12":0,
    "site13":0,
    "site14":0,
    "site15":0,
    "site16":0,
    "site17":0,
    "site18":0,
    "site19":0,
    "site20":0,
    "site21":0,
    
    }
def threadDownloader(site,fn,url):
    try:
        if(timeOutDict[site]<11):
            res=urlopen(url+"/"+fn,timeout = 10)
            fn1=fn
            fn=fn.replace("\\","-")
            fn=fn.replace('/',"-")
            file=open(site+"/"+fn,"wb+")
            file.write(res.read())
            file.close()
            return url+fn
    except Exception as e:
        if(e.__str__()):
            timeOutDict[site]=timeOutDict[site]+1
        print(e)
def threadDownloaderWithSession(site,fn,url,session):
    try:
        if(timeOutDict[site]<11):
            res=session.get(url+"/"+fn,verify=False,timeout = 4)
            fn1=fn
            fn=fn.replace("\\","-")
            fn=fn.replace('/',"-")
            file=open(site+"/"+fn,"wb+")
            file.write(res.content)
            file.close()
            print(url+"/"+fn1)
            return url+fn
    except Exception as e:
        if(e.__str__()):
            timeOutDict[site]=timeOutDict[site]+1
        print(e)


def site1Scrapper():
    url1="http://prices.shufersal.co.il/"
    try:
        page = requests.get(url1,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    soup=BeautifulSoup(page.text,'html.parser')
    table=soup.find("table")
    td=table.findAll('td')
    n=1
    for t in td:
        if(t.find("a") is not None):
            try:
                url=t.find('a')["href"]
                if("http" in url):
                    print(url)
                    r = requests.get(url)            
                    try:
                        n=n+1
                        with open("site1/file"+n.__str__()+".gz", 'wb') as f:
                            f.write(r.content)
                    except exception as e:
                        print(e)
            except:
                pass
    

def site2Scrapper():
    date=datetime.today().strftime('%Y-%m-%d')
    date=date.replace("-","")
    url="http://publishprice.mega.co.il/"+date
    try:
        page = requests.get(url,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    soup=BeautifulSoup(page.text,'html.parser')
    table=soup.find("table")
    td=table.findAll('td')
    n=1
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for t in td:
            if(t.find("a") is not None):
                s=t.text
                tempUrl = ""
                try:
                    if(".gz" in s and "promo" not in s.lower()):
                        if ("http" in s):
                            tempUrl = s
                            n=n+1
                            executor.submit(threadDownloader, "site2","",tempUrl)
                            print(n.__str__())
                        else:
                            n=n+1
                            executor.submit(threadDownloader, "site2",s,url)
                            print(n.__str__())
                except Exception as e:
                    print(e)


def site4Scrapper():
    date=datetime.today().strftime('%Y-%m-%d')
    date=date.replace("-","")
    url = "https://url.publishedprices.co.il/login/user"
    payload='username=doralon&password=&Submit=Sign%2Bin'
    url2 = "https://url.publishedprices.co.il/file/ajax_dir"
    payload2="sEcho=1&iColumns=5&sColumns=%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=100000&mDataProp_0=fname&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=type&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=false&mDataProp_2=size&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=ftime&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=false&sSearch=&bRegex=false&iSortingCols=0&cd=%2F"
    s = requests.Session()
    try:
        res = s.post(url,payload,timeout = 10)
        res2 = s.post(url2,payload2,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    j = json.loads(res2.text)
    print(json.dumps(j,indent=3))
    aaData=j["aaData"]
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for data in aaData:
            try:
                print(data["fname"])
                if("promo" not in data["fname"].lower() and date in data["fname"]):
                    n=n+1
                    executor.submit(threadDownloaderWithSession,"site3",data["fname"],"https://url.publishedprices.co.il/file/d/",s)
                    print(n.__str__()+"  files downloaded")
            except Exception as e:
                print(e)

site4Scrapper()           
        
def site5Scrapper():
    url = "http://matrixcatalog.co.il/NBCompetitionRegulations.aspx"
    urlD="http://matrixcatalog.co.il/"
    s=requests.Session()
    try:
        res = s.get(url,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    soup=BeautifulSoup(res.text,'html.parser')
    tr = soup.findAll('tr')
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for data in tr:
            try:
                d = data.findAll("td")
                if(len(d)>0 ):
                    n=n+1
                    s=d[7].find("a")["href"]
                    if("Promo" not in s):
                        n=n+1
                        executor.submit(threadDownloader, "site4",s,urlD)
                        print(n.__str__()+"  files downloaded")
            except Exception as e:
                print(e)

def site6Scrapper():
    date=datetime.today().strftime('%Y-%m-%d')
    date=date.replace("-","")
    url="http://publishprice.mega-market.co.il/"+date+"/"
    try:
        page = requests.get(url,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    soup=BeautifulSoup(page.text,'html.parser')
    table=soup.find("table")
    td=table.findAll('td')
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for t in td:
            try:
                if(t.find("a") is not None):
                    s=t.text
                    if("Promo" not in s):
                        if("gz" in s):
                            n=n+1
                            executor.submit(threadDownloader,"site5",s,url)
                            print(n.__str__()+"  files downloaded")
            except Exception as e:
                        print(e)


def site7Scrapper():
    url="http://141.226.222.202/"
    try:
        page = requests.get(url,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    soup=BeautifulSoup(page.text,'html.parser')
    table=soup.find("table")
    tr=table.findAll('tr')
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for t in tr:
            td=t.findAll("td")
            if "ברכל" in td[1] or "נתיב החסד" in td[1]:
                file=td[7].find("a")["href"]
                if("Promo" not in file):
                    n=n+1
                    try:                
                        executor.submit(threadDownloader,"site6",file,url)
                        print(n.__str__()+"  files downloaded")
                    except Exception as e:
                        print(e)
        


def site8Scrapper():
    date=datetime.today().strftime('%d/%m/%Y')
    url="http://matrixcatalog.co.il/NBCompetitionRegulations.aspx/"
    urlD="http://matrixcatalog.co.il/"
    try:
        page = requests.get(url,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    soup=BeautifulSoup(page.text,'html.parser')
    table=soup.find("table")
    tr=table.findAll('tr')
    n=1
    futures=[]
    file=""
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for t in tr:
            td=t.findAll("td")
            if(len(td)>6):
                if date in td[6].text:
                    if "קואופ שופ" in td[1] or "מחסני השוק" in td[1] or "ויקטורי" in td[1] or "סופר ברקת" in td[1]:
                        file=td[7].find("a")["href"]
                        n=n+1
                try:
                    futures.append(executor.submit(threadDownloader, "site7",file,urlD))
                    print(n.__str__()+"  files downloaded")
                except Exception as e:
                    print(e)


def site9Scrapper():
    date=datetime.today().strftime('%d/%m/%Y')
    print(date)
    url="https://www.kingstore.co.il/Food_Law/MainIO_Hok.aspx?_=1616004697415&WStore=&WDate=&WFileType=0"
    urlD="https://www.kingstore.co.il/Food_Law/Download/"
    try:
        page = requests.get(url,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    jsn=json.loads(page.text)
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for element in jsn:
            if(date in element["DateFile"]):
                try:
                    #if("קינג סטור" in element["Store"]):
                    if("promo" not in element["FileNm"].lower()):
                        file=element["FileNm"]
                        n=n+1
                        executor.submit(threadDownloader, "site8",file,urlD)
                        print(n.__str__()+"  files downloaded")
                except Exception as e:
                    print(e)
def site10Scrapper():
    date=datetime.today().strftime('%d/%m/%Y')
    print(date)
    url="http://maayan2000.binaprojects.com/MainIO_Hok.aspx?_=1616008448484&WStore=&WDate=&WFileType=0"
    urlD="http://maayan2000.binaprojects.com/Download/"
    try:
        page = requests.get(url,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    jsn=json.loads(page.text)
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for element in jsn:
            if(date in element["DateFile"]):
                try:
                    if("promo" not in element["FileNm"].lower()):
                        file=element["FileNm"]
                        n=n+1
                        executor.submit(threadDownloader, "site9",file,urlD)
                        print(n.__str__()+"  files downloaded")
                except Exception as e:
                    print(e)
def site11Scrapper():
    date=datetime.today().strftime('%d/%m/%Y')
    print(date)
    url="http://zolvebegadol.binaprojects.com/MainIO_Hok.aspx?_=1616169178349&WStore=&WDate=&WFileType=0"
    urlD="http://zolvebegadol.binaprojects.com/Download/"
    try:
        page = requests.get(url,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    jsn=json.loads(page.text)
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for element in jsn:
            if(date in element["DateFile"]):
                try:
                    if("promo" not in element["FileNm"].lower()):
                        file=element["FileNm"]
                        n=n+1
                        executor.submit(threadDownloader,"site10",file,urlD)
                        print(n.__str__()+"  files downloaded")
                except Exception as e:
                    print(e)

def site12Scrapper():
    url = "https://url.publishedprices.co.il/login/user"
    payload='username=TivTaam&password=&Submit=Sign%2Bin'
    url2 = "https://url.publishedprices.co.il/file/ajax_dir"
    payload2="sEcho=1&iColumns=5&sColumns=%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=100000&mDataProp_0=fname&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=type&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=false&mDataProp_2=size&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=ftime&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=false&sSearch=&bRegex=false&iSortingCols=0&cd=%2F"
    s = requests.Session()
    try:
        res = s.post(url,payload,timeout = 10)
        res2 = s.post(url2,payload2,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    j = json.loads(res2.text)
    print("got response")
    aaData=j["aaData"]
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for data in aaData:
            try:
                if("promo" not in data["fname"].lower()):
                    n=n+1
                    executor.submit(threadDownloaderWithSession,"site11",data["fname"],"https://url.publishedprices.co.il/file/d",s)
                    print(n.__str__()+"  files downloaded")
            except Exception as e:
                print(e)

def site13Scrapper():
    url = "https://url.publishedprices.co.il/login/user"
    payload='username=HaziHinam&password=&Submit=Sign%2Bin'
    url2 = "https://url.publishedprices.co.il/file/ajax_dir"
    payload2="sEcho=1&iColumns=5&sColumns=%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=100000&mDataProp_0=fname&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=type&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=false&mDataProp_2=size&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=ftime&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=false&sSearch=&bRegex=false&iSortingCols=0&cd=%2F"
    s = requests.Session()
    try:
        res = s.post(url,payload,timeout = 10)
        res2 = s.post(url2,payload2,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    j = json.loads(res2.text)
    print("got response")
    aaData=j["aaData"]
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for data in aaData:
            try:
                if("promo" not in data["fname"].lower()):
                    n=n+1
                    executor.submit(threadDownloaderWithSession,"site12",data["fname"],"https://url.publishedprices.co.il/file/d/",s)
                    print(n.__str__()+"  files downloaded")
            except Exception as e:
                print(e)

def site14Scrapper():
    url = "https://url.retail.publishedprices.co.il/login/user"
    payload='username=yohananof&password=&Submit=Sign%2Bin'
    url2 = "https://url.retail.publishedprices.co.il/file/ajax_dir"
    payload2="sEcho=1&iColumns=5&sColumns=%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=100000&mDataProp_0=fname&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=type&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=false&mDataProp_2=size&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=ftime&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=false&sSearch=&bRegex=false&iSortingCols=0&cd=%2F"
    s = requests.Session()
    try:
        res = s.post(url,payload,verify=False,timeout = 10)
        res2 = s.post(url2,payload2,verify=False,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    j = json.loads(res2.text)
    print("got response")
    aaData=j["aaData"]	
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for data in aaData:
            try:
                if("promo" not in data["fname"].lower()):
                    n=n+1
                    executor.submit(threadDownloaderWithSession, "site13",data["fname"],"https://url.retail.publishedprices.co.il/file/d/",s)
                    print(n.__str__()+"  files downloaded")
            except Exception as e:
                print(e)


def site15Scrapper():
    url = "https://url.publishedprices.co.il/login/user"
    payload='username=osherad&password=&Submit=Sign%2Bin'
    url2 = "https://url.publishedprices.co.il/file/ajax_dir"
    payload2="sEcho=1&iColumns=5&sColumns=%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=100000&mDataProp_0=fname&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=type&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=false&mDataProp_2=size&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=ftime&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=false&sSearch=&bRegex=false&iSortingCols=0&cd=%2F"
    s = requests.Session()
    try:
        res = s.post(url,payload,timeout = 5)
        res2 = s.post(url2,payload2,timeout = 5)
    except Exception as e:
        print("Server timed out in intital request")
        return
    j = json.loads(res2.text)
    print("got response")
    aaData=j["aaData"]	
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for data in aaData:
            try:
                if("promo" not in data["fname"].lower()):
                    n=n+1
                    executor.submit(threadDownloaderWithSession,"site14",data["fname"],"https://url.publishedprices.co.il/file/d/",s)
                    print(n.__str__()+"  files downloaded")
            except Exception as e:
                print(e)


def site16Scrapper():
    url = "https://url.retail.publishedprices.co.il/login/user"
    payload='username=Retalix&password=12345&Submit=Sign%2Bin'
    url2 = "https://url.retail.publishedprices.co.il/file/ajax_dir"
    payload1="sEcho=2&iColumns=5&sColumns=%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=50&mDataProp_0=fname&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=type&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=false&mDataProp_2=size&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=ftime&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=false&sSearch=&bRegex=false&iSortingCols=0&cd=%2FSalachDabach"
    payload2="sEcho=2&iColumns=5&sColumns=%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=50&mDataProp_0=fname&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=type&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=false&mDataProp_2=size&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=ftime&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=false&sSearch=&bRegex=false&iSortingCols=0&cd=%2FSuperCofix"
    s = requests.Session()
    try:
        res = s.post(url,payload,verify=False,timeout = 10)
        res2 = s.post(url2,payload1,verify=False,timeout = 10)
        res3 = s.post(url2,payload2,verify=False,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    j = json.loads(res2.text)
    j2=json.loads(res3.text)
    print("got response")
    aaData=j["aaData"]
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for data in aaData:
            try:
                if("promo" not in data["fname"].lower()):
                    n=n+1
                    executor.submit(threadDownloaderWithSession, "site15",data["fname"],"https://url.retail.publishedprices.co.il/file/d/SalachDabach/",s)
                    print(n.__str__()+"  files downloaded")
            except Exception as e:
                print(e)


def site17Scrapper():
    url = "https://url.retail.publishedprices.co.il/login/user"
    payload='username=Stop_Market&password=&Submit=Sign%2Bin'
    url2 = "https://url.retail.publishedprices.co.il/file/ajax_dir"
    payload2="sEcho=1&iColumns=5&sColumns=%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=100000&mDataProp_0=fname&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=type&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=false&mDataProp_2=size&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=ftime&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=false&sSearch=&bRegex=false&iSortingCols=0&cd=%2F"
    s = requests.Session()
    try:
        res = s.post(url,payload,verify=False,timeout = 10)
        res2 = s.post(url2,payload2,verify=False,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    j = json.loads(res2.text)
    print("got response")
    aaData=j["aaData"]	
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for data in aaData:
            try:
                if("promo" not in data["fname"].lower() and "NULL" not in data["fname"]):
                    n=n+1
                    print("https://url.retail.publishedprices.co.il/file/d/SalachDabach/"+data["fname"])
                    executor.submit(threadDownloaderWithSession,"site16",data["fname"],"https://url.retail.publishedprices.co.il/file/d/",s)
                    print(n.__str__()+"  files downloaded")
            except Exception as e:
                print(e)


def site18Scrapper():
    url = "https://url.retail.publishedprices.co.il/login/user"
    payload='username=freshmarket&password=&Submit=Sign%2Bin'
    url2 = "https://url.retail.publishedprices.co.il/file/ajax_dir"
    payload2="sEcho=1&iColumns=5&sColumns=%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=100000&mDataProp_0=fname&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=type&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=false&mDataProp_2=size&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=ftime&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=false&sSearch=&bRegex=false&iSortingCols=0&cd=%2F"
    s = requests.Session()
    try:
        res = s.post(url,payload,verify=False,timeout = 10)
        res2 = s.post(url2,payload2,verify=False,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    j = json.loads(res2.text)
    print("got response")
    aaData=j["aaData"]
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for data in aaData:
            try:
                if("promo" not in data["fname"].lower()):
                    n=n+1
                    executor.submit(threadDownloaderWithSession, "site17",data["fname"],"https://url.retail.publishedprices.co.il/file/d/",s)
                    print(n.__str__()+"  files downloaded")
            except Exception as e:
                print(e)

def site19Scrapper():
    url = "https://url.retail.publishedprices.co.il/login/user"
    payload='username=keshet&password=&Submit=Sign%2Bin'
    url2 = "https://url.retail.publishedprices.co.il/file/ajax_dir"
    payload2="sEcho=1&iColumns=5&sColumns=%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=100000&mDataProp_0=fname&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=type&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=false&mDataProp_2=size&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=ftime&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=false&sSearch=&bRegex=false&iSortingCols=0&cd=%2F"
    s = requests.Session()
    try:
        res = s.post(url,payload,verify=False,timeout = 10)
        res2 = s.post(url2,payload2,verify=False,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    j = json.loads(res2.text)
    print("got response")
    aaData=j["aaData"]
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for data in aaData:
            try:
                if("promo" not in data["fname"].lower()):
                    n=n+1
                    executor.submit(threadDownloaderWithSession, "site18",data["fname"],"https://url.retail.publishedprices.co.il/file/d/",s)
                    print(n.__str__()+"  files downloaded")
            except Exception as e:
                print(e)

def site20Scrapper():
    url = "https://url.retail.publishedprices.co.il/login/user"
    payload='username=RamiLevi&password=&Submit=Sign%2Bin'
    url2 = "https://url.retail.publishedprices.co.il/file/ajax_dir"
    payload2="sEcho=1&iColumns=5&sColumns=%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=100000&mDataProp_0=fname&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=type&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=false&mDataProp_2=size&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=ftime&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=false&sSearch=&bRegex=false&iSortingCols=0&cd=%2F"
    s = requests.Session()
    try:
        res = s.post(url,payload,verify=False,timeout = 10)
        res2 = s.post(url2,payload2,verify=False,timeout = 10)
    except Exception as e:
        print("Server timed out in intital request")
        return
    print(res2.status_code)
    try:
        j = json.loads(res2.text)
    except Exception as e:
        pass
    print("got response")
    aaData=j["aaData"]
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for data in aaData:
            try:
                if("promo" not in data["fname"].lower()):
                    n=n+1
                    executor.submit(threadDownloaderWithSession,"site19",data["fname"],"https://url.retail.publishedprices.co.il/file/d/",s)
                    print(n.__str__()+"  files downloaded")
            except Exception as e:
                print(json.dumps(data,indent=3))
                print(e)


def site21Scrapper():
    date=datetime.today().strftime('%d/%m/%Y')
    print(date)
    url="http://shuk-hayir.binaprojects.com/MainIO_Hok.aspx?_=1616575705403&WStore=&WDate=&WFileType="
    urlD="http://shuk-hayir.binaprojects.com/Download/"
    try:
        page = requests.get(url,timeout = 5)
    except Exception as e:
        print("Server timed out in intital request")
        return
    jsn=json.loads(page.text)
    n=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor:
        for element in jsn:
            if(date in element["DateFile"]):
                try:
                    if("promo" not in element["FileNm"].lower()):
                        executor.submit(threadDownloader, "site20",element["FileNm"],urlD)
                        n=n+1
                        print(n.__str__()+"  files downloaded")
                except Exception as e:
                    print(e)
