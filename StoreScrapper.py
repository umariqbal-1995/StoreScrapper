
import zipfile
from datetime import datetime
import json
import os
import shutil
import gzip, xmltodict, json
import mysql.connector as msql
from mysql.connector import Error
import Scrappers
import Database

import time
# Code to
def getDictFromGz(filename):
    try:
        f = gzip.open(filename, 'rb')
        file_content = f.read()
        f.close()
        content = file_content.decode("UTF-8")
        contentDict = xmltodict.parse(content)
        return contentDict
    except Exception as e:
        zf = zipfile.ZipFile(filename, 'r')
        fList=zf.namelist()
        file=None
        for f in fList:
            if("xml" in f.__str__()):
                file=f
        content=zf.read(file)
        content=content.decode("UTF-8")
        contentDict = xmltodict.parse(content)
        return contentDict

def getJsonStringFromDict(dictObj):
    '''
    input: Python Dict object
    output: encoded json string with indentation
    the output string can be written in a file using binary write mode.
    '''
    json_encoded = json.dumps(dictObj, indent=2, ensure_ascii=False).encode("UTF-8", errors="ignore")
    return json_encoded

#------------------------
sqlStatements=[]


#--------Code to recreate directory structure----

def createDirectoryStructure():
    for i in range(1,21):
        if os.path.exists("site"+i.__str__()):
            pass
        else:
            os.mkdir("site"+i.__str__())

    print("Directory Creation done")
#----------------------------------------------


#----------Delete all files from a folder-----
def deleteFilesRecursively():
    for i in range(1,21):
        try:
            shutil.rmtree(os.path.join(os.path.abspath(os.getcwd()),"site"+i.__str__()))
        except Exception as e:
            print(e)
    print("File Deletion Done")

#------------------

#---------add ata to sql-----
def unitOfQtyReplacer(q):
    f=open("units.csv",'rb')
    s=f.read()
    s=s.decode("utf8")
    s=s.split('\n')
    for st in s:
        arr=st.split(',')
        l=len(arr)
        for i in range(1,l):
            if(arr[i]==q):
                return arr[0]

def cleanSqlandExecute(branchID,chainID,priceUpdateDate,itemCode,itemType, itemName,
               manufacturerName,manufacturerCountry,manufacturerItemDescription,
               unitQty,quantity,bIsWeighted,unitOfMeasure,qtyInPackage,itemPrice,
               unitOfMeasurePrice,allowedDiscount,itemState,site):
    try:
        if(unitQty is not None):
            unitQty=unitOfQtyReplacer(unitQty)
        priceUpdateDate=priceUpdateDate.replace("/","-")
        if(manufacturerItemDescription is None):
            manufacturerItemDescription=""
        itemType=itemType.replace('"',"")
        itemType=itemType.replace('\\',"")
        itemType=itemType.replace('/',"")
        itemType=itemType.replace("'","")
        itemName=itemName.replace('"',"")
        itemName=itemName.replace('\\',"")
        itemName=itemName.replace('/',"")
        itemName=itemName.replace("'","")
        manufacturerName=manufacturerName.replace('"',"")
        manufacturerName=manufacturerName.replace('\\',"")
        manufacturerName=manufacturerName.replace('/',"")
        manufacturerName=manufacturerName.replace("'","")
        manufacturerItemDescription=manufacturerItemDescription.replace('"',"")
        manufacturerItemDescription=manufacturerItemDescription.replace('\\',"")
        manufacturerItemDescription=manufacturerItemDescription.replace('/',"")
        manufacturerItemDescription=manufacturerItemDescription.replace("'","")
        unitQty=unitQty.replace('"',"")
        unitQty=unitQty.replace('\\',"")
        unitQty=unitQty.replace('/',"")
        unitQty=unitQty.replace("'","")
        quantity=quantity.replace('"',"").replace('\\',"").replace('/',"").replace("'","")
        unitOfMeasure=unitOfMeasure.replace('"',"").replace('\\',"").replace('/',"").replace("'","")
        qtyInPackage=qtyInPackage.replace('"',"").replace('\\',"").replace('/',"").replace("'","")
        itemPrice=itemPrice.replace('"',"").replace('\\',"").replace('/',"").replace("'","")
        unitOfMeasurePrice=unitOfMeasurePrice.replace('"',"").replace('\\',"").replace('/',"").replace("'","")
        site=site.replace("site","")
        insertIntoDatabase(branchID,chainID,priceUpdateDate,itemCode,itemType, itemName,
               manufacturerName,manufacturerCountry,manufacturerItemDescription,
               unitQty,quantity,bIsWeighted,unitOfMeasure,qtyInPackage,itemPrice,
               unitOfMeasurePrice,allowedDiscount,itemState,site)
    except Exception as e:
        print(e)
        
    


def insertIntoDatabase(branchID,chainID,priceUpdateDate,itemCode,itemType, itemName,
               manufacturerName,manufacturerCountry,manufacturerItemDescription,
               unitQty,quantity,bIsWeighted,unitOfMeasure,qtyInPackage,itemPrice,
               unitOfMeasurePrice,allowedDiscount,itemState,site):
    try:
        Database.conn=Database.connect()
        manID=Database.getManufacturer(manufacturerName)
        if(manID is None):
            try:
                Database.insertManufacturer(manufacturerName,manufacturerCountry)
            except:
                pass
            manID=Database.getManufacturer(manufacturerName)
        try:
            Database.insertBranch(branchID,site,chainID)
        except:
            pass
        Database.insertProduct(bIsWeighted,itemCode,itemName,itemState,itemType,manufacturerItemDescription,manID,qtyInPackage,quantity,unitOfMeasure,unitQty)  
        print("inserting data")
        Database.insertPrice(itemCode,itemPrice,priceUpdateDate,allowedDiscount,unitOfMeasurePrice,site,branchID)
    except Exception as e:
        print(e)
        time.sleep(100)
      
#-----------------------



def getSqlFromFile():    
    dr=os.listdir()
    for d in dr:
        print(d)
        if(os.path.isdir(d)):
            files=os.listdir(d)
            for f in files:  
                fl=open("log.txt","a+")
                fl.write(d.__str__()+"\n")
                fl.close()
                Jobj=""
                items=""
                try:
                    Jobj=getJsonStringFromDict(getDictFromGz(d+"/"+f))
                    Jobj=json.loads(Jobj)
                    root=None
                    itemName=None
                    Items=None
                    itemsText="Items"
                    itemText="Item"
                    manText="Manufacturer"
                    bIsText="bIs"
                    itemStatusText="ItemStatus"
                    unitOfMeasureText="UnitOfMeasure"
                    if("Root" in Jobj):
                        root="Root"
                    if("root" in Jobj):
                        root="root"
                    if(root is None):
                        itemsText="Products"
                        itemText="Product"
                        root="Prices"
                    if("StoreId" in Jobj[root]):
                        branchID=Jobj[root]["StoreId"]
                        chainID=Jobj[root]["ChainId"]
                    if("StoreID" in Jobj[root]):
                        branchID=Jobj[root]["StoreID"]
                        chainID=Jobj[root]["ChainID"]
                        items=Jobj[root][itemsText]
                    if(itemsText in Jobj[root]):
                        Items=True
                    else:
                        Items=False
                    if(Items is False):
                        if("ItemName" in Jobj[root][itemText]):
                            itemName="ItemName"
                        else:
                            itemName="ItemNm"
                        if("ManufactureName" in items):
                            manText="Manufacture"
                        if("BisWeighted" in items):
                            bIsText="Bis"
                        if("UnitMeasure" in items):
                            unitOfMeasureText="UnitMeasure"
                        if("itemStatus" in items):
                            itemStatusText="itemStatus"
                        cleanSqlandExecute(branchID,chainID,items["PriceUpdateDate"],items["ItemCode"],items["ItemType"], items[itemName],
                                items[manText+"rName"],items["ManufactureCountry"],items[manText+"ItemDescription"],
                                items["UnitQty"],items["Quantity"],items[bIsText+"Weighted"],items[unitOfMeasureText],items["QtyInPackage"],items["ItemPrice"],
                                items["UnitOfMeasurePrice"],items["AllowDiscount"],items[itemStatusText],d.__str__())
                    else:
                        if("@Count" in Jobj[root][itemsText]):
                            if Jobj[root][itemsText]["@Count"] =='0':
                                continue
                        items=Jobj[root][itemsText][itemText]
                        if("ItemName" in items):
                            itemName="ItemName"
                        else:
                            itemName="ItemNm"
                        if("ItemCode" in Jobj[root][itemsText][itemText]):
                            if("ManufactureName" in items):
                                manText="Manufacture"
                            if("BisWeighted" in items):
                                bIsText="Bis"
                            if("UnitMeasure" in items):
                                unitOfMeasureText="UnitMeasure"
                            if("itemStatus" in items):
                                itemStatusText="itemStatus"
                            cleanSqlandExecute(branchID,chainID,items["PriceUpdateDate"],items["ItemCode"],items["ItemType"], items[itemName],
                                items[manText+"Name"],items["ManufactureCountry"],items[manText+"ItemDescription"],
                                items["UnitQty"],items["Quantity"],items[bIsText+"Weighted"],items[unitOfMeasureText],items["QtyInPackage"],items["ItemPrice"],
                                items["UnitOfMeasurePrice"],items["AllowDiscount"],items[itemStatusText],d.__str__())
                        else:
                            i=0
                            for i in items:
                                if("ItemName" in i):
                                    itemName="ItemName"
                                else:
                                    itemName="ItemNm"
                                if("ManufactureName" in i):
                                    manText="Manufacture"
                                if("BisWeighted" in i):
                                    bIsText="Bis"
                                if("UnitMeasure" in i):
                                    unitOfMeasureText="UnitMeasure"
                                if("itemStatus" in i):
                                    itemStatusText="itemStatus"
                                cleanSqlandExecute(branchID,chainID,i["PriceUpdateDate"],i["ItemCode"],i["ItemType"], i[itemName],
                                    i[manText+"Name"],i["ManufactureCountry"],i[manText+"ItemDescription"],
                                    i["UnitQty"],i["Quantity"],i[bIsText+"Weighted"],i[unitOfMeasureText],i["QtyInPackage"],i["ItemPrice"],
                                    i["UnitOfMeasurePrice"],i["AllowDiscount"],i[itemStatusText],d.__str__())
                            
                except Exception as e:
                    print(e.__str__()  +" Exception thrown")
                    
                   
while(True):
    deleteFilesRecursively()
    createDirectoryStructure()
    Scrappers.site1Scrapper()
    Scrappers.site2Scrapper()
    Scrappers.site4Scrapper()
    Scrappers.site5Scrapper()
    Scrappers.site6Scrapper()
    Scrappers.site7Scrapper()
    Scrappers.site8Scrapper()
    Scrappers.site9Scrapper()
    Scrappers.site10Scrapper()
    Scrappers.site11Scrapper()
    Scrappers.site12Scrapper()
    Scrappers.site13Scrapper()
    Scrappers.site14Scrapper()
    Scrappers.site15Scrapper()
    Scrappers.site16Scrapper()
    Scrappers.site17Scrapper()
    Scrappers.site18Scrapper()
    Scrappers.site19Scrapper()
    Scrappers.site20Scrapper()
    Scrappers.site21Scrapper()
    getSqlFromFile()
